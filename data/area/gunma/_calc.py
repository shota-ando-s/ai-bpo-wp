#!/usr/bin/env python3
"""群馬県35市町村の試算の割り当てを計算し、重なりを確かめる（2026-11-05）。

data/area/kagoshima/_calc.py を元に作った。県ページ（/area/gunma/）には試算を入れないので、PLAN は35行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **北海道・北関東3県・沖縄の取り決め**: 月の削減時間（0.25時間刻み）×4 を5で割った余りが 3（群馬県）の時間だけを使う
     （0.75, 2.0, 3.25, 4.5, … の1.25時間刻み。data/area/_batch5/shared.md）
  1. 35ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、群馬県を除く）の「## 試算」の節の「◯時間」「◯万円」と重ならない
  3. 全県の data/area/*/_calc.py の PLAN（群馬県を除く。glob で全部読む）の月の削減時間・月の時間換算額と重ならない。
     読めないファイルは警告。REQUIRED の県はファイルがなければ NG。金額が茨城・栃木・北海道・沖縄と重なったら、先に push した県を優先する
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md の事例の会社と同じにならない（CASES と照合。鹿児島と同じ判定）
  6. slug が _brief.md の35市町村と一致する
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
使い方: python3 data/area/gunma/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/gunma/_calc.py free <業種> <最小時間> <最大時間>   （空いている時間と金額を並べる）
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
SELF = "gunma"
KYUSHU_MOD = 3  # 5県の割り当て（月の削減時間×4 を5で割った余り）。群馬県は 3
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
    # 市（12）
    "maebashi", "takasaki", "kiryu", "isesaki", "ota", "numata", "tatebayashi", "shibukawa", "fujioka", "tomioka",
    "annaka", "midori",
    # 町（15）
    "yoshioka", "kanna", "shimonita", "kanra", "nakanojo", "naganohara", "kusatsu", "higashiagatsuma", "minakami",
    "tamamura", "itakura", "meiwa", "chiyoda", "oizumi", "ora",
    # 村（8）
    "shinto", "ueno-village", "nanmoku", "tsumagoi", "takayama-village-gunma", "katashina", "kawaba", "showa-village-gunma",
}

# 九州以外で照合が必須の県（2026-11-04 にある _calc.py）。ファイルがなければ NG
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "kagoshima", "kumamoto", "miyazaki", "nagasaki", "oita", "saga")

# cases.md・cases_outside.md・subsidy_a_areas.md（採択・交付決定の手がかり）の事例の会社（2026-11-04）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・交付決定・使用済み・目標を含む〕)
# cases2.md（2026-11-04 の補充調査）の会社も足した（「# cases2.md」の行）。cases2.md が更新されたら足して再実行する
CASES = [
    # cases.md（2026-11-05）
    ("栄工業（ChatGPT で樹脂欠品の監視の試作、金属部品の塗装・組立）", "太田市", {"塗装", "金属部品の塗装", "組立"}, None, True),
    ("澤藤電機（生成AIツールを200名に展開、854名。90%削減は AI ではない）", "太田市", {"電気機械", "電装品", "発電機"}, (854, 854), True),
    ("糸井商会（ぐんまDX技術革新補助金の採択、LLM で技能ギャップ）", "太田市", {"業種未確認"}, None, True),
    ("サイテックス（透明樹脂の AI 外観検査、岐阜県恵那市で使用済み）", "太田市", {"プラスチック製品", "精密プラスチック成形"}, None, True),
    ("日本発条 群馬工場（シートのシワの AI 検出、大企業の工場）", "太田市", {"輸送用機械", "自動車用シート"}, None, True),
    ("石川建設（AI クラウド工程管理の導入、ベンダーの発表）", "太田市", {"建設", "総合工事業"}, None, True),
    ("大西ライト工業所（生成AIで RFID の記録システム、射出成形。本店は桐生市）", "桐生市", {"プラスチック製品", "射出成形", "精密成形"}, None, True),
    ("中一陸運（ぐんまDX技術革新補助金の採択、AI-OCR、運送）", "伊勢崎市", {"運輸", "道路貨物運送", "運送"}, None, True),
    ("高柳エンジニアリング（AI付OCR、製造設備・治具、14人）", "伊勢崎市", {"生産用機械", "治具"}, (10, 14), True),
    ("藤田デバイス（生成AIで事前調査、ダイシング・画像検査装置、100名）", "高崎市", {"電子部品", "半導体", "検査装置"}, (100, 100), True),
    ("Calm Living Design（AI 文字起こし・AI 電子カルテ、訪問看護、13人）", "高崎市", {"医療", "訪問看護"}, (13, 13), True),
    ("トキオエンジニアリング（段ボールの AI 外観検査装置の共同研究）", "高崎市", {"生産用機械", "生産設備"}, None, True),
    ("内外（鋳造欠陥の AI 判定、アルミ鋳造）", "高崎市", {"金属製品", "鋳造", "非鉄金属"}, None, True),
    ("FUTURENAUT（コオロギ養殖の AI、採択）", "高崎市", {"養殖", "食料品"}, None, True),
    ("スタジオ・スイロ（LLM で Web 制作サービス、提供側）", "高崎市", {"Web制作", "情報サービス"}, None, True),
    ("群馬大学医学部附属病院（生成AIで説明同意文書のチェック）", "前橋市", {"医療", "病院"}, None, True),
    ("大道産業（AI 異物検査装置、食品加工機械、岐阜県安八町で使用済み）", "前橋市", {"生産用機械", "食品加工機械"}, None, True),
    ("数理設計研究所（エッジAIの衛星、採択、提供側）", "前橋市", {"宇宙機器", "AI製品開発"}, None, True),
    ("C&T（AI 通訳の Web ソリューション、採択、提供側）", "前橋市", {"AI製品開発", "通訳"}, None, True),
    ("スズキワーパー（AI 織物検査装置の試作、整経機メーカー）", "桐生市", {"生産用機械", "織物準備機械"}, None, True),
    ("ヒロイ（溶接の AI 検査、バッテリーパック、岐阜県可児市で使用済み）", "安中市", {"電気機械", "バッテリーパック"}, None, True),
    ("LUC（倉庫の仕組みに AI を使う計画、電池加工・運送）", "安中市", {"電気機械", "運輸"}, None, False),
    ("エルグ（生成AIで社内システムを内製、精密めっき、65名）", "富岡市", {"めっき", "表面処理", "金属製品"}, (65, 65), True),
    ("野口製作所（AI のプレス部品の自動検査装置、採択）", "富岡市", {"金属製品", "プレス", "精密プレス部品"}, None, True),
    ("倉沢製作所（AI カメラのプラスチック製品の良否判定、採択）", "藤岡市", {"プラスチック製品", "射出成形"}, None, True),
    ("太陽誘電 玉村工場（深層学習の画像検査、大企業の工場）", "玉村町", {"電子部品", "コンデンサ"}, None, True),
    ("内田病院（OPTiM AI ホスピタル、山形県庄内町で使用済み）", "沼田市", {"医療", "病院"}, None, True),
    ("雪ほたか（AI チャットの試験運用、米のブランド管理・販売、10人）", "川場村", {"米穀卸", "農産物販売"}, (10, 10), True),
    ("山崎酒造（AI 杜氏、採択。所在は subsidy・cases で確かめる）", "所在未確認", {"酒類製造", "飲料"}, None, True),
    ("キュウリの自動収穫ロボットの実証（県・JA全農ぐんま）", "所在未確認", {"農業", "きゅうり"}, None, True),
    # cases2.md（2026-11-06）
    ("協和（みどり市、板金。見積作成30〜70%短縮・文書作成2〜3倍速、県のリスキリングかわら版の発表の要約）", "みどり市", {"金属製品", "板金"}, None, True),
    ("アイ・リンクホールディングス（桐生市、運送。議事録に生成AI、数値なし）", "桐生市", {"運輸", "道路貨物運送"}, None, True),
    ("前橋橋本合金（GPU のシミュレーション、AI ではない）", "前橋市", {"非鉄金属", "鋳造"}, None, False),
    ("ヒザワ種苗（FAX の自動振り分け、AI の記載なし）", "前橋市", {"種苗", "卸売"}, None, False),
    ("千代田製作所（AI ではない）", "太田市", {"業種未確認"}, None, False),
    # cases_outside.md（県外）
    ("アスカカンパニー（兵庫県加東市、射出成形 約250名、AIカメラを含む全数検査）", "県外", {"プラスチック製品", "射出成形"}, (250, 250), True),
    ("タマプリント（東京都青梅市、印刷）", "県外", {"印刷", "商業印刷"}, None, True),
    ("ライフタイムサポート（埼玉県越谷市、内装・リフォーム 32名）", "県外", {"建設", "内装工事", "リフォーム"}, (32, 32), True),
    ("カネク（東京都青梅市、食料品 156名、AI 以外と合算）", "県外", {"食料品"}, (156, 156), True),
    ("比企オプティクス（埼玉県秩父市、合算）", "県外", {"光学機器", "業務用機械"}, None, True),
    ("伊田テクノス（埼玉県東松山市、建設、合算）", "県外", {"建設", "総合工事業"}, None, True),
    ("ニッシン・パーテクチュアル（埼玉県春日部市、金属加工、合算）", "県外", {"金属製品", "精密加工"}, None, True),
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種・業態は stats.md の「市町村ごとの主要産業の候補」の (B) 中小企業の業種（経済センサスの事業所数・従業者数）から選んだ。
# 霧島市の電子部品（16所・7,169人）、薩摩川内市の窯業・土石（21所・4,728人）、志布志市の飲料・たばこ・飼料（出荷額の70.2%）、
# 伊佐市・いちき串木野市の非鉄金属（1所）、南種子町の技術サービス業・輸送用機械（1所）、湧水町の電子部品（3所）など、
# 大企業の工場・特定の施設と読める中分類は試算の業種にしない。農業・漁業・林業も試算の業種にしない
# （畜産・茶・さとうきびの町村は食料品製造〔食肉・鶏卵・製茶・でん粉・農産加工〕・卸売〔集出荷〕などにした）。
# 2026-11-04: 既存の地域ページ（試算の節がある約690本）と13県の PLAN で埋まっていない値を探して決めた。
# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種は stats.md の「市町村ごとの主要産業の候補」の中小企業の業種から選んだ。輸送用機械の完成車・大企業の工場と読める業態、農林業は試算の業種にしない。
# 2026-11-05: 既存の地域ページと15県の PLAN で埋まっていない値を、規模の小さい順に小さい値から当てた（scratchpad の assign2.py）。
PLAN = [
    ('前橋市', 'maebashi', '情報通信業', 'ソフトウェア業（業務システムの受託開発・保守）', {'ソフトウェア受託開発', '業務システム'}, 85,
     '顧客からの問い合わせ・障害連絡への一次回答の下書きと、要件定義の打合せ記録の要約、仕様書・提案書の下書き', 24, 29.5),
    ('高崎市', 'takasaki', '学術研究・専門技術サービス', '建設コンサルタント・測量（公共の調査・設計）', {'測量', '建設コンサルタント'}, 95,
     '発注者との協議記録の要約と、調査・設計の報告書の下書き、提出書類の点検', 32, 32.75),
    ('桐生市', 'kiryu', '製造業', '繊維（織物の製造と整理加工）', {'織物', '繊維'}, 48,
     'アパレル・問屋の取引先からの納期・在庫・品質の問い合わせへの回答と、生地の仕様書・見本の説明文、生産の記録の取りまとめ', 32, 26.5),
    ('伊勢崎市', 'isesaki', '卸売業・小売業', '機械器具・工具の卸（工場向けの部品・消耗品）', {'機械器具卸', '卸売', '工具'}, 88,
     '工場の取引先からの在庫・納期・代替品の問い合わせへの回答と、見積書・発注書の作成、メーカーへの照会文の下書き', 26, 38.0),
    ('太田市', 'ota', '製造業', '金属製品（自動車部品のプレス加工・溶接）', {'溶接', '金属製品', 'プレス加工'}, 96,
     '取引先からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録・不具合の報告書の取りまとめ', 29, 37.0),
    ('沼田市', 'numata', '製造業', '木材・木製品（製材とプレカット）', {'プレカット', '製材', '木材・木製品'}, 44,
     '工務店からの見積・納期・加工の問い合わせへの回答と、プレカットの加工図の確認の連絡、出荷の記録の取りまとめ', 26, 30.5),
    ('館林市', 'tatebayashi', '製造業', '食料品（乾麺・製麺）', {'食料品', '製麺'}, 125,
     '量販店・問屋の取引先からの規格・原材料・アレルゲンの問い合わせへの回答と、規格書の改訂、製造・衛生管理の記録の取りまとめ', 32, 35.25),
    ('渋川市', 'shibukawa', '宿泊・飲食サービス業', '温泉旅館（宴会・団体の受け入れを含む）', {'温泉旅館', '宿泊'}, 110,
     '予約サイト・メールの問い合わせへの返信の下書きと、団体・宴会の見積書、館内案内の多言語の文の作成', 48, 22.25),
    ('藤岡市', 'fujioka', '建設業', '総合工事業（土木・舗装、公共工事が中心）', {'総合工事業', '土木', '建設'}, 62,
     '公共工事の施工計画書・提出書類の作成と、工事写真の整理、発注者との打合せ記録の要約', 24, 38.25),
    ('富岡市', 'tomioka', '製造業', '輸送用機械（自動車部品の切削加工）', {'自動車部品', '切削', '輸送用機械'}, 128,
     '取引先からの図面・仕様・納期の問い合わせへの回答と、工程の変更の連絡書、検査成績書・不具合報告の取りまとめ', 26, 43.0),
    ('安中市', 'annaka', '医療・福祉', '特別養護老人ホーム（短期入所を併設）', {'介護', '特別養護老人ホーム'}, 82,
     'ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成', 28, 37.25),
    ('みどり市', 'midori', '製造業', '業務用機械（計測機器の部品の加工・組立）', {'計測機器', '業務用機械'}, 74,
     '取引先からの仕様・納期の問い合わせへの回答と、組立の手順書・検査記録の取りまとめ、部品メーカーへの照会文', 34, 29.5),
    ('榛東村', 'shinto', '製造業', '食料品（洋菓子・焼き菓子の製造）', {'食料品', '菓子'}, 38,
     '小売店・通販の取引先からの原材料・賞味期限・アレルゲンの問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ', 24, 25.75),
    ('吉岡町', 'yoshioka', '卸売業・小売業', '小売（食料品・日用品のスーパー）', {'スーパー', '食料品小売', '小売'}, 56,
     '仕入先への発注・欠品の連絡と、売場の案内・チラシの文の下書き、客からの取り寄せ・問い合わせへの回答', 22, 39.0),
    ('上野村', 'ueno-village', '医療・福祉', '介護（デイサービスと訪問介護）', {'通所介護', '訪問介護', '介護'}, 26,
     '介護記録の清書と、ケアマネジャーへの報告書、家族への連絡文の作成', 16, 31.75),
    ('神流町', 'kanna', '建設業', '総合工事業（道路・治山の工事）', {'総合工事業', '土木', '建設'}, 39,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理', 24, 28.25),
    ('下仁田町', 'shimonita', '製造業', '食料品（こんにゃく製品の製造）', {'食料品', 'こんにゃく'}, 52,
     '量販店・問屋の取引先からの規格・賞味期限・数量の問い合わせへの回答と、商品の表示の文、製造・出荷の記録の取りまとめ', 36, 24.25),
    ('南牧村', 'nanmoku', '医療・福祉', '介護（特別養護老人ホーム・小規模）', {'介護', '特別養護老人ホーム'}, 31,
     '介護記録・事故報告の清書と、家族への近況の連絡文、職員の研修記録の作成', 12, 44.0),
    ('甘楽町', 'kanra', '製造業', '食料品（漬物・惣菜の製造）', {'漬物', '食料品', '惣菜'}, 66,
     '量販店・土産物店の取引先からの規格・原材料の問い合わせへの回答と、規格書の改訂、衛生管理の記録の取りまとめ', 23, 41.0),
    ('中之条町', 'nakanojo', '宿泊・飲食サービス業', '温泉旅館（個人客が中心）', {'温泉旅館', '宿泊'}, 46,
     '予約サイト・メールの問い合わせへの返信の下書きと、送迎・食事の手配の連絡、館内案内の多言語の文の作成', 22, 36.5),
    ('長野原町', 'naganohara', '建設業', '職別工事業（建築の内装・設備工事）', {'設備工事', '職別工事業', '建設'}, 41,
     '元請・施主への見積書・工程表の作成と、安全書類の取りまとめ、打合せ記録の要約', 17, 44.0),
    ('嬬恋村', 'tsumagoi', '卸売業・小売業', '農産物の集出荷（高原野菜の市場への出荷手配）', {'卸売', '農産物の集出荷', '野菜'}, 58,
     '市場・量販店からの入荷・規格・数量の問い合わせへの回答と、出荷手配の連絡、出荷の伝票の取りまとめ', 38, 23.5),
    ('草津町', 'kusatsu', '宿泊・飲食サービス業', '温泉ホテル（団体・インバウンドの受け入れを含む）', {'温泉ホテル', '宿泊'}, 145,
     '予約サイト・メールの問い合わせへの返信の下書きと、団体の見積書・行程の連絡、館内案内・注意書きの多言語の文の作成', 34, 34.5),
    ('高山村', 'takayama-village-gunma', '医療・福祉', '介護老人保健施設（通所リハビリを併設）', {'介護老人保健施設', '介護'}, 64,
     'リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成', 29, 32.0),
    ('東吾妻町', 'higashiagatsuma', '製造業', 'プラスチック製品（射出成形）', {'射出成形', 'プラスチック製品'}, 90,
     '取引先からの金型・納期・品質の問い合わせへの回答と、成形条件・検査記録の取りまとめ、不具合の報告書の下書き', 46, 23.0),
    ('片品村', 'katashina', '宿泊・飲食サービス業', '民宿・ペンション（スキー・尾瀬の客が中心）', {'ペンション', '民宿', '宿泊'}, 42,
     '予約の電話・メールの問い合わせへの返信の下書きと、送迎・季節の行事の案内の文、宿泊者の記録の整理', 28, 27.25),
    ('川場村', 'kawaba', '医療・福祉', '障害者支援施設（生活介護・就労支援）', {'障害福祉', '障害者支援施設'}, 57,
     '支援記録・個別支援計画の清書と、家族・相談支援専門員への報告、行事の案内文の作成', 32, 25.25),
    ('昭和村', 'showa-village-gunma', '製造業', '食料品（野菜の加工〔カット野菜・漬物〕）', {'野菜加工', '食料品', 'カット野菜'}, 70,
     '量販店・外食の取引先からの規格・数量・産地の問い合わせへの回答と、規格書の作成、製造・衛生管理の記録の取りまとめ', 24, 40.75),
    ('みなかみ町', 'minakami', '宿泊・飲食サービス業', '温泉ホテル（体験・アウトドアの手配を含む）', {'温泉ホテル', '宿泊'}, 118,
     '予約サイト・メールの問い合わせへの返信の下書きと、体験の手配・天候による変更の連絡、館内案内の多言語の文の作成', 44, 25.75),
    ('玉村町', 'tamamura', '運輸業・郵便業', '道路貨物運送（倉庫を併設した配送）', {'倉庫', '運輸', '道路貨物運送'}, 104,
     '荷主からの配送状況・納品の問い合わせへの回答と、配車の連絡、運行の記録・点呼記録の取りまとめ', 38, 28.5),
    ('板倉町', 'itakura', '製造業', '化学（化粧品・洗浄剤の受託製造）', {'化学', '化粧品', '受託製造'}, 76,
     '取引先からの処方・原料・規格の問い合わせへの回答と、製品の安全データシートの改訂、製造記録の取りまとめ', 31, 33.0),
    ('明和町', 'meiwa', '製造業', '印刷（パッケージ・商業印刷）', {'印刷', 'パッケージ印刷'}, 68,
     '取引先からの校正・納期・仕様の問い合わせへの回答と、見積書・作業指示書の作成、入稿データの点検の記録', 36, 26.75),
    ('千代田町', 'chiyoda', '運輸業・郵便業', '倉庫業（化学品・資材の保管と配送）', {'運輸', '倉庫業'}, 80,
     '荷主からの在庫・入出庫の問い合わせへの回答と、入出庫の記録・在庫報告の作成、配送業者への手配の連絡', 28, 34.75),
    ('大泉町', 'oizumi', '製造業', 'はん用機械（ポンプ・送風機の部品の加工）', {'はん用機械', '機械部品'}, 112,
     '取引先からの仕様・納期の問い合わせへの回答と、作業手順書（多言語）・検査記録の取りまとめ', 28, 39.75),
    ('邑楽町', 'ora', '製造業', '電気機械（配電盤・制御盤の製造）', {'配電盤', '制御盤', '電気機械'}, 84,
     '取引先からの仕様・納期の問い合わせへの回答と、図面の変更の連絡書、検査記録・取扱説明書の下書き', 24, 43.25),
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
                print(f"  NG 群馬県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 群馬県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは群馬県の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 35 else "NG")


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
