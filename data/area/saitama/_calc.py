#!/usr/bin/env python3
"""埼玉県63市町村の試算の割り当てを計算し、重なりを確かめる（2026-11-13）。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

取り決め（2026-11-11 ユーザー決定）: **他県との重なりは許容し、埼玉県の中だけ時間・金額・規模を重ねない**。
他県の記事・PLAN と重なったものは参考として表示するだけ（NG にしない）。

確かめること（NG になるもの）:
  1. 63ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  3. slug が _brief.md の63市町村と一致する（県ページには試算を入れないので PLAN は63行）
  4. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
  5. 対象人数が従業員数より少なく、1人の月の業務量が 10〜60 時間
  6. 試算の業態・規模が事例の会社（CASES）と同じにならない（業態のキーが重なり、従業員数が ±30% 以内なら NG）
  7. 従業員数が、その市町村の民営従業者数（STAFF_LIMIT、stats.md の経済センサス2021）を超えない
使い方: python3 -B data/area/saitama/_calc.py            （末尾に OK / NG）
        python3 -B data/area/saitama/_calc.py free 製造業 30 200 （埼玉の中で使っていない時間と金額の候補を出す）
"""
import sys

sys.dont_write_bytecode = True

import glob  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
from collections import Counter  # noqa: E402
from decimal import Decimal, ROUND_HALF_UP  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ART = os.path.join(ROOT, "articles")

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

SLUGS = {
    "saitama-city", "kawaguchi", "warabi", "toda", "asaka", "shiki", "wako", "niiza", "fujimi-city", "fujimino",
    "miyoshi-town", "konosu", "ageo", "okegawa", "kitamoto", "ina-town", "kasukabe", "soka", "koshigaya", "yashio",
    "misato-city", "yoshikawa", "matsubushi", "gyoda", "kazo", "hanyu", "kuki", "hasuda", "satte", "shiraoka",
    "miyashiro", "sugito", "tokorozawa", "hanno", "sayama", "iruma", "hidaka-city", "kawagoe", "higashimatsuyama",
    "sakado", "tsurugashima", "moroyama", "ogose", "namegawa", "ranzan", "ogawa-town", "kawajima", "yoshimi",
    "hatoyama", "tokigawa", "higashichichibu", "kumagaya", "honjo", "fukaya", "misato-town-saitama", "kamikawa-town",
    "kamisato", "yorii", "chichibu", "yokoze", "minano", "nagatoro", "ogano",
}

# slug → 民営従業者数（経済センサス2021、stats.md）。D1 が埋める。空なら判定しない
STAFF_LIMIT = {}

# 事例の会社（cases.md・cases2.md・cases_outside.md）: (会社, 業態のキーの集合, 従業員数)
CASES = [
    ("日本精密金型", {"金型", "金属製品"}, 44),
    ("セントラルサービス", {"清掃", "ビルメンテナンス"}, 15),
    ("らしく", {"文書検索"}, 3),
    ("尼高運輸", {"倉庫", "流通加工"}, None),
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
PLAN = [
]


def man(yen):
    return Decimal(yen / 10000).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def calc(row):
    _, _, ind, _, _, staff, _, n, hrs = row
    hours = n * hrs * 0.25
    yen = hours * RATE[ind]
    return hours, yen


def others():
    """他県の記事の試算の時間・金額（参考表示用）"""
    hs, ys = Counter(), Counter()
    for p in glob.glob(os.path.join(ART, "2026-1?-*-area-*.md")):
        if "-area-saitama" in p:
            continue
        s = open(p, encoding="utf-8").read()
        m = re.search(r"\n## 試算.*?(?=\n## )", s, re.S)
        if not m:
            continue
        sec = m.group(0)
        for h in re.findall(r"月(?:の削減時間)?[^\n|]*?\|\s*約?([\d,.]+)時間", sec):
            hs[float(h.replace(",", ""))] += 1
        for y in re.findall(r"約([\d,.]+)万円", sec):
            ys[y.replace(",", "")] += 1
    return hs, ys


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "free":
        return free(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    ng = []
    slugs = [r[1] for r in PLAN]
    if set(slugs) != SLUGS or len(slugs) != len(SLUGS):
        miss = SLUGS - set(slugs)
        extra = set(slugs) - SLUGS
        dup = [s for s, c in Counter(slugs).items() if c > 1]
        ng.append(f"slug が一致しない: 足りない {sorted(miss)} / 余分 {sorted(extra)} / 重複 {dup}")
    hours_c, man_c, staff_c = Counter(), Counter(), Counter()
    oh, oy = others()
    rows = []
    for r in PLAN:
        name, slug, ind, gyotai, keys, staff, task, n, hrs = r
        if ind not in RATE:
            ng.append(f"{name}: 業種 {ind} が wages.md にない")
            continue
        h, y = calc(r)
        if abs(h * 4 - round(h * 4)) > 1e-9:
            ng.append(f"{name}: 時間 {h} が0.25刻みでない")
        frac = (y / 10000 * 100) % 10  # 0.01万円単位の端数
        if abs(frac - 5) * 100 < 100:  # 境目 ◯.◯5万円 から100円以内
            ng.append(f"{name}: 金額 {y:.0f}円 が四捨五入の境目に近い")
        if not (n < staff):
            ng.append(f"{name}: 対象人数 {n} が従業員数 {staff} 以上")
        if not (10 <= hrs <= 60):
            ng.append(f"{name}: 1人の月の業務量 {hrs} 時間が範囲外")
        lim = STAFF_LIMIT.get(slug)
        if lim and staff > lim:
            ng.append(f"{name}: 従業員数 {staff} が民営従業者数 {lim} を超える")
        for cn, ck, cs in CASES:
            if keys & ck and (cs is None or abs(staff - cs) <= cs * 0.3):
                ng.append(f"{name}: 事例の会社 {cn} と業態・規模が近い")
        hours_c[h] += 1
        man_c[str(man(y))] += 1
        staff_c[staff] += 1
        rows.append((name, slug, ind, staff, n, hrs, h, man(y)))
    for name, slug, ind, staff, n, hrs, h, m in rows:
        dup = []
        if hours_c[h] > 1:
            dup.append("時間")
        if man_c[str(m)] > 1:
            dup.append("金額")
        if staff_c[staff] > 1:
            dup.append("従業員数")
        if dup:
            ng.append(f"{name}: 埼玉の中で {'・'.join(dup)} が重なる")
        ref = []
        if oh.get(h):
            ref.append(f"時間は他県の記事{oh[h]}本と同じ")
        if oy.get(str(m)):
            ref.append(f"金額は他県の記事{oy[str(m)]}本と同じ")
        print(f"{name}\t{slug}\t{ind}\t{staff}名\t{n}人×{hrs}h\t月{h:g}時間\t約{m}万円" + (f"\t（参考: {'・'.join(ref)}）" if ref else ""))
    for x in ng:
        print("NG:", x)
    print("OK" if not ng else f"NG {len(ng)}件")
    return 0 if not ng else 1


def free(ind, lo, hi):
    used_h = {calc(r)[0] for r in PLAN}
    used_m = {str(man(calc(r)[1])) for r in PLAN}
    out = 0
    for q in range(lo * 4, hi * 4 + 1):
        h = q / 4
        y = h * RATE[ind]
        m = str(man(y))
        frac = (y / 10000 * 100) % 10
        if h in used_h or m in used_m or abs(frac - 5) * 100 < 100:
            continue
        print(f"月{h:g}時間\t約{m}万円")
        out += 1
        if out > 60:
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
