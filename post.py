#!/usr/bin/env python3
"""WordPress記事自動投稿スクリプト

使い方:
    python3 post.py articles/記事ファイル.md

記事ファイルはYAMLフロントマター付きMarkdown形式:
    ---
    title: 記事タイトル
    categories: [カテゴリ名]
    tags: [タグ1, タグ2]
    status: publish  # または draft
    ---
    本文...

.envにOPENAI_API_KEYを設定するとH2ごとにDALL-E 3で画像を自動生成・挿入します。
"""

import sys
import os
import io
import json
import base64
import re
import urllib.request
import urllib.error
import urllib.parse

try:
    import yaml
except ImportError:
    print("Error: pip3 install PyYAML", file=sys.stderr)
    sys.exit(1)

try:
    import markdown as md_lib
except ImportError:
    print("Error: pip3 install markdown", file=sys.stderr)
    sys.exit(1)

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

def auth_header():
    user = os.environ.get("WP_USER", "")
    password = os.environ.get("WP_APP_PASSWORD", "")
    if not user or not password:
        print("Error: .env に WP_USER と WP_APP_PASSWORD を設定してください", file=sys.stderr)
        sys.exit(1)
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

def api(endpoint, method="GET", data=None):
    base = os.environ.get("WP_URL", "http://ai-bpo.site").rstrip("/")
    url = f"{base}/wp-json/wp/v2/{endpoint}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=auth_header(), method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"API Error {e.code}: {e.read().decode()}", file=sys.stderr)
        raise

def get_or_create_term(taxonomy, name):
    results = api(f"{taxonomy}?search={urllib.parse.quote(name)}&per_page=100")
    for term in results:
        if term["name"] == name:
            return term["id"]
    new_term = api(taxonomy, method="POST", data={"name": name})
    return new_term["id"]

def parse_frontmatter(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1]) or {}, parts[2].strip()
    return {}, text.strip()

def find_post_by_slug(slug):
    results = api(f"posts?slug={urllib.parse.quote(slug)}&status=any&per_page=1")
    return results[0] if results else None

