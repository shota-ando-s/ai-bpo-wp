#!/usr/bin/env python3
"""福岡県60市町村の試算の割り当てを計算し、重なりを確かめる（D1 統計の下書き用、2026-11-04）。

data/area/okayama/_calc.py を元に作った（他県の PLAN の読み方は data/area/saga/_calc.py の形）。
県ページ（/area/fukuoka/）には試算を入れないので、PLAN は60行（福岡市・北九州市は1行ずつ。区のページはない）。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **九州7県の取り決め**: 月の削減時間（0.25時間刻み）×4 を7で割った余りが 0（福岡県）の時間だけを使う
     （＝1.75時間の倍数。1.75, 3.5, 5.25, 7, … data/area/_kyushu/shared.md）
  1. 60ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、福岡県を除く）の「## 試算」の節に出てくる
     「◯時間」「◯万円」の値と重ならない。拾い方は岡山県の _calc.py と同じ
  3. 全県の data/area/*/_calc.py の PLAN（福岡県を除く。glob で全部読む）の月の削減時間・月の時間換算額と重ならない。
     REQUIRED の県はファイルがなければ NG。九州の他県（熊本・鹿児島など）は push されていれば glob で読む。
     PLAN の形が違って読めない県はエラーにせず、読めた分だけ照合し、読めなかった県を表示して NG にする
     （READERS に県ごとの読み方を足せば読める）。**金額が九州の他県と重なったら、福岡側が直す**（先に push した県が優先）
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases2.md（・あれば cases_outside.md）の事例の会社と同じにならない（CASES と照合）
     - AI の事例で、業態のキーが重なり、従業員数が事例の範囲（下限×0.85〜上限×1.15）に入る → NG
     - AI の事例で、業態のキーが重なり、同じ市町村で、事例の従業員数が分からない → NG（その会社の値と読まれるため）
     - 業種が確かめられていない事例（キー「業種未確認」）と同じ市町村 → 参考として表示（NG にしない）
     - AI ではない事例と業態・規模が近い → 参考として表示
  6. slug が _brief.md の60市町村と一致する（福岡市は fukuoka-city、川崎町は kawasaki-town）
  7. 試算の業種が wages.md にある（農業・漁業・林業は試算の業種にしない）
使い方: python3 -B data/area/fukuoka/_calc.py   （末尾に OK / NG を出す。-B で __pycache__ を作らない）
"""
import ast
import glob
import os
import re
import sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

sys.dont_write_bytecode = True

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ART = os.path.join(ROOT, "articles")
HERE = os.path.dirname(os.path.abspath(__file__))
SELF = "fukuoka"
KYUSHU_MOD = 0  # 九州7県の割り当て（月の削減時間×4 を7で割った余り）。福岡県は 0
KYUSHU = ("saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima")

# wages.md の人件費時給（時給①×1.2 を十円単位に丸めた値。記事でも「約◯円」と書く値）。9業種とも wages.md にある
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
    # 市（29）
    "kitakyushu", "fukuoka-city", "omuta", "kurume", "nogata", "iizuka", "tagawa", "yanagawa", "yame", "chikugo",
    "okawa", "yukuhashi", "buzen", "nakama", "ogori", "chikushino", "kasuga", "onojo", "munakata", "dazaifu",
    "koga", "fukutsu", "ukiha", "miyawaka", "kama", "asakura", "miyama", "itoshima", "nakagawa",
    # 町（29）
    "umi", "sasaguri", "shime", "sue", "shingu", "hisayama", "kasuya", "ashiya", "mizumaki", "okagaki", "onga",
    "kotake", "kurate", "keisen", "chikuzen", "tachiarai", "oki", "hirokawa", "kawara", "soeda", "itoda",
    "kawasaki-town", "oto", "fukuchi", "kanda", "miyako", "yoshitomi", "koge", "chikujo",
    # 村（2）
    "toho", "aka",
}

# 照合が必須の県（2026-11-04 に main にある _calc.py）。ファイルがなければ NG
REQUIRED = ("gifu", "hiroshima", "miyazaki", "nagano", "nagasaki", "oita", "okayama", "saga", "shimane", "tottori",
            "yamaguchi", "yamanashi")


