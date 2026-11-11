#!/usr/bin/env python3
"""静岡県35市町の試算の割り当てを計算し、重なりを確かめる（2026-11-11）。

data/area/nara/_calc.py を元に作った。県ページ（/area/shizuoka/）には試算を入れないので、PLAN は35行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **静岡・愛知・三重・京都の取り決め**: 月の削減時間（0.25時間刻み）×4 を4で割った余りが 0（静岡県）の時間だけを使う
     （＝ちょうどの時間。1時間刻み。data/area/_tokai/shared.md）
  1. 35ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、静岡県を除く）の「## 試算」の節に出てくる
     「◯時間」「◯万円」の値と重ならない（広めに拾う）
  3. 全県の data/area/*/_calc.py の PLAN（静岡県を除く。glob で全部読む。愛知・三重・京都・兵庫・北海道を含む）の
     月の削減時間・月の時間換算額と重ならない。**読めないファイルは NG にせず警告**。
     REQUIRED の県はファイルがなければ NG。**金額が重なったら先に PLAN を push した府県を優先する**
     （北海道は他県との重なりを許容する取り決めだが、静岡からは北海道の PLAN とも重ねない）
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md・cases2.md（あれば）の事例の会社と同じにならない（CASES と照合）
  6. slug が _brief.md の35市町と一致する（静岡市 shizuoka-city、小山町 oyama-town、森町 mori-town-shizuoka、清水町 shimizu-town-shizuoka）
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
  8. 県ページには試算を入れない（PLAN は35行）
  9. 仮の会社の従業員数が、その市町の民営従業者数・選んだ中分類の従業者数（stats.md、経済センサス2021）を超えない（STAT と照合）
使い方: python3 data/area/shizuoka/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/shizuoka/_calc.py free 製造業 30 200   （余り0の時間で、既存・他県・静岡の中と重ならない時間と金額の候補を出す）
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
SELF = "shizuoka"
PREF_JA = "静岡県"
MOD_N, MOD_R = 4, 0  # 静岡・愛知・三重・京都の割り当て（月の削減時間×4 を4で割った余り）。静岡県は 0
N_PAGES = 35

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
    # 政令市（2）・市（21）
    "shizuoka-city", "hamamatsu", "numazu", "atami", "mishima", "fujinomiya", "ito", "shimada", "fuji", "iwata",
    "yaizu", "kakegawa", "fujieda", "gotemba", "fukuroi", "shimoda", "susono", "kosai", "izu", "omaezaki",
    "kikugawa", "izunokuni", "makinohara",
    # 町（12）
    "higashiizu", "kawazu", "minamiizu", "matsuzaki", "nishiizu", "kannami", "shimizu-town-shizuoka", "nagaizumi",
    "oyama-town", "yoshida", "kawanehon", "mori-town-shizuoka",
}
VILLAGES = set()  # 静岡県に村はない

# 照合が必須の県（2026-11-07 に _calc.py がある県。近畿の和歌山・滋賀を含む）。ファイルがなければ NG。ほかに見つかった _calc.py も全部読む
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima",
            "hokkaido", "ibaraki", "tochigi", "gunma", "okinawa", "wakayama", "shiga", "nara")

# cases.md・cases_outside.md・subsidy_a_areas.md・companies.md（大企業の工場・AI を作る側）の会社（2026-11-07）
# (会社名, 市町村〔県外は「県外」〕, 業態のキー, 従業員数〔(下限, 上限)。分からなければ None〕, AI の事例か〔実証・使用済み・提供側を含む〕)
# cases2.md ができたら D2 が「# cases2.md」の行に足す
CASES = [
    # cases.md（2026-11-11）
    ("スズキ部品製造（県の生成AI実証、駆動系・足回り部品、994名）", "浜松市", {"輸送用機械", "自動車部品"}, (994, 994), True),
    ("ヤマハモーターエンジニアリング（県の生成AI実証、CAE 受託、464名）", "磐田市", {"設計受託", "CAE", "技術サービス"}, (464, 464), True),
    ("Sスズキ技研工業（AI でアプリ、射出成形金型、10名）", "静岡市", {"金型", "プラスチック製品"}, (10, 10), True),
    ("岩本工業（ChatGPT で VBA、着色ペレット）", "静岡市", {"化学", "着色ペレット"}, None, True),
    ("渡辺プレス工業（ChatGPT でマクロ、プレス、25名）", "静岡市", {"金属製品", "プレス"}, (25, 25), True),
    ("セイリン（ChatGPT、鍼の製造、参考）", "静岡市", {"医療機器"}, None, True),
    ("愛工業（AI Quest・共同研究、プラスチック成形、約200名）", "静岡市", {"プラスチック製品", "射出成形"}, (200, 200), True),
    ("三和新静（AI-OCR のトライアル、卸売）", "静岡市", {"業種未確認"}, None, True),
    ("エフワイケー（HAI の伴走で生成AI、試験装置・省力化設備）", "磐田市", {"生産用機械", "試験装置", "省力化装置"}, None, True),
    ("ユニクラフトナグラ（財団の生成AI等活用実証の採択）", "湖西市", {"業種未確認"}, None, True),
    ("イハラ製作所（財団の採択、アルミダイカストの AI 外観検査）", "浜松市", {"ダイカスト", "非鉄金属"}, None, True),
    ("駿遠商会（Copilot 研修、機械部品の卸、27名）", "島田市", {"卸売", "機械器具卸", "機械部品"}, (27, 27), True),
    ("大豊建設 大井川取水工作業所（AI 文字起こし、大企業の現場）", "島田市", {"建設", "総合工事業", "土木"}, None, True),
    ("オーアイ・イノベーション（帯鋸歯 AI 検査の開発、作る側）", "島田市", {"製材機械", "AI製品開発"}, None, True),
    ("イシダテック（冷凍カツオの AI 試験機の開発、作る側）", "焼津市", {"食品機械", "AI製品開発"}, None, True),
    ("ドゥシステム（輸液ポンプ点検 AI アプリ、作る側）", "三島市", {"AI製品開発", "ソフトウェア"}, None, True),
    ("SIer・アルモニコス・イメージテック・カタナコーポレーション・ロボセンサー技研（AI を作る側）", "浜松市",
     {"AI製品開発", "ソフトウェア", "情報サービス"}, None, True),
    ("落合刃物工業（茶園管理システム、AI の語なし）", "菊川市", {"茶の機械", "農業機械"}, None, False),
    ("浜松倉庫（DXセレクション、AI ではない、116人）", "浜松市", {"倉庫", "運輸"}, (116, 116), False),
    # 既出（他県で使用済み）
    ("丸紅（島田市、滋賀で使用済み）", "島田市", {"業種未確認"}, None, True),
    ("浜の湯（伊豆稲取温泉の旅館、福井で使用済み）", "東伊豆町", {"宿泊", "温泉旅館"}, None, True),
    ("古屋旅館（熱海市、大分で使用済み）", "熱海市", {"宿泊", "温泉旅館"}, None, True),
    ("東邦農園（島田市、製茶工場の AI カメラ、福岡で使用済み）", "島田市", {"製茶", "農業"}, None, True),
    ("菅山園・エコグリーン勝間田（牧之原市、茶の AI 解析、佐賀で使用済み）", "牧之原市", {"茶", "農業"}, None, True),
    ("ベルファーム（菊川市、選果の AI、熊本で使用済み）", "菊川市", {"農業", "選果"}, None, True),
    ("JAみっかび（浜松市、ミカンの AI 選果、愛媛・香川で使用済み）", "浜松市", {"農協", "選果"}, None, True),
    ("マルミフーズ 焼津工場（TUNA SCOPE、青森で使用済み）", "焼津市", {"水産加工", "冷凍まぐろ"}, None, True),
    ("協和製作所（沼津市、AI 類似図面検索、広島で使用済み）", "沼津市", {"生産用機械", "機械加工"}, None, True),
    ("昭和冷凍（静岡市、自動配車、福島で使用済み）", "静岡市", {"冷蔵倉庫", "運輸"}, None, True),
    ("橋本組（焼津市、AI inside、建設）", "焼津市", {"建設", "総合工事業"}, None, True),
    ("LIFEFUND（浜松市、勉強会）", "浜松市", {"業種未確認"}, None, True),
    # cases2.md（2026-11-11）
    ("もこあもこ合同会社（袋井市、障がい児通所支援、16名。AI 音声入力で面談記録 62.5h/月、市の DX 事例集）", "袋井市", {"障害福祉", "障がい児通所支援"}, (16, 16), True),
    ("マルマ（浜松市三ヶ日、みかんの出荷。蜜柑AIビジョン）", "浜松市", {"選果", "農産物の集出荷", "みかん"}, None, True),
    ("酪農王国（函南町、観光牧場・クラフトビール、約50名。生成AIで文書の下書き、ベンダーの発表）", "函南町", {"観光牧場", "乳製品", "酒類製造"}, (50, 50), True),
    ("早川製作所（袋井市、製造、74名。Excel と AI で集計、AI の寄与は不明）", "袋井市", {"業種未確認"}, (74, 74), True),
    ("タクシー支援サービス（静岡市、静岡市デジタル活用補助金の採択）", "静岡市", {"タクシー", "運輸"}, None, True),
    ("レコードデスク（静岡市、AI 映像補正、静岡市デジタル活用補助金の採択）", "静岡市", {"映像制作", "映像"}, None, True),
    # cases_outside.md（県外、2026-11-11）
    ("フライスター（神奈川県横浜市港北区、パン粉などの食品製造、166人。受注AIエージェント）", "県外", {"食料品", "パン粉"}, (166, 166), True),
    ("エヌアセット（神奈川県川崎市高津区、賃貸仲介・管理、107名。AI でメール下書き）", "県外", {"不動産管理", "賃貸仲介"}, (107, 107), True),
]

# 市町村の民営従業者数と、試算に選んだ中分類の事業所数・従業者数（stats.md の一覧表と (B)。経済センサス 2021年6月1日、民営）
# slug: (民営従業者, 中分類, 中分類の事業所, 中分類の従業者)
STAT = {
    # slug: (民営従業者, 中分類〔または大分類〕, 事業所〔分からなければ None〕, 従業者)。stats.md の経済センサス 2021年6月1日、民営
    "shizuoka-city": (346576, "情報サービス業", 225, 4995),
    "hamamatsu": (382432, "生産用機械器具製造業", 508, 8250),
    "numazu": (100460, "食料品製造業", 162, 2763),
    "atami": (17731, "不動産業，物品賃貸業（中分類の値は未確認。民営従業者で代用。D1 が確かめる）", None, 17731),
    "mishima": (44496, "卸売業，小売業（大分類 16.8%）", None, 7475),
    "fujinomiya": (56524, "生産用機械器具製造業", 68, 2677),
    "ito": (26468, "宿泊業", 314, 3772),
    "shimada": (37608, "卸売業，小売業（大分類 19.1%）", None, 7183),
    "fuji": (119854, "パルプ・紙・紙加工品製造業", 271, 9126),
    "iwata": (82775, "プラスチック製品製造業", 73, 2468),
    "yaizu": (60261, "道路貨物運送業", 141, 3733),
    "kakegawa": (55856, "電気機械器具製造業", None, 2402),
    "fujieda": (55789, "社会保険・社会福祉・介護事業（7.4%）", None, 4128),
    "gotemba": (40039, "宿泊業", None, 1670),
    "fukuroi": (42226, "道路貨物運送業（6.4%）", None, 2702),
    "shimoda": (9638, "宿泊業（15.4%）", None, 1484),
    "susono": (26680, "学術研究，専門・技術サービス業（大分類 16.9%）", None, 4509),
    "kosai": (36046, "プラスチック製品製造業", None, 1007),
    "izu": (11656, "社会保険・社会福祉・介護事業（8.1%）", None, 944),
    "omaezaki": (14484, "建設業（大分類 11.4%）", None, 1651),
    "kikugawa": (19960, "生産用機械器具製造業", None, 1185),
    "izunokuni": (18651, "医療業（13.1%）", None, 2443),
    "makinohara": (26973, "飲料・たばこ・飼料製造業", 149, 2197),
    "higashiizu": (4936, "社会保険・社会福祉・介護事業（7.8%）", None, 385),
    "kawazu": (2585, "医療業（16.9%）", None, 437),
    "minamiizu": (2667, "宿泊業（19.2%）", None, 512),
    "matsuzaki": (1972, "飲食料品小売業（12.0%）", None, 237),
    "nishiizu": (2845, "食料品製造業", None, 219),
    "kannami": (9775, "飲食料品小売業（11.2%）", None, 1095),
    "shimizu-town-shizuoka": (16392, "卸売業，小売業（大分類 25.4%）", None, 4164),
    "nagaizumi": (20215, "プラスチック製品製造業", None, 913),
    "oyama-town": (7651, "金属製品製造業", None, 511),
    "yoshida": (17056, "食料品製造業", None, 2540),
    "kawanehon": (2873, "建設業（大分類 11.1%）", None, 319),
    "mori-town-shizuoka": (8805, "輸送用機械器具製造業", None, 2048),
}

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])（茨城と同じ9列）
# 業種・業態は stats.md の各市町村の「(B) 中小企業の業種の候補」（経済センサスの中分類）から選んだ。
# 大和郡山市の食料品・業務用機械（大企業の工場）、天理市・葛城市の電機、橿原市の輸送用機械、天理市・川西町の大きな生産用機械、
# 川西町の印刷・輸送用機械（数所で千人規模）、安堵町の金属製品、上北山村の飲食料品卸売（1所・291人）、天理市の宗教、
# 三郷町の医療業（大きな病院と読める）は試算の業種・業態にしない。農業・林業も試算の業種にしない。
# (市町, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種は stats.md の「市町ごとの主要産業の候補」の中小企業の業種から選んだ。完成車・二輪・楽器・製紙の大企業の工場と読める業態、
# 1〜数事業所の中分類（裾野市の研究機関・森町のゴム・湖西市の電気機械・御前崎市の電気業）、農林漁業は試算の業種にしない。
# 事例の会社と同じ市・同じ業態にならないようにした（熱海市は古屋旅館〔大分で使用済み〕、東伊豆町は浜の湯〔福井で使用済み〕があるので宿泊にしない、
# 焼津市は水産加工の事例〔マルミフーズ・イシダテック〕があるので冷蔵倉庫、菊川市は茶の機械〔落合刃物工業〕を避けた）。
# 2026-11-11: 余り0（ちょうどの時間）で既存1,169本と23県の PLAN と重ならない値を、規模の小さい順に小さい値から当てた（_assign.py）。
# ちょうどの時間で約62万円未満の空きはほぼなく、町でも42〜124名・月318時間以上になった（1人の月の業務量が40時間を超えるページがある）。
PLAN = [
    ('静岡市', 'shizuoka-city', '情報通信業', 'ソフトウェア業（業務システムの受託開発・保守）', {'業務システム', 'ソフトウェア受託開発'}, 150,
     '顧客からの問い合わせ・障害連絡への一次回答の下書きと、要件定義の打合せ記録の要約、仕様書・提案書の下書き', 48, 24.25),
    ('浜松市', 'hamamatsu', '製造業', '生産用機械（自動化設備・専用機の設計と製造）', {'自動化設備', '専用機', '生産用機械'}, 180,
     '取引先からの仕様・納期の問い合わせへの回答と、設計変更の連絡書、取扱説明書・検査記録の下書き', 56, 26.0),
    ('沼津市', 'numazu', '製造業', '食料品（干物・水産加工品の製造）', {'食料品', '干物', '水産加工'}, 70,
     '量販店・土産物店の取引先からの規格・原材料・賞味期限の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 32, 41.75),
    ('熱海市', 'atami', '不動産・物品賃貸業', '不動産管理（リゾートマンション・別荘の管理）', {'マンション管理', '不動産管理', '別荘管理'}, 65,
     '区分所有者・別荘の持ち主からの問い合わせへの回答と、管理組合の議事録・総会資料の下書き、点検・修繕の報告書の作成', 32, 20.75),
    ('三島市', 'mishima', '卸売業・小売業', '食料品・酒類の卸（飲食店・ホテル向け）', {'卸売', '酒類卸', '食料品卸'}, 85,
     '飲食店・ホテルの取引先からの在庫・納期・規格の問い合わせへの回答と、見積書・発注書の作成、メーカーへの照会文の下書き', 40, 33.5),
    ('富士宮市', 'fujinomiya', '製造業', '生産用機械（製紙・食品機械の部品の加工）', {'機械部品', '生産用機械', '製紙機械'}, 95,
     '取引先からの図面・仕様・納期の問い合わせへの回答と、作業手順書・検査記録の取りまとめ、不具合の報告書の下書き', 48, 29.0),
    ('伊東市', 'ito', '宿泊・飲食サービス業', '温泉旅館（個人客・家族客が中心）', {'宿泊', '温泉旅館'}, 90,
     '予約サイト・メールの問い合わせへの返信の下書きと、送迎・食事の手配の連絡、館内案内の多言語の文の作成', 48, 29.75),
    ('島田市', 'shimada', '卸売業・小売業', '茶の問屋（荒茶の仕入れと仕上げ茶の販売）', {'茶の卸', '茶問屋'}, 60,
     '小売店・通販の取引先からの在庫・規格・産地の問い合わせへの回答と、見積書・商品説明の文の作成、出荷の記録の取りまとめ', 40, 30.5),
    ('富士市', 'fuji', '製造業', 'パルプ・紙・紙加工品（紙器・段ボールの加工）', {'紙器', '段ボール', '紙加工品'}, 120,
     '取引先からの仕様・納期・数量の問い合わせへの回答と、見積書・作業指示書の作成、品質の記録・不具合報告の取りまとめ', 48, 29.5),
    ('磐田市', 'iwata', '製造業', 'プラスチック製品（自動車部品の射出成形）', {'射出成形', 'プラスチック製品'}, 110,
     '取引先からの金型・納期・品質の問い合わせへの回答と、成形条件・検査記録の取りまとめ、不具合の報告書の下書き', 44, 32.0),
    ('焼津市', 'yaizu', '運輸業・郵便業', '冷凍・冷蔵の倉庫と配送（水産物・食品）', {'運輸', '冷蔵倉庫', '道路貨物運送'}, 100,
     '荷主からの在庫・入出庫・配送の問い合わせへの回答と、入出庫の記録・在庫報告の作成、配車の連絡', 52, 26.0),
    ('掛川市', 'kakegawa', '製造業', '電気機械（制御盤・配電盤の製造）', {'電気機械', '制御盤', '配電盤'}, 92,
     '取引先からの仕様・納期の問い合わせへの回答と、図面の変更の連絡書、検査記録・取扱説明書の下書き', 32, 43.25),
    ('藤枝市', 'fujieda', '医療・福祉', '介護老人保健施設（通所リハビリを併設）', {'介護老人保健施設', '介護'}, 102,
     'リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成', 49, 28.0),
    ('御殿場市', 'gotemba', '宿泊・飲食サービス業', 'ホテル（観光・ゴルフ・研修の客）', {'宿泊', 'ホテル'}, 115,
     '予約サイト・メールの問い合わせへの返信の下書きと、団体・研修の見積書・行程の連絡、館内案内の多言語の文の作成', 48, 31.0),
    ('袋井市', 'fukuroi', '運輸業・郵便業', '道路貨物運送（倉庫を併設した配送）', {'倉庫', '運輸', '道路貨物運送'}, 130,
     '荷主からの配送状況・納品の問い合わせへの回答と、配車の連絡、運行の記録・点呼記録の取りまとめ', 46, 30.0),
    ('下田市', 'shimoda', '宿泊・飲食サービス業', '温泉旅館（海水浴・観光の客）', {'宿泊', '温泉旅館'}, 55,
     '予約の電話・メールの問い合わせへの返信の下書きと、送迎・季節の行事の案内の文、宿泊者の記録の整理', 40, 35.5),
    ('裾野市', 'susono', '学術研究・専門技術サービス', '設計の受託（機械部品の CAD 設計・解析）', {'技術サービス', '設計受託', 'CAD設計'}, 80,
     '取引先との仕様の打合せ記録の要約と、設計・解析の報告書の下書き、図面の変更履歴の取りまとめ', 26, 34.0),
    ('湖西市', 'kosai', '製造業', 'プラスチック製品（自動車の内装部品の成形）', {'内装部品', 'プラスチック製品'}, 86,
     '取引先からの図面変更・納期の問い合わせへの回答と、作業手順書（多言語）・検査記録の取りまとめ', 48, 28.5),
    ('伊豆市', 'izu', '医療・福祉', '特別養護老人ホーム（短期入所を併設）', {'特別養護老人ホーム', '介護'}, 71,
     'ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成', 48, 27.25),
    ('御前崎市', 'omaezaki', '建設業', '総合工事業（港湾・土木、公共工事が中心）', {'土木', '建設', '総合工事業'}, 63,
     '公共工事の施工計画書・提出書類の作成と、工事写真の整理、発注者との打合せ記録の要約', 32, 39.25),
    ('菊川市', 'kikugawa', '製造業', '生産用機械（自動車部品の加工治具・省力化装置）', {'省力化装置', '治具', '生産用機械'}, 75,
     '取引先からの仕様・納期の問い合わせへの回答と、組立の手順書・検査記録の取りまとめ、部品メーカーへの照会文', 40, 34.0),
    ('伊豆の国市', 'izunokuni', '医療・福祉', '病院（回復期リハビリ・療養病床）', {'病院', '医療'}, 160,
     '入院・退院の説明文書と、他の病院・ケアマネジャーへの紹介状・報告書の下書き、委員会の議事録の作成', 48, 29.25),
    ('牧之原市', 'makinohara', '製造業', '製茶（荒茶の仕上げ加工・ティーバッグの製造）', {'製茶', '仕上げ茶'}, 66,
     '茶商・量販店の取引先からの規格・数量・残留農薬の検査の問い合わせへの回答と、規格書の作成、製造の記録の取りまとめ', 41, 32.0),
    ('東伊豆町', 'higashiizu', '医療・福祉', '特別養護老人ホーム（デイサービスを併設）', {'特別養護老人ホーム', '通所介護', '介護'}, 62,
     '介護記録・事故報告の清書と、家族への近況の連絡文、職員の研修記録の作成', 32, 41.5),
    ('河津町', 'kawazu', '医療・福祉', '病院（一般・療養病床、訪問診療）', {'病院', '医療'}, 96,
     '入院・退院の説明文書と、紹介状・診療情報の返書の下書き、委員会の議事録の作成', 48, 28.25),
    ('南伊豆町', 'minamiizu', '宿泊・飲食サービス業', '民宿・旅館（海の客・釣り客が中心）', {'宿泊', '民宿'}, 54,
     '予約の電話・メールの問い合わせへの返信の下書きと、送迎・食事の手配の連絡、宿泊者の記録の整理', 40, 32.5),
    ('松崎町', 'matsuzaki', '卸売業・小売業', '小売（食料品・日用品のスーパー）', {'食料品小売', 'スーパー', '小売'}, 48,
     '仕入先への発注・欠品の連絡と、売場の案内・チラシの文の下書き、客からの取り寄せ・問い合わせへの回答', 32, 39.75),
    ('西伊豆町', 'nishiizu', '製造業', '食料品（干物・塩かつおなど水産加工品の製造）', {'食料品', '干物', '水産加工'}, 50,
     '土産物店・通販の取引先からの原材料・賞味期限の問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ', 32, 40.25),
    ('函南町', 'kannami', '卸売業・小売業', '食料品スーパー（地域の数店舗）', {'食料品小売', 'スーパー', '小売'}, 124,
     '仕入先への発注・欠品の連絡と、店舗間の在庫の連絡、売場の案内・チラシの文の下書き', 44, 31.0),
    ('清水町', 'shimizu-town-shizuoka', '卸売業・小売業', '機械器具・工具の卸（工場向けの部品・消耗品）', {'機械器具卸', '卸売', '工具'}, 72,
     '工場の取引先からの在庫・納期・代替品の問い合わせへの回答と、見積書・発注書の作成、メーカーへの照会文の下書き', 48, 26.75),
    ('長泉町', 'nagaizumi', '製造業', 'プラスチック製品（医療用の容器・部品の成形）', {'医療用容器', 'プラスチック製品'}, 105,
     '取引先からの規格・ロット・品質の問い合わせへの回答と、製造記録・検査成績書の取りまとめ、変更の連絡書の下書き', 50, 28.0),
    ('小山町', 'oyama-town', '製造業', '金属製品（建築金物・板金の加工）', {'金属製品', '板金', '建築金物'}, 58,
     '工務店・元請からの見積・納期・加工の問い合わせへの回答と、加工図の確認の連絡、出荷の記録の取りまとめ', 32, 40.75),
    ('吉田町', 'yoshida', '製造業', '食料品（冷凍食品・惣菜の製造）', {'食料品', '冷凍食品', '惣菜'}, 135,
     '量販店・外食の取引先からの規格・原材料・アレルゲンの問い合わせへの回答と、規格書の改訂、製造・衛生管理の記録の取りまとめ', 64, 22.25),
    ('川根本町', 'kawanehon', '建設業', '総合工事業（林道・治山・道路の工事）', {'土木', '建設', '総合工事業'}, 42,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理', 29, 44.0),
    ('森町', 'mori-town-shizuoka', '製造業', '輸送用機械（二輪・四輪の部品の切削加工）', {'切削', '輸送用機械', '自動車部品'}, 88,
     '取引先からの図面・仕様・納期の問い合わせへの回答と、工程の変更の連絡書、検査成績書・不具合報告の取りまとめ', 43, 32.0),
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
            print(f"  NG {city} の時間 {h} は近畿3県の割り当て（×4 を{MOD_N}で割った余り {MOD_R}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 静岡県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 静岡県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは静岡県の中だけを NG にする）")
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
