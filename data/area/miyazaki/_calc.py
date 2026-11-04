#!/usr/bin/env python3
"""宮崎県26市町村の試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-11-04）。

data/area/okayama/_calc.py を元に作った（九州の割り当ての照合は data/area/oita/_calc.py と同じ形）。
県ページ（/area/miyazaki/）には試算を入れない（島根・鳥取・広島・山口・岡山・大分と同じ）ので、PLAN は26行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **九州7県の割り当て**: 月の削減時間（0.25時間刻み）×4 を7で割った余りが 5（宮崎県）になる時間だけを使う
     （1.25, 3, 4.75, 6.5 … 1.75時間刻み。data/area/_kyushu/shared.md）
  1. 26ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、宮崎県を除く。岡山県を含む）の「## 試算」の節の
     「◯時間」「◯万円」の値と重ならない（拾い方は鳥取・広島・岡山の _calc.py と同じ。拾いすぎは「重ならない」側に働く）
  3. 山梨・島根・鳥取・山口・広島・岡山の _calc.py の PLAN（必須。ファイルがなければ NG）と、
     九州の他県の _calc.py の PLAN（main に入っていれば。なければ飛ばす。git pull してから実行する）と重ならない。
     **金額が九州の他県と重なったら宮崎側が直す**（先に PLAN を push した県を優先する取り決め）
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円ちょうど）にならない
  5. 試算の業種（業態）・規模が cases.md（あれば cases2.md・cases_outside.md）の事例の会社と同じにならない（CASES と照合）
     - AI の事例で、業態のキーが重なり、従業員数が事例の範囲（区分なら下限×0.85〜上限×1.15）に入る → NG
     - AI の事例で、業態のキーが重なり、同じ市町村で、事例の従業員数が分からない → NG
     - 業種が確かめられていない事例（キー「業種未確認」）と同じ市町村 → 参考として表示（NG にしない）
     - AI ではない事例と業態・規模が近い → 参考として表示
  6. slug が _brief.md の26市町村と一致する（宮崎市は miyazaki-city、美郷町は misato-town-miyazaki）
  7. 試算の業種が wages.md にある（農業・林業・漁業は試算の業種にしない）
使い方: python3 data/area/miyazaki/_calc.py   （末尾に OK / NG を出す）
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
SELF = "miyazaki"
KYUSHU_MOD = 5  # 九州7県の割り当て（月の削減時間×4 を7で割った余り）

# wages.md の人件費時給（時給①×1.2 を十円単位に丸めた値。記事でも「約◯円」と書く値）。
# 山口県の PLAN が不動産・学術研究・情報通信を使っているので、他県の PLAN を読むために9業種とも入れる
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

SLUGS = {"miyazaki-city", "miyakonojo", "nobeoka", "nichinan", "kobayashi", "hyuga", "kushima", "saito", "ebino",
         "mimata", "takaharu", "kunitomi", "aya", "takanabe", "shintomi", "kijo", "kawaminami", "tsuno",
         "kadogawa", "misato-town-miyazaki", "takachiho", "hinokage", "gokase", "nishimera", "morotsuka", "shiiba"}

# 照合する他県の PLAN（公開前の割り当て）。6県とも必須
OTHER_PLANS = (("yamanashi", "山梨県"), ("shimane", "島根県"), ("tottori", "鳥取県"),
               ("yamaguchi", "山口県"), ("hiroshima", "広島県"), ("okayama", "岡山県"))
# 九州の他県（並行で作成中）。_calc.py が main に入っていれば照合する（なければ飛ばす）。git pull してから実行する
KYUSHU_PLANS = (("fukuoka", "福岡県"), ("saga", "佐賀県"), ("nagasaki", "長崎県"), ("kumamoto", "熊本県"),
                ("oita", "大分県"), ("kagoshima", "鹿児島県"))

# cases.md の事例の会社（2026-11-04 の cases.md から。cases2.md・cases_outside.md はまだない）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・使用済み・研究・計画を含む〕)
# subsidy_a_areas.md・gov_ai.md の「事例の手がかり」（cases2 に送った会社）も、cases2.md ができる前の予防として入れた
CASES = [
    # 宮崎市
    ("宮崎銀行（生成AIの稟議書、大企業・報道）", "宮崎市", {"銀行", "金融"}, None, True),
    ("デンサン（牛個体識別AIの研究、IT企業）", "宮崎市", {"情報サービス", "システム開発"}, (214, 214), True),
    ("宮崎トヨタ自動車（RPA・AI-OCR、島根の cases_outside で記録済み）", "宮崎市", {"自動車販売", "自動車整備"}, None, True),
    ("丸栄宮崎（県の事例集、AIの記述なし）", "宮崎市", {"業種未確認"}, None, False),
    ("クリエイティブマシン（CAD連携の見積、AIは今後）", "宮崎市", {"機械加工", "金属加工", "生産用機械"}, None, False),
    ("前田包装容器（県の事例集、イラストAI・ChatGPT、手がかり）", "宮崎市", {"卸売", "包装資材", "包装資材の卸売"}, (20, 20), True),
    ("アシストユウ（AI移動式監視カメラ、ベンダー自身）", "宮崎市", {"情報サービス", "AIカメラ"}, (8, 8), True),
    ("スパークジャパン（RPA＆AI-OCR、ベンダー自身）", "宮崎市", {"情報サービス", "システム開発"}, (84, 84), True),
    ("教育情報サービス（AIの自動作問・添削、県の委員会資料）", "宮崎市", {"教育", "eラーニング", "情報サービス"}, None, True),
    ("フェニックスリゾート（観光、AIの語あり、大企業とみられる）", "宮崎市", {"宿泊", "ホテル", "リゾート"}, None, True),
    # 新富町
    ("AGRIST／AGRIST FARM（自社農場、ベンダー自身の発表）", "新富町", {"農業", "野菜", "ロボット開発"}, (30, 30), True),
    ("新富町農業研究会（使用済み・高知県芸西村）", "新富町", {"農業", "野菜"}, None, True),
    # 都城市
    ("スマイリング・パーク（生成AI・介護記録の音声入力、数値なし）", "都城市", {"介護", "社会福祉法人", "障害福祉", "保育"}, None, True),
    ("ヤマエ食品工業（受注のデジタル化、AIは今後）", "都城市", {"食料品", "食品製造", "調味料"}, None, False),
    ("ＬＣトランス（飼料タンクのIoT、AIは今後）", "都城市", {"運送", "飼料の配送", "道路貨物運送"}, None, False),
    ("サニー・シーリング（使用済み・島根県出雲市）", "都城市", {"業種未確認"}, None, True),
    ("山田第二農場（使用済み・青森県十和田市）", "都城市", {"畜産", "養豚"}, None, True),
    ("霧島酒造（使用済み・香川県直島町）", "都城市", {"酒類製造", "焼酎", "飲料"}, None, True),
    ("都城医科機器（県の事例集、AIは計画だけ）", "都城市", {"卸売", "医療機器の卸売"}, (12, 12), False),
    # 小林市
    ("坂下組（AIの労務安全書類の入力補助、数値なし）", "小林市", {"建設", "土木", "総合工事"}, None, True),
    ("川野畜産（使用済み・山形県尾花沢市）", "小林市", {"畜産", "肉用牛"}, None, True),
    # 西都市
    ("アルバック機工（AIカメラ・スマートファクトリー、規模未確認）", "西都市", {"はん用機械", "生産用機械", "真空ポンプ"}, None, True),
    ("ジェイエイフーズみやざき（AIの収量予測は計画）", "西都市", {"食料品", "冷凍野菜", "農産加工"}, None, False),
    # 日南市・串間市
    ("浅野水産（近海かつお一本釣り、AIは今後）", "日南市", {"漁業", "水産"}, None, False),
    ("ニチワ（ドライブレコーダー、AIではない）", "日南市", {"業種未確認"}, None, False),
    ("大田商店（陸上養殖、AIの記述なし）", "串間市", {"養殖", "水産"}, None, False),
    ("黒瀬水産（使用済み・愛媛県愛南町）", "串間市", {"養殖", "水産"}, None, True),
    # 延岡市・日向市・門川町・諸塚村・高千穂町
    ("三桜電設（県の事例集、AI-OCRは今後）", "延岡市", {"電気工事", "建設"}, (80, 80), False),
    ("吉玉精鍍・中園工業所（IoT・ロボット、AIではない）", "延岡市", {"業種未確認"}, None, False),
    ("旭建設（gov の手がかり、未確認）", "日向市", {"建設", "土木", "総合工事"}, None, True),
    ("クリエート（直売所システム、AIではない。ベンダー）", "門川町", {"情報サービス"}, None, False),
    ("諸塚村の森林DXの実証（使用済み・愛媛県久万高原町）", "諸塚村", {"林業"}, None, True),
    ("プリエール高千穂（デジタルサイネージ、AIではない）", "高千穂町", {"業種未確認"}, None, False),
    # 県（所在を確かめていない・社名なし）
    ("ドリームブロッサム（AIのEC自動掲載、県の委員会資料。所在未確認）", "所在未確認", {"卸売", "小売", "通販", "知育玩具"}, None, True),
    ("県の肉用牛 A社のスマート機器（社名なし）", "所在未確認", {"畜産", "肉用牛"}, None, True),
    ("県の海面養殖の AI 魚体測定・尾数カウント（社名なし）", "所在未確認", {"養殖", "水産"}, None, True),
    ("県の令和5年度実装事例（食材残量のAI・生成AI、社名なし）", "所在未確認", {"業種未確認"}, None, True),
    ("工業技術センターのネジの外観検査AI（企業名なし）", "所在未確認", {"業種未確認"}, None, True),
    ("新福青果（国の実証、ICTでAIではない。検索の要約だけ）", "所在未確認", {"農業", "野菜"}, None, False),
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 2026-11-04: 九州の割り当て（×4 を7で割った余り5）の時間で、既存の全ページ（宮崎を除く）と6県＋九州2県（長崎・大分）の PLAN に
# 空いている値を探して決めた（月71.25〜228.75時間・約24.9万〜81.0万円・20〜180名）。余り5で月110時間未満に空いている時間は
# 71.25・83.5・90.5・102.75 などごくわずかで、小さい組（対象5〜10名・◯.0/◯.5時間）は作れない。
# 業種・業態は stats.md の「市町村ごとの主要産業の候補」の (B) 中小企業の業種（経済センサスの従業者・中分類）から選んだ。
# 諸塚村だけ1人の業務量が◯.25時間、綾町・都農町・西都市が◯.75時間（ほかに空きがない。D1.md の判断が必要な点）
PLAN = [
    # 宮崎・東諸県（3）
    ("宮崎市", "miyazaki-city", "卸売業・小売業", "飲食料品の卸売（業務用食品・農産物。市内に本社と配送センター）", {"卸売", "飲食料品卸"}, 180,
     "飲食店・ホテル・量販店からの受注・欠品・納期の問い合わせへの回答と、商品規格書・提案書・見積書の下書き", 30, 30.5),
    ("国富町", "kunitomi", "製造業", "金属製品（金属部品の板金・溶接加工）", {"金属製品", "板金", "溶接"}, 65,
     "取引先からの図面・見積の問い合わせへの回答と、材料の証明書・検査成績書・作業日報の取りまとめ", 20, 26.5),
    ("綾町", "aya", "製造業", "飲料（酒類・清涼飲料などの飲料の製造）", {"飲料", "酒類製造"}, 40,
     "酒販店・取引先からの受注・在庫・出荷の問い合わせへの回答と、製造・出荷の記録、商品説明の文の作成", 12, 37.75),
    # 南那珂（2）
    ("日南市", "nichinan", "製造業", "木材・木製品（スギの製材・乾燥材の製造）", {"木材・木製品", "製材"}, 75,
     "工務店・プレカット工場からの在庫・寸法・納期の問い合わせへの回答と、出荷伝票・乾燥や品質の記録の取りまとめ", 20, 33.5),
    ("串間市", "kushima", "医療・福祉", "介護老人保健施設（通所リハビリを併設）", {"介護", "介護老人保健施設"}, 50,
     "リハビリ・ケアの記録の要約と、入所・退所の説明文書、ケアマネジャーへの報告書の作成", 17, 39.0),
    # 北諸県（2）
    ("都城市", "miyakonojo", "製造業", "食料品（食肉の処理・食肉加工品の製造）", {"食料品", "食肉加工"}, 160,
     "量販店・外食の取引先からの規格・原料の産地・アレルゲンの問い合わせへの回答と、規格書の改訂・衛生管理の記録の取りまとめ", 26, 32.5),
    ("三股町", "mimata", "運輸業・郵便業", "道路貨物運送（食品・飼料などの地場輸送）", {"運送", "道路貨物運送"}, 60,
     "配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計", 18, 41.5),
    # 西諸県（3）
    ("小林市", "kobayashi", "医療・福祉", "特別養護老人ホーム（短期入所・通所介護を併設）", {"介護", "特別養護老人ホーム"}, 90,
     "ケア記録・事故やヒヤリハットの報告の清書と、家族への近況の連絡文、介護計画の見直しの下書き", 26, 29.0),
    ("えびの市", "ebino", "卸売業・小売業", "飲食料品の小売（農畜産物・特産品の販売店と通信販売）", {"小売", "飲食料品小売", "通販"}, 42,
     "通販の注文・問い合わせへの返信と商品説明の文の作成、店舗の売上・在庫の日報の取りまとめ", 19, 29.0),
    ("高原町", "takaharu", "製造業", "木材・木製品（プレカット・木材の加工）", {"木材・木製品", "プレカット"}, 36,
     "工務店からの加工図・納期の問い合わせへの回答と、加工指示書・出荷の記録の取りまとめ", 10, 28.5),
    # 西都・児湯（7）
    ("西都市", "saito", "建設業", "総合工事業（土木・農業土木）", {"建設", "土木"}, 62,
     "公共工事の施工計画書・提出書類の作成と、工事写真・出来形の記録の整理", 12, 44.75),
    ("高鍋町", "takanabe", "宿泊・飲食サービス業", "飲食店（町内と近隣に数店舗。仕出し・宴会を含む）", {"飲食店", "仕出し"}, 48,
     "予約・宴会・仕出しの問い合わせへの返信と見積書の下書き、店舗ごとの売上・仕入れの日報の取りまとめ", 15, 47.0),
    ("新富町", "shintomi", "製造業", "食料品（野菜の加工品・カット野菜の製造）", {"食料品", "農産加工", "カット野菜"}, 70,
     "量販店・給食の取引先からの規格・数量変更の連絡への回答と、原料の受入れ記録・衛生管理の記録の取りまとめ", 22, 29.5),
    ("西米良村", "nishimera", "建設業", "総合工事業（治山・林道の工事）", {"建設", "治山", "林道"}, 30,
     "治山・林道工事の施工計画書・安全書類の作成と、作業日報・出来形の記録の整理", 12, 46.5),
    ("木城町", "kijo", "医療・福祉", "通所介護・訪問介護（居宅介護支援を併設）", {"介護", "通所介護", "訪問介護"}, 44,
     "通所・訪問の記録の清書と、ケアマネジャー・家族への連絡文、サービス提供の実績の取りまとめ", 18, 34.5),
    ("川南町", "kawaminami", "製造業", "食料品（豚肉の処理とハム・ソーセージなどの食肉加工品の製造）", {"食料品", "食肉加工", "ハム・ソーセージ"}, 110,
     "通販・量販店向けの商品説明・表示の文の作成と、受注・製造ロット・出荷の記録の取りまとめ", 24, 32.0),
    ("都農町", "tsuno", "卸売業・小売業", "農畜産物・加工品の集出荷と卸売", {"農産物の卸売", "集出荷"}, 38,
     "取引先・量販店からの注文・数量・規格の問い合わせへの回答と、出荷伝票・精算書の取りまとめ", 12, 34.25),
    # 日向・東臼杵（5）
    ("日向市", "hyuga", "製造業", "食料品（鶏肉の処理・加工品の製造）", {"食料品", "鶏肉加工"}, 150,
     "取引先からの受注量・納期・規格の問い合わせへの回答と、出荷ロットごとの品質記録・取引先向けの報告書の作成", 27, 30.0),
    ("門川町", "kadogawa", "製造業", "食料品（水産物・農産物の加工品の製造）", {"食料品", "水産加工"}, 85,
     "取引先からの原料・産地・賞味期限の問い合わせへの回答と、製造記録・表示の確認表の取りまとめ", 22, 33.0),
    ("諸塚村", "morotsuka", "建設業", "総合工事業（村道・治山の土木工事）", {"建設", "土木"}, 20,
     "土木工事の提出書類・写真台帳の作成と、作業日報の取りまとめ", 8, 45.25),
    ("椎葉村", "shiiba", "建設業", "総合工事業（道路・河川の土木、災害復旧）", {"建設", "土木", "災害復旧"}, 39,
     "災害復旧・公共工事の提出書類と写真台帳の作成、発注者への工程・安全の報告の取りまとめ", 16, 41.0),
    ("美郷町", "misato-town-miyazaki", "医療・福祉", "介護老人福祉施設（地域密着型。グループホームを併設）", {"介護", "グループホーム", "地域密着型"}, 34,
     "ケア記録・夜勤の申し送りの清書と、家族への連絡文、提出書類の下書き", 13, 44.0),
    # 延岡（1）
    ("延岡市", "nobeoka", "製造業", "生産用機械（工場設備・産業機械の部品加工・組立。大手工場の協力会社）", {"生産用機械", "機械部品", "設備保全"}, 130,
     "元請けの工場からの図面・仕様・納期の問い合わせへの回答と、加工・組立の記録、検査成績書・作業報告書の取りまとめ", 25, 31.0),
    # 西臼杵（3）
    ("高千穂町", "takachiho", "宿泊・飲食サービス業", "旅館・ホテル（観光客の宿泊・団体の食事を含む）", {"宿泊", "旅館"}, 55,
     "予約サイト・メールの問い合わせへの返信の下書きと、団体・ツアーの見積書、多言語の館内・周辺の案内文の作成", 16, 44.5),
    ("日之影町", "hinokage", "卸売業・小売業", "食品・日用品の小売（町内に数店舗、配達を含む）", {"小売", "食品・日用品"}, 26,
     "取引先への発注・欠品の連絡と、配達の注文の受付・整理、店舗の日報・売場の掲示の文の作成", 11, 45.0),
    ("五ヶ瀬町", "gokase", "建設業", "総合工事業（建築・土木）", {"建設"}, 28,
     "工事日報・安全書類の取りまとめと、施主・発注者への工程の連絡文、見積書の下書き", 12, 43.0),
]

def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def other_plans():
    """5県の _calc.py の PLAN を読み、(県, 市町村, 削減時間, 万円) を返す。ファイルがなければ None を入れる（NG）。"""
    out = []
    for pref, label in OTHER_PLANS + KYUSHU_PLANS:
        path = os.path.join(ROOT, "data", "area", pref, "_calc.py")
        if not os.path.exists(path) and (pref, label) in KYUSHU_PLANS:
            print(f"（参考）{label}の _calc.py はまだない")
            continue
        if not os.path.exists(path):
            print(f"NG {label}の _calc.py がない: {path}")
            out.append(None)
            continue
        src = open(path, encoding="utf-8").read()
        i = src.index("PLAN = [")
        j = src.index("\n]\n", i)
        rows = ast.literal_eval(src[i + 7:j + 2])
        n_skip = 0
        for r in rows:
            city, ind, n, hrs = r[0], r[2], r[-2], r[-1]
            if ind not in RATE:
                n_skip += 1
                continue
            h = Decimal(str(n)) * Decimal(str(hrs)) * Decimal("0.25")
            out.append((label, city, h, man(h * RATE[ind])))
        if n_skip:
            print(f"NG {label}の PLAN に時給の分からない業種が {n_skip}行ある（RATE に足す）")
            out.append(None)
    return out


def existing():
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（鳥取県・広島県の _calc.py と同じ拾い方）。"""
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


