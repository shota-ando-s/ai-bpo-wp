#!/usr/bin/env python3
"""京都府26市町村の試算の割り当てを計算し、重なりを確かめる（2026-11-11）。

data/area/shiga/_calc.py を元に作った。府ページ（/area/kyoto/）には試算を入れないので、PLAN は26行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **静岡・愛知・三重・京都の取り決め**: 月の削減時間（0.25時間刻み）×4 を4で割った余りが 3（京都府）の時間だけを使う
     （端数が .75 の時間。data/area/_tokai/shared.md）
  1. 26ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、京都府を除く）の「## 試算」の節の「◯時間」「◯万円」と重ならない
  3. 全県の data/area/*/_calc.py の PLAN（京都府を除く。glob で全部読む）の月の削減時間・月の時間換算額と重ならない。
     読めないファイルは警告。REQUIRED の県はファイルがなければ NG。金額が静岡・愛知・三重・北海道と重なったら、先に push した県を優先する
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md の事例の会社と同じにならない（CASES と照合。鹿児島と同じ判定）
  6. slug が _brief.md の26市町村と一致する
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
使い方: python3 data/area/kyoto/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/kyoto/_calc.py free <業種> <最小時間> <最大時間>   （空いている時間と金額を並べる）
他県の PLAN は後から変わることがあるので、push の直前に git pull してもう一度実行する。
"""
import ast
import glob
import importlib.util
import io
import os
import re
import sys
from collections import Counter
from contextlib import redirect_stdout
from decimal import Decimal, ROUND_HALF_UP

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ART = os.path.join(ROOT, "articles")
HERE = os.path.dirname(os.path.abspath(__file__))
SELF = "kyoto"
KYUSHU_MOD = 3  # 静岡・愛知・三重・京都の割り当て（月の削減時間×4 を4で割った余り）。京都府は 3
DIV = 4

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
    # 市（15）
    "kyoto-city", "fukuchiyama", "maizuru", "ayabe", "uji", "miyazu", "kameoka", "joyo", "muko", "nagaokakyo",
    "yawata", "kyotanabe", "kyotango", "nantan", "kizugawa",
    # 町（10）・村（1）
    "oyamazaki", "kumiyama", "ide", "ujitawara", "kasagi", "wazuka", "seika", "kyotamba", "ine", "yosano",
    "minamiyamashiro",
}

# 九州以外で照合が必須の県（2026-11-04 にある _calc.py）。ファイルがなければ NG
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima",
            "gunma", "ibaraki", "tochigi", "okinawa", "hokkaido",
            "shiga", "nara", "wakayama")

# cases.md・cases_outside.md・subsidy_a_areas.md（採択・交付決定の手がかり）の事例の会社（2026-11-04）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・交付決定・使用済み・目標を含む〕)
# cases2.md（2026-11-04 の補充調査）の会社も足した（「# cases2.md」の行）。cases2.md が更新されたら足して再実行する
CASES = [
    # cases.md（2026-11-11）
    ("伊東板金工業（AI でプログラムを作る曲げ機。機械全体の効果、88人）", "京都市", {"金属製品", "板金"}, (88, 88), True),
    ("京都電機器（AI 外観検査、検証段階の見込み、235名）", "宇治市", {"電子部品", "電気機械"}, (235, 235), True),
    ("HILLTOP（加工プログラムの自動作成、AI と明記なし、123人）", "宇治市", {"金属製品", "切削"}, (123, 123), True),
    ("井上株式会社（ブドウの摘粒の AI、開発側の実証）", "福知山市", {"情報サービス", "ソフトウェア"}, None, True),
    ("旅館こうろ（PR 記事、数値なし）", "京都市", {"宿泊", "旅館"}, None, True),
    ("Bird fab studio（生地のマッチング、4人）", "舞鶴市", {"繊維・衣服等卸売"}, (4, 4), True),
    ("長崎工業（中央会の一覧の計画名、金属フィン）", "舞鶴市", {"金属製品"}, None, True),
    ("西陣織の加地織物・大光・細尾（中央会の一覧の計画名）", "京都市", {"繊維", "織物"}, None, True),
    ("宇治田原製茶場（GROWTH VERSE の AIMSTAR、数値なし）", "宇治田原町", {"茶", "製茶"}, None, True),
    ("Geek Guild（AI を作る側、西京区）", "京都市", {"情報サービス", "ソフトウェア"}, None, True),
    # cases_outside.md（2026-11-11）
    ("ホテルフォーシーズン徳島（観光庁の事例集、23室・5人、定性）", "県外", {"宿泊", "旅館"}, (5, 5), True),
    ("足立翔裕園（東京都足立区の特養、AI 議事録、数値なし）", "県外", {"介護", "特別養護老人ホーム"}, None, True),
]

