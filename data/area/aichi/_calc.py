#!/usr/bin/env python3
"""愛知県54市町村の試算の割り当てを計算し、重なりを確かめる（2026-11-11）。

data/area/nara/_calc.py を元に作った（京都・三重の _calc.py と同じ形）。県ページ（/area/aichi/）には試算を入れないので、PLAN は54行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **静岡・愛知・三重・京都の取り決め**: 月の削減時間（0.25時間刻み）×4 を4で割った余りが 1（愛知県）の時間だけを使う
     （端数が .25 の時間。data/area/_tokai/shared.md）
  1. 54ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、愛知県を除く）の「## 試算」の節の「◯時間」「◯万円」と重ならない
  3. 全県の data/area/*/_calc.py の PLAN（愛知県を除く。glob で全部読む。静岡・三重・京都・北海道を含む）の
     月の削減時間・月の時間換算額と重ならない。行頭の「PLAN = [」だけを読む。読めないファイルは警告。
     REQUIRED の県はファイルがなければ NG。**金額が重なったら先に push した府県を優先する**
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md・cases2.md の事例の会社と同じにならない（CASES と照合）
  6. slug が _brief.md の54市町村と一致する
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
  8. 県ページには試算を入れない（PLAN は54行）
  9. 仮の会社の従業員数が、その市町村の民営従業者数・選んだ中分類の従業者数（stats.md の (B)、経済センサス2021）を超えない
使い方: python3 data/area/aichi/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/aichi/_calc.py free 製造業 30 200   （余り1の時間で、既存・他県・愛知の中と重ならない時間と金額の候補を出す）
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
SELF = "aichi"
PREF_JA = "愛知県"
MOD_N, MOD_R = 4, 1  # 静岡・愛知・三重・京都の割り当て（月の削減時間×4 を4で割った余り）。愛知県は 1
N_PAGES = 54

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
    # 市（38）
    "nagoya", "toyohashi", "okazaki", "ichinomiya", "seto", "handa", "kasugai", "toyokawa", "tsushima-city", "hekinan",
    "kariya", "toyota", "anjo", "nishio", "gamagori", "inuyama", "tokoname", "konan-city", "komaki", "inazawa",
    "shinshiro", "tokai-city", "obu", "chita", "chiryu", "owariasahi", "takahama-city", "iwakura", "toyoake", "nisshin",
    "tahara", "aisai", "kiyosu", "kitanagoya", "yatomi", "miyoshi-city", "ama-city", "nagakute",
    # 町（14）
    "togo", "toyoyama", "oguchi", "fuso", "oharu", "kanie", "agui", "higashiura", "minamichita", "mihama-town-aichi",
    "taketoyo", "kota", "shitara", "toei",
    # 村（2）
    "tobishima", "toyone",
}
VILLAGES = {"tobishima", "toyone", "shitara", "toei"}  # 村と奥三河の小さい町（村と同じ参考の判定をする）

# 照合が必須の県（2026-11-11 に _calc.py がある県。静岡・三重・京都を含む）。ファイルがなければ NG。ほかに見つかった _calc.py も全部読む
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima",
            "hokkaido", "ibaraki", "tochigi", "gunma", "okinawa", "wakayama", "shiga", "nara",
            "kyoto", "mie", "shizuoka")

# cases.md・cases_outside.md・subsidy_a_areas.md・companies.md（大企業の工場・AI を作る側）の会社（2026-11-07）
# (会社名, 市町村〔県外は「県外」〕, 業態のキー, 従業員数〔(下限, 上限)。分からなければ None〕, AI の事例か〔実証・使用済み・提供側を含む〕)
# cases2.md ができたら D2 が「# cases2.md」の行に足す
# cases.md の会社（2026-11-11）。cases_outside.md・cases2.md ができたら足す
# (会社名, 市町村〔県外は「県外」〕, 業態のキー, 従業員数〔(下限, 上限)。分からなければ None〕, AI の事例か)
CASES = [
    ("野場電工（生成AIで品質管理の文書・見積、自動車用部品の加工・組立・樹脂成形、270人）", "豊田市",
     {"自動車部品", "輸送用機械", "樹脂成形", "組立"}, (270, 270), True),
    ("名古屋東部陸運（AI-OCR で配車票、本番に至らず。貨物自動車運送、550名）", "豊田市",
     {"道路貨物運送", "運送", "自動車部品輸送"}, (550, 550), True),
    ("えぷろんフーズ（AI-OCR で伝票入力、生鮮食品スーパー6店舗）", "豊田市", {"食品スーパー", "スーパー", "食料品小売"}, None, True),
    ("藤塗装工業（AI-OCR で検収、金属部品の工業塗装、114名）", "碧南市", {"塗装", "金属塗装", "表面処理"}, (114, 114), True),
    ("栄四郎瓦（県のDX補助の採択、瓦の外観検査AI）", "碧南市", {"瓦", "窯業・土石", "粘土瓦"}, None, True),
    ("中埜総合印刷（AI の生産計画を試行、印刷・食酢、265人）", "半田市", {"印刷", "食酢", "調味料"}, (265, 265), True),
    ("神谷ベルト（AI-OCR、ゴム・プラスチックの商社、30人程度）", "名古屋市", {"ゴム製品卸", "商社", "樹脂卸"}, (30, 30), True),
    ("スガキコシステムズ（需要予測AI、飲食チェーン）", "名古屋市", {"飲食チェーン", "ラーメン", "飲食店"}, None, True),
    ("ユーアイ精機（AI-OCR、プレス試作・金型、12人程度。登記は名古屋市守山区）", "尾張旭市", {"金型", "プレス加工", "試作"}, (12, 12), True),
    ("ディヴェロップ（RPA、土木・下水道工事、30人程度。AI ではない）", "岡崎市", {"土木", "総合工事業"}, (30, 30), False),
    ("スチールテック（Gemini を全社で、金型部品の金属加工・商社、47名程度）", "大府市",
     {"金型部品", "金属加工", "金属製品", "鋼材"}, (47, 47), True),
    ("愛厚ホーム大府苑（AI でシフト作成、介護。大きい法人）", "大府市", {"特別養護老人ホーム", "介護"}, None, True),
    ("春日井市民病院（生成AIで退院サマリー、市立病院）", "春日井市", {"病院"}, None, True),
    ("オーテック（保全の生成AIを自社開発、冷間鍛造・切削の自動車部品、80名）", "小牧市",
     {"自動車部品", "冷間鍛造", "切削加工", "精密部品"}, (80, 80), True),
    ("コモ（生成AIの受注の検証、ロングライフパンの製造）", "小牧市", {"パン", "食料品", "菓子"}, None, True),
    ("テルミック（Copilot、金属加工部品）", "刈谷市", {"金属加工", "金属製品", "切削加工"}, None, True),
    ("中部特殊合板（AI で NC プログラム、樹脂・合板の加工・遊技部品）", "北名古屋市", {"合板", "木材加工", "樹脂加工", "遊技部品"}, None, True),
    ("ヤマサちくわ（需要予測AI、水産練り製品）", "豊橋市", {"水産練り製品", "水産加工", "食料品"}, None, True),
    ("ドラッグストアー・カミヤ（店頭の AI 健康支援ツール、調剤薬局）", "豊橋市", {"調剤薬局", "ドラッグストア"}, None, True),
    ("伊藤金属工業（AI 外観検査、自動車部品・ボルトユニオン）", "東浦町", {"自動車部品", "金属製品", "ボルト"}, None, True),
    ("久野金属工業（部署別の生成AI、自動車部品のプレス・金型、352名。登記は名古屋市緑区）", "常滑市",
     {"プレス加工", "金型", "自動車部品"}, (352, 352), True),
    ("PTアイランド（一宮商工会議所の生成AI WG、動画作成）", "一宮市", {"動画制作", "広告"}, None, True),
    ("昌和染工（一宮商工会議所の生成AI WG、染色整理）", "一宮市", {"染色整理", "染色"}, None, True),
    ("川本鋼材（岐阜県富加町で使用済み、鋼材）", "あま市", {"鋼材", "鉄鋼卸"}, None, True),
]

# 市町村の民営従業者数と、試算に選んだ中分類の事業所数・従業者数（stats.md の各市町村の節の (B)。経済センサス 2021年6月1日、民営）
# slug: (民営従業者, 中分類, 中分類の事業所, 中分類の従業者)
STAT = {
    'nagoya': (1450337, '機械器具卸売業', 4395, 64961),
    'toyohashi': (164058, '医療業', 664, 10310),
    'okazaki': (165945, '輸送用機械器具製造業', 150, 19971),
    'ichinomiya': (140911, '繊維工業', None, 140911),
    'seto': (46247, '窯業・土石製品製造業', 424, 3158),
    'handa': (57224, '飲食店', 533, 3848),
    'kasugai': (111307, 'その他の小売業', 576, 5316),
    'toyokawa': (78350, '輸送用機械器具製造業', 147, 10506),
    'tsushima-city': (27539, '飲食料品小売業', 130, 1649),
    'hekinan': (35859, 'はん用機械器具製造業', 22, 2222),
    'kariya': (117314, '（学術研究，専門・技術サービス業）', None, 117314),
    'toyota': (247911, '道路貨物運送業', 235, 9416),
    'anjo': (107931, '輸送用機械器具製造業', 147, 20316),
    'nishio': (84341, '輸送用機械器具製造業', 136, 27526),
    'gamagori': (32958, '繊維工業', 231, 1933),
    'inuyama': (31904, '飲食店', 258, 1595),
    'tokoname': (29031, '窯業・土石製品製造業', 141, 1691),
    'konan-city': (29009, '医療業', 199, 3454),
    'komaki': (106426, '道路貨物運送業', 356, 10635),
    'inazawa': (63402, '社会保険・社会福祉・介護事業', 169, 3563),
    'shinshiro': (18731, '生産用機械器具製造業', 26, 1294),
    'tokai-city': (60069, '道路貨物運送業', 119, 3720),
    'obu': (49471, '生産用機械器具製造業', 109, 4727),
    'chita': (20235, '飲食料品小売業', 93, 1383),
    'chiryu': (24713, '機械器具卸売業', 40, 1490),
    'owariasahi': (23688, '社会保険・社会福祉・介護事業', 132, 2125),
    'takahama-city': (21945, 'プラスチック製品製造業（別掲を除く）', 16, 1119),
    'iwakura': (14538, '道路貨物運送業', 34, 1126),
    'toyoake': (28656, '医療業', 117, 4327),
    'nisshin': (30868, '社会保険・社会福祉・介護事業', 125, 2371),
    'tahara': (30094, 'その他の小売業', 210, 1274),
    'aisai': (17830, '社会保険・社会福祉・介護事業', 85, 1820),
    'kiyosu': (28969, '食料品製造業', 35, 1431),
    'kitanagoya': (32493, '医療業', 136, 1787),
    'yatomi': (22293, '道路貨物運送業', 111, 2511),
    'miyoshi-city': (33410, '生産用機械器具製造業', 49, 1348),
    'ama-city': (25499, '食料品製造業', 26, 1341),
    'nagakute': (27217, 'その他の小売業', 141, 1830),
    'togo': (15421, '金属製品製造業', 38, 1474),
    'toyoyama': (14417, '飲食料品卸売業', 112, 2087),
    'oguchi': (27086, '生産用機械器具製造業', 42, 4768),
    'fuso': (9238, '飲食店', 129, 1057),
    'oharu': (8613, '社会保険・社会福祉・介護事業', 25, 698),
    'kanie': (13688, '飲食店', 180, 1423),
    'agui': (9697, '飲食料品小売業', 61, 1108),
    'higashiura': (17191, '家具・装備品製造業', 11, 851),
    'minamichita': (7045, '宿泊業', 133, 1213),
    'mihama-town-aichi': (8501, '食料品製造業', 15, 591),
    'taketoyo': (13918, '社会保険・社会福祉・介護事業', 36, 972),
    'kota': (20163, '輸送用機械器具製造業', 21, 2602),
    'shitara': (1675, '社会保険・社会福祉・介護事業', 9, 246),
    'toei': (1064, '総合工事業', 21, 121),
    'tobishima': (11606, '運輸に附帯するサービス業', 91, 1682),
    'toyone': (496, '総合工事業', 11, 115),
}

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])（奈良と同じ9列）
# 業種・業態は stats.md の各市町村の「(B) 中小企業の業種の候補」から選んだ。(A) 大企業の工場と読める業種
# （豊田市・田原市などの輸送用機械の大きな工場、東海市の鉄鋼、安城市・幸田町の電気機械、知多市の石油製品など）は
# 工場の値と読めない業態（下請けの小さい部品加工・物流・卸など）にした。農業・漁業・林業は試算の業種にしない。
PLAN = [
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
            print(f"  NG {city} の時間 {h} は東海・京都の割り当て（×4 を{MOD_N}で割った余り {MOD_R}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 愛知県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 愛知県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは愛知県の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == N_PAGES else "NG")


def free(ind, lo, hi):
    """業種 ind で、lo〜hi 時間の空いている（時間, 万円）を並べる（余り1の時間だけ）"""
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
