#!/bin/bash
# 書き終えた千葉の記事を area-chiba-wip ブランチに退避（main の index は触らない）
set -e
cd /home/user/ai-bpo-wp
export GIT_INDEX_FILE=$(mktemp -u /tmp/claude-0/-home-user-ai-bpo-wp/9507660a-04b8-5d4c-b4ee-ec094c45776e/scratchpad/idx.XXXX)
git fetch -q origin area-chiba-wip 2>/dev/null && BASE=origin/area-chiba-wip || BASE=HEAD
git read-tree $BASE
for f in "$@"; do git update-index --add "$f"; done
T=$(git write-tree)
C=$(git commit-tree $T -p $(git rev-parse $BASE) -m "wip(area): 千葉県の記事の退避 $*")
git push -q origin $C:refs/heads/area-chiba-wip
rm -f $GIT_INDEX_FILE
echo pushed $C