def main():
    n_files, n_sec, ex_h, ex_m, ex_s, per_file = existing()
    empty = [k for k, v in per_file.items() if v[1] == 0]
    if empty:
        print("NG 試算の金額を拾えなかった既存の記事:", empty)
    by_pref = Counter(re.sub(r"^2026-1\d-\d+-area-([a-z]+).*", r"\1", k) for k in per_file)
    print(f"既存の地域ページ: {n_files}本（うち試算の節があるもの {n_sec}本。山梨 {by_pref.get('yamanashi', 0)}本・"
          f"島根 {by_pref.get('shimane', 0)}本・鳥取 {by_pref.get('tottori', 0)}本・広島 {by_pref.get('hiroshima', 0)}本・"
          f"山口 {by_pref.get('yamaguchi', 0)}本・岡山 {by_pref.get('okayama', 0)}本を含む）。拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種・規模 {len(ex_s)}種")
    op = other_plans()
    ok = None not in op
    pl_h, pl_m = {}, {}
    for r in op:
        if r is None:
            continue
        label, city, h, m = r
        pl_h.setdefault(h, f"{label}{city}（_calc.py の PLAN）")
        pl_m.setdefault(m, f"{label}{city}（_calc.py の PLAN）")
    print(f"他県の PLAN: {len([r for r in op if r])}行（時間 {len(pl_h)}種・万円 {len(pl_m)}種）")
    for fn in ("cases2.md", "cases_outside.md"):
        if os.path.exists(os.path.join(HERE, fn)):
            print(f"（注意）{fn} がある。会社（業態・従業員数）を CASES に足したか確かめる")

    seen_h, seen_m, seen_s = {}, {}, {}
    n_quarter = 0
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
                print(f"  NG 宮崎県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 宮崎県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
            ok = False
        seen_s[size] = city
        if (h * 4) % 1 == 0 and int(h * 4) % 7 != KYUSHU_MOD:
            print(f"  NG {city} の時間 {h} は九州の割り当て（×4 を7で割った余り {KYUSHU_MOD}）に合わない（余り {int(h * 4) % 7}）")
            ok = False
        if (h * 4) % 1 != 0:
            print(f"  NG {city} の時間が0.25時間刻みでない ({h})")
            ok = False
        if (h * 2) % 1 != 0:
            n_quarter += 1
        if (yen % 1000) == 500:
            print(f"  NG {city} の金額が四捨五入の境目（{yen}円）")
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
        print("NG slug が _brief.md と違う:", slugs ^ SLUGS)
        ok = False
    if not PLAN:
        print("NG PLAN が空")
        print("NG")
        return
    n_ex_size = sum(1 for p in PLAN if p[5] in ex_s)
    print(f"\n市町村ページ: {len(PLAN)}、市町村名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}")
    print(f"時間の範囲 {min(seen_h)}〜{max(seen_h)}時間、金額の範囲 約{min(seen_m)}〜{max(seen_m)}万円、規模 {min(seen_s)}〜{max(seen_s)}名")
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは宮崎県の中だけを NG にする）")
    print(f"（参考）時間が◯.25・◯.75になるページ: {n_quarter}件")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 26 else "NG")


if __name__ == "__main__":
    main()
