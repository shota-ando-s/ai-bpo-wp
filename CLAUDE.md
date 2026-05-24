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
```
