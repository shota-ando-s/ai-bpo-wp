# Memory Index — ai-bpo-wp

- [ドメイン移行](project_domain_migration.md) — 本番は hikitsugi.jp。旧 ai-bpo.site は301用に2027年5月まで解約不可、.well-known除外必須。
- [SEOコンテンツ計画](project_content_plan.md) — Phase1〜3の13記事構成、進捗状況・内部リンク設計・執筆ルールを管理
- [画像生成ルール](feedback_post_image_generation.md) — 記事更新時は画像再生成しない。初回投稿のみ、最初の3見出しだけ生成。
- [地図を画像にしない](feedback_no_map_images.md) — 生成AIの地図は形が崩れる。地域ページで地図・輪郭を描かせない。
- [デプロイ前コミット必須](feedback_deploy_commit_first.md) — deploy前に必ずgit commitする。未コミットのままだと変更がサーバーに反映されない。
- [記事slug照合](project_article_slug_matching.md) — post.pyはslugで既存記事を照合。.mdのslugがWP本番値と不一致だと重複ポストを作る。
- [メール送信はSMTP経由](project_mail_smtp.md) — さくらのmail()は外部宛リレー不可。hikitsugi-smtpプラグイン＋wp-config.phpの定数で送る。
- [CF7とcf7-to-zapierの罠](project_cf7_zapier_gotcha.md) — send_mail=0でメール停止、Webhook失敗でmail_failedに塗り替え。設定は_ctz_zapier。
- [地域別AIメディア企画](project_area_ai_media.md) — ◯◯市 AI 等の地域ページ＋補助金DB＋地域パートナー。企画書 docs/area-ai-media-brief.md
- [ブランド名はヒキツギAI](project_brand_name.md) — 旧称オフボードは全面置換済み。架空の事例・実績・提携は書かない。
- [返事は日本語で](feedback_reply_in_japanese.md) — ユーザーへの返事は必ず日本語。英語で返さない。
