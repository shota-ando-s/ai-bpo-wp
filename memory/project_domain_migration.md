---
name: project-domain-migration
description: 本番は kantan-ai.jp（2026-11-08に hikitsugi.jp から移行、その前は ai-bpo.site）。旧2ドメインは301用に解約不可、.well-known除外必須。メールの差出人は未移行。
metadata:
  type: project
---

本番ドメインは **kantan-ai.jp**（ブランド名「かんたんAI」、[[brand-name-kantan-ai]]）。経緯:
- 2026-07-26 `ai-bpo.site` → `hikitsugi.jp`
- 2026-11-08 `hikitsugi.jp` → `kantan-ai.jp`（ユーザーの指示。kantan-ai.jp は 2026-11-07 にさくらで取得）

どちらも、さくらの同じサーバー・同じフォルダ `~/www/aibpo` のままドメインを付け替えた。パーマリンク `/%postname%/` は変えていないので、パスは1対1で対応する。

**切り替えのやり方**（2026-11-08）: `scripts/cutover_kantan.sh` を `MAIL=0` で実行した。
- データベースは `wp search-replace` で置き換えた（ヒキツギAI 1,932箇所、https://hikitsugi.jp 29,825箇所など）。
- リポジトリは `scripts/rebrand_kantan.py` で置き換えた。
- 置き換える前のバックアップは `~/backups/pre-kantan-202611081007.sql.gz`、`.htaccess.pre-kantan-*`、`wp-config.php.pre-kantan-*`。
- 変えなかったもの: ページの URL のパス（/hikitsugi-ai-bpo-step/ など）、プラグインやコードの内部名（hikitsugi-smtp・HIKITSUGI_SMTP_* など）、checklist.hikitsugi.jp（別サーバーの別サービス）、Site Kit の Search Console 設定。

**旧ドメインは解約しないこと。**
- 301 の転送: `~/www/aibpo/.htaccess` の先頭（`# BEGIN DOMAIN MIGRATION` ブロック、WordPress のマーカーの外）で、ai-bpo.site・hikitsugi.jp（www つきも）を **直接** https://kantan-ai.jp/ にパスを保ったまま301で転送している。転送を2段にしない。
- 解約できない期間: ai-bpo.site は最低 2027-05-23 の更新を通す。hikitsugi.jp も最低1年（2027-11まで）は残す。
- 転送の除外条件は消さない。
  - `.well-known/` を除外しないと、Let's Encrypt の HTTP-01 チャレンジまで転送されて旧ドメインの証明書の更新が失敗し、HTTPS での301ごと止まる。
  - `google*.html` は、旧ドメインの Search Console の所有権の確認に使う（アドレス変更に必要）。
- www.kantan-ai.jp は、さくら側（nginx）が 302 で kantan-ai.jp へ転送している（.htaccess より手前）。

**切り替え時点で残っていたこと**（2026-11-08）:
- メールの差出人はまだ `noreply@send.hikitsugi.jp`。Resend で send.kantan-ai.jp を登録して Verified になってから、wp-config.php の `HIKITSUGI_SMTP_FROM` と FROM_NAME を変える（[[project_mail_smtp]]）。
- Search Console のアドレス変更（hikitsugi.jp → kantan-ai.jp）、Site Kit の接続し直し、GA4 のデータストリームの URL はユーザーが行う。
- LP のスクリーンショット画像（images/hikitsugi-lp*.jpg）には「ヒキツギAI」の文字が残っている。

**Why:** ユーザーがブランドを「かんたんAI」に変えると決めた。

**How to apply:**
- 内部リンク・`.env` の `WP_URL` は `https://kantan-ai.jp`。[[project-article-slug-matching]] のスラッグの照合もこのドメインが前提。
- `.htaccess` の転送ブロックを触るときは、上の除外条件を残す。
