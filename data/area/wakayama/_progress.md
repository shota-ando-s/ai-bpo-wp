# 和歌山県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-07。WebSearch はセッションで200回まで（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（奈良・滋賀〔と北海道〕を別々のセッションで同時に作っている）。

和歌山県だけのファイル（data/area/wakayama/、docs/area-writing-spec-wakayama.md、articles/*-area-wakayama*.md）は自由に作る。`data/subsidies/wakayama.yml` は areas.yml の和歌山県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_kinki/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（30市町村＝9市20町1村。県コード30）
- 一覧は data/area/wakayama/_brief.md（総務省の全国地方公共団体コードで確認、2026-11-07）
- 和歌山市 `wakayama-city`、かつらぎ町 `katsuragi-town`、美浜町 `mihama-town`、日高町 `hidaka-town-wakayama`、新宮市 `shingu-city`、広川町 `hirogawa`、北山村 `kitayama-village`（共有メモに push 済み）
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を3で割った余りが1の時間だけ**（0.25, 1.0, 1.75, … の0.75時間刻み）。全県の記事・全県の _calc.py の PLAN（奈良・滋賀・北海道を含む）と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 25 |
| gov | gov_ai.md（県・9市・国の出先機関・総務省表の全30行・支援機関） | 12 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・9市） | 10 |
| choson | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（20町1村） | 12 |
| companies | companies.json / companies.md | 12 |
| outside | cases_outside.md / serp.md | 15 |
| cases2 | cases2.md（補充） | 10 |
| 合計 | | 110 |

## 状態
- [x] _brief.md・wages.md・_calc.py の枠（2026-11-07）
- [ ] 調査
- [ ] PLAN を決めて push
- [ ] 執筆仕様 docs/area-writing-spec-wakayama.md
- [ ] 記事 31本（県1＋市町村30）
- [ ] data/subsidies/wakayama.yml・areas.yml・build（同じコミット）
- [ ] 地域ガイド（近畿地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック（check_article・extract_claims・area_uniq・_calc.py）
- [ ] main に push

## 実績メモ
- 2026-11-07 ネットワーク確認（pref.wakayama.lg.jp・soumu.go.jp とも開けた）。HEAD が detached だったので `git checkout -B main origin/main`。市町村30を総務省のコード表で確認。area_uniq.py に wakayama を足し、共有メモに slug を push
- stats・cases を起動
