#!/bin/bash
# 書き終えた埼玉の記事を area-saitama-wip ブランチに退避する（main には入れない）
set -e
cd /home/user/ai-bpo-wp
export GIT_INDEX_FILE=/tmp/claude-0/-home-user-ai-bpo-wp/8953cae9-d2a2-5ca8-b543-cb8f9f38aaab/scratchpad/wip.index
git fetch -q origin area-saitama-wip 2>/dev/null && PARENT=$(git rev-parse FETCH_HEAD) || PARENT=""
git read-tree $(git rev-parse origin/main^{tree})
git add -f articles/2026-11-12-area-saitama*.md
TREE=$(git write-tree)
if [ -n "$PARENT" ]; then C=$(git commit-tree $TREE -p $PARENT -m "wip(area): 埼玉県の書き終えた記事の退避"); else C=$(git commit-tree $TREE -m "wip(area): 埼玉県の書き終えた記事の退避"); fi
git push -q origin $C:refs/heads/area-saitama-wip
echo "pushed $C"
