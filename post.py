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
"""

import sys
import os
import json
import base64
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

def post_article(filepath):
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
    existing = find_post_by_slug(slug) if slug else None
    if existing:
        result = api(f"posts/{existing['id']}", method="POST", data=payload)
        print(f"更新完了: {result['link']}")
    else:
        result = api("posts", method="POST", data=payload)
        print(f"投稿完了: {result['link']}")
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"使い方: python3 {sys.argv[0]} <記事.md>", file=sys.stderr)
        sys.exit(1)
    load_env()
    post_article(sys.argv[1])