def read_plan_standard(src):
    """岡山県の形の PLAN（行頭の `PLAN = [` から行頭の `]` まで。各行の [0]=市町村, [2]=業種, [-2]=対象人数, [-1]=1人の月の業務量）。
    docstring の中の「PLAN = [」を拾わないよう、行頭の代入だけを探す（佐賀県の _calc.py は docstring に同じ文字列がある）"""
    m = re.search(r"^PLAN = \[", src, re.M)
    if not m:
        raise ValueError("行頭の PLAN = [ がない")
    j = src.index("\n]\n", m.start())
    rows = ast.literal_eval(src[m.start() + 7:j + 2])
    return [(r[0], r[2], r[-2], r[-1]) for r in rows]


# 県ごとの PLAN の読み方。2026-11-04 の12県はすべて岡山県と同じ形（read_plan_standard）で読めた。
# 形の違う県が入ったら、ここに "県": 関数 を足す（関数は src を受け取り (市町村, 業種, 対象人数, 1人の業務量) のリストを返す）
READERS = {}

# cases.md・cases2.md の事例の会社（2026-11-04）。cases_outside.md は 2026-11-04 の時点でまだない（あれば注意を出す）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・計画・使用済み・自社製品を含む〕)
CASES = [
    # 北九州市（cases.md）
    ("九州鉄道機器製造（AIビジョンのバリ取りロボット、相談事例）", "北九州市", {"金属製品", "鉄道部品", "鉄鋼"}, None, True),
    ("山本工作所（音紋解析の故障予知、計画）", "北九州市", {"金属製品", "ドラム缶", "集塵機"}, None, True),
    ("リョーワ（AI外観検査の開発・販売、提供側）", "北九州市", {"情報サービス", "油圧装置", "設備保全"}, None, True),
    ("ハピクロ（保育園のAIカメラ、自社製品）", "北九州市", {"保育", "保育所"}, (19, 19), True),
    ("ミシマ・オーエー・システム（SCADA、計画）", "北九州市", {"情報サービス", "ソフトウェア", "制御システム"}, None, True),
    ("熱産ヒート（熱処理の遠隔監視、今後AI）", "北九州市", {"金属製品", "熱処理"}, None, True),
    ("ゼムケンサービス（AI＋ARのツール、開発中）", "北九州市", {"業種未確認"}, None, True),
    ("デンソー九州（大企業、外観検査AI）", "北九州市", {"輸送用機械", "自動車部品", "熱交換器"}, (1000, 99999), True),
    ("プーラビダ（訪問看護、使用済み・宮城県山元町）", "北九州市", {"訪問看護", "介護", "医療"}, None, True),
    ("海峡都市関門DMO（使用済み・青森県三沢市など）", "北九州市", {"観光", "宿泊"}, None, True),
    ("北九州生成AI研究会・VIVINKO（研究会）", "北九州市", {"業種未確認"}, None, True),
    # 北九州市（cases2.md）
    ("シャボン玉石けん（AIの生産計画、DX大賞）", "北九州市", {"化学", "石けん", "日用品の製造"}, None, True),
    ("不動産中央情報センター（AI/ICT、DX大賞）", "北九州市", {"不動産"}, None, True),
    ("アイム製作所（日報のAI解析）", "北九州市", {"業種未確認"}, None, True),
    ("CHK GROUP（HAGUKUMI 採択）", "北九州市", {"業種未確認"}, None, True),
    ("ワイルド化成（HAGUKUMI 採択、AIエージェントの実証）", "北九州市", {"化学", "プラスチック製品"}, None, True),
    ("戸畑ターレット工作所（HAGUKUMI 採択、約180人）", "北九州市", {"機械部品", "金属製品", "はん用機械"}, (180, 180), True),
    # 北九州市（AI ではない・AI の記述なし）
    ("西原商事HD（AIではない）", "北九州市", {"廃棄物処理"}, None, False),
    ("松本工業（AIではない）", "北九州市", {"輸送用機械", "自動車部品"}, None, False),
    ("グランド印刷（AIではない）", "北九州市", {"印刷"}, None, False),
    ("EVモーターズ・ジャパン（AIではない）", "北九州市", {"輸送用機械", "電気自動車"}, (102, 102), False),
    ("クラウン製パン（AIではない）", "北九州市", {"食料品", "パン"}, (400, 400), False),
    ("ケントク（AIではない）", "北九州市", {"建設"}, (9, 9), False),
    ("白海（AIではない、浚渫）", "北九州市", {"建設", "浚渫", "港湾工事"}, None, False),
    ("池間組（AIではない、港湾工事）", "北九州市", {"建設", "港湾工事"}, None, False),
    ("白石書店（AIではない）", "北九州市", {"書店", "小売"}, None, False),
    ("製鉄記念八幡病院（AIではない）", "北九州市", {"医療", "病院"}, None, False),
    ("大英産業（AIではない）", "北九州市", {"不動産", "住宅"}, None, False),
    ("小倉運送（AIではない、デジタコ）", "北九州市", {"運送", "道路貨物運送"}, None, False),
    # 福岡市
    ("ペンシル（生成AIのテスト導入、約140人）", "福岡市", {"Web制作", "Webコンサルティング", "広告", "情報サービス"}, (140, 140), True),
    ("糸島みるくぷらんと本社（AIの生産計画の実証）", "福岡市", {"食料品", "乳製品"}, None, True),
    ("Regnio（AIの開発、提供側）", "福岡市", {"情報サービス"}, None, True),
    ("福岡銀行（大企業、見込み）", "福岡市", {"金融"}, (1000, 99999), True),
    ("九州日立システムズ（大企業、研修ベンダーの発表）", "福岡市", {"情報サービス"}, (577, 577), True),
    ("九州大学病院・九州がんセンター（大病院）", "福岡市", {"医療", "病院"}, None, True),
    ("山口油屋福太郎（使用済み・横浜市・高松市）", "福岡市", {"食料品", "明太子", "菓子"}, None, True),
    ("ヤマエ久野（使用済み・盛岡市、中小企業の基準を超える）", "福岡市", {"卸売", "飲食料品卸"}, None, True),
    ("グッデイ（使用済み・青森県三戸町、1,500名）", "福岡市", {"小売", "ホームセンター"}, (1500, 1500), True),
    ("福岡市の公共工事の写真管理のAI実証（市の事業、使用済み）", "福岡市", {"行政"}, None, True),
    ("如水法律事務所（広島の予備）", "福岡市", {"法律事務所", "士業"}, None, True),
    ("アイメトリカ（呼吸音のAI解析の実証採択、AIを作る側）", "福岡市", {"情報サービス", "介護"}, None, True),
    ("シティアスコム（自社LLM、顧客事例なし）", "福岡市", {"情報サービス"}, (534, 534), True),
    ("福岡運輸（AIではない、受領書の電子化）", "福岡市", {"運送", "道路貨物運送", "低温物流"}, None, False),
    # 大川市・糸島市・須恵町・直方市・八女市・篠栗町・久山町・粕屋町
    ("大川家具ドットコム（生成AIの家具相談、数値なし）", "大川市", {"家具", "家具の通販", "小売"}, None, True),
    ("糸島みるくぷらんと糸島工場（AIの生産計画の実証）", "糸島市", {"食料品", "乳製品"}, None, True),
    ("リキマン（同定できず、verified: false）", "須恵町", {"業種未確認"}, None, True),
    ("フォーバンド（使用済み・広島県府中市、精密部品加工、18名）", "直方市", {"金属製品", "機械部品", "精密部品加工"}, (18, 18), True),
    ("Cotona（使用済み・岡山県倉敷市、学校販売店向け AI OCR）", "八女市", {"学生服", "受注事務", "OCR", "情報サービス"}, None, True),
    ("やまやコミュニケーションズ（使用済み・愛媛県松前町、明太子）", "篠栗町", {"食料品", "明太子", "水産加工"}, None, True),
    ("久原本家（使用済み・香川県観音寺市、調味料）", "久山町", {"食料品", "調味料"}, None, True),
    ("東福運送（使用済み・山形市）", "粕屋町", {"運送", "道路貨物運送"}, None, True),
    # 久留米市
    ("新古賀病院（使用済み・青森県弘前市）", "久留米市", {"医療", "病院"}, None, True),
    ("田主丸中央病院（使用済み・徳島県小松島市）", "久留米市", {"医療", "病院"}, None, True),
    ("BooFooUooJAPAN（会計業務へのAI導入、数値なし）", "久留米市", {"カーリース", "物品賃貸", "自動車販売"}, None, True),
    ("溝田設計事務所（長崎県の橋梁診断の実証、長崎県が使う）", "久留米市", {"建設コンサルタント", "設計"}, None, True),
    ("久留米運送（AIではない）", "久留米市", {"運送", "道路貨物運送"}, None, False),
    ("カラーリングファーム（AIではない）", "久留米市", {"農業", "野菜"}, None, False),
    ("安全タクシー（AIではない）", "久留米市", {"旅客運送", "タクシー"}, None, False),
    ("天年堂（AIではない、お香）", "久留米市", {"その他の製造業", "お香"}, None, False),
    # 宗像市（副業プロ人材の選定。成果なし）
    ("田中建設（AIを課題に選定、成果なし）", "宗像市", {"建設", "総合工事業", "土木"}, None, True),
    ("ライフ電気（AIを課題に選定、5名）", "宗像市", {"建設", "設備工事", "電気工事"}, (5, 5), True),
    ("ヒロメンテナンス商会（AIを課題に選定、金属加工）", "宗像市", {"金属製品", "金属加工", "車両部品"}, None, True),
    # 大野城市・大牟田市・春日市
    ("ミナミホールディングス・南福岡自動車学校（顔認証、ベンダーの事例）", "大野城市", {"自動車学校", "教育"}, None, True),
    ("山本工作所の大牟田工場（本社は北九州市、工場の取組ではない）", "大牟田市", {"金属製品", "ドラム缶"}, None, False),
    ("西鉄バス大牟田のスマートバス停（AIではない）", "大牟田市", {"旅客運送", "バス"}, None, False),
    ("ふく電協のAIチャットボット（行政）", "春日市", {"行政"}, None, False),
    # 九州の他県が使う事例（shared.md の「事例の割り当て」。福岡県では使わない）
    ("税理士法人さくら優和パートナーズ（熊本県が使う、福岡にも拠点）", "所在未確認", {"税理士", "士業"}, None, True),
    ("Reaf の AI 採用代行の介護事業所（社名なし、15名、使わない）", "所在未確認", {"介護", "通所介護"}, (15, 15), True),
]

