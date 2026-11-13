# Memory Index — ai-bpo-wp

- [ドメイン移行](project_domain_migration.md) — 本番は kantan-ai.jp（2026-11-08移行）。旧 hikitsugi.jp・ai-bpo.site は直接301用に解約不可、.well-known除外必須。メール差出人は未移行。
- [SEOコンテンツ計画](project_content_plan.md) — Phase1〜3の13記事構成、進捗状況・内部リンク設計・執筆ルールを管理
- [画像生成ルール](feedback_post_image_generation.md) — 記事更新時は画像再生成しない。初回投稿のみ、最初の3見出しだけ生成。
- [地図を画像にしない](feedback_no_map_images.md) — 生成AIの地図は形が崩れる。地域ページで地図・輪郭を描かせない。
- [デプロイ前コミット必須](feedback_deploy_commit_first.md) — deploy前に必ずgit commitする。未コミットのままだと変更がサーバーに反映されない。
- [記事slug照合](project_article_slug_matching.md) — post.pyはslugで既存記事を照合。.mdのslugがWP本番値と不一致だと重複ポストを作る。
- [メール送信はSMTP経由](project_mail_smtp.md) — さくらのmail()は外部宛リレー不可。hikitsugi-smtpプラグイン＋wp-config.phpの定数で送る。
- [CF7とcf7-to-zapierの罠](project_cf7_zapier_gotcha.md) — send_mail=0でメール停止、Webhook失敗でmail_failedに塗り替え。設定は_ctz_zapier。
- [地域別AIメディア企画](project_area_ai_media.md) — 2026-11-13に3a03059まで投稿済み（北海道124・愛知・千葉・兵庫・静岡・神奈川・三重・京都の401ページを新規公開）。その後に作った北海道の宗谷・留萌（179市町村そろう）と埼玉県（63市町村）は投稿待ち。OpenAIのクレジット切れで画像なしで公開→scripts/add_missing_h2_images.py で後から足す。2026-11-13時点で273ページは済み、千葉の習志野以降など約127ページはまたクレジット切れで画像なし（同じコマンドを再実行すれば残りだけ）。投稿状況は .post_state.json と post_changed.py --dry-run で確認。手順・次の候補・企画書は docs/area-ai-media-brief.md
- [ブランド名はかんたんAI](project_brand_name.md) — 2026-11-08にヒキツギAIから変更。旧称ヒキツギAI・オフボードは使わない。架空の事例・実績・提携は書かない。
- [連載「#ルーティン地獄」](project_routine_jigoku.md) — くり返す業務をだましだまし続ける状態を、業種を特定した場面とAIでのBefore/Afterで書く連載（SNS漫画の記事版、名前は仮）。9つの型。架空の場面は想定例と明記すれば可。まず3本（図鑑・入金消込・工務店の転記）。企画書 docs/routine-jigoku-brief.md
- [返事は日本語で](feedback_reply_in_japanese.md) — ユーザーへの返事は必ず日本語。英語で返さない。
