#!/usr/bin/env python3
"""栃木県25市町の試算の割り当てを計算し、重なりを確かめる（2026-11-06）。

data/area/kagoshima/_calc.py を元に作った。県ページ（/area/tochigi/）には試算を入れないので、PLAN は25行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **北海道・北関東3県・沖縄の取り決め**: 月の削減時間（0.25時間刻み）×4 を5で割った余りが 2（栃木県）の時間だけを使う
     （0.5, 1.75, 3.0, 4.25, … の1.25時間刻み。data/area/_batch5/shared.md）
  1. 25ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、栃木県を除く）の「## 試算」の節の「◯時間」「◯万円」と重ならない
  3. 全県の data/area/*/_calc.py の PLAN（栃木県を除く。glob で全部読む。茨城・群馬・北海道・沖縄も入れば読む）と重ならない。
     読めないファイルは警告。REQUIRED の県はファイルがなければ NG
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md の事例の会社と同じにならない（CASES と照合。鹿児島と同じ判定）
  6. slug が _brief.md の25市町と一致する（栃木市 tochigi-city、那珂川町 nakagawa-town）
  7. 試算の業種が wages.md の9業種にある（農業は試算の業種にしない）
使い方: python3 data/area/tochigi/_calc.py   （末尾に OK / NG を出す）
並行の県の PLAN は後から入るので、push の直前に git pull してもう一度実行する。
"""
import ast
import glob
import importlib.util
import io
import os
import re
import sys
from collections import Counter
from contextlib import redirect_stdout
from decimal import Decimal, ROUND_HALF_UP

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ART = os.path.join(ROOT, "articles")
HERE = os.path.dirname(os.path.abspath(__file__))
SELF = "tochigi"
BATCH_MOD = 2  # 北海道・北関東3県・沖縄の割り当て（月の削減時間×4 を5で割った余り）。栃木県は 2

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
    # 市（14）
    "utsunomiya", "ashikaga", "tochigi-city", "sano", "kanuma", "nikko", "oyama", "moka", "otawara", "yaita",
    "nasushiobara", "sakura", "nasukarasuyama", "shimotsuke",
    # 町（11）
    "kaminokawa", "mashiko", "motegi", "ichikai", "haga", "mibu", "nogi", "shioya", "takanezawa", "nasu", "nakagawa-town",
}

# 照合が必須の県（2026-11-06 にある _calc.py）。ファイルがなければ NG
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima")

