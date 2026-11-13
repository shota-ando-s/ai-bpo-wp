#!/usr/bin/env python3
"""千葉県54市町村の試算の割り当てを計算し、重なりを確かめる（2026-11-13）。

data/area/aichi/_calc.py を元に作り、他県との重なりの扱いは data/area/hokkaido/_calc.py の形（参考表示だけ）にした。
県ページ（/area/chiba/）には試算を入れないので、PLAN は54行。PLAN と STAT は _assign.py の出力
（作り直すときは python3 -B data/area/chiba/_assign.py write）。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

取り決め（2026-11-11 ユーザー決定。data/area/_shutoken/shared.md）:
  **他県の記事・PLAN との重なりは許容し（参考表示だけ）、千葉県の54ページの中だけ月の時間・金額・規模（業種×従業員数）を重ねない**。
  時間の端数（.25 など）は限らない（東海・北関東の「×4 を割った余り」の取り決めは使わない）。
確かめること（NG なら最後の行が NG）:
  1. 54ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）が重ならない。業種×従業員数が重ならない
  2. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  3. 試算の業種（業態）・規模が cases.md・cases2.md・cases_outside.md の事例の会社と同じにならない（CASES と照合）
  4. slug が _brief.md の54市町村と一致する
  5. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
  6. 対象人数は従業員数の6割以下、1人の月の業務量は20〜42時間
  7. 仮の会社の従業員数が、その市町村の民営従業者数・選んだ中分類の従業者数（STAT。経済センサス2021など）を超えない。
     町村（TOWNS）は、中分類の従業者の半分・1所あたりの3倍を超えたら（参考）を出す
  8. 書いた記事（articles/2026-11-12-area-chiba-<slug>.md）があれば、試算の節に PLAN の時間と金額（約◯万円）が出てくる
  （参考）既存の他県の地域ページの試算・他県の _calc.py の PLAN と同じ時間・金額は、件数と市町村を表示するだけ（NG にしない）
使い方: python3 -B data/area/chiba/_calc.py          （末尾に OK / NG を出す）
        python3 -B data/area/chiba/_calc.py free <業種> <最小時間> <最大時間>   （千葉県の中と他県で空いている時間と金額を並べる）
"""
import sys

sys.dont_write_bytecode = True  # 他県の _calc.py を import しても __pycache__ を作らない

import ast  # noqa: E402
import glob  # noqa: E402
import importlib.util  # noqa: E402
import io  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
from collections import Counter  # noqa: E402
from contextlib import redirect_stdout  # noqa: E402
from decimal import Decimal, ROUND_HALF_UP  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ART = os.path.join(ROOT, "articles")
HERE = os.path.dirname(os.path.abspath(__file__))
SELF = "chiba"
PREF_JA = "千葉県"
N_PAGES = 54
ART_GLOB = "2026-1?-??-area-chiba-*.md"

# wages.md の人件費時給（時給①×1.2 を十円単位に丸めた値。記事でも「約◯円」と書く値）。9業種とも入れる（他県の PLAN を読むため）
RATE = {
    "製造業": 3500,
    "卸売業・小売業": 3540,
    "建設業": 3520,
    "運輸業・郵便業": 2980,
    "医療・福祉": 3180,
    "宿泊・飲食サービス業": 2510,
    "不動産・物品賃貸業": 3790,
    "学術研究・専門技術サービス": 4320,
    "情報通信業": 4260,
}
WAGES_MD = set(RATE)

SLUGS = {
    # 市（37）
    "chiba-city", "choshi", "ichikawa-city", "funabashi", "tateyama-city", "kisarazu", "matsudo", "noda-city", "mobara",
    "narita", "sakura-city", "togane", "asahi-city", "narashino", "kashiwa", "katsuura-city", "ichihara", "nagareyama",
    "yachiyo-city", "abiko", "kamogawa", "kamagaya", "kimitsu", "futtsu", "urayasu", "yotsukaido", "sodegaura",
    "yachimata", "inzai", "shiroi", "tomisato", "minamiboso", "sosa", "katori", "sammu", "isumi", "oamishirasato",
    # 町（16）
    "shisui", "sakae-town", "kozaki", "tako", "tonosho-town", "kujukuri", "shibayama", "yokoshibahikari",
    "ichinomiya-town", "mutsuzawa", "shirako", "nagara", "chonan", "otaki-town", "onjuku", "kyonan",
    # 村（1）
    "chosei",
}
TOWNS = {"shisui", "sakae-town", "kozaki", "tako", "tonosho-town", "kujukuri", "shibayama", "yokoshibahikari",
         "ichinomiya-town", "mutsuzawa", "shirako", "nagara", "chonan", "otaki-town", "onjuku", "kyonan", "chosei"}

