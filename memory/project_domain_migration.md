---
name: project-domain-migration
description: 本番ドメインは hikitsugi.jp（2026-07-26にai-bpo.siteから移行）。旧ドメインは301用に最低2027年5月まで解約不可。
metadata: 
  node_type: memory
  type: project
  originSessionId: 0cce5f9a-7db3-482b-acdd-3f54fac417a1
  modified: 2026-07-26T01:59:21.058Z
---

本番ドメインは **hikitsugi.jp**。2026-07-26 に `ai-bpo.site` から移行した（さくら同一サーバー・同一ドキュメントルート `~/www/aibpo` のままドメインを付け替え。パーマリンクは `/%postname%/` で不変なのでパスは1:1）。

**旧ドメイン ai-bpo.site は解約しないこと。** `~/www/aibpo/.htaccess` の先頭（`# BEGIN DOMAIN MIGRATION` ブロック、WordPressマーカー外）でパス保持の301を返している。SEOの301評価が固まるまで最低1年、**2027-05-23の更新を最低1回は通す**。

この301には `.well-known/` の除外条件が必須。除外しないと Let's Encrypt の HTTP-01 チャレンジが新ドメインへリダイレクトされ、ai-bpo.site の証明書更新が失敗 → HTTPSでの301ごと死ぬ。`.htaccess` を触るときはこの条件を消さないこと。

**Why:** ドメインが2026-05取得と若く、記事群も「引き継ぎ」系にシフト済みだったため、exact-matchの `hikitsugi.jp` へ移すコストが最小のタイミングだった。

**How to apply:** 新規記事の内部リンクは `https://hikitsugi.jp/...` を使う。`.env` の `WP_URL`、[[project-article-slug-matching]] のslug照合もこのドメイン前提。診断ツールを作る場合は `offboard.hikitsugi.jp`（front-page.php の `$offboard_tool_url` に定義済み・未稼働）。
