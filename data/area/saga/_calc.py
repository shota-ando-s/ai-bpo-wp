#!/usr/bin/env python3
"""佐賀県20市町の試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-11-04）。

data/area/okayama/_calc.py を元に作った。県ページ（/area/saga/）には試算を入れないので、PLAN は20行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **九州7県の取り決め**: 月の削減時間（0.25時間刻み）×4 を7で割った余りが 1（佐賀県）の時間だけを使う
     （0.25, 2.0, 3.75, 5.5, … の1.75時間刻み。data/area/_kyushu/shared.md）
  1. 20ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、佐賀県を除く）の「## 試算」の節に出てくる
     「◯時間」「◯万円」の値と重ならない。拾い方は岡山県の _calc.py と同じ
  3. 全県の data/area/*/_calc.py の PLAN（佐賀県を除く。glob で全部読む）の月の削減時間・月の時間換算額と重ならない。
     REQUIRED の10県はファイルがなければ NG。九州の他県（福岡・熊本・宮崎・鹿児島など）は後から入っても glob で読む。
     PLAN の形が違って読めない県は READERS に県ごとの読み方を足す。読めない県があれば NG
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md（・cases2.md）の事例の会社と同じにならない（CASES と照合）
     - AI の事例で、業態のキーが重なり、従業員数が事例の範囲（下限×0.85〜上限×1.15）に入る → NG
     - AI の事例で、業態のキーが重なり、同じ市町で、事例の従業員数が分からない → NG（その会社の値と読まれるため）
     - 業種が確かめられていない事例（キー「業種未確認」）と同じ市町 → 参考として表示（NG にしない）
     - AI ではない事例と業態・規模が近い → 参考として表示
  6. slug が _brief.md の20市町と一致する（佐賀市は saga-city、大町町は omachi-town、白石町は shiroishi-town）
  7. 試算の業種が wages.md にある（農業・漁業・林業は試算の業種にしない）
使い方: python3 data/area/saga/_calc.py   （末尾に OK / NG を出す）
"""
import ast
import glob
import os
import re
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ART = os.path.join(ROOT, "articles")
HERE = os.path.dirname(os.path.abspath(__file__))
SELF = "saga"
KYUSHU_MOD = 1  # 九州7県の割り当て（月の削減時間×4 を7で割った余り）。佐賀県は 1

# wages.md の人件費時給（時給①×1.2 を十円単位に丸めた値。記事でも「約◯円」と書く値）。
# 他県の PLAN（山口・岡山・長崎・大分）が不動産・学術研究・情報通信を使っているので、他県の PLAN を読むために9業種とも入れる
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
# 佐賀県の試算で使ってよい業種（wages.md の表にあり、農林漁業でないもの）
WAGES_MD = set(RATE)

SLUGS = {"saga-city", "karatsu", "tosu", "taku", "imari", "takeo", "kashima", "ogi", "ureshino", "kanzaki",
         "yoshinogari", "kiyama", "kamimine", "miyaki", "genkai", "arita", "omachi-town", "kohoku",
         "shiroishi-town", "tara"}

