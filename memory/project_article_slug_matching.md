---
name: project_article_slug_matching
description: post.pyはslugで既存記事を照合。.mdのslugがWP本番値と不一致だと重複ポストを作る
metadata: 
  node_type: memory
  type: project
  originSessionId: bdbde84c-a8d6-4d22-91e7-e9e8741316f0
---

`post.py` は frontmatter の `slug` で `find_post_by_slug` を実行し、一致した記事を更新（upsert）する。**`.md` の slug が WordPress 本番の実スラッグと一致していないと、既存記事を見つけられず新規ポストを作成し、重複が発生する**（さらに新規扱いで画像も再生成される → [[feedback_post_image_generation]] のルールが効かなくなる）。

AI-BPO導入支援シリーズ9記事の本番slugは `hikitsugi-ai-bpo-roadmap` / `hikitsugi-ai-bpo-step1`〜`step8`（ファイル名は `2026-05-28-hikitsugi-ai-*` だが、roadmap↔support-hub のように名称がズレている点に注意）。

**How to apply:** 既存記事をリライト・再投稿する前に、`.md` の slug が WP の公開URLと一致するか必ず確認する。一致しなければ slug を本番値に直してから `post.py` を実行する。`merge_sections` はテキスト変更のあったH2セクションを画像なしの新HTMLで差し替えるため、更新時はブランド名変更などで該当セクションの画像が消える点も留意。
