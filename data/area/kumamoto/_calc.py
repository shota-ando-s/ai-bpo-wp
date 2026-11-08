#!/usr/bin/env python3
"""熊本県45市町村の試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-11-04）。

data/area/okayama/_calc.py を元に作った（他県の PLAN を glob で全部読む形は data/area/fukuoka/_calc.py と同じ）。
県ページ（/area/kumamoto/）には試算を入れないので、PLAN は45行（熊本市は1行。区のページはない）。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **九州7県の取り決め**: 月の削減時間（0.25時間刻み）×4 を7で割った余りが 3（熊本県）の時間だけを使う
     （0.75, 2.5, 4.25, 6, 7.75, … data/area/_kyushu/shared.md）
  1. 45ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、熊本県を除く）の「## 試算」の節に出てくる
     「◯時間」「◯万円」の値と重ならない。拾い方は岡山県の _calc.py と同じ
  3. 全県の data/area/*/_calc.py の PLAN（熊本県を除く。glob で全部読むので、県が増えても読む）の
     月の削減時間・月の時間換算額と重ならない。REQUIRED の県はファイルがなければ NG。
     PLAN の形が違って読めない県はエラーにせず、読めた分だけ照合し、読めなかった県を表示して NG にする
     （READERS に県ごとの読み方を足せば読める）。**金額が九州の他県と重なったら、熊本側が直す**（先に push した県が優先）
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md（・あれば cases2.md）の事例の会社と同じにならない（CASES と照合）
     - AI の事例で、業態のキーが重なり、従業員数が事例の範囲（下限×0.85〜上限×1.15）に入る → NG
     - AI の事例で、業態のキーが重なり、同じ市町村で、事例の従業員数が分からない → NG（その会社の値と読まれるため）
     - 業種が確かめられていない事例（キー「業種未確認」）と同じ市町村 → 参考として表示（NG にしない）
     - AI ではない事例と業態・規模が近い → 参考として表示
  6. slug が _brief.md の45市町村と一致する（熊本市は kumamoto-city、美里町は misato-town-kumamoto、嘉島町は kashima-town）
  7. 試算の業種が wages.md にある（農業・漁業・林業は試算の業種にしない）
使い方: python3 -B data/area/kumamoto/_calc.py   （末尾に OK / NG を出す。-B で __pycache__ を作らない）
"""
import ast
import glob
import os
import re
import sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

sys.dont_write_bytecode = True

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ART = os.path.join(ROOT, "articles")
HERE = os.path.dirname(os.path.abspath(__file__))
SELF = "kumamoto"
KYUSHU_MOD = 3  # 九州7県の割り当て（月の削減時間×4 を7で割った余り）。熊本県は 3
KYUSHU = ("fukuoka", "saga", "nagasaki", "oita", "miyazaki", "kagoshima")

# wages.md の人件費時給（時給①×1.2 を十円単位に丸めた値。記事でも「約◯円」と書く値）。9業種とも wages.md にある
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

SLUGS = {
    # 市（14）
    "kumamoto-city", "yatsushiro", "hitoyoshi", "arao", "minamata", "tamana", "yamaga", "kikuchi", "uto",
    "kamiamakusa", "uki", "aso", "amakusa", "koshi",
    # 町（23）
    "misato-town-kumamoto", "gyokuto", "nankan", "nagasu", "nagomi", "ozu", "kikuyo", "minamioguni", "oguni",
    "takamori", "mifune", "kashima-town", "mashiki", "kosa", "yamato", "hikawa", "ashikita", "tsunagi", "nishiki",
    "taragi", "yunomae", "asagiri", "reihoku",
    # 村（8）
    "ubuyama", "nishihara", "minamiaso", "mizukami", "sagara", "itsuki", "yamae", "kuma",
}

# 照合が必須の県（2026-11-04 に main にある _calc.py）。ファイルがなければ NG。これ以外の県も glob で読む
REQUIRED = ("fukuoka", "gifu", "hiroshima", "miyazaki", "nagano", "nagasaki", "oita", "okayama", "saga", "shimane",
            "tottori", "yamaguchi", "yamanashi")


