#!/usr/bin/env python3
"""東京都の試算の割り当てを計算し、重なりを確かめる（2026-11-14）。段階ごとに PLAN を足す（段階2＝23区）。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値。神奈川と同じ値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

取り決め（2026-11-11 ユーザー決定）: **他県との重なりは許容し、東京都の中だけ時間・金額・規模を重ねない**。
確かめること（NG なら最後に NG）:
  1. PLAN の中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  3. PLAN の slug が _brief.md の62区市町村にある（段階ごとに足すので、全部そろっていなくてよい）
  4. 試算の業種が wages.md の9業種にある
  5. 対象人数 ≤ 従業員数の6割、1人の月の業務量は20〜40時間
  6. 書いた記事（articles/2026-1?-??-area-tokyo-*.md）の試算の節に、PLAN の時間と金額が出てくるか（記事ができたら）
他県の記事・PLAN との重なりは参考表示だけ（NG にしない）。
使い方: python3 -B data/area/tokyo/_calc.py
"""
import glob, os, re, sys
from decimal import Decimal, ROUND_HALF_UP
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RATE = {"製造業": 3500, "卸売業・小売業": 3540, "建設業": 3520, "運輸業・郵便業": 2980, "医療・福祉": 3180,
        "宿泊・飲食サービス業": 2510, "不動産・物品賃貸業": 3790, "学術研究・専門技術サービス": 4320, "情報通信業": 4260}
SLUGS = set("""chiyoda-ku chuo-ku minato shinjuku bunkyo taito sumida koto shinagawa meguro ota-ku setagaya shibuya nakano-ku
suginami toshima-ku kita-ku arakawa itabashi nerima adachi katsushika edogawa
hachioji tachikawa musashino mitaka ome fuchu-city-tokyo akishima chofu machida koganei kodaira hino-city higashimurayama
kokubunji kunitachi fussa komae higashiyamato kiyose higashikurume musashimurayama tama inagi hamura akiruno nishitokyo
mizuho-town hinode okutama oshima hachijo hinohara toshima-village-tokyo niijima kozushima miyake-village mikurajima aogashima ogasawara""".split())
# slug: (名前, 業種, 業態, 従業員数, 対象人数, 1人の月の業務量〔時間〕, 対象業務)
PLAN = {
# 段階2: 23区
"chiyoda-ku": ('千代田区', '学術研究・専門技術サービス', '税理士・社会保険労務士の事務所', 32, 10, 28, '申告・届出の書類の下書き、顧客からの問い合わせの返信、法令改正の要点の整理'),
"chuo-ku": ('中央区', '卸売業・小売業', '食品・日用品の卸売（専門商社）', 48, 13, 30, '見積書・受発注メールの作成、FAXの注文書の転記、仕入先への問い合わせ'),
"minato": ('港区', '情報通信業', 'Web制作・システムの受託開発', 55, 15, 27, '提案書・仕様書・議事録の作成、問い合わせの一次回答'),
"shinjuku": ('新宿区', '不動産・物品賃貸業', '不動産の賃貸・管理', 28, 9, 30, '入居者からの問い合わせの返信、物件の紹介文、契約書類・報告書の下書き'),
"bunkyo": ('文京区', '製造業', '出版物の印刷・製本', 34, 8, 29, '見積書の作成、入稿データと指示書の照合、作業日報の集計'),
"taito": ('台東区', '卸売業・小売業', '雑貨・皮革製品の卸売', 26, 8, 33, '受発注の転記、商品説明文の作成、取引先への連絡'),
"sumida": ('墨田区', '製造業', '金属製品・日用品の製造（町工場）', 22, 6, 31, '見積書の作成、図面と注文書の照合、作業日報の集計'),
"koto": ('江東区', '運輸業・郵便業', '道路貨物運送・倉庫', 60, 14, 32, '配車表・運行記録の集計、荷主への連絡、請求書の作成'),
"shinagawa": ('品川区', '卸売業・小売業', '機械器具の卸売', 40, 11, 26, '見積書・仕様の比較表の作成、受発注メール、問い合わせの返信'),
"meguro": ('目黒区', '医療・福祉', '診療所（クリニック）', 18, 6, 25, '問い合わせの返信、診療記録の下書き、院内文書の作成'),
"ota-ku": ('大田区', '製造業', '金属加工・生産用機械の部品（町工場）', 30, 7, 27, '見積書の作成、図面の照合、検査成績書の作成'),
"setagaya": ('世田谷区', '医療・福祉', '介護事業所（訪問介護・居宅介護支援）', 45, 13, 28, '訪問記録・ケアプランの文案、事業所間の連絡文'),
"shibuya": ('渋谷区', '情報通信業', 'Web広告・コンテンツの制作', 24, 8, 31, '広告文・記事の下書き、制作物の確認表、顧客への報告書'),
"nakano-ku": ('中野区', '医療・福祉', '通所介護（デイサービス）', 20, 7, 23, '介護記録・連絡帳の作成、送迎表の作成'),
"suginami": ('杉並区', '宿泊・飲食サービス業', '飲食店（区内に数店舗）', 23, 7, 26, '予約・問い合わせの返信、メニュー・案内文の作成、シフトと発注の集計'),
"toshima-ku": ('豊島区', '学術研究・専門技術サービス', 'デザイン・広告制作の事務所', 15, 5, 31, '提案書・企画書の下書き、制作の進行表、議事録'),
"kita-ku": ('北区', '医療・福祉', '病院・診療所の事務', 42, 12, 21, '診療記録の下書き、問い合わせの返信、院内文書の作成'),
"arakawa": ('荒川区', '製造業', '紙製品・印刷の加工（町工場）', 19, 5, 29, '見積書の作成、受注の転記、作業指示書の作成'),
"itabashi": ('板橋区', '製造業', '精密機械・光学部品の製造', 52, 12, 24, '見積書・図面の照合、品質記録・不具合報告の作成'),
"nerima": ('練馬区', '医療・福祉', '介護老人福祉施設（特別養護老人ホーム）', 65, 16, 26, '介護記録・サービス提供記録の作成、ケア会議の議事録'),
"adachi": ('足立区', '製造業', '金属製品の加工（プレス・溶接）', 38, 9, 26, '見積書の作成、作業日報の集計、取引先への連絡'),
"katsushika": ('葛飾区', '製造業', '金属製品・プラスチック製品の製造', 27, 7, 30, '受注の転記、検査記録の作成、取引先への連絡'),
"edogawa": ('江戸川区', '卸売業・小売業', '飲食料品の小売（地域のスーパー）', 50, 13, 24, '発注・売上の集計、販促文の作成、問い合わせの返信'),
}
def man(y): return Decimal(y / 10000).quantize(Decimal("0.1"), ROUND_HALF_UP)
ng = []
rows = []
for s, (nm, ind, biz, emp, n, h, task) in PLAN.items():
    hours = n * h * 0.25
    yen = hours * RATE[ind]
    if abs(hours * 4 - round(hours * 4)) > 1e-9: ng.append(f"{nm}: 0.25刻みでない {hours}")
    if abs((yen % 1000) - 500) < 100: ng.append(f"{nm}: 金額が四捨五入の境目 {yen}")
    if ind not in RATE: ng.append(f"{nm}: 業種 {ind}")
    if n > emp * 0.6: ng.append(f"{nm}: 対象人数が多い {n}/{emp}")
    if not 20 <= h <= 40: ng.append(f"{nm}: 業務量 {h}")
    rows.append((s, nm, ind, biz, emp, n, h, hours, yen, man(yen), task))
