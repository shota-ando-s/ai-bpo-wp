#!/usr/bin/env python3
"""山梨県27市町村の試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-10-31）。

data/area/nagano/_calc.py をコピーして、PLAN・CASES・照合の対象を山梨県に直した。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  1. 27ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の市町村ページ（articles/2026-10-*-area-*.md、山梨県を除く。長野県を含む）の「## 試算」の節に出てくる
     「◯時間」「◯万円」の値と重ならない。既存の記事は県ごとに表の形が違うので、節の中の数値を
     広めに拾う（1人の業務量・年間の額・差し引き後の額なども拾う。拾いすぎは「重ならない」側に働く）
  3. 時間は0.25時間刻み（既存の記事で10〜35時間の0.5刻みの値がほぼ埋まっているため、◯.25・◯.75も使う）。
     金額が四捨五入の境目（◯.◯5万円ちょうど）にならない
  4. 試算の業種・規模が cases.md の事例の会社と同じにならない（CASES の表と照合）。
     業種が分からない会社は、同じ市町村で規模が±15%に入るものを NG にする
使い方: python3 data/area/yamanashi/_calc.py   （末尾に OK / NG を出す）
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

# cases.md の事例の会社（業種の目安, 従業員数〔分からなければ None〕, 市町村）
# 試算の「業種（業態）＋規模」がこれと同じ・近い（±15%）にならないことを確かめる。
# 業種が「不明」の会社は、同じ市町村の試算の規模が±15%に入らないことを確かめる
CASES = [
    ("欣寿会（法人、富士吉田市）", "介護", 150, "富士吉田市"),
    ("おりひめ（欣寿会の特養、富士吉田市）", "介護（特別養護老人ホーム）", 35, "富士吉田市"),
    ("JAフルーツ山梨（山梨市）", "果物の集出荷（農協）", None, "山梨市"),
    ("甲府通運（中央市）", "道路貨物運送", 109, "中央市"),
    ("勝沼醸造（甲州市）", "飲料（ワイナリー）", None, "甲州市"),
    ("かがみもち（甲州市）", "娯楽（太神楽）", None, "甲州市"),
    ("株式会社アルプス（昭和町）", "不明", None, "昭和町"),
    ("豊前医化（中央市）", "不明", None, "中央市"),
    ("山梨県立中央病院（甲府市）", "病院", None, "甲府市"),
    ("国際建設（甲府市、AIではない）", "総合工事業", 51, "甲府市"),
    ("オズ プリンティング（甲府市、AIではない）", "印刷", 20, "甲府市"),
    ("太陽社（昭和町、AIではない）", "建設（塗装工事）", 17, "昭和町"),
    ("新和運輸（南アルプス市、AIではない）", "道路貨物運送", 37, "南アルプス市"),
    ("山十産業（南アルプス市、AIではない）", "不明", 21, "南アルプス市"),
    ("エフエーエム（富士河口湖町、AIではない）", "不明", 18, "富士河口湖町"),
    ("韮崎電子（韮崎市、AIではない）", "不明", 95, "韮崎市"),
    ("ササキ（韮崎市、AIではない）", "不明", 380, "韮崎市"),
    ("あさひホーム（韮崎市、AIではない）", "介護（介護老人保健施設）", None, "韮崎市"),
    ("カインドネスケア（山梨市、AIではない）", "介護", None, "山梨市"),
    ("田富荘（中央市、AIではない）", "介護（特別養護老人ホーム）", None, "中央市"),
    ("クピド・ファーム（韮崎市、既出）", "農業（ぶどう）", None, "韮崎市"),
    ("ホテル湖龍（河口湖畔、既出）", "ホテル", None, "富士河口湖町"),
    ("アルソア慧央グループ（北杜市、既出）", "化学（化粧品）", None, "北杜市"),
]

# (市町村, slug, 業種, 業態〔中分類など〕, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
PLAN = [
    # 中北（7）
    ("甲府市", "kofu", "卸売業・小売業", "食品・日用品の卸売", 160, "得意先からの受注・在庫の問い合わせへの回答と、営業担当の商談記録の要約", 14, 25.5),
    ("韮崎市", "nirasaki", "製造業", "生産用機械", 260, "装置の仕様書・過去の設計資料の検索と、顧客からの技術的な問い合わせへの回答の下書き", 16, 31),
    ("南アルプス市", "minami-alps", "製造業", "輸送用機械・自動車部品", 180, "顧客からの品質の問い合わせへの回答と、不具合の報告書の下書き", 14, 30.5),
    ("北杜市", "hokuto", "製造業", "飲料", 85, "取引先に出す商品規格書の作成・成分の問い合わせへの回答と、出荷検査の記録の取りまとめ", 10, 29.5),
    ("甲斐市", "kai", "卸売業・小売業", "食品スーパー", 70, "店舗ごとの発注量の見積と、売場のPOP・チラシの文の作成", 11, 31),
    ("中央市", "chuo", "製造業", "食料品", 140, "製造記録・衛生管理の記録の点検と、取引先からの品質の問い合わせへの回答", 14, 28.5),
    ("昭和町", "showa", "製造業", "業務用機械", 200, "顧客ごとの仕様書・検査基準の検索と、出荷検査の成績書の作成", 15, 29),
    # 峡東（3）
    ("山梨市", "yamanashi-city", "医療・福祉", "病院", 115, "紹介状への返書・診療情報提供書の下書きと、入退院の説明文書の作成", 13, 27),
    ("笛吹市", "fuefuki", "卸売業・小売業", "果物の集出荷・販売", 30, "出荷先ごとの数量・等級の連絡と、出荷伝票・精算書の取りまとめ", 9, 25),
    ("甲州市", "koshu", "卸売業・小売業", "果物の直売と贈答品の通信販売", 12, "贈答品の注文・配送先の取りまとめと、収穫・発送の案内文の作成", 2, 7.5),
    # 峡南（5）
    ("市川三郷町", "ichikawamisato", "製造業", "紙加工品", 28, "取引先からの仕様・在庫の問い合わせへの回答と、見積書の作成", 2, 26.5),
    ("早川町", "hayakawa", "建設業", "総合工事業", 13, "公共工事の提出書類と、工事日報の取りまとめ", 2, 8.5),
    ("身延町", "minobu", "医療・福祉", "特別養護老人ホーム", 48, "ケア記録と夜勤の申し送りの要約と、家族への近況報告文の作成", 9, 37),
    ("南部町", "nanbu", "製造業", "プラスチック製品", 50, "成形条件・検査記録の取りまとめと、顧客に出す品質報告の作成", 9, 35),
    ("富士川町", "fujikawa", "製造業", "業務用機械の部品加工", 34, "加工図面の読み取りと、見積書の作成", 7, 37),
    # 富士・東部（12）
    ("富士吉田市", "fujiyoshida", "製造業", "繊維・織物", 22, "取引先からの柄・仕様の問い合わせへの回答と、自社商品の通信販売の商品説明文の作成", 6, 34.5),
    ("都留市", "tsuru", "製造業", "非鉄金属", 72, "材料の成分・検査データの照合と、顧客に出す試験成績書の作成", 10, 30.5),
    ("大月市", "otsuki", "医療・福祉", "通所・訪問の介護事業所", 58, "訪問・通所の記録の清書と、ケアマネジャーへの報告文の作成", 10, 34.5),
    ("上野原市", "uenohara", "製造業", "化学", 45, "安全データシート（SDS）・製品規格書の改訂と、取引先からの含有物質の問い合わせへの回答", 9, 33),
    ("道志村", "doshi", "建設業", "総合工事業", 10, "施工計画書と、出来形・品質管理の書類の作成", 1, 11),
    ("西桂町", "nishikatsura", "製造業", "電子部品", 26, "検査記録の取りまとめと、顧客からの納期・品質の問い合わせへの回答", 7, 31),
    ("忍野村", "oshino", "製造業", "生産用機械", 110, "保守部品・修理の問い合わせへの一次回答と、過去の対応記録の検索", 13, 29),
    ("山中湖村", "yamanakako", "宿泊・飲食サービス業", "ホテル・保養施設", 40, "団体・合宿の予約の連絡と、献立・食物アレルギー対応の確認", 10, 32.5),
    ("鳴沢村", "narusawa", "製造業", "生産用機械の部品加工", 38, "加工手順書の改訂と、新人向けの作業指示書の作成", 9, 31),
    ("富士河口湖町", "fujikawaguchiko", "宿泊・飲食サービス業", "ホテル", 95, "外国語を含む予約・問い合わせメールへの返信の下書きと、館内案内の多言語化", 12, 31),
    ("小菅村", "kosuge", "宿泊・飲食サービス業", "観光施設の飲食・売店", 9, "飲食・売店の仕入れ量の見積と、季節のお知らせ文の作成", 1, 13),
    ("丹波山村", "tabayama", "宿泊・飲食サービス業", "民宿・宿泊施設", 5, "予約メールへの返信と、周辺の案内文の作成", 2, 9.5),
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def existing():
    """既存の市町村ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う。

    県ごとに表の形が違うので、次のように拾う（拾いすぎは「重ならない」側に働くので、迷うものは拾う）:
      - 表の行: 1列目が前提（人数・業務量・時給・月額・差し引き・回収など）の行は拾わない。それ以外の行の値の列から拾う
      - 本文の行: 時給の説明（毎月勤労統計・総実労働時間）・月額・差し引き・残り・初期費用・回収の語より後ろは拾わない
      - 括弧の中（計算式「12名 × 21時間 × 25%」や年間の額）は除いてから拾う
    """
    hours, mans, sizes, per_file = {}, {}, {}, {}
    files = [f for f in sorted(glob.glob(os.path.join(ART, "2026-10-*-area-*.md"))) if "-area-yamanashi" not in f]
    n_sec = 0
    skip_h_label = re.compile(r"人数|業務量|使う人|人と時間|時間（仮定）|1人|時給|時間単価|1時間あたり")
    skip_m_label = re.compile(r"時給|時間単価|1時間あたり|月額|引|回収|費用|利用料|料金")
    cut_line = re.compile(r"毎月勤労統計|総実労働|ヒキツギAI|月額|差し引|引いた|引いても|払っても|払った|残り|残ります|初期費用|回収|戻る|取り戻せる")
    for f in files:
        t = open(f, encoding="utf-8").read()
        m = re.search(r"^## 試算.*?(?=^## )", t, re.M | re.S)
        if not m:
            continue  # 県ページなど
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
                    take_h = take_m = True  # 結果の行・横長の結果表の見出し行
                if re.match(r"[*約月]*\d", label):
                    val = " ".join(cells)  # 横長の結果表の値の行（1列目から値）
                    take_h = take_m = True
                if take_h and re.search(r"人数|業務量|使う人|時給", label) and "削減" not in label:
                    take_h = False
            else:
                val = cut_line.split(line)[0]  # 時給の説明・月額・差し引き・回収の語より前だけ
                take_h = take_m = True
            v = re.sub(r"（[^）]*）|\([^)]*\)", "", val)
            if take_h:
                for x in re.findall(r"([\d,]+(?:\.\d+)?)\s*時間", v):
                    fh.add(Decimal(x.replace(",", "")))
            if take_m:
                for a, b in re.findall(r"(\d+)万([\d,]+)円", v):  # 「約17万5,000円」の形
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
    no_h = [k for k, v in per_file.items() if v[0] == 0]
    if no_h:
        print("（参考）試算の時間を拾えなかった既存の記事（結果表に時間の行がない形）:", no_h)
    print(f"既存の地域ページ: {n_files}本（うち試算の節があるもの {n_sec}本）。拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種・規模 {len(ex_s)}種")

    ok = True
    seen_h, seen_m, seen_s = {}, {}, {}
    n_quarter = 0
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | 年間 |")
    for (city, slug, ind, sub, size, task, n, hrs) in PLAN:
        h = Decimal(str(n)) * Decimal(str(hrs)) * Decimal("0.25")
        yen = h * RATE[ind]
        m = man(yen)
        y = man(yen * 12)
        print(f"| {city} | {ind}（{sub}） | {size}名 | {n}名×{hrs}h×25% | {h.normalize():f}h | {RATE[ind]:,}円 | 約{m}万円 | 約{y}万円 |")
        for label, key, seen, exd in (("時間", h, seen_h, ex_h), ("金額", m, seen_m, ex_m)):
            if key in seen:
                print(f"  NG 山梨県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 山梨県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
        for (cname, cind, csize, ccity) in CASES:
            if csize is None or abs(size - csize) > csize * 0.15:
                continue
            same_ind = cind.split("（")[0] in sub or sub.split("（")[0] in cind or (
                ind == "医療・福祉" and "介護" in cind and "介護" in sub)
            if same_ind or (cind == "不明" and ccity == city):
                print(f"  NG {city} の試算（{sub}・{size}名）が事例 {cname}（{cind}・{csize}名）に近い")
                ok = False
    n_ex_size = sum(1 for p in PLAN if p[4] in ex_s)
    print(f"\n27ページ: {len(PLAN)}、slug の重なり: {len(PLAN) - len({p[1] for p in PLAN})}、市町村名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}")
    print(f"時間の範囲 {min(seen_h)}〜{max(seen_h)}h、金額の範囲 {min(seen_m)}〜{max(seen_m)}万円、規模 {min(seen_s)}〜{max(seen_s)}名")
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは山梨県の中だけを NG にする）")
    print(f"（参考）時間が◯.25・◯.75になるページ: {n_quarter}件（既存の記事で0.5刻みの値がほぼ使われているため）")
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 27 else "NG")


if __name__ == "__main__":
    main()
