---
name: feedback_deploy_commit_first
description: デプロイ前に必ずgit commitを行う。未コミットのままdeployするとdeploy.shがpushをスキップして変更が反映されない問題が頻発している
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 67fd1e26-71d9-4c53-b4a2-c70eb3347e53
---

デプロイ前に必ず `git add` → `git commit` を実行してから `./deploy.sh` を呼ぶ。

**Why:** deploy.sh は `git push` → サーバーで `git pull` する仕組みのため、未コミットの変更があっても "Everything up-to-date" となってサーバーに反映されない。このパターンがこのプロジェクトで頻発している。

**How to apply:** ファイル編集後にデプロイを求められたら、まず `git status` で未コミット変更を確認し、あれば `git add <file> && git commit` してから `./deploy.sh` を実行する。
