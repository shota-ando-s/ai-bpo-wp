#!/usr/bin/env python3
"""岡山県27市町村の試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-11-03）。

data/area/hiroshima/_calc.py を元に作った。県ページ（/area/okayama/）には試算を入れない（島根・鳥取・広島・山口と同じ）ので、PLAN は27行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  1. 27ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、岡山県を除く。山梨・島根・鳥取・広島・山口の記事を含む）の
     「## 試算」の節に出てくる「◯時間」「◯万円」の値と重ならない。拾い方は鳥取県・広島県の _calc.py と同じ
     （1人の業務量・年間の額・差し引き後の額なども広めに拾う。拾いすぎは「重ならない」側に働く）
  3. 山梨県・島根県・鳥取県・山口県・広島県の _calc.py の PLAN の月の削減時間・月の時間換算額とも重ならない
     （5県とも必須。ファイルがなければ NG）
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円ちょうど）にならない
  5. 試算の業種（業態）・規模が cases.md（・cases_outside.md）の事例の会社と同じにならない（CASES と照合）
     - AI の事例で、業態のキーが重なり、従業員数が事例の範囲（区分なら下限×0.85〜上限×1.15）に入る → NG
     - AI の事例で、業態のキーが重なり、同じ市町村で、事例の従業員数が分からない → NG（その会社の値と読まれるため）
     - 業種が確かめられていない事例（キー「業種未確認」）と同じ市町村 → 参考として表示（NG にしない）
     - AI ではない事例と業態・規模が近い → 参考として表示
  6. slug が _brief.md の27市町村と一致する（岡山市は okayama-city、新庄村は shinjo-village）
  7. 試算の業種が wages.md にある（農業・漁業・林業は試算の業種にしない）
使い方: python3 data/area/okayama/_calc.py   （末尾に OK / NG を出す）
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
SELF = "okayama"

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

SLUGS = {"okayama-city", "kurashiki", "tsuyama", "tamano", "kasaoka", "ibara", "soja", "takahashi", "niimi", "bizen",
         "setouchi", "akaiwa", "maniwa", "mimasaka", "asakuchi", "wake", "hayashima", "satosho", "yakage", "kagamino",
         "shoo", "nagi", "kumenan", "misaki", "kibichuo", "shinjo-village", "nishiawakura"}

# 照合する他県の PLAN（公開前の割り当て）。5県とも必須
OTHER_PLANS = (("yamanashi", "山梨県"), ("shimane", "島根県"), ("tottori", "鳥取県"),
               ("yamaguchi", "山口県"), ("hiroshima", "広島県"))

# cases.md の事例の会社（2026-11-03 の cases.md から）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・使用済みを含む〕)
# cases_outside.md（完成版）と cases2.md の会社は 2026-11-03 に D2 が足した
CASES = [
    # 岡山市
    ("水内ゴム（AIカメラの良否判定、見込み）", "岡山市", {"ゴム製品"}, None, True),
    ("ピコシステム（生成AI研修、ベンダーの事例）", "岡山市", {"情報サービス", "システム開発", "OA機器"}, (161, 161), True),
    ("サンホーム岡山（ベンダーの事例、数値なし）", "岡山市", {"不動産"}, (50, 99), True),
    ("イタミアート（上場、ベンダーの発表）", "岡山市", {"印刷", "販促物"}, None, True),
    ("安信工業（AI は設計の支援、数値は RPA）", "岡山市", {"金属製品", "金属加工"}, (13, 13), True),
    ("トスコ（県警との協定、数値なし）", "岡山市", {"情報サービス"}, None, True),
    ("白獅子（県の研究開発の採択）", "岡山市", {"情報サービス", "VR"}, None, True),
    ("ゴフェルテック（県の研究開発の採択）", "岡山市", {"情報サービス", "データ処理"}, None, True),
    ("岡山旭東病院（使用済み・香川県三木町）", "岡山市", {"医療", "病院"}, None, True),
    ("フジワラテクノアート（他県の cases_outside で使用済み）", "岡山市", {"生産用機械", "醸造機械"}, None, True),
    ("協電田中工業（AIではない）", "岡山市", {"金属製品", "機械部品", "農機具部品"}, (10, 10), False),
    ("elims（AIではない）", "岡山市", {"業種未確認"}, None, False),
    ("IME・頼鉄工所（AIではない、クラウド）", "岡山市", {"業種未確認"}, None, False),
    # 津山市
    ("日笠商事（ベンダーの事例、数値なし）", "津山市", {"OA機器", "事務機器の商社", "オフィス家具"}, (20, 49), True),
    ("マルイ（使用済み・青森市）", "津山市", {"小売", "食品スーパー"}, None, True),
    ("津山鶴山ホテル（使用済み・福島県猪苗代町）", "津山市", {"宿泊"}, None, True),
    ("アイテック・ツリタニ（AIではない）", "津山市", {"半導体検査機器の部品", "生産用機械"}, None, False),
    # 笠岡市
    ("エーアンドエス（使用済み・鳥取県北栄町）", "笠岡市", {"農業", "野菜"}, None, True),
    # 久米南町
    ("カッピーのりあい号（町の運行、使用済み・青森県鶴田町）", "久米南町", {"旅客運送", "乗合タクシー"}, None, True),
    # 倉敷市
    ("協同（県の研究開発の採択、所在は県資料の表記）", "倉敷市", {"学生服", "ワッペン", "刺しゅう"}, None, True),
    ("新来島サノヤス造船（AIではない）", "倉敷市", {"造船"}, None, False),
    # 備前市
    ("ビジュアルサーボ（県の研究開発の採択、業種未確認）", "備前市", {"業種未確認"}, None, True),
    # 赤磐市
    ("みのる産業（AIではない）", "赤磐市", {"農業機械"}, None, False),
    # 玉野市
    ("エイビス・うのベースAI部（コミュニティ、事例ではない）", "玉野市", {"業種未確認"}, None, False),
    # 県（所在を確かめていない・規模が大きい）
    ("岡山ダイハツ販売（島根の予備、使わない）", "所在未確認", {"自動車販売"}, (412, 412), True),
    ("ホテル鹿の湯（所在未確認、verified: false）", "所在未確認", {"宿泊"}, None, False),
    # cases_outside.md（県外。2026-11-03 の書き途中の版から D1 が追加。規模の分からない県外の事例は同じ市町村の NG にならない）
    ("のぞみ会居宅介護支援事業所（千葉県松戸市、県の事例集）", "県外", {"介護", "居宅介護支援"}, (6, 6), True),
    ("ノバ・メディクス（千葉県君津市、県の事例集）", "県外", {"介護", "居宅介護支援"}, (13, 13), True),
    ("Cotona（福岡県八女市、ベンダーの事例）", "県外", {"学生服", "受注事務", "OCR"}, None, True),
    ("竹中製作所（大阪府東大阪市、予備）", "県外", {"金属製品", "ボルト"}, (150, 150), True),
    ("広島県 ぶどうAI等級判定ステーション（参考、県の開発）", "県外", {"農業", "果実"}, None, False),
    ("たすけあい訪問介護センター（千葉県香取市、AIではない）", "県外", {"介護", "訪問介護"}, None, False),
    # cases2.md（2026-11-03 の補充。D2 が追加）
    # 倉敷市（中国精油の数値は水島工場〔倉敷市玉島乙島〕。本社は岡山市北区）
    ("中国精油（水島工場、AI画像解析＋IoTカメラ、県のチラシの45%）", "倉敷市", {"化学", "化学品", "蒸留精製", "潤滑油"}, (158, 158), True),
    ("中国精油（本社、生成AIの伴走支援に選定）", "岡山市", {"化学", "化学品", "蒸留精製", "潤滑油"}, (158, 158), True),
    ("旭金属工業（県の中堅企業の生成AI伴走支援に選定）", "倉敷市", {"金属製品", "配線用ボックス"}, None, True),
    ("中山鉄工所（県の中堅企業の生成AI伴走支援に選定）", "倉敷市", {"機械部品", "部品の復元", "鉄工"}, None, True),
    ("坂本織物（県の中堅企業の支援に選定、デジタルマーケティングだけ。AIではない）", "倉敷市", {"繊維", "織物", "真田紐"}, None, False),
    # 笠岡市
    ("正文社印刷所（県の中堅企業の生成AI伴走支援に選定、法人番号で未確認）", "笠岡市", {"印刷"}, None, True),
    ("丸善トレー（県の中堅企業の支援に選定、デジタルマーケティングだけ。AIではない）", "笠岡市", {"業種未確認"}, None, False),
    # 岡山市（市のデジタルマーケティング事例集。AI の効果の数値なし）
    ("協同プレス（市の事例集、AIビジュアル制作）", "岡山市", {"印刷", "Web制作", "雑貨"}, None, True),
    ("セイワ（市の事例集、生成AIのブログ）", "岡山市", {"清掃用品", "日用品の製造"}, None, True),
    ("エスプランニング（市の事例集、AIのブログ。所在が法人番号と不一致）", "岡山市", {"保険代理"}, None, True),
    ("宮下酒造（市の事例集、AI生成画像）", "岡山市", {"酒類製造", "食料品", "飲料"}, None, True),
    ("岡山市 IoT・AI補助の過去の採択（社名なし）", "岡山市", {"業種未確認"}, None, True),
    ("elims・ヨシハラ機工・ダイヤ工業（市の事例集、AIではない）", "岡山市", {"業種未確認"}, None, False),
    ("2024年の成果発表会の5社（社名と数値が結び付かない、AIか不明）", "岡山市", {"業種未確認"}, None, False),
    ("日進ゴム（事例報告会の対談、資料なし、AIではない）", "岡山市", {"ゴム製品"}, None, False),
    # 津山市・美作市・総社市
    ("院庄林業（AIではない、kintone・RPA）", "津山市", {"林業", "木材・木製品", "建築"}, None, False),
    ("英田エンジニアリング（令和7年度の支援先、verified: false）", "美作市", {"業種未確認"}, None, False),
    ("総社市 DAgree（市役所、企業の事例ではない）", "総社市", {"行政"}, None, False),
    # 県（所在を確かめていない。AIではない）
    ("県の介護モデル事業所3か所（AIではない、施設名なし）", "所在未確認", {"介護", "介護老人保健施設", "訪問介護", "グループホーム"}, None, False),
    ("県の人手不足対策補助・第1期の4社（AIではない）", "所在未確認", {"建設", "業種未確認"}, None, False),
    ("島根県 介護テクノロジー専門家派遣（県外、AIの数値なし）", "県外", {"介護", "通所介護"}, None, False),
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 2026-11-03: 既存の地域ページ（642本）と5県の PLAN（109行）で、月約21.7万円未満と、1人の業務量を◯.0・◯.5時間にした
# 小さい組（対象5〜10名）の値はほぼ埋まっている。空いている値を探して決めた（月53.75〜231時間・約23.2万〜81.8万円・12〜175名）。
# 業種・業態は stats.md の「市町村ごとの主要産業の候補」の (B) 中小企業の業種（経済センサスの事業所数・従業者数）から選んだ。
# 新庄村・久米南町だけ1人の業務量が◯.25・◯.75時間（ほかに空きがない。D1.md の判断が必要な点）
PLAN = [
    # 備前県民局（7）
    ("岡山市", "okayama-city", "卸売業・小売業", "飲食料品の卸売（市内に本社と物流センター）", {"卸売", "飲食料品卸"}, 175,
     "得意先（小売店・飲食店）からの受注・欠品・納期の問い合わせへの回答と、商品の規格書・提案書の下書き", 24, 38.5),
    ("玉野市", "tamano", "製造業", "輸送用機械（船舶のブロック・艤装品の製作。造船所の協力会社）", {"輸送用機械", "造船", "船舶部品"}, 60,
     "元請けからの図面・工程の問い合わせへの回答と、溶接・検査の記録と作業日報の取りまとめ", 13, 43),
    ("備前市", "bizen", "製造業", "窯業・土石製品（耐火物・セラミックスの製造）", {"窯業・土石", "耐火物"}, 85,
     "顧客からの仕様・納期の問い合わせへの回答と、ロットごとの試験成績書・製造記録の取りまとめ", 16, 39.5),
    ("瀬戸内市", "setouchi", "運輸業・郵便業", "道路貨物運送（地場の配送・中距離輸送）", {"運送", "道路貨物運送"}, 38,
     "配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報の集計", 12, 44.5),
    ("赤磐市", "akaiwa", "製造業", "生産用機械（食品機械・搬送装置の設計・組立）", {"生産用機械", "食品機械", "搬送装置"}, 50,
     "引合い・仕様の打合せ記録の要約と、見積書・取扱説明書の下書き", 14, 38.5),
    ("和気町", "wake", "医療・福祉", "介護老人保健施設（通所リハビリを併設）", {"介護", "介護老人保健施設"}, 40,
     "リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成", 14, 37.5),
    ("吉備中央町", "kibichuo", "製造業", "金属製品（金属部品の切削・溶接加工）", {"金属製品", "金属加工"}, 65,
     "取引先からの図面・見積の問い合わせへの回答と、材料の証明書・検査成績書の取りまとめ", 14, 42.5),
    # 備中県民局（10）
    ("倉敷市", "kurashiki", "製造業", "繊維（ジーンズ・カジュアル衣料の縫製・洗い加工）", {"繊維", "衣服の縫製", "ジーンズ"}, 120,
     "取引先（アパレル）からの仕様・納期の問い合わせへの回答と、縫製仕様書・検品記録の取りまとめ", 22, 38.5),
    ("笠岡市", "kasaoka", "製造業", "食料品（冷凍食品・惣菜の製造）", {"食料品", "冷凍食品", "惣菜"}, 90,
     "量販店・外食の取引先からの商品の問い合わせへの回答と、原材料の切り替えに伴う規格書の改訂、衛生管理の記録の取りまとめ", 17, 37),
    ("井原市", "ibara", "製造業", "プラスチック製品（自動車部品・日用品の射出成形）", {"プラスチック製品", "射出成形"}, 70,
     "取引先からの金型・納期の問い合わせへの回答と、成形条件表・不良の対策報告書の作成", 16, 38),
    ("総社市", "soja", "製造業", "輸送用機械（自動車部品のプレス・溶接）", {"輸送用機械", "自動車部品"}, 150,
     "取引先（自動車部品の一次取引先など）からの品質・変更の問い合わせへの回答と、変化点の管理表・品質記録の取りまとめ", 22, 37.5),
    ("高梁市", "takahashi", "医療・福祉", "特別養護老人ホーム（短期入所を併設）", {"介護", "特別養護老人ホーム"}, 55,
     "ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文の作成", 14, 34.5),
    ("新見市", "niimi", "建設業", "総合工事業（土木・舗装）", {"建設", "土木"}, 42,
     "公共工事の施工計画書・提出書類の作成と、工事写真・出来形の記録の整理", 12, 37),
    ("浅口市", "asakuchi", "製造業", "食料品（加工食品の製造）", {"食料品", "加工食品"}, 46,
     "取引先からの原材料・産地・賞味期限の問い合わせへの回答と、出荷・ロットの記録の取りまとめ", 14, 35.5),
    ("早島町", "hayashima", "運輸業・郵便業", "倉庫・物流センター（荷主の在庫管理と配送を受託）", {"倉庫", "運送", "物流センター"}, 140,
     "荷主からの入出庫・在庫の問い合わせへの回答と、作業実績・誤出荷の報告書の取りまとめ", 22, 38),
    ("里庄町", "satosho", "製造業", "生産用機械（自動機・省力化装置の設計・製作）", {"生産用機械", "自動機"}, 75,
     "顧客との仕様の打合せ記録の要約と、見積書・設計変更の連絡書の作成", 16, 37),
    ("矢掛町", "yakage", "製造業", "電気機械（電装品・制御部品の組立）", {"電気機械"}, 62,
     "取引先からの部品の切り替え・納期の問い合わせへの回答と、作業手順書・検査記録の取りまとめ", 14, 33.5),
    # 美作県民局（10）
    ("津山市", "tsuyama", "製造業", "はん用機械（ポンプ・送風機などの部品の加工・組立）", {"はん用機械", "機械部品"}, 80,
     "取引先からの仕様・納期の問い合わせへの回答と、作業指示書・組立記録の取りまとめ", 16, 36.5),
    ("真庭市", "maniwa", "製造業", "木材・木製品（製材・集成材の製造）", {"木材・木製品", "製材", "集成材"}, 95,
     "工務店・プレカット工場からの在庫・納期の問い合わせへの回答と、出荷伝票・品質の記録の取りまとめ", 18, 37.5),
    ("美作市", "mimasaka", "宿泊・飲食サービス業", "温泉旅館（宴会・日帰り入浴を含む）", {"宿泊", "旅館"}, 52,
     "予約サイト・メールの問い合わせへの返信の下書きと、宴会・団体の見積書、館内案内の多言語の文の作成", 15, 41),
    ("新庄村", "shinjo-village", "卸売業・小売業", "農産物・加工品の集出荷と販売", {"農産物の卸売", "直売"}, 18,
     "取引先・個人客からの注文・在庫の問い合わせへの回答と、出荷伝票・精算書の取りまとめ", 8, 34.75),
    ("鏡野町", "kagamino", "製造業", "食料品（農産物の加工品の製造）", {"食料品", "農産加工"}, 48,
     "通販・小売の取引先に出す商品説明・表示の文の作成と、受注・出荷の記録の取りまとめ", 12, 42.5),
    ("勝央町", "shoo", "製造業", "化学工業（工業用の薬品・樹脂原料の製造）", {"化学"}, 105,
     "顧客からの成分・安全データシート（SDS）の問い合わせへの回答と、試験成績書・製造記録の取りまとめ", 19, 38),
    ("奈義町", "nagi", "建設業", "総合工事業（建築・土木）", {"建設"}, 30,
     "工事日報・安全書類の取りまとめと、施主・発注者への工程の連絡文の作成", 11, 43),
    ("西粟倉村", "nishiawakura", "学術研究・専門技術サービス", "専門サービス（地域の事業の企画・デザイン・調査）", {"専門サービス", "デザイン", "コンサルティング"}, 12,
     "受託した事業の報告書・企画書の下書きと、打合せ記録の要約", 5, 43),
    ("久米南町", "kumenan", "医療・福祉", "通所介護・訪問介護", {"介護", "通所介護", "訪問介護"}, 26,
     "通所・訪問の記録の清書と、ケアマネジャー・家族への連絡文の作成", 8, 37.75),
    ("美咲町", "misaki", "製造業", "プラスチック製品（成形品の製造）", {"プラスチック製品", "成形"}, 44,
     "取引先からの受注・仕様の変更の連絡と、生産計画表・出荷書類の作成", 14, 41.5),
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def other_plans():
    """5県の _calc.py の PLAN を読み、(県, 市町村, 削減時間, 万円) を返す。ファイルがなければ None を入れる（NG）。"""
    out = []
    for pref, label in OTHER_PLANS:
        path = os.path.join(ROOT, "data", "area", pref, "_calc.py")
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


def main():
    n_files, n_sec, ex_h, ex_m, ex_s, per_file = existing()
    empty = [k for k, v in per_file.items() if v[1] == 0]
    if empty:
        print("NG 試算の金額を拾えなかった既存の記事:", empty)
    by_pref = Counter(re.sub(r"^2026-1\d-\d+-area-([a-z]+).*", r"\1", k) for k in per_file)
    print(f"既存の地域ページ: {n_files}本（うち試算の節があるもの {n_sec}本。山梨 {by_pref.get('yamanashi', 0)}本・"
          f"島根 {by_pref.get('shimane', 0)}本・鳥取 {by_pref.get('tottori', 0)}本・広島 {by_pref.get('hiroshima', 0)}本・"
          f"山口 {by_pref.get('yamaguchi', 0)}本を含む）。拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種・規模 {len(ex_s)}種")
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
    if os.path.exists(os.path.join(HERE, "cases_outside.md")):
        print("（注意）cases_outside.md がある。県外の会社（業態・従業員数）を CASES に足したか確かめる")

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
                print(f"  NG 岡山県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 岡山県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
            ok = False
        seen_s[size] = city
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは岡山県の中だけを NG にする）")
    print(f"（参考）時間が◯.25・◯.75になるページ: {n_quarter}件")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 27 else "NG")


if __name__ == "__main__":
    main()
