#!/bin/bash
# 書き終えた東京都の記事を area-tokyo-wip ブランチに退避（main の index は触らない）
set -e
cd /home/user/ai-bpo-wp
export GIT_INDEX_FILE=$(mktemp -u /tmp/claude-0/-home-user-ai-bpo-wp/4a8df5ad-9cda-5b10-a097-5208d477a9b5/scratchpad/idx.XXXX)
git fetch -q origin area-tokyo-wip 2>/dev/null && BASE=origin/area-tokyo-wip || BASE=HEAD
git read-tree $BASE
for f in "$@"; do git update-index --add "$f"; done
T=$(git write-tree)
C=$(git commit-tree $T -p $(git rev-parse $BASE) -m "wip(area): 東京都の記事の退避 $*")
git push -q origin $C:refs/heads/area-tokyo-wip
rm -f $GIT_INDEX_FILE
echo pushed $C
