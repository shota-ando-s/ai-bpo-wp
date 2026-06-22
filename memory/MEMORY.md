# Memory Index — ai-bpo-wp

- [SEOコンテンツ計画](project_content_plan.md) — Phase1〜3の13記事構成、進捗状況・内部リンク設計・執筆ルールを管理
- [画像生成ルール](feedback_post_image_generation.md) — 記事更新時は画像再生成しない。初回投稿のみ生成。
- [デプロイ前コミット必須](feedback_deploy_commit_first.md) — deploy前に必ずgit commitする。未コミットのままだと変更がサーバーに反映されない。
- [記事slug照合](project_article_slug_matching.md) — post.pyはslugで既存記事を照合。.mdのslugがWP本番値と不一致だと重複ポストを作る。
