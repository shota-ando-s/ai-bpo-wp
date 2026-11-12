#!/usr/bin/env python3
"""兵庫県41市町の試算の割り当てを計算し、重なりを確かめる（親が統計の調査のあとすぐ決めた、2026-11-11）。

data/area/nara/_calc.py を元に作った。県ページ（/area/hyogo/）には試算を入れないので、PLAN は41行。値の当て方は _assign.py。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **静岡・愛知・三重・京都・兵庫の取り決め**（data/area/_tokai/shared.md）: 4府県は月の削減時間×4 を4で割った余りで時間を分けた。
     兵庫は端数を限らないが、4府県の PLAN（push されていれば）と既存の全県と照合し、**重なったら兵庫側が直す**
  1. 41ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、兵庫県を除く）の「## 試算」の節に出てくる
     「◯時間」「◯万円」の値と重ならない（拾い方は奈良県の _calc.py と同じ）
  3. 全県の data/area/*/_calc.py の PLAN（兵庫県を除く。glob で全部読む。静岡・愛知・三重・京都・北海道を含む）の
     月の削減時間・月の時間換算額と重ならない。読めないファイルは NG にせず警告。REQUIRED の県はファイルがなければ NG
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md などの事例の会社と同じにならない（CASES と照合）
  6. slug が _brief.md の41市町と一致する
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
  8. 県ページには試算を入れない（PLAN は41行）
  9. 仮の会社の従業員数が、その市町の民営従業者数・選んだ中分類の従業者数（stats.md、経済センサス2021）を超えない
使い方: python3 data/area/hyogo/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/hyogo/_calc.py free 製造業 30 200   （既存・他県・兵庫の中と重ならない時間と金額の候補を出す）
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
SELF = "hyogo"
PREF_JA = "兵庫県"
MOD_N, MOD_R = 4, None  # 兵庫は端数を限らない（余りは表示だけ）
N_PAGES = 41

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
    # 市（29）
    "kobe", "himeji", "amagasaki", "akashi", "nishinomiya", "sumoto", "ashiya-city", "itami", "aioi", "toyooka-city",
    "kakogawa", "ako", "nishiwaki", "takarazuka", "miki-city", "takasago", "kawanishi-city", "ono-city", "sanda",
    "kasai", "tambasasayama", "yabu", "tamba", "minamiawaji", "asago", "awaji", "shiso", "kato", "tatsuno-city",
    # 町（12）
    "inagawa", "taka", "inami-town-hyogo", "harima", "ichikawa", "fukusaki", "kamikawa", "taishi", "kamigori", "sayo",
    "kami-town-hyogo", "shinonsen",
}
VILLAGES = set()  # 兵庫県に村はない

# 照合が必須の県（2026-11-11 に _calc.py がある県）。ファイルがなければ NG。ほかに見つかった _calc.py（静岡・愛知・三重・京都など）も全部読む
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima",
            "hokkaido", "ibaraki", "tochigi", "gunma", "okinawa", "wakayama", "shiga", "nara")

# cases.md（2026-11-11）の会社。(会社名, 市町〔県外は「県外」〕, 業態のキー, 従業員数〔(下限, 上限)。分からなければ None〕, AI の事例か)
# cases2.md・cases_outside.md・subsidy_*_areas.md ができたら行を足して再実行する
CASES = [
    ("神戸化成（食品添加物の製造、61名。AI は開発中）", "神戸市", {"食品添加物", "食料品", "着色料"}, (61, 61), True),
    ("北神地域振興（道の駅の運営、AI 需要予測。数値なし）", "神戸市", {"道の駅", "小売", "農産物直売"}, None, True),
    ("エヌエスケーケー（auショップの運営、63名。他県で使用済み）", "神戸市", {"携帯電話販売", "小売"}, (63, 63), True),
    ("旭光電機（センサ・自動ドアのコントローラ、204名）", "神戸市", {"電気機械", "センサ", "制御機器"}, (204, 204), True),
    ("ネオスタイル（老人ホームの紹介、面談の記録の解析）", "神戸市", {"老人ホーム紹介", "介護"}, None, True),
    ("ドリームヒルズ滝山（介護老人保健施設、県の介護の表彰。AI の数値なし）", "神戸市", {"介護老人保健施設", "介護"}, None, False),
    ("川崎重工業（大企業）", "神戸市", {"輸送用機械", "船舶", "重工業"}, None, True),
    ("神明ホールディングス（米穀・青果卸、大企業グループ）", "神戸市", {"米穀卸", "青果卸", "卸売"}, None, True),
    ("香山組（建設業、ペーパーレス。AI ではない）", "尼崎市", {"建設", "総合工事業"}, None, False),
    ("JR西日本カスタマーリレーションズ（コールセンター、大企業グループ）", "尼崎市", {"コールセンター"}, None, True),
    ("関通ホールディングス（物流、大企業。グループ会社が尼崎・三田・宝塚）", "尼崎市", {"物流", "倉庫", "倉庫業", "EC物流"}, None, True),
    ("関通のグループ会社（物流）", "三田市", {"物流", "倉庫", "倉庫業"}, None, True),
    ("関通のグループ会社（物流）", "宝塚市", {"物流", "倉庫", "倉庫業"}, None, True),
    ("神戸規志税理士事務所（Gemini で記帳、月70時間。職員数は未確認）", "明石市", {"税理士", "会計事務所", "士業"}, None, True),
    ("医療法人せいふう会 川西リハビリテーション病院（medimo、グループの値）", "川西市", {"病院", "リハビリ", "医療"}, None, True),
    ("医療法人せいふう会（主たる事務所）", "猪名川町", {"病院", "リハビリ", "医療"}, None, True),
    ("ダイハツメタル（本店 川西市、956名。工場は島根）", "川西市", {"金属製品", "軸受"}, (956, 956), True),
    ("フォレスト（注文住宅、生成AI研修）", "姫路市", {"注文住宅", "工務店", "住宅"}, None, True),
    ("日高食品工業（昆布などの海産物の加工）", "姫路市", {"海産物加工", "食料品", "昆布"}, None, True),
    ("澤田棉行（繊維原料・不織布、約20人。他県で使用済み）", "姫路市", {"繊維", "不織布", "繊維原料"}, (20, 20), True),
    ("関西陸運（家具・事務機材の配送、AI の語なし）", "姫路市", {"運送", "道路貨物運送"}, None, False),
    ("龍野実業建築家（不動産の生成AI研修）", "たつの市", {"不動産", "建築"}, None, True),
    ("ミツテック（県立工業技術センターと深層学習の外観検査の共同研究）", "淡路市", {"金属加工", "部品加工", "外観検査"}, None, True),
    ("マイ・マート（スーパー、約200人。他県で使用済み）", "洲本市", {"スーパー", "食料品小売", "小売"}, (200, 200), True),
    ("城崎温泉 但馬屋（12室・15人。他県で使用済み）", "豊岡市", {"旅館", "宿泊", "温泉旅館"}, (15, 15), True),
    ("西村屋（城崎温泉。観光庁の実証）", "豊岡市", {"旅館", "宿泊", "温泉旅館"}, None, True),
    ("稲坂油圧機器（AI 外観検査、280名。他県で使用済み）", "加東市", {"油圧機器", "はん用機械", "機械部品"}, (280, 280), True),
    ("アスカカンパニー（射出成形、約250名。他県で使用済み）", "加東市", {"プラスチック製品", "射出成形"}, (250, 250), True),
    ("ブレイン（BakeryScan、23名。提供側）", "西脇市", {"情報サービス", "画像認識", "AI製品開発"}, (23, 23), True),
    ("オオナガ（事例集では稲美町、25人。本店は神戸市西区）", "稲美町", {"機械部品", "金属加工"}, (25, 25), True),
    ("明石機械工業（約1,500名、大企業）", "稲美町", {"輸送用機械", "変速機"}, (1500, 1500), True),
    ("キング醸造（みりん、AI 需要予測。他県で使用済み）", "稲美町", {"みりん", "食料品", "調味料", "醸造"}, None, True),
    ("ロザイ工業 赤穂工場（AQUSEL、220名。本店県外）", "赤穂市", {"産業廃棄物", "選別", "リサイクル"}, (220, 220), True),
    ("福伸電機（823名、AI ではない）", "福崎町", {"電気機械", "検査装置"}, (823, 823), False),
    ("サグリ（提供側）", "丹波市", {"情報サービス", "農業"}, None, True),
    ("ホープファーム（アイガモロボ、AI の記載なし）", "丹波市", {"農業"}, None, False),
    # cases2.md（2026-11-11）の会社（D1 が足した）
    ("HKテクノロジー（化学吸着フィルターの製造、29名。AI 搭載のロボットアーム）", "神戸市", {"フィルター", "化学吸着フィルター", "化学"}, (29, 29), True),
    ("兵庫精密工業所（機械加工部品の製造・組立、75名。刻印読取は AI の語なし）", "神戸市", {"機械部品", "金属加工", "切削加工", "輸送用機械"}, (75, 75), True),
    ("兵庫精密工業所 社南坊工場（機械加工部品）", "加東市", {"機械部品", "金属加工", "切削加工"}, (75, 75), True),
    ("兵庫精密工業所 篠山工場（機械加工部品）", "丹波篠山市", {"機械部品", "金属加工", "切削加工"}, (75, 75), True),
    ("ナガサワ文具センター（文房具専門店。ペアマインドとの協業）", "神戸市", {"文房具", "小売"}, None, True),
    ("ペアマインド（県立大発、AI のインテリア絵画。提供側）", "神戸市", {"情報サービス", "AI製品開発"}, None, True),
    ("テラアクソン（特殊詐欺監視 AI。提供側）", "神戸市", {"情報サービス", "AI製品開発"}, None, True),
    ("GEOソリューションズ（空中写真測量・ドローン点検の AI 解析。提供側）", "西宮市", {"測量", "技術サービス", "情報サービス"}, None, True),
    ("恵美須屋（市の補助金の計画名だけ。業種・規模は未確認）", "豊岡市", {"業種未確認"}, None, True),
    # cases_outside.md（県外。D2 で詳述ページを決めた。2026-11-12 に親が足した）
    ("FIKA（東京都、宿泊12人、AI チャットボット。省力化ナビ）", "県外", {"宿泊", "旅館", "ホテル", "ゲストハウス"}, (12, 12), True),
    ("川島製作所（埼玉県、包装機 約300人、AI 見積。省力化ナビ）", "県外", {"包装機", "生産用機械", "機械"}, (300, 300), True),
    ("中央運送（東京都、200人、AI 点呼。省力化ナビ）", "県外", {"運送", "道路貨物運送", "トラック運送"}, (200, 200), True),
]

# 市町の民営従業者数と、試算に選んだ中分類の事業所数・従業者数（経済センサス 2021年6月1日、民営。stats.md・e-Stat ec_6_1）
# slug: (民営従業者, 中分類, 中分類の事業所, 中分類の従業者)
STAT = {
    "kobe": (725828, "倉庫業", 257, 5440),
    "himeji": (256076, "設備工事業", 612, 5651),
    "amagasaki": (194617, "金属製品製造業", 345, 4841),
    "akashi": (99773, "飲食料品小売業", 494, 7268),
    "nishinomiya": (153089, "飲料・たばこ・飼料製造業", 17, 791),
    "sumoto": (16963, "宿泊業", 45, 1503),
    "ashiya-city": (23586, "社会保険・社会福祉・介護事業", 119, 3286),
    "itami": (68928, "道路貨物運送業", 116, 2876),
    "aioi": (11061, "食料品製造業", 16, 533),
    "toyooka-city": (35649, "なめし革・同製品・毛皮製造業", 121, 1248),
    "kakogawa": (88858, "機械器具小売業", 246, 1709),
    "ako": (17459, "宿泊業", 25, 509),
    "nishiwaki": (15430, "繊維工業", 177, 1299),
    "takarazuka": (54613, "社会保険・社会福祉・介護事業", 348, 7859),
    "miki-city": (35072, "その他の卸売業", 127, 1215),
    "takasago": (41174, "技術サービス業（他に分類されないもの）", 89, 3222),
    "kawanishi-city": (37548, "飲食料品小売業", 186, 3147),
    "ono-city": (24270, "金属製品製造業", 140, 1624),
    "sanda": (41031, "社会保険・社会福祉・介護事業", 116, 3141),
    "kasai": (22112, "道路貨物運送業", 52, 1652),
    "tambasasayama": (15746, "飲食料品小売業", 121, 1256),
    "yabu": (8415, "宿泊業", 63, 347),
    "tamba": (25834, "プラスチック製品製造業（別掲を除く）", 41, 698),
    "minamiawaji": (17898, "飲食料品卸売業", 94, 791),
    "asago": (12847, "飲食店", 135, 812),
    "awaji": (17159, "その他の製造業", 48, 497),
    "shiso": (13919, "食料品製造業", 266, 1953),
    "kato": (21773, "その他の製造業", 40, 681),
    "tatsuno-city": (31839, "なめし革・同製品・毛皮製造業", 137, 1120),
    "inagawa": (6810, "社会保険・社会福祉・介護事業", 28, 921),
    "taka": (7397, "社会保険・社会福祉・介護事業", 40, 980),
    "inami-town-hyogo": (14515, "生産用機械器具製造業", 32, 800),
    "harima": (11531, "運輸に附帯するサービス業", 12, 316),
    "ichikawa": (3782, "プラスチック製品製造業（別掲を除く）", 12, 237),
    "fukusaki": (11614, "金属製品製造業", 25, 811),
    "kamikawa": (3338, "社会保険・社会福祉・介護事業", 12, 412),
    "taishi": (11680, "飲食店", 119, 999),
    "kamigori": (4659, "社会保険・社会福祉・介護事業", 27, 650),
    "sayo": (6654, "総合工事業", 81, 448),
    "kami-town-hyogo": (5847, "食料品製造業", 72, 787),
    "shinonsen": (5075, "宿泊業", 37, 499),
}

# (市町, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])（奈良と同じ9列）。_assign.py の出力
# 2026-11-12: 養父市は北海道 下川町（上川の PLAN、あとから push）と金額 28.0万円が重なったので、兵庫側で 24名・8人×55.75h → 54名・36人×40.5h に直した（_assign.py では出ない値。手で直した）
# 大企業の工場と読める業種（高砂市のはん用・生産用機械・化学、明石市・三田市の輸送用機械、加東市の情報通信機械、太子町の電子部品、播磨町の化学など）は使わない
PLAN = [
    ('神戸市', 'kobe', '運輸業・郵便業', '倉庫業と港湾の貨物の運送（輸出入の貨物の保管・配送）', {'運送', '港湾運送', '倉庫業'}, 140,
     '荷主からの在庫・入出庫・配送状況の問い合わせへの回答と、入出庫の記録・在庫報告の作成、通関業者・配送業者への手配の連絡', 42, 37.5),
    ('姫路市', 'himeji', '建設業', '設備工事業（工場・プラントの配管・電気設備の工事と保守）', {'設備工事', '配管工事', '電気工事'}, 96,
     '施主・元請からの工程・仕様の問い合わせへの回答と、施工計画書・安全書類の作成、点検・保守の報告書の下書き', 44, 37.75),
    ('尼崎市', 'amagasaki', '製造業', '金属製品（機械部品の切削・板金加工）', {'金属製品', '切削加工', '板金'}, 58,
     '取引先からの図面変更・納期の問い合わせへの回答と、見積書・作業指示書の作成、検査記録・不具合の報告書の取りまとめ', 38, 37.5),
    ('明石市', 'akashi', '卸売業・小売業', '鮮魚・水産加工品の小売と卸（店舗と飲食店への配達）', {'水産物卸', '鮮魚', '食料品小売', '水産物小売'}, 44,
     '飲食店・客からの入荷・価格・配達の問い合わせへの回答と、注文の取りまとめ、商品の説明文・贈答の案内文の作成', 34, 40.5),
    ('西宮市', 'nishinomiya', '製造業', '飲料（清酒の製造と販売）', {'清酒', '酒造', '飲料'}, 52,
     '酒販店・飲食店・通販の取引先からの在庫・出荷・商品の問い合わせへの回答と、商品の説明文、製造・出荷の記録の取りまとめ', 36, 39.25),
    ('洲本市', 'sumoto', '宿泊・飲食サービス業', 'ホテル・旅館（温泉の個人客・団体）', {'温泉旅館', 'ホテル', '宿泊', '旅館'}, 72,
     '予約サイト・メールの問い合わせへの返信の下書きと、団体の見積書・送迎の案内文、館内案内の多言語の文の作成', 43, 38.0),
    ('芦屋市', 'ashiya-city', '医療・福祉', '住宅型有料老人ホーム（訪問介護を併設）', {'訪問介護', '有料老人ホーム', '介護'}, 64,
     'ケア記録の清書と、入居者の家族への近況の連絡文、入居の問い合わせへの返信の下書き', 40, 38.5),
    ('伊丹市', 'itami', '運輸業・郵便業', '道路貨物運送（阪神間の工場・倉庫の配送）', {'運送', '道路貨物運送'}, 66,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計', 40, 37.75),
    ('相生市', 'aioi', '製造業', '食料品（かきなどの水産加工品の製造）', {'食料品', 'かき', '水産加工'}, 34,
     '小売店・通販の取引先からの数量・規格・賞味期限の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 26, 50.5),
    ('豊岡市', 'toyooka-city', '製造業', 'かばん（なめし革・同製品。かばん・袋物の製造と卸）', {'かばん', '袋物', 'なめし革・同製品'}, 46,
     '問屋・小売店・通販の取引先からの在庫・納期・仕様の問い合わせへの回答と、商品の説明文、生産の指示書の取りまとめ', 35, 39.0),
    ('加古川市', 'kakogawa', '卸売業・小売業', '自動車の販売と整備（新車・中古車の店舗と整備工場）', {'機械器具小売', '自動車整備', '自動車販売'}, 48,
     '客からの見積・整備の予約・車検の問い合わせへの回答と、見積書・整備の記録の作成、メーカー・部品商への照会文の下書き', 36, 37.25),
    ('赤穂市', 'ako', '宿泊・飲食サービス業', '旅館（温泉地の個人客と団体）', {'温泉旅館', '宿泊', '旅館'}, 38,
     '予約サイト・電話・メールの問い合わせへの返信の下書きと、団体の見積書、館内・周辺の案内文の作成', 28, 47.75),
    ('西脇市', 'nishiwaki', '製造業', '繊維（播州織の先染め織物の製織）', {'繊維', '先染め織物', '織物', '播州織'}, 31,
     '産元商社・アパレルの取引先からの納期・在庫・仕様の問い合わせへの回答と、生地の仕様書、生産の記録の取りまとめ', 24, 52.75),
    ('宝塚市', 'takarazuka', '医療・福祉', '特別養護老人ホーム（短期入所・通所介護を併設）', {'介護', '短期入所', '通所介護', '特別養護老人ホーム'}, 92,
     'ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成', 42, 38.0),
    ('三木市', 'miki-city', '卸売業・小売業', '金物の卸売（大工道具・作業工具・刃物の問屋）', {'作業工具', '金物卸', '金物', '卸売'}, 42,
     '小売店・ホームセンターの取引先からの在庫・価格・納期の問い合わせへの回答と、メーカーへの発注・照会の連絡、見積書・商品の説明文の作成', 33, 44.0),
    ('高砂市', 'takasago', '学術研究・専門技術サービス', '技術サービス（工場の設備の設計・検査・分析の受託）', {'設計', '検査', '分析', '技術サービス'}, 45,
     '依頼元との打合せ記録の要約と、検査・分析の報告書の下書き、見積書・受付の連絡文の作成', 24, 37.5),
    ('川西市', 'kawanishi-city', '卸売業・小売業', '飲食料品の小売（住宅地の食品スーパーを数店舗）', {'食料品小売', 'スーパー', '小売'}, 82,
     '仕入先への発注・欠品の連絡と、売場のPOP・チラシの文、客からの問い合わせへの回答の下書き', 41, 38.0),
    ('小野市', 'ono-city', '製造業', '金属製品（はさみ・刃物の製造）', {'金属製品', 'はさみ', '刃物'}, 29,
     '問屋・理美容ディーラーなどの取引先からの在庫・仕様・納期の問い合わせへの回答と、商品の説明文、出荷・修理の記録の取りまとめ', 20, 56.75),
    ('三田市', 'sanda', '医療・福祉', '介護老人保健施設（通所リハビリを併設）', {'リハビリ', '介護', '介護老人保健施設'}, 76,
     'リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成', 44, 38.0),
    ('加西市', 'kasai', '運輸業・郵便業', '道路貨物運送（工業団地の部品・製品の輸送）', {'運送', '道路貨物運送'}, 62,
     '荷主からの配送状況・納品の問い合わせへの回答と、配車の連絡、運行の記録・点呼記録の取りまとめ', 39, 38.0),
    ('丹波篠山市', 'tambasasayama', '卸売業・小売業', '特産品の小売（黒大豆などの農産物・加工品の店舗と通販）', {'食料品小売', '特産品', '通信販売', '小売'}, 36,
     '通販・店舗の客からの在庫・配送・贈答の問い合わせへの回答と、商品の説明文、注文の取りまとめ', 28, 45.25),
    ('養父市', 'yabu', '宿泊・飲食サービス業', '旅館・民宿（スキー場・高原の観光客と合宿の団体）', {'民宿', '宿泊', '旅館'}, 54,
     '予約・団体の問い合わせへの返信の下書きと、合宿・団体の見積書、送迎・食事の案内文の作成', 36, 40.5),
    ('丹波市', 'tamba', '製造業', 'プラスチック製品（工業用部品の射出成形）', {'工業用部品', 'プラスチック製品', '射出成形'}, 40,
     '取引先からの金型・納期・品質の問い合わせへの回答と、成形条件・検査記録の取りまとめ、不具合の報告書の下書き', 31, 43.0),
    ('南あわじ市', 'minamiawaji', '卸売業・小売業', '飲食料品の卸売（玉ねぎなどの農産物の集荷・出荷）', {'青果卸', '農産物卸', '玉ねぎ', '飲食料品卸'}, 33,
     '市場・小売の取引先からの入荷・規格・価格の問い合わせへの回答と、出荷の手配の連絡、出荷・請求の記録の取りまとめ', 16, 49.25),
    ('朝来市', 'asago', '宿泊・飲食サービス業', '飲食店（観光客と団体を受け入れる食事処・土産物の店）', {'食事処', '飲食サービス', '飲食店'}, 30,
     '予約・団体の問い合わせへの返信の下書きと、団体の見積書・献立の案内文、多言語のメニューの文の作成', 16, 57.25),
    ('淡路市', 'awaji', '製造業', '線香（その他の製造業。線香・お香の製造と卸）', {'線香', 'お香', 'その他の製造業'}, 32,
     '問屋・小売店・通販の取引先からの在庫・納期・仕様の問い合わせへの回答と、商品の説明文、出荷の記録の取りまとめ', 20, 57.25),
    ('宍粟市', 'shiso', '製造業', '食料品（手延べ素麺の製造）', {'素麺', '麺類', '手延べ素麺', '食料品'}, 37,
     '問屋・組合・量販店の取引先からの規格・原材料・アレルゲンの問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 28, 48.5),
    ('加東市', 'kato', '製造業', '釣針・釣具（その他の製造業。釣針の加工と卸）', {'釣針', 'その他の製造業', '釣具'}, 35,
     '釣具店・問屋・海外の取引先からの在庫・仕様・納期の問い合わせへの回答と、商品の説明文、出荷の記録の取りまとめ', 28, 44.75),
    ('たつの市', 'tatsuno-city', '製造業', '皮革（なめし革の製造と仕上げ）', {'なめし革・同製品', '皮革', 'なめし革'}, 28,
     '革製品メーカー・問屋の取引先からの在庫・色・納期の問い合わせへの回答と、仕様書・商品の説明文、生産の記録の取りまとめ', 18, 56.5),
    ('猪名川町', 'inagawa', '医療・福祉', '通所介護と訪問介護（送迎を含む）', {'訪問介護', '介護', '通所介護'}, 41,
     '利用の記録と個別機能訓練計画書の下書き、家族への連絡帳の文、サービス担当者会議の記録の作成', 27, 47.0),
    ('多可町', 'taka', '医療・福祉', '特別養護老人ホーム（短期入所を併設）', {'介護', '短期入所', '特別養護老人ホーム'}, 50,
     'ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成', 36, 40.25),
    ('稲美町', 'inami-town-hyogo', '製造業', '生産用機械（工場の省力化装置・治具の設計製作）', {'治具', '生産用機械', '省力化装置'}, 27,
     '顧客との仕様の打合せ記録の要約と、見積書・取扱説明書・設計変更の連絡書の下書き', 20, 52.75),
    ('播磨町', 'harima', '運輸業・郵便業', '運輸に附帯するサービス（港湾の荷役・梱包と通関の手配）', {'通関', '港湾運送', '運輸附帯', '梱包'}, 26,
     '荷主からの船積み・入出庫の問い合わせへの回答と、作業の手配の連絡、作業・出荷の記録の取りまとめ', 20, 45.25),
    ('市川町', 'ichikawa', '製造業', 'プラスチック製品（日用品・工業用部品の成形）', {'プラスチック製品', '射出成形', '日用品'}, 22,
     '取引先からの図面・仕様の変更と納期の問い合わせへの回答と、成形条件・検査記録の取りまとめ、不具合の報告書の下書き', 12, 57.25),
    ('福崎町', 'fukusaki', '製造業', '金属製品（製缶・溶接による機械部品の製造）', {'溶接', '製缶', '金属製品'}, 21,
     '取引先からの図面変更・納期の問い合わせへの回答と、溶接・検査の記録の取りまとめ、作業手順書の改訂の下書き', 12, 52.75),
    ('神河町', 'kamikawa', '医療・福祉', '認知症対応型グループホームと小規模多機能型居宅介護', {'小規模多機能', '介護', 'グループホーム'}, 25,
     '生活記録の清書と、運営推進会議の議事録、家族への便りの文の作成', 20, 48.25),
    ('太子町', 'taishi', '宿泊・飲食サービス業', '飲食店（幹線道路沿いの食堂・ファミリー向けの店を数店舗）', {'飲食サービス', '飲食店'}, 39,
     '予約・団体の問い合わせへの返信の下書きと、仕入先への発注の連絡、店頭・SNSの案内文と多言語のメニューの文の作成', 31, 49.0),
    ('上郡町', 'kamigori', '医療・福祉', '訪問看護と居宅介護支援', {'医療', '居宅介護支援', '訪問看護'}, 23,
     '訪問の記録の清書と、主治医への報告書・計画書の下書き、家族への連絡文の作成', 16, 49.75),
    ('佐用町', 'sayo', '建設業', '総合工事業（道路・河川の土木工事、公共工事が中心）', {'土木', '総合工事業', '建設'}, 53,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真・出来形の記録の整理', 38, 38.0),
    ('香美町', 'kami-town-hyogo', '製造業', '食料品（カニ・干物などの水産加工品の製造と通販）', {'食料品', 'カニ', '干物', '水産加工'}, 43,
     '小売店・通販の客からの数量・配送・賞味期限の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 34, 36.5),
    ('新温泉町', 'shinonsen', '宿泊・飲食サービス業', '旅館（湯村温泉の個人客と団体）', {'温泉旅館', '宿泊', '旅館'}, 47,
     '予約サイト・メールの問い合わせへの返信の下書きと、団体の見積書・送迎の案内文、館内案内の多言語の文の作成', 37, 37.0),
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
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | ×4 を4で割った余り（参考） |")
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
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 兵庫県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 兵庫県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは兵庫県の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == N_PAGES else "NG")


def free(ind, lo, hi):
    """業種 ind で、lo〜hi 時間の空いている（時間, 万円）を並べる"""
    h_used, m_used = used_values()
    mine_h = {Decimal(str(p[7])) * Decimal(str(p[8])) * Decimal("0.25") for p in PLAN}
    mine_m = {man(Decimal(str(p[7])) * Decimal(str(p[8])) * Decimal("0.25") * RATE[p[2]]) for p in PLAN}
    h = Decimal(str(lo))
    out = []
    while h <= Decimal(str(hi)):
        if (h * 4) % 1 == 0 and h not in h_used and h not in mine_h:
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
