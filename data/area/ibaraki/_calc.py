#!/usr/bin/env python3
"""茨城県44市町村の試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-11-06）。

data/area/kagoshima/_calc.py（群馬・北海道の free の形も）を元に作った。県ページ（/area/ibaraki/）には試算を入れないので、PLAN は44行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **北海道・北関東3県・沖縄の取り決め**: 月の削減時間（0.25時間刻み）×4 を5で割った余りが 1（茨城県）の時間だけを使う
     （0.25, 1.5, 2.75, 4.0, … の1.25時間刻み。data/area/_batch5/shared.md）
  1. 44ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、茨城県を除く）の「## 試算」の節に出てくる
     「◯時間」「◯万円」の値と重ならない。拾い方は鹿児島県の _calc.py と同じ（広めに拾う）
  3. 全県の data/area/*/_calc.py の PLAN（茨城県を除く。glob で全部読む。北海道・栃木・群馬・沖縄は作業中で後から増える）の
     月の削減時間・月の時間換算額と重ならない。他県の _calc.py は import で読み、だめなら行頭の「PLAN = [」
     （改行のすぐ後ろのものだけ。docstring の中の文字列は拾わない）を文字列で切り出して読む。
     **読めないファイルは NG にせず警告**。REQUIRED の県はファイルがなければ NG。金額が重なったら先に push した県を優先する
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md・cases2.md（あれば）・subsidy_*_areas.md の事例の会社と同じにならない
     （CASES と照合。鹿児島と同じ判定）
     - AI の事例で、業態のキーが重なり、従業員数が事例の範囲（下限×0.85〜上限×1.15）に入る → NG
     - AI の事例で、業態のキーが重なり、同じ市町村で、事例の従業員数が分からない → NG（その会社の値と読まれるため）
     - 業種が確かめられていない事例（キー「業種未確認」）と同じ市町村 → 参考として表示（NG にしない）
     - AI ではない事例と業態・規模が近い → 参考として表示
  6. slug が _brief.md の44市町村と一致する（茨城町 ibaraki-town、境町 sakai-town。古河市 koga・鹿嶋市 kashima・那珂市 naka）
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
  8. 県ページには試算を入れない（PLAN は44行）
使い方: python3 data/area/ibaraki/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/ibaraki/_calc.py free 製造業 100 200   （余り1の時間で、既存・他県・茨城の中と重ならない時間と金額の候補を出す）
並行の県の PLAN は後から入るので、push の直前に git pull してもう一度実行する。
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
SELF = "ibaraki"
MOD_N, MOD_R = 5, 1  # 北海道・北関東3県・沖縄の割り当て（月の削減時間×4 を5で割った余り）。茨城県は 1
N_PAGES = 44

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
    # 市（32）
    "mito", "hitachi", "tsuchiura", "koga", "ishioka", "yuki", "ryugasaki", "shimotsuma", "joso", "hitachiota",
    "takahagi", "kitaibaraki", "kasama", "toride", "ushiku", "tsukuba", "hitachinaka", "kashima", "itako", "moriya",
    "hitachiomiya", "naka", "chikusei", "bando", "inashiki", "kasumigaura", "sakuragawa", "kamisu", "namegata",
    "hokota", "tsukubamirai", "omitama",
    # 町（10）
    "ibaraki-town", "oarai", "shirosato", "daigo", "ami", "kawachi", "yachiyo", "goka", "sakai-town", "tone",
    # 村（2）
    "tokai", "miho",
}

# 照合が必須の県（2026-11-06 に _calc.py がある県）。ファイルがなければ NG。ほかに見つかった _calc.py も全部読む
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "kagoshima", "kumamoto", "miyazaki", "nagasaki", "oita", "saga",
            "hokkaido", "tochigi", "gunma", "okinawa")

# cases.md・cases_outside.md・subsidy_a_areas.md・subsidy_b_areas.md・companies.md（大企業の工場）の事例の会社（2026-11-06）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・見込み・使用済み・提供側を含む〕)
# cases2.md はこの版の時点でまだない。できたら会社を「# cases2.md」の行に足して再実行する
CASES = [
    # 水戸市（cases.md）
    ("アーストラベル水戸（生成AIで名簿と入金データの照合、教育旅行の企画。従業員数は未確認）", "水戸市",
     {"旅行", "旅行業", "教育旅行"}, None, True),
    ("ユードム（ITIC の生成AI支援の受託・アーストラベル水戸の支援側、429名）", "水戸市",
     {"情報サービス", "ソフトウェア", "システム開発"}, (429, 429), True),
    ("クォンタムフラワーズ＆フーズ（県の戦略分野の採択、AI の発酵監視ソフト。バイオ）", "水戸市",
     {"バイオ", "研究開発", "AI製品開発"}, None, True),
    ("ヴィオーラ（おしぼりの包装数の IoT、AI ではない）", "水戸市", {"おしぼり", "リネンサプライ"}, None, False),
    ("トヨタモビリティパーツ 茨城支社（AI-OCR の伝票入力、自動車部品の卸。大企業の子会社）", "水戸市",
     {"卸売", "自動車部品卸"}, None, True),
    ("常陽銀行（行内のローカルLLM、大企業）", "水戸市", {"銀行", "金融"}, None, True),
    # ひたちなか市
    ("川崎製作所（AI の切削工具の劣化予測、難削材の切削加工。従業員数は未確認）", "ひたちなか市",
     {"金属加工", "切削加工", "精密加工", "金属製品", "航空機部品"}, None, True),
    # 常総市
    ("ハリガイ工業（画像判別AIの外観検査の見込み、ゴム成型・吸着パッド、100名）", "常総市",
     {"ゴム製品", "ゴム成型", "吸着パッド"}, (100, 100), True),
    ("本田技術研究所の AI・自動運転の実証（常総市は実証地、主体は Honda。shared.md）", "常総市",
     {"自動運転", "研究開発"}, None, True),
    # 東海村
    ("ヒューマンサポートテクノロジー（画像認識AIを作る側、ソフトウェア開発。IIS チャレンジ基金の採択も）", "東海村",
     {"情報サービス", "ソフトウェア", "画像認識"}, None, True),
    ("水木木材工業（木材の残量の通知、IoT。AI ではない）", "東海村", {"木材", "木材・木製品"}, None, False),
    ("伊藤鋳造鉄工所（加工機の稼働通知、AI ではない）", "東海村", {"鋳造", "金属製品"}, None, False),
    ("東海村 省力化・生産性向上設備の採択実績（技術サービス業の GNSS 測量機器・印刷業の受注システム。社名なし、AI か不明）",
     "東海村", {"技術サービス", "測量", "印刷"}, None, False),
    # 小美玉市
    ("森久（秤の値のエクセル転送、不燃木材。AI ではない）", "小美玉市", {"木材", "木材・木製品", "不燃木材"}, None, False),
    # つくば市
    ("Optech Innovation（県の戦略分野の採択、後付AI基盤。光学）", "つくば市", {"光学", "検査装置", "AI製品開発"}, None, True),
    ("テクノハイウェイ（県の戦略分野の採択、撮影計画AI。インフラ点検）", "つくば市",
     {"インフラ点検", "AI製品開発"}, None, True),
    ("NeuralX（県の戦略分野の採択、養殖の予測AI）", "つくば市", {"情報サービス", "AI製品開発", "養殖"}, None, True),
    ("ホンダ茨城南（電話の履歴管理、AI の効果ではない。自動車販売）", "つくば市", {"自動車販売", "小売"}, None, False),
    ("高エネルギー加速器研究機構（KEK、AI の記述なし。研究機関）", "つくば市", {"研究機関", "学術・開発研究機関"}, None, False),
    ("おはなリハ ケアマネステーション（音声記録AI要約＋RPA、居宅介護支援。shared.md で茨城向け、cases2.md で確かめる）",
     "つくば市", {"介護", "居宅介護支援", "ケアマネジャー"}, None, True),
    # 日立市
    ("日立製作所 大みか事業所（AI の外観検査の PoC、情報制御システム。大企業、就業人員 約2,450人〔2020年〕）", "日立市",
     {"電気機械", "情報制御システム", "制御盤"}, (2450, 2450), True),
    ("日立市の県の採択3社（今橋製作所・菊池精機・宮本製作所。事業名に AI なし、業種は未確認）", "日立市",
     {"業種未確認"}, None, False),
    # 常陸大宮市・龍ケ崎市・坂東市（農業）
    ("つづく農園（AI 養液土耕の実証、いちご。宮城県亘理町で使用済み）", "常陸大宮市", {"農業", "いちご"}, None, True),
    ("横田農場ほか（国のスマート農業実証、水稲。AI ではない）", "龍ケ崎市", {"農業", "水稲"}, None, False),
    ("アグリ山﨑（国のスマート農業実証、水稲。AI ではない）", "坂東市", {"農業", "水稲"}, None, False),
    ("ライス&グリーン石島（国のスマート農業実証。AI ではない）", "所在未確認", {"農業", "水稲"}, None, False),
    # 大洗町・古河市・阿見町
    ("天地人×大洗町（オープンデータの水道管の漏水リスク判定の実証。自治体の実証）", "大洗町",
     {"情報サービス", "水道"}, None, True),
    ("吉田製作所（県の採択、AI ではない。業種は未確認）", "古河市", {"業種未確認"}, None, False),
    ("キシダ化学（県の採択、AI ではない）", "阿見町", {"化学", "化学工業"}, None, False),
    # subsidy_a_areas.md（IIS いばらきチャレンジ基金 R8 1次。所在地の記載なし、AI を作る側）
    ("ネクステッジテクノロジー（IIS の採択、空間認識AIの見守りシステム）", "所在未確認",
     {"AI製品開発", "見守りシステム", "情報サービス"}, None, True),
    ("BONSAI STUDIO（IIS の採択、AI連携の映像制作）", "所在未確認", {"映像制作", "情報サービス"}, None, True),
    ("FAIR Aid・エイゾス（IIS の採択、AI の語なし）", "所在未確認", {"研究開発", "情報サービス"}, None, False),
    # cases_outside.md（県外。栃木・群馬・北海道・沖縄を除く）
    ("農園たや（福井市、生成AIで業務アプリ、ベビーリーフ。鉾田市・行方市・八千代町向け）", "県外",
     {"農業", "野菜", "ベビーリーフ"}, None, True),
    ("カネク（青梅市、食料品〔粉わさび〕、156名。群馬に割り当て済み）", "県外", {"食料品", "食品製造", "わさび"}, (156, 156), True),
    ("ホッタ晴信堂薬局（福生市、薬局・ドラッグストア。県南の小売向け）", "県外", {"小売", "薬局", "ドラッグストア"}, None, True),
    ("JA西東京（青梅市、AI 録音機で議事録の見込み、188名。群馬に割り当て済み）", "県外",
     {"農業団体", "協同組合"}, (188, 188), True),
    ("ホーライ（東大阪市、粉砕機・破砕機、AI の入金照合、164名）", "県外", {"はん用機械", "生産用機械", "粉砕機"}, (164, 164), True),
    # 大企業の工場（companies.md。AI の事例ではないが、試算が工場の値と読まれないよう業態のキーを入れる）
    ("コマツ 茨城工場（建設機械、大企業の工場）", "ひたちなか市", {"建設機械", "はん用機械", "生産用機械"}, None, False),
    ("日本製鉄 東日本製鉄所 鹿島地区（銑鋼一貫、約3,000人）", "鹿嶋市", {"鉄鋼", "製鉄"}, (3000, 3000), False),
    ("信越化学工業 鹿島工場・三菱ケミカル 茨城事業所（化学、大企業の工場）", "神栖市", {"化学", "化学工業", "石油化学"}, None, False),
    ("日野自動車 古河工場（トラック、大企業の工場）", "古河市", {"輸送用機械", "自動車"}, None, False),
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種・業態は stats.md の各市町村の「(B) 中小企業の業種の候補」（経済センサスの中分類の事業所数・従業者数）から選んだ。
# 日立市・ひたちなか市の電機・電子部品、鹿嶋市の鉄鋼、神栖市の化学・石油製品、古河市・結城市の輸送用機械の完成車、
# 土浦市・つくばみらい市・阿見町の生産用機械の大きな工場、取手市の業務用機械（5所・4,564人）、美浦村の電子部品（1所）、
# 東海村・大洗町の学術・開発研究機関と技術サービス業（原子力の事業所と読める）は、試算の業種・業態にしない。
# 農業・漁業・林業も試算の業種にしない（鉾田市・稲敷市は集出荷・米穀の卸、小美玉市は鶏卵の加工にした）。
# 2026-11-06: 既存の地域ページと19県の PLAN で埋まっていない値を free で探して決めた。
PLAN = [
    ('日立市', 'hitachi', '製造業', '電気機械器具（制御盤・電機部品の組立と配線の協力会社）', {'電気機械', '電機部品', '協力会社', '組立'}, 135,
     '元請けの工場からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録・出荷の報告書の取りまとめ', 36, 33.5),
    ('常陸太田市', 'hitachiota', '医療・福祉', '特別養護老人ホーム（短期入所を併設）', {'特別養護老人ホーム', '介護'}, 82,
     'ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成', 26, 46.0),
    ('高萩市', 'takahagi', '医療・福祉', '介護老人保健施設（通所リハビリを併設）', {'介護老人保健施設', '介護'}, 92,
     'リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成', 34, 26.5),
    ('北茨城市', 'kitaibaraki', '製造業', 'プラスチック製品（工業用部品の射出成形）', {'工業用部品', '射出成形', 'プラスチック製品'}, 112,
     '取引先からの図面・仕様の変更と納期の問い合わせへの回答と、成形条件・検査記録の取りまとめ、不具合の報告書の下書き', 32, 31.75),
    ('常陸大宮市', 'hitachiomiya', '医療・福祉', '認知症対応型グループホームと小規模多機能型居宅介護', {'グループホーム', '小規模多機能', '介護'}, 55,
     '生活記録の清書と、運営推進会議の議事録、家族への便りの文の作成', 24, 39.0),
    ('大子町', 'daigo', '建設業', '総合工事業（道路・河川の土木工事、公共工事が中心）', {'土木', '建設', '総合工事業'}, 50,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真・出来形の記録の整理', 22, 35.5),
    ('水戸市', 'mito', '医療・福祉', '病院（急性期の一般病床と外来）', {'医療', '病院'}, 235,
     '退院時サマリー・診療情報提供書の下書きと、患者・家族への説明文書、院内の委員会の議事録の作成', 47, 28.0),
    ('笠間市', 'kasama', '卸売業・小売業', '小売（建築資材・園芸用品・日用品の専門店を数店舗）', {'園芸用品', '小売', '建築資材'}, 62,
     '客からの取り寄せ・在庫の問い合わせへの回答と、仕入先への発注・入荷の連絡、売場の案内文・チラシの文の作成', 24, 46.5),
    ('ひたちなか市', 'hitachinaka', '宿泊・飲食サービス業', '飲食店（海産物の料理店を数店舗、観光客と団体の受け入れ）', {'海鮮料理', '飲食サービス', '飲食店'}, 88,
     '予約・団体の問い合わせへの返信の下書きと、団体の見積書・献立の案内文、多言語のメニューの文の作成', 32, 26.75),
    ('那珂市', 'naka', '運輸業・郵便業', '道路貨物運送（県央の地場配送と中距離輸送）', {'道路貨物運送', '運送'}, 78,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計', 27, 43.0),
    ('小美玉市', 'omitama', '製造業', '食料品（鶏卵の選別・包装と液卵・加工卵の製造）', {'鶏卵加工', '食料品', '液卵'}, 122,
     '量販店・食品メーカーの取引先からの数量・規格の問い合わせへの回答と、出荷の記録・衛生管理の記録の取りまとめ', 28, 38.25),
    ('茨城町', 'ibaraki-town', '医療・福祉', '病院（一般病床・療養病床と外来）', {'医療', '病院'}, 118,
     '紹介状・診療情報提供書の下書きと、患者・家族への説明文、地域の診療所・介護事業所への連絡文の作成', 44, 25.25),
    ('大洗町', 'oarai', '宿泊・飲食サービス業', 'ホテル・旅館（海水浴・観光の個人客と団体、宴会を含む）', {'宿泊', '旅館', 'ホテル'}, 54,
     '予約サイト・メールの問い合わせへの返信の下書きと、団体・宴会の見積書、館内案内の多言語の文の作成', 16, 42.25),
    ('城里町', 'shirosato', '医療・福祉', '通所介護（デイサービス、送迎を含む）と訪問介護', {'通所介護', '介護', '訪問介護'}, 53,
     '利用の記録と個別機能訓練計画書の下書き、家族への連絡帳の文、サービス担当者会議の記録の作成', 24, 25.25),
    ('東海村', 'tokai', '医療・福祉', '訪問看護ステーション（訪問リハビリを含む）', {'医療', '訪問看護'}, 38,
     '訪問看護の記録の清書と、主治医への報告書・計画書の下書き、家族への連絡文の作成', 16, 44.75),
    ('鹿嶋市', 'kashima', '建設業', '設備工事業（電気・配管の設備工事と保守点検）', {'設備工事', '管工事', '電気工事', '建設'}, 98,
     '施工計画書・作業手順書・安全書類の作成と、点検報告書の取りまとめ、発注者との打合せ記録の要約', 29, 29.0),
    ('潮来市', 'itako', '卸売業・小売業', '飲食料品の小売（食品スーパーを数店舗）', {'食料品小売', '小売', 'スーパー'}, 76,
     '仕入先への発注・欠品の連絡と、売場のPOP・チラシの文、客からの問い合わせへの回答の下書き', 28, 28.25),
    ('神栖市', 'kamisu', '運輸業・郵便業', '港湾運送・倉庫（臨海部の貨物の荷役・保管とトラック輸送）', {'港湾運送', '運送', '倉庫'}, 165,
     '荷主からの入出庫・在庫・配送の問い合わせへの回答と、作業実績の報告書・作業手順書の取りまとめ', 33, 37.0),
    ('行方市', 'namegata', '建設業', '総合工事業（土木・農業土木、公共工事が中心）', {'土木', '建設', '総合工事業'}, 57,
     '公共工事の施工計画書・提出書類の作成と、工事写真・出来形の記録の整理、発注者との打合せ記録の要約', 24, 32.75),
    ('鉾田市', 'hokota', '卸売業・小売業', '農産物（野菜・いも類）の集出荷・卸売', {'卸売', '農産物の集出荷'}, 66,
     '市場・量販店・加工業者の取引先からの入荷・規格・価格の問い合わせへの回答と、出荷の伝票・精算書の取りまとめ', 24, 47.75),
    ('土浦市', 'tsuchiura', '医療・福祉', '病院（回復期リハビリテーション病棟と外来）', {'リハビリ', '医療', '病院'}, 158,
     'リハビリの実施記録の要約と、退院前カンファレンスの記録、患者・家族への説明文書、紹介元の医療機関への報告書の作成', 44, 26.5),
    ('石岡市', 'ishioka', '製造業', '金属製品（建築用金属製品・板金の加工）', {'金属製品', '板金', '建築用金属製品'}, 74,
     '工務店・建設会社の取引先からの図面・寸法・納期の問い合わせへの回答と、見積書・作業指示書の作成、検査記録の取りまとめ', 28, 25.75),
    ('龍ケ崎市', 'ryugasaki', '製造業', '食料品（惣菜・弁当の製造、量販店向け）', {'惣菜', '弁当', '食料品'}, 126,
     '量販店の取引先からの規格・アレルゲンの問い合わせへの回答と、規格書の改訂、衛生管理の記録の取りまとめ', 32, 35.5),
    ('取手市', 'toride', '医療・福祉', '病院（二次救急の一般病床と外来）', {'医療', '病院'}, 205,
     '診療情報提供書・退院時サマリーの下書きと、院内の会議の議事録、患者向けの案内文の作成', 48, 25.75),
    ('牛久市', 'ushiku', '医療・福祉', '介護付き有料老人ホーム（デイサービスを併設）', {'有料老人ホーム', '介護'}, 86,
     'ケア記録の清書と、入居者の家族への近況の連絡文、入居の問い合わせへの返信の下書き', 32, 34.25),
    ('つくば市', 'tsukuba', '学術研究・専門技術サービス', '技術サービス（研究機関・企業から受託する試験・分析）', {'分析', '技術サービス', '受託試験'}, 72,
     '依頼元との仕様の打合せ記録の要約と、試験・分析の報告書の下書き、見積書・作業手順書の作成', 24, 41.5),
    ('守谷市', 'moriya', '宿泊・飲食サービス業', '飲食店（家族向けのレストランを数店舗）', {'レストラン', '飲食サービス', '飲食店'}, 64,
     '予約・宴会の問い合わせへの返信の下書きと、シフトの連絡、メニュー・アレルゲンの案内文の作成', 24, 42.75),
    ('稲敷市', 'inashiki', '卸売業・小売業', '米穀の集荷・精米・卸売', {'米穀卸', '卸売'}, 56,
     '米穀店・飲食店・量販店の取引先からの在庫・品種・価格の問い合わせへの回答と、出荷伝票・精算書の取りまとめ', 23, 37.0),
    ('かすみがうら市', 'kasumigaura', '運輸業・郵便業', '道路貨物運送（県南の地場配送・中距離輸送）', {'道路貨物運送', '運送'}, 124,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計', 38, 29.5),
    ('つくばみらい市', 'tsukubamirai', '運輸業・郵便業', '倉庫・物流センター（日用品・通販の商品の保管・出荷）', {'運送', '物流センター', '倉庫'}, 188,
     '荷主からの在庫・出荷の問い合わせへの回答と、入出庫の記録・作業実績の報告書の取りまとめ、作業手順書の改訂', 42, 30.5),
    ('美浦村', 'miho', '医療・福祉', '認知症対応型グループホーム（2ユニット）', {'グループホーム', '介護'}, 49,
     '生活記録の清書と、運営推進会議の議事録、家族への便りの文の作成', 22, 43.0),
    ('阿見町', 'ami', '製造業', '生産用機械（産業機械の部品・治具の設計製作）', {'治具', '部品加工', '生産用機械'}, 84,
     '取引先（工場）との仕様の打合せ記録の要約と、見積書・取扱説明書・設計変更の連絡書の下書き', 32, 24.25),
    ('河内町', 'kawachi', '建設業', '総合工事業（農業土木・土木の工事）', {'土木', '建設', '総合工事業'}, 36,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理', 13, 47.0),
    ('利根町', 'tone', '卸売業・小売業', '食料品・日用品の小売店（宅配を含む）', {'食料品小売', '小売', '日用品'}, 30,
     '仕入先への発注・欠品の連絡と、宅配の注文の取りまとめ、客からの問い合わせへの回答の下書き', 12, 44.25),
    ('古河市', 'koga', '製造業', '食料品（冷凍食品・調理食品の製造）', {'食料品', '調理食品', '冷凍食品'}, 215,
     '量販店・外食の取引先からの規格・原材料・アレルゲンの問い合わせへの回答と、規格書の改訂、製造・衛生管理の記録の取りまとめ', 48, 27.0),
    ('結城市', 'yuki', '製造業', '輸送用機械器具（自動車部品のプレス加工・溶接の協力会社）', {'自動車部品', '溶接', '輸送用機械', 'プレス'}, 96,
     '取引先からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録・不具合の報告書の取りまとめ', 36, 27.25),
    ('下妻市', 'shimotsuma', '製造業', '金属製品（機械部品の溶接・製缶加工）', {'金属製品', '溶接', '製缶'}, 68,
     '取引先からの図面・納期の問い合わせへの回答と、見積書・作業指示書の作成、検査記録の取りまとめ', 26, 41.0),
    ('常総市', 'joso', '製造業', '食料品（パン・洋菓子の製造、量販店・コンビニ向け）', {'食料品', 'パン', '菓子'}, 185,
     '量販店・コンビニの取引先からの規格・原材料・アレルゲンの問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 41, 31.0),
    ('筑西市', 'chikusei', '製造業', 'プラスチック製品（食品容器・包装資材の成形）', {'プラスチック製品', '食品容器', '包装資材'}, 152,
     '食品メーカーの取引先からの仕様・在庫・納期の問い合わせへの回答と、規格書・検査成績書の作成、生産の記録の取りまとめ', 32, 38.0),
    ('坂東市', 'bando', '運輸業・郵便業', '道路貨物運送と倉庫（食品・日用品の輸送と保管）', {'道路貨物運送', '運送', '倉庫'}, 142,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録・入出庫の記録の集計', 34, 34.0),
    ('桜川市', 'sakuragawa', '製造業', '窯業・土石製品（石製品の加工と販売）', {'石製品', '窯業・土石'}, 42,
     '客・石材店・工務店からの見積・納期・仕様の問い合わせへの回答と、見積書・図面の説明文、受注・加工の記録の取りまとめ', 12, 24.25),
    ('八千代町', 'yachiyo', '運輸業・郵便業', '道路貨物運送（野菜など農産物と食品の輸送）', {'道路貨物運送', '運送', '農産物輸送'}, 63,
     '配車表の下書きと、荷主・市場への到着予定・遅延の連絡、運転日報・点呼記録の集計', 24, 45.25),
    ('五霞町', 'goka', '製造業', '食料品（麺類・調理食品の製造）', {'麺類', '食料品', '調理食品'}, 94,
     '量販店・外食の取引先からの規格・原材料の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 31, 31.0),
    ('境町', 'sakai-town', '医療・福祉', '介護老人保健施設（通所リハビリを併設）', {'介護老人保健施設', '介護'}, 77,
     'リハビリ・ケアの記録の要約と、入所・退所の説明文書、家族への近況の連絡文の作成', 28, 40.75),
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
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | 年間 | ×4 を5で割った余り |")
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
        res = int(q) % MOD_N if q % 1 == 0 else None
        print(f"| {city} | {ind}（{sub}） | {size}名 | {n}名×{hrs}時間×25% | {h.normalize():f}時間 | 約{RATE[ind]:,}円 | 約{m}万円 | 約{y}万円 | {res} |")
        if q % 1 != 0:
            print(f"  NG {city} の時間が0.25時間刻みでない ({h})")
            ok = False
        elif res != MOD_R:
            print(f"  NG {city} の時間 {h} は5県の割り当て（×4 を{MOD_N}で割った余り {MOD_R}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 茨城県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 茨城県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは茨城県の中だけを NG にする）")
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
