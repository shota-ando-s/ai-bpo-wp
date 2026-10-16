#!/usr/bin/env python3
"""公開済みページの見出し画像のうち、地図が描かれたものを探して作り直す。

生成AIは実在の地形や行政区域の形を正しく描けず、地域ページで形の崩れた地図になる。
画像を1枚ずつビジョンモデルで判定し、地図が入ったものだけを post.py の（地図を禁止した）
プロンプトで作り直して差し替える。地図でない画像はそのまま残す。

使い方:
    python3 scripts/fix_map_images.py articles/2026-10-17-area-ehime*.md            # 判定だけ
    python3 scripts/fix_map_images.py --apply articles/2026-10-17-area-ehime*.md    # 作り直して差し替え
    python3 scripts/fix_map_images.py --apply --src <画像URL> articles/<記事>.md      # 判定で漏れた画像を指定して作り直す

判定は見落としがある（薄い輪郭だけの地図など）。作り直した後は、画像を一覧にして目でも確かめる。

.env の OPENAI_API_KEY と WP_USER / WP_APP_PASSWORD を使う。
"""
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import post  # noqa: E402

FIGURE = re.compile(
    r'<figure class="wp-block-image[^"]*\b(?:h2-section-image|intro-image)\b[^"]*">\s*'
    r'<img src="([^"]+)" alt="([^"]*)"')
QUESTION = (
    "Does this image contain a map of any kind: a map, a coastline, an island or landmass shape, "
    "terrain seen from above, or the outline of a country, prefecture, city or region? "
    "Answer with exactly one word: YES or NO."
)


def has_map(image_url):
    body = json.dumps({
        "model": "gpt-4o-mini",
        "max_tokens": 3,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": QUESTION},
            {"type": "image_url", "image_url": {"url": image_url, "detail": "high"}},
        ]}],
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions", data=body, method="POST",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        answer = json.loads(r.read())["choices"][0]["message"]["content"]
    return answer.strip().upper().startswith("YES")


def fix_page(filepath, apply, forced=()):
    meta, _ = post.parse_frontmatter(open(filepath, encoding="utf-8").read())
    endpoint, existing, _ = post.find_existing(meta)
    if not existing:
        print(f"ページが見つかりません: {filepath}", file=sys.stderr)
        return 0
    page = post.api(f"{endpoint}/{existing['id']}?context=edit")
    raw = page["content"]["raw"]
    title = meta.get("title", "")
    found = 0
    for src, alt in FIGURE.findall(raw):
        if src not in forced and not has_map(src):
            continue
        found += 1
        print(f"  地図あり: {alt or '(見出しなし)'}  {src}")
        if not apply:
            continue
        image = post.dalle_generate(alt or title, title)
        if not image:
            print("  作り直しに失敗。元の画像を残します", file=sys.stderr)
            continue
        new_src = post.upload_image_to_wp(image, os.path.basename(src).rsplit(".", 1)[0] + "-v2.png", alt)
        if not new_src:
            continue
        # 作り直した画像も地図になっていないか確かめてから差し替える
        if has_map(new_src):
            print("  作り直した画像にも地図が入ったため、元の画像を残します", file=sys.stderr)
            continue
        raw = raw.replace(f'src="{src}"', f'src="{new_src}"')
        print(f"  差し替え: {new_src}")
    if apply and found:
        post.api(f"{endpoint}/{existing['id']}", method="POST", data={"content": raw})
    return found


def main():
    args = sys.argv[1:]
    apply = "--apply" in args
    forced = [args[i + 1] for i, a in enumerate(args) if a == "--src"]
    files = [a for i, a in enumerate(args) if a.endswith(".md") and (i == 0 or args[i - 1] != "--src")]
    if not files:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    post.load_env()
    total = 0
    for f in files:
        print(f"=== {f}")
        total += fix_page(f, apply, forced)
    print(f"地図の入った画像: {total}枚" + ("（作り直し済み）" if apply else "（判定のみ）"))


if __name__ == "__main__":
    main()
