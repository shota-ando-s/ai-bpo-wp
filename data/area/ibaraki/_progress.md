# 茨城県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-05。WebSearch はセッションで200回まで（調査は115回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（北海道・北関東3県・沖縄を同時に作っている。アカウントの7日間の利用上限が警告の状態）。

茨城県だけのファイル（data/area/ibaraki/、docs/area-writing-spec-ibaraki.md、articles/*-area-ibaraki*.md）は自由に作る。`data/subsidies/ibaraki.yml` は areas.yml の茨城県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_batch5/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（44市町村。県コード08）
- 一覧は data/area/ibaraki/_brief.md
- 茨城町 `ibaraki-town`、境町 `sakai-town`。古河市 `koga`・鹿嶋市 `kashima`・那珂市 `naka` は他県と同じ slug（親ページが違う）
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を5で割った余りが1の時間だけ**（0.25, 1.5, 2.75, …の1.25時間刻み）。全県の記事・全県の _calc.py の PLAN と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 25 |
| gov | gov_ai.md（県・32市・国の出先機関・総務省表の全44行） | 14 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・32市） | 12 |
| choson | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（10町2村） | 10 |
| companies | companies.json / companies.md | 12 |
| outside | cases_outside.md / serp.md | 15 |
| cases2 | cases2.md（補充） | 10 |
| 合計 | | 112 |

## 状態
- [x] _brief.md・wages.md（2026-11-05）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-ibaraki.md
- [ ] 記事 45本（県1＋市町村44）
- [ ] data/subsidies/ibaraki.yml・areas.yml・build
- [ ] 地域ガイド（北関東の段）・area_uniq.py・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-05 ネットワーク確認（pref.ibaraki.jp・soumu.go.jp とも開けた）。ローカルの main が detached だったので origin/main に合わせ直した
