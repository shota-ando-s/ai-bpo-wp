#!/usr/bin/env python3
"""山口県19市町の試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-11-01）。

data/area/tottori/_calc.py を元に作った。県ページには試算を入れない（鳥取県と同じ）ので、PLAN は19行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  1. 19ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、山口県を除く。山梨・島根・鳥取の記事を含む）の
     「## 試算」の節に出てくる「◯時間」「◯万円」の値と重ならない。拾い方は鳥取県の _calc.py と同じ
     （1人の業務量・年間の額・差し引き後の額なども広めに拾う。拾いすぎは「重ならない」側に働く）
  3. 山梨県・島根県・鳥取県の _calc.py の PLAN、広島県の _calc.py（data/area/hiroshima/_calc.py。あれば）の PLAN の
     月の削減時間・月の時間換算額とも重ならない（公開前の割り当て。ファイルを読んで照合する）
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円ちょうど）にならない
  5. 試算の業種（業態）・規模が cases.md（cases_outside.md ができたら県外の行も）の事例の会社と同じにならない（CASES と照合）
     - 業態のキーが重なり、従業員数が事例の±15%以内 → NG
     - 業態のキーが重なり、同じ市町で、事例の従業員数が分からない AI の事例 → NG（その会社の値と読まれるため）
     - 業種が確かめられていない AI の事例（キー「業種未確認」）と同じ市町 → 参考として表示（NG にしない）
     - 同じ市町・同じ業態で、AI ではない事例（規模不明） → 参考として表示（NG にしない）
  6. slug が _brief.md の19市町と一致する
  7. 試算の業種が wages.md にある（農業・漁業は試算の業種にしない）
使い方: python3 data/area/yamaguchi/_calc.py   （末尾に OK / NG を出す）
"""
import ast
import glob
import os
import re
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ART = os.path.join(ROOT, "articles")
SELF = "yamaguchi"

# wages.md の人件費時給（時給①×1.2 を十円単位に丸めた値。記事でも「約◯円」と書く値）
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

SLUGS = {"shimonoseki", "ube", "yamaguchi-city", "hagi", "hofu", "kudamatsu", "iwakuni", "hikari", "nagato",
         "yanai", "mine", "shunan", "sanyo-onoda", "suo-oshima", "waki", "kaminoseki", "tabuse", "hirao", "abu"}

# 照合する他県の PLAN（公開前の割り当て）。hiroshima は広島県のセッションが作業中で、ファイルがなければ飛ばす
OTHER_PLANS = (("yamanashi", "山梨県", True), ("shimane", "島根県", True), ("tottori", "鳥取県", True),
               ("hiroshima", "広島県", False))

