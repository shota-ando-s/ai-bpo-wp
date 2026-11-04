#!/usr/bin/env python3
"""長崎県21市町の試算の割り当てを計算し、重なりを確かめる（2026-11-04）。

data/area/okayama/_calc.py を元に作った。県ページ（/area/nagasaki/）には試算を入れない。PLAN は21行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給）。万円は小数1桁に四捨五入して比べる。

確かめること:
  0. **九州7県の時間の割り当て**: 月の削減時間×4 を7で割った余りが 2（長崎県）
  1. 21ページの中で、月の削減時間・月の時間換算額・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、長崎県を除く。九州の他県の記事があればそれも）の「## 試算」の値と重ならない
  3. 山梨・島根・鳥取・山口・広島・岡山の _calc.py の PLAN（必須）と、九州の他県の _calc.py の PLAN（push されていれば）と重ならない。
     金額が九州の他県と重なったら、先に PLAN を push した県を優先し、あとの県が直す
  4. 時間は0.25時間刻み。金額が四捨五入の境目にならない
  5. 試算の業種・規模が cases.md の事例の会社と同じにならない
  6. slug が _brief.md の21市町と一致する
使い方: python3 data/area/nagasaki/_calc.py   （末尾に OK / NG を出す）
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
SELF = "nagasaki"

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

SLUGS = {"nagasaki-city", "sasebo", "shimabara", "isahaya", "omura", "hirado", "matsuura", "tsushima", "iki", "goto",
         "saikai", "unzen", "minamishimabara", "nagayo", "togitsu", "higashisonogi", "kawatana", "hasami", "ojika", "saza",
         "shinkamigoto"}
RESIDUE = 2  # 九州7県の割り当て（data/area/_kyushu/shared.md）

# 照合する他県の PLAN（公開前の割り当て）。5県とも必須
OTHER_PLANS = (("yamanashi", "山梨県"), ("shimane", "島根県"), ("tottori", "鳥取県"),
               ("yamaguchi", "山口県"), ("hiroshima", "広島県"), ("okayama", "岡山県"))
# 九州の他県（push されていれば読む。なくても NG にしない）
KYUSHU_PLANS = (("fukuoka", "福岡県"), ("saga", "佐賀県"), ("kumamoto", "熊本県"), ("oita", "大分県"),
                ("miyazaki", "宮崎県"), ("kagoshima", "鹿児島県"))

# cases.md の事例の会社（2026-11-03 の cases.md から）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・使用済みを含む〕)
# cases_outside.md（完成版）と cases2.md の会社は 2026-11-03 に D2 が足した
CASES = [
    ("滲透工業（県工技センターとの AI サーバー、業種未確認）", "長崎市", {"業種未確認"}, None, True),
    ("Ｎｍｅｄｉａ・協和機電工業・システック井上（作る側の助成）", "長崎市", {"情報サービス", "電気機械", "生産用機械"}, None, True),
    ("医療DX実地検証（病院名なし）", "所在未確認", {"医療", "病院"}, None, True),
    ("ホテル長崎（使用済み・高知県四万十市）", "長崎市", {"宿泊", "ホテル"}, (33, 33), True),
    ("ムラセグループ（自動車学校・ホテル・レンタカー、支援開始）", "佐世保市", {"自動車学校", "宿泊", "ホテル", "レンタカー"}, None, True),
    ("佐世保市北部商工会（AI-OCR）", "佐世保市", {"商工会"}, None, True),
    ("ジャパネットHD（大企業）", "佐世保市", {"通信販売", "小売"}, (1000, 5000), True),
    ("させぼ広域かんきつ部会（使用済み）", "佐世保市", {"農業", "果実"}, None, True),
    ("長崎県建設技術研究センター（橋梁診断の実証）", "大村市", {"建設コンサルタント", "橋梁点検"}, None, True),
    ("かとりストアー（使用済み・山形県三川町）", "大村市", {"小売", "食品スーパー"}, None, True),
    ("白洋社×クラスタス（AI セルフレジ）", "島原市", {"クリーニング"}, None, True),
    ("白洋社×クラスタス（AI セルフレジ、開発側）", "南島原市", {"クリーニング", "情報サービス"}, None, True),
    ("南島原スマート農業研究会（アスパラ）", "南島原市", {"農業", "野菜"}, (12, 12), True),
    ("西海市商工会（AI-OCR）", "西海市", {"商工会"}, None, True),
    ("西海クリエイティブカンパニー（作る側の助成）", "西海市", {"情報サービス"}, None, True),
    ("双日ツナファーム鷹島（構想、AI 未使用）", "松浦市", {"水産養殖"}, None, False),
    ("松浦地区の水産のデジタル化構想", "松浦市", {"水産", "市場"}, None, False),
    ("日本紙器（AI か不明）", "時津町", {"紙器", "パルプ・紙"}, None, False),
    ("五島市スマートアイランド実証", "五島市", {"水産"}, None, True),
    ("JA島原雲仙ブロッコリー部会（AI か不明）", "雲仙市", {"農業", "野菜"}, None, False),
    ("ことのうみ柑橘部会（使用済み）", "長与町", {"農業", "果実"}, None, True),
    ("窯業技術センター（研究段階・使用済み）", "波佐見町", {"窯業・土石", "陶磁器"}, None, True),
]

# (市町, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種・業態は stats.md の「市町ごとの主要産業の候補」の (B) 中小企業の業種から選んだ。既存の記事と7県の PLAN を避け、余りが2になる値を探して決めた（月75.75〜247.25時間。小さい規模の値は埋まっているので中規模以上）
PLAN = [
    ('長崎市', 'nagasaki-city', '卸売業・小売業', '水産物・加工食品の卸売（市内の量販店・飲食店・ホテルへの納品）', {'卸売', '飲食料品卸', '水産物卸'}, 160,
     '得意先からの受注・欠品・入荷予定の問い合わせへの回答と、商品の規格書・産地の説明資料の下書き', 26, 37.5),
    ('佐世保市', 'sasebo', '製造業', '輸送用機械（船舶の艤装品・ブロックの製作。造船所の協力会社）', {'船舶部品', '造船', '輸送用機械'}, 115,
     '元請けからの図面・工程の問い合わせへの回答と、溶接・検査の記録と作業日報の取りまとめ', 22, 33.5),
    ('島原市', 'shimabara', '製造業', '食料品（野菜の加工・冷凍野菜の製造）', {'冷凍食品', '野菜加工', '食料品'}, 78,
     '量販店・外食の取引先からの規格・産地の問い合わせへの回答と、衛生管理・ロットの記録の取りまとめ', 16, 43),
    ('諫早市', 'isahaya', '運輸業・郵便業', '道路貨物運送（工業団地の部品・食品の輸送）', {'道路貨物運送', '運送'}, 92,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計', 18, 35.5),
    ('大村市', 'omura', '製造業', '生産用機械（製造装置の部品加工・組立）', {'装置部品', '生産用機械'}, 68,
     '取引先からの仕様・納期の問い合わせへの回答と、見積書・組立手順書の下書き', 17, 31),
    ('平戸市', 'hirado', '宿泊・飲食サービス業', '旅館・ホテル（団体・修学旅行を含む）', {'宿泊', '旅館'}, 46,
     '予約サイト・メールの問い合わせへの返信の下書きと、団体の見積書、館内案内の多言語の文の作成', 17, 45),
    ('松浦市', 'matsuura', '製造業', '食料品（水産加工。アジ・サバの冷凍・フィレ加工）', {'食料品', '水産加工'}, 64,
     '取引先からの規格・産地・漁獲日の問い合わせへの回答と、衛生管理・出荷の記録の取りまとめ', 18, 28.5),
    ('対馬市', 'tsushima', '卸売業・小売業', '水産物の集荷・卸売（島外の市場・取引先への出荷）', {'卸売', '水産物卸'}, 38,
     '取引先からの入荷・規格・価格の問い合わせへの回答と、出荷の伝票・船便の手配の連絡文の作成', 15, 44),
    ('壱岐市', 'iki', '製造業', '飲料（酒類の製造と販売）', {'酒類製造', '飲料'}, 50,
     '取引先・通販の客からの在庫・商品の問い合わせへの回答と、商品説明・表示の文の作成、出荷の記録の取りまとめ', 19, 41),
    ('五島市', 'goto', '医療・福祉', '特別養護老人ホーム（短期入所を併設）', {'介護', '特別養護老人ホーム'}, 62,
     'ケア記録・ヒヤリハット報告の清書と、家族への近況の連絡文、会議録の作成', 20, 36.5),
    ('西海市', 'saikai', '製造業', '金属製品（鉄構・配管の製作。造船所・プラントの協力会社）', {'配管', '金属製品', '鉄構'}, 48,
     '元請けからの図面・数量の問い合わせへの回答と、材料の証明書・検査記録の取りまとめ', 20, 43.5),
    ('雲仙市', 'unzen', '製造業', '繊維（衣服の縫製）', {'繊維', '衣服の縫製'}, 57,
     '取引先（アパレル）からの仕様・納期の問い合わせへの回答と、縫製仕様書・検品記録の取りまとめ', 20, 29.5),
    ('南島原市', 'minamishimabara', '医療・福祉', '介護老人保健施設（通所リハビリを併設）', {'介護', '介護老人保健施設'}, 72,
     'リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成', 22, 40.5),
    ('長与町', 'nagayo', '医療・福祉', '訪問看護・居宅介護支援', {'介護', '訪問看護', '居宅介護支援'}, 24,
     '訪問の記録の清書と、主治医への報告書・ケアプランの文の下書き', 12, 25.25),
    ('時津町', 'togitsu', '製造業', 'はん用機械（ポンプ・ボイラー部品の加工・組立）', {'機械部品', 'はん用機械'}, 86,
     '取引先からの仕様・納期の問い合わせへの回答と、作業指示書・検査成績書の取りまとめ', 22, 44),
    ('東彼杵町', 'higashisonogi', '卸売業・小売業', '茶・農産加工品の卸売と通信販売', {'通信販売', '卸売', '茶'}, 40,
     '通販・取引先からの注文・在庫の問い合わせへの回答と、商品説明の文・出荷の記録の作成', 16, 37.75),
    ('川棚町', 'kawatana', '製造業', '食料品（水産練り製品の製造）', {'食料品', '水産練り製品'}, 58,
     '量販店の取引先からの規格・アレルゲンの問い合わせへの回答と、規格書の改訂、製造記録の取りまとめ', 22, 26.5),
    ('波佐見町', 'hasami', '卸売業・小売業', '陶磁器（食器）の卸売（産地の商社）', {'卸売', '食器の卸'}, 32,
     '小売店・飲食店からの在庫・納期の問い合わせへの回答と、商品カタログの文・見積書の作成', 16, 34.25),
    ('小値賀町', 'ojika', '卸売業・小売業', '食品・日用品の小売と島内の配送（島の商店）', {'食品', '小売', '日用品'}, 22,
     '船便の入荷予定と欠品の連絡、島内の注文・配送の受付と伝票・在庫の記録の取りまとめ', 11, 46),
    ('佐々町', 'saza', '医療・福祉', '認可保育所（一時預かりを含む）', {'児童福祉', '保育所'}, 42,
     '保育の記録・連絡帳の清書と、保護者へのお知らせ、行事の計画書の作成', 23, 43),
    ('新上五島町', 'shinkamigoto', '建設業', '総合工事業（土木・港湾の工事）', {'建設', '土木', '港湾'}, 34,
     '公共工事の施工計画書・提出書類の作成と、工事写真・出来形の記録の整理', 20, 34.75),
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
                print(f"  NG 長崎県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 長崎県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
            ok = False
        seen_s[size] = city
        if (h * 4) % 1 != 0 or int(h * 4) % 7 != RESIDUE:
            print(f"  NG {city} の時間×4 を7で割った余りが {RESIDUE} でない ({h})")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは岡山県の中だけを NG にする）")
    print(f"（参考）時間が◯.25・◯.75になるページ: {n_quarter}件")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 21 else "NG")


if __name__ == "__main__":
    main()
