---
name: post
description: 前回投稿したあとに変わった記事を、まとめて hikitsugi.jp に投稿する。補助金データ・テーマ・プラグインが変わっていればデプロイもする。「投稿して」「全部投稿して」「変更を投稿して」「反映して」「WordPressに上げて」と言われたとき、ファイル名の指定がなければこれを使う。新しい記事を書いてから投稿する流れは seo-article。
argument-hint: "[--no-deploy]"
---

# 変わった記事をまとめて投稿する

`scripts/post_changed.py` が、前回すべて投稿し終えたコミットから HEAD までに変わった `articles/*.md` を投稿する。親ページから順に投稿し、失敗したら1回だけ投稿し直す。途中で止まっても、次に実行すれば残りだけを投稿する。記録は `.post_state.json`（Git 管理外）。

ローカル（`.env` と `ssh sakura` がある Mac）で動かす。クラウドのセッションには `.env` も SSH もないので、そこで頼まれたら、コミットして push するところまでやり、「Mac で『投稿して』と言ってください」と伝える。

ユーザーへの確認は取らずに最後まで進める（「投稿して」と言われた時点で承認済み）。止まるのは下の「止まるとき」だけ。

## 手順

1. リポジトリのルートに移り、GitHub の変更を取り込む（クラウドで直して push した分）。
   ```bash
   cd "$(git rev-parse --show-toplevel)" && git pull --ff-only origin main
   ```
   fast-forward できなければ止まって、ユーザーに状況を伝える。
2. `git status --short -- articles themes plugins data` でコミットしていない変更を見る。あれば、変更の中身を見てコミットする。`data/subsidies/*.yml` が変わっていれば、先に `python3 scripts/build_shindan_data.py` を実行し、JSON も一緒にコミットする。
3. 初回だけ（`.post_state.json` がないとき）: 2026-10-30 の `e4e56bd`（岐阜県の投稿・デプロイと画像の確認を記録）までは投稿済み。`python3 scripts/post_changed.py --init e4e56bd` で記録する。`e4e56bd` が履歴にないときは、ユーザーにどのコミットまで投稿済みかを聞く。
4. 対象を確かめる。
   ```bash
   python3 scripts/post_changed.py --dry-run
   ```
   投稿する記事が0件で、デプロイも「しない」なら、そう伝えて終わる。
5. 投稿する。1件あたり数秒〜十数秒かかる。**30件を超えるときは Bash の `run_in_background` で実行し、出力をログに残す**（Bash の上限10分を超えるため）。
   ```bash
   python3 scripts/post_changed.py $ARGUMENTS 2>&1 | tee /tmp/post_changed.log
   ```
6. 失敗が残ったら、出力の `API Error` を読む。WordPress の空の応答や 5xx なら、もう一度同じコマンドを実行する（残りだけ投稿される）。2回目も同じ記事で失敗したら止まる。
7. 「新しく作ったページ」が出たら、画像に地図が入っていないかを確かめる（CLAUDE.md の「画像生成ルール」）。地図があれば `python3 scripts/fix_map_images.py --apply <記事.md>`。
8. 報告する: 投稿・更新した件数、新しく作ったページの URL、デプロイしたか、失敗が残っているか。記事の一覧は、20件を超えたら県ごとの件数にまとめる。

## 止まるとき

- `git pull --ff-only` が失敗した（ローカルと GitHub の両方に別のコミットがある）
- コミットしていない変更が、意図した変更か分からない（ほかの作業の途中など）
- 同じ記事が2回続けて失敗した
- `deploy.sh` が失敗した（SSH・push の失敗）

## 補足

- 1つの記事だけ投稿するなら、今までどおり `python3 post.py articles/<file>.md` でよい。次に一括で投稿するとき、その記事も対象に入るが、変わった H2 だけ差し替えるので害はない（画像も作り直されない）
- 削除した記事は WordPress からは消さない（一覧に出るので、消すならユーザーに伝えて WordPress の管理画面で）
- デプロイだけしたいときは `./deploy.sh`（`/deploy`）