def dalle_generate(heading, article_title):
    """gpt-image-1でH2テーマに合ったビジネス画像を生成し、画像バイトを返す"""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return None
    prompt = (
        f"A clean, professional illustration for a Japanese business blog article titled '{article_title}'. "
        f"Section theme: '{heading}'. "
        "Wide landscape format, modern flat design style, no text, no letters, no words anywhere in the image. "
        "Use soft business colors (blue, white, light gray). High quality, visually appealing."
    )
    body = json.dumps({
        "model": "gpt-image-1",
        "prompt": prompt,
        "n": 1,
        "size": "1536x1024",
        "quality": "medium",
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        b64 = data["data"][0].get("b64_json") or data["data"][0].get("url")
        if data["data"][0].get("b64_json"):
            return base64.b64decode(b64)
        # url形式の場合はダウンロード
        with urllib.request.urlopen(b64) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"画像生成エラー ({heading}): {e.code} {err_body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"画像生成エラー ({heading}): {e}", file=sys.stderr)
        return None

def upload_image_to_wp(image_bytes, filename, alt_text=""):
    """画像バイトをWordPressメディアライブラリにアップロードしてURLを返す"""
    base = os.environ.get("WP_URL", "http://ai-bpo.site").rstrip("/")
    upload_url = f"{base}/wp-json/wp/v2/media"

    headers = auth_header()
    headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    headers["Content-Type"] = "image/png"

    req = urllib.request.Request(upload_url, data=image_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            result = json.loads(r.read())
        return result.get("source_url")
    except urllib.error.HTTPError as e:
        print(f"WPアップロードエラー {e.code}: {e.read().decode()}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"WPアップロードエラー: {e}", file=sys.stderr)
        return None

def insert_h2_images(html, h2_texts, article_title):
    """H2タグの直前にDALL-E 3生成画像を挿入する"""
    if not h2_texts:
        return html

    for i, heading_text in enumerate(h2_texts):
        print(f"  [{i+1}/{len(h2_texts)}] 生成中: {heading_text}")
        image_bytes = dalle_generate(heading_text, article_title)
        if not image_bytes:
            print(f"  スキップ: {heading_text}", file=sys.stderr)
            continue

        ascii_part = re.sub(r"[^\x00-\x7F]", "", heading_text)
        safe_name = re.sub(r"[^\w]", "-", ascii_part).strip("-")[:40] or f"h2-{i}"
        wp_url = upload_image_to_wp(image_bytes, f"{safe_name}.png", heading_text)
        if not wp_url:
            continue

        img_block = (
            f'<figure class="wp-block-image size-large h2-section-image">'
            f'<img src="{wp_url}" alt="{heading_text}" loading="lazy"/>'
            f'</figure>'
        )

        escaped = re.escape(heading_text)
        html = re.sub(
            rf"(<h2[^>]*>)({escaped})(</h2>)",
            lambda m: m.group(0) + img_block,
            html,
            count=1,
        )
        print(f"  完了: {wp_url}")

    return html

def convert_to_blocks(html):
    """HTML を WordPress Gutenberg ブロック形式に変換する"""
    # li → wp:list-item（ul/ol wrapping の前に処理）
    html = re.sub(
        r'<li>(.*?)</li>',
        r'<!-- wp:list-item --><li>\1</li><!-- /wp:list-item -->',
        html, flags=re.DOTALL
    )
    # ul → wp:list
    html = re.sub(
        r'<ul>(.*?)</ul>',
        r'<!-- wp:list --><ul class="wp-block-list">\1</ul><!-- /wp:list -->',
        html, flags=re.DOTALL
    )
    # ol → wp:list ordered
    html = re.sub(
        r'<ol>(.*?)</ol>',
        r'<!-- wp:list {"ordered":true} --><ol class="wp-block-list">\1</ol><!-- /wp:list -->',
        html, flags=re.DOTALL
    )
    # h2 〜 h4 → wp:heading
    for level in [2, 3, 4]:
        html = re.sub(
            rf'<h{level}>(.*?)</h{level}>',
            rf'<!-- wp:heading {{"level":{level}}} --><h{level} class="wp-block-heading">\1</h{level}><!-- /wp:heading -->',
            html, flags=re.DOTALL
        )
    # p → wp:paragraph
    html = re.sub(
        r'<p>(.*?)</p>',
        r'<!-- wp:paragraph --><p>\1</p><!-- /wp:paragraph -->',
        html, flags=re.DOTALL
    )
    # table → wp:table
    html = re.sub(
        r'<table>(.*?)</table>',
        r'<!-- wp:table --><figure class="wp-block-table"><table>\1</table></figure><!-- /wp:table -->',
        html, flags=re.DOTALL
    )
    # wp-block-image figure（画像挿入後に呼ぶこと）→ wp:image
    html = re.sub(
        r'(<figure class="wp-block-image[^"]*">.*?</figure>)',
        r'<!-- wp:image -->\1<!-- /wp:image -->',
        html, flags=re.DOTALL
    )
    return html


def insert_intro_image(html, article_title):
    """記事冒頭（最初の<p>の直前）にDALL-E生成画像を1枚挿入する"""
    image_bytes = dalle_generate(article_title, article_title)
    if not image_bytes:
        print("イントロ画像生成失敗", file=sys.stderr)
        return html

    ascii_part = re.sub(r"[^\x00-\x7F]", "", article_title)
    safe_name = re.sub(r"[^\w]", "-", ascii_part).strip("-")[:40] or "intro"
    wp_url = upload_image_to_wp(image_bytes, f"{safe_name}-intro.png", article_title)
    if not wp_url:
        return html

    img_block = (
        f'<figure class="wp-block-image size-large intro-image">'
        f'<img src="{wp_url}" alt="{article_title}" loading="lazy"/>'
        f'</figure>'
    )
    html = re.sub(r"(<p)", img_block + r"\1", html, count=1)
    print(f"イントロ画像挿入完了: {wp_url}")
    return html


def add_intro_image_to_existing_post(filepath):
    """既存WPコンテンツを取得して冒頭に画像を1枚挿入する（H2画像を保持）"""
    with open(filepath, encoding="utf-8") as f:
        raw = f.read()
    meta, _ = parse_frontmatter(raw)
    slug = meta.get("slug")
    title = meta.get("title") or os.path.splitext(os.path.basename(filepath))[0]

    existing = find_post_by_slug(slug) if slug else None
    if not existing:
        print("既存記事が見つかりません。通常投稿を使ってください。", file=sys.stderr)
        return

    # WPに保存されている現在のHTMLを取得（H2画像込み）
    post_data = api(f"posts/{existing['id']}?context=edit")
    current_html = post_data.get("content", {}).get("raw", "")

    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY が設定されていません", file=sys.stderr)
        return

    print("イントロ画像生成中...")
    current_html = insert_intro_image(current_html, title)

    result = api(f"posts/{existing['id']}", method="POST", data={"content": current_html})
    print(f"更新完了: {result['link']}")


def post_article(filepath, rebuild_images=False):
    with open(filepath, encoding="utf-8") as f:
        raw = f.read()

    meta, body = parse_frontmatter(raw)

    title = meta.get("title") or os.path.splitext(os.path.basename(filepath))[0]
    status = meta.get("status", "publish")
    categories = meta.get("categories") or []
    tags = meta.get("tags") or []
    slug = meta.get("slug")
    excerpt = meta.get("excerpt")

    html = md_lib.markdown(body, extensions=["nl2br", "tables", "fenced_code"])

    existing = find_post_by_slug(slug) if slug else None
    h2_texts = re.findall(r"^## (.+)$", body, re.MULTILINE)
    # 新規投稿 or --rebuild-images 時にH2画像を生成
    if h2_texts and os.environ.get("OPENAI_API_KEY") and (not existing or rebuild_images):
        print(f"H2画像生成中... ({len(h2_texts)}件、1枚あたり約15秒)")
        html = insert_h2_images(html, h2_texts, title)

    if rebuild_images and os.environ.get("OPENAI_API_KEY"):
        print("イントロ画像生成中...")
        html = insert_intro_image(html, title)

    # 新規投稿はブロックエディタ形式で出力（更新時はWP既存コンテンツを使うためスキップ）
    if not existing:
        html = convert_to_blocks(html)

    category_ids = [get_or_create_term("categories", c) for c in categories]
    tag_ids = [get_or_create_term("tags", t) for t in tags]

    payload = {
        "title": title,
        "content": html,
        "status": status,
        "categories": category_ids,
        "tags": tag_ids,
    }
    if slug:
        payload["slug"] = slug
    if excerpt:
        payload["excerpt"] = excerpt

    # slug が既存記事と一致する場合は更新（upsert）
    if existing:
        result = api(f"posts/{existing['id']}", method="POST", data=payload)
        print(f"更新完了: {result['link']}")
    else:
        result = api("posts", method="POST", data=payload)
        print(f"投稿完了: {result['link']}")
    return result

def update_excerpt_only(filepath):
    with open(filepath, encoding="utf-8") as f:
        raw = f.read()
    meta, _ = parse_frontmatter(raw)
    slug = meta.get("slug")
    excerpt = meta.get("excerpt")
    if not excerpt:
        print(f"excerpt が見つかりません: {filepath}", file=sys.stderr)
        return
    existing = find_post_by_slug(slug) if slug else None
    if not existing:
        print(f"記事が見つかりません (slug={slug}): {filepath}", file=sys.stderr)
        return
    result = api(f"posts/{existing['id']}", method="POST", data={"excerpt": excerpt})
    print(f"抜粋更新完了: {result['link']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"使い方: python3 {sys.argv[0]} [--excerpt-only|--add-intro-image] <記事.md>", file=sys.stderr)
        sys.exit(1)
    load_env()
    if sys.argv[1] == "--excerpt-only":
        if len(sys.argv) < 3:
            print(f"使い方: python3 {sys.argv[0]} --excerpt-only <記事.md>", file=sys.stderr)
            sys.exit(1)
        for filepath in sys.argv[2:]:
            update_excerpt_only(filepath)
    elif sys.argv[1] == "--add-intro-image":
        if len(sys.argv) < 3:
            print(f"使い方: python3 {sys.argv[0]} --add-intro-image <記事.md>", file=sys.stderr)
            sys.exit(1)
        for filepath in sys.argv[2:]:
            add_intro_image_to_existing_post(filepath)
    elif sys.argv[1] == "--rebuild-images":
        if len(sys.argv) < 3:
            print(f"使い方: python3 {sys.argv[0]} --rebuild-images <記事.md>", file=sys.stderr)
            sys.exit(1)
        for filepath in sys.argv[2:]:
            post_article(filepath, rebuild_images=True)
    else:
        post_article(sys.argv[1])