# cases.md・cases2.md・cases_outside.md（と companies.md の大企業）の会社（2026-11-13）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。分からなければ None〕, AI の事例か〔実証・計画・使用済み・作る側を含む〕)
CASES = [
    # cases.md（数値つき・未使用）
    ("松戸運送（AI式ドライブレコーダー、一般貨物運送、従業員62名。松戸市の補助金の活用事例）", "松戸市",
     {"道路貨物運送", "運送", "一般貨物"}, (62, 62), True),
    ("ノバ・メディクス（居宅介護支援、職員13名。県の介護の事例集 R7）", "君津市", {"居宅介護支援", "ケアプラン", "介護"}, (13, 13), True),
    # cases.md（使用済み・数値なし・計画）
    ("のぞみ会居宅介護支援事業所（職員6名。岡山県和気町で使用済み）", "松戸市", {"居宅介護支援", "ケアプラン", "介護"}, (6, 6), True),
    ("ホテル三日月（ホテル、県の補助金で生成AIの接客を計画）", "木更津市", {"ホテル", "宿泊", "旅館"}, None, True),
    ("吉野機械製作所（プレスブレーキのメーカー、生成AIの保守支援を計画。作る側）", "千葉市", {"生産用機械", "プレスブレーキ", "機械製造"}, None, True),
    ("PITHIAS Technologies（品質管理の AI、計画）", "千葉市", {"ソフトウェア", "品質管理"}, None, True),
    ("ダイヤサービス（ドローンの AI 検知、計画）", "千葉市", {"ドローン"}, None, True),
    ("誠馨会（病院、大きい医療法人）", "千葉市", {"病院"}, None, True),
    ("誠馨会 新東京病院（病院）", "松戸市", {"病院"}, None, True),
    ("亀田IVFクリニック幕張（クリニック）", "千葉市", {"診療所", "クリニック", "不妊治療"}, None, True),
    ("銚子丸（すし、配膳ロボット。本文未読）", "千葉市", {"すし", "飲食チェーン", "回転寿司"}, None, True),
    ("ヒカリシステム（温浴施設の客向けの AI）", "習志野市", {"温浴施設", "娯楽"}, None, True),
    ("リエイ（介護・フードサービス、社内規程Botの試作）", "浦安市", {"介護", "給食", "フードサービス"}, None, True),
    ("大剛運輸（AI の数値なし。他県のデータに記録）", "浦安市", {"道路貨物運送", "運送"}, None, True),
    ("銚子信用金庫（生成AI、金融）", "銚子市", {"信用金庫", "金融"}, None, True),
    ("武井製作所（金属部品加工、切削の AI を計画）", "松戸市", {"金属製品", "金属部品加工", "切削加工"}, None, True),
    ("米屋（和菓子、カメラ＋レーザーの清掃。AI の語なし）", "成田市", {"和菓子", "菓子"}, None, False),
    ("伊藤ハム米久プラント 柏工場（食肉加工、大手）", "柏市", {"食肉加工", "ハム"}, None, True),
    ("千葉薬品（ドラッグストア、見出しのみ）", "所在未確認", {"ドラッグストア", "調剤薬局"}, None, True),
    ("嘉創・協同水産流通（食品加工工場の画像解析、計画）", "所在未確認", {"食品加工", "水産流通"}, None, True),
    ("COMZOW（介護施設の見守り、計画）", "所在未確認", {"見守り", "介護施設"}, None, True),
    ("ライナロジクス（AI 配車、作る側）", "市川市", {"ソフトウェア", "配車システム"}, None, True),
    ("農情人（農業の AI 活用の支援、支援する側）", "船橋市", {"農業支援"}, None, True),
    ("利衛門（農業、使用済み）", "香取市", {"農業", "野菜"}, None, True),
    ("芝山農園ほか（農業、使用済み）", "香取市", {"農業", "かんしょ"}, None, True),
    ("土屋ライスファーム（農業、使用済み）", "東金市", {"農業", "落花生"}, None, True),
    ("ヤマニ果樹農園（果樹、使用済み）", "市川市", {"農業", "果樹"}, None, True),
    # cases.md（AI ではない）
    ("葛西屋商店（呉服小売、6名。AI ではない）", "松戸市", {"呉服", "衣料品小売"}, (6, 6), False),
    ("ハリマ産業（ふすま等の製造、20名。AI ではない）", "松戸市", {"ふすま", "建具", "木製品"}, (20, 20), False),
    ("小金タクシー（タクシー、61名。AI ではない）", "松戸市", {"タクシー", "旅客運送"}, (61, 61), False),
    ("HAYASE（新聞小売、9名。AI ではない）", "松戸市", {"新聞販売"}, (9, 9), False),
    ("柏きらりの風（介護施設、80名。AI の語なし）", "柏市", {"介護施設", "特別養護老人ホーム"}, (80, 80), False),
    ("中郷記念館（介護施設、約90名。AI の語なし）", "木更津市", {"介護施設", "特別養護老人ホーム"}, (90, 90), False),
    ("九十九里ホーム シオン（介護施設、63名。AI の語なし）", "匝瑳市", {"介護施設", "特別養護老人ホーム"}, (63, 63), False),
    ("たすけあい訪問介護センター（訪問介護、8名。AI の語なし）", "香取市", {"訪問介護"}, (8, 8), False),
    # cases2.md
    ("平山建設（建設、社員85名。日本DX大賞2026 の受賞理由）", "成田市", {"建設", "総合工事業", "建築"}, (85, 85), True),
    ("京成タクシーセントラル 習志野営業所（AI ドラレコ、タクシー）", "習志野市", {"タクシー", "旅客運送"}, None, True),
    ("旭福祉会（デイサービス、職員230名。AI ではない）", "旭市", {"通所介護", "デイサービス"}, (230, 230), False),
    ("伊藤ポンプ（管工事、5名。AI ではない）", "旭市", {"管工事", "設備工事"}, (5, 5), False),
    ("うなかみ幼稚園（教職員24名。AI ではない）", "旭市", {"幼稚園"}, (24, 24), False),
    ("charlie（自転車販売・カフェ、2名。AI ではない）", "旭市", {"自転車", "カフェ"}, (2, 2), False),
    ("フルールセゾン（農業、5軒25名。AI ではない）", "旭市", {"農業"}, (25, 25), False),
    ("いすみ市の法人A（農業、自動水管理。AI ではない）", "いすみ市", {"農業"}, None, False),
    ("ハクダイ食品（水産加工とみられる。南房総市・館山市の伴走支援、中身なし）", "所在未確認", {"水産加工"}, None, False),
    ("加瀬建設・三浦建設（建設。南房総市・館山市の支援、AI ではない）", "所在未確認", {"建設", "総合工事業"}, None, False),
    ("谷川自動車（自動車整備。AI ではない）", "所在未確認", {"自動車整備"}, None, False),
    ("小林クリーニング店（AI ではない）", "所在未確認", {"クリーニング"}, None, False),
    # cases_outside.md（県外。本文用1件）
    ("東多摩再資源化事業協同組合（東京都、資源回収、加盟10社・車両109台。AI ドラレコ）", "県外",
     {"資源回収", "運送", "道路貨物運送"}, None, True),
]

