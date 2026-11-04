#!/usr/bin/env python3
"""鹿児島県43市町村の試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-11-04）。

data/area/okayama/_calc.py・data/area/saga/_calc.py・data/area/oita/_calc.py を元に作った。
県ページ（/area/kagoshima/）には試算を入れないので、PLAN は43行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **九州7県の取り決め**: 月の削減時間（0.25時間刻み）×4 を7で割った余りが 6（鹿児島県）の時間だけを使う
     （1.5, 3.25, 5.0, 6.75, … の1.75時間刻み。data/area/_kyushu/shared.md）
  1. 43ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、鹿児島県を除く）の「## 試算」の節に出てくる
     「◯時間」「◯万円」の値と重ならない。拾い方は岡山県・佐賀県の _calc.py と同じ（広めに拾う）
  3. 全県の data/area/*/_calc.py の PLAN（鹿児島県を除く。glob で全部読む）の月の削減時間・月の時間換算額と重ならない。
     他県の _calc.py は import で読み（佐賀・大分の書き方）、だめなら行頭の `PLAN = [` を文字列で切り出して読む。
     **読めないファイルは NG にせず警告**。九州以外の8県（REQUIRED）はファイルがなければ NG
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md（・cases2.md）・subsidy_a_areas.md の事例の会社と同じにならない（CASES と照合。岡山と同じ判定）
     - AI の事例で、業態のキーが重なり、従業員数が事例の範囲（下限×0.85〜上限×1.15）に入る → NG
     - AI の事例で、業態のキーが重なり、同じ市町村で、事例の従業員数が分からない → NG（その会社の値と読まれるため）
     - 業種が確かめられていない事例（キー「業種未確認」）と同じ市町村 → 参考として表示（NG にしない）
     - AI ではない事例と業態・規模が近い → 参考として表示
  6. slug が _brief.md の43市町村と一致する（鹿児島市 kagoshima-city、大崎町 osaki-town、瀬戸内町 setouchi-town、
     大和村 yamato-village、十島村 toshima-village、三島村 mishima-village）
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
  8. 県ページには試算を入れない（PLAN は43行）
使い方: python3 data/area/kagoshima/_calc.py   （末尾に OK / NG を出す）
九州の他県の PLAN は後から変わることがあるので、push の直前に git pull してもう一度実行する。
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
SELF = "kagoshima"
KYUSHU_MOD = 6  # 九州7県の割り当て（月の削減時間×4 を7で割った余り）。鹿児島県は 6

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
    # 市（19）
    "kagoshima-city", "kanoya", "makurazaki", "akune", "izumi", "ibusuki", "nishinoomote", "tarumizu",
    "satsumasendai", "hioki", "soo", "kirishima", "ichikikushikino", "minamisatsuma", "shibushi", "amami",
    "minamikyushu", "isa", "aira",
    # 町（20）
    "satsuma", "nagashima", "yusui", "osaki-town", "higashikushira", "kinko", "minamiosumi", "kimotsuki",
    "nakatane", "minamitane", "yakushima", "setouchi-town", "tatsugo", "kikai", "tokunoshima", "amagi", "isen",
    "wadomari", "china", "yoron",
    # 村（4）
    "mishima-village", "toshima-village", "yamato-village", "uken",
}

# 九州以外で照合が必須の県（2026-11-04 にある _calc.py）。ファイルがなければ NG
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi")

# cases.md・cases_outside.md・subsidy_a_areas.md（採択・交付決定の手がかり）の事例の会社（2026-11-04）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・交付決定・使用済み・目標を含む〕)
# cases2.md（2026-11-04 の補充調査）の会社も足した（「# cases2.md」の行）。cases2.md が更新されたら足して再実行する
CASES = [
    # 鹿児島市（cases.md）
    ("JA鹿児島県中央会（生成AIの実証の開始、ベンダーの発表）", "鹿児島市", {"農業団体", "協同組合"}, None, True),
    ("現場サポート（建設業向けソフト、生成AIでサポート、126名）", "鹿児島市", {"情報サービス", "ソフトウェア"}, (126, 126), True),
    ("フタマタ開発（AI の画像認識で産廃の選別、報道）", "鹿児島市", {"産業廃棄物処理", "廃棄物処理"}, None, True),
    ("ZIFISH（県の新事業創出の採択、水産業の AI）", "鹿児島市", {"情報サービス", "システム開発"}, None, True),
    ("システムビジョン（KISC 助成、AI のボトルチェッカ）", "鹿児島市", {"生産用機械", "検査装置"}, None, True),
    ("FineMetrics 鹿児島事業所（KISC 助成、特許の AI）", "鹿児島市", {"情報サービス", "知的財産"}, None, True),
    ("オービジョン（産直サイト、生成AIは検索の要約だけ、3名）", "鹿児島市", {"小売", "通販", "産地直送"}, (3, 3), True),
    ("GiFFT（社内向け ChatGPT の提供側、5名）", "鹿児島市", {"情報サービス"}, (5, 5), True),
    ("ドリームワンカゴシマ（子牛の AI の研究の参加企業）", "鹿児島市", {"情報サービス", "畜産システム"}, None, True),
    # 鹿児島市（subsidy_a_areas.md。県のDX推進補助金 1次の交付決定・ものづくり中核企業の採択。AI のテーマ。成果なし）
    ("HGM（DX補助 1次、AIクラウドERP）", "鹿児島市", {"宿泊", "飲食店", "飲食サービス"}, None, True),
    ("コスモコンサルタンツ（DX補助 1次、建設コンサル）", "鹿児島市", {"建設コンサルタント", "技術サービス"}, None, True),
    ("社会保険労務士法人HR Trust（DX補助 1次、生成AIのナレッジ共有）", "鹿児島市", {"社会保険労務士", "士業"}, None, True),
    ("ノーティス（DX補助 1次、産業カウンセリングの記録）", "鹿児島市", {"産業カウンセリング", "専門サービス"}, None, True),
    ("はなふさ社労士事務所（DX補助 1次、Gemini API）", "鹿児島市", {"社会保険労務士", "士業"}, None, True),
    ("ビッグファイブ（DX補助 1次、食品製造の AI 帳票）", "鹿児島市", {"食料品", "食品製造"}, None, True),
    ("宮崎施設機械（DX補助 1次、建設業のバックオフィス）", "鹿児島市", {"建設", "設備工事"}, None, True),
    ("リバース（DX補助 1次、卸売業・小売業、保育現場の AI 人事考課）", "鹿児島市", {"卸売", "小売", "保育"}, None, True),
    ("さつま無双（ものづくり中核企業、出荷の AI。焼酎）", "鹿児島市", {"酒類製造", "焼酎", "飲料"}, None, True),
    ("Miami（ものづくり中核企業、AI 在庫・生産管理。食料品）", "鹿児島市", {"食料品", "食品製造"}, None, True),
    # 霧島市
    ("キリシマ精工（AI の生産スケジューラー・DX補助の類似図面検索、53名）", "霧島市", {"金属加工", "精密加工", "金属製品"}, (53, 53), True),
    ("インタッチサポート（DX補助 1次、広告案件管理）", "霧島市", {"卸売", "小売", "広告"}, None, True),
    ("霧島第一牧場（子牛の AI 実証、愛媛県西予市で使用済み）", "霧島市", {"農業", "肉用牛", "畜産"}, None, True),
    # 志布志市
    ("鹿児島堀口製茶（AI の葉期判定、国の実証。茶 270ha）", "志布志市", {"茶", "製茶", "農業"}, None, True),
    ("Farmers Villa Ume（DX補助 1次、ピーマンの営農AI）", "志布志市", {"農業", "ピーマン"}, None, True),
    # 曽於市・大崎町
    ("鹿児島大学ほか 子牛の疾病予兆 AI（目標、だいち）", "曽於市", {"農業", "肉用牛", "畜産"}, None, True),
    ("Eco-Pork（東京の会社、曽於市に拠点。AI 豚カメラの提供側）", "曽於市", {"養豚", "畜産", "情報サービス"}, None, True),
    ("イケシタ電工（DX補助 1次、AI 施工管理）", "曽於市", {"建設", "電気工事"}, None, True),
    ("ジャパンファーム（AI 豚カメラ、ベンダーの発表）", "大崎町", {"養豚", "農業", "畜産"}, None, True),
    # 枕崎市・鹿屋市（使用済み）・いちき串木野市・南さつま市・出水市・姶良市・湧水町・伊佐市・肝付町・日置市・長島町
    ("薩摩酒造（原料芋の選別 AI の実証・AI-OCR の採択、226名。長野県伊那市で使用済み）", "枕崎市",
     {"酒類製造", "焼酎", "飲料"}, (192, 226), True),
    ("うしの中山（ローカル5G・AI カメラ、青森県七戸町で使用済み）", "鹿屋市", {"農業", "肉用牛", "畜産"}, None, True),
    ("東一誠税理士事務所（DX補助 1次、会計システムの AI 機能）", "鹿屋市", {"税理士", "士業"}, None, True),
    ("濵田酒造（ものづくり中核企業、AI の RAG。焼酎）", "いちき串木野市", {"酒類製造", "焼酎", "飲料"}, None, True),
    ("コワダヤ（ものづくり中核企業、バーコード読み取りの AI。食料品）", "南さつま市", {"食料品", "食品製造"}, None, True),
    ("エルム（LED 照明、AI は今後の予定）", "南さつま市", {"電気機械", "照明"}, None, False),
    ("田頭建設（DX補助 1次、自社専用 AI ツール）", "出水市", {"建設", "総合工事業"}, None, True),
    ("加治木産業（DX補助 1次、スキャナと AI。製造業、中分類は未確認）", "姶良市", {"業種未確認"}, None, True),
    ("In Touch Network（DX補助 1次、広告案件管理）", "湧水町", {"広告", "専門サービス"}, None, True),
    ("Farm-K（DX補助 1次、AI 搭載の会計・販売管理。農業）", "伊佐市", {"農業"}, None, True),
    ("山佐木材（DX補助 1次、AI 画像センサの目視検査の自動化）", "肝付町", {"木材・木製品", "製材", "集成材"}, None, True),
    ("fab（KISC の起業支援、AI 感情分析の SaaS）", "日置市", {"情報サービス", "ソフトウェア"}, None, True),
    ("獅子丸水産（AI の自動給餌機、岩手県宮古市で使用済み）", "長島町", {"養殖", "水産養殖", "マダイ"}, None, True),
    ("日本計器鹿児島製作所（茶園の防霜散水の確認システム、AI ではない）", "南九州市", {"電気機械", "計測機器"}, None, False),
    ("三島村肉用牛生産組合（畜産ネットシステム、AI ではない）", "三島村", {"農業", "肉用牛", "畜産"}, None, False),
    # 所在未確認
    ("轟木税理士事務所（AI の自動仕訳、入力作業 50%減・自己申告、2名。南九州市川辺町の事務所とみられる）", "所在未確認",
     {"税理士", "士業"}, (2, 2), True),
    ("ポテトかいつか（さつまいもの AI 選別ライン、所在・規模未確認）", "所在未確認", {"さつまいも", "青果"}, None, True),
    # cases2.md（2026-11-04）
    ("ARS（ドクターカーの AI 音声記録の PoC、IT 企業）", "鹿児島市", {"情報サービス", "ソフトウェア"}, None, True),
    ("七徳会 大井病院（ARS の PoC の協力、救急医療）", "姶良市", {"医療", "病院"}, None, True),
    ("ファーマーズサポート（畜産の AI カメラのサブスク、提供側、3名）", "鹿児島市", {"情報サービス", "畜産システム"}, (3, 3), True),
    ("中野ファーム（AI 検知式の分娩監視カメラ、繁殖牛）", "肝付町", {"農業", "肉用牛", "畜産"}, None, True),
    ("さつま町の繁殖牛農家（AI カメラの発情・分娩通知、3名）", "さつま町", {"農業", "肉用牛", "畜産"}, (3, 3), True),
    ("ア・トスフーズ（AI のツールで営業の進捗管理、食品加工、102名）", "薩摩川内市", {"食料品", "食品加工"}, (102, 102), True),
    ("CANFORA COMPANI（ChatGPT でメール作成、情報サービス、5名）", "薩摩川内市", {"情報サービス"}, (5, 5), True),
    ("薩摩中華 こたろう（Gemini で SNS の案、飲食店、16名）", "薩摩川内市", {"飲食店", "飲食サービス"}, (16, 16), True),
    ("にしやま食品（Gemini でキャッチコピー、仕出し・飲食店、5名）", "薩摩川内市", {"仕出し", "飲食店", "食料品"}, (5, 5), True),
    ("Village AI（AI 人材育成の会社、導入事例ではない）", "中種子町", {"情報サービス", "研修"}, None, True),
    ("Core-Support（畜産の遠隔監視カメラ、AI ではない）", "伊仙町", {"情報サービス", "畜産システム"}, None, False),
    ("鹿児島市 小規模事業者ICT導入促進支援事業のアンケート（9事業者、AI ではない）", "鹿児島市", {"業種未確認"}, None, False),
    ("薩摩川内市の事例集の残り8社（AI ではない）", "薩摩川内市", {"業種未確認"}, None, False),
    # cases_outside.md（県外。九州以外）
    ("かわに（石川県金沢市、さつまいもの形の AI 判別、2018年度）", "県外", {"農業", "さつまいも"}, None, True),
    ("サイトー電子（岐阜県、検査員の眠気検知 AI、予備）", "県外", {"電子部品", "検査"}, None, True),
    ("有川組・神野商事・城山観光ほか（県の DX 事例集、AI の記載なし）", "所在未確認", {"建設", "卸売", "宿泊"}, None, False),
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種・業態は stats.md の「市町村ごとの主要産業の候補」の (B) 中小企業の業種（経済センサスの事業所数・従業者数）から選んだ。
# 霧島市の電子部品（16所・7,169人）、薩摩川内市の窯業・土石（21所・4,728人）、志布志市の飲料・たばこ・飼料（出荷額の70.2%）、
# 伊佐市・いちき串木野市の非鉄金属（1所）、南種子町の技術サービス業・輸送用機械（1所）、湧水町の電子部品（3所）など、
# 大企業の工場・特定の施設と読める中分類は試算の業種にしない。農業・漁業・林業も試算の業種にしない
# （畜産・茶・さとうきびの町村は食料品製造〔食肉・鶏卵・製茶・でん粉・農産加工〕・卸売〔集出荷〕などにした）。
# 2026-11-04: 既存の地域ページ（試算の節がある約690本）と13県の PLAN で埋まっていない値を探して決めた。
PLAN = [
    # 鹿児島地域振興局（5）
    ("鹿児島市", "kagoshima-city", "医療・福祉", "病院（急性期の一般病床と外来）", {"医療", "病院"}, 260,
     "退院時サマリー・診療情報提供書の下書きと、患者・家族への説明文書、院内の委員会の議事録の作成", 39, 33.0),
    ("日置市", "hioki", "医療・福祉", "特別養護老人ホーム（短期入所を併設）", {"介護", "特別養護老人ホーム"}, 78,
     "ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成", 22, 41.0),
    ("いちき串木野市", "ichikikushikino", "製造業", "食料品（水産練り製品の製造）", {"食料品", "水産加工", "水産練り製品"}, 140,
     "量販店・土産物店の取引先からの規格・原材料・賞味期限の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ", 36, 30.5),
    ("三島村", "mishima-village", "卸売業・小売業", "食料品・日用品の小売店（船便で仕入れ）", {"小売", "食料品小売", "日用品"}, 28,
     "仕入先への発注・欠品の連絡と、船便の入荷の記録、島内の客からの注文の取りまとめ", 12, 26.75),
    ("十島村", "toshima-village", "宿泊・飲食サービス業", "民宿（食事の提供を含む）", {"宿泊", "民宿"}, 32,
     "予約の電話・メールの問い合わせへの返信の下書きと、船便の運航に合わせた予約の変更の連絡、宿泊者の記録の整理", 12, 40.75),
    # 南薩地域振興局（4）
    ("枕崎市", "makurazaki", "製造業", "食料品（水産加工品の製造）", {"食料品", "水産加工"}, 150,
     "問屋・食品メーカーの取引先からの規格・産地・ロットの問い合わせへの回答と、規格書・検査成績書の作成、製造記録の取りまとめ", 34, 32.5),
    ("指宿市", "ibusuki", "宿泊・飲食サービス業", "温泉ホテル（宴会・団体の受け入れを含む）", {"宿泊", "温泉ホテル"}, 135,
     "予約サイト・メールの問い合わせへの返信の下書きと、団体・宴会の見積書、館内案内の多言語の文の作成", 30, 38.0),
    ("南さつま市", "minamisatsuma", "医療・福祉", "介護老人保健施設（通所リハビリを併設）", {"介護", "介護老人保健施設"}, 100,
     "リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成", 29, 34.0),
    ("南九州市", "minamikyushu", "製造業", "飲料（荒茶の仕上げ加工・製茶と茶の販売）", {"飲料", "製茶", "茶"}, 92,
     "茶商・小売の取引先からの在庫・品質・納期の問い合わせへの回答と、商品の説明・表示の文、製造・出荷の記録の取りまとめ", 25, 40.0),
    # 北薩地域振興局（5）
    ("阿久根市", "akune", "製造業", "食料品（惣菜・調理冷凍食品の製造）", {"食料品", "惣菜", "冷凍食品"}, 85,
     "量販店・外食の取引先からの規格・アレルゲンの問い合わせへの回答と、規格書の改訂、衛生管理の記録の取りまとめ", 24, 37.0),
    ("出水市", "izumi", "製造業", "食料品（鶏卵の選別・包装と加工卵の製造）", {"食料品", "鶏卵加工"}, 160,
     "量販店・食品メーカーの取引先からの数量・規格の問い合わせへの回答と、出荷の記録・衛生管理の記録の取りまとめ", 32, 36.5),
    ("薩摩川内市", "satsumasendai", "建設業", "総合工事業（土木・建築、公共工事が中心）", {"建設", "総合工事業", "土木"}, 115,
     "公共工事の施工計画書・提出書類の作成と、工事写真・出来形の記録の整理、発注者との打合せ記録の要約", 26, 39.0),
    ("さつま町", "satsuma", "製造業", "電気機械（電装部品・制御盤の組立）", {"電気機械", "制御盤", "電装部品"}, 95,
     "取引先からの部品の切り替え・納期の問い合わせへの回答と、作業手順書・検査記録の取りまとめ", 30, 31.0),
    ("長島町", "nagashima", "製造業", "食料品（養殖魚の加工〔フィレ・冷凍〕と出荷）", {"食料品", "水産加工"}, 68,
     "量販店・飲食店の取引先からの数量・規格・出荷日の問い合わせへの回答と、出荷・ロットの記録、衛生管理の記録の取りまとめ", 23, 31.0),
    # 姶良・伊佐地域振興局（4）
    ("霧島市", "kirishima", "製造業", "生産用機械（半導体・電子部品の製造装置の部品・治具の設計製作）", {"生産用機械", "製造装置", "治具"}, 190,
     "顧客（工場）との仕様の打合せ記録の要約と、見積書・取扱説明書・設計変更の連絡書の下書き", 32, 40.0),
    ("伊佐市", "isa", "卸売業・小売業", "米穀の集荷・精米・卸売", {"卸売", "米穀卸"}, 75,
     "米穀店・飲食店・量販店の取引先からの在庫・品種・価格の問い合わせへの回答と、出荷伝票・精算書の取りまとめ", 27, 29.0),
    ("姶良市", "aira", "運輸業・郵便業", "道路貨物運送（県内の地場配送・中距離輸送）", {"運送", "道路貨物運送"}, 170,
     "配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計", 34, 36.0),
    ("湧水町", "yusui", "医療・福祉", "認知症対応型グループホームと小規模多機能型居宅介護", {"介護", "グループホーム", "小規模多機能"}, 70,
     "生活記録の清書と、運営推進会議の議事録、家族への便りの文の作成", 24, 31.75),
    # 大隅地域振興局（9）
    ("鹿屋市", "kanoya", "製造業", "食料品（牛肉・豚肉の部分肉の加工と出荷）", {"食料品", "食肉加工"}, 200,
     "量販店・外食の取引先からの部位・規格・数量の問い合わせへの回答と、規格書の改訂、トレーサビリティ・衛生管理の記録の取りまとめ", 38, 33.5),
    ("垂水市", "tarumizu", "製造業", "食料品（鶏肉の処理・加工）", {"食料品", "食鳥処理", "鶏肉加工"}, 155,
     "量販店・食品メーカーの取引先からの規格・数量・納期の問い合わせへの回答と、出荷の記録・衛生管理の記録の取りまとめ", 31, 37.0),
    ("曽於市", "soo", "製造業", "食料品（豚肉の加工品〔ハム・ソーセージ〕の製造）", {"食料品", "食肉加工品", "ハム・ソーセージ"}, 125,
     "通販・小売の取引先に出す商品説明・表示の文の作成と、ギフトの受注・出荷の記録、製造記録の取りまとめ", 30, 34.5),
    ("志布志市", "shibushi", "運輸業・郵便業", "港湾運送・倉庫（飼料原料などの荷役・保管とトラック輸送）", {"港湾運送", "倉庫", "運送"}, 120,
     "荷主からの入出庫・在庫・配送の問い合わせへの回答と、作業実績の報告書・作業手順書の取りまとめ", 32, 29.5),
    ("大崎町", "osaki-town", "卸売業・小売業", "農産物（野菜・さつまいも）の集出荷・卸売", {"卸売", "農産物の集出荷"}, 72,
     "市場・量販店・加工業者の取引先からの入荷・規格・価格の問い合わせへの回答と、出荷の伝票・精算書の取りまとめ", 24, 35.25),
    ("東串良町", "higashikushira", "製造業", "食料品（野菜の一次加工〔カット野菜・冷凍野菜〕）", {"食料品", "野菜加工", "カット野菜"}, 60,
     "外食・給食の取引先からの規格・産地・数量の問い合わせへの回答と、規格書・製造記録の取りまとめ", 20, 37.75),
    ("錦江町", "kinko", "医療・福祉", "訪問介護と居宅介護支援の事業所", {"介護", "訪問介護", "居宅介護支援"}, 64,
     "訪問の記録の清書と、サービス担当者会議の記録、ケアプランの文案の下書き", 22, 44.5),
    ("南大隅町", "minamiosumi", "医療・福祉", "通所介護（デイサービス、送迎を含む）", {"介護", "通所介護"}, 66,
     "利用の記録と個別機能訓練計画書の下書き、家族への連絡帳の文の作成", 11, 47.0),
    ("肝付町", "kimotsuki", "建設業", "総合工事業（土木・林道・農業土木）", {"建設", "総合工事業", "土木"}, 47,
     "工事日報・安全書類の取りまとめと、発注者への工程の連絡文、出来形の記録の整理", 16, 43.25),
    # 熊毛支庁（4）
    ("西之表市", "nishinoomote", "建設業", "総合工事業（建築・土木、島内の公共工事と住宅）", {"建設", "総合工事業"}, 63,
     "施工計画書・提出書類の作成と、資材の船便の手配の連絡、工事写真の整理", 20, 43.0),
    ("中種子町", "nakatane", "製造業", "食料品（さつまいもの加工品・でん粉の製造）", {"食料品", "でん粉", "農産加工"}, 62,
     "取引先からの規格・数量・出荷日の問い合わせへの回答と、原料の受け入れ・製造の記録の取りまとめ", 22, 30.5),
    ("南種子町", "minamitane", "宿泊・飲食サービス業", "ホテル・民宿（食事の提供を含む）", {"宿泊", "ホテル"}, 45,
     "予約の問い合わせへの返信の下書きと、長期滞在・団体の見積書、宿泊者の記録の整理", 16, 32.75),
    ("屋久島町", "yakushima", "宿泊・飲食サービス業", "ホテル・旅館（ガイド・送迎の手配を含む）", {"宿泊", "ホテル", "旅館"}, 90,
     "予約サイト・メールの問い合わせへの返信の下書きと、ガイド・送迎の手配の連絡、館内案内の多言語の文の作成", 26, 35.5),
    # 大島支庁（12）
    ("奄美市", "amami", "卸売業・小売業", "飲食料品・日用品の卸売（群島内の小売店・飲食店へ納品）", {"卸売", "飲食料品卸"}, 110,
     "小売店・飲食店からの受注・欠品・入荷予定の問い合わせへの回答と、船便の入荷に合わせた納品の連絡、商品の案内文の作成", 27, 36.0),
    ("大和村", "yamato-village", "建設業", "総合工事業（土木・道路の工事）", {"建設", "総合工事業", "土木"}, 34,
     "工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理", 10, 47.5),
    ("宇検村", "uken", "医療・福祉", "障害福祉サービス（生活介護・就労継続支援）", {"障害福祉", "生活介護", "就労継続支援"}, 52,
     "支援記録の清書と、個別支援計画の下書き、家族・相談支援専門員への報告書の作成", 20, 27.25),
    ("瀬戸内町", "setouchi-town", "建設業", "総合工事業（港湾・道路の土木工事）", {"建設", "総合工事業", "土木", "港湾"}, 56,
     "施工計画書・提出書類の作成と、資材・作業船の手配の連絡、出来形の記録の整理", 20, 32.5),
    ("龍郷町", "tatsugo", "宿泊・飲食サービス業", "リゾートホテル（レストランを含む）", {"宿泊", "ホテル", "リゾートホテル"}, 58,
     "予約サイト・メールの問い合わせへの返信の下書きと、体験・送迎の手配の連絡、館内案内の多言語の文の作成", 20, 34.25),
    ("喜界町", "kikai", "製造業", "食料品（さとうきびなど農産物の加工品の製造）", {"食料品", "農産加工"}, 44,
     "通販・土産物店の取引先からの注文・賞味期限・原材料の問い合わせへの回答と、商品の表示の文、製造記録の取りまとめ", 20, 39.5),
    ("徳之島町", "tokunoshima", "医療・福祉", "病院（一般病床・療養病床と外来）", {"医療", "病院"}, 80,
     "紹介状・診療情報提供書の下書きと、患者・家族への説明文、本土の医療機関への転院の連絡文の作成", 23, 38.0),
    ("天城町", "amagi", "卸売業・小売業", "小売（農業資材・建築資材・日用品）", {"小売", "農業資材", "建築資材"}, 50,
     "客からの取り寄せ・在庫の問い合わせへの回答と、仕入先への発注・船便の入荷の連絡、売場の案内文の作成", 18, 33.0),
    ("伊仙町", "isen", "建設業", "総合工事業（農業土木・道路の工事）", {"建設", "総合工事業", "土木"}, 54,
     "工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理", 18, 36.5),
    ("和泊町", "wadomari", "卸売業・小売業", "花き・ばれいしょの集出荷（本土の市場への出荷手配）", {"卸売", "花き", "農産物の集出荷"}, 46,
     "市場・仲卸からの入荷・規格・価格の問い合わせへの回答と、船便・航空便の出荷手配の連絡、出荷の伝票の取りまとめ", 16, 39.75),
    ("知名町", "china", "医療・福祉", "訪問看護ステーション（訪問リハビリを含む）", {"医療", "訪問看護"}, 55,
     "訪問看護の記録の清書と、主治医への報告書・計画書の下書き、家族への連絡文の作成", 19, 39.0),
    ("与論町", "yoron", "宿泊・飲食サービス業", "ホテル（マリンレジャーの手配を含む）", {"宿泊", "ホテル"}, 48,
     "予約サイト・メールの問い合わせへの返信の下書きと、航空便・船便の欠航時の予約変更の連絡、館内案内の多言語の文の作成", 16, 36.25),
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
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | 年間 | ×4 を7で割った余り |")
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
                print(f"  NG 鹿児島県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 鹿児島県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは鹿児島県の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 43 else "NG")


if __name__ == "__main__":
    main()
