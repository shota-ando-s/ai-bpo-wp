#!/usr/bin/env python3
"""島根県19市町村＋県ページの試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-10-31）。

data/area/nagano/_calc.py を元に作った。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  1. 20ページ（19市町村＋県ページ）の中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-10-*-area-*.md、島根県を除く。長野県の77本・県ページを含む）の
     「## 試算」の節に出てくる「◯時間」「◯万円」の値と重ならない。拾い方は長野県の _calc.py と同じ
     （1人の業務量・年間の額・差し引き後の額なども広めに拾う。拾いすぎは「重ならない」側に働く）
  3. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円ちょうど）にならない
  4. 試算の業種（業態）・規模が cases.md・cases_outside.md の事例の会社と同じにならない（CASES と照合）
     - 業態のキーが重なり、従業員数が事例の±15%以内 → NG
     - 業態のキーが重なり、同じ市町村で、事例の従業員数が分からない AI の事例 → NG（その会社の値と読まれるため）
     - 同じ市町村・同じ業態で、AI ではない事例（規模不明） → 参考として表示（NG にしない）
  5. slug が _brief.md の19市町村と一致する
使い方: python3 data/area/shimane/_calc.py   （末尾に OK / NG を出す）
"""
import glob
import os
import re
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ART = os.path.join(ROOT, "articles")

# wages.md の人件費時給（時給①×1.2 を十円単位に丸めた値。記事でも「約◯円」と書く値）
RATE = {
    "製造業": 3500,
    "卸売業・小売業": 3540,
    "建設業": 3520,
    "運輸業・郵便業": 2980,
    "医療・福祉": 3180,
    "宿泊・飲食サービス業": 2510,
}

SLUGS = {"matsue", "hamada", "izumo", "masuda", "oda", "yasugi", "gotsu", "unnan", "okuizumo", "iinan",
         "kawamoto", "misato-town-shimane", "onan", "tsuwano", "yoshika", "ama", "nishinoshima", "chibu",
         "okinoshima"}

