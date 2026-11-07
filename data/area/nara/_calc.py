#!/usr/bin/env python3
"""奈良県39市町村の試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-11-07）。

data/area/ibaraki/_calc.py を元に作った（和歌山・滋賀の _calc.py と同じ形）。県ページ（/area/nara/）には試算を入れないので、PLAN は39行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **奈良・和歌山・滋賀の取り決め**: 月の削減時間（0.25時間刻み）×4 を3で割った余りが 0（奈良県）の時間だけを使う
     （0.75, 1.5, 2.25, … の0.75時間刻み。data/area/_kinki/shared.md）
  1. 39ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、奈良県を除く）の「## 試算」の節に出てくる
     「◯時間」「◯万円」の値と重ならない。拾い方は茨城県・鹿児島県の _calc.py と同じ（広めに拾う）
  3. 全県の data/area/*/_calc.py の PLAN（奈良県を除く。glob で全部読む。和歌山・滋賀・北海道を含む）の
     月の削減時間・月の時間換算額と重ならない。他県の _calc.py は import で読み、だめなら行頭の「PLAN = [」
     （改行のすぐ後ろのものだけ）を文字列で切り出して読む。**読めないファイルは NG にせず警告**。
     REQUIRED の県はファイルがなければ NG。**金額が重なったら先に push した県（和歌山・滋賀）を優先し、奈良を変える**
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md・cases2.md（あれば）・subsidy_*_areas.md の事例の会社と
     同じにならない（CASES と照合。茨城と同じ判定）
  6. slug が _brief.md の39市町村と一致する（奈良市 nara-city、川西町 kawanishi-town、川上村 kawakami）
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
  8. 県ページには試算を入れない（PLAN は39行）
  9. **仮の会社の従業員数が、その市町村の民営従業者数・選んだ中分類の従業者数（stats.md の (B)、経済センサス2021）を
     超えない**（STAT と照合。沖縄で村の仮の会社が村の民営従業者より大きくなったため）。村は中分類の従業者の半分を
     超えたら参考として表示する
使い方: python3 data/area/nara/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/nara/_calc.py free 製造業 30 200   （余り0の時間で、既存・他県・奈良の中と重ならない時間と金額の候補を出す）
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
SELF = "nara"
PREF_JA = "奈良県"
MOD_N, MOD_R = 3, 0  # 奈良・和歌山・滋賀の割り当て（月の削減時間×4 を3で割った余り）。奈良県は 0
N_PAGES = 39

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
    # 市（12）
    "nara-city", "yamatotakada", "yamatokoriyama", "tenri", "kashihara", "sakurai", "gojo", "gose", "ikoma",
    "kashiba", "katsuragi", "uda",
    # 町（15）
    "heguri", "sango", "ikaruga", "ando", "kawanishi-town", "miyake", "tawaramoto", "takatori", "kanmaki", "oji",
    "koryo", "kawai", "yoshino", "oyodo", "shimoichi",
    # 村（12）
    "yamazoe", "soni", "mitsue", "asuka", "kurotaki", "tenkawa", "nosegawa", "totsukawa", "shimokitayama",
    "kamikitayama", "kawakami", "higashiyoshino",
}
VILLAGES = {"yamazoe", "soni", "mitsue", "asuka", "kurotaki", "tenkawa", "nosegawa", "totsukawa", "shimokitayama",
            "kamikitayama", "kawakami", "higashiyoshino"}

# 照合が必須の県（2026-11-07 に _calc.py がある県。近畿の和歌山・滋賀を含む）。ファイルがなければ NG。ほかに見つかった _calc.py も全部読む
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima",
            "hokkaido", "ibaraki", "tochigi", "gunma", "okinawa", "wakayama", "shiga")

# cases.md・cases_outside.md・subsidy_a_areas.md・companies.md（大企業の工場・AI を作る側）の会社（2026-11-07）
# (会社名, 市町村〔県外は「県外」〕, 業態のキー, 従業員数〔(下限, 上限)。分からなければ None〕, AI の事例か〔実証・使用済み・提供側を含む〕)
# cases2.md ができたら D2 が「# cases2.md」の行に足す
CASES = [
    # 奈良市（cases.md）
    ("アイニコグループ（全10事業部で生成AI、1年間で2,247時間〔自己申告〕。注文住宅・不動産・リフォーム・介護・保育・民泊。"
     "従業員数は配信になし。福島で使用済み）", "奈良市",
     {"工務店", "注文住宅", "住宅", "不動産", "リフォーム", "介護", "保育", "民泊"}, None, True),
    ("社会福祉法人史明会 特別養護老人ホームLino（カメラ型AIセンサー、特養・短期入所、85名。徳島で使用済み）", "奈良市",
     {"特別養護老人ホーム", "介護", "短期入所"}, (85, 85), True),
    ("ハンナ（運行の見える化、IoT。AI は今後。一般貨物自動車運送、115名）", "奈良市",
     {"道路貨物運送", "運送", "トラック運送"}, (115, 115), False),
    ("奈良交通（バスロケ、AI ではない。大企業）", "奈良市", {"路線バス", "バス"}, None, False),
    ("まほろば創研（配管劣化判定AIの共同開発、AI を作る側）", "奈良市", {"情報サービス", "AI製品開発", "ソフトウェア"}, None, True),
    ("トヨタユナイテッド奈良（学生の生成AIコンテストの題材、自動車販売）", "奈良市", {"自動車販売"}, None, True),
    ("中川政七商店（AI は今後の予定、工芸の製造小売）", "奈良市", {"工芸", "雑貨", "製造小売"}, None, False),
    ("cars（自動車業界向けAI、AI を売る側）", "奈良市", {"情報サービス", "AI製品開発"}, None, True),
    ("伊田重機（県のデジタル化支援、紙資料のデジタル化。AI ではない）", "奈良市", {"重機", "建設機械"}, None, False),
    ("ニュートラルソフトウェア（ChatGPT の会話システム、ソフトウェア開発、22名。companies.md）", "奈良市",
     {"情報サービス", "ソフトウェア", "システム開発"}, (22, 22), True),
    ("南都コンピュータサービス（AI・RPA の支援、南都銀行グループ）", "奈良市", {"情報サービス", "ソフトウェア"}, None, True),
    # 大和高田市
    ("ワキ製薬（AI 外観検査、家庭配置薬・OTC 医薬品の製造、72名。香川で使用済み・ベンダーの事例）", "大和高田市",
     {"医薬品", "配置薬", "医薬品製造"}, (72, 72), True),
    ("大峰堂薬品工業（データ整備で入力を約8割削減、AI と書かれていない。漢方などの医薬品製造）", "大和高田市",
     {"医薬品", "漢方", "医薬品製造"}, None, False),
    ("奈良OAシステム（OA機器の販売・ソフト開発、88名。companies.md）", "大和高田市", {"OA機器", "情報サービス"}, (88, 88), False),
    # 橿原市・香芝市（県の中小企業デジタル化等支援事業の事例。AI ではない）
    ("サンロード（営業支援・名刺管理、食品工場向け衛生キャップ等。AI ではない）", "橿原市", {"衛生用品", "衛生キャップ"}, None, False),
    ("C's（発注管理アプリ、AI ではない。業種は未確認）", "香芝市", {"業種未確認"}, None, False),
    # 五條市・下市町（農業）
    ("JAならけん西吉野柿部会ほか（AI 外観センサーの柿の選果の実証、目標。愛媛で使用済み）", "五條市",
     {"農業", "柿", "選果"}, None, True),
    ("赤松ハウス柿生産組合ほか（AI の成熟度判定の実証、数値は AI 以外。五條市・下市町）", "五條市", {"農業", "柿"}, None, True),
    ("赤松ハウス柿生産組合の「ほか」（下市町の経営体、名前なし）", "下市町", {"農業", "柿"}, None, True),
    # cases_outside.md（県外。本文用0件、参考3件）
    ("En Journey（観光バスの予約事務の AI、上場会社のグループ。見積り）", "県外", {"観光バス", "旅行"}, None, True),
    ("ナイガイ（靴下・レッグウェアの大手、在庫管理AI・マーケティングAI。大企業・見出しだけ）", "県外",
     {"靴下", "繊維", "ニット", "レッグウェア"}, None, True),
    ("LIFEFUND・EXCEED GROUP（工務店の勉強会、AI の時間の数値なし）", "県外", {"工務店", "住宅"}, None, True),
    # cases2.md（2026-11-07。中央会のものづくり補助事業成果事例集ほか）
    ("昭和化成工業（AI の画像処理つき自動箱詰めロボット付検査装置、ダイアライザー用容器の樹脂成形、38名）", "葛城市",
     {"樹脂成形", "プラスチック製品", "医療用容器", "射出成形"}, (38, 38), True),
    ("大和化成（生産計画を AI で自動立案、プラスチックの化粧品・薬品ボトル。従業員数は書かれていない）", "大和郡山市",
     {"プラスチック製品", "プラスチック容器", "ボトル", "樹脂成形"}, None, True),
    ("宮本金型製作所（IoT・AI でマシニングセンタを連携・監視、プレス金型の設計製作・プレス加工。従業員数は未確認）", "生駒市",
     {"金型", "プレス加工", "金属加工", "金属製品", "生産用機械"}, None, True),
    ("ツバサファクトリー（AI の画像処理ソフトの試作開発の計画、AI を作る側）", "香芝市", {"情報サービス", "画像処理", "AI製品開発"}, None, True),
    ("田村薬品工業（AI の品質管理の計画名だけ。所在未確認）", "所在未確認", {"医薬品", "医薬品製造"}, None, True),
    ("葛城工業（ディープラーニングの計画名だけ。所在が広陵町か葛城市か決まらない、業種は未確認）", "所在未確認", {"業種未確認"}, None, True),
    ("北村製箸所（画像処理判定の割箸の選別の計画、AI と書かれていない。所在未確認）", "所在未確認", {"割り箸", "木製品"}, None, False),
    ("ベルグ（歯科技工、AI は業界の一般論）", "大和郡山市", {"歯科技工"}, None, False),
    # 大企業の工場（companies.md・stats.md。AI の事例ではないが、試算が工場の値と読まれないよう業態のキーを入れる）
    ("ハウス食品 奈良工場・サンヨー食品 関西工場（大和郡山市、食品の大企業の工場）", "大和郡山市",
     {"食料品", "食品製造", "即席めん", "調味食品"}, None, False),
    ("シャープ 奈良事業所（大和郡山市、複合機ほか。業務用機械器具）", "大和郡山市",
     {"業務用機械", "複写機", "電気機械"}, None, False),
    ("シャープ 天理事業所（天理市）", "天理市", {"業務用機械", "電気機械", "電子部品"}, None, False),
    ("シャープ 葛城事業所（葛城市）", "葛城市", {"業務用機械", "電気機械", "電子部品"}, None, False),
    ("ジェイテクト 奈良工場（橿原市、ステアリング。輸送用機械器具）", "橿原市", {"輸送用機械", "自動車部品", "ステアリング"}, None, False),
    ("ジェイテクトサーモシステム（天理市、熱処理炉・半導体製造装置、619人〔gBizINFO〕）", "天理市",
     {"生産用機械", "熱処理炉", "半導体製造装置"}, (619, 619), False),
    ("ジェイテクトサープレット（安堵町、ベアリング等の旋削・熱処理・研磨）", "安堵町", {"金属製品", "ベアリング", "金属加工"}, None, False),
    ("東洋シヤッター 奈良工場（川西町、シャッター。会社534名は全社）", "川西町", {"金属製品", "シャッター", "建築用金属製品"}, None, False),
    ("川西町の印刷・同関連業（3所・1,129人）・輸送用機械（2所・761人）の大きな事業所（会社名は確かめていない）", "川西町",
     {"印刷", "輸送用機械"}, None, False),
]

# 市町村の民営従業者数と、試算に選んだ中分類の事業所数・従業者数（stats.md の一覧表と (B)。経済センサス 2021年6月1日、民営）
# slug: (民営従業者, 中分類, 中分類の事業所, 中分類の従業者)
STAT = {
    "nara-city": (127481, "宿泊業", 95, 1962),
    "yamatotakada": (18901, "繊維工業", 120, 1128),
    "yamatokoriyama": (40758, "道路貨物運送業", 70, 2712),
    "tenri": (28533, "飲食料品小売業", 142, 1873),
    "kashihara": (44133, "医療業", 269, 7087),
    "sakurai": (17607, "食料品製造業", 59, 1333),
    "gojo": (11240, "木材・木製品製造業（家具を除く）", None, 420),
    "gose": (9288, "プラスチック製品製造業（別掲を除く）", 17, 432),
    "ikoma": (29201, "社会保険・社会福祉・介護事業", 161, 3232),
    "kashiba": (18439, "飲食料品小売業", 97, 1888),
    "katsuragi": (12137, "社会保険・社会福祉・介護事業", 37, 1152),
    "uda": (7026, "総合工事業", 66, 418),
    "yamazoe": (1055, "社会保険・社会福祉・介護事業", 8, 157),
    "heguri": (3281, "飲食料品小売業", 32, 547),
    "sango": (4364, "社会保険・社会福祉・介護事業", 45, 815),
    "ikaruga": (5759, "飲食店", 70, 528),
    "ando": (2212, "社会保険・社会福祉・介護事業", 14, 379),
    "kawanishi-town": (4029, "卸売業（中分類の計）", 10, 138),
    "miyake": (1374, "道路貨物運送業", 8, 115),
    "tawaramoto": (12297, "道路貨物運送業", 27, 843),
    "soni": (559, "食料品製造業", 6, 75),
    "mitsue": (405, "その他の小売業", 7, 65),
    "takatori": (2276, "化学工業", 11, 349),
    "asuka": (1380, "飲食料品小売業", 16, 123),
    "kanmaki": (5300, "社会保険・社会福祉・介護事業", 42, 935),
    "oji": (7751, "飲食料品小売業", 38, 720),
    "koryo": (9057, "繊維工業", 119, 1007),
    "kawai": (3987, "医療業", 35, 308),
    "yoshino": (2952, "木材・木製品製造業（家具を除く）", 88, 428),
    "oyodo": (6002, "社会保険・社会福祉・介護事業", 26, 601),
    "shimoichi": (1596, "木材・木製品製造業（家具を除く）", 25, 160),
    "kurotaki": (200, "木材・木製品製造業（家具を除く）", 12, 27),
    "tenkawa": (721, "宿泊業", 44, 196),
    "nosegawa": (149, "総合工事業", 9, 42),
    "totsukawa": (1327, "総合工事業", 44, 353),
    "shimokitayama": (409, "宿泊業", 8, 70),
    "kamikitayama": (550, "宿泊業", 6, 37),
    "kawakami": (535, "総合工事業", 13, 70),
    "higashiyoshino": (645, "食料品製造業", 6, 60),
}

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])（茨城と同じ9列）
# 業種・業態は stats.md の各市町村の「(B) 中小企業の業種の候補」（経済センサスの中分類）から選んだ。
# 大和郡山市の食料品・業務用機械（大企業の工場）、天理市・葛城市の電機、橿原市の輸送用機械、天理市・川西町の大きな生産用機械、
# 川西町の印刷・輸送用機械（数所で千人規模）、安堵町の金属製品、上北山村の飲食料品卸売（1所・291人）、天理市の宗教、
# 三郷町の医療業（大きな病院と読める）は試算の業種・業態にしない。農業・林業も試算の業種にしない。
PLAN = [
    # 村・小さい町（空いている時間・金額が少ないので、先に小さい値を当てた。仮の会社は村の民営従業者・中分類の従業者を超えない）
    ('黒滝村', 'kurotaki', '製造業', '木材・木製品（丸太・木材の加工と販売）', {'木材', '木材・木製品', '製材'}, 20,
     '工務店・材木店の取引先からの寸法・在庫・納期の問い合わせへの回答と、見積書・出荷の記録・請求の取りまとめ', 12, 48.5),
    ('野迫川村', 'nosegawa', '建設業', '総合工事業（道路・林道の土木工事、公共工事が中心）', {'土木', '建設', '総合工事業'}, 19,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理', 12, 49.75),
    ('上北山村', 'kamikitayama', '宿泊・飲食サービス業', '旅館・民宿（登山・観光の個人客と団体）', {'宿泊', '旅館', '民宿'}, 21,
     '予約サイト・電話・メールの問い合わせへの返信の下書きと、団体の見積書、館内・周辺の案内文の作成', 12, 49.25),
    ('御杖村', 'mitsue', '卸売業・小売業', 'その他の小売（燃料・日用品・農業資材の販売と配達）', {'小売', '燃料小売', '日用品'}, 22,
     '仕入先への発注・欠品の連絡と、配達の注文の取りまとめ、客からの問い合わせへの回答の下書き', 12, 47.75),
    ('三宅町', 'miyake', '運輸業・郵便業', '道路貨物運送（県内の地場配送）', {'道路貨物運送', '運送'}, 24,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計', 12, 39.25),
    ('東吉野村', 'higashiyoshino', '製造業', '食料品（農産物・川魚などの加工食品の製造）', {'食料品', '加工食品'}, 33,
     '取引先（小売店・道の駅・通販）からの数量・規格の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 20, 37.5),
    ('川上村', 'kawakami', '建設業', '総合工事業（道路・河川・砂防の土木工事、公共工事が中心）', {'土木', '建設', '総合工事業'}, 39,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真・出来形の記録の整理', 24, 46.25),
    ('下北山村', 'shimokitayama', '宿泊・飲食サービス業', '宿泊施設（キャンプ場・コテージと食堂、観光客と団体）', {'宿泊', 'キャンプ場', '飲食サービス'}, 40,
     '予約・団体の問い合わせへの返信の下書きと、団体の見積書・食事の案内文、利用の案内文の作成', 24, 42.5),
    ('明日香村', 'asuka', '卸売業・小売業', '飲食料品・土産物の小売（観光客向けの店舗と通信販売）', {'土産物', '小売', '食料品小売'}, 41,
     '客・通販の注文の問い合わせへの回答と、仕入先への発注の連絡、商品の説明文・案内文の作成', 24, 45.0),
    ('曽爾村', 'soni', '製造業', '食料品（漬物・農産物の加工品の製造）', {'食料品', '漬物', '加工食品'}, 42,
     '取引先（小売店・道の駅・通販）からの数量・規格の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 25, 45.0),
    ('天川村', 'tenkawa', '宿泊・飲食サービス業', '旅館（温泉地の個人客と団体、登山客）', {'宿泊', '旅館', '温泉旅館'}, 44,
     '予約サイト・メールの問い合わせへの返信の下書きと、団体の見積書、館内・周辺の案内の多言語の文の作成', 26, 43.5),
    ('十津川村', 'totsukawa', '建設業', '総合工事業（道路・河川・砂防の土木工事、災害の復旧工事を含む）', {'土木', '建設', '総合工事業'}, 50,
     '公共工事の施工計画書・提出書類の作成と、工事写真・出来形の記録の整理、発注者との打合せ記録の要約', 30, 39.5),
    ('山添村', 'yamazoe', '医療・福祉', '特別養護老人ホーム（短期入所・通所介護を併設）', {'特別養護老人ホーム', '介護', '通所介護'}, 57,
     'ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成', 34, 25.5),
    # 町・市（空いている値が月約260〜460時間に集まるので、規模はその範囲で決めた）
    ('下市町', 'shimoichi', '製造業', '木材・木製品（木製品・木工品の加工と卸）', {'木材', '木材・木製品', '木工品'}, 54,
     '問屋・小売店の取引先からの数量・納期の問い合わせへの回答と、見積書・出荷の記録・請求の取りまとめ', 27, 45.0),
    ('吉野町', 'yoshino', '製造業', '木材・木製品（製材と建築用材の加工）', {'木材', '製材', '木材・木製品'}, 56,
     '工務店・材木店の取引先からの寸法・在庫・納期の問い合わせへの回答と、見積書・出荷の記録・請求の取りまとめ', 28, 43.5),
    ('河合町', 'kawai', '医療・福祉', '診療所（内科の外来と訪問診療）', {'医療', '診療所', '訪問診療'}, 52,
     '紹介状・診療情報提供書の下書きと、訪問診療の記録の要約、患者・家族への案内文の作成', 26, 45.0),
    ('川西町', 'kawanishi-town', '卸売業・小売業', '卸売（建築資材・機械工具の卸と配送）', {'卸売', '建築資材', '機械工具'}, 55,
     '取引先からの在庫・価格・納期の問い合わせへの回答と、仕入先への発注の連絡、見積書・納品の記録の取りまとめ', 27, 44.0),
    ('宇陀市', 'uda', '建設業', '総合工事業（道路・河川の土木工事と住宅の建築）', {'土木', '建設', '総合工事業'}, 58,
     '工事日報・安全書類の取りまとめと、発注者・施主への工程の連絡文、工事写真の整理', 28, 45.0),
    ('安堵町', 'ando', '医療・福祉', '通所介護と訪問介護（送迎を含む）', {'通所介護', '介護', '訪問介護'}, 60,
     '利用の記録と個別機能訓練計画書の下書き、家族への連絡帳の文、サービス担当者会議の記録の作成', 30, 44.5),
    ('斑鳩町', 'ikaruga', '宿泊・飲食サービス業', '飲食店（観光客と団体を受け入れる食事処を数店舗）', {'飲食店', '飲食サービス', '食事処'}, 61,
     '予約・団体の問い合わせへの返信の下書きと、団体の見積書・献立の案内文、多言語のメニューの文の作成', 30, 41.5),
    ('広陵町', 'koryo', '製造業', '繊維（靴下の編立・仕上げ、OEM が中心）', {'靴下', '繊維', '編立'}, 62,
     '取引先（アパレル・量販店）からの仕様・数量・納期の問い合わせへの回答と、仕様書・生産の指示書、検品の記録の取りまとめ', 30, 35.5),
    ('大淀町', 'oyodo', '医療・福祉', '介護老人保健施設（通所リハビリを併設）', {'介護老人保健施設', '介護'}, 59,
     'リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成', 28, 44.25),
    ('三郷町', 'sango', '医療・福祉', '認知症対応型グループホームと小規模多機能型居宅介護', {'グループホーム', '小規模多機能', '介護'}, 63,
     '生活記録の清書と、運営推進会議の議事録、家族への便りの文の作成', 30, 45.0),
    ('高取町', 'takatori', '製造業', '化学（医薬品・医薬部外品の製造）', {'医薬品', '医薬部外品', '化学工業'}, 53,
     '販売先・卸からの製品・成分・在庫の問い合わせへの回答と、製造・品質の記録の取りまとめ、手順書の改訂の下書き', 30, 36.5),
    ('五條市', 'gojo', '製造業', '木材・木製品（集成材・プレカット材の加工）', {'集成材', '木材・木製品', 'プレカット'}, 65,
     '工務店・住宅会社の取引先からの仕様・納期の問い合わせへの回答と、加工の指示書・出荷の記録の取りまとめ', 32, 39.0),
    ('上牧町', 'kanmaki', '医療・福祉', '住宅型有料老人ホーム（訪問介護を併設）', {'有料老人ホーム', '介護', '訪問介護'}, 68,
     'ケア記録の清書と、入居者の家族への近況の連絡文、入居の問い合わせへの返信の下書き', 34, 39.0),
    ('王寺町', 'oji', '卸売業・小売業', '飲食料品の小売（駅周辺の食品スーパー・専門店を数店舗）', {'食料品小売', '小売', 'スーパー'}, 66,
     '仕入先への発注・欠品の連絡と、売場のPOP・チラシの文、客からの問い合わせへの回答の下書き', 33, 40.0),
    ('平群町', 'heguri', '卸売業・小売業', '飲食料品の小売（食品スーパーと宅配）', {'食料品小売', '小売', '宅配'}, 69,
     '仕入先への発注・欠品の連絡と、宅配の注文の取りまとめ、売場の案内文・チラシの文の作成', 34, 37.5),
    ('大和高田市', 'yamatotakada', '製造業', '繊維（靴下・ニット製品の製造と卸）', {'靴下', '繊維', 'ニット製品'}, 67,
     '取引先（アパレル・量販店）からの仕様・数量・納期の問い合わせへの回答と、仕様書・生産の指示書、検品の記録の取りまとめ', 31, 42.0),
    ('御所市', 'gose', '製造業', 'プラスチック製品（工業用部品・日用品の成形）', {'工業用部品', '射出成形', 'プラスチック製品'}, 72,
     '取引先からの図面・仕様の変更と納期の問い合わせへの回答と、成形条件・検査記録の取りまとめ、不具合の報告書の下書き', 36, 35.5),
    ('桜井市', 'sakurai', '製造業', '食料品（素麺・乾麺の製造と卸）', {'食料品', '麺類', '素麺'}, 76,
     '問屋・量販店の取引先からの規格・原材料・アレルゲンの問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 38, 31.5),
    ('田原本町', 'tawaramoto', '運輸業・郵便業', '道路貨物運送と倉庫（食品・日用品の輸送と保管）', {'道路貨物運送', '運送', '倉庫'}, 70,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録・入出庫の記録の集計', 30, 41.0),
    ('葛城市', 'katsuragi', '医療・福祉', '特別養護老人ホーム（短期入所を併設）', {'特別養護老人ホーム', '介護', '短期入所'}, 71,
     'ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成', 36, 31.75),
    ('天理市', 'tenri', '卸売業・小売業', '飲食料品の小売（食品スーパーを数店舗）', {'食料品小売', '小売', 'スーパー'}, 74,
     '仕入先への発注・欠品の連絡と、売場のPOP・チラシの文、客からの問い合わせへの回答の下書き', 37, 36.0),
    ('奈良市', 'nara-city', '宿泊・飲食サービス業', 'ホテル・旅館（観光の個人客・修学旅行・団体、外国人客を含む）', {'宿泊', 'ホテル', '旅館'}, 90,
     '予約サイト・メールの問い合わせへの返信の下書きと、団体・修学旅行の見積書・行程の案内文、館内案内の多言語の文の作成', 38, 34.5),
    ('香芝市', 'kashiba', '卸売業・小売業', '飲食料品の小売（郊外の食品スーパーを数店舗）', {'食料品小売', '小売', 'スーパー'}, 86,
     '仕入先への発注・欠品の連絡と、売場のPOP・チラシの文、客からの問い合わせへの回答の下書き', 42, 31.5),
    ('大和郡山市', 'yamatokoriyama', '運輸業・郵便業', '道路貨物運送と倉庫（県北部の配送・中距離輸送）', {'道路貨物運送', '運送', '倉庫'}, 96,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録・入出庫の記録の集計', 42, 32.0),
    ('生駒市', 'ikoma', '医療・福祉', '介護老人保健施設（通所リハビリ・訪問リハビリを併設）', {'介護老人保健施設', '介護', 'リハビリ'}, 112,
     'リハビリ・ケアの記録の要約と、入所・退所の説明文書、家族への近況の連絡文の作成', 45, 32.0),
    ('橿原市', 'kashihara', '医療・福祉', '病院（回復期リハビリテーション病棟・療養病棟と外来）', {'医療', '病院', 'リハビリ'}, 150,
     'リハビリの実施記録の要約と、退院前カンファレンスの記録、患者・家族への説明文書、紹介元の医療機関への報告書の作成', 57, 32.0),
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
    cut_line = re.compile(r"毎月勤労統計|総実労働|ヒキツギAI|月額|差し引|引いた|引いても|払っても|払った|残り|残ります|初期費用|回収|戻る|取り戻せる")
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
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | ×4 を3で割った余り |")
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
            print(f"  NG {city} の時間 {h} は近畿3県の割り当て（×4 を{MOD_N}で割った余り {MOD_R}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 奈良県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 奈良県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは奈良県の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == N_PAGES else "NG")


def free(ind, lo, hi):
    """業種 ind で、lo〜hi 時間の空いている（時間, 万円）を並べる（余り0の時間だけ）"""
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
