#!/bin/bash
# ヒキツギAI（hikitsugi.jp）→ かんたんAI（kantan-ai.jp）への本番の切り替え。
#
# 前提（さくら・Resend の管理画面で済ませておく）:
#   - kantan-ai.jp と www.kantan-ai.jp をサーバーに追加し、フォルダは /www/aibpo
#   - 両方に無料SSL（Let's Encrypt）
#   - メールも移すなら、Resend で send.kantan-ai.jp を Verified にしておく（まだなら MAIL=0）
#
# 使い方:
#   ./scripts/cutover_kantan.sh            # 確認 → バックアップ → リポジトリ → DB → .htaccess → メール
#   MAIL=0 ./scripts/cutover_kantan.sh     # メールの差出人は変えない
#
# 戻すとき: ~/backups/pre-kantan-*.sql.gz を wp db import、.htaccess.pre-kantan・wp-config.php.pre-kantan を戻す
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

MAIL="${MAIL:-1}"
REMOTE_WP="~/www/aibpo"
STAMP="$(date +%Y%m%d%H%M)"

echo "==> 1. 確認"
git pull --ff-only origin main
if [ -n "$(git status --porcelain -- articles themes plugins data scripts post.py)" ]; then
  echo "コミットしていない変更があります。先にコミットしてください" >&2; exit 1
fi
# kantan-ai.jp がこのサーバーに届き、証明書が正しいこと（いまは WordPress が hikitsugi.jp へ転送する）
out="$(curl -sS -o /dev/null -m 20 -w '%{http_code} %{redirect_url}' https://kantan-ai.jp/ || true)"
echo "    https://kantan-ai.jp/ → $out"
case "$out" in
  "200 "*|"301 https://hikitsugi.jp/"*|"301 https://kantan-ai.jp/"*) ;;
  *) echo "kantan-ai.jp がまだこのサーバーで HTTPS で開けません（DNS・ドメイン追加・SSL を確かめる）" >&2; exit 1 ;;
esac
if [ "$MAIL" = 1 ] && [ -z "$(dig +short TXT resend._domainkey.send.kantan-ai.jp)" ]; then
  echo "send.kantan-ai.jp の DKIM が DNS にありません。Resend の設定を済ませるか MAIL=0 で実行してください" >&2; exit 1
fi

echo "==> 2. サーバーのバックアップ"
ssh sakura "bash -s" <<EOF
set -e
cd $REMOTE_WP
mkdir -p ~/backups
wp db export - | gzip > ~/backups/pre-kantan-$STAMP.sql.gz
cp -p .htaccess .htaccess.pre-kantan-$STAMP
cp -p wp-config.php wp-config.php.pre-kantan-$STAMP
ls -la ~/backups/pre-kantan-$STAMP.sql.gz
EOF

echo "==> 3. リポジトリの置き換え・コミット・デプロイ"
python3 scripts/rebrand_kantan.py
sed -i '' 's#/images/hikitsugi_logo.png#/images/kantan_logo.png#' themes/generatepress-child/functions.php
sed -i '' 's#^WP_URL=.*#WP_URL=https://kantan-ai.jp#' .env
python3 scripts/build_shindan_data.py
git add -A articles themes plugins data docs scripts post.py CLAUDE.md memory .claude/skills tools
git commit -q -m "chore(brand): ヒキツギAI（hikitsugi.jp）→ かんたんAI（kantan-ai.jp）

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
./deploy.sh

