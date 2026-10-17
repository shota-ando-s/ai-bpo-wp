#!/usr/bin/env python3
"""記事Markdownから検証すべき事実的主張を抜き出し、AIO・LLMO 上の危険箇所を機械的に洗い出す。

使い方:
    python3 .claude/skills/fact-check/scripts/extract_claims.py articles/2026-10-14-foo.md
    python3 .claude/skills/fact-check/scripts/extract_claims.py articles/foo.md --check-links --site
    python3 .claude/skills/fact-check/scripts/extract_claims.py articles/foo.md --json

--check-links  本文の外部リンクに実際にアクセスし、リンク切れを ERROR にする
--site         他の記事で同じ用語を別の言い方で定義していないかを並べて出す
--json         検証エージェントに渡すための JSON を出力する

ERROR が1件でもあれば終了コード1。
"""
import argparse
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

# 主張の種類を判定するパターン
NUM = r"[0-9０-９][0-9０-９,，.．]*"
CATEGORY_PATTERNS = [
    ("数値・統計", rf"{NUM}\s*(%|％|割|倍|兆|億|万|千|円|社|人|名|件|時間|日|か月|ヶ月|カ月|年間|ポイント|pt)"),
    ("日付・時期", rf"({NUM}\s*年\s*({NUM}\s*月)?|令和\s*{NUM}\s*年|平成\s*{NUM}\s*年)"),
    ("法律・制度", r"((?<![方手寸文作])法(?!人)|法律|条例|政令|省令|ガイドライン|指針|補助金|助成金|交付金|税制|第\s*[0-9０-９一二三四五六七八九十百]+\s*条|義務|罰則)"),
    ("出典・引用", r"(によると|によれば|の調査|調査では|白書|統計調査|が発表|が公表|報告書)"),
    ("定義", r"^[^。]{1,40}とは[、，]"),
    ("最上級・断定", r"(最安|最高|最速|最も|唯一|初めて|日本初|業界初|No\.?\s*1|ナンバーワン|必ず(?:成功|削減|回収|効果|改善|採択|通る|儲)|絶対|確実に|100\s*[%％]|すべての企業|誰でも)"),
    ("価格・料金", rf"({NUM}\s*円|無料|月額|年額|初期費用|料金|価格)"),
]

SUPERLATIVE = CATEGORY_PATTERNS[5][1]
TIMESTAMP = rf"({NUM}\s*年\s*({NUM}\s*月)?\s*(時点|現在)|{NUM}\s*年度|{NUM}\s*年\s*{NUM}\s*月|{NUM}\s*年の|{NUM}\s*年に)"
SELF_ESTIMATE = r"(当社試算|当社調べ|想定例|試算)"
ANAPHORA_START = r"^(それ|これ|その|この|あれ|前述|上記|先述|以上|同様に|そのため|このため|したがって)"
PRIMARY_DOMAINS = (".go.jp", ".lg.jp", ".ac.jp", ".or.jp", "e-gov.go.jp", "stat.go.jp", "jil.go.jp",
                   "meti.go.jp", "mhlw.go.jp", "soumu.go.jp", "chusho.meti.go.jp", "ipa.go.jp")
SECONDARY_HINTS = ("note.com", "qiita.com", "zenn.dev", "ameblo.jp", "hatena", "matome", "wikipedia.org")

# 官公庁のサイトには、ブラウザ以外の User-Agent を 403 で弾くものがある（中小企業庁など）
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
PLAIN_UA = "hikitsugi-linkcheck/1.0"

results = []  # (level, message)


def err(msg):
    results.append(("ERROR", msg))


def warn(msg):
    results.append(("WARN", msg))


