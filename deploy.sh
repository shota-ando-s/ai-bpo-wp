#!/bin/bash
# さくらサーバーへのデプロイスクリプト
# 使い方: ./deploy.sh
# 前提: ~/.ssh/config にさくらサーバーの設定済み

set -euo pipefail

SAKURA_HOST="${SAKURA_HOST:-sakura}"          # ~/.ssh/config のホスト名
SAKURA_USER="${SAKURA_USER:-}"                # さくらのユーザー名（未設定時は環境変数から）
REMOTE_REPO="${REMOTE_REPO:-~/repos/ai-bpo-wp}"  # サーバー上のリポジトリパス
WP_CONTENT="${WP_CONTENT:-~/www/wp-content}"      # WordPress の wp-content パス

echo "==> Pushing to GitHub..."
git push origin main

echo "==> Deploying to Sakura server..."
ssh "${SAKURA_HOST}" bash <<EOF
  set -e
  echo "-- git pull"
  cd ${REMOTE_REPO}
  git pull origin main

  echo "-- sync themes"
  rsync -av --delete ${REMOTE_REPO}/themes/ ${WP_CONTENT}/themes/

  echo "-- sync plugins"
  rsync -av --delete ${REMOTE_REPO}/plugins/ ${WP_CONTENT}/plugins/

  echo "Done."
EOF

echo "==> Deploy complete!"
