#!/usr/bin/env python3
"""本番WordPressの記事本文で articles/*.md を上書きする（本番 → Markdown の同期）

使い方:
    python3 scripts/sync_articles_from_wp.py            # 差分がある記事を一覧するだけ
    python3 scripts/sync_articles_from_wp.py --write    # 差分がある記事の本文とフロントマターを本番に合わせる

- 画像（<figure> / <img>）はMarkdownに入れない。画像はWordPress側で管理し、
  post.py は本文のテキストが同じセクションをWP側のまま残すので、画像は消えない。
- 書き換えたあと、post.py と同じ方法（H2セクションごとのテキスト比較）で差分が0になることを確かめる。
- 固定ページ（type: page）は対象外。
"""

import argparse
import glob
import html
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import post  # noqa: E402

import markdown as md_lib  # noqa: E402
import yaml  # noqa: E402


class HtmlToMarkdown(HTMLParser):
    """記事で使っているタグだけを扱う、HTML → Markdown 変換"""

    BLOCKS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "table", "blockquote", "pre", "hr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []          # 完成したブロック
        self.buf = []          # 今のインライン文字列
        self.lists = []        # ネストしたリストの種類と番号
        self.table = None      # 表の行
        self.row = None
        self.cell = None
        self.skip = 0          # figure/img/script の中
        self.link = []
        self.pre = False
        self.quote = False
        self.heading = None

    # --- 出力の補助 ---
    def _text(self):
        return "".join(self.buf)

    def _flush(self, prefix=""):
        text = self._text().strip()
        self.buf = []
        if text:
            if self.quote:
                text = "\n".join("> " + line for line in text.split("\n"))
            self.out.append(prefix + text)

    def _inline(self, s):
        if self.cell is not None:
            self.cell.append(s)
        else:
            self.buf.append(s)

    # --- パーサ ---
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.skip:
            if tag in ("figure", "script", "style"):
                self.skip += 1
            return
        if tag in ("script", "style"):
            self.skip = 1
            return
        if tag == "figure":
            # 表を包む figure は中身を出す。画像の figure は捨てる
            if "wp-block-table" not in (a.get("class") or ""):
                self.skip = 1
            return
        if tag == "img":
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush()
            self.heading = int(tag[1])
        elif tag == "p":
            if self.cell is None and not self.lists:
                self._flush()
        elif tag in ("ul", "ol"):
            if not self.lists:
                self._flush()
            else:
                self._flush_list_item()
            self.lists.append([tag, 0])
        elif tag == "li":
            self._flush_list_item()
            self.lists[-1][1] += 1
        elif tag == "table":
            self._flush()
            self.table = []
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []
        elif tag in ("strong", "b"):
            self._inline("**")
        elif tag in ("em", "i"):
            self._inline("*")
        elif tag == "a":
            self.link.append(a.get("href", ""))
            self._inline("[")
        elif tag == "br":
            self._inline("\n" if self.cell is None else " ")
        elif tag == "code" and not self.pre:
            self._inline("`")
        elif tag == "pre":
            self._flush()
            self.pre = True
        elif tag == "blockquote":
            self._flush()
            self.quote = True
        elif tag == "hr":
            self._flush()
            self.out.append("---")

    def handle_endtag(self, tag):
        if self.skip:
            if tag in ("figure", "script", "style"):
                self.skip -= 1
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush("#" * self.heading + " ")
            self.heading = None
        elif tag == "p":
            if self.cell is None and not self.lists:
                self._flush()
        elif tag == "li":
            self._flush_list_item()
        elif tag in ("ul", "ol"):
            self._flush_list_item()
            self.lists.pop()
        elif tag in ("td", "th"):
            text = re.sub(r"\s+", " ", "".join(self.cell)).strip().replace("|", "\\|")
            self.row.append(text)
            self.cell = None
        elif tag == "tr":
            self.table.append(self.row)
            self.row = None
        elif tag == "table":
            rows = [r for r in self.table if r]
            if rows:
                lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * len(rows[0])]
                lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
                self.out.append("\n".join(lines))
            self.table = None
        elif tag in ("strong", "b"):
            self._inline("**")
        elif tag in ("em", "i"):
            self._inline("*")
        elif tag == "a":
            self._inline("](" + self.link.pop() + ")")
        elif tag == "code" and not self.pre:
            self._inline("`")
        elif tag == "pre":
            self.out.append("```\n" + self._text().strip("\n") + "\n```")
            self.buf = []
            self.pre = False
        elif tag == "blockquote":
            self._flush()
            self.quote = False

    def _flush_list_item(self):
        text = self._text().strip()
        self.buf = []
        if not text or not self.lists:
            return
        depth = len(self.lists) - 1
        kind, n = self.lists[-1]
        marker = f"{n}. " if kind == "ol" else "- "
        text = text.replace("\n", "\n" + "    " * (depth + 1))
        self.out.append(("    " * depth) + marker + text)

    def handle_data(self, data):
        if self.skip:
            return
        if self.pre:
            self.buf.append(data)
            return
        if self.cell is None and not self.buf and not data.strip():
            return
        data = re.sub(r"[ \t\r\n]+", " ", data)
        self._inline(data)

    def markdown(self):
        self._flush()
        # 連続するリスト項目は空行を挟まずにつなぐ
        blocks = []
        for b in self.out:
            is_item = bool(re.match(r"^(\s*)(- |\d+\. )", b))
            if blocks and is_item and blocks[-1][1]:
                blocks[-1] = (blocks[-1][0] + "\n" + b, True)
            else:
                blocks.append((b, is_item))
        return "\n\n".join(b for b, _ in blocks).strip() + "\n"


