---
name: feedback-article-images
description: 記事投稿時はH2直下にgpt-image-1生成画像を自動挿入する（post.pyで実装済み）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 26f5ddf7-202a-4913-8976-ff23bbe20843
---

記事を投稿・更新するときは必ず `python3 post.py articles/ファイル名.md` を使い、H2ごとにgpt-image-1で生成した画像をH2直下に自動挿入する。

**Why:** ユーザーが各H2セクションに画像を入れたいと要望し、post.pyに実装・確認済み。

**How to apply:** 新しい記事を作成して投稿するときも、このコマンドを使う。`.env` に `OPENAI_API_KEY` が設定済みなので追加作業不要。画像はH2の直下（見出しの次）に配置される。
