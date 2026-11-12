#!/usr/bin/env python3
"""愛知県54市町村の試算の割り当てを計算し、重なりを確かめる（2026-11-11）。

data/area/nara/_calc.py を元に作った（京都・三重の _calc.py と同じ形）。県ページ（/area/aichi/）には試算を入れないので、PLAN は54行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **静岡・愛知・三重・京都の取り決め**: 月の削減時間（0.25時間刻み）×4 を4で割った余りが 1（愛知県）の時間だけを使う
     （端数が .25 の時間。data/area/_tokai/shared.md）
  1. 54ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、愛知県を除く）の「## 試算」の節の「◯時間」「◯万円」と重ならない
  3. 全県の data/area/*/_calc.py の PLAN（愛知県を除く。glob で全部読む。静岡・三重・京都・北海道を含む）の
     月の削減時間・月の時間換算額と重ならない。行頭の「PLAN = [」だけを読む。読めないファイルは警告。
     REQUIRED の県はファイルがなければ NG。**金額が重なったら先に push した府県を優先する**
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md・cases2.md の事例の会社と同じにならない（CASES と照合）
  6. slug が _brief.md の54市町村と一致する
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
  8. 県ページには試算を入れない（PLAN は54行）
  9. 仮の会社の従業員数が、その市町村の民営従業者数・選んだ中分類の従業者数（stats.md の (B)、経済センサス2021）を超えない
使い方: python3 data/area/aichi/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/aichi/_calc.py free 製造業 30 200   （余り1の時間で、既存・他県・愛知の中と重ならない時間と金額の候補を出す）
他県の PLAN は後から変わるので、push の直前に git pull してもう一度実行し、最後の行が OK のときだけ push する。
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
SELF = "aichi"
PREF_JA = "愛知県"
MOD_N, MOD_R = 4, 1  # 静岡・愛知・三重・京都の割り当て（月の削減時間×4 を4で割った余り）。愛知県は 1
N_PAGES = 54

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
    # 市（38）
    "nagoya", "toyohashi", "okazaki", "ichinomiya", "seto", "handa", "kasugai", "toyokawa", "tsushima-city", "hekinan",
    "kariya", "toyota", "anjo", "nishio", "gamagori", "inuyama", "tokoname", "konan-city", "komaki", "inazawa",
    "shinshiro", "tokai-city", "obu", "chita", "chiryu", "owariasahi", "takahama-city", "iwakura", "toyoake", "nisshin",
    "tahara", "aisai", "kiyosu", "kitanagoya", "yatomi", "miyoshi-city", "ama-city", "nagakute",
    # 町（14）
    "togo", "toyoyama", "oguchi", "fuso", "oharu", "kanie", "agui", "higashiura", "minamichita", "mihama-town-aichi",
    "taketoyo", "kota", "shitara", "toei",
    # 村（2）
    "tobishima", "toyone",
}
VILLAGES = {"tobishima", "toyone", "shitara", "toei"}  # 村と奥三河の小さい町（村と同じ参考の判定をする）

# 照合が必須の県（2026-11-11 に _calc.py がある県。静岡・三重・京都を含む）。ファイルがなければ NG。ほかに見つかった _calc.py も全部読む
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima",
            "hokkaido", "ibaraki", "tochigi", "gunma", "okinawa", "wakayama", "shiga", "nara",
            "kyoto", "mie", "shizuoka")

# cases.md・cases_outside.md・subsidy_a_areas.md・companies.md（大企業の工場・AI を作る側）の会社（2026-11-07）
# (会社名, 市町村〔県外は「県外」〕, 業態のキー, 従業員数〔(下限, 上限)。分からなければ None〕, AI の事例か〔実証・使用済み・提供側を含む〕)
# cases2.md ができたら D2 が「# cases2.md」の行に足す
# cases.md の会社（2026-11-11）。cases_outside.md・cases2.md ができたら足す
# (会社名, 市町村〔県外は「県外」〕, 業態のキー, 従業員数〔(下限, 上限)。分からなければ None〕, AI の事例か)
CASES = [
    ("野場電工（生成AIで品質管理の文書・見積、自動車用部品の加工・組立・樹脂成形、270人）", "豊田市",
     {"自動車部品", "輸送用機械", "樹脂成形", "組立"}, (270, 270), True),
    ("名古屋東部陸運（AI-OCR で配車票、本番に至らず。貨物自動車運送、550名）", "豊田市",
     {"道路貨物運送", "運送", "自動車部品輸送"}, (550, 550), True),
    ("えぷろんフーズ（AI-OCR で伝票入力、生鮮食品スーパー6店舗）", "豊田市", {"食品スーパー", "スーパー", "食料品小売"}, None, True),
    ("藤塗装工業（AI-OCR で検収、金属部品の工業塗装、114名）", "碧南市", {"塗装", "金属塗装", "表面処理"}, (114, 114), True),
    ("栄四郎瓦（県のDX補助の採択、瓦の外観検査AI）", "碧南市", {"瓦", "窯業・土石", "粘土瓦"}, None, True),
    ("中埜総合印刷（AI の生産計画を試行、印刷・食酢、265人）", "半田市", {"印刷", "食酢", "調味料"}, (265, 265), True),
    ("神谷ベルト（AI-OCR、ゴム・プラスチックの商社、30人程度）", "名古屋市", {"ゴム製品卸", "商社", "樹脂卸"}, (30, 30), True),
    ("スガキコシステムズ（需要予測AI、飲食チェーン）", "名古屋市", {"飲食チェーン", "ラーメン", "飲食店"}, None, True),
    ("ユーアイ精機（AI-OCR、プレス試作・金型、12人程度。登記は名古屋市守山区）", "尾張旭市", {"金型", "プレス加工", "試作"}, (12, 12), True),
    ("ディヴェロップ（RPA、土木・下水道工事、30人程度。AI ではない）", "岡崎市", {"土木", "総合工事業"}, (30, 30), False),
    ("スチールテック（Gemini を全社で、金型部品の金属加工・商社、47名程度）", "大府市",
     {"金型部品", "金属加工", "金属製品", "鋼材"}, (47, 47), True),
    ("愛厚ホーム大府苑（AI でシフト作成、介護。大きい法人）", "大府市", {"特別養護老人ホーム", "介護"}, None, True),
    ("春日井市民病院（生成AIで退院サマリー、市立病院）", "春日井市", {"病院"}, None, True),
    ("オーテック（保全の生成AIを自社開発、冷間鍛造・切削の自動車部品、80名）", "小牧市",
     {"自動車部品", "冷間鍛造", "切削加工", "精密部品"}, (80, 80), True),
    ("コモ（生成AIの受注の検証、ロングライフパンの製造）", "小牧市", {"パン", "食料品", "菓子"}, None, True),
    ("テルミック（Copilot、金属加工部品）", "刈谷市", {"金属加工", "金属製品", "切削加工"}, None, True),
    ("中部特殊合板（AI で NC プログラム、樹脂・合板の加工・遊技部品）", "北名古屋市", {"合板", "木材加工", "樹脂加工", "遊技部品"}, None, True),
    ("ヤマサちくわ（需要予測AI、水産練り製品）", "豊橋市", {"水産練り製品", "水産加工", "食料品"}, None, True),
    ("ドラッグストアー・カミヤ（店頭の AI 健康支援ツール、調剤薬局）", "豊橋市", {"調剤薬局", "ドラッグストア"}, None, True),
    ("伊藤金属工業（AI 外観検査、自動車部品・ボルトユニオン）", "東浦町", {"自動車部品", "金属製品", "ボルト"}, None, True),
    ("久野金属工業（部署別の生成AI、自動車部品のプレス・金型、352名。登記は名古屋市緑区）", "常滑市",
     {"プレス加工", "金型", "自動車部品"}, (352, 352), True),
    ("PTアイランド（一宮商工会議所の生成AI WG、動画作成）", "一宮市", {"動画制作", "広告"}, None, True),
    ("昌和染工（一宮商工会議所の生成AI WG、染色整理）", "一宮市", {"染色整理", "染色"}, None, True),
    ("川本鋼材（岐阜県富加町で使用済み、鋼材）", "あま市", {"鋼材", "鉄鋼卸"}, None, True),
    # cases2.md（2026-11-11）
    ("山田裕也氏（スプレーギクの農家、15名、農業用生成AI「栽培AI」）", "豊川市", {"農業", "花き", "スプレーギク"}, (15, 15), True),
    ("JA西三河いちご部会（AI 選果の20%は目標）", "西尾市", {"農業", "いちご", "選果"}, None, True),
    ("トクイテン（農場が知多市、農業）", "知多市", {"農業"}, None, True),
    ("バンズヘア（AI の鏡、美容室、1名）", "名古屋市", {"美容室"}, (1, 1), True),
    ("ビジネスサポート（AI のチャットボット、550名）", "名古屋市", {"事務代行", "ビジネスサポート"}, (550, 550), True),
    # D2 の判断14（2026-11-11）
    ("旭鉄工（自動車部品、愛媛県西条市で使用済み）", "碧南市", {"自動車部品", "輸送用機械"}, None, True),
    ("ダイケン商会（ダイケンフードソリューションズ、食品衛生のコンサル・商社、20〜49名。宮崎県都城市で使用済み）", "豊橋市",
     {"食品衛生", "商社", "コンサルティング"}, (20, 49), True),
    # cases_outside.md（県外。本文用1件）
    ("野嵩商会（沖縄県宜野湾市、食品スーパー、AI の需要予測で発注。正社員370名・パート1,460名、ベンダーの記載）", "県外",
     {"食品スーパー", "スーパー", "食料品小売"}, (370, 1830), True),
]

# 市町村の民営従業者数と、試算に選んだ中分類の事業所数・従業者数（stats.md の各市町村の節の (B)。経済センサス 2021年6月1日、民営）
# slug: (民営従業者, 中分類, 中分類の事業所, 中分類の従業者)
STAT = {
    'nagoya': (1450337, '機械器具卸売業', 4395, 64961),
    'toyohashi': (164058, '医療業', 664, 10310),
    'okazaki': (165945, '輸送用機械器具製造業', 150, 19971),
    'ichinomiya': (140911, '繊維工業', None, 140911),
    'seto': (46247, '窯業・土石製品製造業', 424, 3158),
    'handa': (57224, '飲食店', 533, 3848),
    'kasugai': (111307, 'その他の小売業', 576, 5316),
    'toyokawa': (78350, '輸送用機械器具製造業', 147, 10506),
    'tsushima-city': (27539, '飲食料品小売業', 130, 1649),
    'hekinan': (35859, 'はん用機械器具製造業', 22, 2222),
    'kariya': (117314, '（学術研究，専門・技術サービス業）', None, 117314),
    'toyota': (247911, '道路貨物運送業', 235, 9416),
    'anjo': (107931, '輸送用機械器具製造業', 147, 20316),
    'nishio': (84341, '輸送用機械器具製造業', 136, 27526),
    'gamagori': (32958, '繊維工業', 231, 1933),
    'inuyama': (31904, '飲食店', 258, 1595),
    'tokoname': (29031, '窯業・土石製品製造業', 141, 1691),
    'konan-city': (29009, '医療業', 199, 3454),
    'komaki': (106426, '道路貨物運送業', 356, 10635),
    'inazawa': (63402, '社会保険・社会福祉・介護事業', 169, 3563),
    'shinshiro': (18731, '生産用機械器具製造業', 26, 1294),
    'tokai-city': (60069, '道路貨物運送業', 119, 3720),
    'obu': (49471, '生産用機械器具製造業', 109, 4727),
    'chita': (20235, '飲食料品小売業', 93, 1383),
    'chiryu': (24713, '機械器具卸売業', 40, 1490),
    'owariasahi': (23688, '社会保険・社会福祉・介護事業', 132, 2125),
    'takahama-city': (21945, 'プラスチック製品製造業（別掲を除く）', 16, 1119),
    'iwakura': (14538, '道路貨物運送業', 34, 1126),
    'toyoake': (28656, '医療業', 117, 4327),
    'nisshin': (30868, '社会保険・社会福祉・介護事業', 125, 2371),
    'tahara': (30094, 'その他の小売業', 210, 1274),
    'aisai': (17830, '社会保険・社会福祉・介護事業', 85, 1820),
    'kiyosu': (28969, '食料品製造業', 35, 1431),
    'kitanagoya': (32493, '医療業', 136, 1787),
    'yatomi': (22293, '道路貨物運送業', 111, 2511),
    'miyoshi-city': (33410, '生産用機械器具製造業', 49, 1348),
    'ama-city': (25499, '食料品製造業', 26, 1341),
    'nagakute': (27217, 'その他の小売業', 141, 1830),
    'togo': (15421, '金属製品製造業', 38, 1474),
    'toyoyama': (14417, '飲食料品卸売業', 112, 2087),
    'oguchi': (27086, '生産用機械器具製造業', 42, 4768),
    'fuso': (9238, '飲食店', 129, 1057),
    'oharu': (8613, '社会保険・社会福祉・介護事業', 25, 698),
    'kanie': (13688, '飲食店', 180, 1423),
    'agui': (9697, '飲食料品小売業', 61, 1108),
    'higashiura': (17191, '家具・装備品製造業', 11, 851),
    'minamichita': (7045, '宿泊業', 133, 1213),
    'mihama-town-aichi': (8501, '食料品製造業', 15, 591),
    'taketoyo': (13918, '社会保険・社会福祉・介護事業', 36, 972),
    'kota': (20163, '輸送用機械器具製造業', 21, 2602),
    'shitara': (1675, '社会保険・社会福祉・介護事業', 9, 246),
    'toei': (1064, '総合工事業', 21, 121),
    'tobishima': (11606, '運輸に附帯するサービス業', 91, 1682),
    'toyone': (496, '総合工事業', 11, 115),
}

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])（奈良と同じ9列）
# 業種・業態は stats.md の各市町村の「(B) 中小企業の業種の候補」から選んだ。(A) 大企業の工場と読める業種
# （豊田市・田原市などの輸送用機械の大きな工場、東海市の鉄鋼、安城市・幸田町の電気機械、知多市の石油製品など）は
# 工場の値と読めない業態（下請けの小さい部品加工・物流・卸など）にした。農業・漁業・林業は試算の業種にしない。
PLAN = [
    ('名古屋市', 'nagoya', '卸売業・小売業', '機械器具卸売（工作機械・工具・機械部品の専門商社）', {'専門商社', '機械器具卸売', '工具卸'}, 113,
     '取引先からの在庫・価格・納期の問い合わせへの回答と、仕入先への発注の連絡、見積書・提案書の下書き', 58, 32.5),
    ('豊橋市', 'toyohashi', '医療・福祉', '病院（回復期リハビリテーション病棟と外来）', {'医療', 'リハビリ', '病院'}, 120,
     'リハビリの実施記録の要約と、退院前カンファレンスの記録、紹介元の医療機関への報告書の作成', 54, 31.5),
    ('岡崎市', 'okazaki', '製造業', '輸送用機械（自動車部品の切削・研削加工、2次・3次の取引先）', {'切削加工', '自動車部品', '輸送用機械'}, 66,
     '取引先からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録・不具合の報告書の取りまとめ', 38, 35.5),
    ('一宮市', 'ichinomiya', '製造業', '繊維（毛織物の製織、尾州の機屋）', {'繊維', '織物', '毛織物'}, 110,
     'アパレル・生地商からの品番・数量・納期の問い合わせへの回答と、生地の仕様書・生産の指示書、出荷の記録の取りまとめ', 66, 34.5),
    ('瀬戸市', 'seto', '製造業', '窯業・土石（陶磁器のノベルティ・食器の製造）', {'窯業・土石', '陶磁器', 'ノベルティ'}, 69,
     '問屋・小売店・通販の取引先からの在庫・仕様・納期の問い合わせへの回答と、商品の説明文、出荷の記録の取りまとめ', 41, 41.0),
    ('半田市', 'handa', '宿泊・飲食サービス業', '飲食店（宴会を受ける和食店を数店舗）', {'和食', '飲食店', '宴会'}, 137,
     '予約・宴会の問い合わせへの返信の下書きと、宴会の見積書・献立の案内文、仕入先への発注の連絡', 82, 32.5),
    ('春日井市', 'kasugai', '卸売業・小売業', 'その他の小売（調剤薬局とドラッグストアを数店舗）', {'ドラッグストア', '調剤薬局', '小売'}, 132,
     '仕入先への発注・欠品の連絡と、客からの問い合わせへの回答の下書き、店舗の掲示・案内文の作成', 79, 31.0),
    ('豊川市', 'toyokawa', '製造業', '輸送用機械（自動車部品の樹脂部品の成形と組立、2次の取引先）', {'自動車部品', '樹脂部品', '輸送用機械'}, 63,
     '取引先からの仕様・納期の問い合わせへの回答と、成形条件・検査記録の取りまとめ、不具合の報告書の下書き', 36, 34.25),
    ('津島市', 'tsushima-city', '卸売業・小売業', '飲食料品の小売（和菓子・食品の店を数店舗と通販）', {'食料品小売', '小売', '和菓子'}, 85,
     '客・通販の注文の問い合わせへの回答と、仕入先への発注の連絡、商品の説明文・季節の案内文の作成', 51, 31.0),
    ('碧南市', 'hekinan', '製造業', 'はん用機械（ポンプ・送風機の部品の加工）', {'ポンプ', 'はん用機械', '機械部品'}, 125,
     '取引先からの図面・納期の問い合わせへの回答と、見積書の作成、検査記録・作業日報の取りまとめ', 75, 39.0),
    ('刈谷市', 'kariya', '学術研究・専門技術サービス', '機械設計の受託（自動車部品・生産設備の設計と図面の作成）', {'設計受託', '技術サービス', '機械設計'}, 35,
     '顧客との仕様の打合せ記録の要約と、設計の検討書・報告書の下書き、図面の変更点の連絡文の作成', 12, 34.75),
    ('豊田市', 'toyota', '運輸業・郵便業', '道路貨物運送（部品・資材の工場間の輸送）', {'道路貨物運送', '運送'}, 83,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計', 49, 33.0),
    ('安城市', 'anjo', '製造業', '輸送用機械（自動車部品の溶接・組立、2次の取引先）', {'自動車部品', '輸送用機械', '溶接'}, 58,
     '取引先からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録・不具合の報告書の取りまとめ', 34, 42.5),
    ('西尾市', 'nishio', '製造業', '輸送用機械（自動車部品の熱処理・表面処理の受託加工）', {'熱処理', '輸送用機械', '表面処理'}, 140,
     '取引先からの処理の仕様・納期の問い合わせへの回答と、処理の記録・検査成績書の取りまとめ、見積書の作成', 84, 34.25),
    ('蒲郡市', 'gamagori', '製造業', '繊維（ロープ・繊維製品の製造）', {'繊維製品', 'ロープ', '繊維'}, 109,
     '取引先からの仕様・数量・納期の問い合わせへの回答と、仕様書・生産の指示書、出荷の記録の取りまとめ', 65, 37.0),
    ('犬山市', 'inuyama', '宿泊・飲食サービス業', '飲食店（観光地の食事処と土産物の販売）', {'土産物', '飲食店', '食事処'}, 122,
     '団体・予約の問い合わせへの返信の下書きと、団体の見積書・献立の案内文、多言語のメニューの文の作成', 73, 37.0),
    ('常滑市', 'tokoname', '製造業', '窯業・土石（急須・植木鉢などの陶器の製造）', {'窯業・土石', '陶器', '急須'}, 70,
     '問屋・小売店・通販の取引先からの在庫・仕様の問い合わせへの回答と、商品の説明文、出荷の記録の取りまとめ', 42, 36.5),
    ('江南市', 'konan-city', '医療・福祉', '診療所（内科・整形外科の外来とリハビリ）', {'診療所', '医療', '整形外科'}, 84,
     '紹介状・診療情報提供書の下書きと、リハビリの記録の要約、患者への案内文の作成', 50, 32.5),
    ('小牧市', 'komaki', '運輸業・郵便業', '道路貨物運送と倉庫（名古屋圏の配送拠点）', {'道路貨物運送', '倉庫', '運送'}, 91,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録・入出庫の記録の集計', 46, 29.5),
    ('稲沢市', 'inazawa', '医療・福祉', '通所介護と小規模多機能型居宅介護', {'通所介護', '小規模多機能', '介護'}, 119,
     '利用の記録と個別機能訓練計画書の下書き、家族への連絡帳の文、サービス担当者会議の記録の作成', 71, 39.0),
    ('新城市', 'shinshiro', '製造業', '生産用機械（工作機械・専用機の部品の加工）', {'専用機', '生産用機械', '機械部品'}, 89,
     '取引先からの図面・納期の問い合わせへの回答と、見積書の作成、検査記録・作業日報の取りまとめ', 53, 29.0),
    ('東海市', 'tokai-city', '運輸業・郵便業', '道路貨物運送（鋼材・建材の輸送）', {'道路貨物運送', '鋼材輸送', '運送'}, 139,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計', 83, 31.0),
    ('大府市', 'obu', '製造業', '生産用機械（工場の省力化装置・治具の設計製作）', {'省力化装置', '治具', '生産用機械'}, 142,
     '顧客との仕様の打合せ記録の要約と、見積書・取扱説明書・設計変更の連絡書の下書き', 85, 33.0),
    ('知多市', 'chita', '卸売業・小売業', '飲食料品の小売（食品スーパーを数店舗）', {'スーパー', '食料品小売', '小売'}, 135,
     '仕入先への発注・欠品の連絡と、売場のPOP・チラシの文、客からの問い合わせへの回答の下書き', 81, 33.0),
    ('知立市', 'chiryu', '卸売業・小売業', '機械器具卸売（自動車部品・工具・油脂の卸）', {'部品卸', '機械器具卸売', '工具卸'}, 95,
     '取引先からの在庫・価格・納期の問い合わせへの回答と、仕入先への発注の連絡、見積書・納品の記録の取りまとめ', 57, 33.0),
    ('尾張旭市', 'owariasahi', '医療・福祉', '訪問介護と居宅介護支援', {'訪問介護', '介護', '居宅介護支援'}, 114,
     '訪問の記録の清書と、ケアプランの下書き・モニタリングの記録、家族への連絡文の作成', 68, 30.25),
    ('高浜市', 'takahama-city', '製造業', 'プラスチック製品（自動車用の樹脂部品の成形）', {'樹脂部品', 'プラスチック製品', '射出成形'}, 105,
     '取引先からの金型・納期・品質の問い合わせへの回答と、成形条件・検査記録の取りまとめ、不具合の報告書の下書き', 63, 39.0),
    ('岩倉市', 'iwakura', '運輸業・郵便業', '道路貨物運送（食品・日用品の地場配送）', {'道路貨物運送', '運送'}, 82,
     '荷主からの配送状況・納品時刻の問い合わせへの回答と、配車の連絡、運転日報・点呼記録の取りまとめ', 49, 29.0),
    ('豊明市', 'toyoake', '医療・福祉', '訪問看護ステーション（訪問リハビリを含む）', {'訪問看護', '医療', '訪問リハビリ'}, 65,
     '訪問の記録の要約と、主治医への報告書・計画書の下書き、利用者・家族への連絡文の作成', 39, 39.0),
    ('日進市', 'nisshin', '医療・福祉', '介護付き有料老人ホーム', {'有料老人ホーム', '介護'}, 129,
     'ケア記録の清書と、入居者の家族への近況の連絡文、入居の問い合わせへの返信の下書き', 77, 33.0),
    ('田原市', 'tahara', '卸売業・小売業', 'その他の小売（農業資材・肥料・園芸用品の販売と配達）', {'園芸用品', '農業資材', '小売'}, 87,
     '農家・客からの在庫・価格の問い合わせへの回答と、仕入先への発注の連絡、配達の注文の取りまとめ', 52, 33.25),
    ('愛西市', 'aisai', '医療・福祉', '障害福祉サービス（就労継続支援と生活介護）', {'生活介護', '就労継続支援', '障害福祉'}, 112,
     '利用者の支援記録の清書と、個別支援計画の下書き、家族・相談支援専門員への連絡文の作成', 67, 35.0),
    ('清須市', 'kiyosu', '製造業', '食料品（菓子の製造と卸）', {'食料品', '菓子'}, 117,
     '取引先（小売店・量販店）からの規格・原材料・アレルゲンの問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 70, 35.5),
    ('北名古屋市', 'kitanagoya', '医療・福祉', '歯科診療所（分院を含む数か所）', {'歯科診療所', '医療', '歯科'}, 57,
     '患者への案内文・説明文書の下書きと、診療の記録の要約、問い合わせへの返信の下書き', 34, 44.5),
    ('弥富市', 'yatomi', '運輸業・郵便業', '道路貨物運送（港の海上コンテナの陸送）', {'コンテナ輸送', '道路貨物運送', '運送'}, 127,
     '配車表の下書きと、荷主・海貨業者への到着予定・遅延の連絡、運転日報・点呼記録の集計', 76, 31.75),
    ('みよし市', 'miyoshi-city', '製造業', '生産用機械（金型の設計製作）', {'生産用機械', '金型'}, 97,
     '取引先からの図面・仕様変更・納期の問い合わせへの回答と、見積書の作成、設計変更・検査の記録の取りまとめ', 58, 30.5),
    ('あま市', 'ama-city', '製造業', '食料品（漬物・佃煮の製造と卸）', {'佃煮', '漬物', '食料品'}, 100,
     '取引先（小売店・量販店）からの規格・原材料・賞味期限の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 60, 31.75),
    ('長久手市', 'nagakute', '卸売業・小売業', 'その他の小売（家具・インテリア雑貨の専門店と通販）', {'インテリア', '家具小売', '小売'}, 92,
     '客・通販の問い合わせへの回答と、商品の説明文、仕入先への発注・配送の連絡', 55, 35.0),
    ('東郷町', 'togo', '製造業', '金属製品（板金・溶接による部品の製造）', {'金属製品', '溶接', '板金'}, 115,
     '取引先からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録・不具合の報告書の取りまとめ', 69, 37.0),
    ('豊山町', 'toyoyama', '卸売業・小売業', '飲食料品卸売（青果・水産物の仲卸）', {'青果卸', '飲食料品卸売', '仲卸'}, 104,
     '飲食店・量販店の取引先からの入荷・規格・価格の問い合わせへの回答と、商品の説明文、出荷の記録の取りまとめ', 62, 33.5),
    ('大口町', 'oguchi', '製造業', '生産用機械（工作機械の部品の加工と組立）', {'生産用機械', '工作機械', '機械部品'}, 130,
     '取引先からの図面・納期の問い合わせへの回答と、見積書の作成、検査記録・組立の記録の取りまとめ', 78, 33.5),
    ('扶桑町', 'fuso', '宿泊・飲食サービス業', '飲食店（家族客向けの飲食店を数店舗）', {'飲食店'}, 74,
     '予約・問い合わせへの返信の下書きと、仕入先への発注の連絡、メニュー・店内の案内文の作成', 44, 32.75),
    ('大治町', 'oharu', '医療・福祉', '通所介護（送迎を含む）', {'通所介護', '介護'}, 60,
     '利用の記録と個別機能訓練計画書の下書き、家族への連絡帳の文、送迎表の作成', 36, 43.25),
    ('蟹江町', 'kanie', '宿泊・飲食サービス業', '飲食店（宴会・法事を受ける料理店）', {'料理店', '飲食店', '宴会'}, 64,
     '予約・宴会の問い合わせへの返信の下書きと、宴会の見積書・献立の案内文、仕入先への発注の連絡', 38, 39.5),
    ('阿久比町', 'agui', '卸売業・小売業', '飲食料品の小売（地元の食品スーパー）', {'スーパー', '食料品小売', '小売'}, 90,
     '仕入先への発注・欠品の連絡と、売場のPOP・チラシの文、客からの問い合わせへの回答の下書き', 54, 33.5),
    ('東浦町', 'higashiura', '製造業', '家具・装備品（店舗の什器・木製家具の製作）', {'家具・装備品', '木製家具', '店舗什器'}, 77,
     '取引先からの見積・納期・仕様の問い合わせへの回答と、製作の指示書・図面の変更点の連絡、出荷の記録の取りまとめ', 46, 33.5),
    ('南知多町', 'minamichita', '宿泊・飲食サービス業', '旅館（海水浴・釣り・団体の客）', {'宿泊', '旅館'}, 72,
     '予約サイト・電話・メールの問い合わせへの返信の下書きと、団体の見積書、館内・周辺の案内文の作成', 43, 39.0),
    ('美浜町', 'mihama-town-aichi', '製造業', '食料品（干物・佃煮などの水産加工）', {'水産加工', '食料品', '干物'}, 75,
     '量販店・通販の取引先からの原材料・産地・賞味期限の問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ', 45, 37.0),
    ('武豊町', 'taketoyo', '医療・福祉', '特別養護老人ホーム（短期入所を併設）', {'特別養護老人ホーム', '短期入所', '介護'}, 124,
     'ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成', 74, 38.5),
    ('幸田町', 'kota', '製造業', '輸送用機械（自動車部品のゴム・樹脂部品の加工、2次の取引先）', {'ゴム部品', '自動車部品', '輸送用機械'}, 99,
     '取引先からの仕様・納期の問い合わせへの回答と、作業手順書・検査記録の取りまとめ、不具合の報告書の下書き', 59, 31.0),
    ('設楽町', 'shitara', '医療・福祉', '特別養護老人ホーム（通所介護を併設）', {'特別養護老人ホーム', '介護', '通所介護'}, 79,
     'ケア記録の清書と、家族への近況の連絡文、委員会の議事録の作成', 47, 31.0),
    ('東栄町', 'toei', '建設業', '総合工事業（道路・林道・河川の土木工事、公共工事が中心）', {'建設', '総合工事業', '土木'}, 62,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理', 37, 41.0),
    ('飛島村', 'tobishima', '運輸業・郵便業', '運輸に附帯するサービス（港湾地区の倉庫・通関・荷役の手配）', {'港湾運送', '通関', '倉庫'}, 102,
     '荷主からの在庫・入出庫・通関の問い合わせへの回答と、入出庫の記録・在庫報告の作成、運送業者への手配の連絡', 61, 33.0),
    ('豊根村', 'toyone', '建設業', '総合工事業（道路・砂防の土木工事、公共工事が中心）', {'建設', '総合工事業', '土木'}, 55,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真・出来形の記録の整理', 33, 41.0),
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def read_plan_text(src):
    """PLAN を文字列で切り出す（改行のすぐ後ろの「PLAN = [」から行頭の「]」まで）。docstring の中の「PLAN = [」は拾わない"""
    i = src.find("\nPLAN = [")
    if i < 0:
        raise ValueError("行頭の PLAN = [ がない")
    start = i + 1
    j = src.index("\n]", start)
    return ast.literal_eval(src[start + len("PLAN = "):j + 2])


def load_plan(path):
    """他県の _calc.py を import して PLAN を返す（main は __name__ のガードで動かない）。だめなら文字列で読む。読めなければ例外"""
    pref = os.path.basename(os.path.dirname(path))
    sys.dont_write_bytecode = True  # 他県のフォルダに __pycache__ を作らない
    try:
        spec = importlib.util.spec_from_file_location("plan_" + pref, path)
        mod = importlib.util.module_from_spec(spec)
        with redirect_stdout(io.StringIO()):
            spec.loader.exec_module(mod)
        return list(mod.PLAN)
    except Exception:  # noqa: BLE001 import できなければ文字列で読む
        return read_plan_text(open(path, encoding="utf-8").read())


def other_plans():
    """全県の _calc.py の PLAN を読み、(県, 市町村, 削減時間, 万円) を返す。
    必須の県のファイルがなければ None を入れる（NG）。読めないファイルは警告だけ（NG にしない）。"""
    out, read, warn = [], {}, []
    paths = sorted(glob.glob(os.path.join(ROOT, "data", "area", "*", "_calc.py")))
    found = {os.path.basename(os.path.dirname(p)): p for p in paths}
    for pref in REQUIRED:
        if pref not in found:
            print(f"NG {pref} の _calc.py がない（必須）")
            out.append(None)
    for pref, path in found.items():
        if pref == SELF:
            continue
        try:
            rows = load_plan(path)
        except Exception as e:  # noqa: BLE001
            warn.append(f"{pref} の _calc.py の PLAN が読めない（{type(e).__name__}: {e}）。照合から外した")
            continue
        n_skip = 0
        for r in rows:
            try:
                city, ind, n, hrs = r[0], r[2], r[-2], r[-1]
            except Exception:  # noqa: BLE001
                n_skip += 1
                continue
            if ind not in RATE:
                n_skip += 1
                continue
            h = Decimal(str(n)) * Decimal(str(hrs)) * Decimal("0.25")
            out.append((pref, city, h, man(h * RATE[ind])))
        if n_skip:
            warn.append(f"{pref} の PLAN に読めない行・時給の分からない業種が {n_skip}行ある（RATE に足す）")
        read[pref] = len(rows)
    return out, read, warn


def existing():
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（鹿児島県の _calc.py と同じ拾い方）。"""
    hours, mans, sizes, per_file = {}, {}, {}, {}
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
        for x in re.findall(r"従業員\s*(\d+)\s*名", sec.splitlines()[0]):
            sizes.setdefault(int(x), name)
    return len(files), n_sec, hours, mans, sizes, per_file


def used_values():
    """既存の記事と他県の PLAN で使われている時間・万円（探索用。main と同じ集め方）"""
    _, _, ex_h, ex_m, _, _ = existing()
    op, _, _ = other_plans()
    h = set(ex_h) | {r[2] for r in op if r}
    m = set(ex_m) | {r[3] for r in op if r}
    return h, m


def in_range(size, csize):
    lo, hi = csize
    return lo * 0.85 <= size <= hi * 1.15


def border_ok(yen):
    """四捨五入の境目（◯.◯5万円＝千円の位で500円）から100円より離れているか"""
    return abs(int(yen % 1000) - 500) > 100


def main():
    n_files, n_sec, ex_h, ex_m, ex_s, per_file = existing()
    empty = [k for k, v in per_file.items() if v[1] == 0]
    if empty:
        print("NG 試算の金額を拾えなかった既存の記事:", empty)
    by_pref = Counter(re.sub(r"^2026-1\d-\d+-area-([a-z]+).*", r"\1", k) for k in per_file)
    print(f"既存の地域ページ: {n_files}本（うち試算の節があるもの {n_sec}本。県別 {dict(sorted(by_pref.items()))}）。"
          f"拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種・規模 {len(ex_s)}種")
    op, read, warn = other_plans()
    ok = None not in op
    pl_h, pl_m = {}, {}
    for r in op:
        if r is None:
            continue
        pref, city, h, m = r
        pl_h.setdefault(h, f"{pref} {city}（_calc.py の PLAN）")
        pl_m.setdefault(m, f"{pref} {city}（_calc.py の PLAN）")
    print(f"他県の PLAN: {len(read)}県 {sum(read.values())}行（{', '.join(f'{k} {v}' for k, v in read.items())}）。"
          f"時間 {len(pl_h)}種・万円 {len(pl_m)}種")
    for w in warn:
        print("（警告）", w)
    if not os.path.exists(os.path.join(HERE, "cases2.md")):
        print("（注意）cases2.md はまだない。できたら会社を CASES に足して再実行する")

    seen_h, seen_m, seen_s = {}, {}, {}
    notes = []
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | ×4 を4で割った余り |")
    print("|---|---|---|---|---|---|---|---|")
    for (city, slug, ind, sub, keys, size, task, n, hrs) in PLAN:
        if ind not in WAGES_MD:
            print(f"  NG {city} の業種 {ind} は wages.md にない（農林漁業は試算の業種にしない）")
            ok = False
            continue
        h = Decimal(str(n)) * Decimal(str(hrs)) * Decimal("0.25")
        yen = h * RATE[ind]
        m = man(yen)
        y = man(yen * 12)
        q = h * 4
        res = int(q) % MOD_N if q % 1 == 0 else None
        print(f"| {city} | {ind}（{sub}） | {size}名 | {n}名×{hrs}時間×25% | {h.normalize():f}時間 | 約{RATE[ind]:,}円 | 約{m}万円 | {res} |")
        if q % 1 != 0:
            print(f"  NG {city} の時間が0.25時間刻みでない ({h})")
            ok = False
        elif res != MOD_R:
            print(f"  NG {city} の時間 {h} は東海・京都の割り当て（×4 を{MOD_N}で割った余り {MOD_R}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 愛知県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 愛知県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
            ok = False
        seen_s[size] = city
        if not border_ok(yen):
            print(f"  NG {city} の金額が四捨五入の境目に近い（{yen}円）")
            ok = False
        if n > size:
            print(f"  NG {city} の対象人数が従業員数より多い")
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
            elif slug in VILLAGES and size * 2 > mid_emp:
                notes.append(f"{city}: 仮の会社 {size}名が村の「{mid}」の従業者 {mid_emp}人の半分を超える（規模を小さくするか、県内の例と書く）")
            if mid_n and size > 3 * mid_emp / mid_n and slug in VILLAGES:
                notes.append(f"{city}: 仮の会社 {size}名は村の「{mid}」の1所あたり {mid_emp / mid_n:.1f}人の3倍を超える")
        for (cname, ccity, ckeys, csize, is_ai) in CASES:
            if "業種未確認" in ckeys:
                if ccity == city:
                    notes.append(f"{city}: 業種を確かめていない事例 {cname} がある（試算は {sub}・{size}名。試算の節で事例の会社に触れない）")
                continue
            if not (keys & ckeys):
                continue
            if not is_ai:
                if (csize is not None and in_range(size, csize)) or (csize is None and ccity == city):
                    notes.append(f"{city}: 試算（{sub}・{size}名）と業態が近い AI ではない事例 {cname}（{csize or '規模不明'}）")
                continue
            if csize is not None and in_range(size, csize):
                print(f"  NG {city} の試算（{sub}・{size}名）が事例 {cname}（{'・'.join(sorted(ckeys))}・{csize[0]}〜{csize[1]}名）に近い")
                ok = False
            elif csize is None and ccity == city:
                print(f"  NG {city} の試算（{sub}）が同じ市町村の事例 {cname}（規模不明）と同じ業態")
                ok = False
            elif ccity in ("所在未確認", "県外"):
                notes.append(f"{city}: 試算（{sub}・{size}名）と業態のキーが重なる{ccity}の事例 {cname}"
                             f"（{'規模不明' if csize is None else f'{csize[0]}〜{csize[1]}名で範囲外'}・別の市町村なので NG にしない）")
    slugs = [p[1] for p in PLAN]
    if set(slugs) != SLUGS or len(slugs) != len(set(slugs)):
        print("NG slug が _brief.md と違う:", set(slugs) ^ SLUGS, [s for s, c in Counter(slugs).items() if c > 1])
        ok = False
    if not PLAN:
        print("NG PLAN が空")
        print("NG")
        return
    n_ex_size = sum(1 for p in PLAN if p[5] in ex_s)
    print(f"\n市町村ページ: {len(PLAN)}、市町村名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}")
    print(f"時間の範囲 {min(seen_h).normalize():f}〜{max(seen_h).normalize():f}時間、金額の範囲 約{min(seen_m)}〜{max(seen_m)}万円、規模 {min(seen_s)}〜{max(seen_s)}名")
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは愛知県の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == N_PAGES else "NG")


def free(ind, lo, hi):
    """業種 ind で、lo〜hi 時間の空いている（時間, 万円）を並べる（余り1の時間だけ）"""
    h_used, m_used = used_values()
    mine_h = {Decimal(str(p[7])) * Decimal(str(p[8])) * Decimal("0.25") for p in PLAN}
    mine_m = {man(Decimal(str(p[7])) * Decimal(str(p[8])) * Decimal("0.25") * RATE[p[2]]) for p in PLAN}
    h = Decimal(str(lo))
    out = []
    while h <= Decimal(str(hi)):
        if (h * 4) % 1 == 0 and int(h * 4) % MOD_N == MOD_R and h not in h_used and h not in mine_h:
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
