#!/usr/bin/env python3
"""神奈川県33市町村の試算の割り当てを計算し、重なりを確かめる（2026-11-12）。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

取り決め（2026-11-11 ユーザー決定）: **他県との重なりは許容し、神奈川県の中だけ時間・金額・規模を重ねない**。
確かめること（NG なら最後に NG）:
  1. 33ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  3. slug が _brief.md の33市町村と一致する（大和市 yamato-city）
  4. 試算の業種が wages.md の9業種にある
  5. 対象人数 ≤ 従業員数の6割、1人の月の業務量は20〜40時間
  6. 書いた記事（articles/2026-1?-??-area-kanagawa-*.md と 2026-10-17-area-yokohama.md）の試算の節に、PLAN の時間と金額が出てくるか（記事ができたら）
他県の記事・PLAN との重なりは参考表示だけ（NG にしない）。
使い方: python3 -B data/area/kanagawa/_calc.py
"""
import glob, os, re, sys
from decimal import Decimal, ROUND_HALF_UP
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RATE = {"製造業": 3500, "卸売業・小売業": 3540, "建設業": 3520, "運輸業・郵便業": 2980, "医療・福祉": 3180,
        "宿泊・飲食サービス業": 2510, "不動産・物品賃貸業": 3790, "学術研究・専門技術サービス": 4320, "情報通信業": 4260}
