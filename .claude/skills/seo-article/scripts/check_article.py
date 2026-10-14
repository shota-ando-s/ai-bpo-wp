#!/usr/bin/env python3
"""記事Markdownが SEO・AIO の執筆ルールを満たすかを機械的に点検する。

使い方:
    python3 .claude/skills/seo-article/scripts/check_article.py articles/2026-10-14-foo.md [--kw "メインキーワード"]

ERROR が1件でもあれば終了コード1。WARN は人が判断する項目。
"""
import argparse
import glob
import os
import re
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

results = []  # (level, message)


def err(msg):
    results.append(("ERROR", msg))


def warn(msg):
    results.append(("WARN", msg))


def ok(msg):
    results.append(("OK", msg))


def parse(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    return (yaml.safe_load(parts[1]) or {}), parts[2].strip()


def plain(md):
    """リンク・装飾を外した本文テキスト。"""
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_`>#|]", "", s)
    return s


def other_slugs(path):
    slugs = {}
    for f in glob.glob(os.path.join(ROOT, "articles", "*.md")):
        if os.path.abspath(f) == os.path.abspath(path):
            continue
        try:
            meta, _ = parse(f)
        except Exception:
            continue
        if meta.get("slug"):
            slugs[str(meta["slug"])] = os.path.basename(f)
    return slugs


def sections(body):
    """[(level, heading, text_until_next_heading)]"""
    out = []
    matches = list(re.finditer(r"^(#{1,6})\s+(.+)$", body, re.M))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        out.append((len(m.group(1)), m.group(2).strip(), body[m.end():end].strip()))
    return out


def first_sentence(text):
    """最初の地の文の段落（表・引用・画像は飛ばす）の一文目。"""
    paras = [p for p in re.split(r"\n\s*\n", text)
             if p.strip() and not p.lstrip().startswith(("|", ">", "!", "<"))]
    t = plain(paras[0] if paras else text).strip()
    t = re.sub(r"^\s*[-\d.]+\s*", "", t)
    m = re.search(r"^(.+?[。！？])", t, re.S)
    return (m.group(1) if m else t[:120]).replace("\n", "")


def check(path, kw):
    meta, body = parse(path)

    # --- フロントマター ---
    title = str(meta.get("title") or "")
    if not title:
        err("title がない")
    else:
        n = len(title)
        if n > 40:
            err(f"title が長すぎる（{n}字）。検索結果で切れる。32字前後を目安に")
        elif n > 34:
            warn(f"title が{n}字。主要語が前半にあれば可、なければ詰める")
        else:
            ok(f"title {n}字")
        if kw and kw.split()[0] not in title[:20]:
            warn(f"title の前半20字にメインKW「{kw.split()[0]}」がない")

    excerpt = str(meta.get("excerpt") or "")
    if not excerpt:
        err("excerpt がない（CLAUDE.md の必須項目。Rank Math のメタディスクリプションにも使われる）")
    else:
        n = len(excerpt)
        if not 100 <= n <= 140:
            warn(f"excerpt が{n}字（目安 100〜140字）")
        else:
            ok(f"excerpt {n}字")
        if kw and kw.split()[0] not in excerpt:
            warn("excerpt にメインKWがない")

    if "description" in meta and not excerpt:
        err("description は post.py が送らない。excerpt に書く")

    slug = str(meta.get("slug") or "")
    if not slug:
        err("slug がない（post.py は slug で既存記事を照合する。無いと重複投稿になる）")
    elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        err(f"slug「{slug}」は英小文字・数字・ハイフンのみ")
    else:
        dup = other_slugs(path).get(slug)
        if dup:
            warn(f"slug「{slug}」は {dup} と同じ。更新のつもりでなければ変える")
        else:
            ok(f"slug {slug}")
        base = os.path.basename(path)
        if not base.endswith(f"-{slug}.md"):
            warn(f"ファイル名 {base} が slug と一致しない（YYYY-MM-DD-{slug}.md）")

    for key in ("categories", "tags"):
        if meta.get("type") != "page" and not meta.get(key):
            err(f"{key} がない")
    if meta.get("status") not in ("publish", "draft", "future", "private"):
        warn(f"status が「{meta.get('status')}」")

    # --- 見出し構造 ---
    secs = sections(body)
    if any(lv == 1 for lv, _, _ in secs):
        err("本文に H1（# ）がある。H1 は WordPress がタイトルから出す")
    prev = 1
    for lv, h, _ in secs:
        if lv > prev + 1:
            err(f"見出しレベルが飛んでいる: 「{h}」(H{lv}) の前が H{prev}")
        prev = lv
    h2s = [h for lv, h, _ in secs if lv == 2]
    if len(h2s) < 4:
        warn(f"H2 が{len(h2s)}個。網羅性が足りない可能性")
    else:
        ok(f"H2 {len(h2s)}個")
    q_heads = [h for lv, h, _ in secs if lv in (2, 3) and re.search(r"[？?]$|とは", h)]
    if len(q_heads) < 3:
        warn(f"疑問形・「〜とは」の見出しが{len(q_heads)}個。検索クエリの形の見出しを増やす")

    # --- 冒頭（リード） ---
    lead = body.split("\n## ", 1)[0]
    lead_plain = plain(lead)
    if kw:
        first = kw.split()[0]
        if first not in plain(body)[:150]:
            err(f"冒頭150字にメインKW「{first}」がない")
        else:
            ok("冒頭150字にメインKW")
    if len(lead_plain.strip()) > 400:
        warn(f"リードが{len(lead_plain.strip())}字。結論を早く出す（300字以内目安）")

    # --- 回答先出し: H2 直下の最初の一文 ---
    long_starts = []
    for lv, h, text in secs:
        if lv != 2 or not text or h.startswith(("よくある質問", "まとめ")):
            continue
        s = first_sentence(text.split("\n### ", 1)[0] or text)
        if len(s) > 90:
            long_starts.append(f"「{h}」({len(s)}字)")
    if long_starts:
        warn("H2 直下の最初の一文が長い（AIが抜き出しにくい。60字前後で結論を言い切る）: " + ", ".join(long_starts))

    # --- 定義文 ---
    if re.search(r"とは[、，]?.{2,80}?(です|ことです|を指します|を意味します)", plain(body)):
        ok("定義文（〜とは、〜です）あり")
    else:
        warn("定義文（〇〇とは、〜です）がない")

    # --- FAQ ---
    faq = None
    for i, (lv, h, _) in enumerate(secs):
        if lv == 2 and "よくある質問" in h:
            faq = i
            break
    if faq is None:
        err("「## よくある質問」セクションがない")
    else:
        qs = []
        for lv, h, text in secs[faq + 1:]:
            if lv <= 2:
                break
            if lv == 3:
                qs.append((h, text))
        if not qs and re.search(r"^\*\*Q", secs[faq][2], re.M):
            err("FAQ が **Q.** 形式。テーマの FAQ 抽出は見出ししか拾わないので「### 質問？」にする")
        elif len(qs) < 5:
            err(f"FAQ が{len(qs)}問（5問以上、推奨7問）")
        else:
            ok(f"FAQ {len(qs)}問")
        for h, text in qs:
            if not re.search(r"([？?]|ください)$", h):
                warn(f"FAQ見出しが疑問形でない: {h}")
            if not text:
                err(f"FAQ に回答がない: {h}")
                continue
            s = first_sentence(text)
            if len(s) > 80:
                warn(f"FAQ回答の一文目が長い（{len(s)}字）: {h}")

    # --- まとめ ---
    if not any(lv == 2 and "まとめ" in h for lv, h, _ in secs):
        warn("「## まとめ」がない")

    # --- 表・リスト ---
    if not re.search(r"^\|.+\|\s*$\n^\|[\s:|-]+\|\s*$", body, re.M):
        warn("表がない（比較・目安・費用は表にするとAIに引用されやすい）")
    else:
        ok("表あり")
    if not re.search(r"^\s*(\d+\.|[-*])\s+", body, re.M):
        warn("箇条書き・番号リストがない")

    # --- リンク ---
    links = re.findall(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)", body)
    internal = [u for _, u in links if u.startswith("/") or "hikitsugi.jp" in u]
    external = [u for _, u in links if u.startswith("http") and "hikitsugi.jp" not in u]
    if len(internal) < 3:
        err(f"内部リンクが{len(internal)}本（3本以上。ピラー・関連記事・サービス導線）")
    else:
        ok(f"内部リンク {len(internal)}本")
    if len(external) < 2:
        err(f"外部リンク（出典）が{len(external)}本。数値には一次情報の出典を付ける")
    else:
        ok(f"外部リンク {len(external)}本")
    if "ai-bpo.site" in body:
        err("旧ドメイン ai-bpo.site へのリンクがある")
    vague = [t for t, _ in links if t.strip() in ("こちら", "ここ", "このページ", "詳しくはこちら", "リンク")]
    if vague:
        warn(f"アンカーテキストが曖昧: {vague}")

    # --- 数値と出典の近さ ---
    paras = [p for p in re.split(r"\n\s*\n", body) if not p.lstrip().startswith(("#", "|"))]
    unsourced = 0
    for p in paras:
        if re.search(r"\d+(\.\d+)?\s*(%|％|億|兆|万人|社)", p) and "](http" not in p and "出典" not in p:
            unsourced += 1
    if unsourced:
        warn(f"出典リンクのない統計らしき数値を含む段落が{unsourced}個。出典を付けるか自社試算と明記する")

    # --- 鮮度 ---
    if not re.search(r"20\d\d年", body):
        warn("本文に年の記載がない（いつ時点の情報か示す）")

    # --- 画像 ---
    for alt, _ in re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", body):
        if not alt.strip():
            err("alt が空の画像がある")

    # --- 残骸 ---
    for pat in ("要出典", "TODO", "TBD", "XX", "〇〇"):
        if pat in body:
            warn(f"本文に「{pat}」が残っている")

    # --- 分量・読みやすさ ---
    n = len(re.sub(r"\s", "", plain(body)))
    ok(f"本文 約{n:,}字")
    if n < 3000:
        warn("本文が3,000字未満。戦略で決めた推奨文字数と比べる")
    long_paras = [p for p in paras if len(plain(p).replace("\n", "")) > 300]
    if long_paras:
        warn(f"300字を超える段落が{len(long_paras)}個（AIが一部を抜き出しにくい。分ける）")
    sentences = re.split(r"[。！？]", plain(body))
    long_s = [s for s in sentences if len(s.strip()) > 100]
    if long_s:
        warn(f"100字を超える文が{len(long_s)}個")

    # --- 誇張・言い切りすぎ ---
    for pat in ("必ず儲か", "絶対に", "100%", "業界No.1", "最安"):
        if pat in body:
            warn(f"根拠の要る表現「{pat}」がある")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--kw", default="", help="メインキーワード（スペース区切りなら先頭語で判定）")
    a = ap.parse_args()
    check(a.path, a.kw.strip())
    for level in ("ERROR", "WARN", "OK"):
        for lv, msg in results:
            if lv == level:
                mark = {"ERROR": "❌", "WARN": "⚠️ ", "OK": "✅"}[lv]
                print(f"{mark} {msg}")
    errors = sum(1 for lv, _ in results if lv == "ERROR")
    warns = sum(1 for lv, _ in results if lv == "WARN")
    print(f"\nERROR {errors} / WARN {warns}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