# 照合が必須の県（2026-11-04 にある _calc.py）。ファイルがなければ NG
REQUIRED = ("gifu", "hiroshima", "nagano", "nagasaki", "oita", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi")


def read_plan_standard(src):
    """岡山県の形の PLAN（`PLAN = [` から行頭の `]` まで。各行の [0]=市町村, [2]=業種, [-2]=対象人数, [-1]=1人の月の業務量）"""
    i = src.index("PLAN = [")
    j = src.index("\n]\n", i)
    rows = ast.literal_eval(src[i + 7:j + 2])
    return [(r[0], r[2], r[-2], r[-1]) for r in rows]


# 県ごとの PLAN の読み方。2026-11-04 の10県はすべて岡山県と同じ形（read_plan_standard）で読めた。
# 形の違う県が入ったら、ここに "県": 関数 を足す（関数は src を受け取り (市町村, 業種, 対象人数, 1人の業務量) のリストを返す）
READERS = {}

# cases.md・cases_outside.md・subsidy_a_areas.md（採択の手がかり）の事例の会社（2026-11-04）
# (会社名, 市町〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・使用済み・計画を含む〕)
# cases2.md（2026-11-04 の補充調査）の会社も足した（「# cases2.md」の行）。cases2.md が更新されたら足して再実行する
CASES = [
    # 佐賀市
    ("ビープラスト（生成AI、市の事例集の約60%）", "佐賀市", {"映像制作", "Web制作", "広告", "デザイン"}, None, True),
    ("レグナテック（生成AIの提案画像、数値なし）", "佐賀市", {"家具", "木製家具", "木材・木製品"}, None, True),
    ("佐賀玉屋（AIカメラ、2022年）", "佐賀市", {"百貨店", "小売"}, None, True),
    ("中野建設（AI は鉄筋検測、数値は RPA）", "佐賀市", {"建設", "総合工事業"}, None, True),
    ("バイオテックス（マナビDX Quest、未確認）", "佐賀市", {"建設"}, None, True),
    ("松尾建設（県の実証、列車検知。県内大手）", "佐賀市", {"建設", "鉄道工事"}, None, True),
    ("イケマコ（オプティムの実証、2017年）", "佐賀市", {"農業", "大豆"}, None, True),
    ("美川眼科医院（オプティムの臨床研究、2018年）", "佐賀市", {"医療", "眼科", "診療所"}, None, True),
    ("スーパーモリナガ（県の実証、2020年度）", "佐賀市", {"小売", "食品スーパー"}, None, True),
    ("福博印刷（県の実証、ベンダー側）", "佐賀市", {"印刷", "情報サービス"}, (216, 216), True),
    ("三福海苔・サン海苔（市の事例集、AIではない）", "佐賀市", {"のり加工", "水産加工", "食料品"}, None, False),
    ("市の事例集の6社（千代田館・ミズマチ・ミズ・ブラステム・丸秀醤油・西九州月星、AIではない）", "佐賀市",
     {"宿泊", "小売", "金属表面処理", "醤油", "食料品", "卸売"}, None, False),
    ("ソロン（DXセレクション、AIの記述なし）", "佐賀市", {"業種未確認"}, None, False),
    ("佐賀広告センター（将来の話）", "佐賀市", {"広告"}, None, False),
    ("アグリ・クリエイティブ・シード（試作、農場は福岡県）", "佐賀市", {"農業", "いちご"}, None, False),
    # 多久市
    ("山口産業（生成AI研修、数値なし）", "多久市", {"膜構造建築", "テント", "建設"}, None, True),
    ("アシス（AIカメラの精算機、計画と発言）", "多久市", {"小売", "飲食店", "カフェ"}, None, True),
    ("ECO-5（県の実証、鳥獣認識AI）", "多久市", {"鳥獣害防止装置"}, None, True),
    # 伊万里市
    ("まるきん（NotebookLM・ChatGPT、数値なし）", "伊万里市", {"釣具", "アウトドア用品", "小売"}, None, True),
    ("東方会（議事録に NotebookLM、184名）", "伊万里市", {"社会福祉法人", "障害福祉", "保育", "介護"}, (184, 184), True),
    # 有田町
    ("セイブ（碍子の検査、県の実証 2019年）", "有田町", {"碍子", "電気用陶磁器", "窯業・土石"}, None, True),
    # 鳥栖市
    ("九動（生成AIの計画）", "鳥栖市", {"実験動物", "受託検査"}, None, True),
    # 唐津市
    ("サンエスライン（マナビDX Quest の需要予測、未確認）", "唐津市", {"卸売", "小売"}, None, True),
    ("青木ブロイラー（使用済み・岩手県一関市）", "唐津市", {"農業", "ブロイラー", "養鶏"}, None, True),
    # 鹿島市
    ("森鉄工（AI-OCR 構築中）", "鹿島市", {"生産用機械", "液圧プレス", "鍛圧機械"}, None, True),
    ("織田病院（使用済み・愛媛県東温市）", "鹿島市", {"医療", "病院"}, None, True),
    # 神埼市
    ("井上製麺（AI-OCR のデモ、2023年）", "神埼市", {"食料品", "製麺"}, None, True),
    # 吉野ヶ里町
    ("KITSライン（AI-OCR の計画、2022年）", "吉野ヶ里町", {"物流", "運送", "道路貨物運送"}, None, True),
    ("ロケモAI（佐賀大学・町との協定、2020年）", "吉野ヶ里町", {"情報サービス"}, None, True),
    ("ゴール 九州工場（IoT、AIではない）", "吉野ヶ里町", {"金属製品", "鍵・錠前"}, None, False),
    # 太良町・白石町
    ("山本農園（音声AIの電話注文をテスト）", "太良町", {"農業", "果実", "みかん"}, None, True),
    ("JAさが白石地区×オプティム（県の実証、2020年度、不成功）", "白石町", {"農業", "野菜"}, None, True),
    # 武雄市・玄海町（AIではない）
    ("土橋産業（ChatGPT は予定だけ）", "武雄市", {"建設", "住宅建築"}, None, False),
    ("上場食肉（配膳ロボット、AIの事例にしない）", "玄海町", {"食肉販売", "飲食店", "小売"}, None, False),
    # 補助金の採択・支援先（subsidy_a_areas.md。所在・規模は確かめていない）
    # cases2.md（2026-11-04。大栄工業・日興食品・玄海漬の所在は cases2.md の法人番号の照合による）
    ("椎原寿恵会（チャットGPTでケアプランのひな型、佐賀新聞、387名）", "鳥栖市",
     {"社会福祉法人", "特別養護老人ホーム", "介護", "障害福祉", "保育"}, (387, 387), True),
    ("大栄工業（NEXT 採択、AI 姿勢推定の検査装置。採択まで）", "みやき町", {"プラスチック製品", "成形", "検査装置"}, None, True),
    ("石丸食肉産業（AI-OCR の検討、2023年）", "みやき町", {"食肉販売", "小売"}, None, True),
    ("日興食品（NEXT 採択、AI 画像解析の果肉選別。採択まで）", "佐賀市", {"食料品", "果実加工"}, None, True),
    ("新成工務店（AI は将来の希望、事例にしない）", "佐賀市", {"建設", "工務店"}, None, False),
    ("玄海漬（R7 DX伴走、データ活用。AIではない）", "唐津市", {"食料品", "漬物"}, (13, 13), False),
    ("平岡石油店（OCR の帳簿保存。AIではない）", "唐津市", {"石油製品の販売"}, None, False),
    ("吉田刃物（きらめく採択、AI の語なし）", "多久市", {"刃物", "金属製品"}, None, False),
    ("香蘭社（陶磁器、OCR は希望。所在未確認）", "所在未確認", {"窯業・土石", "陶磁器"}, None, False),
    ("マーゼルン（桐製家具、RPA。所在未確認）", "所在未確認", {"家具"}, None, False),
    ("たこ萬（福岡県大牟田市、佐銀デジタルパートナーズの AI-OCR。佐賀の事例にしない）", "県外", {"カット野菜", "食料品"}, None, True),
    ("藤津碍子（県の実証 R2、本文未読）", "所在未確認", {"碍子", "窯業・土石"}, None, True),
    # cases_outside.md（県外。九州以外）
    ("CRAFT BANK（京都府福知山市、クラフトビールの発酵、規模不明）", "県外", {"酒類製造", "飲料", "ビール"}, None, True),
    ("茶夢茶夢ランド菅山園ほか（静岡県、茶の開葉数の AI 推定）", "県外", {"農業", "茶"}, None, True),
    ("丸秀（東京都大田区・山形の工場、AI外観検査、170名）", "県外", {"輸送用機械", "自動車部品", "外観検査"}, (170, 170), True),
    ("イントロダクション（東京都新宿区、SES、9名。予備）", "県外", {"情報サービス", "ソフトウェア開発"}, (9, 9), True),
    ("白井グループ（東京都足立区、AI配車、220名。参考）", "県外", {"廃棄物処理", "収集運搬"}, (220, 220), True),
]

# (市町, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種・業態は stats.md の「市町ごとの主要産業の候補」の (B) 中小企業の業種（経済センサスの事業所数・従業者数）から選んだ。
# 1〜4事業所で数百人の中分類（伊万里市・大町町・吉野ヶ里町の電子部品、神埼市の輸送用機械、上峰町の鉄鋼、
# 江北町の非鉄金属、嬉野市・鳥栖市のゴム製品、小城市の飲料など）は特定の工場と読めるので試算の業種にしない。
# 2026-11-04: 既存の地域ページ（試算の節がある約650本）と10県の PLAN で、余りが1の時間のうち空いているのは約60種だけで、
# 月約27万円未満の金額と、対象10名未満・1人の業務量を◯.0・◯.5時間にした小さい組はほぼ埋まっていた。
# 空いている値を探して決めた（月77.25〜224.25時間・約27.2万〜77.5万円・22〜165名）。
PLAN = [
    # 佐賀中部保健福祉事務所（5）
    ("佐賀市", "saga-city", "卸売業・小売業", "建材・住宅設備機器の卸売（県内の工務店・設備業者へ納品）", {"卸売", "建材卸", "住宅設備"}, 165,
     "工務店・設備業者からの見積・在庫・納期の問い合わせへの回答と、商品の仕様書・施工説明の資料の下書き", 24, 36.5),
    ("多久市", "taku", "製造業", "金属製品（鋼構造物・建築金物の製作）", {"金属製品", "鉄骨", "建築金物"}, 45,
     "元請け・工務店からの図面・数量の問い合わせへの回答と、製作要領書・溶接の検査記録の取りまとめ", 17, 33),
    ("小城市", "ogi", "製造業", "食料品（和菓子・焼き菓子の製造・販売）", {"食料品", "菓子"}, 55,
     "土産物店・通販の取引先からの注文・賞味期限・原材料の問い合わせへの回答と、商品の表示・説明文の作成、製造記録の取りまとめ", 16, 35.5),
    ("神埼市", "kanzaki", "医療・福祉", "特別養護老人ホーム（短期入所・通所介護を併設）", {"介護", "特別養護老人ホーム"}, 52,
     "ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成", 16, 37.25),
    ("吉野ヶ里町", "yoshinogari", "製造業", "プラスチック製品（食品容器・包装資材の成形）", {"プラスチック製品", "食品容器", "包装資材"}, 58,
     "取引先（食品メーカー）からの仕様・数量変更の問い合わせへの回答と、成形条件表・出荷検査の記録の取りまとめ", 19, 31),
    # 鳥栖保健福祉事務所（4）
    ("鳥栖市", "tosu", "運輸業・郵便業", "倉庫・物流センター（荷主の保管・流通加工・配送を受託）", {"倉庫", "物流センター", "運送"}, 150,
     "荷主からの入出庫・在庫・配送の問い合わせへの回答と、作業実績・誤出荷の報告書、作業手順書の取りまとめ", 26, 34.5),
    ("基山町", "kiyama", "製造業", "生産用機械（省力化装置・搬送装置の設計・製作）", {"生産用機械", "省力化装置", "搬送装置"}, 70,
     "顧客との仕様の打合せ記録の要約と、見積書・取扱説明書・設計変更の連絡書の下書き", 20, 28.75),
    ("上峰町", "kamimine", "運輸業・郵便業", "道路貨物運送（工業団地・食品工場の地場配送）", {"運送", "道路貨物運送"}, 42,
     "配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計", 16, 26.75),
    ("みやき町", "miyaki", "製造業", "食料品（惣菜・調理冷凍食品の製造）", {"食料品", "惣菜", "冷凍食品"}, 80,
     "量販店・外食の取引先からの規格・アレルゲンの問い合わせへの回答と、規格書の改訂、衛生管理の記録の取りまとめ", 20, 32.25),
    # 唐津保健福祉事務所（2）
    ("唐津市", "karatsu", "製造業", "食料品（水産練り製品・干物などの水産加工）", {"食料品", "水産加工", "水産練り製品"}, 120,
     "量販店・土産物店の取引先からの規格・産地・賞味期限の問い合わせへの回答と、ロット・衛生管理の記録の取りまとめ", 26, 31),
    ("玄海町", "genkai", "建設業", "総合工事業（建築・土木）", {"建設", "総合工事業"}, 38,
     "公共工事・民間工事の施工計画書・提出書類の作成と、工事写真・日報の整理", 15, 36),
    # 伊万里保健福祉事務所（2）
    ("伊万里市", "imari", "製造業", "輸送用機械（自動車部品のプレス・溶接）", {"輸送用機械", "自動車部品", "プレス"}, 95,
     "取引先（自動車部品の一次取引先など）からの品質・変更の問い合わせへの回答と、変化点の管理表・検査記録の取りまとめ", 22, 32.5),
    ("有田町", "arita", "卸売業・小売業", "陶磁器の卸売（産地の商社。業務用食器の企画・受注）", {"卸売", "陶磁器卸", "業務用食器"}, 33,
     "ホテル・飲食店・小売店からの見積・在庫・納期の問い合わせへの回答と、商品の説明文・カタログの原稿の作成", 12, 39.75),
    # 杵藤保健福祉事務所（7）
    ("武雄市", "takeo", "製造業", "窯業・土石製品（陶磁器の食器の製造）", {"窯業・土石", "陶磁器", "食器"}, 64,
     "商社・小売の取引先からの仕様・数量・納期の問い合わせへの回答と、生産計画表・検品の記録の取りまとめ", 18, 33.5),
    ("鹿島市", "kashima", "製造業", "飲料（日本酒の製造と販売。蔵元）", {"酒類製造", "飲料", "日本酒"}, 36,
     "酒販店・通販の客からの在庫・商品の問い合わせへの回答と、商品説明・表示の文の作成、製造・出荷の記録の取りまとめ", 12, 32.75),
    ("嬉野市", "ureshino", "宿泊・飲食サービス業", "温泉旅館（宴会・日帰り入浴を含む）", {"宿泊", "旅館"}, 68,
     "予約サイト・メールの問い合わせへの返信の下書きと、宴会・団体の見積書、館内案内の多言語の文の作成", 22, 29),
    ("大町町", "omachi-town", "医療・福祉", "診療所（外来と訪問診療）", {"医療", "診療所", "訪問診療"}, 22,
     "紹介状・診療情報提供書の下書きと、患者・家族への説明文、訪問診療の記録の清書", 8, 44.75),
    ("江北町", "kohoku", "医療・福祉", "介護老人保健施設（通所リハビリを併設）", {"介護", "介護老人保健施設"}, 40,
     "リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成", 12, 43.25),
    ("白石町", "shiroishi-town", "卸売業・小売業", "農産物（たまねぎなどの野菜）の集出荷・卸売", {"卸売", "農産物の卸売"}, 50,
     "市場・量販店の取引先からの入荷・規格・価格の問い合わせへの回答と、出荷の伝票・精算書の取りまとめ", 20, 30.5),
    ("太良町", "tara", "建設業", "総合工事業（土木・漁港の工事）", {"建設", "土木"}, 25,
     "工事日報・安全書類の取りまとめと、発注者への工程の連絡文、出来形の記録の整理", 12, 25.75),
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def other_plans():
    """全県の _calc.py の PLAN を読み、(県, 市町村, 削減時間, 万円) を返す。読めない県・必須の県のファイルがなければ None を入れる（NG）。"""
    out, read = [], {}
    paths = sorted(glob.glob(os.path.join(ROOT, "data", "area", "*", "_calc.py")))
    found = {os.path.basename(os.path.dirname(p)): p for p in paths}
    for pref in REQUIRED:
        if pref not in found:
            print(f"NG {pref} の _calc.py がない（必須）")
            out.append(None)
    for pref, path in found.items():
        if pref == SELF:
            continue
        src = open(path, encoding="utf-8").read()
        try:
            rows = READERS.get(pref, read_plan_standard)(src)
        except Exception as e:  # noqa: BLE001 形が違う
            print(f"NG {pref} の PLAN が読めない（{type(e).__name__}: {e}）。READERS に読み方を足す")
            out.append(None)
            continue
        n_skip = 0
        for city, ind, n, hrs in rows:
            if ind not in RATE:
                n_skip += 1
                continue
            h = Decimal(str(n)) * Decimal(str(hrs)) * Decimal("0.25")
            out.append((pref, city, h, man(h * RATE[ind])))
        if n_skip:
            print(f"NG {pref} の PLAN に時給の分からない業種が {n_skip}行ある（RATE に足す）")
            out.append(None)
        read[pref] = len(rows)
        if not rows:
            print(f"（参考）{pref} の PLAN はまだ空（作成中）。行が入ったら再実行する")
    return out, read


def existing():
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（岡山県の _calc.py と同じ拾い方）。"""
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
    op, read = other_plans()
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
    if not os.path.exists(os.path.join(HERE, "cases2.md")):
        print("（注意）cases2.md はまだない。できたら会社を CASES に足して再実行する")

    seen_h, seen_m, seen_s = {}, {}, {}
    notes = []
    print("| 市町 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | 年間 | ×4 を7で割った余り |")
    print("|---|---|---|---|---|---|---|---|---|")
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
        res = int(q) % 7 if q % 1 == 0 else None
        print(f"| {city} | {ind}（{sub}） | {size}名 | {n}名×{hrs}時間×25% | {h.normalize():f}時間 | 約{RATE[ind]:,}円 | 約{m}万円 | 約{y}万円 | {res} |")
        if q % 1 != 0:
            print(f"  NG {city} の時間が0.25時間刻みでない ({h})")
            ok = False
        elif res != KYUSHU_MOD:
            print(f"  NG {city} の時間 {h} は九州の割り当て（×4 を7で割った余り {KYUSHU_MOD}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 佐賀県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 佐賀県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
            ok = False
        seen_s[size] = city
        if not border_ok(yen):
            print(f"  NG {city} の金額が四捨五入の境目に近い（{yen}円）")
            ok = False
        if n > size:
            print(f"  NG {city} の対象人数が従業員数より多い")
            ok = False
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
                print(f"  NG {city} の試算（{sub}）が同じ市町の事例 {cname}（規模不明）と同じ業態")
                ok = False
            elif ccity in ("所在未確認", "県外"):
                notes.append(f"{city}: 試算（{sub}・{size}名）と業態のキーが重なる{ccity}の事例 {cname}"
                             f"（{'規模不明' if csize is None else f'{csize[0]}〜{csize[1]}名で範囲外'}・別の市町なので NG にしない）")
    slugs = {p[1] for p in PLAN}
    if slugs != SLUGS:
        print("NG slug が _brief.md と違う:", slugs ^ SLUGS)
        ok = False
    if not PLAN:
        print("NG PLAN が空")
        print("NG")
        return
    n_ex_size = sum(1 for p in PLAN if p[5] in ex_s)
    print(f"\n市町ページ: {len(PLAN)}、市町名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}")
    print(f"時間の範囲 {min(seen_h).normalize():f}〜{max(seen_h).normalize():f}時間、金額の範囲 約{min(seen_m)}〜{max(seen_m)}万円、規模 {min(seen_s)}〜{max(seen_s)}名")
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは佐賀県の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 20 else "NG")


if __name__ == "__main__":
    main()
