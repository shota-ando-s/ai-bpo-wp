#!/bin/bash
# 書き終えた大阪府の記事を area-osaka-wip ブランチに退避する（main には入れない）
set -e
cd /home/user/ai-bpo-wp
export GIT_INDEX_FILE=/tmp/claude-0/-home-user-ai-bpo-wp/6d5460e2-6805-52c7-b309-7510874d64b2/scratchpad/wip.index
git fetch -q origin area-osaka-wip 2>/dev/null && PARENT=$(git rev-parse FETCH_HEAD) || PARENT=""
git fetch -q origin main
git read-tree $(git rev-parse origin/main^{tree})
git add -f articles/2026-11-14-area-osaka*.md
TREE=$(git write-tree)
if [ -n "$PARENT" ]; then C=$(git commit-tree $TREE -p $PARENT -m "wip(area): 大阪府の書き終えた記事の退避"); else C=$(git commit-tree $TREE -m "wip(area): 大阪府の書き終えた記事の退避"); fi
git push -q origin $C:refs/heads/area-osaka-wip
echo "pushed $C"