# 市町村の民営従業者数と、試算に選んだ中分類の事業所数・従業者数（stats.md の各市町村の節の (B)。経済センサス 2021年6月1日、民営。
# (B) にない中分類は stats.md の「主要産業の裏づけ」〔ec_6_1〕か mfg2025 参考表〔2025年6月1日〕の値。事業所数が分からなければ None）
# slug: (民営従業者, 中分類, 中分類の事業所, 中分類の従業者)
STAT = {
    'chiba-city': (411172, '飲食料品小売業', 1327, 23856),
    'ichihara': (106758, '道路貨物運送業', None, 5433),
    'ichikawa-city': (122660, '倉庫業', 60, 3425),
    'funabashi': (192205, '食料品製造業', 57, 6833),
    'narashino': (57071, '飲食店', 410, 3988),
    'yachiyo-city': (59569, '金属製品製造業', 39, 1197),
    'urayasu': (84448, '鉄鋼業', 48, 1224),
    'matsudo': (131013, '社会保険・社会福祉・介護事業', 703, 13084),
    'noda-city': (55330, '道路貨物運送業', 175, 4636),
    'kashiwa': (147694, '医療業', 716, 12620),
    'nagareyama': (43359, '社会保険・社会福祉・介護事業', 265, 5543),
    'abiko': (27032, '情報サービス業', 49, 1511),
    'kamagaya': (26779, '医療業', 193, 3240),
    'narita': (88154, '運輸に附帯するサービス業', 162, 13142),
    'sakura-city': (51439, '社会保険・社会福祉・介護事業', 216, 4950),
    'yotsukaido': (23012, '社会保険・社会福祉・介護事業', 143, 3052),
    'yachimata': (20712, '食料品製造業', 38, 1208),
    'inzai': (34676, '倉庫業', 14, 1766),
    'shiroi': (19980, '金属製品製造業', 89, 1328),
    'tomisato': (17129, '道路貨物運送業', 55, 1435),
    'shisui': (7705, '織物・衣服・身の回り品小売業', 118, 696),
    'sakae-town': (4688, '飲食料品卸売業', 15, 509),
    'katori': (25146, '飲食店', 284, 1592),
    'kozaki': (1859, '窯業・土石製品製造業', 4, 256),
    'tako': (6832, '食料品製造業', 12, 396),
    'tonosho-town': (3760, '社会保険・社会福祉・介護事業', 25, 551),
    'choshi': (23531, '食料品製造業', 129, 3681),
    'asahi-city': (24752, '食料品製造業', 34, 1013),
    'sosa': (11723, '総合工事業', 114, 657),
    'togane': (23260, '生産用機械器具製造業', 17, 655),
    'sammu': (15291, '家具・装備品製造業', 10, 510),
    'oamishirasato': (9418, '社会保険・社会福祉・介護事業', 80, 1612),
    'kujukuri': (4844, '食料品製造業', 41, 364),
    'shibayama': (8303, '道路貨物運送業', 44, 833),
    'yokoshibahikari': (7067, '総合工事業', 57, 459),
    'mobara': (32716, '社会保険・社会福祉・介護事業', 138, 2659),
    'ichinomiya-town': (3313, '社会保険・社会福祉・介護事業', 28, 717),
    'mutsuzawa': (2066, '社会保険・社会福祉・介護事業', 18, 483),
    'chosei': (4123, '金属製品製造業', 4, 144),
    'shirako': (2838, '宿泊業', 27, 285),
    'nagara': (4303, '道路貨物運送業', 6, 321),
    'chonan': (3293, '生産用機械器具製造業', 6, 356),
    'katsuura-city': (6053, '宿泊業', 55, 591),
    'isumi': (10327, '飲食料品小売業', 93, 983),
    'otaki-town': (4049, '飲食料品小売業', 39, 343),
    'onjuku': (1694, '社会保険・社会福祉・介護事業', 5, 177),
    'tateyama-city': (17839, '飲食店', 315, 1323),
    'kamogawa': (16139, '宿泊業', 73, 1290),
    'minamiboso': (10511, '社会保険・社会福祉・介護事業', 98, 1489),
    'kyonan': (2155, '飲食料品小売業', 37, 304),
    'kisarazu': (52229, '飲食店', 598, 4062),
    'kimitsu': (36721, '技術サービス業（他に分類されないもの）', 72, 2574),
    'futtsu': (16400, '金属製品製造業', 14, 534),
    'sodegaura': (26246, '社会保険・社会福祉・介護事業', 116, 2285),
}

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])（愛知と同じ9列）
# 業種・業態は stats.md の各市町村の「(B) 中小企業の業種の候補」から選んだ。(A) 大企業の工場・施設と読める業種
# （市原市・袖ケ浦市の石油製品・化学、君津市・千葉市中央区の鉄鋼、成田市の航空運輸、浦安市の娯楽業〔テーマパーク〕、
#  茂原市の電子部品・化学、長生村の生産用機械、長柄町の飲料など）は試算の業種にしない。農業・漁業・林業も試算の業種にしない。
PLAN = [
    ('千葉市', 'chiba-city', '卸売業・小売業', '飲食料品の小売（食品スーパーと惣菜の店を数店舗）', {'スーパー', '惣菜', '食料品小売'}, 115,
     '店舗ごとの発注数の下書きと欠品・入荷の連絡、チラシ・売場の案内文、客からの問い合わせへの返信の下書き', 52, 29.75),
    ('市原市', 'ichihara', '運輸業・郵便業', '道路貨物運送と倉庫（建材・工業製品の輸送）', {'道路貨物運送', '倉庫', '運送'}, 97,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録・入出庫の記録の集計', 45, 29.0),
    ('市川市', 'ichikawa-city', '運輸業・郵便業', '倉庫と配送（湾岸の物流拠点で通販・小売の荷物を扱う）', {'配送', '倉庫', '物流センター'}, 120,
     '荷主からの在庫・出荷の問い合わせへの回答と、入出庫の記録・在庫報告の作成、配送業者への手配の連絡', 55, 30.0),
    ('船橋市', 'funabashi', '製造業', '食料品（惣菜・弁当の製造、量販店向け）', {'弁当', '惣菜', '食料品'}, 85,
     '量販店からの規格・原材料・アレルゲンの問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 44, 28.75),
    ('習志野市', 'narashino', '宿泊・飲食サービス業', '飲食店（駅前の居酒屋・定食店を数店舗）', {'居酒屋', '定食', '飲食店'}, 80,
     '予約・宴会の問い合わせへの返信の下書きと、仕入先への発注の連絡、メニュー・求人の文の作成', 48, 32.25),
    ('八千代市', 'yachiyo-city', '製造業', '金属製品（板金・溶接による部品の製造）', {'溶接', '板金', '金属製品'}, 74,
     '取引先からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録・不具合の報告書の取りまとめ', 44, 31.75),
    ('浦安市', 'urayasu', '製造業', '鉄鋼（鋼材の切断・曲げなどの加工、建設・機械向け）', {'鋼材加工', '鋼材', '鉄鋼'}, 40,
     '取引先からの寸法・数量・納期の問い合わせへの回答と、加工の指示書・材料の証明書の整理、出荷の記録の取りまとめ', 18, 31.5),
    ('松戸市', 'matsudo', '医療・福祉', '通所介護（デイサービス）と短期入所', {'通所介護', 'デイサービス', '短期入所'}, 85,
     '利用の記録と個別機能訓練計画書の下書き、家族への連絡帳の文、送迎表の作成', 48, 30.5),
    ('野田市', 'noda-city', '運輸業・郵便業', '道路貨物運送（首都圏の配送と倉庫）', {'道路貨物運送', '運送'}, 102,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計', 52, 30.0),
    ('柏市', 'kashiwa', '医療・福祉', '診療所（整形外科・リハビリの外来、2院）', {'リハビリ', '整形外科', '診療所'}, 80,
     '紹介状・診療情報提供書の下書きと、リハビリの記録の要約、患者への案内文の作成', 48, 31.5),
    ('流山市', 'nagareyama', '医療・福祉', '認可保育所（数園を運営）', {'保育所', '保育'}, 84,
     '保育日誌・連絡帳の下書きと、保護者へのお知らせ文、指導計画の取りまとめ', 50, 30.5),
    ('我孫子市', 'abiko', '情報通信業', '情報サービス（受託のシステム開発・保守）', {'受託開発', '情報サービス', 'システム保守'}, 54,
     '顧客の問い合わせへの一次回答と、仕様書・テスト仕様書・議事録の下書き、作業報告書の作成', 32, 28.25),
    ('鎌ケ谷市', 'kamagaya', '医療・福祉', '訪問看護ステーション（訪問リハビリを含む）', {'訪問看護', '訪問リハビリ'}, 40,
     '訪問の記録の要約と、主治医への報告書・計画書の下書き、利用者・家族への連絡文の作成', 18, 29.0),
    ('成田市', 'narita', '運輸業・郵便業', '運輸に附帯するサービス（国際貨物の取扱い・通関書類の作成、空港周辺の中規模の事業所）', {'貨物取扱', '通関', 'フォワーダー'}, 80,
     '荷主からの貨物の状況・必要書類の問い合わせへの回答と、通関・輸出入の書類の下書き、運送業者・倉庫への手配の連絡', 48, 31.75),
    ('佐倉市', 'sakura-city', '医療・福祉', '特別養護老人ホーム（短期入所を含む）', {'特別養護老人ホーム', '短期入所'}, 123,
     'ケア記録の清書と、入居者の家族への近況の連絡文、委員会の議事録・研修記録の作成', 56, 30.25),
    ('四街道市', 'yotsukaido', '医療・福祉', '障害福祉サービス（就労継続支援と共同生活援助）', {'障害福祉', '就労継続支援', '共同生活援助'}, 45,
     '利用者の支援記録の清書と、個別支援計画の下書き、家族・相談支援専門員への連絡文の作成', 20, 30.0),
    ('八街市', 'yachimata', '製造業', '食料品（豆類・野菜の加工品の製造と卸）', {'豆類加工', '食料品', '農産加工'}, 67,
     '小売店・土産物店からの規格・原材料・賞味期限の問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ', 40, 37.0),
    ('印西市', 'inzai', '運輸業・郵便業', '倉庫（物流施設での入出庫・在庫管理の受託）', {'倉庫', '物流センター', '入出庫'}, 87,
     '荷主からの在庫・出荷予定の問い合わせへの回答と、入出庫・棚卸の記録の集計、作業の指示書の作成', 52, 31.0),
    ('白井市', 'shiroi', '製造業', '金属製品（精密板金・機械部品の加工）', {'機械部品', '金属製品', '精密板金'}, 45,
     '取引先からの図面・納期の問い合わせへの回答と、見積書の作成、検査記録・作業日報の取りまとめ', 20, 30.5),
    ('富里市', 'tomisato', '運輸業・郵便業', '道路貨物運送（青果・食品の冷蔵輸送）', {'冷蔵輸送', '道路貨物運送'}, 40,
     '荷主・市場への到着予定の連絡と、配車表の下書き、温度記録・運転日報の取りまとめ', 15, 30.0),
    ('酒々井町', 'shisui', '卸売業・小売業', '衣料品・服飾雑貨の小売（町内の商業施設などに数店舗）', {'服飾雑貨', '衣料品小売'}, 14,
     '客からの在庫・取り置きの問い合わせへの返信と、商品の説明文・SNSの投稿文、仕入先への発注の連絡', 6, 30.5),
    ('栄町', 'sakae-town', '卸売業・小売業', '飲食料品の卸売（業務用の食品の卸）', {'飲食料品卸売', '食品卸'}, 24,
     '飲食店・小売店からの注文・欠品の問い合わせへの回答と、受注の記録の転記、仕入先への発注の連絡', 13, 31.0),
    ('香取市', 'katori', '宿泊・飲食サービス業', '飲食店（観光客向けの食事処と土産物の販売）', {'食事処', '飲食店', '土産物'}, 43,
     '予約・団体の問い合わせへの返信と、季節の献立・土産物の案内文、外国人客向けの案内の翻訳', 20, 31.25),
    ('神崎町', 'kozaki', '製造業', '窯業・土石（コンクリート製品の製造）', {'窯業・土石', 'コンクリート製品'}, 23,
     '建設会社からの規格・数量・納期の問い合わせへの回答と、製品の検査記録・出荷の記録の取りまとめ', 12, 29.75),
    ('多古町', 'tako', '製造業', '食料品（農産物・鶏卵の加工品の製造）', {'鶏卵加工', '食料品', '農産加工'}, 28,
     '取引先からの原材料・賞味期限・数量の問い合わせへの回答と、商品の表示の文、製造・出荷の記録の取りまとめ', 15, 31.0),
    ('東庄町', 'tonosho-town', '医療・福祉', '通所介護と小規模な入所施設', {'通所介護', '入所施設'}, 24,
     '介護記録の清書と、家族への連絡文、サービスの提供記録・請求の確認の取りまとめ', 14, 29.0),
    ('銚子市', 'choshi', '製造業', '食料品（魚介の加工品の製造と卸）', {'水産加工', '食料品', '魚介加工'}, 77,
     '量販店・問屋からの産地・規格・賞味期限の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 46, 32.0),
    ('旭市', 'asahi-city', '製造業', '食料品（食肉・野菜の加工品の製造）', {'野菜加工', '食料品', '食肉加工品'}, 46,
     '取引先からの規格・原材料・アレルゲンの問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ', 22, 29.0),
    ('匝瑳市', 'sosa', '建設業', '総合工事業（住宅・土木の工事）', {'土木', '住宅工事', '総合工事業'}, 30,
     '工事日報・安全書類の取りまとめと、施主・発注者への工程の連絡文、工事写真の整理', 14, 31.5),
    ('東金市', 'togane', '製造業', '生産用機械（食品・包装機械の部品の加工と組立）', {'機械部品', '生産用機械', '組立'}, 44,
     '取引先からの図面・仕様の問い合わせへの回答と、見積書・組立の記録・検査成績書の取りまとめ', 20, 28.25),
    ('山武市', 'sammu', '製造業', '家具・装備品（店舗の什器・木製家具の製作）', {'家具', '装備品', '什器'}, 38,
     '取引先からの見積・納期・仕様の問い合わせへの回答と、製作の指示書・図面の変更点の連絡、出荷の記録の取りまとめ', 17, 29.0),
    ('大網白里市', 'oamishirasato', '医療・福祉', '訪問介護とサービス付き高齢者向け住宅', {'訪問介護', 'サービス付き高齢者向け住宅'}, 38,
     '訪問の記録の清書と、サービス提供責任者の手順書の下書き、家族・ケアマネジャーへの連絡文の作成', 18, 28.5),
    ('九十九里町', 'kujukuri', '製造業', '食料品（水産物の加工品の製造）', {'水産加工', '食料品'}, 18,
     '取引先・通販の客からの原材料・賞味期限の問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ', 8, 26.75),
    ('芝山町', 'shibayama', '運輸業・郵便業', '道路貨物運送（空港周辺の貨物の地場輸送）', {'空港貨物', '道路貨物運送'}, 33,
     '荷主への集荷・到着の連絡と、配車表の下書き、運転日報・点呼記録の取りまとめ', 16, 28.5),
    ('横芝光町', 'yokoshibahikari', '建設業', '総合工事業（土木・舗装の工事）', {'土木', '舗装', '総合工事業'}, 19,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真・出来形の記録の整理', 8, 32.0),
    ('茂原市', 'mobara', '医療・福祉', '介護老人保健施設（通所リハビリを含む）', {'介護老人保健施設', '通所リハビリ'}, 87,
     'ケア記録・リハビリの記録の要約と、在宅復帰の計画書の下書き、家族への連絡文の作成', 52, 30.5),
    ('一宮町', 'ichinomiya-town', '医療・福祉', '特別養護老人ホーム（町内の中規模の施設）', {'入所介護', '特別養護老人ホーム'}, 30,
     'ケア記録の清書と、家族への近況の連絡文、委員会の議事録の作成', 14, 26.5),
    ('睦沢町', 'mutsuzawa', '医療・福祉', '有料老人ホームとデイサービス', {'有料老人ホーム', 'デイサービス'}, 23,
     '介護記録の清書と、入居・利用の問い合わせへの返信の下書き、家族への連絡文の作成', 12, 27.25),
    ('長生村', 'chosei', '製造業', '金属製品（機械部品・構造物の加工）', {'機械部品', '金属製品'}, 24,
     '取引先からの図面・納期の問い合わせへの回答と、見積書の作成、検査記録・作業日報の取りまとめ', 12, 32.0),
    ('白子町', 'shirako', '宿泊・飲食サービス業', '旅館（合宿・スポーツの団体客）', {'合宿', '旅館'}, 23,
     '団体・合宿の予約の問い合わせへの返信の下書きと、見積書・日程表の作成、館内の案内文の作成', 12, 31.5),
    ('長柄町', 'nagara', '運輸業・郵便業', '道路貨物運送（県内の工場・倉庫の輸送）', {'道路貨物運送', '運送'}, 34,
     '配車表の下書きと、荷主への到着予定の連絡、運転日報・点呼記録の取りまとめ', 16, 27.25),
    ('長南町', 'chonan', '製造業', '生産用機械（機械部品の加工と組立）', {'機械部品', '生産用機械'}, 27,
     '取引先からの図面・仕様の問い合わせへの回答と、作業手順書・検査記録の取りまとめ', 16, 29.0),
    ('勝浦市', 'katsuura-city', '宿泊・飲食サービス業', 'ホテル・旅館（観光・釣りの客）', {'ホテル', '旅館', '宿泊'}, 37,
     '予約サイト・電話・メールの問い合わせへの返信の下書きと、団体の見積書、館内・周辺の案内文の作成', 13, 33.0),
    ('いすみ市', 'isumi', '卸売業・小売業', '飲食料品の小売（地元の食品スーパー）', {'スーパー', '食料品小売'}, 45,
     '仕入先への発注・欠品の連絡と、売場のPOP・チラシの文、客からの問い合わせへの返信の下書き', 20, 29.0),
    ('大多喜町', 'otaki-town', '卸売業・小売業', '飲食料品の小売（地元の食料品店と総菜の販売）', {'総菜', '食料品小売'}, 20,
     '仕入先への発注の連絡と、総菜の表示・案内の文、客からの注文の問い合わせへの返信', 9, 27.0),
    ('御宿町', 'onjuku', '医療・福祉', 'グループホームと小規模なデイサービス', {'グループホーム', 'デイサービス'}, 18,
     '介護記録の清書と、家族への連絡文、運営推進会議の記録の作成', 8, 27.25),
    ('館山市', 'tateyama-city', '宿泊・飲食サービス業', '飲食店（観光客向けの海鮮料理店を数店舗）', {'海鮮料理', '飲食店'}, 50,
     '予約・団体の問い合わせへの返信の下書きと、仕入先への発注の連絡、季節のメニュー・店内の案内文の作成', 26, 30.5),
    ('鴨川市', 'kamogawa', '宿泊・飲食サービス業', '旅館・ホテル（海沿いの観光客と合宿）', {'ホテル', '旅館', '宿泊'}, 79,
     '予約サイト・電話の問い合わせへの返信の下書きと、合宿・団体の見積書、館内の多言語の案内文の作成', 47, 34.0),
    ('南房総市', 'minamiboso', '医療・福祉', '特別養護老人ホームとデイサービス', {'特別養護老人ホーム', 'デイサービス'}, 44,
     'ケア記録・利用の記録の清書と、家族への連絡文、送迎表・委員会の記録の作成', 20, 31.0),
    ('鋸南町', 'kyonan', '卸売業・小売業', '飲食料品の小売（鮮魚・干物の店と通販）', {'食料品小売', '鮮魚小売'}, 19,
     '通販・電話の注文の問い合わせへの返信と、商品の説明文、発送の記録・仕入先への連絡の取りまとめ', 7, 29.0),
    ('木更津市', 'kisarazu', '宿泊・飲食サービス業', '飲食店（郊外のレストランと宴会場を数店舗）', {'宴会', 'レストラン', '飲食店'}, 87,
     '予約・宴会の問い合わせへの返信の下書きと、宴会の見積書・献立の案内文、仕入先への発注の連絡', 52, 28.25),
    ('君津市', 'kimitsu', '学術研究・専門技術サービス', '技術サービス（非破壊検査・計測・設計の受託）', {'非破壊検査', '計測', '技術サービス'}, 60,
     '顧客との打合せの記録の要約と、検査・計測の報告書の下書き、見積書・作業計画書の作成', 23, 23.0),
    ('富津市', 'futtsu', '製造業', '金属製品（鉄骨・鋼構造物の製作）', {'鉄骨', '金属製品', '鋼構造物'}, 43,
     '取引先からの図面変更・納期の問い合わせへの回答と、製作の指示書・検査記録・ミルシートの整理', 20, 31.75),
    ('袖ケ浦市', 'sodegaura', '医療・福祉', '小規模多機能型居宅介護とグループホーム', {'小規模多機能', 'グループホーム'}, 67,
     '利用の記録の清書と、介護計画の下書き、家族・ケアマネジャーへの連絡文の作成', 40, 36.5),
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def plan_hours(n, hrs):
    return Decimal(str(n)) * Decimal(str(hrs)) * Decimal("0.25")


def read_plan_text(src):
    """PLAN を文字列で切り出す（改行のすぐ後ろの「PLAN = [」か「PLAN = {」から行頭の「]」「}」まで）"""
    for op, cl in (("[", "]"), ("{", "}")):
        i = src.find("\nPLAN = " + op)
        if i < 0:
            continue
        start = i + 1
        j = src.index("\n" + cl, start)
        return ast.literal_eval(src[start + len("PLAN = "):j + 2])
    raise ValueError("行頭の PLAN = [ / { がない")


def load_plan(path):
    """他県の _calc.py を import して PLAN を返す（main は __name__ のガードで動かない）。だめなら文字列で読む"""
    pref = os.path.basename(os.path.dirname(path))
    try:
        spec = importlib.util.spec_from_file_location("plan_" + pref.replace("-", "_"), path)
        mod = importlib.util.module_from_spec(spec)
        with redirect_stdout(io.StringIO()):
            spec.loader.exec_module(mod)
        return mod.PLAN
    except Exception:  # noqa: BLE001 import できなければ文字列で読む
        return read_plan_text(open(path, encoding="utf-8").read())


def rows_of(plan):
    """PLAN の行を (市町村, 業種, 対象人数, 業務量) にそろえる。
    list の行（奈良・愛知の9列など）は 名前=r[0]・業種=r[2]・人数=r[-2]・時間=r[-1]。
    dict の行（神奈川: slug → (名前, 業種, 業態, 従業員数, 対象人数, 業務量, 対象業務)）は 人数=v[4]・時間=v[5]"""
    if isinstance(plan, dict):
        for k, v in plan.items():
            yield (v[0], v[1], v[4], v[5])
    else:
        for r in plan:
            yield (r[0], r[2], r[-2], r[-1])


def other_plans():
    """全県の _calc.py の PLAN を読み、(県, 市町村, 削減時間, 万円) を返す。読めないファイルは警告だけ"""
    out, read, warn = [], {}, []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "area", "*", "_calc.py"))):
        pref = os.path.basename(os.path.dirname(path))
        if pref == SELF:
            continue
        try:
            plan = load_plan(path)
        except Exception as e:  # noqa: BLE001
            warn.append(f"{pref} の _calc.py の PLAN が読めない（{type(e).__name__}: {e}）。照合から外した")
            continue
        n_skip = n_rows = 0
        try:
            for city, ind, n, hrs in rows_of(plan):
                n_rows += 1
                if ind not in RATE:
                    n_skip += 1
                    continue
                h = plan_hours(n, hrs)
                out.append((pref, city, h, man(h * RATE[ind])))
        except Exception as e:  # noqa: BLE001
            warn.append(f"{pref} の PLAN の形が読めない（{type(e).__name__}）。照合から外した")
            continue
        if n_skip:
            warn.append(f"{pref} の PLAN に時給の分からない業種・読めない行が {n_skip}行ある")
        read[pref] = n_rows
    return out, read, warn


def existing():
    """既存の地域ページ（千葉県を除く）の「## 試算」の節から、結果の時間・万円を拾う（愛知県の _calc.py と同じ拾い方）。"""
    hours, mans, per_file = {}, {}, {}
    files = [f for f in sorted(glob.glob(os.path.join(ART, "2026-1?-*-area-*.md"))) if f"-area-{SELF}" not in f]
    n_sec = 0
    skip_h_label = re.compile(r"人数|業務量|使う人|人と時間|時間（仮定）|1人|時給|時間単価|1時間あたり")
    skip_m_label = re.compile(r"時給|時間単価|1時間あたり|月額|引|回収|費用|利用料|料金")
    cut_line = re.compile(r"毎月勤労統計|総実労働|かんたんAI|月額|差し引|引いた|引いても|払っても|払った|残り|残ります|初期費用|回収|戻る|取り戻せる")
    for f in files:
        t = open(f, encoding="utf-8").read()
        m = re.search(r"^## 試算.*?(?=^## )", t, re.M | re.S)
        if not m:
            continue
        n_sec += 1
        sec = m.group(0)
        name = os.path.basename(f)
        fh, fm = set(), set()
        for line in sec.splitlines():
            if line.startswith("|"):
                cells = [x.strip() for x in line.strip().strip("|").split("|")]
                if len(cells) < 2 or set(cells[0]) <= set("-: "):
                    continue
                label, val = cells[0], " ".join(cells[1:])
                take_h = not skip_h_label.search(label)
                take_m = not skip_m_label.search(label)
                if re.search(r"減る|削減時間|浮く|減らせる|取り戻す|試算|結果|当社|項目|月の|削減|換算|効果", label):
                    take_h = take_m = True
                if re.match(r"[*約月]*\d", label):
                    val = " ".join(cells)
                    take_h = take_m = True
                if take_h and re.search(r"人数|業務量|使う人|時給", label) and "削減" not in label:
                    take_h = False
            else:
                val = cut_line.split(line)[0]
                take_h = take_m = True
            v = re.sub(r"（[^）]*）|\([^)]*\)", "", val)
            if take_h:
                for x in re.findall(r"([\d,]+(?:\.\d+)?)\s*時間", v):
                    fh.add(Decimal(x.replace(",", "")))
            if take_m:
                for a, b in re.findall(r"(\d+)万([\d,]+)円", v):
                    fm.add((Decimal(a) + Decimal(b.replace(",", "")) / 10000).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
                for x in re.findall(r"([\d,]+(?:\.\d+)?)\s*万円", v):
                    fm.add(Decimal(x.replace(",", "")))
        for x in fh:
            hours.setdefault(x, name)
        for x in fm:
            mans.setdefault(x, name)
        per_file[name] = (len(fh), len(fm))
    return len(files), n_sec, hours, mans, per_file


def used_values():
    """既存の他県の記事と他県の PLAN で使われている時間・万円（_assign.py が「なるべく避ける」ために使う。NG ではない）"""
    _, _, ex_h, ex_m, _ = existing()
    op, _, _ = other_plans()
    return set(ex_h) | {r[2] for r in op}, set(ex_m) | {r[3] for r in op}


def border_ok(yen):
    """四捨五入の境目（◯.◯5万円＝千円の位で500円）から100円より離れているか"""
    return abs(int(yen % 1000) - 500) > 100


def in_range(size, csize):
    lo, hi = csize
    return lo * 0.85 <= size <= hi * 1.15


def case_check(city, sub, keys, size):
    """事例の会社との照合。(NG の文の list, 参考の文の list)"""
    ng, notes = [], []
    for (cname, ccity, ckeys, csize, is_ai) in CASES:
        if not (keys & ckeys):
            continue
        if not is_ai:
            if (csize is not None and in_range(size, csize)) or (csize is None and ccity == city):
                notes.append(f"{city}: 試算（{sub}・{size}名）と業態が近い AI ではない事例 {cname}")
            continue
        if csize is not None and in_range(size, csize):
            ng.append(f"{city} の試算（{sub}・{size}名）が事例 {cname}（{csize[0]}〜{csize[1]}名）に近い")
        elif csize is None and ccity == city:
            ng.append(f"{city} の試算（{sub}）が同じ市町村の事例 {cname}（規模不明）と同じ業態")
        elif ccity in ("所在未確認", "県外"):
            notes.append(f"{city}: 試算（{sub}・{size}名）と業態のキーが重なる{ccity}の事例 {cname}（別の市町村なので NG にしない）")
    return ng, notes


def check_articles():
    """書いた記事の試算の節に、PLAN の時間と金額が出てくるか。(NG の list, 見た記事の数)"""
    ng, n = [], 0
    by_slug = {p[1]: p for p in PLAN}
    for f in sorted(glob.glob(os.path.join(ART, ART_GLOB))):
        slug = re.sub(r"^2026-1\d-\d\d-area-chiba-", "", os.path.basename(f))[:-3]
        p = by_slug.get(slug)
        if p is None:
            continue
        n += 1
        t = open(f, encoding="utf-8").read()
        m = re.search(r"^## 試算.*?(?=^## )", t, re.M | re.S)
        if not m:
            ng.append(f"{os.path.basename(f)} に「## 試算」の節がない")
            continue
        sec = m.group(0).replace(",", "")
        h = plan_hours(p[7], p[8])
        mm = man(h * RATE[p[2]])
        if f"{h.normalize():f}時間" not in sec:
            ng.append(f"{os.path.basename(f)} の試算の節に {h.normalize():f}時間 がない")
        if f"{mm}万円" not in sec:
            ng.append(f"{os.path.basename(f)} の試算の節に 約{mm}万円 がない")
    return ng, n


def main():
    n_files, n_sec, ex_h, ex_m, per_file = existing()
    print(f"既存の他県の地域ページ: {n_files}本（うち試算の節があるもの {n_sec}本）。拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種")
    op, read, warn = other_plans()
    ok = True
    pl_h, pl_m = {}, {}
    for pref, city, h, m in op:
        pl_h.setdefault(h, f"{pref} {city}")
        pl_m.setdefault(m, f"{pref} {city}")
    print(f"他県の PLAN: {len(read)}県 {sum(read.values())}行。時間 {len(pl_h)}種・万円 {len(pl_m)}種")
    for w in warn:
        print("（警告）", w)

    seen_h, seen_m, seen_s = {}, {}, {}
    notes, overlap = [], []
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 |")
    print("|---|---|---|---|---|---|---|")
    for (city, slug, ind, sub, keys, size, task, n, hrs) in PLAN:
        if ind not in WAGES_MD:
            print(f"  NG {city} の業種 {ind} は wages.md にない（農林漁業は試算の業種にしない）")
            ok = False
            continue
        h = plan_hours(n, hrs)
        yen = h * RATE[ind]
        m = man(yen)
        print(f"| {city} | {ind}（{sub}） | {size}名 | {n}名×{hrs}時間×25% | {h.normalize():f}時間 | 約{RATE[ind]:,}円 | 約{m}万円 |")
        if (h * 4) % 1 != 0:
            print(f"  NG {city} の時間が0.25時間刻みでない ({h})")
            ok = False
        ov = []
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 千葉県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                ov.append(f"{label} {key} が既存の記事 {exd[key]}")
            if key in pld:
                ov.append(f"{label} {key} が他県の PLAN（{pld[key]}）")
        if ov:
            overlap.append(f"{city}: " + "、".join(ov))
        if (ind, size) in seen_s:
            print(f"  NG 千葉県の中で業種×規模が重なる: {city} と {seen_s[(ind, size)]} ({ind} {size}名)")
            ok = False
        seen_s[(ind, size)] = city
        if not border_ok(yen):
            print(f"  NG {city} の金額が四捨五入の境目に近い（{yen}円）")
            ok = False
        if n > size * 0.6:
            print(f"  NG {city} の対象人数 {n}名が従業員数 {size}名の6割を超える")
            ok = False
        if not (20 <= hrs <= 42):
            print(f"  NG {city} の1人の月の業務量 {hrs}時間が20〜42時間の外")
            ok = False
        st = STAT.get(slug)
        if st is None:
            print(f"  NG {city} の STAT（民営従業者・中分類）がない")
            ok = False
        else:
            emp, mid, mid_n, mid_emp = st
            if size > emp:
                print(f"  NG {city} の仮の会社（{size}名）が民営従業者 {emp:,}人より大きい")
                ok = False
            if size > mid_emp:
                print(f"  NG {city} の仮の会社（{size}名）が中分類「{mid}」の従業者 {mid_emp:,}人より大きい")
                ok = False
            elif slug in TOWNS and size * 2 > mid_emp:
                notes.append(f"{city}: 仮の会社 {size}名が町村の「{mid}」の従業者 {mid_emp}人の半分を超える")
            if mid_n and slug in TOWNS and size > 3 * mid_emp / mid_n:
                notes.append(f"{city}: 仮の会社 {size}名は町村の「{mid}」の1所あたり {mid_emp / mid_n:.1f}人の3倍を超える")
        cng, cnotes = case_check(city, sub, keys, size)
        for x in cng:
            print("  NG", x)
            ok = False
        notes += cnotes
    slugs = [p[1] for p in PLAN]
    if set(slugs) != SLUGS or len(slugs) != len(set(slugs)):
        print("NG slug が _brief.md と違う:", set(slugs) ^ SLUGS, [s for s, c in Counter(slugs).items() if c > 1])
        ok = False
    if not PLAN:
        print("NG PLAN が空")
        print("NG")
        return
    ang, n_art = check_articles()
    for x in ang:
        print("  NG", x)
        ok = False
    print(f"\n市町村ページ: {len(PLAN)}、市町村名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}。書いた記事の照合: {n_art}本")
    print(f"時間の範囲 {min(seen_h).normalize():f}〜{max(seen_h).normalize():f}時間、金額の範囲 約{min(seen_m)}〜{max(seen_m)}万円、"
          f"規模 {min(p[5] for p in PLAN)}〜{max(p[5] for p in PLAN)}名")
    print(f"（参考）他県の記事・PLAN と時間・金額が同じ: {len(overlap)}市町村（2026-11-11 ユーザー決定で許容。NG にしない）")
    for x in overlap:
        print("（参考・重なり）", x)
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and len(PLAN) == N_PAGES else "NG")


def free(ind, lo, hi):
    """業種 ind で、lo〜hi 時間の、千葉県の中で空いていて他県とも重ならない（時間, 万円）を並べる"""
    h_used, m_used = used_values()
    mine_h = {plan_hours(p[7], p[8]) for p in PLAN}
    mine_m = {man(plan_hours(p[7], p[8]) * RATE[p[2]]) for p in PLAN}
    h = Decimal(str(lo))
    out = []
    while h <= Decimal(str(hi)):
        if h not in h_used and h not in mine_h:
            yen = h * RATE[ind]
            m = man(yen)
            if m not in m_used and m not in mine_m and border_ok(yen):
                out.append(f"{h.normalize():f}h/{m}万")
        h += Decimal("0.25")
    print(f"{ind} {lo}〜{hi}時間の空き {len(out)}件:", " ".join(out))


if __name__ == "__main__":
    if len(sys.argv) >= 5 and sys.argv[1] == "free":
        free(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
    else:
        main()