# cases.md・cases_outside.md の事例の会社
# (会社名, 市町村〔県外は「県外」〕, 業態のキー, 従業員数〔分からなければ None〕, AI の事例か)
CASES = [
    # cases.md（島根県内）
    ("みしまや", "松江市", {"小売", "スーパー"}, None, True),          # 民間DBの253名は使わない
    ("中浦食品", "松江市", {"食料品", "菓子"}, 185, True),
    ("高橋産業", "松江市", {"業種未確認"}, None, True),
    ("長岡塗装店", "松江市", {"建設"}, 24, True),
    ("TSKエンタープライズDC", "松江市", {"コンテンツ制作"}, 49, True),
    ("サンテクノス", "松江市", {"非破壊検査"}, None, True),
    ("明石屋", "松江市", {"卸売"}, None, True),
    ("コダマ（計画）", "松江市", {"鋳造"}, 51, True),
    ("まつくる（計画）", "松江市", {"まちづくり"}, 5, True),
    ("モルツウェル（AIカメラを断念）", "松江市", {"食料品"}, 130, False),
    ("浅利観光（AIではない）", "松江市", {"宿泊"}, None, False),
    ("宮本食肉店（AIではない）", "松江市", {"食料品"}, None, False),
    ("ダイハツメタル 出雲工場", "出雲市", {"鋳造", "輸送用機械"}, 558, True),
    ("ダイハツメタル（全社）", "出雲市", {"鋳造", "輸送用機械"}, 956, True),
    ("出雲東郷電機", "出雲市", {"電気機械"}, None, True),
    ("イーシーアイ", "出雲市", {"小売"}, None, True),
    ("津山屋製菓", "出雲市", {"食料品", "菓子"}, 90, True),
    ("山陰ヤクルト販売（計画）", "出雲市", {"卸売", "食料品"}, 110, True),
    ("城東化成", "安来市", {"プラスチック", "ゴム"}, 151, True),
    ("ナカサ", "安来市", {"金属製品", "板金"}, 120, True),
    ("Ton-ton（AIではない）", "安来市", {"食料品"}, None, False),
    ("ガット（県の資料）", "奥出雲町", {"金属加工", "精密機械加工"}, 24, True),
    ("ガット（ITOC の事例シート）", "奥出雲町", {"金属加工", "精密機械加工"}, 27, True),
    ("ニッポー 島根工場（AIではない）", "奥出雲町", {"農業用機器"}, 109, False),
    ("アルプロン", "雲南市", {"食料品", "健康食品"}, None, True),
    ("ゼンキンメタル（AIではない）", "雲南市", {"金属製品", "板金"}, None, False),
    ("シバオ", "大田市", {"窯業・土石", "瓦"}, None, True),
    ("大田市の社会福祉法人（計画）", "大田市", {"介護", "特別養護老人ホーム"}, None, True),
    ("山﨑組（AIではない）", "大田市", {"建設", "解体"}, 40, False),
    ("丸惣", "江津市", {"窯業・土石", "瓦"}, None, True),
    ("しちだ・教育研究所（研究）", "江津市", {"教育"}, None, True),
    ("千曲", "益田市", {"小売", "自動販売機"}, 9, True),
    ("出雲ポンプ（AIではない）", "益田市", {"消防設備"}, None, False),
    ("タカハシ包装センター（AIではない）", "浜田市", {"卸売", "包装資材"}, 189, False),
    ("デルタ・シー・アンド・エス（AIではない）", "浜田市", {"繊維", "縫製"}, 191, False),
    # cases_outside.md（県外）
    ("カワトT.P.C.（岩国市）", "県外", {"プラスチック", "配管"}, 340, True),
    ("カワトT.P.C.（県の紹介ページ）", "県外", {"プラスチック", "配管"}, 324, True),
    ("内能美漁協ほか（江田島市）", "県外", {"漁業", "養殖"}, None, True),
    ("アイグラン（広島市）", "県外", {"保育"}, 3188, True),
    ("ひびき精機（下関市）", "県外", {"金属加工", "精密機械加工"}, 100, False),
    ("美東電子（美祢市）", "県外", {"農業", "きのこ"}, 126, False),
    ("岡山ダイハツ販売", "県外", {"小売", "自動車販売"}, 412, True),
    ("宮崎トヨタ自動車", "県外", {"小売", "自動車販売"}, None, True),
    ("ニチワ（日南市）", "県外", {"製造"}, 150, False),
    ("サニー・シーリング（都城市）", "県外", {"印刷"}, None, True),
    ("中国芝浦電子", "県外", {"電子部品"}, None, True),
    ("旭酒造（岩国市）", "県外", {"食料品", "酒"}, None, True),
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
PLAN = [
    # 出雲地域（松江圏・出雲圏・雲南圏）
    ("松江市", "matsue", "宿泊・飲食サービス業", "温泉旅館・ホテル", {"宿泊"}, 118,
     "海外の旅行会社・個人客からの問い合わせメールへの返信の下書きと、宿泊プラン・館内案内の多言語の説明文の作成", 16, 31),
    ("出雲市", "izumo", "卸売業・小売業", "青果・農産物の卸売", {"卸売", "青果"}, 64,
     "取引先からの受注メール・FAXの入力と、入荷・相場の案内文の作成", 12, 31),
    ("安来市", "yasugi", "運輸業・郵便業", "道路貨物運送", {"運送"}, 52,
     "配車表の下書きと、荷主への運行・到着の連絡", 10, 25.5),
    ("雲南市", "unnan", "製造業", "金属製品（機械部品の加工）", {"金属製品"}, 43,
     "図面・仕様の問い合わせへの回答と、過去の加工実績を引いた見積書の作成", 9, 35),
    ("奥出雲町", "okuizumo", "卸売業・小売業", "米・農産物の直売と通信販売", {"小売", "米"}, 11,
     "通信販売の注文の取りまとめと、季節の商品案内文の作成", 2, 7.5),
    ("飯南町", "iinan", "製造業", "食料品（農産物の加工）", {"食料品", "農産加工"}, 26,
     "原材料・アレルゲン表示の確認と、取引先に出す商品規格書の作成", 6, 34.5),
    # 石見地域（大田圏・浜田圏・益田圏）
    ("浜田市", "hamada", "製造業", "食料品（水産加工）", {"食料品", "水産加工"}, 72,
     "取引先に出す商品規格書（原材料・産地・アレルゲン）の作成と、製造・衛生管理の記録の取りまとめ", 14, 35),
    ("益田市", "masuda", "卸売業・小売業", "建築資材・農業資材の卸売", {"卸売", "建築資材"}, 46,
     "商品の在庫・納期の問い合わせへの回答と、見積書の作成", 9, 25),
    ("大田市", "oda", "製造業", "食料品", {"食料品"}, 33,
     "取引先からの受注・出荷の連絡と、製造ロット・賞味期限の記録の整理", 9, 33),
    ("江津市", "gotsu", "医療・福祉", "特別養護老人ホーム", {"介護", "特別養護老人ホーム"}, 62,
     "ケア記録・夜勤の申し送りの要約と、家族への近況報告文の作成", 12, 29),
    ("川本町", "kawamoto", "運輸業・郵便業", "道路貨物運送", {"運送"}, 14,
     "運転日報の集計と、荷主への配送予定の連絡", 2, 18.5),
    ("美郷町", "misato-town-shimane", "建設業", "総合工事業", {"建設"}, 12,
     "工事写真の台帳と、発注者に出す工事書類の作成", 1, 17),
    ("邑南町", "onan", "医療・福祉", "介護老人保健施設・通所介護", {"介護", "介護老人保健施設"}, 58,
     "介護記録の清書と、事故・ヒヤリハット報告書の下書き", 11, 23),
    ("津和野町", "tsuwano", "卸売業・小売業", "土産物・食品の小売", {"小売", "土産"}, 16,
     "観光客からの問い合わせへの回答と、商品の説明文の作成", 1, 11),
    ("吉賀町", "yoshika", "医療・福祉", "診療所・訪問看護", {"医療", "訪問看護"}, 21,
     "訪問記録の要約と、主治医・ケアマネジャーへの報告書の下書き", 6, 35.5),
    # 隠岐地域（隠岐圏）
    ("海士町", "ama", "製造業", "食料品（水産加工）", {"食料品", "水産加工"}, 13,
     "島外の取引先からの注文・出荷の連絡と、商品規格書の作成", 2, 26.5),
    ("西ノ島町", "nishinoshima", "宿泊・飲食サービス業", "旅館・民宿", {"宿泊"}, 8,
     "予約・問い合わせへの返信と、船・飛行機の欠航時の連絡文の作成", 2, 9.5),
    ("知夫村", "chibu", "宿泊・飲食サービス業", "民宿", {"宿泊"}, 4,
     "予約メールへの返信と、島内の案内文の作成", 1, 13),
    ("隠岐の島町", "okinoshima", "建設業", "総合工事業", {"建設"}, 47,
     "公共工事の提出書類と、工事日報の取りまとめ", 9, 31),
    # 県ページ（試算を入れるかは判断が必要な点。入れるときの割り当て）
    ("島根県（県ページ）", "shimane", "医療・福祉", "介護事業所を複数運営する法人", {"介護"}, 80,
     "介護記録・申し送りの要約と、職員研修・会議の記録の作成", 14, 33),
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def existing():
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（長野県の _calc.py と同じ拾い方）。"""
    hours, mans, sizes, per_file = {}, {}, {}, {}
    files = [f for f in sorted(glob.glob(os.path.join(ART, "2026-10-*-area-*.md"))) if "-area-shimane" not in f]
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


def main():
    n_files, n_sec, ex_h, ex_m, ex_s, per_file = existing()
    empty = [k for k, v in per_file.items() if v[1] == 0]
    if empty:
        print("NG 試算の金額を拾えなかった既存の記事:", empty)
    print(f"既存の地域ページ: {n_files}本（うち試算の節があるもの {n_sec}本）。拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種・規模 {len(ex_s)}種")

    ok = True
    seen_h, seen_m, seen_s = {}, {}, {}
    n_quarter = 0
    notes = []
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | 年間 |")
    print("|---|---|---|---|---|---|---|---|")
    for (city, slug, ind, sub, keys, size, task, n, hrs) in PLAN:
        h = Decimal(str(n)) * Decimal(str(hrs)) * Decimal("0.25")
        yen = h * RATE[ind]
        m = man(yen)
        y = man(yen * 12)
        print(f"| {city} | {ind}（{sub}） | {size}名 | {n}名×{hrs}時間×25% | {h.normalize():f}時間 | 約{RATE[ind]:,}円 | 約{m}万円 | 約{y}万円 |")
        for label, key, seen, exd in (("時間", h, seen_h, ex_h), ("金額", m, seen_m, ex_m)):
            if key in seen:
                print(f"  NG 島根県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 島根県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
            if not (keys & ckeys):
                continue
            if csize is not None and abs(size - csize) <= csize * 0.15:
                print(f"  NG {city} の試算（{sub}・{size}名）が事例 {cname}（{'・'.join(sorted(ckeys))}・{csize}名）に近い")
                ok = False
            elif csize is None and ccity == city:
                if is_ai:
                    print(f"  NG {city} の試算（{sub}）が同じ市町村の事例 {cname}（規模不明）と同じ業態")
                    ok = False
                else:
                    notes.append(f"{city}: 試算（{sub}・{size}名）と同じ業態の AI ではない事例 {cname}（規模不明）がある")
    pages = [p for p in PLAN if p[1] != "shimane"]
    slugs = {p[1] for p in pages}
    if slugs != SLUGS:
        print("NG slug が _brief.md と違う:", slugs ^ SLUGS)
        ok = False
    n_ex_size = sum(1 for p in PLAN if p[5] in ex_s)
    print(f"\n市町村ページ: {len(pages)}（＋県ページ {len(PLAN) - len(pages)}）、市町村名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}")
    print(f"時間の範囲 {min(seen_h)}〜{max(seen_h)}時間、金額の範囲 約{min(seen_m)}〜{max(seen_m)}万円、規模 {min(seen_s)}〜{max(seen_s)}名")
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは島根県の中だけを NG にする）")
    print(f"（参考）時間が◯.25・◯.75になるページ: {n_quarter}件")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(pages) == 19 else "NG")


if __name__ == "__main__":
    main()