if set(PLAN) - SLUGS: ng.append(f"slug が一覧にない: {set(PLAN) - SLUGS}")
for k, lab in ((7, "時間"), (9, "万円"), (4, "従業員数")):
    seen = {}
    for r in rows:
        if r[k] in seen: ng.append(f"{lab}が重なる: {seen[r[k]]} と {r[1]} ({r[k]})")
        seen[r[k]] = r[1]
print("| 区市町村 | 業種 | 業態 | 従業員 | 対象 | 1人の月の業務量 | 月の削減時間 | 時間単価 | 月の時間換算額 | 対象業務 |")
print("|---|---|---|---|---|---|---|---|---|---|")
for s, nm, ind, biz, emp, n, h, hours, yen, m, task in sorted(rows, key=lambda r: r[7]):
    print(f"| {nm}（{s}） | {ind} | {biz} | {emp}名 | {n}名 | {h:g}時間 | {hours:g}時間（{n}名×{h:g}時間×25%） | 約{RATE[ind]:,}円 | 約{m}万円（{yen:,.0f}円） | {task} |")
# 記事との照合
arts = {re.search(r"area-tokyo-(.+)\.md$", f).group(1): f for f in glob.glob(os.path.join(ROOT, "articles", "2026-1?-??-area-tokyo-*.md"))}
for s, nm, ind, biz, emp, n, h, hours, yen, m, task in rows:
    f = arts.get(s)
    if not f: continue
    sec = re.search(r"## 試算.*?(?=\n## )", open(f).read(), re.S)
    if not sec: continue
    t = sec.group(0)
    hs = f"{hours:g}時間"; ms = f"{m}万円"
    if hs not in t or ms not in t: ng.append(f"{nm}: 記事の試算の節に {hs} / {ms} がない")
# 他県の記事との重なり（参考）
other = []
for f in glob.glob(os.path.join(ROOT, "articles", "2026-1?-??-area-*.md")):
    if "area-tokyo" in f: continue
    sec = re.search(r"## 試算.*?(?=\n## )", open(f).read(), re.S)
    if sec: other.append(sec.group(0))
txt = "\n".join(other)
ref = [r[1] for r in rows if f"{r[7]:g}時間" in txt and f"{r[9]}万円" in txt]
print(f"\n参考（許容）: 他県の記事と時間・金額の両方が出てくる市町村 {len(ref)}: {'・'.join(ref)}")
print("\n".join(ng) if ng else "")
print("NG" if ng else "OK")
