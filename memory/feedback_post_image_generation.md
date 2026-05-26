---
name: feedback-post-image-generation
description: post.pyで記事を更新するとき画像を再生成しない
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e555af58-4239-44a5-946f-61f1af8a762a
---

記事の編集・更新時は画像を再生成しない。初回投稿（新規作成）のみ画像生成を行う。

画像生成中にAPIタイムアウトが発生してスキップされた場合は、ユーザーに報告せず無視する。

**Why:** 既存記事を更新するたびに画像を再生成するとコストがかかり、意図しない画像の差し替えが起きる。タイムアウトは都度報告不要とのこと。

**How to apply:** post.pyでスラッグが既存記事と一致する場合（upsert時）はDALL-E画像生成をスキップする。`--excerpt-only`フラグを使えば抜粋だけ更新できる。タイムアウトによるスキップはユーザーに伝えない。
