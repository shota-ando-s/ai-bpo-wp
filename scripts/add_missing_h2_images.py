#!/usr/bin/env python3
"""見出し画像が1枚もない公開済みページに、最初の3つの H2 の画像を足す。

新しく投稿したときに画像の生成が失敗する（OpenAI のクレジット切れなど）と、ページは画像なしで
公開される。post.py は更新のときに画像を作らないので、このスクリプトで後から足す。
WordPress 側の本文に画像を差し込むだけで、本文の文言は変えない。

- すでに h2-section-image が1枚でもあるページは飛ばす（作り直しはしない）
- 画像は post.dalle_generate で作る（地名を除いたプロンプト＋地図の判定。地図なら作り直し、
  3回とも地図なら入れない）
- 3枚とも作れなかったページは更新しない。次に実行すれば、そのページだけまた試す

使い方:
    python3 scripts/add_missing_h2_images.py --dry-run articles/2026-11-13-area-*.md   # 画像のないページを数えるだけ
    python3 scripts/add_missing_h2_images.py articles/2026-11-13-area-*.md             # 画像を作って足す

.env の OPENAI_API_KEY と WP_USER / WP_APP_PASSWORD を使う。
"""
import html as htmllib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import post  # noqa: E402

H2_BLOCK = re.compile(
    r'(?:<!-- wp:heading \{"level":2\} -->[ \t]*)?<h2[^>]*>(.*?)</h2>(?:[ \t]*<!-- /wp:heading -->)?',
    re.DOTALL,
)


def add_images(filepath, dry_run):
    meta, _ = post.parse_frontmatter(open(filepath, encoding="utf-8").read())
    title = meta.get("title", "")
    endpoint, existing, _ = post.find_existing(meta)
    if not existing:
        print(f"ページが見つかりません: {filepath}", file=sys.stderr)
        return "missing"
    page = post.api(f"{endpoint}/{existing['id']}?context=edit")
    raw = page["content"]["raw"]
    if "h2-section-image" in raw:
        return "has"
    heads = list(H2_BLOCK.finditer(raw))[: post.MAX_H2_IMAGES]
    if dry_run:
        print(f"画像なし: {filepath}（見出し {len(heads)}）")
        return "todo"

    print(f"==> {filepath}")
    inserts = []  # (挿入位置, ブロック)
    for i, m in enumerate(heads):
        alt_html = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        heading = htmllib.unescape(alt_html)
        print(f"  [{i+1}/{len(heads)}] 生成中: {heading}")
        image_bytes = post.dalle_generate(heading, title)
        if not image_bytes:
            print(f"  スキップ: {heading}", file=sys.stderr)
            continue
        ascii_part = re.sub(r"[^\x00-\x7F]", "", heading)
        safe_name = re.sub(r"[^\w]", "-", ascii_part).strip("-")[:40] or f"h2-{i}"
        wp_url = post.upload_image_to_wp(image_bytes, f"{safe_name}.png", heading)
        if not wp_url:
            continue
        alt = alt_html.replace('"', "&quot;")
        block = (
            '<!-- wp:image --><figure class="wp-block-image size-large h2-section-image">'
            f'<img src="{wp_url}" alt="{alt}" loading="lazy"/>'
            "</figure><!-- /wp:image -->"
        )
        inserts.append((m.end(), block))
        print(f"  完了: {wp_url}")

    if not inserts:
        print("  画像を1枚も作れなかったので更新しません", file=sys.stderr)
        return "failed"
    for pos, block in sorted(inserts, reverse=True):
        raw = raw[:pos] + block + raw[pos:]
    result = post.api(f"{endpoint}/{existing['id']}", method="POST", data={"content": raw})
    print(f"  更新完了（{len(inserts)}枚）: {result['link']}")
    return "added" if len(inserts) == len(heads) else "partial"


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    post.load_env()
    if not dry_run and not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY が設定されていません", file=sys.stderr)
        sys.exit(1)
    counts = {}
    for f in files:
        try:
            r = add_images(f, dry_run)
        except Exception as e:  # 1ページの失敗で全体を止めない
            print(f"エラー: {f}: {e}", file=sys.stderr)
            r = "error"
        counts[r] = counts.get(r, 0) + 1
    print("結果:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
