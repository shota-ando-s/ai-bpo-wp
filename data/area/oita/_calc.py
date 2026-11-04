#!/usr/bin/env python3
"""大分県18市町村の試算の割り当てを計算し、重なりを確かめる（2026-11-04）。

data/area/okayama/_calc.py を元に作った。県ページ（/area/oita/）には試算を入れないので、PLAN は18行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる。

確かめること:
  0. **九州7県の割り当て**: 月の削減時間×4 を7で割った余りが 4（大分県）になる時間だけを使う
  1. 18ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（大分県を除く）の「## 試算」の節の「◯時間」「◯万円」の値と重ならない
  3. 山梨・島根・鳥取・山口・広島・岡山の _calc.py の PLAN（必須）と、九州の他県の _calc.py の PLAN（push されていれば）と重ならない
  4. 時間は0.25時間刻み。金額が四捨五入の境目にならない
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md の事例の会社と同じにならない（CASES と照合）
  6. slug が _brief.md の18市町村と一致する（大分市は oita-city）
  7. 試算の業種が wages.md にある
使い方: python3 data/area/oita/_calc.py   （末尾に OK / NG を出す）
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
SELF = "oita"
KYUSHU_MOD = 4  # 九州7県の割り当て（月の削減時間×4 を7で割った余り）

# wages.md の人件費時給（時給①×1.2 を十円単位に丸めた値。記事でも「約◯円」と書く値）。
# 山口県の PLAN が不動産・学術研究・情報通信を使っているので、他県の PLAN を読むために9業種とも入れる
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

SLUGS = {"oita-city", "beppu", "nakatsu", "hita", "saiki", "usuki", "tsukumi", "taketa", "bungotakada", "kitsuki",
         "usa", "bungoono", "yufu", "kunisaki", "hiji", "kokonoe", "kusu", "himeshima"}

# 照合する他県の PLAN（公開前の割り当て）。5県とも必須
OTHER_PLANS = (("yamanashi", "山梨県"), ("shimane", "島根県"), ("tottori", "鳥取県"),
               ("yamaguchi", "山口県"), ("hiroshima", "広島県"), ("okayama", "岡山県"))
# 九州の他県（並行で作成中）。_calc.py が push されていれば照合する（なければ飛ばす）。git pull してから実行する
KYUSHU_PLANS = (("fukuoka", "福岡県"), ("saga", "佐賀県"), ("nagasaki", "長崎県"), ("kumamoto", "熊本県"),
                ("miyazaki", "宮崎県"), ("kagoshima", "鹿児島県"))

# cases.md の事例の会社（2026-11-03 の cases.md から）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・使用済みを含む〕)
# cases_outside.md（完成版）と cases2.md の会社は 2026-11-03 に D2 が足した
CASES = [
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 2026-11-03: 既存の地域ページ（642本）と5県の PLAN（109行）で、月約21.7万円未満と、1人の業務量を◯.0・◯.5時間にした
# 小さい組（対象5〜10名）の値はほぼ埋まっている。空いている値を探して決めた（月53.75〜231時間・約23.2万〜81.8万円・12〜175名）。
# 業種・業態は stats.md の「市町村ごとの主要産業の候補」の (B) 中小企業の業種（経済センサスの事業所数・従業者数）から選んだ。
# 新庄村・久米南町だけ1人の業務量が◯.25・◯.75時間（ほかに空きがない。D1.md の判断が必要な点）
PLAN = [
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def other_plans():
    """5県の _calc.py の PLAN を読み、(県, 市町村, 削減時間, 万円) を返す。ファイルがなければ None を入れる（NG）。"""
    out = []
    for pref, label in OTHER_PLANS + KYUSHU_PLANS:
        path = os.path.join(ROOT, "data", "area", pref, "_calc.py")
        if not os.path.exists(path) and (pref, label) in KYUSHU_PLANS:
            print(f"（参考）{label}の _calc.py はまだない")
            continue
        if not os.path.exists(path):
            print(f"NG {label}の _calc.py がない: {path}")
            out.append(None)
            continue
        src = open(path, encoding="utf-8").read()
        i = src.index("PLAN = [")
        j = src.index("\n]\n", i)
        rows = ast.literal_eval(src[i + 7:j + 2])
        n_skip = 0
        for r in rows:
            city, ind, n, hrs = r[0], r[2], r[-2], r[-1]
            if ind not in RATE:
                n_skip += 1
                continue
            h = Decimal(str(n)) * Decimal(str(hrs)) * Decimal("0.25")
            out.append((label, city, h, man(h * RATE[ind])))
        if n_skip:
            print(f"NG {label}の PLAN に時給の分からない業種が {n_skip}行ある（RATE に足す）")
            out.append(None)
    return out


def existing():
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（鳥取県・広島県の _calc.py と同じ拾い方）。"""
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
          f"島根 {by_pref.get('shimane', 0)}本・鳥取 {by_pref.get('tottori', 0)}本・広島 {by_pref.get('hiroshima', 0)}本・"
          f"山口 {by_pref.get('yamaguchi', 0)}本を含む）。拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種・規模 {len(ex_s)}種")
    op = other_plans()
    ok = None not in op
    pl_h, pl_m = {}, {}
    for r in op:
        if r is None:
            continue
        label, city, h, m = r
        pl_h.setdefault(h, f"{label}{city}（_calc.py の PLAN）")
        pl_m.setdefault(m, f"{label}{city}（_calc.py の PLAN）")
    print(f"他県の PLAN: {len([r for r in op if r])}行（時間 {len(pl_h)}種・万円 {len(pl_m)}種）")
    if os.path.exists(os.path.join(HERE, "cases_outside.md")):
        print("（注意）cases_outside.md がある。県外の会社（業態・従業員数）を CASES に足したか確かめる")

    seen_h, seen_m, seen_s = {}, {}, {}
    n_quarter = 0
    notes = []
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | 年間 |")
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
                print(f"  NG 大分県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 大分県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
            ok = False
        seen_s[size] = city
        if (h * 4) % 1 == 0 and int(h * 4) % 7 != KYUSHU_MOD:
            print(f"  NG {city} の時間 {h} は九州の割り当て（×4 を7で割った余り {KYUSHU_MOD}）に合わない（余り {int(h * 4) % 7}）")
            ok = False
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
                if (csize is not None and in_range(size, csize)) or (csize is None and ccity == city):
                    notes.append(f"{city}: 試算（{sub}・{size}名）と業態が近い AI ではない事例 {cname}（{csize or '規模不明'}）")
                continue
            if csize is not None and in_range(size, csize):
                print(f"  NG {city} の試算（{sub}・{size}名）が事例 {cname}（{'・'.join(sorted(ckeys))}・{csize[0]}〜{csize[1]}名）に近い")
                ok = False
            elif csize is None and ccity == city:
                print(f"  NG {city} の試算（{sub}）が同じ市町村の事例 {cname}（規模不明）と同じ業態")
                ok = False
    slugs = {p[1] for p in PLAN}
    if slugs != SLUGS:
        print("NG slug が _brief.md と違う:", slugs ^ SLUGS)
        ok = False
    if not PLAN:
        print("NG PLAN が空")
        print("NG")
        return
    n_ex_size = sum(1 for p in PLAN if p[5] in ex_s)
    print(f"\n市町村ページ: {len(PLAN)}、市町村名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}")
    print(f"時間の範囲 {min(seen_h)}〜{max(seen_h)}時間、金額の範囲 約{min(seen_m)}〜{max(seen_m)}万円、規模 {min(seen_s)}〜{max(seen_s)}名")
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは大分県の中だけを NG にする）")
    print(f"（参考）時間が◯.25・◯.75になるページ: {n_quarter}件")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 18 else "NG")


if __name__ == "__main__":
    main()
