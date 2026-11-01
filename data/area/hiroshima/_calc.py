#!/usr/bin/env python3
"""広島県23市町の試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-11-01）。

data/area/tottori/_calc.py を元に作った。県ページ（/area/hiroshima/）には試算を入れない案なので PLAN は23行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  1. 23ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-??-area-*.md、広島県を除く。山梨・島根・鳥取の記事を含む）の
     「## 試算」の節に出てくる「◯時間」「◯万円」の値と重ならない。拾い方は鳥取県の _calc.py と同じ
     （1人の業務量・年間の額・差し引き後の額なども広めに拾う。拾いすぎは「重ならない」側に働く）
  3. 山梨県・島根県・鳥取県の _calc.py の PLAN の月の削減時間・月の時間換算額とも重ならない。
     山口県（data/area/yamaguchi/_calc.py）は並行のセッションが後で push する。ファイルがあれば PLAN を読んで照合し、
     なければ「まだない」と表示する（NG にはしない。push の前に再実行して確かめる）
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円ちょうど）にならない
  5. 試算の業種（業態）・規模が cases.md（・cases_outside.md）の事例の会社と同じにならない（CASES と照合）
     - AI の事例で、業態のキーが重なり、従業員数が事例の範囲（区分なら下限×0.85〜上限×1.15）に入る → NG
     - AI の事例で、業態のキーが重なり、同じ市町で、事例の従業員数が分からない → NG（その会社の値と読まれるため）
     - 業種が確かめられていない AI の事例（キー「業種未確認」）と同じ市町 → 参考として表示（NG にしない）
     - AI ではない事例（県の事例集の「広島県内事例」。所在地は確かめていない）と業態・規模が近い → 参考として表示
  6. slug が _brief.md の23市町と一致する
  7. 試算の業種が wages.md にある（農業・漁業は試算の業種にしない）
使い方: python3 data/area/hiroshima/_calc.py   （末尾に OK / NG を出す）
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

# wages.md の人件費時給（時給①×1.2 を十円単位に丸めた値。記事でも「約◯円」と書く値）
RATE = {
    "製造業": 3500,
    "卸売業・小売業": 3540,
    "建設業": 3520,
    "運輸業・郵便業": 2980,
    "医療・福祉": 3180,
    "宿泊・飲食サービス業": 2510,
}

SLUGS = {"hiroshima-city", "kure", "takehara", "mihara", "onomichi", "fukuyama", "fuchu-city", "miyoshi", "shobara",
         "otake", "higashihiroshima", "hatsukaichi", "akitakata", "etajima", "fuchu-town", "kaita", "kumano", "saka",
         "akiota", "kitahiroshima", "osakikamijima", "sera", "jinsekikogen"}

# cases.md の事例の会社
# (会社名, 市町〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。県の事例集の規模の区分。分からなければ None〕, AI の事例か)
# cases_outside.md は 2026-11-01 の下書きの時点で未作成。できたら県外の行（業態・従業員数）を足して再実行する
CASES = [
    # cases.md（広島県内の AI の事例・実証）
    ("ツーセル", "広島市", {"医療系の研究開発", "医薬品", "医療機器"}, (11, 50), True),
    ("レリーフ", "広島市", {"情報サービス", "印刷", "Web制作"}, (1, 10), True),
    ("en.company", "広島市", {"宿泊"}, (11, 50), True),
    ("オオケン", "広島市", {"ビルメンテナンス"}, (301, 900), True),
    ("ハコジム（AI はサービスの一部）", "広島市", {"フィットネス"}, (1, 10), True),
    ("広島県リースタオル（実証中）", "広島市", {"リネンサプライ", "おしぼり"}, None, True),
    ("津田製作所（実証中）", "広島市", {"業種未確認"}, None, True),
    ("寺尾園芸土木（実証中）", "広島市", {"建設", "造園"}, None, True),
    ("医療法人松栄会（実証中）", "広島市", {"医療", "介護"}, None, True),
    ("インシップス（実証中）", "広島市", {"業種未確認"}, None, True),
    ("メビウスマネジメントサービス（実証中）", "広島市", {"経営コンサルタント", "M&A"}, None, True),
    ("アイグラン（対象外・島根で詳述）", "広島市", {"保育"}, None, True),
    ("尾道さつき会", "尾道市", {"介護", "特別養護老人ホーム", "通所介護"}, None, True),  # 職員数は「約40名分の勤務表」だけ
    ("鳴滝工業（実証中）", "尾道市", {"業種未確認"}, None, True),
    ("せともす（実証中）", "尾道市", {"宿泊"}, None, True),
    ("門井商店（実証中）", "福山市", {"食料品", "食品卸"}, None, True),  # 業種は未確認。「食品規格書」から食品関係として照合
    ("常石造船（使用済み）", "福山市", {"造船", "船舶"}, None, True),
    ("山陽病院（使用済み）", "福山市", {"医療", "病院"}, None, True),
    ("クラハシ（使用済み）", "福山市", {"卸売", "水産卸"}, None, True),
    ("晃祐堂", "熊野町", {"筆", "その他の製造業"}, None, True),
    ("大崎上島町のレモン農家3者", "大崎上島町", {"農業", "果実", "レモン"}, None, True),
    ("三原駅かなもと眼科（実証中）", "三原市", {"医療", "診療所"}, None, True),
    ("医療法人社団明和会（実証中）", "廿日市市", {"介護", "医療"}, None, True),
    ("地御前漁協（使用済み）", "廿日市市", {"漁業", "かき"}, None, True),
    ("チチヤス（使用済み）", "廿日市市", {"食料品", "乳製品"}, None, True),
    ("ヤルキマントッキーズ（実証中）", "東広島市", {"スポーツ"}, None, True),
    ("有限会社前田（AI は付随、所在未確認）", "所在未確認", {"動物病院"}, (11, 50), True),
    ("東洋シート（2019年の実証）", "海田町", {"輸送用機械", "自動車部品"}, None, True),
    ("とびしま柑橘倶楽部", "呉市", {"農業", "果実", "レモン"}, None, True),
    ("アヲハタ（使用済み）", "竹原市", {"食料品", "ジャム"}, None, True),
    ("世羅幸水農園（使用済み）", "世羅町", {"農業", "果実", "梨"}, None, True),
    ("内能美漁協ほか（対象外・島根で詳述）", "江田島市", {"漁業", "かき"}, None, True),
    # D2 の照合で足した県内の会社（2026-11-01。福山市の AI ビジネスキャンプの成果資料・よろず支援拠点の成果事例。所在は法人番号で確認）
    ("モン・ハマオカ（よろず、HP制作に生成AI）", "福山市", {"繊維", "縫製", "衣服"}, None, True),  # 従業員数は公式サイトにない
    ("宇田被服（AIビジネスキャンプ2024、数値なし）", "福山市", {"繊維", "縫製", "衣服"}, None, True),  # 従業員数は未確認
    ("くるま生活（AIビジネスキャンプ2024、SNS投稿）", "福山市", {"業種未確認"}, None, True),
    ("ディスカバーリンクせとうち（AIビジネスキャンプ2024、数値なし）", "福山市", {"業種未確認"}, None, True),
    ("西部運輸（AIビジネスキャンプ2025、数値なし）", "福山市", {"運送", "倉庫"}, (1854, 1854), True),  # グループ社員数（2026年2月）
    ("Plaque（AIビジネスキャンプ2025、AI ツールの開発会社）", "福山市", {"情報サービス"}, None, True),
    # cases_outside.md（県外。2026-11-01 D2 が追加）
    ("フォーバンド（福岡県直方市）", "県外", {"金属製品", "機械部品", "精密部品加工"}, (18, 18), True),
    ("協和製作所（静岡県沼津市）", "県外", {"生産用機械", "機械部品", "精密部品加工"}, (20, 20), True),
    ("コクネ製作（愛知県西尾市）", "県外", {"機械部品", "機械加工", "鋳物"}, (51, 100), True),
    ("朝日共販（愛媛県伊方町）", "県外", {"食料品", "水産加工"}, None, True),
    # cases.md の「AIではない」（県の事例集の「広島県内事例」。所在地は確かめていない → 参考）
    ("日本サカス（AIではない）", "所在未確認", {"プラスチック製品"}, (11, 50), False),
    ("天女山（AIではない）", "所在未確認", {"林業"}, (11, 50), False),
    ("このみや（AIではない）", "所在未確認", {"洋服修理"}, (11, 50), False),
    ("スタンダード（AIではない）", "所在未確認", {"運送", "軽貨物"}, (51, 100), False),
    ("府中メッキ工業所（AIではない）", "所在未確認", {"金属製品", "めっき"}, (11, 50), False),
    ("廣島織染協同組合（AIではない）", "所在未確認", {"繊維"}, (11, 50), False),
    ("アンダンテ・サルート・TAT（AIではない）", "所在未確認", {"介護", "医療"}, None, False),
    ("ホテル清風館・大根屋・まんまる（AIではない）", "所在未確認", {"宿泊", "飲食店"}, None, False),
]

# (市町, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
PLAN = [
    # 広島圏域（8）
    ("広島市", "hiroshima-city", "卸売業・小売業", "機械器具・産業資材の卸売（市内に本社と営業所）", {"卸売", "機械器具"}, 180,
     "得意先からの在庫・納期・価格の問い合わせへの回答と、営業担当の見積書の下書き・商談記録の要約", 28, 32),
    ("安芸高田市", "akitakata", "製造業", "金属製品（プレス・板金の加工）", {"金属製品", "金属プレス"}, 58,
     "取引先からの図面・仕様の問い合わせへの回答と、検査成績書・作業日報の取りまとめ", 13, 37),
    ("府中町", "fuchu-town", "宿泊・飲食サービス業", "飲食店（町内外に複数の店舗）", {"飲食店"}, 48,
     "予約・団体利用の問い合わせへの返信と、店舗のメニュー・アレルギー表示の説明文の作成", 12, 39.5),
    ("海田町", "kaita", "卸売業・小売業", "食品スーパー（複数店舗）", {"小売", "食品スーパー"}, 65,
     "商品の入荷・在庫の問い合わせへの回答と、売場のPOP・チラシの商品説明文の作成", 12, 39),
    ("熊野町", "kumano", "医療・福祉", "通所介護・居宅介護支援", {"介護", "通所介護"}, 28,
     "利用者ごとの通所の記録の清書と、ケアマネジャー・家族への連絡文の作成", 10, 42.5),
    ("坂町", "saka", "運輸業・郵便業", "倉庫・道路貨物運送", {"運送", "倉庫"}, 125,
     "荷主からの入出庫・配送の問い合わせへの回答と、運転日報・入出庫記録の集計", 20, 38),
    ("安芸太田町", "akiota", "医療・福祉", "訪問介護・グループホーム", {"介護", "訪問介護", "グループホーム"}, 24,
     "訪問・入居者の記録の清書と、家族への近況報告・事故報告書の下書き", 10, 40.5),
    ("北広島町", "kitahiroshima", "建設業", "総合工事業（土木）", {"建設"}, 38,
     "公共工事の施工計画書・提出書類の作成と、工事写真の台帳の整理", 10, 38.5),
    # 広島西圏域（2）
    ("大竹市", "otake", "医療・福祉", "病院", {"医療", "病院"}, 100,
     "紹介状への返書・退院時の診療情報提供書の下書きと、患者向けの検査・入院の説明文書の作成", 17, 38),
    ("廿日市市", "hatsukaichi", "宿泊・飲食サービス業", "旅館・ホテル", {"宿泊"}, 85,
     "国内外の予約客からの問い合わせメールへの返信の下書きと、宿泊プラン・館内案内の多言語の説明文の作成", 15, 37),
    # 呉圏域（2）
    ("呉市", "kure", "製造業", "生産用機械（産業機械の部品の加工・組立）", {"生産用機械", "機械部品"}, 110,
     "顧客からの仕様・納期の問い合わせへの回答と、過去の図面・不具合記録の検索、作業手順書の下書き", 18, 37),
    ("江田島市", "etajima", "製造業", "食料品（かきなど水産物の加工）", {"食料品", "水産加工"}, 36,
     "取引先に出す商品規格書（原材料・産地・アレルゲン）の作成と、出荷・衛生管理の記録の取りまとめ", 10, 43),
    # 広島中央圏域（3）
    ("東広島市", "higashihiroshima", "製造業", "輸送用機械（自動車部品）", {"輸送用機械", "自動車部品"}, 140,
     "顧客からの品質の問い合わせへの回答と、不具合の対策報告書・検査記録の取りまとめ", 22, 37),
    ("竹原市", "takehara", "医療・福祉", "介護老人保健施設（通所リハビリを併設）", {"介護", "介護老人保健施設"}, 62,
     "ケア記録・リハビリ記録の要約と、入所・退所の説明文書の作成", 13, 38),
    ("大崎上島町", "osakikamijima", "製造業", "輸送用機械（船舶の建造・修理）", {"輸送用機械", "造船"}, 33,
     "船主からの仕様・工程の問い合わせへの回答と、工程表・作業日報の取りまとめ", 10, 41.5),
    # 尾三圏域（3）
    ("三原市", "mihara", "製造業", "輸送用機械（自動車・船舶の部品）", {"輸送用機械", "機械部品"}, 90,
     "取引先からの図面・納期の問い合わせへの回答と、品質記録・出荷書類の作成", 14, 36),
    ("尾道市", "onomichi", "製造業", "食料品（水産物・かんきつの加工）", {"食料品", "水産加工", "農産加工"}, 70,
     "取引先に出す商品規格書・アレルゲン表示の確認と、製造ロット・賞味期限の記録の取りまとめ", 12, 40.5),
    ("世羅町", "sera", "卸売業・小売業", "鶏卵・野菜の集出荷と販売", {"卸売", "鶏卵", "野菜"}, 31,
     "取引先からの受注・出荷数量の連絡と、出荷伝票・精算書の取りまとめ", 11, 37),
    # 福山・府中圏域（3）
    ("福山市", "fukuyama", "製造業", "繊維工業（衣服の縫製・染色加工）", {"繊維", "縫製"}, 160,
     "取引先からの仕様・納期の問い合わせへの回答と、生産指示書・検品記録の取りまとめ", 24, 38),
    ("府中市", "fuchu-city", "製造業", "家具・装備品（受注家具の製造）", {"家具"}, 45,
     "受注家具の仕様の確認と見積書・図面の説明文の作成、施主・工務店への納期の連絡", 11, 41),
    ("神石高原町", "jinsekikogen", "建設業", "総合工事業", {"建設"}, 21,
     "工事日報の取りまとめと、発注者に出す工事書類・写真の整理", 8, 44.5),
    # 備北圏域（2）
    ("三次市", "miyoshi", "運輸業・郵便業", "道路貨物運送", {"運送"}, 40,
     "配車表の下書きと、荷主への配送予定・遅延の連絡", 11, 39),
    ("庄原市", "shobara", "医療・福祉", "特別養護老人ホーム", {"介護", "特別養護老人ホーム"}, 80,
     "ケア記録・夜勤の申し送りの要約と、家族への近況報告文の作成", 15, 38),
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def other_plans():
    """山梨県・島根県・鳥取県（と、あれば山口県）の _calc.py の PLAN を読み、(県, 市町村, 削減時間, 万円) を返す。
    必須の3県のファイルがなければ None を入れる（NG）。山口県はなければ表示だけ。"""
    out, missing_optional = [], []
    for pref, label, required in (("yamanashi", "山梨県", True), ("shimane", "島根県", True),
                                  ("tottori", "鳥取県", True), ("yamaguchi", "山口県", False)):
        path = os.path.join(ROOT, "data", "area", pref, "_calc.py")
        if not os.path.exists(path):
            if required:
                print(f"NG {label}の _calc.py がない: {path}")
                out.append(None)
            else:
                missing_optional.append(label)
            continue
        src = open(path, encoding="utf-8").read()
        i = src.index("PLAN = [")
        j = src.index("\n]\n", i)
        for r in ast.literal_eval(src[i + 7:j + 2]):
            city, ind, n, hrs = r[0], r[2], r[-2], r[-1]
            if ind not in RATE:
                continue
            h = Decimal(str(n)) * Decimal(str(hrs)) * Decimal("0.25")
            out.append((label, city, h, man(h * RATE[ind])))
    return out, missing_optional


def existing():
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（鳥取県の _calc.py と同じ拾い方）。"""
    hours, mans, sizes, per_file = {}, {}, {}, {}
    files = [f for f in sorted(glob.glob(os.path.join(ART, "2026-1?-??-area-*.md"))) if "-area-hiroshima" not in f]
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
          f"島根 {by_pref.get('shimane', 0)}本・鳥取 {by_pref.get('tottori', 0)}本・山口 {by_pref.get('yamaguchi', 0)}本を含む）。"
          f"拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種・規模 {len(ex_s)}種")
    op, missing_optional = other_plans()
    ok = None not in op
    pl_h, pl_m = {}, {}
    for r in op:
        if r is None:
            continue
        label, city, h, m = r
        pl_h.setdefault(h, f"{label}{city}（_calc.py の PLAN）")
        pl_m.setdefault(m, f"{label}{city}（_calc.py の PLAN）")
    print(f"他県の PLAN: {len([r for r in op if r])}行（時間 {len(pl_h)}種・万円 {len(pl_m)}種）")
    for label in missing_optional:
        print(f"（注意）{label}の _calc.py はまだない（並行のセッションが push したら、この照合を再実行する）")
    if os.path.exists(os.path.join(HERE, "cases_outside.md")):
        print("（注意）cases_outside.md がある。県外の会社（業態・従業員数）を CASES に足したか確かめる")

    seen_h, seen_m, seen_s = {}, {}, {}
    n_quarter = 0
    notes = []
    print("| 市町 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | 年間 |")
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
                print(f"  NG 広島県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 広島県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
                if csize is not None and in_range(size, csize):
                    notes.append(f"{city}: 試算（{sub}・{size}名）と業態が近い AI ではない事例 {cname}（{csize or '規模不明'}、所在未確認）")
                continue
            if csize is not None and in_range(size, csize):
                print(f"  NG {city} の試算（{sub}・{size}名）が事例 {cname}（{'・'.join(sorted(ckeys))}・{csize[0]}〜{csize[1]}名）に近い")
                ok = False
            elif csize is None and ccity == city:
                print(f"  NG {city} の試算（{sub}）が同じ市町の事例 {cname}（規模不明）と同じ業態")
                ok = False
    slugs = {p[1] for p in PLAN}
    if slugs != SLUGS:
        print("NG slug が _brief.md と違う:", slugs ^ SLUGS)
        ok = False
    n_ex_size = sum(1 for p in PLAN if p[5] in ex_s)
    print(f"\n市町ページ: {len(PLAN)}、市町名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}")
    print(f"時間の範囲 {min(seen_h)}〜{max(seen_h)}時間、金額の範囲 約{min(seen_m)}〜{max(seen_m)}万円、規模 {min(seen_s)}〜{max(seen_s)}名")
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは広島県の中だけを NG にする）")
    print(f"（参考）時間が◯.25・◯.75になるページ: {n_quarter}件")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 23 else "NG")


if __name__ == "__main__":
    main()