def wp_to_markdown(raw):
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
    parser = HtmlToMarkdown()
    parser.feed(raw)
    parser.close()
    return parser.markdown()


def section_diff(wp_raw, body):
    new = post.convert_to_blocks(md_lib.markdown(body, extensions=["nl2br", "tables", "fenced_code"]))
    wp = dict(post._split_sections(wp_raw))
    return [h or "(冒頭)" for h, c in post._split_sections(new)
            if not (wp.get(h) and post._section_text(wp[h]) == post._section_text(c))]


def term_names(taxonomy, ids):
    return [html.unescape(post.api(f"{taxonomy}/{i}")["name"]) for i in ids]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    post.load_env()

    ok, failed = 0, []
    for path in sorted(glob.glob(os.path.join(ROOT, "articles", "*.md"))):
        text = open(path, encoding="utf-8").read()
        meta, body = post.parse_frontmatter(text)
        if meta.get("type") == "page":
            continue
        p = post.find_post_by_slug(meta.get("slug", ""))
        name = os.path.basename(path)
        if not p:
            print(f"{name}: 本番に記事が見つかりません（slug={meta.get('slug')}）")
            continue
        wp = post.api(f"posts/{p['id']}?context=edit")
        raw = wp["content"]["raw"]
        if not section_diff(raw, body):
            continue
        new_body = wp_to_markdown(raw)
        remain = section_diff(raw, new_body)
        print(f"{name}: 差分あり → 変換後の差分 {len(remain)} {remain if remain else ''}")
        if remain:
            failed.append(name)
            continue
        if args.write:
            meta["title"] = html.unescape(wp["title"]["raw"])
            excerpt = html.unescape(re.sub(r"<[^>]+>", "", wp["excerpt"]["raw"])).strip()
            if excerpt:
                meta["excerpt"] = excerpt
            meta["categories"] = term_names("categories", wp["categories"])
            meta["tags"] = term_names("tags", wp["tags"])
            meta["status"] = wp["status"]
            front = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1000).strip()
            open(path, "w", encoding="utf-8").write(f"---\n{front}\n---\n\n{new_body}")
            ok += 1
    print(f"\n書き換え: {ok}件" if args.write else "")
    if failed:
        print("変換で差分が残った記事（手で直す）:", ", ".join(failed))


if __name__ == "__main__":
    main()