# cases.md の事例の会社（2026-11-01 の cases.md から）
# (会社名, 市町〔県外は「県外」〕, 業態のキー, 従業員数〔分からなければ None〕, AI の事例か)
# cases_outside.md は 2026-11-01 の下書きの時点で未作成。できたら県外の行を足して再実行する
CASES = [
    # 下関市
    ("アクシス", "下関市", {"金属製品", "精密板金", "車両部品"}, 25, True),
    ("ひびき精機（山梨で使用済み）", "下関市", {"機械部品", "金属加工", "生産用機械"}, 118, True),  # DXの手引きでは100人
    ("住吉工業（県の実証）", "下関市", {"業種未確認"}, None, True),
    ("テンシステム", "下関市", {"障害福祉", "就労継続支援", "情報サービス"}, 20, True),
    ("コプロス（AIではない）", "下関市", {"建設", "3DCG"}, None, False),
    ("JRCS（AIではない）", "下関市", {"業種未確認"}, None, False),
    # 周南市
    ("高橋鉄工", "周南市", {"金型", "金属製品", "金属加工"}, 15, True),
    ("ミヤハラ", "周南市", {"生産用機械", "製造装置"}, 50, True),
    ("周南マリコム（計画）", "周南市", {"電気通信工事", "見守り"}, 65, True),
    ("徳機（AIではない）", "周南市", {"業種未確認"}, None, False),
    ("トクヤマ（大企業、使わない）", "周南市", {"化学"}, None, True),
    ("東ソー（大企業、未確認）", "周南市", {"化学"}, None, True),
    # 下松市
    ("日進工業", "下松市", {"技術サービス", "プラント検査", "設備保全", "検査"}, 78, True),
    ("鋼鈑工業（AIではない）", "下松市", {"業種未確認"}, None, False),
    ("くだまつ平成会（手がかり、AIか未確認）", "下松市", {"介護"}, None, False),
    # 宇部市
    ("UBE（大企業）", "宇部市", {"化学"}, None, True),
    ("エコマス", "宇部市", {"業種未確認"}, None, True),
    ("リード（所在未確認）", "宇部市", {"業種未確認"}, None, True),
    ("WAVES COFFEE", "宇部市", {"食料品", "コーヒー焙煎"}, None, True),
    ("スマートレビュー・テクノロジーズ（計画）", "宇部市", {"業種未確認"}, None, True),
    ("MOT総合研究所（計画）", "宇部市", {"情報サービス"}, None, True),
    # 山口市
    ("中国芝浦電子", "山口市", {"電子部品"}, None, True),
    ("YOODS", "山口市", {"業種未確認"}, None, True),
    ("スクエアイノベーション（計画）", "山口市", {"不動産"}, None, True),
    ("山口システム通信（計画）", "山口市", {"ゴルフ", "娯楽"}, None, True),
    ("ニュージャパンナレッジ（AIではない）", "山口市", {"情報サービス"}, None, False),
    # 防府市
    ("村重石油", "防府市", {"業種未確認"}, None, True),
    ("大村印刷（計画）", "防府市", {"印刷"}, None, True),
    ("王子ゴム化成（AIではない）", "防府市", {"ゴム製品"}, None, False),
    ("三友（AIではない）", "防府市", {"業種未確認"}, None, False),
    # 美祢市
    ("美東電子（真名ファーム）", "美祢市", {"農業", "きのこ"}, 85, True),  # DXの手引きでは126人
    # 長門市
    ("深川養鶏農協（産技センターの研究）", "長門市", {"養鶏", "畜産", "鶏肉"}, None, True),
    # 岩国市
    ("カワトT.P.C.（山梨で詳述）", "岩国市", {"設備工事", "建設"}, None, True),
    ("旭酒造（他県で使用済み）", "岩国市", {"酒造", "飲料"}, None, True),
    ("シーパーツ（計画）", "岩国市", {"自動車リユース部品", "中古部品"}, None, True),
    # 山陽小野田市
    ("長州産業（AIではない）", "山陽小野田市", {"業種未確認"}, None, False),
    # 県外（cases_outside.md、2026-11-01。D2 で追加。規模の分からない県外の事例は、同じ市町の NG にならない〔ccity が「県外」〕）
    ("ガンズコーポレーション（東京都江戸川区）", "県外", {"設備工事", "通信設備工事", "建設"}, 11, True),
    ("大日コンサルタント（岐阜市）", "県外", {"建設コンサルタント", "技術サービス"}, 363, True),
    ("南紀白浜エアポート（和歌山県白浜町）", "県外", {"空港運営", "点検"}, None, True),
    ("大阪港埠頭ターミナル（大阪府）", "県外", {"倉庫", "港湾運送"}, None, True),
    ("オーシャントランス・東京港フェリーターミナル（東京都）", "県外", {"フェリー", "水運"}, None, True),
    ("JAながさき西海 させぼ広域かんきつ部会（長崎県）", "県外", {"農業", "柑橘"}, None, True),
    ("JA長崎せいひ ことのうみ柑橘部会（長崎県）", "県外", {"農業", "柑橘"}, None, True),
    ("熱海市・熱海観光局（静岡県）", "県外", {"観光案内", "自治体"}, None, True),
]

