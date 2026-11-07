#!/usr/bin/env python3
"""滋賀県19市町の試算の割り当てを計算し、重なりを確かめる（2026-11-07）。

data/area/kagoshima/_calc.py を元に作った。県ページ（/area/shiga/）には試算を入れないので、PLAN は19行。

前提: 月の削減時間 = 対象人数 × 1人の月の業務量 × 25%
      月の時間換算額 = 月の削減時間 × 時間単価（wages.md の人件費時給〔全国の時給①×1.2〕を十円単位に丸めた値）
      万円は小数1桁に四捨五入して比べる（記事の「約◯万円」と同じ）。

確かめること:
  0. **奈良・和歌山・滋賀の取り決め**: 月の削減時間（0.25時間刻み）×4 を3で割った余りが 2（滋賀県）の時間だけを使う
     （0.5, 1.25, 2.0, 2.75, … の0.75時間刻み。data/area/_kinki/shared.md）
  1. 19ページの中で、月の削減時間・月の時間換算額（万円、小数1桁）・従業員数が重ならない
  2. 既存の全県の地域ページ（articles/2026-1?-*-area-*.md、滋賀県を除く）の「## 試算」の節の「◯時間」「◯万円」と重ならない
  3. 全県の data/area/*/_calc.py の PLAN（滋賀県を除く。glob で全部読む）の月の削減時間・月の時間換算額と重ならない。
     読めないファイルは警告。REQUIRED の県はファイルがなければ NG。金額が奈良・和歌山・北海道と重なったら、先に push した県を優先する
  4. 時間は0.25時間刻み。金額が四捨五入の境目（◯.◯5万円）から100円より離れている
  5. 試算の業種（業態）・規模が cases.md・cases_outside.md の事例の会社と同じにならない（CASES と照合。鹿児島と同じ判定）
  6. slug が _brief.md の19市町と一致する
  7. 試算の業種が wages.md の9業種にある（農業・漁業・林業は試算の業種にしない）
使い方: python3 data/area/shiga/_calc.py          （末尾に OK / NG を出す）
        python3 data/area/shiga/_calc.py free <業種> <最小時間> <最大時間>   （空いている時間と金額を並べる）
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
SELF = "shiga"
KYUSHU_MOD = 2  # 近畿3県の割り当て（月の削減時間×4 を3で割った余り）。滋賀県は 2
DIV = 3

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
    # 市（13）
    "otsu", "hikone", "nagahama", "omihachiman", "kusatsu-city", "moriyama", "ritto", "koka", "yasu", "konan-shiga",
    "takashima", "higashiomi", "maibara",
    # 町（6）
    "hino-town-shiga", "ryuo", "aisho", "toyosato", "kora", "taga",
}

# 九州以外で照合が必須の県（2026-11-04 にある _calc.py）。ファイルがなければ NG
REQUIRED = ("gifu", "hiroshima", "nagano", "okayama", "shimane", "tottori", "yamaguchi", "yamanashi",
            "fukuoka", "saga", "nagasaki", "kumamoto", "oita", "miyazaki", "kagoshima",
            "gunma", "ibaraki", "tochigi", "okinawa", "hokkaido")

# cases.md・cases_outside.md・subsidy_a_areas.md（採択・交付決定の手がかり）の事例の会社（2026-11-04）
# (会社名, 市町村〔県外は「県外」、所在を確かめていないものは「所在未確認」〕, 業態のキー,
#  従業員数〔(下限, 上限)。1つの値なら (n, n)。分からなければ None〕, AI の事例か〔実証・採択・交付決定・使用済み・目標を含む〕)
# cases2.md（2026-11-04 の補充調査）の会社も足した（「# cases2.md」の行）。cases2.md が更新されたら足して再実行する
CASES = [
    # cases.md（2026-11-07）。県「ものづくりAIパイロット事業」の参加5社（成果未公表）ほか。業種は companies の担当の確認を待つ
    ("ハヤミ工産（ものづくりAIパイロット事業。AVファニチャー、公式90名）", "長浜市", {"家具・装備品", "AVファニチャー"}, (90, 90), True),
    ("原馬化成（ものづくりAIパイロット事業。射出成形・塗装・印刷、公式46名）", "長浜市", {"プラスチック製品", "射出成形"}, (46, 46), True),
    ("江州計器工業（ものづくりAIパイロット事業。射出成形の長さ計、公式14名）", "大津市", {"プラスチック製品", "射出成形"}, (14, 14), True),
    ("廣瀬バルブ工業（ものづくりAIパイロット事業）", "彦根市", {"業種未確認"}, None, True),
    ("日光精器（ものづくりAIパイロット事業。電気製品・医療機器、公式200名〔2020年〕、登記は大阪府枚方市・公式の本社は近江八幡市）", "近江八幡市", {"電気機械", "医療機器"}, (200, 200), True),
    ("Auto-IDフロンティア（社内の生成AI、プラザ R7 成果報告）", "守山市", {"業種未確認"}, None, True),
    ("ワボウ電子（AI のデータ抽出の講座、プラザ R7 成果報告）", "長浜市", {"電子部品", "業種未確認"}, None, True),
    ("警備会社（草津商工会議所の支援、AI 交通誘導、社名なし）", "草津市", {"警備"}, None, True),
    ("MotorAI（AI を作る側）", "草津市", {"情報サービス", "ソフトウェア"}, None, True),
    ("アヤハエンジニアリング（AI を作る側）", "草津市", {"情報サービス", "ソフトウェア"}, None, True),
    # cases_outside.md（2026-11-07）
    ("丸紅（静岡県島田市、土木。図面の数量拾い、69人）", "県外", {"建設", "総合工事業", "土木"}, (69, 69), True),
    ("AMED 介護DX実証の老健5施設（匿名）", "県外", {"介護", "介護老人保健施設"}, None, True),
    ("SIP 実証の訪問看護6ステーション（新潟県長岡市・三条市）", "県外", {"医療", "訪問看護"}, None, True),
    ("石田運輸商会（秋田県大館市、33人。AI の数値なし）", "県外", {"運送", "道路貨物運送"}, (33, 33), True),
    ("合通カシロジ（大阪府松原市、倉庫・物流。年約720時間はベンダーの推定）", "県外", {"運輸", "倉庫業"}, None, True),
    ("堀田木工所（広島県、家具、50名）", "県外", {"家具・装備品", "木製家具"}, (50, 50), True),
    ("イシグロ（管材商社）", "県外", {"卸売", "機械器具卸"}, None, True),
]

# (市町, slug, 業種, 業態, 業態のキー, 従業員数, 対象業務, 対象人数, 1人の月の業務量[時間])
# 業種は stats.md の「市町ごとの主要産業の候補」の (B) 中小企業の業種から選ぶ。大企業の工場と読める中分類、農林漁業は試算の業種にしない。
PLAN = [
    ('大津市', 'otsu', '情報通信業', 'ソフトウェア業（業務システムの受託開発・保守）', {'情報サービス', 'ソフトウェア受託開発', '業務システム'}, 74,
     '顧客からの問い合わせ・障害連絡への一次回答の下書きと、打合せ記録の要約、仕様書・提案書の下書き', 47, 25.0),
    ('彦根市', 'hikone', '製造業', '印刷（商業印刷・パッケージ印刷）', {'商業印刷', '印刷'}, 58,
     '取引先からの校正・納期・仕様の問い合わせへの回答と、見積書・作業指示書の作成、入稿データの点検の記録', 40, 25.25),
    ('長浜市', 'nagahama', '製造業', '繊維（絹織物の製織と整理加工）', {'織物', '繊維', '絹織物'}, 44,
     '問屋・アパレルの取引先からの納期・在庫・仕様の問い合わせへの回答と、生地の仕様書・商品の説明文、生産の記録の取りまとめ', 32, 27.25),
    ('近江八幡市', 'omihachiman', '卸売業・小売業', '食肉の卸売・小売（牛肉の加工と店舗・通販での販売）', {'卸売', '食肉', '小売'}, 54,
     '通販・店舗の客と飲食店の取引先からの在庫・配送・部位の問い合わせへの回答と、商品の説明文、贈答の注文の取りまとめ', 40, 22.25),
    ('草津市', 'kusatsu-city', '学術研究・専門技術サービス', '技術サービス（製品の試験・分析の受託）', {'分析', '技術サービス', '試験'}, 72,
     '依頼元との打合せ記録の要約と、試験・分析の報告書の下書き、見積書・受付の連絡文の作成', 20, 24.25),
    ('守山市', 'moriyama', '運輸業・郵便業', '倉庫業（工場の部品・製品の保管と配送）', {'倉庫業', '運輸'}, 68,
     '荷主からの在庫・入出庫の問い合わせへの回答と、入出庫の記録・在庫報告の作成、配送業者への手配の連絡', 38, 26.5),
    ('栗東市', 'ritto', '卸売業・小売業', '機械器具の卸売（工場向けの機器・部品・工具）', {'卸売', '工具', '機械器具卸'}, 85,
     '工場の取引先からの在庫・納期・代替品の問い合わせへの回答と、見積書・発注書の作成、メーカーへの照会文の下書き', 28, 38.75),
    ('甲賀市', 'koka', '製造業', '窯業・土石（陶器・陶製品の製造）', {'陶磁器', '窯業・土石', '陶器'}, 32,
     '問屋・小売店・通販の取引先からの在庫・納期・仕様の問い合わせへの回答と、商品の説明文、出荷の記録の取りまとめ', 19, 23.0),
    ('野洲市', 'yasu', '製造業', '生産用機械（工場の自動化設備・治具の設計製作）', {'自動化設備', '治具', '生産用機械'}, 64,
     '顧客との仕様の打合せ記録の要約と、見積書・取扱説明書・設計変更の連絡書の下書き', 40, 26.75),
    ('湖南市', 'konan-shiga', '運輸業・郵便業', '道路貨物運送（工業団地の部品・製品の輸送）', {'運送', '道路貨物運送'}, 118,
     '荷主からの配送状況・納品の問い合わせへの回答と、配車の連絡、運行の記録・点呼記録の取りまとめ', 32, 37.75),
    ('高島市', 'takashima', '宿泊・飲食サービス業', '湖畔の旅館・民宿（夏の水遊び・冬のスキーの客を含む）', {'民宿', '宿泊', '旅館'}, 42,
     '予約サイト・メールの問い合わせへの返信の下書きと、体験・送迎の手配の連絡、館内案内の多言語の文の作成', 25, 38.0),
    ('東近江市', 'higashiomi', '製造業', '金属製品（板金・溶接による部品の製造）', {'溶接', '板金', '金属製品'}, 88,
     '取引先からの図面変更・納期の問い合わせへの回答と、作業手順書・検査記録・不具合の報告書の取りまとめ', 40, 28.25),
    ('米原市', 'maibara', '製造業', 'プラスチック製品（射出成形品の製造）', {'プラスチック製品', '射出成形'}, 95,
     '取引先からの金型・納期・品質の問い合わせへの回答と、成形条件・検査記録の取りまとめ、不具合の報告書の下書き', 29, 40.0),
    ('日野町', 'hino-town-shiga', '医療・福祉', '介護老人保健施設（通所リハビリを併設）', {'介護', '介護老人保健施設'}, 62,
     'リハビリ・ケアの記録の要約と、入所・退所の説明文書、居宅のケアマネジャーへの報告書の作成', 26, 40.0),
    ('竜王町', 'ryuo', '運輸業・郵便業', '道路貨物運送（自動車部品・資材の工場向けの定期輸送）', {'運送', '道路貨物運送'}, 48,
     '配車表の下書きと、荷主への到着予定・遅延の連絡、運転日報・点呼記録の集計', 16, 38.75),
    ('愛荘町', 'aisho', '製造業', '家具・装備品（木製の家具・建具の製造）', {'建具', '木製家具', '家具・装備品'}, 34,
     '工務店・小売店の取引先からの見積・納期・仕様の問い合わせへの回答と、図面の確認の連絡、製作の記録の取りまとめ', 20, 41.5),
    ('豊郷町', 'toyosato', '医療・福祉', '訪問看護ステーション（訪問リハビリを含む）', {'訪問看護', '医療'}, 28,
     '訪問看護の記録の清書と、主治医への報告書・計画書の下書き、家族への連絡文の作成', 16, 28.25),
    ('甲良町', 'kora', '建設業', '総合工事業（土木・農業用水路の工事）', {'土木', '総合工事業', '建設'}, 30,
     '工事日報・安全書類の取りまとめと、発注者への工程の連絡文、工事写真の整理', 20, 31.75),
    ('多賀町', 'taga', '製造業', '食料品（和菓子の製造と販売）', {'和菓子', '食料品', '菓子'}, 56,
     '土産物店・通販の取引先からの原材料・賞味期限・アレルゲンの問い合わせへの回答と、商品の表示の文、製造の記録の取りまとめ', 31, 32.0),
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
    print("| 市町村 | 業種（業態） | 従業員 | 対象人数×業務量×25% | 月の削減時間 | 時間単価 | 月の時間換算額 | 年間 | ×4 を3で割った余り |")
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
            print(f"  NG {city} の時間 {h} は近畿3県の割り当て（×4 を3で割った余り {KYUSHU_MOD}）に合わない（余り {res}）")
            ok = False
        for label, key, seen, exd, pld in (("時間", h, seen_h, ex_h, pl_h), ("金額", m, seen_m, ex_m, pl_m)):
            if key in seen:
                print(f"  NG 滋賀県の中で{label}が重なる: {city} と {seen[key]} ({key})")
                ok = False
            seen[key] = city
            if key in exd:
                print(f"  NG 既存の記事と{label}が重なる: {city} と {exd[key]} ({key})")
                ok = False
            if key in pld:
                print(f"  NG 他県の PLAN と{label}が重なる: {city} と {pld[key]} ({key})")
                ok = False
        if size in seen_s:
            print(f"  NG 滋賀県の中で規模が重なる: {city} と {seen_s[size]} ({size}名)")
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
    print(f"（参考）既存の記事の試算の見出しと同じ規模: {n_ex_size}件（規模の重なりは滋賀県の中だけを NG にする）")
    for x in notes:
        print("（参考）", x)
    print("業種の内訳:", dict(Counter(p[2] for p in PLAN)))
    print("OK" if ok and not empty and len(PLAN) == 19 else "NG")


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
