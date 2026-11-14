#!/bin/bash
# さくらサーバーへのデプロイスクリプト
# 使い方: ./deploy.sh
# 前提: ~/.ssh/config に Host sakura の設定済み

set -euo pipefail

SAKURA_HOST="${SAKURA_HOST:-sakura}"
REMOTE_REPO="~/repos/ai-bpo-wp"

echo "==> Pushing to GitHub..."
git push origin main

echo "==> Deploying to Sakura server (git pull)..."
ssh "${SAKURA_HOST}" "cd ${REMOTE_REPO} && git pull origin main"

echo "==> Deploy complete!"