# (市町, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 2026-11-01: 小さい試算（月約21.7万円未満）は既存の記事でほぼ埋まっているので、月59〜242時間・約25.6〜84.5万円・22〜170名の範囲で、
# 空いている値を探して決めた（重化学工業の比重が大きいので、設備工事・輸送用機械の部品など規模の大きい中小・中堅を含む）
PLAN = [
    # 西部（観光統計の地域。3市）
    ("下関市", "shimonoseki", "製造業", "食料品（水産加工）", {"食料品", "水産加工"}, 110,
     "取引先に出す商品規格書（原材料・産地・アレルゲン）の作成と、製造・衛生管理の記録の取りまとめ", 17, 42),
    ("宇部市", "ube", "医療・福祉", "病院", {"医療", "病院"}, 170,
     "紹介状への返書・診療情報提供書の下書きと、入退院の説明文書の作成", 21, 38),
    ("山陽小野田市", "sanyo-onoda", "製造業", "はん用機械（ポンプ・産業機械の部品）", {"はん用機械", "機械部品"}, 85,
     "図面・仕様の問い合わせへの回答と、過去の加工実績を引いた見積書の作成", 14, 41),
    # 中部（3市）
    ("山口市", "yamaguchi-city", "運輸業・郵便業", "道路貨物運送", {"運送"}, 100,
     "配車表の下書きと、荷主への配送予定・遅延の連絡、運転日報の集計", 15, 42),
    ("防府市", "hofu", "製造業", "輸送用機械の部品（自動車部品のプレス・溶接）", {"輸送用機械", "自動車部品"}, 160,
     "取引先からの図面・仕様変更の連絡の整理と、品質記録・不具合報告書の作成", 23, 42),
    ("美祢市", "mine", "製造業", "窯業・土石製品（コンクリート製品・石灰製品）", {"窯業・土石", "コンクリート製品"}, 38,
     "見積書・出荷伝票の作成と、取引先からの納期・在庫の問い合わせへの回答", 12, 41.5),  # 2026-11-01 広島県の PLAN と重なったので変更（元 10名×41.5時間）
    # 北部（2市1町）
    ("萩市", "hagi", "宿泊・飲食サービス業", "旅館・ホテル", {"宿泊"}, 46,
     "予約・問い合わせメールへの返信の下書きと、観光・交通の案内文の作成", 14, 40.5),  # 2026-11-01 広島県の PLAN と重なったので変更（元 12名×39.5時間）
    ("長門市", "nagato", "製造業", "食料品（水産練り製品）", {"食料品", "水産練り製品"}, 50,
     "原材料・アレルゲン表示の確認と、取引先に出す商品規格書の作成", 13, 39),
    ("阿武町", "abu", "卸売業・小売業", "農産物・加工品の直売と通信販売", {"小売", "農産物の直売"}, 22,
     "通信販売の注文・配送先の取りまとめと、季節の商品案内文の作成", 7, 47),
    # 東部（4市6町）
    ("岩国市", "iwakuni", "医療・福祉", "特別養護老人ホーム", {"介護", "特別養護老人ホーム"}, 80,
     "ケア記録・夜勤の申し送りの要約と、家族への近況報告文の作成", 15, 39),
    ("周南市", "shunan", "建設業", "設備工事（化学工場の配管・機械の据え付けと設備保全）", {"設備工事", "設備保全"}, 140,
     "定期修理（工場の停止期間の工事）の作業計画書・安全書類の作成と、作業日報・点検記録の取りまとめ", 18, 46),
    ("下松市", "kudamatsu", "製造業", "輸送用機械の部品（鉄道車両の部品の加工・溶接）", {"輸送用機械", "鉄道車両部品"}, 95,
     "図面・仕様の問い合わせへの回答と、検査記録・出荷書類の作成", 14, 39.5),
    ("光市", "hikari", "製造業", "金属製品（製缶・機械部品の加工）", {"金属製品", "製缶"}, 48,
     "図面からの見積書の作成と、取引先への納期の連絡", 13, 41),
    ("柳井市", "yanai", "卸売業・小売業", "食品・日用品の小売（複数店舗）", {"小売", "食品"}, 75,
     "チラシ・売場の商品紹介文の作成と、発注・在庫の問い合わせへの回答", 14, 36.5),  # 2026-11-01 広島県の PLAN と重なったので変更（元 13名×37時間）
    ("周防大島町", "suo-oshima", "医療・福祉", "通所介護・訪問介護", {"介護", "通所介護", "訪問介護"}, 34,
     "訪問・通所の記録の清書と、ケアマネジャーへの報告文の作成", 11, 44),  # 2026-11-01 広島県の PLAN と重なったので変更（元 10名×42.5時間）
    ("和木町", "waki", "学術研究・専門技術サービス", "技術サービス（工場設備の設計・図面作成の受託）", {"設計", "図面作成"}, 26,
     "発注元の工場とのやり取りの記録の要約と、図面の変更履歴・報告書の作成", 6, 39.5),
    ("上関町", "kaminoseki", "建設業", "総合工事業", {"建設"}, 24,
     "公共工事の提出書類と、工事写真の台帳の作成", 8, 43.25),  # 2026-11-01 広島県の PLAN と重なったので変更（元 8名×44.5時間）
    ("田布施町", "tabuse", "製造業", "金属製品（板金・溶接）", {"金属製品", "板金"}, 36,
     "見積書の作成と、取引先からの納期・仕様の問い合わせへの回答", 10, 44.5),  # 2026-11-01 広島県の PLAN と重なったので変更（元 11名×41時間）
    ("平生町", "hirao", "医療・福祉", "介護老人保健施設", {"介護", "介護老人保健施設"}, 55,
     "介護記録の清書と、事故・ヒヤリハット報告書の下書き", 14, 38),  # 2026-11-01 広島県の PLAN と重なったので変更（元 13名×38時間）
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def other_plans():
    """他県の _calc.py の PLAN を読み、(県, 市町村, 削減時間, 万円) を返す。必須の県のファイルがなければ None を入れる。"""
    out = []
    for pref, label, required in OTHER_PLANS:
        path = os.path.join(ROOT, "data", "area", pref, "_calc.py")
        if not os.path.exists(path):
            if required:
                print(f"NG {label}の _calc.py がない: {path}")
                out.append(None)
            else:
                print(f"（参考）{label}の _calc.py はまだない（{path}）。できたら再実行する")
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
    return out


def existing():
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（鳥取県の _calc.py と同じ拾い方）。"""
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


def taken():
    """既存の記事と他県の PLAN で使われている (時間の dict, 万円の dict, ok) を返す（空きを探すときにも使う）。"""
    n_files, n_sec, ex_h, ex_m, ex_s, per_file = existing()
    op = other_plans()
    pl_h, pl_m = {}, {}
    for r in op:
        if r is None:
            continue
        label, city, h, m = r
        pl_h.setdefault(h, f"{label}{city}（_calc.py の PLAN）")
        pl_m.setdefault(m, f"{label}{city}（_calc.py の PLAN）")
    return (n_files, n_sec, ex_h, ex_m, ex_s, per_file), (op, pl_h, pl_m)


def main():
    (n_files, n_sec, ex_h, ex_m, ex_s, per_file), (op, pl_h, pl_m) = taken()
    empty = [k for k, v in per_file.items() if v[1] == 0]
    if empty:
        print("NG 試算の金額を拾えなかった既存の記事:", empty)
    by_pref = Counter(re.sub(r"^2026-1\d-\d+-area-([a-z]+).*", r"\1", k) for k in per_file)
    print(f"既存の地域ページ: {n_files}本（うち試算の節があるもの {n_sec}本。山梨 {by_pref.get('yamanashi', 0)}本・"
          f"島根 {by_pref.get('shimane', 0)}本・鳥取 {by_pref.get('tottori', 0)}本・広島 {by_pref.get('hiroshima', 0)}本を含む）。"
          f"拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種・規模 {len(ex_s)}種")
    ok = None not in op
    print(f"他県の PLAN: {len([r for r in op if r])}行（時間 {len(pl_h)}種・万円 {len(pl_m)}種）")

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
                print(f"  NG 山口県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 山口県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
            if csize is not None and abs(size - csize) <= csize * 0.15:
                print(f"  NG {city} の試算（{sub}・{size}名）が事例 {cname}（{'・'.join(sorted(ckeys))}・{csize}名）に近い")
                ok = False
            elif csize is None and ccity == city:
                if is_ai:
                    print(f"  NG {city} の試算（{sub}）が同じ市町の事例 {cname}（規模不明）と同じ業態")
                    ok = False
                else:
                    notes.append(f"{city}: 試算（{sub}・{size}名）と同じ業態の AI ではない事例 {cname}（規模不明）がある")
    slugs = {p[1] for p in PLAN}
    if slugs != SLUGS:
        print("NG slug が _brief.md と違う:", slugs ^ SLUGS)
        ok = False
    n_ex_size = sum(1 for p in PLAN if p[5] in ex_s)
    print(f"\n市町ページ: {len(PLAN)}（県ページには試算を入れない）、市町名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}")
    print(f"時間の範囲 {min(seen_h).normalize():f}〜{max(seen_h).normalize():f}時間、金額の範囲 約{min(seen_m)}〜{max(seen_m)}万円、規模 {min(seen_s)}〜{max(seen_s)}名")
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは山口県の中だけを NG にする）")
    print(f"（参考）時間が◯.25・◯.75になるページ: {n_quarter}件")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 19 else "NG")


if __name__ == "__main__":
    main()