# cases.md（2026-11-06）の事例の会社。cases_outside.md・subsidy_a_areas.md ができたら足して再実行する
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・交付決定・使用済み・目標を含む〕)
CASES = [
    ("トチシュー（AI の画像検査、木材の切削面）", "鹿沼市", {"木材・木製品", "集成材", "製材"}, None, True),
    ("吉澤石灰工業（キルン部品の劣化の AI 画像診断、238名）", "佐野市", {"窯業・土石", "石灰"}, (238, 238), True),
    ("竹中（県の補助で AI 員数判定、所在・業種未確認）", "佐野市", {"業種未確認"}, None, True),
    ("晃和（県の補助で AI 精密検品、業種未確認）", "佐野市", {"業種未確認"}, None, True),
    ("アップデート（IT。日光市の自販機の AI カメラの客層分析）", "宇都宮市", {"情報サービス"}, None, True),
    ("フォーカス（画像検査 AI の提供側）", "宇都宮市", {"情報サービス", "ソフトウェア"}, None, True),
    ("ミナテラスとちぎ（栃木トヨタ自動車、AI カメラ分析、687名）", "宇都宮市", {"自動車小売", "小売"}, (687, 687), True),
    ("スマートde愛ショップ（道の駅の無人店舗、AI の来訪者分析、～10人）", "宇都宮市", {"小売", "農産物直売"}, (10, 10), True),
    ("下野新聞社（AI で記事を学年別の文章に変換、実証）", "宇都宮市", {"新聞", "出版"}, None, True),
    ("轟（ホテル・飲食店向けオーダーシステム、未来技術の採択）", "宇都宮市", {"情報サービス", "ソフトウェア"}, None, True),
    ("那須赤十字病院（生成AIの退院サマリ、試算の時間）", "大田原市", {"医療", "病院"}, None, True),
    ("オプトニクス精密（AI 穴形状外観検査、極薄金属部品）", "足利市", {"金属製品", "精密部品"}, None, True),
    ("sync（足利のカフェのデータ分析、AI ではない）", "足利市", {"飲食店"}, None, False),
    ("藤成測量（ドローン・3D 測量・AI で索道の点検、実証）", "栃木市", {"測量", "技術サービス"}, None, True),
    ("アイ・シイ・エス 栃木工場（熱処理の IoT、AI ではない、186名）", "栃木市", {"金属熱処理", "金属製品"}, (186, 186), False),
    ("東京鐵鋼（IoT・AI の DX 研修、約815名）", "小山市", {"鉄鋼"}, (815, 815), True),
    ("大和鋼管工業（AI の SOP 活用、未来技術の採択）", "さくら市", {"鉄鋼", "鋼管"}, None, True),
    ("敷島ファーム（子牛の体温監視、AI の記載なし）", "那須町", {"農業", "畜産", "肉用牛"}, None, False),
    ("宇都宮大学 農学部附属農場（乳用牛の AI 画像分析、所在未確認）", "所在未確認", {"農業", "酪農"}, None, True),
    ("寺内動物病院（電子カルテ化、AI ではない）", "高根沢町", {"獣医"}, None, False),
    ("ヤイタ工業（VOC センサー、AI ではない）", "塩谷町", {"生産用機械", "塗装設備"}, None, False),
    ("明治鋼業（生成AIのスマートファクトリー、本社 東京）", "所在未確認", {"鉄鋼", "金属製品"}, None, True),
    # 2026-11-06 D125: subsidy_a_areas.md の県の交付決定で AI がテーマの会社（AI を作る側）
    ("ならでわ（生成AIの口コミレビュー分析の開発、県のイノベーションエコシステム推進 R8 2次）", "宇都宮市", {"情報サービス", "ソフトウェア"}, None, True),
    ("HCCソフト（AI 活用型組織成長支援システムの研究開発、県のものづくり技術強化 R8。本社 さくら市）", "さくら市", {"情報サービス", "ソフトウェア"}, None, True),
    # 2026-11-06 D125: cases_outside.md（青梅法人会の成果発表会 2026-09-19。従業員数はどれも未確認）
    ("佐久間建設（東京都奥多摩町、総合建設。積算のアプリで1件100→40時間）", "県外", {"建設", "総合工事業", "土木"}, None, True),
    ("くら蔵（東京都奥多摩町、弁当・惣菜。弁当の設計 最短5分・月約30時間は見込み）", "県外", {"食料品", "惣菜", "弁当"}, None, True),
    ("社会福祉法人 年輪（東京都青梅市、障害福祉。個別支援計画書 約15→約6時間）", "県外", {"障害福祉", "福祉", "個別支援計画"}, None, True),
    ("サンメディカルサービス（東京都青梅市、病院・介護施設へのリネン配送。配送記録 週29.8→5.53時間）", "県外", {"リネン", "配送", "運送"}, None, True),
    ("清水燃料（LPガスの配送計画、月90時間は試算。所在未確認）", "所在未確認", {"燃料卸", "配送", "運送"}, None, True),
    ("サムライTシャツ（東京都西多摩地域、プリント加工。過去の入稿データの画像検索）", "県外", {"プリント加工", "繊維"}, None, True),
]
# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種・業態は stats.md の「市町村ごとの主要産業の候補」の (B) 中小企業の業種（経済センサスの事業所数・従業者数）から選んだ。
# 霧島市の電子部品（16所・7,169人）、薩摩川内市の窯業・土石（21所・4,728人）、志布志市の飲料・たばこ・飼料（出荷額の70.2%）、
# 伊佐市・いちき串木野市の非鉄金属（1所）、南種子町の技術サービス業・輸送用機械（1所）、湧水町の電子部品（3所）など、
# 大企業の工場・特定の施設と読める中分類は試算の業種にしない。農業・漁業・林業も試算の業種にしない
# （畜産・茶・さとうきびの町村は食料品製造〔食肉・鶏卵・製茶・でん粉・農産加工〕・卸売〔集出荷〕などにした）。
# 2026-11-04: 既存の地域ページ（試算の節がある約690本）と13県の PLAN で埋まっていない値を探して決めた。# (市町, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種・業態は stats.md の「市町ごとの主要産業の候補」の (B) 中小企業の業種（経済センサスの事業所数・従業者数）から選んだ。
# 上三川町の輸送用機械（日産自動車の栃木工場）、那須塩原市のゴム製品（ブリヂストンの2工場）、真岡市の非鉄金属、市貝町のパルプ・紙、
# 芳賀町の輸送用機械・研究機関、高根沢町の研究機関、小山市の情報通信機械など、大企業の工場・研究所と読める中分類は試算の業種にしない。
# 農業も試算の業種にしない（酪農の那須塩原市は乳製品の製造、米の高根沢町は米穀の卸にした）。
# 事例の会社と業態を分けた: 鹿沼市（トチシュー＝木材加工）は運送、大田原市（那須赤十字病院）は生産用機械、佐野市（吉澤石灰工業・竹中・晃和）はプラスチック製品。
# 2026-11-06: 既存の地域ページと全県の PLAN で埋まっていない値を探して決めた（data/area/_batch5/shared.md の余り2）。
PLAN = [
    # 河内（2）
    ("宇都宮市", "utsunomiya", "卸売業・小売業", "機械器具の卸売（産業機械・部品を県内の工場へ納品）", {"卸売", "機械器具卸"}, 180,
     "取引先の工場からの見積・納期・代替品の問い合わせへの回答と、見積書・提案書の下書き、受注の記録の取りまとめ", 36, 34.5),
    ("上三川町", "kaminokawa", "運輸業・郵便業", "道路貨物運送（部品・資材の工場向けの定期輸送）", {"運送", "道路貨物運送"}, 76,
     "配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計", 24, 35.5),
    # 上都賀（2）
    ("鹿沼市", "kanuma", "運輸業・郵便業", "道路貨物運送（県内・首都圏への中距離輸送と倉庫）", {"運送", "道路貨物運送", "倉庫"}, 135,
     "荷主からの集荷・配送の依頼と問い合わせへの回答、配車の下書き、乗務記録・請求の明細の取りまとめ", 32, 37.25),
    ("日光市", "nikko", "宿泊・飲食サービス業", "温泉旅館（団体・宴会の受け入れを含む）", {"宿泊", "温泉旅館", "旅館"}, 128,
     "予約サイト・メールの問い合わせへの返信の下書きと、団体・宴会の見積書、館内案内の多言語の文の作成", 32, 34.75),
    # 芳賀（5）
    ("真岡市", "moka", "製造業", "金属製品（プレス・板金部品の加工）", {"金属製品", "プレス", "板金"}, 96,
     "取引先からの図面・数量・納期の問い合わせへの回答と、見積書・作業手順書の下書き、検査記録の取りまとめ", 26, 29.5),
    ("益子町", "mashiko", "卸売業・小売業", "陶磁器の卸売・小売（窯元から仕入れて店舗・通販で販売）", {"卸売", "小売", "陶磁器"}, 48,
     "通販・店舗の客からの在庫・配送・作り手の問い合わせへの回答と、商品の説明文、取引先への発注の連絡の作成", 19, 43.0),
    ("茂木町", "motegi", "宿泊・飲食サービス業", "宿泊施設と飲食店（観光客・イベントの来場者向け）", {"宿泊", "飲食店"}, 39,
     "予約・団体の問い合わせへの返信の下書きと、イベントの日の予約の取りまとめ、メニュー・案内の文の作成", 16, 40.75),
    ("市貝町", "ichikai", "製造業", "プラスチック製品（成形品の製造）", {"プラスチック製品", "成形"}, 58,
     "取引先からの仕様・数量・納期の問い合わせへの回答と、作業標準書・検査記録の取りまとめ、日報の集計", 24, 41.75),
    ("芳賀町", "haga", "学術研究・専門技術サービス", "技術サービス（設計図面・試験報告書の作成の受託）", {"技術サービス", "設計", "試験"}, 68,
     "顧客との打合せ記録の要約と、試験報告書・設計の説明書の下書き、見積書の作成", 23, 44.0),
    # 下都賀（5）
    ("栃木市", "tochigi-city", "製造業", "食料品（惣菜・弁当の製造）", {"食料品", "惣菜", "弁当"}, 125,
     "量販店・コンビニの取引先からの規格・アレルゲンの問い合わせへの回答と、規格書の改訂、衛生管理の記録の取りまとめ", 29, 33.0),
    ("小山市", "oyama", "製造業", "はん用機械（ポンプ・送風機などの部品の加工と組立）", {"はん用機械", "機械部品"}, 150,
     "取引先からの仕様・納期の問い合わせへの回答と、取扱説明書・作業手順書の下書き、検査成績書の取りまとめ", 32, 33.5),
    ("下野市", "shimotsuke", "医療・福祉", "介護老人保健施設（通所リハビリを併設）", {"介護", "介護老人保健施設"}, 92,
     "リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成", 24, 30.5),
    ("壬生町", "mibu", "医療・福祉", "訪問看護ステーション（訪問リハビリを含む）", {"医療", "訪問看護"}, 47,
     "訪問看護の記録の清書と、主治医への報告書・計画書の下書き、家族への連絡文の作成", 23, 29.0),
    ("野木町", "nogi", "製造業", "鉄鋼（鋳物の製造）", {"鉄鋼", "鋳物", "鋳造"}, 73,
     "取引先からの材質・数量・納期の問い合わせへの回答と、検査成績書・ミルシートの取りまとめ、作業手順書の下書き", 27, 41.0),
    # 塩谷南那須（6）
    ("矢板市", "yaita", "医療・福祉", "病院（一般病床・療養病床と外来）", {"医療", "病院"}, 142,
     "紹介状・診療情報提供書の下書きと、患者・家族への説明文書、院内の委員会の議事録の作成", 34, 38.0),
    ("さくら市", "sakura", "製造業", "輸送用機械（自動車部品の加工と組立）", {"輸送用機械", "自動車部品"}, 88,
     "取引先からの設計変更・納期の問い合わせへの回答と、作業手順書・品質の記録の取りまとめ、報告書の下書き", 26, 39.5),
    ("那須烏山市", "nasukarasuyama", "医療・福祉", "通所介護と訪問介護の事業所（送迎を含む）", {"介護", "通所介護", "訪問介護"}, 62,
     "利用・訪問の記録の清書と、個別機能訓練計画書の下書き、家族への連絡帳の文の作成", 24, 44.25),
    ("塩谷町", "shioya", "建設業", "総合工事業（土木・道路の工事）", {"建設", "総合工事業", "土木"}, 44,
     "工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理", 23, 34.0),
    ("高根沢町", "takanezawa", "卸売業・小売業", "米穀の集荷・精米・卸売", {"卸売", "米穀卸"}, 53,
     "米穀店・飲食店・量販店の取引先からの在庫・品種・価格の問い合わせへの回答と、出荷伝票・精算書の取りまとめ", 26, 44.5),
    ("那珂川町", "nakagawa-town", "医療・福祉", "特別養護老人ホーム（短期入所を併設）", {"介護", "特別養護老人ホーム"}, 67,
     "ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成", 24, 49.25),
    # 那須（3）
    ("大田原市", "otawara", "製造業", "生産用機械（工場の自動化設備・治具の設計製作）", {"生産用機械", "自動化設備", "治具"}, 106,
     "顧客との仕様の打合せ記録の要約と、見積書・取扱説明書・設計変更の連絡書の下書き", 28, 37.75),
    ("那須塩原市", "nasushiobara", "製造業", "食料品（牛乳・乳製品の製造）", {"食料品", "乳製品"}, 165,
     "量販店・飲食店の取引先からの規格・賞味期限・数量の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ", 34, 33.0),
    ("那須町", "nasu", "宿泊・飲食サービス業", "リゾートホテル（レストラン・ペット同伴の受け入れを含む）", {"宿泊", "ホテル", "リゾートホテル"}, 83,
     "予約サイト・メールの問い合わせへの返信の下書きと、体験・送迎の手配の連絡、館内案内の多言語の文の作成", 26, 42.0),
    # 安足（2）
    ("足利市", "ashikaga", "製造業", "繊維（ニット・織物の製造と加工）", {"繊維", "ニット", "織物"}, 72,
     "アパレル・問屋の取引先からの仕様・数量・納期の問い合わせへの回答と、仕様書・品質の記録の取りまとめ、商品の説明文の作成", 24, 39.25),
    ("佐野市", "sano", "製造業", "プラスチック製品（射出成形品の製造）", {"プラスチック製品", "射出成形"}, 112,
     "取引先からの仕様・数量・納期の問い合わせへの回答と、作業標準書・検査記録の取りまとめ、見積書の下書き", 28, 32.75),
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def read_plan_text(src):
    """岡山県の形の PLAN を文字列で切り出す（行頭の `PLAN = [` から行頭の `]` まで）。docstring の「PLAN = [」は拾わない"""
    m = re.search(r"^PLAN = \[", src, re.M)
    if not m:
        raise ValueError("行頭の PLAN = [ がない")
    j = src.index("\n]\n", m.start())
    return ast.literal_eval(src[m.start() + 7:j + 2])


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
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（岡山県・佐賀県の _calc.py と同じ拾い方）。"""
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
        res = int(q) % 5 if q % 1 == 0 else None
        print(f"| {city} | {ind}（{sub}） | {size}名 | {n}名×{hrs}時間×25% | {h.normalize():f}時間 | 約{RATE[ind]:,}円 | 約{m}万円 | 約{y}万円 | {res} |")
        if q % 1 != 0:
            print(f"  NG {city} の時間が0.25時間刻みでない ({h})")
            ok = False
        elif res != BATCH_MOD:
            print(f"  NG {city} の時間 {h} は北海道・北関東3県・沖縄の割り当て（×4 を5で割った余り {BATCH_MOD}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 栃木県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 栃木県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは栃木県の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 25 else "NG")


if __name__ == "__main__":
    main()
