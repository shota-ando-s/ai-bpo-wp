# ai-bpo-wp プロジェクト

さくらのレンタルサーバー上のWordPressテーマ・プラグインをGitで管理するリポジトリ。

## デプロイ

「デプロイして」「デプロイ」「deploy」と言われたら、以下を実行する：

```bash
./deploy.sh
```

このスクリプトは以下を行う：
1. `git push origin main` でGitHubへpush
2. さくらサーバーで `git pull` して即時反映

## サーバー情報

- SSH接続: `ssh sakura`
- サーバー: www3365.sakura.ne.jp
- ユーザー: dx-wizout-coding
- WordPressパス: `~/www/aibpo/wp-content/`
- リポジトリパス: `~/repos/ai-bpo-wp/`

## ディレクトリ構成

```
themes/generatepress/   → ~/www/aibpo/wp-content/themes/generatepress (symlink)
plugins/*/              → ~/www/aibpo/wp-content/plugins/* (symlink)
articles/               → WordPressへの投稿記事（Markdown形式）
```

## 記事の自動投稿

「〇〇について記事を書いて投稿して」と言われたら：

1. `articles/YYYY-MM-DD-slug.md` を作成（YAMLフロントマター付き）
2. 記事内容をMarkdownで記述
3. 以下を実行して投稿：

```bash
python3 post.py articles/ファイル名.md
```

### 記事ファイルの形式

```markdown
---
title: 記事タイトル
categories: [カテゴリ名]
tags: [タグ1, タグ2]
status: publish
excerpt: 記事の要約（120字前後）。記事冒頭の内容をもとに、読者が「自分に関係ある」と判断できるよう、課題・解決策・本記事で得られる情報を簡潔に伝える。
---

本文（Markdown形式）
```

**`excerpt`は必須項目。** 記事作成時に必ず含めること。120字前後で、記事冒頭の2〜3段落を要約し、読者の検索意図に応える形で書く。

### 画像生成ルール：地図は絶対禁止

画像生成AIに地図を描かせることは絶対に禁止。生成AIは県・市町村・海岸線の形を正しく描けず、変な形の地図になる。

- `post.py` の `dalle_generate` は、地名を取り除いてからプロンプトに渡し、生成した画像をビジョンモデルで判定する。地図が入っていれば作り直し、3回作っても地図なら画像を入れない。この仕組みを外したり弱めたりしない
- 画像のプロンプトに地名・地図・地形・輪郭・位置を示すピンを入れない
- 地域を示したいときは、表やリストで書く
- 公開済みページに地図の画像が残っていたら `python3 scripts/fix_map_images.py --apply <記事.md>` で作り直し、作り直した画像は目でも確かめる

### 初回セットアップ（.envファイル）

`.env` ファイルが必要。WordPressの「ユーザー → プロフィール → アプリケーションパスワード」で発行：

```
WP_URL=http://hikitsugi.jp
WP_USER=ユーザー名
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```