def read_plan_standard(src):
    """岡山県の形の PLAN（行頭の `PLAN = [` から行頭の `]` まで。各行の [0]=市町村, [2]=業種, [-2]=対象人数, [-1]=1人の月の業務量）。
    docstring の中の「PLAN = [」を拾わないよう、行頭の代入だけを探す（佐賀県の _calc.py は docstring に同じ文字列がある）。
    岐阜・長野・山梨のように業態のキーの列がない形も、[0]・[2]・[-2]・[-1] の位置が同じなので読める"""
    m = re.search(r"^PLAN = \[", src, re.M)
    if not m:
        raise ValueError("行頭の PLAN = [ がない")
    j = src.index("\n]\n", m.start())
    rows = ast.literal_eval(src[m.start() + 7:j + 2])
    return [(r[0], r[2], r[-2], r[-1]) for r in rows]


# 県ごとの PLAN の読み方。2026-11-04 の13県はすべて岡山県と同じ形（read_plan_standard）で読めた。
# 形の違う県が入ったら、ここに "県": 関数 を足す（関数は src を受け取り (市町村, 業種, 対象人数, 1人の業務量) のリストを返す）
READERS = {}

# cases.md・cases_outside.md・cases2.md の事例の会社（2026-11-04。cases2.md は 04:41 の版）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・計画・使用済み・自社製品を含む〕)
CASES = [
    # 熊本市（cases.md）
    ("税理士法人さくら優和パートナーズ（ChatGPT 研修、自己申告。156人〔うち熊本本部79人〕）", "熊本市", {"税理士", "会計事務所", "専門サービス"}, (79, 156), True),
    ("社会保険労務士法人プロセスコア（生成AIのコラム、ベンダーの事例）", "熊本市", {"社会保険労務士", "給与計算", "専門サービス"}, (1, 19), True),
    ("学校法人未来創造学園（生成AIのメール、ベンダーの事例）", "熊本市", {"専門学校", "教育"}, (20, 49), True),
    ("福田屋（菓子の製造・卸、AI 画像検査、数値なし）", "熊本市", {"菓子", "菓子製造"}, (75, 75), True),
    ("松栄産業・しょうぶ苑（AI 見守りカメラ、見出しだけ）", "熊本市", {"介護", "特別養護老人ホーム", "介護施設"}, None, True),
    ("熊本中央病院（Sail AI、361床、ベンダーのプレスリリース）", "熊本市", {"病院", "医療"}, None, True),
    ("ロッキー（スーパー、使用済み・高知市。本店は熊本市北区）", "熊本市", {"食品スーパー", "スーパー", "小売"}, None, True),
    ("ロッキー（関係の拠点、益城町福富）", "益城町", {"食品スーパー", "スーパー", "小売"}, None, True),
    ("Plaru × 熊本国際観光コンベンション協会（AI 旅行計画の実証、始まったばかり）", "熊本市", {"観光", "旅行"}, None, True),
    ("肥後銀行（生成AIチャットボット、大企業）", "熊本市", {"銀行", "金融"}, None, True),
    ("JA熊本市なす部会（使用済み・高知県安芸市）", "熊本市", {"農業", "野菜"}, None, True),
    # 天草市（行政の事務。企業の事例ではない）
    ("天草市の営農状況 AI 判定（行政・県の会議資料）", "天草市", {"行政"}, None, True),
    # 嘉島町・錦町（AI ではない）
    ("藤瀬農園（AI ではない、統合環境制御、計25名）", "嘉島町", {"農業", "野菜", "水稲"}, (25, 25), False),
    ("錦町スマート農業推進協議会（AI ではない、草刈りロボット）", "錦町", {"農業", "果樹"}, None, False),
    # 使用済み（要約のみ）
    ("しらぬい荘デイサービスセンター（通所介護の送迎表、使用済み・青森県南部町）", "宇城市", {"通所介護", "介護", "デイサービス"}, None, True),
    ("JA阿蘇いちご部会委託部（収量予測、使用済み・宮城県山元町）", "阿蘇市", {"農業", "いちご"}, None, True),
    ("児嶋牧場（肉牛の発情検知、使用済み・宮城県登米市。菊池郡の町名は未確認）", "所在未確認", {"農業", "肉用牛", "畜産"}, None, True),
    ("狩尾牧場（スマート放牧、verified: false。AI か未確認）", "阿蘇市", {"農業", "畜産"}, None, False),
    ("竹ノ原農園ほか（水田のドローン防除、verified: false。AI か未確認）", "山都町", {"農業", "水稲"}, None, False),
    # cases_outside.md（県外。本文で使えるのはどちらも農業の国の実証。試算の業種〔農業〕は使わない）
    ("沼澤農園（山形県尾花沢市、すいか、ドローン画像AIの出荷予測。山鹿市に割り当て）", "県外", {"農業", "すいか", "露地野菜"}, None, True),
    ("ベルファーム（静岡県菊川市、トマト、AI 自動選別。八代市に割り当て）", "県外", {"農業", "トマト", "施設園芸", "選果"}, None, True),
    ("JA阿寒（北海道釧路市、子牛の活動量のAI解析、予備）", "県外", {"農業", "畜産", "肉用牛"}, None, True),
    ("いちご畑（埼玉県深谷市、参考）", "県外", {"農業", "いちご"}, None, True),
    ("鈴生（静岡県静岡市、ブロッコリー、参考）", "県外", {"農業", "露地野菜"}, None, True),
    # cases2.md（2026-11-04 04:41 の版。D1 が追加）
    ("サイバーレコード（ChatGPT API、ふるさと納税・EC の運営代行、事業者の説明）", "熊本市", {"EC運営代行", "通販", "情報サービス"}, None, True),
    ("TORUTE（議事録の AI、事業承継コンサル、3名、市の事例集）", "熊本市", {"経営コンサルティング", "専門サービス"}, (3, 3), True),
    ("馬場石油（NotebookLM の社内FAQ、石油販売・貨物運送、28名、市の事例集）", "熊本市", {"燃料小売", "石油販売", "LPガス", "運送"}, (28, 28), True),
    ("CENTRIC 熊本支店（AI-OCR＋RPA、コンタクトセンター・BPO、全国企業の支店）", "熊本市", {"コンタクトセンター", "BPO"}, None, True),
    ("コスギ不動産ホールディングス（社内の生成AI、数値なし）", "熊本市", {"不動産", "賃貸管理"}, None, True),
    ("アネシス（住宅・リフォーム・不動産、数値なし）", "熊本市", {"住宅", "リフォーム", "不動産"}, None, True),
    ("SENSTYLE（AI 見守り、住宅型有料老人ホーム・定期巡回、134名）", "熊本市", {"介護", "有料老人ホーム", "訪問介護"}, (134, 134), True),
    ("青柳（郷土料理店、崇城大学と食材判別の AI、数値なし）", "熊本市", {"飲食店", "料理店"}, None, True),
    ("QoQ（ソフトウェア開発・AI 導入支援、数値なし）", "熊本市", {"情報サービス", "ソフトウェア"}, None, True),
    ("熊本放送（FAX の AI チェック、実証中、大きな組織）", "熊本市", {"放送"}, None, True),
    ("くまもとKDSグループ（AI の運転採点、自動車教習所、数値なし）", "熊本市", {"自動車教習所"}, None, True),
    ("WizTry（ワークスタイル変革大賞の奨励賞、名前だけ）", "熊本市", {"業種未確認"}, None, True),
    ("なかせ農園（サツマイモ、県の DX 公募型実証、AI の予測）", "大津町", {"農業", "いも類"}, None, True),
    ("アグリライト研究所（大津町の実証の研究側）", "水俣市", {"研究機関", "学術研究"}, None, True),
    ("熊本国際空港（AI 警備、空港運営、95名〔嘱託含む〕）", "益城町", {"空港運営", "警備"}, (95, 95), True),
    ("Lib Work（AI の住宅プラン検索、自社商品、331名、大企業）", "山鹿市", {"住宅", "建築"}, (331, 331), True),
    ("イマココナビ（令和8年熊本地震の生活情報サイト、市民の取組。企業の事例ではない）", "御船町", {"業種未確認"}, None, False),
    ("レストランバンブ（kuma-digi の事例、Instagram。AI ではない）", "玉名市", {"飲食店"}, None, False),
    ("おしろタクシー（kuma-digi の事例。AI ではない）", "菊陽町", {"旅客運送", "タクシー"}, None, False),
    # D2 が足したもの（2026-11-04。cases.md・cases2.md・cases_outside.md・九州財務局の資料に出る会社のうち、上に無かったもの）
    ("フジバンビ（kuma-digi の事例、センサー。AI ではない）", "熊本市", {"菓子", "菓子製造"}, None, False),
    ("社会福祉法人リデルライトホーム（kumamotodx.jp、AI の活用を模索の1文だけ・数値なし）", "熊本市", {"介護", "介護施設", "障害福祉"}, None, True),
    ("ぼたん園（県の介護の取組み事例、見守りセンサー。AI ではない）", "熊本市", {"介護", "介護施設"}, None, False),
    ("ヒサノ（配車・倉庫管理のシステム。AI ではない。本社 熊本市南区、営業所 菊陽町）", "熊本市", {"運送", "倉庫", "道路貨物運送"}, None, False),
    ("オフィス未来（熊本市 DXアクセラ R6、OCR から Web フォーム。AI ではない）", "熊本市", {"業種未確認"}, None, False),
    ("マイスティア（kumamotodx.jp、RPA で求人広告の効率化。AI ではない）", "益城町", {"情報サービス", "人材"}, None, False),
    ("天草池田電機（kumamotodx.jp、電子指示書。AI ではない）", "上天草市", {"電子部品", "電気機械"}, None, False),
    ("オムロンリレーアンドデバイス（kumamotodx.jp。AI ではない、大企業の工場）", "山鹿市", {"電気機械", "電子部品"}, None, False),
    ("MARUKU（kumamotodx.jp、LINE スタンプラリー。AI ではない）", "山都町", {"観光", "業種未確認"}, None, False),
    ("小国町森林組合（kumamotodx.jp、入札アプリ。AI ではない）", "小国町", {"林業", "木材"}, None, False),
    ("パールカラー（天草市の補助事業活用事例集、写真店。AI ではない）", "天草市", {"写真", "小売"}, None, False),
    ("JA鹿本すいか専門部（JA熊本市なす部会と同じ実証。すいかは営農管理システムで AI ではない）", "山鹿市", {"農業", "すいか"}, None, False),
    ("ソニーセミコンダクタマニュファクチャリング（九州財務局の資料の紹介事例①、センサー内の AI は製品。大企業の工場）", "菊陽町", {"電子部品", "半導体"}, (12800, 12800), True),
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 2026-11-04: 熊本県の時間（×4 を7で割った余り 3）で、既存の記事（711本）と14県の PLAN（443行。鹿児島を含む）で空いている値は、
# 月100時間未満では 84.75・95.25・97時間の3つしか割れる組がなく、多くは月120〜280時間。空いている値を、
# 規模に合わせて割り当てた（月84.75〜275.5時間・約29.8万〜97.5万円・21〜180名）。
# 業種・業態は stats.md の「市町村ごとの主要産業の候補」の (B) 中小企業の業種（経済センサスの事業所数・従業者数）から選んだ。
# 電子部品・生産用機械・輸送用機械の大企業の工場（菊陽町・合志市・大津町）は (A) で、試算には使わない（合志市は金属製品の協力会社、大津町は貨物運送、菊陽町は不動産）
PLAN = [
    # 県北広域本部（18）
    ("荒尾市", "arao", "医療・福祉", "病院（地域の中小病院、外来・入院）", {"病院", "医療"}, 115,
     "入退院の案内文・紹介状の返書の下書きと、看護記録の要約・院内の会議の議事録の作成", 32, 30.5),
    ("玉名市", "tamana", "卸売業・小売業", "青果の集出荷・卸売（市場・量販店へ出荷）", {"青果卸", "農産物の卸売", "卸売"}, 72,
     "取引先（市場・量販店）からの数量・規格・入荷予定の問い合わせへの回答と、出荷計画表・出荷伝票の作成", 26, 37),
    ("山鹿市", "yamaga", "製造業", "生産用機械（省力化装置・治具の設計製作）", {"生産用機械", "省力化装置", "治具"}, 68,
     "顧客との仕様の打合せ記録の要約と、見積書・取扱説明書・設計変更の連絡書の下書き", 22, 41.5),
    ("菊池市", "kikuchi", "製造業", "食料品（食肉の加工〔ハム・ソーセージ・惣菜〕）", {"食料品", "食肉加工"}, 135,
     "取引先からの原料の産地・アレルゲンの問い合わせへの回答と、製造記録・出荷ロットの記録の取りまとめ", 27, 39),
    ("阿蘇市", "aso", "宿泊・飲食サービス業", "温泉旅館・ホテル（団体・宴会を含む）", {"宿泊", "旅館", "ホテル"}, 62,
     "予約サイト・メールの問い合わせへの返信の下書きと、団体の見積書・館内案内の多言語の文の作成", 20, 46),
    ("合志市", "koshi", "製造業", "金属製品（精密板金・機械加工。装置メーカーなどの協力会社）", {"金属製品", "精密板金", "機械加工"}, 67,
     "元請けからの図面・仕様変更の問い合わせへの回答と、見積書・検査成績書・作業日報の取りまとめ", 24, 34.25),
    ("玉東町", "gyokuto", "医療・福祉", "通所介護・小規模多機能型居宅介護", {"通所介護", "小規模多機能", "介護"}, 40,
     "ケア記録の清書と、家族への連絡帳の文・運営推進会議の記録の作成", 16, 34.75),
    ("南関町", "nankan", "製造業", "生産用機械（産業機械の部品加工・組立）", {"生産用機械", "産業機械", "部品加工"}, 76,
     "取引先からの図面・仕様の問い合わせへの回答と、見積書・作業指示書・組立記録の取りまとめ", 24, 43),
    ("長洲町", "nagasu", "製造業", "金属製品（鉄骨・製缶品の溶接加工）", {"金属製品", "製缶", "鉄骨"}, 96,
     "元請けからの図面・工程の問い合わせへの回答と、溶接・検査の記録と作業日報の取りまとめ", 34, 28.5),
    ("和水町", "nagomi", "運輸業・郵便業", "道路貨物運送（地場の配送・倉庫）", {"道路貨物運送", "運送"}, 44,
     "配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報の集計", 17, 36),
    ("大津町", "ozu", "運輸業・郵便業", "道路貨物運送（工場の部品・資材の輸送と構内物流）", {"道路貨物運送", "部品輸送", "構内物流"}, 105,
     "荷主（工場）からの納入時刻・数量の問い合わせへの回答と、配車表・作業日報の取りまとめ", 22, 48.5),
    ("菊陽町", "kikuyo", "不動産・物品賃貸業", "不動産の売買仲介・賃貸管理（社宅・賃貸住宅の管理を含む）", {"不動産", "賃貸管理"}, 46,
     "入居者・オーナーからの問い合わせへの回答と、物件の紹介文・重要事項説明の下書き、管理報告書の作成", 17, 29),
    ("南小国町", "minamioguni", "宿泊・飲食サービス業", "温泉旅館（日帰り入浴・食事処を含む）", {"宿泊", "旅館"}, 48,
     "予約・問い合わせのメールへの返信の下書きと、宿泊プラン・館内案内の多言語の説明文の作成", 18, 41),
    ("小国町", "oguni", "卸売業・小売業", "飲食料品・日用品の小売（町内の店舗と配達）", {"小売", "食料品小売"}, 21,
     "仕入先への発注・在庫の確認と、配達の受付・チラシの文の作成", 8, 48.5),
    ("産山村", "ubuyama", "建設業", "総合工事業（道路・農業土木の工事）", {"建設", "土木", "農業土木"}, 27,
     "公共工事の提出書類の作成と、工事写真・日報の整理", 12, 28.25),
    ("高森町", "takamori", "卸売業・小売業", "農産物・加工品の集出荷と販売（直売所・通販）", {"農産物の販売", "直売所", "通販"}, 30,
     "取引先・個人客からの注文・在庫の問い合わせへの回答と、出荷伝票・商品説明の文の作成", 12, 45.75),
    ("西原村", "nishihara", "製造業", "食料品（惣菜・弁当の製造）", {"食料品", "惣菜", "弁当"}, 80,
     "取引先（小売・給食）からの受注・仕様の変更の連絡と、原材料の規格書・衛生管理の記録の取りまとめ", 30, 29.5),
    ("南阿蘇村", "minamiaso", "宿泊・飲食サービス業", "ペンション・ホテル（レストランを併設）", {"宿泊", "ペンション", "ホテル"}, 42,
     "予約サイト・メールの問い合わせへの返信の下書きと、レストランのメニュー・アレルゲン表示、周辺案内の文の作成", 16, 43.5),
    # 県央広域本部（9）
    ("熊本市", "kumamoto-city", "卸売業・小売業", "医薬品・医療機器の卸売（県内の病院・診療所・薬局へ納品）", {"卸売", "医薬品卸", "医療機器卸"}, 180,
     "得意先（病院・薬局）からの在庫・納期・代替品の問い合わせへの回答と、製品の添付文書・提案資料の要約", 38, 29),
    ("宇土市", "uto", "製造業", "プラスチック製品（包装容器・成形品）", {"プラスチック製品", "包装容器"}, 84,
     "取引先からの仕様・納期の問い合わせへの回答と、成形条件表・品質記録・不良の対策報告書の作成", 25, 41),
    ("宇城市", "uki", "製造業", "食料品（青果物・惣菜の加工）", {"食料品", "青果加工", "惣菜"}, 145,
     "量販店・外食の取引先からの規格・原材料の問い合わせへの回答と、商品規格書の改訂・衛生管理の記録の取りまとめ", 34, 32),
    ("美里町", "misato-town-kumamoto", "建設業", "総合工事業（土木・林道の工事）", {"建設", "土木", "林道"}, 50,
     "公共工事の提出書類・施工計画書の作成と、工事日報・安全書類の取りまとめ", 17, 43),
    ("御船町", "mifune", "卸売業・小売業", "石油製品・LPガスの販売と配送", {"燃料小売", "LPガス", "小売"}, 53,
     "得意先からの注文・配送の受付と配送表の作成、検針・保安点検の記録の取りまとめ", 20, 37.25),
    ("嘉島町", "kashima-town", "宿泊・飲食サービス業", "飲食店（町内と近隣に複数の店舗を運営）", {"飲食店", "外食"}, 66,
     "予約・問い合わせへの返信の下書きと、店舗のシフト表・仕込み量の計画、メニュー・アレルゲン表示の文の作成", 24, 39.5),
    ("益城町", "mashiki", "運輸業・郵便業", "道路貨物運送・倉庫（食品・日用品の共同配送）", {"道路貨物運送", "倉庫", "運送"}, 155,
     "荷主からの配送依頼・入出庫の問い合わせへの回答と、配車表・運転日報・点呼記録の取りまとめ", 23, 47),
    ("甲佐町", "kosa", "医療・福祉", "障害福祉サービス（就労継続支援・生活介護）", {"障害福祉", "就労継続支援"}, 54,
     "利用者の支援記録・個別支援計画の下書きと、家族・相談支援専門員への連絡文の作成", 20, 30.25),
    ("山都町", "yamato", "医療・福祉", "特別養護老人ホーム（短期入所を併設）", {"介護", "特別養護老人ホーム"}, 55,
     "ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文の作成", 20, 42.5),
    # 県南広域本部（15）
    ("八代市", "yatsushiro", "運輸業・郵便業", "道路貨物運送（農産物・食品の輸送）", {"道路貨物運送", "運送", "農産物輸送"}, 125,
     "荷主（農協・食品会社）からの集荷依頼の受付と配車表の下書き、到着予定・遅延の連絡、運転日報の集計", 24, 44.75),
    ("人吉市", "hitoyoshi", "宿泊・飲食サービス業", "温泉旅館・ホテル（宴会・食事処を含む）", {"宿泊", "旅館", "ホテル"}, 58,
     "予約サイト・電話の問い合わせへの返信の下書きと、宴会・団体の見積書、館内・周辺案内の文の作成", 22, 31),
    ("水俣市", "minamata", "医療・福祉", "通所介護・訪問介護（市内に複数の事業所）", {"通所介護", "訪問介護", "介護"}, 61,
     "通所・訪問の記録の清書と、ケアマネジャー・家族への連絡文の作成", 20, 40.75),
    ("氷川町", "hikawa", "医療・福祉", "介護老人保健施設（通所リハビリを併設）", {"介護", "介護老人保健施設"}, 47,
     "リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成", 18, 44.5),
    ("芦北町", "ashikita", "製造業", "窯業・土石製品（コンクリート製品の製造）", {"窯業・土石", "コンクリート製品"}, 51,
     "取引先（建設会社）からの仕様・納期の問い合わせへの回答と、試験成績書・出荷記録の取りまとめ", 20, 35.5),
    ("津奈木町", "tsunagi", "医療・福祉", "訪問介護・居宅介護支援（町内の事業所）", {"訪問介護", "居宅介護支援", "介護"}, 28,
     "訪問の記録の清書と、ケアプランの下書き・事業所間の連絡文の作成", 12, 31.75),
    ("錦町", "nishiki", "卸売業・小売業", "日用品・農業資材の小売（町内の店舗と配達）", {"小売", "農業資材", "日用品"}, 74,
     "得意先からの注文・配達の受付と、在庫表・請求書の取りまとめ、店頭・チラシの案内文の作成", 26, 33.5),
    ("多良木町", "taragi", "建設業", "総合工事業（土木・河川の工事）", {"建設", "土木", "河川工事"}, 78,
     "公共工事の施工計画書・提出書類の作成と、工事写真・出来形の記録の整理", 29, 31),
    ("湯前町", "yunomae", "卸売業・小売業", "食料品中心のスーパー（町内と近隣に店舗）", {"食品スーパー", "小売"}, 39,
     "仕入先への発注・在庫の確認と、売場のPOP・チラシの文の作成、パート・アルバイトの勤務表の取りまとめ", 19, 37),
    ("水上村", "mizukami", "医療・福祉", "特別養護老人ホーム（地域密着型）", {"介護", "特別養護老人ホーム"}, 24,
     "ケア記録の要約と、家族への近況の連絡文・行事の案内文の作成", 10, 46.5),
    ("相良村", "sagara", "製造業", "食料品（茶・農産物の加工品）", {"食料品", "製茶", "農産加工"}, 56,
     "通販・小売の取引先に出す商品説明・表示の文の作成と、受注・出荷・製造の記録の取りまとめ", 22, 34.5),
    ("五木村", "itsuki", "建設業", "総合工事業（道路・河川の維持工事）", {"建設", "土木", "道路維持"}, 22,
     "発注者への工事の報告書・提出書類の作成と、日報・安全書類の取りまとめ", 9, 47),
    ("山江村", "yamae", "建設業", "総合工事業（建築・住宅の改修）", {"建設", "建築", "住宅改修"}, 36,
     "施主への見積書・工程の連絡文の作成と、工事日報・写真の整理", 16, 31.25),
    ("球磨村", "kuma", "医療・福祉", "グループホーム・通所介護（村内の事業所）", {"グループホーム", "通所介護", "介護"}, 38,
     "ケア記録の清書と、家族への連絡文・運営推進会議の記録の作成", 16, 41.75),
    ("あさぎり町", "asagiri", "医療・福祉", "訪問看護・訪問介護（町内の事業所）", {"訪問看護", "訪問介護", "介護"}, 45,
     "訪問の記録の清書と、主治医への報告書・ケアマネジャーへの連絡文の作成", 16, 47),
    # 天草広域本部（3）
    ("上天草市", "kamiamakusa", "運輸業・郵便業", "水運（旅客船・観光船の運航）", {"水運", "旅客船"}, 41,
     "予約・運航状況の問い合わせへの回答と、乗船名簿・運航記録・安全管理の書類の取りまとめ", 16, 45.25),
    ("天草市", "amakusa", "製造業", "食料品（水産物の加工〔干物・練り製品など〕）", {"食料品", "水産加工"}, 60,
     "量販店・通販の取引先からの原材料・産地・賞味期限の問い合わせへの回答と、商品説明・表示の文の作成、製造記録の取りまとめ", 20, 47.75),
    ("苓北町", "reihoku", "医療・福祉", "病院（療養病床を含む地域の病院）", {"病院", "医療"}, 63,
     "入退院の案内文・診療情報提供書の下書きと、病棟の記録・会議録の要約", 24, 37.75),
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def other_plans():
    """全県の _calc.py の PLAN を読み、(県, 市町村, 削減時間, 万円) を返す。読めない県・必須の県のファイルがなければ None を入れる（NG）。"""
    out, read, failed = [], {}, []
    paths = sorted(glob.glob(os.path.join(ROOT, "data", "area", "*", "_calc.py")))
    found = {os.path.basename(os.path.dirname(p)): p for p in paths}
    for pref in REQUIRED:
        if pref not in found:
            print(f"NG {pref} の _calc.py がない（必須）")
            out.append(None)
            failed.append(pref)
    for pref, path in found.items():
        if pref == SELF:
            continue
        src = open(path, encoding="utf-8").read()
        try:
            rows = READERS.get(pref, read_plan_standard)(src)
        except Exception as e:  # noqa: BLE001 形が違う。エラーにせず、読めなかった県として表示する
            print(f"NG {pref} の PLAN が読めない（{type(e).__name__}: {e}）。READERS に読み方を足す")
            out.append(None)
            failed.append(pref)
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
            failed.append(pref)
        read[pref] = len(rows)
        if not rows:
            print(f"（参考）{pref} の PLAN はまだ空（作成中）。行が入ったら再実行する")
    return out, read, failed


def existing():
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（岡山県の _calc.py と同じ拾い方）。"""
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


def in_range(size, csize):
    lo, hi = csize
    return lo * 0.85 <= size <= hi * 1.15


def used_values():
    """既存の記事と他県の PLAN で使われている時間・万円（辞書）を返す。割り当ての探索用"""
    _, _, ex_h, ex_m, _, _ = existing()
    op, _, _ = other_plans()
    pl_h, pl_m = {}, {}
    for r in op:
        if r is None:
            continue
        label, city, h, m = r
        pl_h.setdefault(h, f"{label}{city}")
        pl_m.setdefault(m, f"{label}{city}")
    return ex_h, ex_m, pl_h, pl_m


def main():
    n_files, n_sec, ex_h, ex_m, ex_s, per_file = existing()
    empty = [k for k, v in per_file.items() if v[1] == 0]
    if empty:
        print("NG 試算の金額を拾えなかった既存の記事:", empty)
    by_pref = Counter(re.sub(r"^2026-1\d-\d+-area-([a-z]+).*", r"\1", k) for k in per_file)
    print(f"既存の地域ページ: {n_files}本（うち試算の節があるもの {n_sec}本、{len(by_pref)}県）。"
          f"拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種・規模 {len(ex_s)}種")
    op, read, failed = other_plans()
    ok = None not in op
    pl_h, pl_m, kyushu_m = {}, {}, {}
    for r in op:
        if r is None:
            continue
        label, city, h, m = r
        pl_h.setdefault(h, f"{label}{city}（_calc.py の PLAN）")
        pl_m.setdefault(m, f"{label}{city}（_calc.py の PLAN）")
        if label in KYUSHU:
            kyushu_m.setdefault(m, f"{label}{city}")
    print(f"他県の PLAN: {len([r for r in op if r])}行（{len(read)}県: "
          + "・".join(f"{k} {v}" for k, v in sorted(read.items())) + f"。時間 {len(pl_h)}種・万円 {len(pl_m)}種）")
    print("九州の他県で読んだ PLAN:", "・".join(k for k in KYUSHU if k in read) or "なし",
          "／まだない県:", "・".join(k for k in KYUSHU if k not in read and k not in failed) or "なし")
    if failed:
        print("NG 読めなかった県:", "・".join(failed))
    for fn in ("cases.md", "cases2.md", "cases_outside.md"):
        co = os.path.join(HERE, fn)
        if os.path.exists(co) and os.path.getmtime(co) > os.path.getmtime(os.path.abspath(__file__)):
            print(f"（注意）{fn} が _calc.py より新しい。事例の会社（業態・従業員数・所在）を CASES に足したか確かめる")

    seen_h, seen_m, seen_s = {}, {}, {}
    notes = []
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | 年間 |")
    print("|---|---|---|---|---|---|---|---|")
    for (city, slug, ind, sub, keys, size, task, n, hrs) in PLAN:
        if ind not in RATE:
            print(f"  NG {city} の業種 {ind} は wages.md にない")
            ok = False
            continue
        h = Decimal(str(n)) * Decimal(str(hrs)) * Decimal("0.25")
        yen = h * RATE[ind]
        m = man(yen)
        y = man(yen * 12)
        print(f"| {city} | {ind}（{sub}） | {size}名 | {n}名×{hrs}時間×25% | {h.normalize():f}時間 | 約{RATE[ind]:,}円 | 約{m}万円 | 約{y}万円 |")
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 熊本県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                extra = "（九州の他県。熊本側が直す）" if label == "金額" and key in kyushu_m else ""
                print(f"  NG 他県の PLAN と{label}が重なる{extra}: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 熊本県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
            ok = False
        seen_s[size] = city
        if (h * 4) % 1 != 0:
            print(f"  NG {city} の時間が0.25時間刻みでない ({h})")
            ok = False
        elif int(h * 4) % 7 != KYUSHU_MOD:
            print(f"  NG {city} の時間が九州の割り当て（×4 を7で割った余り {KYUSHU_MOD}）でない ({h}、余り {int(h * 4) % 7})")
            ok = False
        if abs((yen % 1000) - 500) <= 100:
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
    slugs = {p[1] for p in PLAN}
    if slugs != SLUGS:
        print("NG slug が _brief.md と違う:", sorted(slugs ^ SLUGS))
        ok = False
    if not PLAN:
        print("NG PLAN が空")
        print("NG")
        return
    n_ex_size = sum(1 for p in PLAN if p[5] in ex_s)
    print(f"\n市町村ページ: {len(PLAN)}、市町村名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}")
    print(f"時間の範囲 {min(seen_h).normalize():f}〜{max(seen_h).normalize():f}時間、金額の範囲 約{min(seen_m)}〜{max(seen_m)}万円、規模 {min(seen_s)}〜{max(seen_s)}名")
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは熊本県の中だけを NG にする）")
    print(f"（参考）1人の業務量が◯.25・◯.75時間のページ: {sum(1 for p in PLAN if (Decimal(str(p[8])) * 2) % 1 != 0)}件")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 45 else "NG")


if __name__ == "__main__":
    main()