SLUGS = set("""yokohama kawasaki sagamihara yokosuka hiratsuka kamakura fujisawa odawara chigasaki zushi miura hadano atsugi
yamato-city isehara ebina zama minamiashigara ayase hayama samukawa oiso ninomiya nakai oi matsuda yamakita kaisei hakone
manazuru yugawara aikawa kiyokawa""".split())
# slug: (名前, 業種, 業態, 従業員数, 対象人数, 1人の月の業務量〔時間〕, 対象業務)
PLAN = {
"yokohama": ('横浜市', '卸売業・小売業', '機械器具の卸売（法人向けの専門商社）', 45, 12, 30, '見積書・受発注メールの作成、FAXの注文書の転記、仕入先への問い合わせ'),
"kawasaki": ('川崎市', '情報通信業', '業務システムの受託開発', 60, 15, 28, '仕様書・テスト仕様書・議事録の作成、問い合わせの一次回答'),
"sagamihara": ('相模原市', '製造業', '生産用機械の部品加工', 70, 15, 26, '見積書・図面の照合、作業日報の集計、品質記録の作成'),
"yokosuka": ('横須賀市', '医療・福祉', '介護老人福祉施設（特別養護老人ホーム）', 55, 16, 24, '介護記録・サービス提供記録の作成、ケア会議の議事録'),
"hiratsuka": ('平塚市', '製造業', '金属製品の加工', 48, 11, 27, '見積書の作成、受注の転記、検査成績書の作成'),
"kamakura": ('鎌倉市', '宿泊・飲食サービス業', '飲食店（複数店舗）', 30, 9, 22, '予約・問い合わせの返信、多言語のメニュー・案内文、シフトと発注の集計'),
"fujisawa": ('藤沢市', '卸売業・小売業', '食品スーパー（複数店舗）', 52, 13, 25, '発注・売上の集計、販促文の作成、問い合わせの返信'),
"odawara": ('小田原市', '製造業', '水産加工品・食料品の製造', 40, 9, 29, '受注の転記、原料・製造記録の作成、商品説明文の作成'),
"chigasaki": ('茅ヶ崎市', '医療・福祉', '介護事業所（訪問介護・居宅介護支援）', 38, 11, 31, '訪問記録・ケアプランの文案、事業所間の連絡文'),
"zushi": ('逗子市', '医療・福祉', '訪問看護ステーション', 18, 6, 23, '訪問看護記録・報告書の作成'),
"miura": ('三浦市', '卸売業・小売業', '青果の集出荷・卸売', 22, 7, 34, '出荷伝票の転記、取引先への連絡、相場表の整理'),
"hadano": ('秦野市', '製造業', '電気機械の部品製造', 56, 12, 28, '見積書・図面の照合、品質記録・不具合報告の作成'),
"atsugi": ('厚木市', '運輸業・郵便業', '道路貨物運送', 64, 13, 33, '配車表・運行記録の集計、荷主への連絡、請求書の作成'),
"yamato-city": ('大和市', '卸売業・小売業', '衣料品・日用品の小売店（市内に数店舗）', 34, 9, 26, '発注の集計、商品説明文・販促文の作成、問い合わせの返信'),
"isehara": ('伊勢原市', '医療・福祉', '診療所・病院の事務', 44, 12, 21, '診療記録の下書き、問い合わせの返信、院内文書の作成'),
"ebina": ('海老名市', '運輸業・郵便業', '倉庫・物流センター', 50, 11, 30, '入出庫の記録・在庫表の集計、荷主への報告書'),
"zama": ('座間市', '製造業', '生産用機械の製造', 36, 8, 34, '見積書・仕様書の作成、作業手順書の作成'),
"minamiashigara": ('南足柄市', '製造業', 'プラスチック製品の製造', 32, 7, 31, '受注の転記、検査記録の作成、取引先への連絡'),
"ayase": ('綾瀬市', '製造業', '金属製品の加工（プレス・溶接）', 26, 7, 25, '見積書の作成、作業日報の集計'),
"hayama": ('葉山町', '医療・福祉', '通所介護事業所', 15, 5, 26, '介護記録・連絡帳の作成'),
"samukawa": ('寒川町', '製造業', '輸送用機械の部品製造', 42, 10, 24, '品質記録・不具合報告の作成、受注の転記'),
"oiso": ('大磯町', '卸売業・小売業', '小売店', 16, 5, 29, '商品説明文・販促文の作成、問い合わせの返信'),
"ninomiya": ('二宮町', '医療・福祉', '介護事業所', 20, 6, 27, '介護記録・サービス提供記録の作成'),
"nakai": ('中井町', '製造業', '食料品の製造', 28, 7, 30, '受注の転記、製造記録の作成'),
"oi": ('大井町', '運輸業・郵便業', '道路貨物運送', 24, 6, 32, '配車表・運行記録の集計、請求書の作成'),
"matsuda": ('松田町', '医療・福祉', '診療所', 25, 8, 22, '問い合わせの返信、院内文書・記録の下書き'),
"yamakita": ('山北町', '製造業', '飲料・食料品の製造', 31, 8, 28, '受注の転記、製造記録・商品説明文の作成'),
"kaisei": ('開成町', '学術研究・専門技術サービス', '設計・技術サービス', 14, 5, 24, '報告書・提案書の下書き、議事録'),
"hakone": ('箱根町', '宿泊・飲食サービス業', '旅館・ホテル', 46, 10, 26, '予約・問い合わせの返信（多言語）、館内案内文、口コミの返信'),
"manazuru": ('真鶴町', '宿泊・飲食サービス業', '飲食店・宿', 12, 5, 30, '予約・問い合わせの返信、案内文の作成'),
"yugawara": ('湯河原町', '宿泊・飲食サービス業', '旅館', 37, 8, 33, '予約・問い合わせの返信、館内案内文、口コミの返信'),
"aikawa": ('愛川町', '運輸業・郵便業', '道路貨物運送', 41, 10, 29, '配車表・運行記録の集計、荷主への連絡'),
"kiyokawa": ('清川村', '製造業', '食料品の製造', 13, 5, 27, '受注の転記、商品説明文の作成'),
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
if set(PLAN) != SLUGS: ng.append(f"slug の差: {set(PLAN) ^ SLUGS}")
for k, lab in ((7, "時間"), (9, "万円"), (4, "従業員数")):
    seen = {}
    for r in rows:
        if r[k] in seen: ng.append(f"{lab}が重なる: {seen[r[k]]} と {r[1]} ({r[k]})")
        seen[r[k]] = r[1]
print("| 市町村 | 業種 | 業態 | 従業員 | 対象 | 1人の月の業務量 | 月の削減時間 | 時間単価 | 月の時間換算額 | 対象業務 |")
print("|---|---|---|---|---|---|---|---|---|---|")
for s, nm, ind, biz, emp, n, h, hours, yen, m, task in sorted(rows, key=lambda r: r[7]):
    print(f"| {nm}（{s}） | {ind} | {biz} | {emp}名 | {n}名 | {h:g}時間 | {hours:g}時間（{n}名×{h:g}時間×25%） | 約{RATE[ind]:,}円 | 約{m}万円（{yen:,.0f}円） | {task} |")
# 記事との照合
arts = {re.search(r"area-kanagawa-(.+)\.md$", f).group(1): f for f in glob.glob(os.path.join(ROOT, "articles", "2026-1?-??-area-kanagawa-*.md"))}
y = os.path.join(ROOT, "articles", "2026-10-17-area-yokohama.md")
arts["yokohama"] = y
for s, nm, ind, biz, emp, n, h, hours, yen, m, task in rows:
    f = arts.get(s)
    if not f or not os.path.exists(f): continue
    body = open(f).read()
    sec = re.search(r"## 試算.*?(?=\n## )", body, re.S)
    if not sec: continue
    t = sec.group(0)
    hs = f"{hours:g}時間"; ms = f"{m}万円"
    if hs not in t or ms not in t:
        if s == "yokohama" and "2026-11" not in body: continue  # 書き直す前のパイロット
        ng.append(f"{nm}: 記事の試算の節に {hs} / {ms} がない")
# 他県の記事との重なり（参考）
other = []
for f in glob.glob(os.path.join(ROOT, "articles", "2026-1?-??-area-*.md")):
    if "area-kanagawa" in f or f.endswith("area-yokohama.md"): continue
    sec = re.search(r"## 試算.*?(?=\n## )", open(f).read(), re.S)
    if sec: other.append(sec.group(0))
txt = "\n".join(other)
ref = [r[1] for r in rows if f"{r[7]:g}時間" in txt and f"{r[9]}万円" in txt]
print(f"\n参考（許容）: 他県の記事と時間・金額の両方が出てくる市町村 {len(ref)}: {'・'.join(ref)}")
print("\n".join(ng) if ng else "")
print("NG" if ng else "OK")
