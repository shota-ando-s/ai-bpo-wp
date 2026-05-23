# ai-bpo-wp

さくらのレンタルサーバー上のWordPressテーマ・プラグインをGitで管理するリポジトリ。

## ディレクトリ構成

```
ai-bpo-wp/               ← このリポジトリ（wp-content相当）
├── themes/
│   └── your-theme/      ← カスタムテーマ
├── plugins/
│   └── your-plugin/     ← カスタムプラグイン
└── deploy.sh            ← デプロイスクリプト
```

## 初回セットアップ（サーバー側）

### 1. さくらサーバーにSSH接続

```bash
ssh ユーザー名@ドメイン名
```

### 2. GitHubからクローン

```bash
mkdir -p ~/repos
cd ~/repos
git clone https://github.com/YOUR_ORG/ai-bpo-wp.git
```

または SSH クローンの場合（推奨）:

```bash
git clone git@github.com:YOUR_ORG/ai-bpo-wp.git
```

> さくらでGitHub SSH接続する場合は `~/.ssh/config` に GitHub の設定が必要です。

### 3. wp-content へシンボリックリンクを作成（初回のみ）

```bash
# テーマ
ln -s ~/repos/ai-bpo-wp/themes/your-theme ~/www/wp-content/themes/your-theme

# プラグイン
ln -s ~/repos/ai-bpo-wp/plugins/your-plugin ~/www/wp-content/plugins/your-plugin
```

または `deploy.sh` でrsync（シンボリックリンク不要）。

## デプロイ手順

### ローカルで開発 → GitHubにpush

```bash
git add .
git commit -m "feat: ..."
git push origin main
```

### サーバーでpull（手動）

```bash
ssh sakura
cd ~/repos/ai-bpo-wp
git pull origin main
```

### deploy.sh で一括実行

```bash
# ~/.ssh/config に `Host sakura` の設定が必要
./deploy.sh
```

## ~/.ssh/config の設定例

```
Host sakura
  HostName YOUR_DOMAIN.sakura.ne.jp
  User YOUR_USERNAME
  IdentityFile ~/.ssh/id_rsa_sakura
  Port 22
```

## よく使うコマンド

```bash
# テーマを追加（既存テーマをコピーして開始）
cp -r /path/to/existing-theme themes/new-theme

# プラグインを追加
cp -r /path/to/existing-plugin plugins/new-plugin

# 変更を確認
git diff

# コミット
git add themes/your-theme/
git commit -m "style: ヘッダーデザイン修正"
```
