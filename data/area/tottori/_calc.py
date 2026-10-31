#!/usr/bin/env python3
"""鳥取県19市町村＋県ページの試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-10-31）。

data/area/shimane/_calc.py を元に作った。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  1. 20ページ（19市町村＋県ページ）の中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-10-*-area-*.md、鳥取県を除く。島根県・山梨県の記事を含む）の
     「## 試算」の節に出てくる「◯時間」「◯万円」の値と重ならない。拾い方は島根県の _calc.py と同じ
     （1人の業務量・年間の額・差し引き後の額なども広めに拾う。拾いすぎは「重ならない」側に働く）
  3. 山梨県（data/area/yamanashi/_calc.py）と島根県（data/area/shimane/_calc.py）の PLAN の
     月の削減時間・月の時間換算額とも重ならない（公開前の割り当て。ファイルを読んで照合する）
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円ちょうど）にならない
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md の事例の会社と同じにならない（CASES と照合）
     - 業態のキーが重なり、従業員数が事例の±15%以内 → NG
     - 業態のキーが重なり、同じ市町村で、事例の従業員数が分からない AI の事例 → NG（その会社の値と読まれるため）
     - 業種が確かめられていない AI の事例（キー「業種未確認」）と同じ市町村 → 参考として表示（NG にしない）
     - 同じ市町村・同じ業態で、AI ではない事例（規模不明） → 参考として表示（NG にしない）
  6. slug が _brief.md の19市町村と一致する
  7. 試算の業種が wages.md にある（農業・漁業は試算の業種にしない）
使い方: python3 data/area/tottori/_calc.py   （末尾に OK / NG を出す）
"""
import ast
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

SLUGS = {"tottori-city", "yonago", "kurayoshi", "sakaiminato", "iwami", "wakasa", "chizu", "yazu", "misasa",
         "yurihama", "kotoura", "hokuei", "daisen", "nanbu", "hoki", "nichinan", "hino", "kofu", "hiezu"}

