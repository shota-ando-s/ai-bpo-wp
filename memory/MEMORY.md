# Memory Index — ai-bpo-wp

- [ドメイン移行](project_domain_migration.md) — 本番は hikitsugi.jp。旧 ai-bpo.site は301用に2027年5月まで解約不可、.well-known除外必須。
- [SEOコンテンツ計画](project_content_plan.md) — Phase1〜3の13記事構成、進捗状況・内部リンク設計・執筆ルールを管理
- [画像生成ルール](feedback_post_image_generation.md) — 記事更新時は画像再生成しない。初回投稿のみ生成。
- [デプロイ前コミット必須](feedback_deploy_commit_first.md) — deploy前に必ずgit commitする。未コミットのままだと変更がサーバーに反映されない。
- [記事slug照合](project_article_slug_matching.md) — post.pyはslugで既存記事を照合。.mdのslugがWP本番値と不一致だと重複ポストを作る。
- [メール送信はSMTP経由](project_mail_smtp.md) — さくらのmail()は外部宛リレー不可。hikitsugi-smtpプラグイン＋wp-config.phpの定数で送る。
