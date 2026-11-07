#!/usr/bin/env python3
"""和歌山県30市町村の試算の割り当てを計算し、重なりを確かめる（2026-11-07）。

data/area/okinawa/_calc.py を元に作った。県ページ（/area/wakayama/）には試算を入れないので、PLAN は30行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **奈良・和歌山・滋賀の取り決め**: 月の削減時間（0.25時間刻み）×4 を3で割った余りが 1（和歌山県）の時間だけを使う
     （0.25, 1.0, 1.75, 2.5, … の0.75時間刻み。data/area/_kinki/shared.md）
  1. 30ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、和歌山県を除く）の「## 試算」の節に出てくる
     「◯時間」「◯万円」の値と重ならない
  3. 全県の data/area/*/_calc.py の PLAN（和歌山県を除く。glob で全部読む。奈良・滋賀・北海道を含む）の
     月の削減時間・月の時間換算額と重ならない。**読めないファイルは NG にせず警告**。REQUIRED の県はファイルがなければ NG
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases*.md・subsidy_*_areas.md の事例の会社と同じにならない（CASES と照合）
  6. slug が _brief.md の30市町村と一致する
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
  8. 県ページには試算を入れない（PLAN は30行）
使い方: python3 data/area/wakayama/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/wakayama/_calc.py free 製造業 30 200   （余り1の時間で、既存・他県と重ならない時間と金額の候補を出す）
他県の PLAN は後から変わることがあるので、push の直前に git pull してもう一度実行し、最後の行が OK のときだけ push する。
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
SELF = "wakayama"
MOD_N, MOD_R = 3, 1  # 奈良・和歌山・滋賀の割り当て（月の削減時間×4 を3で割った余り）。和歌山県は 1

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
    # 市（9）
    "wakayama-city", "kainan", "hashimoto", "arida", "gobo", "tanabe", "shingu-city", "kinokawa", "iwade",
    # 町（20）
    "kimino", "katsuragi-town", "kudoyama", "koya", "yuasa", "hirogawa", "aridagawa", "mihama-town", "hidaka-town-wakayama",
    "yura", "inami", "minabe", "hidakagawa", "shirahama", "kamitonda", "susami", "nachikatsuura", "taiji", "kozagawa", "kushimoto",
    # 村（1）
    "kitayama-village",
}

# 照合が必須の県（2026-11-07 にある _calc.py）。ファイルがなければ NG
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima",
            "hokkaido", "ibaraki", "tochigi", "gunma", "okinawa")

# cases*.md・subsidy_*_areas.md の事例の会社（調査がそろったら足す）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・交付決定・使用済み・目標を含む〕)
CASES = [
    # cases.md（2026-11-07）。数値つきの県内事例は0件。所在は法人番号で照合済み（cases 担当）
    ("組込ＡＩ研究所（組込AI機器の開発、2名）", "和歌山市", {"電子機器", "AI機器"}, (2, 2), True),
    ("ダートコーヒー（業務用コーヒーの焙煎、和歌山大学の AI 解析、33名）", "和歌山市", {"コーヒー焙煎", "食料品"}, (33, 33), True),
    ("菱岡工業（電気機器・制御機器・ハーネス、AI の文字読み取りで図面、180名）", "和歌山市", {"電気機器", "制御機器", "ハーネス"}, (180, 180), True),
    ("インテリックス（インテリア・カーテン、AI は予定）", "和歌山市", {"インテリア", "カーテン"}, None, True),
    ("河合石灰工業 和歌山工場（計量伝票の AI-OCR、工場23名・会社200名、本社 岐阜）", "和歌山市", {"石灰", "窯業"}, (23, 200), True),
    ("島精機製作所（横編機、生成AI、1,346名）", "和歌山市", {"横編機", "繊維機械"}, (1346, 1346), True),
    ("Kaze（訪問介護の AI 記録アプリのベンダー）", "和歌山市", {"介護ソフト"}, None, True),
    ("西岡会計事務所（生成AI、ベンダーの発表）", "和歌山市", {"会計事務所", "税理士"}, None, True),
    ("ノーリツプレシジョン（AI を作る側、単体300名）", "和歌山市", {"医療機器", "写真処理機"}, (300, 300), True),
    ("城善建設（宅地造成・注文住宅・土木、40人。J-Net21 はクラウド化の話で AI ではない、cases2）", "和歌山市", {"建設", "総合工事業"}, (40, 40), False),
    ("カナプレスト（スプロケット等の金属機械加工、AI カメラで稼働監視、26名）", "紀の川市", {"金属加工", "機械部品"}, (26, 26), True),
    ("サンコー（生活サポート用品、AI は計画、115〜138名）", "海南市", {"生活用品", "家庭用品"}, (115, 138), True),
    ("ニッティド（ニット、Airtable の生産管理。AI ではない）", "海南市", {"繊維", "ニット"}, None, False),
    ("たにぐち（菓子、AI は検証中、154〜160名、本社 大阪）", "日高川町", {"菓子", "食料品"}, (154, 160), True),
    ("中田食品（梅加工、生成AI、300名）", "田辺市", {"梅加工", "食料品"}, (300, 300), True),
    ("TechnologyDock（選果場の AI、ベンダー・検証段階）", "有田川町", {"選果", "ソフトウェア"}, None, True),
    ("浦島観光ホテル（ホテル浦島、AI は今後）", "那智勝浦町", {"宿泊", "ホテル", "温泉旅館"}, None, True),
    ("南紀白浜エアポート（空港の運営、山口県のページで詳述済み）", "白浜町", {"空港"}, None, True),
    ("クオリティソフト（ソフトウェア、AI を作る側）", "白浜町", {"ソフトウェア"}, None, True),
    ("金剛ダイス工業（工場が紀美野町・本社 大阪市、23名。関経連 iot26、AI は今後の予定だけ。稼働率の数値は IoT、cases2）", "紀美野町", {"金型", "ダイス", "金属製品"}, (23, 23), True),
    # cases2.md（2026-11-07）。県の中小企業成長促進補助金の交付決定で計画名に AI（成果の公表なし）
    ("公世社花平（葬儀、AI 行動検知の交付決定、45名）", "橋本市", {"葬儀", "葬祭"}, (45, 45), True),
    ("テルグリットマーケティング（SNS 運用支援、AI の交付決定）", "橋本市", {"広告", "マーケティング"}, None, True),
    ("秋山逓送（本店 御坊市・実施は和歌山市、運送、AI 統合業務管理の交付決定）", "御坊市", {"運送", "道路貨物運送"}, None, True),
    ("秋山逓送（実施場所は和歌山市）", "和歌山市", {"運送", "道路貨物運送"}, None, True),
    ("A&B商事（EC、AI 画像認識の交付決定）", "和歌山市", {"EC", "通販", "小売"}, None, True),
    ("Houseland（自社所有の賃貸管理、AI の交付決定）", "和歌山市", {"不動産", "賃貸管理"}, None, True),
    ("スミカ（AI チャットボットと RPA の交付決定）", "和歌山市", {"住宅", "不動産"}, None, True),
    ("美浜オーキッド（本店 美浜町・実施は御坊市、出荷・販売管理の AI の交付決定）", "美浜町", {"花き", "洋らん"}, None, True),
    ("果無（森林土木の測量、AI 搭載 3D スキャナの交付決定）", "田辺市", {"測量", "森林土木"}, None, True),
    ("サークルマウンテン（自費診療部門の AI の交付決定）", "和歌山市", {"診療所", "自費診療"}, None, True),
    ("メイク広告（看板、AI 見積の交付決定）", "和歌山市", {"看板", "広告"}, None, True),
    # cases2.md のほか
    ("うめひかり（梅農家・梅干しメーカー、AI の梅選別機を開発中、2026-06 稼働予定の報道）", "みなべ町", {"梅加工", "梅干し"}, None, True),
    ("KURAおさかなファーム（くら寿司の子会社、由良町に事務所、AI 給餌。愛媛県宇和島市で使用済み）", "由良町", {"養殖", "水産"}, None, True),
    ("和歌山大同青果（青果卸、販売管理システム。AI ではない）", "和歌山市", {"卸売", "青果物卸"}, None, False),
]

PLAN = [
    ('和歌山市', 'wakayama-city', '医療・福祉', '病院（一般病床・外来・健診）', {'医療', '病院'}, 165,
     '退院時サマリー・診療情報提供書の下書きと、健診の結果説明の文書、院内の委員会の議事録の作成', 40, 31.75),
    ('海南市', 'kainan', '運輸業・郵便業', '道路貨物運送（日用品・家庭用品の配送）', {'運送', '道路貨物運送'}, 85,
     '荷主からの配送日時・数量の問い合わせへの回答と、配車の連絡、日報・事故防止の記録の取りまとめ', 40, 29.5),
    ('橋本市', 'hashimoto', '製造業', '繊維工業（織物の製造と加工）', {'織物', '繊維'}, 52,
     '取引先からの納期・在庫・品質の問い合わせへの回答と、生地の仕様書・見本の説明文、生産の記録の取りまとめ', 40, 28.75),
    ('有田市', 'arida', '製造業', '食料品製造業（果実の加工品）', {'食料品', '果実加工'}, 40,
     '量販店・通販の取引先からの原材料・賞味期限の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 28, 40.0),
    ('御坊市', 'gobo', '製造業', '生産用機械器具製造業（産業機械の部品の加工・組立）', {'産業機械', '生産用機械'}, 70,
     '取引先からの図面・仕様・納期の問い合わせへの回答と、作業手順書・検査記録の取りまとめ、見積書の下書き', 47, 26.0),
    ('田辺市', 'tanabe', '医療・福祉', '特別養護老人ホーム（短期入所を併設）', {'特別養護老人ホーム', '介護'}, 92,
     'ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、委員会の議事録の作成', 34, 37.0),
    ('新宮市', 'shingu-city', '卸売業・小売業', '食料品スーパー（地域の複数店舗）', {'スーパー', '食料品小売', '小売'}, 72,
     '仕入先への発注・欠品の連絡と、売場の案内・チラシの文の下書き、客からの取り寄せ・問い合わせへの回答', 40, 27.25),
    ('紀の川市', 'kinokawa', '製造業', 'はん用機械器具製造業（ポンプ・機械の組立）', {'機械器具', 'はん用機械'}, 62,
     '取引先からの仕様・納期の問い合わせへの回答と、組立の手順書・検査成績書の取りまとめ、部品メーカーへの照会文', 44, 26.75),
    ('岩出市', 'iwade', '宿泊・飲食サービス業', '飲食店（和食・宴会の複数店舗）', {'和食', '飲食店'}, 66,
     '予約・宴会の問い合わせへの返信と、宴会の見積書・献立の案内文、仕入先への発注の連絡の作成', 40, 25.75),
    ('紀美野町', 'kimino', '製造業', '繊維工業（ニット生地の製造）', {'繊維', 'ニット'}, 35,
     '取引先からの納期・在庫の問い合わせへの回答と、生地の仕様書の作成、生産の記録の取りまとめ', 20, 41.75),
    ('かつらぎ町', 'katsuragi-town', '卸売業・小売業', '果物の直売・通販（柿・桃などの出荷）', {'通販', '小売', '果物'}, 26,
     '通販の注文・配送日の問い合わせへの返信と、商品案内・季節の案内の文、発送の記録の取りまとめ', 20, 44.75),
    ('九度山町', 'kudoyama', '医療・福祉', '介護（デイサービスと訪問介護）', {'訪問介護', '通所介護', '介護'}, 38,
     '介護記録の清書と、ケアマネジャーへの報告書、家族への連絡文の作成', 16, 48.25),
    ('高野町', 'koya', '卸売業・小売業', '土産物・食料品の小売（参詣者・観光客向けの店）', {'土産物', '小売'}, 33,
     '仕入先への発注の連絡と、外国人客向けの商品案内の多言語の文、通販の問い合わせへの返信', 20, 47.0),
    ('湯浅町', 'yuasa', '製造業', '食料品製造業（醤油・調味料の醸造）', {'醤油', '醸造', '食料品'}, 48,
     '小売店・通販の取引先からの原材料・賞味期限の問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ', 38, 27.5),
    ('広川町', 'hirogawa', '建設業', '総合工事業（土木・舗装、公共工事が中心）', {'総合工事業', '建設', '土木'}, 36,
     '公共工事の施工計画書・提出書類の作成と、工事写真の整理、発注者との打合せ記録の要約', 25, 43.0),
    ('有田川町', 'aridagawa', '卸売業・小売業', '果実の卸（みかんの集荷と出荷）', {'果実', '青果物卸', '卸売'}, 44,
     '市場・量販店からの数量・規格の問い合わせへの回答と、出荷の記録の取りまとめ、生産者への連絡文の作成', 34, 35.5),
    ('美浜町', 'mihama-town', '医療・福祉', '病院（療養病床とリハビリ）', {'医療', '病院'}, 118,
     'リハビリ・看護の記録の要約と、入院・退院の説明文書、居宅のケアマネジャーへの報告書の作成', 32, 39.5),
    ('日高町', 'hidaka-town-wakayama', '医療・福祉', '介護老人保健施設（通所リハビリを併設）', {'介護老人保健施設', '介護'}, 46,
     'リハビリ・ケアの記録の要約と、入所・退所の説明文書、家族への連絡文の作成', 20, 41.0),
    ('由良町', 'yura', '製造業', '輸送用機械器具製造業（部品の加工）', {'輸送用機械', '部品加工'}, 54,
     '取引先からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録・不具合の報告書の取りまとめ', 31, 40.0),
    ('印南町', 'inami', '建設業', '設備工事業（電気・管工事）', {'電気工事', '管工事', '設備工事'}, 25,
     '見積書・施工の報告書の作成と、元請・施主への日程の連絡、工事写真の整理', 19, 19.0),
    ('みなべ町', 'minabe', '卸売業・小売業', '梅干し・梅の加工品の卸と通販（量販店・ギフト向けの出荷）', {'通販', '卸売'}, 42,
     '量販店・通販の取引先からの規格・塩分・賞味期限・納期の問い合わせへの回答と、ギフトの商品案内の文、出荷の記録の取りまとめ', 28, 43.75),
    ('日高川町', 'hidakagawa', '建設業', '総合工事業（土木・林道・治山）', {'総合工事業', '建設', '土木'}, 29,
     '施工計画書・安全書類の作成と、工事写真の整理、発注者との打合せ記録の要約', 20, 49.25),
    ('白浜町', 'shirahama', '宿泊・飲食サービス業', 'ホテル（温泉リゾート・団体の受け入れを含む）', {'宿泊', 'ホテル'}, 130,
     '予約サイト・メールの問い合わせへの返信の下書きと、団体・宴会の見積書、館内案内の多言語の文の作成', 44, 28.25),
    ('上富田町', 'kamitonda', '運輸業・郵便業', '道路貨物運送（食品・日用品の配送）', {'運送', '道路貨物運送'}, 39,
     '荷主からの配送日時の問い合わせへの回答と、配車の連絡、日報の取りまとめ', 20, 32.75),
    ('すさみ町', 'susami', '製造業', '水産食料品製造業（干物・加工品）', {'食料品', '水産加工'}, 20,
     '通販・小売店の取引先からの原材料・賞味期限の問い合わせへの回答と、商品の表示の文、出荷の記録の取りまとめ', 8, 47.75),
    ('那智勝浦町', 'nachikatsuura', '卸売業・小売業', '水産物の卸（生まぐろの仲卸）', {'まぐろ', '水産物卸', '卸売'}, 31,
     '市場・飲食店の取引先からの入荷・規格の問い合わせへの回答と、出荷の記録の取りまとめ、発送の連絡文の作成', 20, 46.25),
    ('太地町', 'taiji', '卸売業・小売業', '食料品の小売（鮮魚・土産物の店）', {'鮮魚', '土産物', '小売'}, 18,
     '仕入先への発注の連絡と、通販の問い合わせへの返信、商品案内の文の作成', 8, 51.5),
    ('古座川町', 'kozagawa', '医療・福祉', '認知症グループホーム', {'グループホーム', '介護'}, 28,
     '生活記録の清書と、運営推進会議の議事録、家族への便りの文の作成', 17, 23.0),
    ('北山村', 'kitayama-village', '建設業', '総合工事業（道路・林道の工事）', {'総合工事業', '建設', '土木'}, 24,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理', 13, 19.0),
    ('串本町', 'kushimoto', '宿泊・飲食サービス業', '旅館・民宿（ダイビング・観光客の宿）', {'宿泊', '民宿', '旅館'}, 27,
     '予約サイト・メールの問い合わせへの返信と、天候による予約変更の連絡、外国語の案内文・口コミへの返信文の作成', 20, 43.25),
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
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | 年間 | ×4 を3で割った余り |")
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
            print(f"  NG {city} の時間 {h} は3県の割り当て（×4 を3で割った余り {MOD_R}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 和歌山県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 和歌山県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは和歌山県の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 30 else "NG")


def free(ind, lo, hi):
    """余り1の時間で、既存の記事・他県の PLAN と時間も金額も重ならない候補を出す（PLAN の行を決める手がかり）"""
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
