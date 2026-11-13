#!/usr/bin/env python3
"""北海道の市町村の試算の割り当てを計算し、重なりを確かめる（2026-11-05）。

data/area/gunma/_calc.py（kagoshima の形）を元に作った。道のページ（/area/hokkaido/）には試算を入れない。
179市町村を振興局ごとに段階で作るので、SLUGS と PLAN は段階ごとに足す（PLAN の行数 = SLUGS の数）。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **北海道・北関東3県・沖縄の取り決め**: 月の削減時間（0.25時間刻み）×4 を5で割った余りが 0（北海道）の時間だけを使う
     （1.25, 2.5, 3.75, 5.0, … の1.25時間刻み。data/area/_batch5/shared.md）
  1. 北海道のページの中で、月の削減時間・月の時間換算額（万円、小数1桁）が重ならない。従業員数は同じ業種の中で重ならない（2026-11-13 から）
  2・3. **2026-11-11 ユーザー決定（C）: 既存の他県の地域ページの試算、他県の _calc.py の PLAN と時間・金額が重なってもよい**
     （段階1の石狩8市町村は重ならないように作ったが、残り171市町村は空きが足りないため）。重なりは「（参考）」として表示するだけで NG にしない。
     北海道のページの中では、時間・金額・規模を重ねない（1 のとおり）
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md の事例の会社と同じにならない（CASES と照合）
  6. slug が SLUGS と一致する
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
使い方: python3 data/area/hokkaido/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/hokkaido/_calc.py free <業種> <最小時間> <最大時間>   （空いている時間と金額を並べる）
他県の PLAN は後から変わることがあるので、push の直前に git pull してもう一度実行する。
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
SELF = "hokkaido"
KYUSHU_MOD = 0  # 5県の割り当て（月の削減時間×4 を5で割った余り）。北海道は 0
DIV = 5

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
    # 段階1: 石狩振興局（8）。段階が進むごとに足す（PLAN の行数は len(SLUGS) と同じ）
    "sapporo", "ebetsu", "chitose", "eniwa", "kitahiroshima-city", "ishikari", "tobetsu", "shinshinotsu",
    # 段階2: 胆振総合振興局（11）
    "muroran", "tomakomai", "noboribetsu", "date-city", "toyoura", "sobetsu", "shiraoi", "atsuma", "toyako", "abira", "mukawa",
    # 段階3: 渡島総合振興局（11）
    "hakodate", "hokuto-city", "matsumae", "fukushima-town", "shiriuchi", "kikonai", "nanae", "shikabe", "mori", "yakumo", "oshamanbe",
    # 段階4: 上川総合振興局（23）
    "asahikawa", "shibetsu-city", "nayoro", "furano", "takasu", "higashikagura", "toma", "pippu", "aibetsu", "kamikawa", "higashikawa", "biei", "kamifurano", "nakafurano", "minamifurano", "shimukappu", "wassamu", "kenbuchi", "shimokawa", "bifuka", "otoineppu", "nakagawa-town-hokkaido", "horokanai",
    # 段階5: 十勝総合振興局（19）
    "obihiro", "otofuke", "shihoro", "kamishihoro", "shikaoi", "shintoku", "shimizu", "memuro", "nakasatsunai", "sarabetsu", "taiki-town-hokkaido", "hiroo", "makubetsu", "ikeda-town-hokkaido", "toyokoro", "honbetsu", "ashoro", "rikubetsu", "urahoro",
    # 段階6: 空知総合振興局（24）
    "yubari", "iwamizawa", "bibai", "ashibetsu", "akabira", "mikasa", "takikawa", "sunagawa", "utashinai", "fukagawa", "nanporo", "naie", "kamisunagawa", "yuni", "naganuma", "kuriyama", "tsukigata", "urausu", "shintotsukawa", "moseushi", "chippubetsu", "uryu", "hokuryu", "numata-town-hokkaido",
}

# 九州以外で照合が必須の県（2026-11-04 にある _calc.py）。ファイルがなければ NG
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "kagoshima", "kumamoto", "miyazaki", "nagasaki", "oita", "saga")

# cases.md・cases_outside.md・subsidy_a_areas.md（採択・交付決定の手がかり）の事例の会社（2026-11-04）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・交付決定・使用済み・目標を含む〕)
# cases2.md（2026-11-04 の補充調査）の会社も足した（「# cases2.md」の行）。cases2.md が更新されたら足して再実行する
CASES = [
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種・業態は stats.md の「市町村ごとの主要産業の候補」の (B) 中小企業の業種（経済センサスの事業所数・従業者数）から選んだ。
# 霧島市の電子部品（16所・7,169人）、薩摩川内市の窯業・土石（21所・4,728人）、志布志市の飲料・たばこ・飼料（出荷額の70.2%）、
# 伊佐市・いちき串木野市の非鉄金属（1所）、南種子町の技術サービス業・輸送用機械（1所）、湧水町の電子部品（3所）など、
# 大企業の工場・特定の施設と読める中分類は試算の業種にしない。農業・漁業・林業も試算の業種にしない
# （畜産・茶・さとうきびの町村は食料品製造〔食肉・鶏卵・製茶・でん粉・農産加工〕・卸売〔集出荷〕などにした）。
# 2026-11-04: 既存の地域ページ（試算の節がある約690本）と13県の PLAN で埋まっていない値を探して決めた。
PLAN = [
    # 段階1: 石狩振興局（2026-11-06）。業種は stats.md の「市町村ごとの主要産業の候補」の中小企業の業種から選んだ。
    # 千歳市の電子部品（Rapidus など大企業の工場と読める）・石狩市のデータセンターは試算の業種にしない
    ("札幌市", "sapporo", "卸売業・小売業", "食品・日用品の卸売", {"卸売", "食品卸"}, 250,
     "受発注の入力・見積書と納品書の作成・得意先からの問い合わせへの回答", 55, 22),
    ("江別市", "ebetsu", "医療・福祉", "介護施設（特別養護老人ホームなど）", {"介護", "福祉"}, 140,
     "介護記録の清書・ケアプランの下書き・家族への連絡文の作成", 85, 11),
    ("千歳市", "chitose", "卸売業・小売業", "小売（食品・日用品の店舗）", {"小売", "スーパー"}, 110,
     "発注の数量の見込み・売場のPOPと案内文の作成・シフト表の作成", 45, 22),
    ("恵庭市", "eniwa", "製造業", "食料品製造", {"食料品", "食品製造"}, 130,
     "製造記録・衛生管理の帳票の作成・取引先からの規格書の問い合わせへの回答", 45, 19),
    ("北広島市", "kitahiroshima-city", "運輸業・郵便業", "道路貨物運送（トラック運送）", {"運送", "道路貨物運送", "物流"}, 85,
     "配車表の作成・運転日報と点呼記録の整理・荷主への到着の連絡", 39, 20),
    ("石狩市", "ishikari", "製造業", "金属製品製造", {"金属製品", "金属加工"}, 70,
     "見積書の作成・図面からの部品表づくり・検査成績書の作成", 25, 25),
    ("当別町", "tobetsu", "製造業", "食料品製造（農産物の加工）", {"食料品", "食品製造", "農産加工"}, 48,
     "製造記録の清書・原材料の受け入れ記録の整理・商品の表示ラベルの文案", 20, 25.75),
    ("新篠津村", "shinshinotsu", "建設業", "土木工事（農業土木・道路）", {"建設", "土木"}, 40,
     "工事写真の整理・施工計画書と日報の作成・発注者への提出書類の作成", 20, 26.75),
    # 段階2: 胆振総合振興局（2026-11-11）。他県との重なりは許容（ユーザー決定 C）。小さい町は統計の規模に合う小さい会社にした。
    # 室蘭市の鉄鋼業（日本製鉄の室蘭地区）、苫小牧市の石油製品・輸送用機械（製油所・自動車部品の工場）、厚真町の電気業（発電所）は試算の業種にしない
    ("室蘭市", "muroran", "学術研究・専門技術サービス", "技術サービス（設計・検査・技術者派遣）", {"技術サービス", "設計"}, 60,
     "設計図書・検査報告書の作成・技術資料の検索・顧客への報告書の要約", 20, 28),
    ("苫小牧市", "tomakomai", "運輸業・郵便業", "倉庫・港湾の荷役と配送", {"倉庫", "物流", "運送"}, 120,
     "入出庫の伝票と在庫表の整理・作業指示書の作成・荷主への入出庫の報告", 40, 20),
    ("登別市", "noboribetsu", "宿泊・飲食サービス業", "温泉ホテル", {"宿泊", "ホテル", "旅館"}, 135,
     "予約の問い合わせへの返信・外国語の案内文・口コミへの返信文の作成", 45, 16),
    ("伊達市", "date-city", "医療・福祉", "介護事業所（通所・訪問）", {"介護", "福祉"}, 90,
     "介護記録の清書・サービス提供の報告書・家族への連絡帳の文案", 50, 13),
    ("豊浦町", "toyoura", "医療・福祉", "介護事業所（町内の小規模な事業所の例）", {"介護", "福祉"}, 20,
     "介護記録の清書・請求の前の記録の確認・連絡文の作成", 10, 20),
    ("壮瞥町", "sobetsu", "宿泊・飲食サービス業", "温泉旅館（小規模）", {"宿泊", "旅館"}, 30,
     "予約の問い合わせへの返信・外国語の館内案内・献立表と食材の発注表の作成", 10, 25),
    ("白老町", "shiraoi", "製造業", "食料品製造（水産・畜産の加工）", {"食料品", "食品製造", "水産加工"}, 65,
     "製造記録と衛生管理の帳票・原材料の産地と規格の書類・取引先からの問い合わせへの回答", 20, 24),
    ("厚真町", "atsuma", "建設業", "土木・建築工事", {"建設", "土木"}, 32,
     "工事写真の整理・施工の書類と日報の作成・発注者への提出書類", 12, 25),
    ("洞爺湖町", "toyako", "宿泊・飲食サービス業", "温泉ホテル（湖畔）", {"宿泊", "ホテル"}, 80,
     "予約サイトと電話の問い合わせへの返信・多言語の案内文・宴会と団体の見積書", 30, 18),
    ("安平町", "abira", "製造業", "食料品製造", {"食料品", "食品製造"}, 50,
     "製造記録と出荷の書類・表示ラベルの文案・品質の問い合わせへの回答", 18, 20),
    ("むかわ町", "mukawa", "卸売業・小売業", "農産物の集出荷・卸（野菜）", {"卸売", "集出荷", "青果"}, 25,
     "出荷の数量と規格の集計・出荷伝票の作成・取引先への出荷の連絡", 10, 22),
    # 段階3: 渡島総合振興局（2026-11-11）。函館市の輸送用機械（造船）、知内町の電気業（発電所）、七飯町の電子部品（1所）は試算の業種にしない
    ("函館市", "hakodate", "宿泊・飲食サービス業", "市内のホテル（観光・ビジネス）", {"宿泊", "ホテル"}, 160,
     "予約サイトと電話の問い合わせへの返信・多言語の案内文・朝食と宴会の発注の表", 50, 17),
    ("北斗市", "hokuto-city", "運輸業・郵便業", "道路貨物運送（トラック運送）", {"運送", "道路貨物運送", "物流"}, 75,
     "配車表の作成・運転日報の整理・荷主への到着と遅れの連絡", 30, 22),
    ("松前町", "matsumae", "製造業", "水産加工（小規模）", {"水産加工", "食料品"}, 35,
     "製造記録・衛生管理の帳票・取引先への規格書と出荷の連絡", 15, 21),
    ("福島町", "fukushima-town", "建設業", "土木工事", {"建設", "土木"}, 28,
     "工事写真の整理・施工の書類と日報・発注者への提出書類", 10, 29),
    ("知内町", "shiriuchi", "製造業", "食料品製造（水産・農産の加工）", {"食料品", "食品製造"}, 42,
     "製造記録と原材料の受け入れ記録・表示ラベルの文案・取引先からの問い合わせへの回答", 15, 22),
    ("木古内町", "kikonai", "卸売業・小売業", "小売（食品・日用品の店舗）", {"小売"}, 22,
     "発注の数量の見込み・売場の案内文とPOP・シフト表", 8, 32.5),
    ("七飯町", "nanae", "医療・福祉", "介護施設（入所・通所）", {"介護", "福祉"}, 78,
     "介護記録の清書・ケアプランの下書き・家族への連絡文", 30, 15),
    ("鹿部町", "shikabe", "製造業", "水産加工（たらこ・ほたてなど）", {"水産加工", "食料品"}, 45,
     "製造記録と衛生管理の帳票・原料の産地の書類・取引先からの品質の問い合わせへの回答", 20, 22),
    ("森町", "mori", "製造業", "水産加工（中規模）", {"水産加工", "食料品"}, 100,
     "製造と出荷の記録・取引先ごとの規格書・品質の問い合わせへの回答", 35, 21),
    ("八雲町", "yakumo", "製造業", "食料品製造（乳製品・畜産の加工）", {"食料品", "乳製品"}, 55,
     "製造記録と検査の記録・出荷の書類・取引先への規格の回答", 22, 25),
    ("長万部町", "oshamanbe", "卸売業・小売業", "水産物の卸（ほたてなど）", {"卸売", "水産物卸"}, 38,
     "出荷の数量の集計・出荷伝票と請求書の作成・取引先への連絡", 14, 25),
    # 段階4: 上川総合振興局（2026-11-11）。旭川市のパルプ・紙、比布町の研究機関、東神楽町の航空運輸、上富良野町の駐屯地は試算の業種にしない。
    # 時間と金額は北海道の中で空いている値を当社のスクリプトで割り当てた（他県との重なりは許容）
    ("旭川市", "asahikawa", "医療・福祉", "介護施設（入所・通所）", {"介護", "福祉"}, 180,
     "介護記録の清書・ケアプランの下書き・家族への連絡文", 70, 14),
    ("士別市", "shibetsu-city", "建設業", "土木・建築工事", {"土木", "建設"}, 62,
     "工事写真の整理・施工の書類と日報・発注者への提出書類", 22, 32.5),
    ("名寄市", "nayoro", "卸売業・小売業", "小売（食品・日用品の店舗）", {"小売"}, 95,
     "発注の数量の見込み・売場の案内文とPOP・シフト表", 35, 25),
    ("富良野市", "furano", "宿泊・飲食サービス業", "ホテル（観光）", {"宿泊", "ホテル"}, 115,
     "予約の問い合わせへの返信・外国語の案内文・口コミへの返信", 38, 17.5),
    ("鷹栖町", "takasu", "医療・福祉", "介護施設", {"介護", "福祉"}, 58,
     "介護記録の清書・請求の前の記録の確認・家族への連絡文", 25, 16),
    ("東神楽町", "higashikagura", "卸売業・小売業", "小売（食品・日用品の店舗）", {"小売"}, 34,
     "発注の数量の見込み・売場の案内文・シフト表", 12, 22.5),
    ("当麻町", "toma", "製造業", "木材・木製品の加工", {"木製品", "木材"}, 26,
     "見積書と注文書の作成・製材の記録・取引先への出荷の連絡", 10, 24),
    ("比布町", "pippu", "建設業", "土木工事", {"土木", "建設"}, 24,
     "工事写真の整理・施工の書類・発注者への提出書類", 9, 25),
    ("愛別町", "aibetsu", "製造業", "木材・木製品の加工", {"木製品", "木材"}, 21,
     "見積書の作成・製材と出荷の記録", 8, 23.75),
    ("上川町", "kamikawa", "宿泊・飲食サービス業", "温泉ホテル（層雲峡など）", {"宿泊", "ホテル"}, 71,
     "予約の問い合わせへの返信・外国語の案内文・団体の見積書", 26, 20),
    ("東川町", "higashikawa", "製造業", "家具・木工", {"家具", "木工"}, 49,
     "見積書と図面からの部材表づくり・受注の記録・顧客への納期の連絡", 18, 22.5),
    ("美瑛町", "biei", "宿泊・飲食サービス業", "ペンション・ホテル（観光）", {"宿泊"}, 43,
     "予約の問い合わせへの返信・外国語の案内文・口コミへの返信", 15, 25),
    ("上富良野町", "kamifurano", "卸売業・小売業", "小売（食品・日用品の店舗）", {"小売"}, 39,
     "発注の数量の見込み・売場の案内文・シフト表", 14, 20),
    ("中富良野町", "nakafurano", "卸売業・小売業", "農産物の集出荷・卸（野菜）", {"卸売", "青果", "集出荷"}, 31,
     "出荷の数量と規格の集計・出荷伝票・取引先への連絡", 11, 25),
    ("南富良野町", "minamifurano", "医療・福祉", "介護施設（町内の小規模な事業所の例）", {"介護", "福祉"}, 23,
     "介護記録の清書・連絡文の作成", 9, 20),
    ("占冠村", "shimukappu", "宿泊・飲食サービス業", "リゾートホテル", {"宿泊", "ホテル"}, 150,
     "予約の問い合わせへの返信・多言語の案内文・宴会と団体の見積書", 50, 15.5),
    ("和寒町", "wassamu", "建設業", "土木・建築工事", {"土木", "建設"}, 27,
     "工事写真の整理・施工の書類と日報", 10, 26.5),
    ("剣淵町", "kenbuchi", "医療・福祉", "介護事業所", {"介護", "福祉"}, 29,
     "介護記録の清書・サービスの報告書", 11, 15),
    ("下川町", "shimokawa", "製造業", "木材・木製品の加工", {"木製品", "木材"}, 44,
     "注文と見積の書類・製材と出荷の記録・取引先への連絡", 16, 20),
    ("美深町", "bifuka", "卸売業・小売業", "小売（食品・日用品の店舗）", {"小売"}, 18,
     "発注の数量の見込み・売場の案内文", 7, 25),
    ("音威子府村", "otoineppu", "建設業", "土木工事（村内の小規模な事業所の例）", {"土木", "建設"}, 15,
     "工事写真の整理・提出書類の作成", 6, 25),
    ("中川町", "nakagawa-town-hokkaido", "建設業", "土木工事", {"土木", "建設"}, 19,
     "工事写真の整理・施工の書類・提出書類", 7, 30),
    ("幌加内町", "horokanai", "製造業", "食料品製造（そばなど農産の加工）", {"食料品", "食品製造"}, 16,
     "製造記録・表示ラベルの文案・取引先への連絡", 6, 22.5),
    # 段階5: 十勝総合振興局（2026-11-12）。帯広市・幕別町の電子部品、士幌町の大きな製造事業所、大樹町の宇宙関連、研究機関、農業・農協は試算の業種にしない。
    # 萩原建設工業（帯広市、建設189名）と重ならないよう帯広市は卸売にした。時間と金額は北海道の中で空いている値を当社のスクリプトで割り当てた
    ("帯広市", "obihiro", "卸売業・小売業", "卸売（食品・農産物）", {"卸売", "食品卸"}, 151,
     "受注と出荷の伝票の整理・取引先ごとの見積書と請求書・商品の規格の問い合わせへの回答", 56, 16.25),
    ("音更町", "otofuke", "製造業", "食料品製造（農産物の加工）", {"食料品", "食品製造"}, 111,
     "製造記録と原材料の受け入れ記録・表示ラベルの文案・取引先への規格書", 40, 17.75),
    ("士幌町", "shihoro", "製造業", "食料品製造（畜産物の加工）", {"食料品", "食品製造", "畜産加工"}, 63,
     "製造と衛生管理の記録・出荷の書類・取引先からの品質の問い合わせへの回答", 25, 17),
    ("上士幌町", "kamishihoro", "建設業", "土木工事", {"土木", "建設"}, 33,
     "工事写真の整理・施工の書類と日報・発注者への提出書類", 10, 21.5),
    ("新得町", "shintoku", "宿泊・飲食サービス業", "ホテル（温泉・観光）", {"宿泊", "ホテル"}, 46,
     "予約の問い合わせへの返信・外国語の案内文・団体の見積書", 16, 21.25),
    ("清水町", "shimizu", "製造業", "食料品製造（乳製品）", {"食料品", "乳製品"}, 72,
     "製造記録と検査の記録・出荷の書類・取引先への規格の回答", 25, 19),
    ("芽室町", "memuro", "運輸業・郵便業", "道路貨物運送（トラック運送）", {"運送", "物流"}, 86,
     "配車表の作成・運転日報の整理・荷主への到着と遅れの連絡", 36, 18.75),
    ("中札内村", "nakasatsunai", "製造業", "食料品製造（食肉・畜産の加工）", {"食料品", "畜産加工"}, 82,
     "製造記録と衛生管理の帳票・表示ラベルの文案・取引先への出荷の連絡", 30, 19),
    ("更別村", "sarabetsu", "建設業", "土木・建築工事", {"土木", "建設"}, 36,
     "工事写真の整理・施工の書類・発注者への提出書類と見積書", 12, 23.75),
    ("大樹町", "taiki-town-hokkaido", "卸売業・小売業", "小売（食品・日用品の店舗）", {"小売"}, 37,
     "発注の数量の見込み・売場の案内文とPOP・シフト表", 10, 24.5),
    ("広尾町", "hiroo", "製造業", "水産加工", {"水産加工", "食料品"}, 47,
     "製造と出荷の記録・衛生管理の帳票・取引先からの問い合わせへの回答", 20, 19.75),
    ("幕別町", "makubetsu", "医療・福祉", "介護施設（入所・通所）", {"介護", "福祉"}, 76,
     "介護記録の清書・ケアプランの下書き・家族への連絡文", 30, 18.5),
    ("池田町", "ikeda-town-hokkaido", "医療・福祉", "介護施設", {"介護", "福祉"}, 52,
     "介護記録の清書・請求の前の記録の確認・連絡文の作成", 20, 19),
    ("豊頃町", "toyokoro", "建設業", "土木工事（町内の小規模な事業所の例）", {"土木", "建設"}, 17,
     "工事写真の整理・提出書類の作成", 8, 20),
    ("本別町", "honbetsu", "運輸業・郵便業", "道路貨物運送（トラック運送）", {"運送", "物流"}, 41,
     "配車表の作成・運転日報の整理・荷主への連絡", 13, 25),
    ("陸別町", "rikubetsu", "医療・福祉", "介護事業所（町内の小規模な事業所の例）", {"介護", "福祉"}, 14,
     "介護記録の清書・サービスの報告書", 7, 20),
    ("鹿追町", "shikaoi", "卸売業・小売業", "小売（食品・日用品の店舗）", {"小売"}, 53,
     "発注の数量の見込み・売場の案内文・シフト表", 20, 15.5),
    ("足寄町", "ashoro", "製造業", "木材・木製品の加工", {"木製品", "木材"}, 12,
     "見積書と注文書の作成・製材と出荷の記録", 5, 24),
    ("浦幌町", "urahoro", "製造業", "食料品製造（水産・農産の加工）", {"食料品", "水産加工"}, 54,
     "製造記録・表示ラベルの文案・取引先への連絡", 20, 17.75),
    # 段階6: 空知総合振興局（2026-11-13）。芦別市のはん用機械・砂川市の化学の大きな事業所、研究機関、農業・農協は試算の業種にしない。従業員数は同じ業種の中で重ならなければよい
    ("岩見沢市", "iwamizawa", "医療・福祉", "介護施設（入所・通所）", {"介護", "福祉"}, 141,
     "介護記録の清書・ケアプランの下書き・家族への連絡文", 53, 15),
    ("滝川市", "takikawa", "卸売業・小売業", "小売（食品・日用品の店舗）", {"小売"}, 96,
     "発注の数量の見込み・売場の案内文とPOP・シフト表", 31, 20),
    ("深川市", "fukagawa", "製造業", "食料品製造（米・農産物の加工）", {"食料品", "食品製造"}, 71,
     "製造記録と原料の受け入れ記録・表示ラベルの文案・取引先への規格書", 28, 17.5),
    ("夕張市", "yubari", "医療・福祉", "介護施設", {"介護", "福祉"}, 60,
     "介護記録の清書・請求の前の記録の確認・家族への連絡文", 20, 18.25),
    ("美唄市", "bibai", "製造業", "プラスチック製品の製造", {"プラスチック"}, 75,
     "見積書と図面からの部材表づくり・生産の日報・取引先への納期の連絡", 28, 18.75),
    ("芦別市", "ashibetsu", "製造業", "機械部品の加工（はん用機械の協力会社）", {"機械", "金属加工"}, 56,
     "見積書の作成・加工の記録と検査の成績書・取引先への納期の連絡", 20, 19.5),
    ("赤平市", "akabira", "製造業", "革製品（かばん）の製造", {"革製品", "皮革"}, 51,
     "受注の記録・製造の指示書・通販の問い合わせへの返信と商品説明文", 20, 16.75),
    ("三笠市", "mikasa", "卸売業・小売業", "小売（食品・日用品の店舗）", {"小売"}, 58,
     "発注の数量の見込み・売場の案内文・シフト表", 20, 20.5),
    ("砂川市", "sunagawa", "建設業", "土木・建築工事", {"土木", "建設"}, 66,
     "工事写真の整理・施工の書類と日報・発注者への提出書類", 23, 20),
    ("歌志内市", "utashinai", "医療・福祉", "介護事業所（市内の小規模な事業所の例）", {"介護", "福祉"}, 13,
     "介護記録の清書・サービスの報告書", 5, 25),
    ("南幌町", "nanporo", "製造業", "繊維製品の製造", {"繊維"}, 57,
     "受注と生産の記録・取引先への納期の連絡・製品の仕様書", 20, 19.25),
    ("奈井江町", "naie", "製造業", "金属製品の製造", {"金属製品", "金属加工"}, 120,
     "見積書と図面からの部材表づくり・検査の成績書・取引先への納期の連絡", 40, 18.25),
    ("上砂川町", "kamisunagawa", "製造業", "窯業・土石製品の製造", {"窯業", "土石"}, 30,
     "生産の日報・出荷の書類・取引先への規格の回答", 10, 23),
    ("由仁町", "yuni", "製造業", "食料品製造（農産物の加工）", {"食料品", "食品製造"}, 46,
     "製造記録・表示ラベルの文案・取引先への出荷の連絡", 15, 17),
    ("長沼町", "naganuma", "卸売業・小売業", "農産物の集出荷・卸（野菜）", {"卸売", "青果", "集出荷"}, 50,
     "出荷の数量と規格の集計・出荷伝票・取引先への連絡", 20, 17.25),
    ("栗山町", "kuriyama", "建設業", "土木・建築工事", {"土木", "建設"}, 41,
     "工事写真の整理・施工の書類・発注者への提出書類と見積書", 15, 29),
    ("月形町", "tsukigata", "医療・福祉", "介護施設（入所）", {"介護", "福祉"}, 64,
     "介護記録の清書・ケアプランの下書き・連絡文の作成", 24, 17.5),
    ("浦臼町", "urausu", "卸売業・小売業", "農産物の集出荷（米・果実）", {"卸売", "集出荷"}, 12,
     "出荷の数量の集計・出荷伝票", 5, 23),
    ("新十津川町", "shintotsukawa", "医療・福祉", "介護施設", {"介護", "福祉"}, 57,
     "介護記録の清書・請求の前の記録の確認・連絡文の作成", 20, 18.5),
    ("妹背牛町", "moseushi", "製造業", "鉄鋼・金属の加工", {"鉄鋼", "金属加工"}, 31,
     "見積書の作成・加工の記録・取引先への出荷の連絡", 10, 20.5),
    ("秩父別町", "chippubetsu", "宿泊・飲食サービス業", "温泉・宿泊施設", {"宿泊"}, 20,
     "予約の問い合わせへの返信・案内文・団体の見積書", 10, 15.5),
    ("雨竜町", "uryu", "運輸業・郵便業", "道路貨物運送（農産物の運送）", {"運送", "物流"}, 18,
     "配車表の作成・運転日報の整理・荷主への連絡", 8, 21.25),
    ("北竜町", "hokuryu", "建設業", "土木工事", {"土木", "建設"}, 25,
     "工事写真の整理・提出書類の作成", 10, 18.5),
    ("沼田町", "numata-town-hokkaido", "建設業", "土木・建築工事（町内の中小の事業所の例）", {"土木", "建設"}, 29,
     "工事写真の整理・施工の書類と日報・提出書類", 10, 23.5),
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
    九州以外の必須の県のファイルがなければ None を入れる（NG）。読めないファイルは警告だけ（NG にしない）。"""
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
        res = int(q) % DIV if q % 1 == 0 else None
        print(f"| {city} | {ind}（{sub}） | {size}名 | {n}名×{hrs}時間×25% | {h.normalize():f}時間 | 約{RATE[ind]:,}円 | 約{m}万円 | 約{y}万円 | {res} |")
        if q % 1 != 0:
            print(f"  NG {city} の時間が0.25時間刻みでない ({h})")
            ok = False
        elif res != KYUSHU_MOD:
            print(f"  NG {city} の時間 {h} は5県の割り当て（×4 を5で割った余り {KYUSHU_MOD}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 北海道の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            # 2026-11-11 ユーザー決定（C）: 他県の記事・PLAN と時間・金額が重なってもよい。北海道の中だけ重ならないようにする
            if key in exd:
                notes.append(f"{city}: 既存の他県の記事と{label}が同じ {exd[key]} ({key})（重なりは許容）")
            if key in pld:
                notes.append(f"{city}: 他県の PLAN と{label}が同じ {pld[key]} ({key})（重なりは許容）")
        # 2026-11-13: 20〜50名がほぼ埋まったので、従業員数は「同じ業種の中で」重ならなければよいことにした（時間・金額は北海道の中で重ねない）
        if (ind, size) in seen_s:
            print(f"  NG 北海道の中で同じ業種の規模が重なる: {city} と {seen_s[(ind, size)]} ({ind} {size}名)")
            ok = False
        seen_s[(ind, size)] = city
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは北海道の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == len(SLUGS) else "NG")


def free(ind, lo, hi):
    """業種 ind で、lo〜hi 時間の空いている（時間, 万円）を並べる"""
    h_used, m_used = used_values()
    mine_h = {Decimal(str(p[7])) * Decimal(str(p[8])) * Decimal("0.25") for p in PLAN}
    mine_m = {man(Decimal(str(p[7])) * Decimal(str(p[8])) * Decimal("0.25") * RATE[p[2]]) for p in PLAN}
    h = Decimal(str(lo))
    out = []
    while h <= Decimal(str(hi)):
        if int(h * 4) % DIV == KYUSHU_MOD and h not in h_used and h not in mine_h:
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