# 2026-11-11 _assign.py で当てた。端数 .75 の時間で月230時間未満は空きがほぼなく（4h が素数の値だけ残る）、小さい町村は規模を上げて「府内の同じ業種の事業所の例」にした
# (市町, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種は stats.md の「市町ごとの主要産業の候補」の (B) 中小企業の業種から選ぶ。大企業の工場と読める中分類、農林漁業は試算の業種にしない。
PLAN = [
    ('京都市', 'kyoto-city', '卸売業・小売業', '和装品の卸売（呉服・帯・和装小物の問屋）', {'和装', '繊維・衣服等卸売', '卸売'}, 86,
     '小売店・百貨店の取引先からの在庫・納期・仕様の問い合わせへの回答と、商品の説明文・展示会の案内文の作成、受発注の記録の取りまとめ', 52, 26.75),
    ('福知山市', 'fukuchiyama', '建設業', '総合工事業（土木・建築の工事）', {'土木', '総合工事業', '建設'}, 59,
     '工事日報・安全書類の取りまとめと、発注者・協力会社への工程の連絡文、工事写真の整理と報告書の下書き', 35, 41.0),
    ('舞鶴市', 'maizuru', '運輸業・郵便業', '港湾運送・倉庫（港の貨物の荷役・保管と輸送の手配）', {'運輸', '港湾運送', '倉庫業'}, 61,
     '荷主・船会社からの入出港・荷役の予定の問い合わせへの回答と、作業指示書・入出庫の記録の作成、通関業者・運送会社への手配の連絡', 37, 39.0),
    ('綾部市', 'ayabe', '製造業', '金属製品（機械部品の板金・溶接・切削）', {'金属製品', '板金', '溶接'}, 54,
     '取引先からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録の取りまとめ、見積書の下書き', 36, 39.75),
    ('宇治市', 'uji', '卸売業・小売業', '茶の卸売・小売（茶の仕入れ・合組と店舗・通販での販売）', {'小売', '茶', '卸売'}, 56,
     '通販・店舗の客と取引先からの在庫・配送・商品の問い合わせへの回答と、商品の説明文・贈答の注文の取りまとめ、多言語の案内文の作成', 44, 30.25),
    ('宮津市', 'miyazu', '宿泊・飲食サービス業', '旅館・ホテル（観光客の宿泊と食事）', {'旅館', '宿泊'}, 55,
     '予約サイト・メールの問い合わせへの返信の下書きと、送迎・食事の手配の連絡、館内案内の多言語の文の作成', 34, 43.5),
    ('亀岡市', 'kameoka', '製造業', '電子部品（電子部品・基板の受託組立）', {'電子部品', '受託組立'}, 60,
     '取引先からの納期・仕様変更・不具合の問い合わせへの回答と、作業指示書・検査記録の取りまとめ、不具合の報告書の下書き', 47, 29.0),
    ('城陽市', 'joyo', '運輸業・郵便業', '道路貨物運送（食品・資材の地場配送）', {'運送', '道路貨物運送'}, 53,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計', 42, 33.5),
    ('向日市', 'muko', '製造業', '印刷（商業印刷・事務用印刷）', {'商業印刷', '印刷'}, 49,
     '取引先からの校正・納期・仕様の問い合わせへの回答と、見積書・作業指示書の作成、入稿データの点検の記録', 35, 37.0),
    ('長岡京市', 'nagaokakyo', '学術研究・専門技術サービス', '技術サービス（機械の設計と製品の試験の受託）', {'試験', '技術サービス', '設計'}, 57,
     '依頼元との打合せ記録の要約と、設計書・試験報告書の下書き、見積書・仕様の確認の連絡文の作成', 44, 31.25),
    ('八幡市', 'yawata', '運輸業・郵便業', '道路貨物運送（物流センターと店舗の間の食品・日用品の輸送）', {'運送', '道路貨物運送'}, 128,
     '荷主からの配送状況・納品の問い合わせへの回答と、配車の連絡、運行の記録・点呼記録の取りまとめ', 42, 35.5),
    ('京田辺市', 'kyotanabe', '製造業', '窯業・土石（コンクリート製品の製造）', {'窯業・土石', 'コンクリート製品'}, 47,
     '建設会社・資材店からの在庫・納期・規格の問い合わせへの回答と、出荷の記録・試験成績書の取りまとめ、見積書の下書き', 36, 34.75),
    ('京丹後市', 'kyotango', '製造業', '繊維（絹織物の製織）', {'絹織物', '繊維', '織物'}, 45,
     '問屋・染工場の取引先からの納期・在庫・規格の問い合わせへの回答と、生地の仕様書の作成、生産の記録の取りまとめ', 36, 25.75),
    ('南丹市', 'nantan', '製造業', '木材・木製品（製材と住宅用の木材の加工）', {'プレカット', '木材・木製品', '製材'}, 51,
     '工務店・材木店からの在庫・納期・寸法の問い合わせへの回答と、見積書・加工指示書の作成、出荷の記録の取りまとめ', 38, 36.5),
    ('木津川市', 'kizugawa', '医療・福祉', '特別養護老人ホーム（デイサービスを併設）', {'介護', '特別養護老人ホーム'}, 64,
     '介護記録の要約と、家族への連絡文・行事の案内、ケアマネジャー・医療機関への報告書の作成', 38, 38.5),
    ('大山崎町', 'oyamazaki', '製造業', '食料品（惣菜・弁当の製造）', {'食料品', '惣菜'}, 46,
     '取引先からの原材料・アレルゲン・納品の問い合わせへの回答と、商品の表示の文、製造・衛生管理の記録の取りまとめ', 36, 32.75),
    ('久御山町', 'kumiyama', '製造業', 'プラスチック製品（射出成形品の製造）', {'射出成形', 'プラスチック製品'}, 72,
     '取引先からの金型・納期・品質の問い合わせへの回答と、成形条件・検査記録の取りまとめ、不具合の報告書の下書き', 52, 25.75),
    ('井手町', 'ide', '運輸業・郵便業', '道路貨物運送（工場の製品・原材料の輸送）', {'運送', '道路貨物運送'}, 48,
     '荷主からの配送・納品の予定の問い合わせへの回答と、配車の連絡、運転日報の集計', 38, 32.5),
    ('宇治田原町', 'ujitawara', '製造業', '生産用機械（産業機械の部品加工と組立）', {'産業機械', '生産用機械'}, 58,
     '顧客との仕様の打合せ記録の要約と、見積書・取扱説明書・設計変更の連絡書の下書き', 46, 30.5),
    ('笠置町', 'kasagi', '建設業', '総合工事業（土木・住宅の工事）', {'土木', '総合工事業', '建設'}, 37,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理', 29, 43.0),
    ('和束町', 'wazuka', '製造業', '飲料・たばこ・飼料（茶の製造〔荒茶・仕上げ茶〕と販売）', {'飲料', '製茶', '茶'}, 42,
     '茶商・小売店・通販の取引先からの在庫・出荷・商品の問い合わせへの回答と、商品の説明文、製造の記録の取りまとめ', 33, 43.0),
    ('精華町', 'seika', '情報通信業', 'ソフトウェア業（業務システム・データ処理の受託開発）', {'ソフトウェア受託開発', '情報サービス'}, 52,
     '顧客からの問い合わせ・障害連絡への一次回答の下書きと、打合せ記録の要約、仕様書・提案書の下書き', 36, 38.75),
    ('南山城村', 'minamiyamashiro', '医療・福祉', '訪問介護・通所介護（デイサービス）', {'介護', '通所介護', '訪問介護'}, 43,
     '訪問・通所の記録の清書と、ケアマネジャーへの報告書・計画書の下書き、家族への連絡文の作成', 34, 41.5),
    ('京丹波町', 'kyotamba', '製造業', '食料品（農産物の加工品の製造）', {'農産加工', '食料品'}, 50,
     '取引先からの原材料・賞味期限・アレルゲンの問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ', 36, 37.75),
    ('伊根町', 'ine', '宿泊・飲食サービス業', '民宿・旅館（観光客の宿泊と食事）', {'旅館', '民宿', '宿泊'}, 35,
     '予約サイト・メールの問い合わせへの返信の下書きと、食事・送迎の手配の連絡、館内案内の多言語の文の作成', 28, 43.25),
    ('与謝野町', 'yosano', '建設業', '総合工事業（住宅・公共工事）', {'総合工事業', '建設'}, 44,
     '工事日報・安全書類の取りまとめと、発注者・施主への工程の連絡文、工事写真の整理', 34, 39.5),
]


def man(yen):
    """円 → 万円（小数1桁、四捨五入）。yen は Decimal"""
    return (yen / Decimal(10000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def read_plan_text(src):
    """岡山県の形の PLAN を文字列で切り出す（行頭の `PLAN = [` から行頭の `]` まで）。docstring の「PLAN = [」は拾わない"""
    m = re.search(r"^PLAN = \[", src, re.M)
    if not m:
        raise ValueError("行頭の PLAN = [ がない")
    j = src.index("\n]\n", m.start())
    return ast.literal_eval(src[m.start() + 7:j + 2])


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
    九州以外の必須の県のファイルがなければ None を入れる（NG）。読めないファイルは警告だけ（NG にしない）。"""
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
    """既存の地域ページの「## 試算」の節から、結果の時間・万円と、見出しの従業員数を拾う（岡山県・佐賀県の _calc.py と同じ拾い方）。"""
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

    seen_h, seen_m, seen_s = {}, {}, {}
    notes = []
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | 年間 | ×4 を4で割った余り |")
    print("|---|---|---|---|---|---|---|---|---|")
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
        res = int(q) % DIV if q % 1 == 0 else None
        print(f"| {city} | {ind}（{sub}） | {size}名 | {n}名×{hrs}時間×25% | {h.normalize():f}時間 | 約{RATE[ind]:,}円 | 約{m}万円 | 約{y}万円 | {res} |")
        if q % 1 != 0:
            print(f"  NG {city} の時間が0.25時間刻みでない ({h})")
            ok = False
        elif res != KYUSHU_MOD:
            print(f"  NG {city} の時間 {h} は4府県の割り当て（×4 を4で割った余り {KYUSHU_MOD}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 京都府の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 京都府の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
            ok = False
        seen_s[size] = city
        if not border_ok(yen):
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは京都府の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 26 else "NG")


def free(ind, lo, hi):
    """業種 ind で、lo〜hi 時間の空いている（時間, 万円）を並べる"""
    h_used, m_used = used_values()
    mine_h = {Decimal(str(p[7])) * Decimal(str(p[8])) * Decimal("0.25") for p in PLAN}
    mine_m = {man(Decimal(str(p[7])) * Decimal(str(p[8])) * Decimal("0.25") * RATE[p[2]]) for p in PLAN}
    h = Decimal(str(lo))
    out = []
    while h <= Decimal(str(hi)):
        if int(h * 4) % DIV == KYUSHU_MOD and h not in h_used and h not in mine_h:
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
