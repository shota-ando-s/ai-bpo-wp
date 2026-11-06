#!/usr/bin/env python3
"""沖縄県41市町村の試算の割り当てを計算し、重なりを確かめる（2026-11-05）。

data/area/kagoshima/_calc.py を元に作った。県ページ（/area/okinawa/）には試算を入れないので、PLAN は41行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **北海道・北関東3県・沖縄の取り決め**: 月の削減時間（0.25時間刻み）×4 を5で割った余りが 4（沖縄県）の時間だけを使う
     （1.0, 2.25, 3.5, 4.75, … の1.25時間刻み。data/area/_batch5/shared.md）
  1. 41ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、沖縄県を除く）の「## 試算」の節に出てくる
     「◯時間」「◯万円」の値と重ならない。拾い方は鹿児島県の _calc.py と同じ（広めに拾う）
  3. 全県の data/area/*/_calc.py の PLAN（沖縄県を除く。glob で全部読む。北海道・茨城・栃木・群馬を含む）の
     月の削減時間・月の時間換算額と重ならない。他県の _calc.py は import で読み、だめなら行頭の `PLAN = [` を文字列で切り出す。
     **読めないファイルは NG にせず警告**。REQUIRED の県はファイルがなければ NG
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases*.md・subsidy_*_areas.md の事例の会社と同じにならない（CASES と照合。鹿児島と同じ判定）
  6. slug が _brief.md の41市町村と一致する（沖縄市 okinawa-city、西原町 nishihara-town、東村 higashi-village）
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
  8. 県ページには試算を入れない（PLAN は41行）
使い方: python3 data/area/okinawa/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/okinawa/_calc.py free 製造業 30 200   （余り4の時間で、既存・他県と重ならない時間と金額の候補を出す）
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
SELF = "okinawa"
MOD_N, MOD_R = 5, 4  # 北海道・北関東3県・沖縄の割り当て（月の削減時間×4 を5で割った余り）。沖縄県は 4

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
    # 市（11）
    "naha", "ginowan", "ishigaki", "urasoe", "nago", "itoman", "okinawa-city", "tomigusuku", "uruma", "miyakojima", "nanjo",
    # 町（11）
    "motobu", "kin", "kadena", "chatan", "nishihara-town", "yonabaru", "haebaru", "kumejima", "yaese", "taketomi", "yonaguni",
    # 村（19）
    "kunigami", "ogimi", "higashi-village", "nakijin", "onna", "ginoza", "ie", "yomitan", "kitanakagusuku", "nakagusuku",
    "tokashiki", "zamami", "aguni", "tonaki", "minamidaito", "kitadaito", "iheya", "izena", "tarama",
}

# 照合が必須の県（2026-11-05 にある _calc.py）。ファイルがなければ NG
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima")

# cases*.md・subsidy_*_areas.md の事例の会社（調査がそろったら足す）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・交付決定・使用済み・目標を含む〕)
CASES = [
    # 那覇市（cases.md。数値つき・数値なし・ベンダーの発表）
    ("琉球朝日放送（AI アナウンサー・自動翻訳、正規48名）", "那覇市", {"放送", "テレビ"}, (48, 48), True),
    ("琉球新報開発（AI-OCR と RPA で受注業務、正規68名・非正規13名）", "那覇市", {"広告", "イベント"}, (68, 81), True),
    ("金秀建設（社長が生成AIで出来高管理アプリ、130名。残業25%減は AI ではない）", "那覇市", {"建設", "総合工事", "建築工事", "土木"}, (130, 130), True),
    ("育陶園（やちむん、ChatGPT で文章の添削、37名）", "那覇市", {"陶器", "窯業"}, (37, 37), True),
    ("いまいパン（パンの製造・小売・卸、生成AIで書類確認）", "那覇市", {"パン・菓子製造", "小売"}, None, True),
    ("Bim（訪問看護ステーション、生成AIで看護報告書の下書き、16人）", "那覇市", {"医療", "訪問看護"}, (16, 16), True),
    ("志良堂電気商会（電気設備の卸・小売、Notion AI、5人）", "那覇市", {"卸売", "電気設備"}, (5, 5), True),
    ("クラシコ（ワインショップ・レストラン、生成AI、4人）", "那覇市", {"小売", "飲食店"}, (4, 4), True),
    ("沖縄ファミリーマート（AI-OCR の請求書受取、467名。ベンダーの発表）", "那覇市", {"小売", "コンビニ"}, (467, 467), True),
    ("半嶺当徹事務所（土地家屋調査士、沖縄DX推進 R8、生成AIで報告書の下書き）", "那覇市", {"土地家屋調査士", "士業"}, None, True),
    ("ラピラス（児童福祉、沖縄DX推進 R8、生成AIで記録案）", "那覇市", {"児童福祉", "障害福祉"}, None, True),
    ("沖縄県電気工事業工業組合（沖縄DX推進 R8、外部AI連携）", "那覇市", {"業界団体", "電気工事"}, None, True),
    ("求人おきなわ（求人広告、沖縄DX推進 R7、SFA と AI）", "那覇市", {"求人広告", "広告"}, None, True),
    ("沖縄総合貿易（沖縄DX推進 R7、AIカメラの自動発注は R9 の計画）", "那覇市", {"業種未確認"}, None, True),
    ("エフ琉球（沖縄DX推進 R7、AI の需要予測は計画）", "那覇市", {"業種未確認"}, None, True),
    ("琉興リース（沖縄DX推進 R7、AI の需要予測は今後）", "那覇市", {"物品賃貸", "リース"}, None, True),
    ("NTカンパニー（製造業・介護、沖縄DX促進 R4、AI の画像認識は今後）", "那覇市", {"給食", "介護"}, None, True),
    ("沖縄ボイラエンジニアリング（管工事、AI の故障予測は今後、15名）", "那覇市", {"管工事", "設備工事"}, (15, 15), True),
    ("南都（本店 那覇市、おきなわワールドは南城市。AI カメラは計画）", "那覇市", {"観光施設"}, None, True),
    ("高倉コーポレーション（ホテル、AI Travel と提携。会員限定の報道・計画）", "那覇市", {"宿泊", "ホテル"}, None, True),
    # 琉球通運（徳島県松茂町の記事で使用済み）は cases2.md の法人番号の照合で本店が浦添市 → 浦添市の節へ移した（2026-11-06、D2）
    ("大央ハウジング（那覇市泊、OCR・RPA・VBA で年660時間の見込み。AI の記載なし）", "那覇市", {"住宅", "不動産"}, None, False),
    ("エムズ（かりゆしウェアのレンタル、沖縄DX推進 R8。AI の記載なし）", "那覇市", {"衣装レンタル", "小売"}, None, False),
    ("ハンズ・コム（広告、沖縄DX推進 R8。AI の記載なし）", "那覇市", {"広告"}, None, False),
    ("拓商（葬祭、沖縄DX推進 R8。AI の記載なし）", "那覇市", {"葬祭"}, None, False),
    ("美らいふ（保険代理、レンタカー事故管理、沖縄DX推進 R8。AI の記載なし）", "那覇市", {"保険代理"}, None, False),
    ("那覇酒類販売（物流デジタル R8 1次、ハンディターミナル。AI の記載なし。所在は一覧にない）", "所在未確認", {"卸売", "酒類卸売"}, None, False),
    # 宮古島市
    ("宮古新報（新聞、AI の記事作成ツールで1記事約2時間短縮）", "宮古島市", {"新聞"}, None, True),
    ("宮古島観光協会（AI アバターで観光の問い合わせ、実証）", "宮古島市", {"観光協会"}, None, True),
    ("東和（自動車整備、AI 解析の整備支援は2030年頃）", "宮古島市", {"自動車整備"}, None, True),
    ("宮古島の雪塩（物流デジタル R8 1次、WMS。AI の記載なし）", "宮古島市", {"製塩", "食料品"}, None, False),
    # 石垣市
    ("石垣焼窯元（陶器、AI カメラ、8人。時間の数値は予約システム）", "石垣市", {"陶器", "窯業"}, (8, 8), True),
    ("八重山自動車商会（高圧ガス販売、沖縄DX推進 R8。AI の記載なし）", "石垣市", {"高圧ガス販売", "卸売"}, None, False),
    # 浦添市
    ("マルキン海産（もずくなどの食品卸・製造、FAX 注文の AI 判別、65名）", "浦添市", {"水産加工", "水産物卸", "もずく"}, (65, 65), True),
    ("ネイバーフッドケアマネジメント（居宅介護支援、7人のケアマネ、報道）", "浦添市", {"介護", "居宅介護支援"}, (7, 7), True),
    ("コープおきなわ（生協、惣菜コーナーの AI カメラの調査）", "浦添市", {"小売", "生協"}, None, True),
    ("イバノ（食料品卸、AI-OCR 搭載ハンディ。沖縄DX推進 R8・物流デジタル R8 2次）", "浦添市", {"卸売", "飲食料品卸売"}, None, True),
    ("沖縄電子（リユースの卸、AI 査定支援。沖縄DX推進 R8）", "浦添市", {"卸売", "リユース"}, None, True),
    ("BowL（EAP・メンタルヘルス、AI のフィードバック。沖縄DX推進 R8）", "浦添市", {"メンタルヘルス支援"}, None, True),
    ("沖縄急送（運送、AI のマーケティングは計画、227名）", "浦添市", {"道路貨物運送", "運送"}, (227, 227), True),
    ("琉球警備保障（警備、AI の混雑予測は今後）", "浦添市", {"警備"}, None, True),
    ("琉球通運（AI 自動配車、運転手約170人。徳島県松茂町の記事で使用済み。本店は法人番号で浦添市〔cases2〕）", "浦添市", {"道路貨物運送", "運送"}, (170, 170), True),
    # 沖縄市
    ("WAN STYLE（介護、AI の送迎ルート、年約132時間）", "沖縄市", {"介護", "通所介護"}, None, True),
    ("沖縄北あんしん内科クリニック（画像診断 AI・文字起こし、報道）", "沖縄市", {"医療", "診療所"}, None, True),
    # うるま市
    ("CAVE OKINAWA（鍾乳洞の観光施設、生成AIの多言語音声ガイド、報道）", "うるま市", {"観光施設"}, None, True),
    ("タイガー産業（建築材料卸、OCR・AI で書類作成。沖縄DX推進 R8）", "うるま市", {"卸売", "建築材料卸売"}, None, True),
    ("仲松ミート（冷凍食品の製造、AI 音声認識の Alexa）", "うるま市", {"冷凍食品", "食肉加工"}, None, True),
    # 糸満市
    ("G FARM（きゅうり・キャベツ、AI の自動潅水施肥、3名）", "糸満市", {"農業", "野菜"}, (3, 3), True),
    ("糸満自動車学校（AI 教習、2026年7月から）", "糸満市", {"自動車教習所"}, None, True),
    # 南風原町
    ("イカリ消毒沖縄（衛生管理・害虫駆除、AI 搭載ドライブレコーダー）", "南風原町", {"衛生管理", "害虫駆除"}, None, True),
    ("故郷（小規模デイサービス、職員4人、報道。運営会社の所在は南城市）", "南風原町", {"介護", "通所介護"}, (4, 4), True),
    ("大地測量設計（測量、AI の割合は不明。所在は那覇市）", "南風原町", {"測量"}, None, True),
    # 北谷町
    ("ケヤキコーポレーション（宿泊業、ChatGPT 連携のチャットボット）", "北谷町", {"宿泊", "ホテル"}, None, True),
    ("アイムホーム（建設・旅行、多言語メディア×CRM×AI。沖縄DX推進 R8）", "北谷町", {"建設", "不動産", "旅行"}, None, True),
    # 宜野湾市
    ("孝（建設業、AI 画像診断で退去費用の算定。沖縄DX推進 R8）", "宜野湾市", {"建設", "原状回復"}, None, True),
    ("LiLz（IoT カメラと機械学習の点検。作る側）", "宜野湾市", {"情報サービス", "ソフトウェア"}, None, True),
    # 西原町
    ("貴建設（ボーリング調査、RAG 型 AI。沖縄DX推進 R7）", "西原町", {"地質調査", "ボーリング"}, None, True),
    ("南島酒販（酒類卸、配送ルート最適化。沖縄DX推進 R8。AI の記載なし）", "西原町", {"卸売", "酒類卸売"}, None, False),
    # 名護市
    ("琉球ワークス（土産品の卸、AI-OCR で注文データ）", "名護市", {"卸売", "土産品卸売"}, None, True),
    # 南城市
    ("ライフシフト（ケアプランのアプリに AI 要約。作る側）", "南城市", {"情報サービス", "ソフトウェア"}, None, True),
    # 豊見城市
    ("社会医療法人友愛会（健診サービスの DX、沖縄DX推進 R8。AI の記載なし）", "豊見城市", {"医療", "病院"}, None, False),
    # 竹富町（事務所は石垣市美崎町）
    ("竹富町観光協会（生成AIの多言語音声ガイドの実証先）", "竹富町", {"観光協会"}, None, True),
    # 八重瀬町
    ("ぐしちゃんピーマン の AI・データ活用（KDDI・沖縄セルラーの実証）", "八重瀬町", {"農業", "野菜"}, None, True),
    # 国頭村
    ("くにがみ畜産（養豚一貫、AI の増体予測は R10 以降。沖縄DX推進 R8）", "国頭村", {"養豚", "畜産"}, None, True),
    # 恩納村
    ("かりゆし（ホテル、生成AIでツール調査、519名）", "恩納村", {"宿泊", "ホテル"}, (519, 519), True),
    ("ホテルみゆきビーチ（多言語 AI チャットボット。山形県天童市の記事で使用済み）", "恩納村", {"宿泊", "ホテル"}, None, True),
    # cases2.md（2026-11-06）で足した会社・団体（D2 が追加。PLAN は変えていない）
    ("琉球通運航空（AI 電話。香川県宇多津町の記事で使用済み。本店は法人番号で豊見城市〔cases2〕）", "豊見城市", {"航空貨物", "運送"}, None, True),
    ("七和（道路舗装・アスファルト合材、AI-OCR。香川県丸亀市の記事で使用済み。本店は法人番号で那覇市〔cases2〕）", "那覇市", {"舗装工事", "アスファルト合材"}, None, True),
    ("キョウリツ（ホテルみゆきビーチの運営法人。本店 うるま市、ホテルは恩納村〔cases2〕）", "うるま市", {"宿泊", "ホテル"}, None, True),
    ("リュウェル（認知症の診断補助 AI を開発中、情報通信業12名。作る側〔cases2〕）", "那覇市", {"情報サービス", "ソフトウェア", "医療機器"}, (12, 12), True),
    ("沖電グローバルシステムズ（AI の太陽光発電予測、報道の見出しだけ。作る側〔cases2〕）", "那覇市", {"情報サービス", "ソフトウェア"}, None, True),
    ("パシフィックハイウェイ沖縄・Clann（道の駅ぎのざで AI 接客の無人販売機の実証。作る側〔cases2〕）", "那覇市", {"情報サービス"}, None, True),
    ("道の駅ぎのざの AI 接客の無人販売機の実証（IT 企業2社、報道〔cases2〕）", "宜野座村", {"小売", "道の駅"}, None, True),
    ("スタジオユリグラフ（生成AIの文書作成ツール Xaris。作る側〔cases2〕）", "名護市", {"情報サービス", "ソフトウェア"}, None, True),
    ("名護市 AI オンデマンド交通の実証（運行 丸金交通、主体 ジャパンエンターテイメント・沖縄セルラー〔cases2〕）", "名護市", {"旅客運送", "タクシー"}, None, True),
    ("ジャパンエンターテイメント（観光人材の育成。AI の記載なし〔cases2〕）", "名護市", {"観光", "人材育成"}, None, False),
    ("沖縄やんばるDMO（AI 対話ツールで地域の魅力を言語化、報道。法人格・所在未確認〔cases2〕）", "所在未確認", {"観光協会", "DMO"}, None, True),
    ("ナウレッジ（AI の商品判別 EDI。マルキン海産の実証のベンダー。作る側〔cases2〕）", "豊見城市", {"情報サービス", "ソフトウェア"}, None, True),
    ("宮古島デンタルオフィス（AI 機能のある詰め物の製作機器、2021年の報道〔cases2〕）", "宮古島市", {"歯科", "医療"}, None, True),
    ("沖縄福祉創業社（小規模デイサービス「故郷」の運営、本店 南城市〔cases2・cases〕）", "南城市", {"介護", "通所介護"}, (4, 4), True),
    ("沖縄セルラー電話と国頭村の密猟対策の AI 実証（大企業、報道〔cases2〕）", "国頭村", {"通信"}, None, True),
    ("JAおきなわ（営農指導日誌の AI、報道だけ。団体〔cases2〕）", "所在未確認", {"農業協同組合"}, None, True),
    ("街クリーン（廃棄物の収集運搬、収集車でゴミを AI 検出・AI ドラレコ。所在は南城市とみられる〔cases・companies〕）", "南城市", {"廃棄物処理"}, None, True),
    ("野原ファーム（さとうきびの受託、自動操舵・ドローン。AI の記載なし〔cases2〕）", "八重瀬町", {"農業", "さとうきび"}, None, False),
    # 所在未確認・県外（cases_outside.md）
    ("兼正青果（青果卸、発注書 AI-OCR は稼働前の見込み）", "所在未確認", {"卸売", "青果卸売"}, None, True),
    ("大鏡建設（BP Storage で紙の電子化、224名）", "所在未確認", {"建設", "総合工事"}, (224, 224), True),
    ("協栄流通（生協の物流子会社、自動配車。沖縄では使わない）", "県外", {"道路貨物運送", "運送"}, None, True),
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
PLAN = [
    # 南部（14）
    ("那覇市", "naha", "医療・福祉", "病院（急性期の一般病床と外来）", {"医療", "病院"}, 200,
     "退院時サマリー・診療情報提供書の下書きと、患者・家族への説明文書、院内の委員会の議事録の作成", 44, 29.75),
    ("糸満市", "itoman", "製造業", "食料品（水産加工〔まぐろ・ソデイカなどの冷凍・加工品〕）", {"冷凍水産物", "水産加工"}, 110,
     "量販店・外食の取引先からの規格・産地・数量の問い合わせへの回答と、規格書・検査記録の取りまとめ", 27, 42.0),
    ("豊見城市", "tomigusuku", "医療・福祉", "病院（回復期リハビリテーション病棟と外来）", {"医療", "病院"}, 95,
     "リハビリの記録の要約と、退院前の説明文書・紹介状の下書き、カンファレンスの議事録の作成", 28, 43.0),
    ("南城市", "nanjo", "製造業", "食料品（豚肉の加工品〔ハム・ソーセージ〕の製造）", {"ハム・ソーセージ", "食肉加工"}, 68,
     "通販・小売の取引先に出す商品説明・表示の文の作成と、ギフトの受注の記録、製造記録の取りまとめ", 26, 41.5),
    ("与那原町", "yonabaru", "卸売業・小売業", "小売（ドラッグストア・日用品の店舗、町内外の複数店舗）", {"ドラッグストア", "小売"}, 80,
     "店舗からの発注・在庫の問い合わせへの回答と、売場の販促物・商品説明の文の作成、店長会議の議事録", 31, 39.0),
    ("南風原町", "haebaru", "製造業", "印刷（商業印刷・冊子の印刷と加工）", {"印刷"}, 73,
     "顧客からの見積・納期の問い合わせへの回答と、入稿データの確認の連絡、作業指示書・校正の記録の作成", 28, 39.25),
    ("八重瀬町", "yaese", "医療・福祉", "特別養護老人ホーム（短期入所を併設）", {"介護", "特別養護老人ホーム"}, 74,
     "ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成", 28, 41.75),
    ("久米島町", "kumejima", "製造業", "食料品（もずくなど水産物の加工・出荷）", {"もずく", "水産加工"}, 47,
     "本島・本土の取引先からの規格・数量・出荷日の問い合わせへの回答と、出荷の記録・衛生管理の記録の取りまとめ", 18, 40.5),
    ("渡嘉敷村", "tokashiki", "宿泊・飲食サービス業", "民宿・ペンション（食事の提供と港の送迎を含む）", {"宿泊", "民宿"}, 60,
     "予約サイト・メールの問い合わせへの返信と、船の欠航時の予約変更の連絡、口コミへの返信文の作成", 26, 26.5),
    ("座間味村", "zamami", "宿泊・飲食サービス業", "ホテル・ペンション（ダイビング・ホエールウォッチングの手配を含む）", {"ペンション", "宿泊"}, 59,
     "予約・ツアーの問い合わせへの返信と、船の時刻・欠航の案内文、外国語の問い合わせへの返信文の作成", 24, 37.25),
    ("粟国村", "aguni", "医療・福祉", "通所介護と訪問介護の事業所", {"介護", "通所介護"}, 41,
     "利用の記録と個別機能訓練計画書の下書き、家族への連絡帳の文の作成", 16, 47.75),
    ("渡名喜村", "tonaki", "医療・福祉", "訪問介護と通所介護の事業所", {"介護", "訪問介護"}, 32,
     "訪問・通所の記録の清書と、サービス担当者会議の記録、家族への連絡の文の作成", 12, 48.25),
    ("南大東村", "minamidaito", "建設業", "総合工事業（港湾・道路の土木工事）", {"土木", "建設"}, 42,
     "工事日報・安全書類の取りまとめと、発注者への工程の連絡文、資材の船便の手配の連絡の作成", 16, 46.5),
    ("北大東村", "kitadaito", "宿泊・飲食サービス業", "ホテル・民宿（食事の提供を含む）", {"宿泊", "民宿"}, 44,
     "予約の問い合わせへの返信と、飛行機・船の欠航時の予約変更の連絡、長期滞在の宿泊者への案内文の作成", 17, 47.0),
    # 中部（10）
    ("宜野湾市", "ginowan", "卸売業・小売業", "卸売（飲食料品〔市内外の飲食店・ホテルへの納品〕）", {"卸売", "飲食料品卸売"}, 102,
     "飲食店・ホテルの取引先からの在庫・規格・価格の問い合わせへの回答と、見積書・商品案内の作成、受注の記録の取りまとめ", 34, 33.5),
    ("浦添市", "urasoe", "運輸業・郵便業", "倉庫・道路貨物運送（県内の小売店への配送）", {"倉庫", "道路貨物運送"}, 101,
     "配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点検記録の取りまとめ", 26, 44.0),
    ("沖縄市", "okinawa-city", "卸売業・小売業", "小売（食品スーパー、市内外の複数店舗）", {"小売", "食品スーパー"}, 120,
     "店舗からの発注・欠品の問い合わせへの回答と、チラシ・売場の商品説明の文の作成、店長会議の議事録", 33, 38.0),
    ("うるま市", "uruma", "製造業", "金属製品（鉄骨・建築用金属製品の製造）", {"金属製品", "鉄骨"}, 90,
     "工務店・建設会社からの見積・納期の問い合わせへの回答と、製作図の変更の連絡、検査記録・作業指示書の作成", 32, 34.5),
    ("読谷村", "yomitan", "製造業", "窯業・土石（陶器〔やちむん〕の製造と工房の直売）", {"窯業", "陶器"}, 75,
     "店舗・通販の取引先への商品説明の文の作成と、注文・納期の問い合わせへの回答、受注の記録の取りまとめ", 32, 25.75),
    ("嘉手納町", "kadena", "医療・福祉", "訪問介護と居宅介護支援の事業所", {"介護", "居宅介護支援", "訪問介護"}, 70,
     "訪問の記録の清書と、サービス担当者会議の記録、ケアプランの文案の下書き", 27, 37.0),
    ("北谷町", "chatan", "宿泊・飲食サービス業", "飲食店（複数店舗のレストラン・カフェ）", {"飲食店"}, 100,
     "予約・団体の問い合わせへの返信と、外国語のメニュー・案内文の作成、店舗間の連絡・シフトの連絡文", 38, 30.5),
    ("北中城村", "kitanakagusuku", "医療・福祉", "介護付き有料老人ホーム（デイサービスを併設）", {"介護", "有料老人ホーム"}, 67,
     "ケア記録の清書と、入居の相談への返信、家族への近況の連絡文、運営懇談会の記録の作成", 24, 43.5),
    ("中城村", "nakagusuku", "医療・福祉", "有床診療所（外来・訪問診療を含む）", {"医療", "診療所"}, 69,
     "診療情報提供書・訪問診療の記録の下書きと、患者・家族への説明文書、介護事業所への連絡文の作成", 31, 34.0),
    ("西原町", "nishihara-town", "製造業", "食料品（パン・洋菓子の製造）", {"パン・菓子製造"}, 121,
     "量販店・コンビニの取引先からの規格・アレルゲンの問い合わせへの回答と、規格書・表示の文の改訂、製造記録の取りまとめ", 44, 27.25),
    # 北部（12）
    ("名護市", "nago", "宿泊・飲食サービス業", "リゾートホテル（宴会・婚礼を含む）", {"ホテル", "宿泊"}, 130,
     "予約サイト・メールの問い合わせへの返信と、宴会・婚礼の打ち合わせの記録、外国語の案内文・口コミへの返信文の作成", 46, 26.5),
    ("国頭村", "kunigami", "宿泊・飲食サービス業", "ホテル・コテージ（自然体験ツアーの手配を含む）", {"ホテル", "宿泊"}, 64,
     "予約サイト・メールの問い合わせへの返信と、ツアーの手配・雨天時の変更の連絡、口コミへの返信文の作成", 22, 47.0),
    ("大宜味村", "ogimi", "医療・福祉", "認知症対応型グループホームと小規模多機能型居宅介護", {"グループホーム", "介護"}, 61,
     "生活記録の清書と、運営推進会議の議事録、家族への便りの文の作成", 24, 27.25),
    ("東村", "higashi-village", "卸売業・小売業", "果実（パインアップル・マンゴーなど）の集出荷・直売（本土への発送を含む）", {"卸売", "果実の集出荷"}, 58,
     "市場・通販の取引先からの数量・出荷日の問い合わせへの回答と、出荷の記録の取りまとめ、商品案内の文の作成", 22, 39.5),
    ("今帰仁村", "nakijin", "卸売業・小売業", "花き（きくなど）の集出荷（本土の市場への出荷手配）", {"卸売", "花きの集出荷"}, 65,
     "市場・仲卸からの数量・規格の問い合わせへの回答と、出荷の記録・船便と空路の手配の連絡、生産者への連絡文の作成", 28, 34.25),
    ("本部町", "motobu", "宿泊・飲食サービス業", "ホテル（家族客・団体の受け入れ）", {"ホテル", "宿泊"}, 87,
     "予約・団体の問い合わせへの返信と、旅行会社への手配の連絡、外国語の案内文・口コミへの返信文の作成", 33, 33.0),
    ("恩納村", "onna", "建設業", "総合工事業（ホテル・住宅の建築と改修）", {"建築工事", "建設"}, 72,
     "施主・設計事務所への工程の連絡と、工事日報・安全書類の取りまとめ、打ち合わせの議事録の作成", 32, 32.0),
    ("宜野座村", "ginoza", "建設業", "総合工事業（土木・建築）", {"土木", "建設"}, 63,
     "工事日報・安全書類の取りまとめと、発注者への工程の連絡文、打ち合わせの議事録の作成", 24, 41.0),
    ("金武町", "kin", "医療・福祉", "介護老人保健施設（通所リハビリを併設）", {"介護", "老人保健施設"}, 84,
     "リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成", 32, 37.0),
    ("伊江村", "ie", "卸売業・小売業", "小売（食料品・日用品・建築資材、船便で仕入れ）", {"小売", "島の小売店"}, 66,
     "仕入先への発注と船便の手配の連絡と、島内の得意先からの在庫の問い合わせへの回答、売場の案内の文の作成", 28, 26.75),
    ("伊平屋村", "iheya", "製造業", "食料品（もずくの加工〔洗浄・塩蔵〕と出荷）", {"もずく", "水産加工"}, 34,
     "本島・本土の取引先からの規格・数量の問い合わせへの回答と、出荷の記録・衛生管理の記録の取りまとめ", 13, 23.0),
    ("伊是名村", "izena", "建設業", "総合工事業（農業土木・港湾の工事）", {"土木", "建設"}, 62,
     "工事日報・安全書類の取りまとめと、発注者への工程の連絡文、資材の船便の手配の連絡の作成", 28, 31.75),
    # 宮古（2）
    ("宮古島市", "miyakojima", "建設業", "総合工事業（建築・土木、ホテル・住宅の建設を含む）", {"土木", "建築工事", "建設"}, 151,
     "施主・発注者への工程の連絡と、施工計画書・安全書類の下書き、打ち合わせの議事録の作成", 36, 36.5),
    ("多良間村", "tarama", "建設業", "総合工事業（農業土木・道路の工事）", {"土木", "建設"}, 56,
     "工事日報・安全書類の取りまとめと、発注者への工程の連絡文、出来形の記録の整理", 24, 34.75),
    # 八重山（3）
    ("石垣市", "ishigaki", "宿泊・飲食サービス業", "ホテル（離島ツアー・送迎の手配を含む）", {"ホテル", "宿泊"}, 111,
     "予約サイト・メールの問い合わせへの返信と、船の欠航時の予約変更の連絡、外国語の案内文・口コミへの返信文の作成", 29, 41.0),
    ("竹富町", "taketomi", "宿泊・飲食サービス業", "リゾートホテル・旅館（港の送迎を含む）", {"ホテル", "宿泊"}, 78,
     "予約・問い合わせへの返信と、船の欠航時の予約変更の連絡、外国語の案内文の作成", 36, 25.25),
    ("与那国町", "yonaguni", "製造業", "食料品（島の農水産物の加工品の製造・島外への出荷）", {"農水産物加工", "食料品"}, 21,
     "島外の取引先・通販の問い合わせへの回答と、表示の文・商品案内の作成、出荷の記録の取りまとめ", 8, 41.75),
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
            print(f"  NG {city} の時間 {h} は5県の割り当て（×4 を5で割った余り {MOD_R}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 沖縄県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 沖縄県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは沖縄県の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 41 else "NG")


def free(ind, lo, hi):
    """余り4の時間で、既存の記事・他県の PLAN と時間も金額も重ならない候補を出す（PLAN の行を決める手がかり）"""
    used_h, used_m = used_values()
    mine_h = {Decimal(str(p[7])) * Decimal(str(p[8])) * Decimal("0.25") for p in PLAN}
    mine_m = {man(Decimal(str(p[7])) * Decimal(str(p[8])) * Decimal("0.25") * RATE[p[2]]) for p in PLAN}
    q = int(Decimal(str(lo)) * 4)
    out = []
    while Decimal(q) / 4 <= Decimal(str(hi)):
        if q % MOD_N == MOD_R:
            h = Decimal(q) / 4
            yen = h * RATE[ind]
            m = man(yen)
            if h not in used_h and m not in used_m and h not in mine_h and m not in mine_m and border_ok(yen):
                out.append(f"{h.normalize():f}h/{m}万")
        q += 1
    print(f"{ind}（約{RATE[ind]:,}円）{lo}〜{hi}時間の空き {len(out)}件:", " ".join(out))


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "free":
        free(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
        sys.exit()
    main()
