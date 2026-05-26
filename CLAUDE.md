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

### 初回セットアップ（.envファイル）

`.env` ファイルが必要。WordPressの「ユーザー → プロフィール → アプリケーションパスワード」で発行：

```
WP_URL=http://ai-bpo.site
WP_USER=ユーザー名
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```