def parse(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        return {}, text, 0
    parts = text.split("---", 2)
    offset = parts[0].count("\n") + parts[1].count("\n") + 1
    return (yaml.safe_load(parts[1]) or {}), parts[2], offset


def plain(md):
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_`>#]", "", s)
    return s.strip()


def blocks(body, offset):
    """段落・表・リスト項目を (行番号, 種類, 見出し, Markdown, 見出し直後か) で返す。

    表は1つのまとまりとして返す。AI は表を丸ごと抜き出して引用するため。
    """
    out = []
    heading = ""
    in_faq = False
    first = False
    para, start = [], 0
    table, tstart = [], 0
    lines = body.split("\n")

    def flush():
        nonlocal para, table, first
        if para:
            out.append((start, "FAQ回答" if in_faq else "段落", heading, " ".join(para), first))
            para = []
            first = False
        if table:
            out.append((tstart, "表", heading, "\n".join(table), False))
            table = []

    for i, line in enumerate(lines):
        no = offset + i + 1
        s = line.strip()
        m = re.match(r"^(#{2,6})\s+(.+)$", s)
        if m:
            flush()
            heading = m.group(2).strip()
            first = True
            if len(m.group(1)) == 2:
                in_faq = "よくある質問" in heading
            out.append((no, "見出し", heading, heading, False))
            continue
        if not s:
            flush()
            continue
        if s.startswith("|"):
            if para:
                flush()
            if not table:
                tstart = no
            if not re.match(r"^\|[\s:|-]+\|$", s):
                table.append(s)
            continue
        if table:
            flush()
        if re.match(r"^([-*]|\d+\.)\s+", s):
            flush()
            out.append((no, "リスト", heading, re.sub(r"^([-*]|\d+\.)\s+", "", s), False))
            continue
        if s.startswith("!["):
            continue
        if not para:
            start = no
        para.append(s)
    flush()
    return out


def links_in(md):
    return re.findall(r"\[([^\]]*)\]\((https?://[^)\s]+)\)", md)


DATE = rf"({NUM}\s*年\s*)?{NUM}\s*月\s*{NUM}\s*日|{NUM}/{NUM}(/{NUM})?|{NUM}\s*時"


def classify(text):
    # 「10月16日」「2026/10/30」「17時」のような日付・時刻は数値・統計として数えない
    no_dates = re.sub(DATE, "", text)
    cats = []
    for name, pat in CATEGORY_PATTERNS:
        target = no_dates if name in ("数値・統計", "価格・料金") else text
        if re.search(pat, target, re.M):
            cats.append(name)
    return cats


def source_kind(url):
    host = re.sub(r"^https?://", "", url).split("/")[0].lower()
    if host.endswith(PRIMARY_DOMAINS) or host in PRIMARY_DOMAINS:
        return "一次（公的機関）"
    if any(h in host for h in SECONDARY_HINTS):
        return "二次以下（要差し替え検討）"
    return "要判断"


def check_url(url):
    # 日本語を含むURL（帝国データバンクのPDFなど）はそのままだと送れないので、パーセントエンコードする
    safe = urllib.parse.quote(url, safe=":/?&=%#+,;@!$'()*~")
    # 逆に、ブラウザの User-Agent を 406 で弾くサイトもある（岩手県立大学のリポジトリ iwate-pu.repo.nii.ac.jp など）。
    # 403/406 のときは、ブラウザ以外の User-Agent で1回だけ取り直す
    last = None
    for ua in (BROWSER_UA, PLAIN_UA):
        req = urllib.request.Request(safe, method="GET", headers={"User-Agent": ua})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return url, r.status, r.geturl()
        except urllib.error.HTTPError as e:
            last = (url, e.code, url)
            if e.code not in (403, 406):
                return last
        except Exception as e:  # noqa: BLE001 - 接続エラーはまとめて報告する
            return url, f"接続失敗: {type(e).__name__}", url
    return last


def definitions(body):
    """「Xとは、…。」の (X, 定義文) を返す。"""
    out = []
    for m in re.finditer(r"(?:^|\n)\s*([^\n。]{1,30}?)とは[、，]([^\n]*?。)", plain(body)):
        term = re.sub(r"^.*[「『]", "", m.group(1)).strip("」』 ")
        out.append((term, f"{m.group(1)}とは、{m.group(2)}"))
    return out


def site_definitions(path, terms):
    found = {t: [] for t in terms}
    for f in sorted(glob.glob(os.path.join(ROOT, "articles", "*.md"))):
        if os.path.abspath(f) == os.path.abspath(path):
            continue
        try:
            _, body, _ = parse(f)
        except Exception:
            continue
        for term, sentence in definitions(body):
            if term in found:
                found[term].append((os.path.basename(f), sentence))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--check-links", action="store_true")
    ap.add_argument("--site", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    meta, body, offset = parse(args.path)
    full_plain = plain(body)

    # --- 主張の抽出 ---
    claims = []
    all_blocks = blocks(body, offset)
    # 見出しごとに、出典リンクか「当社試算」がどこかにあるか（表の前後に出典を書く書き方を許す）
    section_sourced = {}
    for _, kind, heading, md, _ in all_blocks:
        if kind != "見出し" and (links_in(md) or re.search(SELF_ESTIMATE, md)):
            section_sourced[heading] = True

    for no, kind, heading, md, lead in all_blocks:
        if kind == "見出し":
            continue
        text = plain(md)
        cats = classify(text)
        if not cats:
            continue
        ls = links_in(md)
        has_source = bool(ls) or bool(re.search(SELF_ESTIMATE, text))
        has_time = bool(re.search(TIMESTAMP, text))
        # AI が単独で引用しやすい位置: 定義文・FAQ回答・表・各見出し直後の段落
        quotable = kind in ("FAQ回答", "表") or "定義" in cats or lead
        claims.append({
            "id": f"C{len(claims) + 1:02d}",
            "line": no,
            "kind": kind,
            "heading": heading,
            "categories": cats,
            "text": text,
            "links": [u for _, u in ls],
            "has_source": has_source,
            "has_time": has_time,
            "quotable": quotable,
            "section_sourced": bool(section_sourced.get(heading)),
        })

    # --- 機械的な点検 ---
    for c in claims:
        loc = f"L{c['line']} {c['id']}"
        if "数値・統計" in c["categories"] and not c["has_source"]:
            hard = c["quotable"] and not c["section_sourced"]
            (err if hard else warn)(
                f"{loc}: 数値に出典リンクも「当社試算」もない"
                f"{'' if hard else '（同じ見出し内に出典あり。対応しているか確認）' if c['section_sourced'] else ''}"
                f" — {c['text'][:60]}")
        elif "出典・引用" in c["categories"] and not c["has_source"]:
            warn(f"{loc}: 調査・発表に触れているが出典リンクがない — {c['text'][:60]}")
        if "数値・統計" in c["categories"] and c["has_source"] and not c["has_time"] and not re.search(SELF_ESTIMATE, c["text"]):
            warn(f"{loc}: 数値の時点（〇年〇月時点・〇年調査）が同じ文中にない — {c['text'][:60]}")
        if re.search(SUPERLATIVE, c["text"]):
            warn(f"{loc}: 最上級・断定表現。根拠がなければ弱める — {c['text'][:60]}")
        if c["kind"] in ("段落", "FAQ回答") and re.search(ANAPHORA_START, c["text"]):
            warn(f"{loc}: 指示語で始まり、単独で引用されると意味が通らない — {c['text'][:40]}")

    for i, line in enumerate(body.split("\n")):
        no = offset + i + 1
        if re.search(r"オフボード(?!ィング)", line):
            err(f"L{no}: 旧ブランド名「オフボード」が残っている（ヒキツギAIに置換）")
        if re.search(r"要出典", line):
            err(f"L{no}: 「要出典」が残っている。AI は注記ごと引用するので、確認できない主張は削除する")

    if not re.search(TIMESTAMP, full_plain):
        warn("本文に情報の時点（「2026年10月時点」など）が一度も書かれていない")

    excerpt = str(meta.get("excerpt") or "")
    if excerpt and re.search(NUM, excerpt):
        for n in set(re.findall(rf"{NUM}\s*(?:%|％|円|万|億|社|人|倍)", excerpt)):
            n = n.replace(" ", "")
            num = re.match(r"[0-9,.]+", n).group(0)
            unit = n[len(num):]
            # 「19%」と本文の「19.0%」のように、小数点以下の0だけが違う表記は同じ数値とみなす
            pattern = re.escape(num) + r"(?:\.0+)?\s*" + re.escape(unit)
            if not re.search(pattern, full_plain):
                err(f"excerpt の数値「{n}」が本文にない。メタディスクリプションは AI にも引用される")

    # --- リンク ---
    all_links = sorted({u for _, u in links_in(body)})
    link_report = [{"url": u, "kind": source_kind(u)} for u in all_links]
    if args.check_links and all_links:
        with ThreadPoolExecutor(max_workers=8) as ex:
            status = {u: (s, final) for u, s, final in ex.map(check_url, all_links)}
        for item in link_report:
            s, final = status[item["url"]]
            item["status"] = s
            if final != item["url"]:
                item["redirect"] = final
            if s == 429:
                # アクセス過多による一時的な拒否（Internet Archive など）。リンク切れではない
                warn(f"アクセス制限（429）で確認できず。時間をおいてブラウザで確認: {item['url']}")
            elif not (isinstance(s, int) and s < 400):
                err(f"リンク切れ・取得失敗 ({s}): {item['url']}")

    # --- サイト内の定義の食い違い ---
    site = {}
    if args.site:
        defs = definitions(body)
        site = site_definitions(args.path, [t for t, _ in defs])
        site = {t: {"this": s, "others": site[t]} for t, s in defs if site.get(t)}

    if args.json:
        json.dump({"file": args.path, "title": meta.get("title"), "claims": claims, "links": link_report,
                   "site_definitions": site, "issues": results}, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        print(f"# {meta.get('title', args.path)}\n")
        print(f"## 検証対象の主張 {len(claims)}件（★ = AI が単独で引用しやすい位置）\n")
        for c in claims:
            mark = "★" if c["quotable"] else " "
            flags = ("" if c["has_source"] else " [出典なし]") + ("" if c["has_time"] else " [時点なし]")
            print(f"{mark} {c['id']} L{c['line']} ({c['kind']}/{','.join(c['categories'])}){flags}")
            text = c["text"] if c["kind"] == "表" else c["text"][:160]
            print("    " + text.replace("\n", "\n    "))
            for u in c["links"]:
                print(f"    → {u}")
        print(f"\n## 外部リンク {len(link_report)}件\n")
        for item in link_report:
            st = f" [{item['status']}]" if "status" in item else ""
            rd = f" → {item['redirect']}" if "redirect" in item else ""
            print(f"- {item['kind']}{st} {item['url']}{rd}")
        if args.site:
            print("\n## 他記事の同じ用語の定義\n")
            if not site:
                print("（重複する定義なし）")
            for term, d in site.items():
                print(f"### {term}\n- この記事: {d['this']}")
                for f, s in d["others"]:
                    print(f"- {f}: {s}")
        print("\n## 機械点検\n")
        if not results:
            print("問題なし")
        for level, msg in results:
            print(f"{'❌' if level == 'ERROR' else '⚠️'} {level}: {msg}")

    sys.exit(1 if any(l == "ERROR" for l, _ in results) else 0)


if __name__ == "__main__":
    main()