# cases.md・cases_outside.md の事例の会社
# (会社名, 市町村〔県外は「県外」〕, 業態のキー, 従業員数〔分からなければ None〕, AI の事例か)
# cases_outside.md は 2026-10-31 の下書きの時点で未作成。できたら県外の行を足して再実行する
CASES = [
    # cases.md（鳥取県内）
    ("イングス", "鳥取市", {"介護", "デイサービス"}, 50, True),              # 「職員数約50名」（支援した会社のページ）
    ("気高電機", "鳥取市", {"電気機械", "家電"}, None, True),                # 232名は求人サイト（verified: false）なので使わない
    ("田中製作所", "鳥取市", {"金属製品", "金属プレス"}, None, True),
    ("産業技術センターの支援事例（社名なし、ベニヤ板）", "鳥取市", {"木材・木製品"}, None, True),
    ("やまこう建設（モデル企業）", "鳥取市", {"建設"}, None, True),
    ("聖和精機（AIではない）", "鳥取市", {"金属製品", "機械部品"}, None, False),
    ("鳥取最上インクス（AIではない）", "鳥取市", {"業種未確認"}, None, False),
    ("健康エキス", "米子市", {"食料品", "エキス"}, None, True),
    ("菊水フォージング（モデル企業）", "米子市", {"鍛造", "金属製品"}, None, True),
    ("ニッポン高度紙工業（AIではない）", "米子市", {"パルプ・紙"}, None, False),
    ("グッドスマイルカンパニー 楽月工場", "倉吉市", {"フィギュア", "プラスチック製品"}, 200, True),
    ("明治製作所", "倉吉市", {"業種未確認"}, None, True),
    ("JA鳥取中央（すいか・梨の選果）", "倉吉市", {"農協", "選果", "果物の集出荷"}, None, True),
    ("いないホールディングス（モデル企業）", "倉吉市", {"業種未確認"}, None, True),
    ("バルコス（モデル企業）", "倉吉市", {"業種未確認"}, None, True),
    ("モリタ製作所（AIではない）", "倉吉市", {"金属製品", "旋盤加工"}, None, False),
    ("片木アルミニューム製作所 大山工場", "大山町", {"非鉄金属", "アルミ"}, None, True),
    ("鳥取クリエイティブ研究所（計画）", "八頭町", {"情報サービス", "ドローン"}, None, True),
    ("新興螺子（AIではない）", "北栄町", {"金属製品", "ねじ"}, None, False),
    ("大山乳業農業協同組合（AIではない）", "琴浦町", {"食料品", "乳製品"}, None, False),
    ("千代電子工業（AIではない）", "智頭町", {"電子部品"}, None, False),
    ("TVC（モデル企業、所在未確認）", "所在未確認", {"業種未確認"}, None, True),
    ("馬野建設（BIM/CIM、AIではない）", "東伯郡", {"建設"}, None, False),
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
PLAN = [
    # 東部地区（5）
    ("鳥取市", "tottori-city", "製造業", "食料品（菓子・農産物の加工）", {"食料品", "菓子", "農産加工"}, 95,
     "取引先に出す商品規格書（原材料・アレルゲン）の作成と、製造ロット・賞味期限の記録の取りまとめ", 16, 40),
    ("岩美町", "iwami", "建設業", "総合工事業", {"建設"}, 35,
     "公共工事の提出書類と、工事写真の台帳の作成", 9, 41),
    ("若桜町", "wakasa", "宿泊・飲食サービス業", "旅館・ホテル", {"宿泊"}, 25,
     "予約・問い合わせメールへの返信と、周辺の観光・交通の案内文の作成", 10, 36.5),
    ("智頭町", "chizu", "製造業", "木材・木製品（製材）", {"木材・木製品", "製材"}, 19,
     "取引先からの寸法・在庫の問い合わせへの回答と、見積書・出荷伝票の作成", 6, 44.5),
    ("八頭町", "yazu", "医療・福祉", "特別養護老人ホーム", {"介護", "特別養護老人ホーム"}, 70,
     "ケア記録・夜勤の申し送りの要約と、家族への近況報告文の作成", 14, 37),
    # 中部地区（5）
    ("倉吉市", "kurayoshi", "医療・福祉", "病院", {"医療", "病院"}, 130,
     "紹介状への返書・診療情報提供書の下書きと、入退院の説明文書の作成", 20, 37),
    ("三朝町", "misasa", "宿泊・飲食サービス業", "温泉旅館", {"宿泊", "温泉旅館"}, 75,
     "予約・問い合わせメールへの返信の下書きと、宿泊プラン・館内案内の説明文の作成", 14, 42),
    ("湯梨浜町", "yurihama", "卸売業・小売業", "果物・農産物の直売と通信販売", {"小売", "農産物の直売"}, 21,
     "通信販売の注文・配送先の取りまとめと、季節の商品案内文の作成", 8, 41.5),
    ("琴浦町", "kotoura", "製造業", "食料品（農産物・水産物の加工）", {"食料品", "農産加工"}, 44,
     "原材料・アレルゲン表示の確認と、取引先に出す商品規格書の作成", 13, 31),
    ("北栄町", "hokuei", "運輸業・郵便業", "道路貨物運送", {"運送"}, 37,
     "配車表の下書きと、荷主への運行・到着の連絡", 10, 38),
    # 西部地区（9）
    ("米子市", "yonago", "運輸業・郵便業", "道路貨物運送", {"運送"}, 120,
     "運転日報・運行記録の集計と、荷主への配送予定・遅延の連絡", 18, 39),
    ("境港市", "sakaiminato", "製造業", "食料品（水産加工）", {"食料品", "水産加工"}, 68,
     "取引先に出す商品規格書（原材料・産地・アレルゲン）の作成と、製造・衛生管理の記録の取りまとめ", 13, 42),
    ("日吉津村", "hiezu", "卸売業・小売業", "衣料品・服飾雑貨の小売（複数店舗）", {"小売", "衣料品"}, 33,
     "商品の入荷・在庫の問い合わせへの回答と、売場・SNSの商品紹介文の作成", 11, 33),
    ("大山町", "daisen", "卸売業・小売業", "野菜の集出荷・販売", {"卸売", "野菜"}, 31,
     "取引先からの受注・出荷数量の連絡と、出荷伝票・精算書の取りまとめ", 10, 35.5),
    ("南部町", "nanbu", "医療・福祉", "介護老人保健施設", {"介護", "介護老人保健施設"}, 40,
     "介護記録の清書と、事故・ヒヤリハット報告書の下書き", 10, 41),
    ("伯耆町", "hoki", "宿泊・飲食サービス業", "ホテル・ペンション", {"宿泊"}, 29,
     "予約・団体の問い合わせへの返信と、食物アレルギー対応の確認の連絡", 10, 39.5),
    ("日南町", "nichinan", "建設業", "総合工事業", {"建設"}, 27,
     "工事日報の取りまとめと、発注者に出す工事書類の作成", 10, 33.5),
    ("日野町", "hino", "医療・福祉", "通所介護・訪問介護", {"介護", "通所介護", "訪問介護"}, 16,
     "訪問・通所の記録の清書と、ケアマネジャーへの報告文の作成", 5, 47),
    ("江府町", "kofu", "運輸業・郵便業", "道路貨物運送", {"運送"}, 23,
     "運転日報の集計と、荷主への配送予定の連絡", 9, 43),
    # 県ページ（試算を入れるかは判断が必要な点。入れるときの割り当て）
    ("鳥取県（県ページ）", "tottori", "卸売業・小売業", "食品・日用品の卸売（県内に複数の営業所）", {"卸売", "食品"}, 90,
     "得意先からの受注・在庫の問い合わせへの回答と、営業担当の商談記録の要約", 23, 26),
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def other_plans():
    """山梨県・島根県の _calc.py の PLAN を読み、(県, 市町村, 削減時間, 万円) を返す。"""
    out = []
    for pref, label in (("yamanashi", "山梨県"), ("shimane", "島根県")):
        path = os.path.join(ROOT, "data", "area", pref, "_calc.py")
        if not os.path.exists(path):
            print(f"NG {label}の _calc.py がない: {path}")
            out.append(None)
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
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（島根県の _calc.py と同じ拾い方）。"""
    hours, mans, sizes, per_file = {}, {}, {}, {}
    files = [f for f in sorted(glob.glob(os.path.join(ART, "2026-10-*-area-*.md"))) if "-area-tottori" not in f]
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
    by_pref = Counter(re.sub(r"^2026-10-\d+-area-([a-z]+).*", r"\1", k) for k in per_file)
    print(f"既存の地域ページ: {n_files}本（うち試算の節があるもの {n_sec}本。島根 {by_pref.get('shimane', 0)}本・山梨 {by_pref.get('yamanashi', 0)}本を含む）。"
          f"拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種・規模 {len(ex_s)}種")
    op = other_plans()
    ok = None not in op
    pl_h, pl_m = {}, {}
    for r in op:
        if r is None:
            continue
        label, city, h, m = r
        pl_h.setdefault(h, f"{label}{city}（_calc.py の PLAN）")
        pl_m.setdefault(m, f"{label}{city}（_calc.py の PLAN）")
    print(f"山梨県・島根県の PLAN: {len([r for r in op if r])}行（時間 {len(pl_h)}種・万円 {len(pl_m)}種）")

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
                print(f"  NG 鳥取県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 鳥取県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
                    print(f"  NG {city} の試算（{sub}）が同じ市町村の事例 {cname}（規模不明）と同じ業態")
                    ok = False
                else:
                    notes.append(f"{city}: 試算（{sub}・{size}名）と同じ業態の AI ではない事例 {cname}（規模不明）がある")
    pages = [p for p in PLAN if p[1] != "tottori"]
    slugs = {p[1] for p in pages}
    if slugs != SLUGS:
        print("NG slug が _brief.md と違う:", slugs ^ SLUGS)
        ok = False
    n_ex_size = sum(1 for p in PLAN if p[5] in ex_s)
    print(f"\n市町村ページ: {len(pages)}（＋県ページ {len(PLAN) - len(pages)}）、市町村名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}")
    print(f"時間の範囲 {min(seen_h)}〜{max(seen_h)}時間、金額の範囲 約{min(seen_m)}〜{max(seen_m)}万円、規模 {min(seen_s)}〜{max(seen_s)}名")
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは鳥取県の中だけを NG にする）")
    print(f"（参考）時間が◯.25・◯.75になるページ: {n_quarter}件")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(pages) == 19 else "NG")


if __name__ == "__main__":
    main()
