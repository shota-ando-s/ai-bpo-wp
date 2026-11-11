# 三重県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-11。WebSearch はセッションで200回まで（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（静岡・愛知・京都〔と北海道〕を別々のセッションで同時に作っている）。

三重県だけのファイル（data/area/mie/、docs/area-writing-spec-mie.md、articles/*-area-mie*.md）は自由に作る。`data/subsidies/mie.yml` は areas.yml の三重県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_tokai/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。**書きかけの記事は全ページそろうまで main に入れない**（途中で「投稿して」と言われると親ページなしで子ページが出るため。滋賀の記録）。

## 市町と slug（29市町。県コード24）
- 一覧は data/area/mie/_brief.md
- 他県と同じ slug: 朝日町 `asahi-town`（富山・山形と同じ。過去の記録どおり親ページが違えば別ページ）、明和町 `meiwa`（群馬）、紀北町 `kihoku`（愛媛県鬼北町）。変えた slug: 熊野市 `kumano-city`（広島県熊野町 `kumano`）、御浜町 `mihama-town-mie`（福井 `mihama`・和歌山 `mihama-town`）、川越町 `kawagoe-town`（埼玉県川越市を見越して）。投稿後に別ページになったかを確かめる項目を area-todo に残す
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を4で割った余りが2の時間だけ**（_tokai/shared.md。端数 .50 の時間＝0.5, 1.5, 2.5, … の1時間刻み）。全県の記事・全県の _calc.py の PLAN と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| cases | cases.md | 25 |
| gov | gov_ai.md（県・14市・国の出先機関・総務省表の全29行・リンクの条件） | 14 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・14市） | 12 |
| choson | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（15町） | 10 |
| companies | companies.json / companies.md | 10 |
| outside | cases_outside.md / serp.md | 15 |
| cases2 | cases2.md（事例の補充） | 10 |
| 合計 | | 108 |

## 状態
- [x] _brief.md・wages.md・area_uniq.py に mie（2026-11-11）
- [ ] 調査
- [ ] 試算の PLAN（_calc.py）を push
- [ ] 執筆仕様 docs/area-writing-spec-mie.md
- [ ] 記事 30本（県1＋市町29）
- [ ] data/subsidies/mie.yml・areas.yml・build
- [ ] 地域ガイド・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push（投稿・デプロイはユーザーが Mac で「投稿して」）

## 実績メモ
- 2026-11-11 ネットワーク確認（pref.mie.lg.jp・soumu.go.jp とも WebFetch で開けた）。git pull で最新
- stats・cases 起動