echo "==> 4. データベースの置き換え"
ssh sakura "bash -s" <<'EOF'
set -e
cd ~/www/aibpo
sr() { wp search-replace "$1" "$2" --all-tables-with-prefix --skip-columns=guid --report-changed-only; }
sr 'ヒキツギAI' 'かんたんAI'
sr 'https://www.hikitsugi.jp' 'https://kantan-ai.jp'
sr 'https://hikitsugi.jp' 'https://kantan-ai.jp'
sr 'http://www.hikitsugi.jp' 'https://kantan-ai.jp'
sr 'http://hikitsugi.jp' 'https://kantan-ai.jp'
sr 'https:\/\/hikitsugi.jp' 'https:\/\/kantan-ai.jp'
sr 'http:\/\/hikitsugi.jp' 'https:\/\/kantan-ai.jp'
sr '//hikitsugi.jp' '//kantan-ai.jp'
sr '@hikitsugi.jp' '@kantan-ai.jp'
sr 'send.hikitsugi.jp' 'send.kantan-ai.jp'
sr 'offboard.hikitsugi.jp' 'offboard.kantan-ai.jp'
wp cache flush
echo "home: $(wp option get home) / siteurl: $(wp option get siteurl) / blogname: $(wp option get blogname)"
EOF

echo "==> 5. .htaccess（ai-bpo.site・hikitsugi.jp・www.kantan-ai.jp → kantan-ai.jp）"
ssh sakura "bash -s" <<'EOF'
set -e
cd ~/www/aibpo
python3 - <<'PY'
import re
p = ".htaccess"
s = open(p, encoding="utf-8").read()
block = """# BEGIN DOMAIN MIGRATION (ai-bpo.site, hikitsugi.jp -> kantan-ai.jp) 2026-11
# 注意: .well-known は Let's Encrypt 更新のため除外すること。google*.html は旧ドメインの Search Console の確認用
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{HTTP_HOST} ^(www\\.)?(ai-bpo\\.site|hikitsugi\\.jp)$ [NC,OR]
RewriteCond %{HTTP_HOST} ^www\\.kantan-ai\\.jp$ [NC]
RewriteCond %{REQUEST_URI} !^/\\.well-known/ [NC]
RewriteCond %{REQUEST_URI} !^/google[0-9a-z]+\\.html$ [NC]
RewriteRule ^(.*)$ https://kantan-ai.jp/$1 [R=301,L]
</IfModule>
# END DOMAIN MIGRATION"""
new, n = re.subn(r"# BEGIN DOMAIN MIGRATION.*?# END DOMAIN MIGRATION", lambda m: block, s, flags=re.S)
assert n == 1, "DOMAIN MIGRATION のブロックが見つからない"
open(p, "w", encoding="utf-8").write(new)
PY
sed -n '/BEGIN DOMAIN MIGRATION/,/END DOMAIN MIGRATION/p' .htaccess
EOF

if [ "$MAIL" = 1 ]; then
  echo "==> 6. メールの差出人"
  ssh sakura "bash -s" <<'EOF'
set -e
cd ~/www/aibpo
perl -CSD -Mutf8 -pi -e "s#'noreply\@send\.hikitsugi\.jp'#'noreply\@send.kantan-ai.jp'#; s#ヒキツギAI#かんたんAI#g" wp-config.php
grep -n "HIKITSUGI_SMTP_FROM" wp-config.php
php -l wp-config.php
EOF
fi

echo "==> 7. 投稿の記録を今のコミットにそろえる"
python3 scripts/post_changed.py --init HEAD

echo "==> 8. 確かめる"
for u in https://kantan-ai.jp/ https://www.kantan-ai.jp/area/ https://hikitsugi.jp/area/ http://hikitsugi.jp/ https://ai-bpo.site/area/ https://hikitsugi.jp/.well-known/acme-challenge/x; do
  printf '%-50s %s\n' "$u" "$(curl -sS -o /dev/null -m 20 -w '%{http_code} %{redirect_url}' "$u" || echo NG)"
done
ssh sakura "bash -s" <<'EOF' || true
cd ~/www/aibpo
P=$(wp db prefix)
echo "hikitsugi.jp・ヒキツギが残っている投稿・ページ:"
wp db query "SELECT ID, post_title FROM ${P}posts WHERE post_status IN ('publish','draft','private') AND (post_content LIKE '%hikitsugi.jp%' OR post_content LIKE '%ヒキツギ%')" --skip-column-names
EOF
echo "（残りは checklist.hikitsugi.jp へのリンクなら正常）"
