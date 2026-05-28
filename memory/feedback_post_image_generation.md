---
name: feedback-post-image-generation
description: post.pyで記事を更新するとき画像を再生成しない
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e555af58-4239-44a5-946f-61f1af8a762a
---

記事の編集・更新時は画像を再生成しない。初回投稿（新規作成）のみH2ごとに画像生成を行う。この動作をユーザーが「このままでOK」と明示的に承認済み（`--no-images` オプション追加も不要）。

**Why:** 既存記事を更新するたびに画像を再生成するとコストがかかり、意図しない画像の差し替えが起きる。初回のみ生成することで各記事にビジュアルが入り品質が保たれる。

**How to apply:** post.pyでスラッグが既存記事と一致する場合（upsert時）はDALL-E画像生成をスキップする。`--rebuild-images` は明示的に指示された場合のみ使う。`--excerpt-only`フラグを使えば抜粋だけ更新できる。