# (市町村, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 2026-11-04: 九州の割り当て（月の削減時間が1.75時間の倍数＝対象人数×1人の業務量が7の倍数）で、対象人数か業務量を7の倍数にした。
# 業種・業態は stats.md の「市町村ごとの主要産業の候補」の (B) 中小企業の業種（経済センサスの事業所数・従業者数）から選んだ。
PLAN = [
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def other_plans():
    """全県の _calc.py の PLAN を読み、(県, 市町村, 削減時間, 万円) を返す。読めない県・必須の県のファイルがなければ None を入れる（NG）。"""
    out, read, failed = [], {}, []
    paths = sorted(glob.glob(os.path.join(ROOT, "data", "area", "*", "_calc.py")))
    found = {os.path.basename(os.path.dirname(p)): p for p in paths}
    for pref in REQUIRED:
        if pref not in found:
            print(f"NG {pref} の _calc.py がない（必須）")
            out.append(None)
            failed.append(pref)
    for pref, path in found.items():
        if pref == SELF:
            continue
        src = open(path, encoding="utf-8").read()
        try:
            rows = READERS.get(pref, read_plan_standard)(src)
        except Exception as e:  # noqa: BLE001 形が違う。エラーにせず、読めなかった県として表示する
            print(f"NG {pref} の PLAN が読めない（{type(e).__name__}: {e}）。READERS に読み方を足す")
            out.append(None)
            failed.append(pref)
            continue
        n_skip = 0
        for city, ind, n, hrs in rows:
            if ind not in RATE:
                n_skip += 1
                continue
            h = Decimal(str(n)) * Decimal(str(hrs)) * Decimal("0.25")
            out.append((pref, city, h, man(h * RATE[ind])))
        if n_skip:
            print(f"NG {pref} の PLAN に時給の分からない業種が {n_skip}行ある（RATE に足す）")
            out.append(None)
            failed.append(pref)
        read[pref] = len(rows)
        if not rows:
            print(f"（参考）{pref} の PLAN はまだ空（作成中）。行が入ったら再実行する")
    return out, read, failed


def existing():
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（岡山県の _calc.py と同じ拾い方）。"""
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


def used_values():
    """既存の記事と他県の PLAN で使われている時間・万円（辞書）を返す。割り当ての探索用"""
    _, _, ex_h, ex_m, _, _ = existing()
    op, _, _ = other_plans()
    pl_h, pl_m = {}, {}
    for r in op:
        if r is None:
            continue
        label, city, h, m = r
        pl_h.setdefault(h, f"{label}{city}")
        pl_m.setdefault(m, f"{label}{city}")
    return ex_h, ex_m, pl_h, pl_m


def main():
    n_files, n_sec, ex_h, ex_m, ex_s, per_file = existing()
    empty = [k for k, v in per_file.items() if v[1] == 0]
    if empty:
        print("NG 試算の金額を拾えなかった既存の記事:", empty)
    by_pref = Counter(re.sub(r"^2026-1\d-\d+-area-([a-z]+).*", r"\1", k) for k in per_file)
    print(f"既存の地域ページ: {n_files}本（うち試算の節があるもの {n_sec}本、{len(by_pref)}県）。"
          f"拾った値: 時間 {len(ex_h)}種・万円 {len(ex_m)}種・規模 {len(ex_s)}種")
    op, read, failed = other_plans()
    ok = None not in op
    pl_h, pl_m, kyushu_m = {}, {}, {}
    for r in op:
        if r is None:
            continue
        label, city, h, m = r
        pl_h.setdefault(h, f"{label}{city}（_calc.py の PLAN）")
        pl_m.setdefault(m, f"{label}{city}（_calc.py の PLAN）")
        if label in KYUSHU:
            kyushu_m.setdefault(m, f"{label}{city}")
    print(f"他県の PLAN: {len([r for r in op if r])}行（{len(read)}県: "
          + "・".join(f"{k} {v}" for k, v in sorted(read.items())) + f"。時間 {len(pl_h)}種・万円 {len(pl_m)}種）")
    print("九州の他県で読んだ PLAN:", "・".join(k for k in KYUSHU if k in read) or "なし",
          "／まだない県:", "・".join(k for k in KYUSHU if k not in read and k not in failed) or "なし")
    if failed:
        print("NG 読めなかった県:", "・".join(failed))
    if os.path.exists(os.path.join(HERE, "cases_outside.md")):
        print("（注意）cases_outside.md がある。県外の会社（業態・従業員数）を CASES に足したか確かめる")

    seen_h, seen_m, seen_s = {}, {}, {}
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
                print(f"  NG 福岡県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                extra = "（九州の他県。福岡側が直す）" if label == "金額" and key in kyushu_m else ""
                print(f"  NG 他県の PLAN と{label}が重なる{extra}: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 福岡県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
            ok = False
        seen_s[size] = city
        if (h * 4) % 1 != 0:
            print(f"  NG {city} の時間が0.25時間刻みでない ({h})")
            ok = False
        elif int(h * 4) % 7 != KYUSHU_MOD:
            print(f"  NG {city} の時間が九州の割り当て（×4 を7で割った余り {KYUSHU_MOD}）でない ({h}、余り {int(h * 4) % 7})")
            ok = False
        if abs((yen % 1000) - 500) <= 100:
            print(f"  NG {city} の金額が四捨五入の境目に近い（{yen}円）")
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
        print("NG slug が _brief.md と違う:", sorted(slugs ^ SLUGS))
        ok = False
    if not PLAN:
        print("NG PLAN が空")
        print("NG")
        return
    n_ex_size = sum(1 for p in PLAN if p[5] in ex_s)
    print(f"\n市町村ページ: {len(PLAN)}、市町村名の重なり: {len(PLAN) - len({p[0] for p in PLAN})}")
    print(f"時間の範囲 {min(seen_h)}〜{max(seen_h)}時間、金額の範囲 約{min(seen_m)}〜{max(seen_m)}万円、規模 {min(seen_s)}〜{max(seen_s)}名")
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは福岡県の中だけを NG にする）")
    print(f"（参考）1人の業務量が◯.25・◯.75時間のページ: {sum(1 for p in PLAN if (Decimal(str(p[8])) * 2) % 1 != 0)}件")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 60 else "NG")


if __name__ == "__main__":
    main()
