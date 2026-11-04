# 宮崎県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-04。九州7県を別セッションで同時に作成中（共有メモ data/area/_kyushu/shared.md）。WebSearch はセッションで200回まで（調査は110回まで）。サブエージェントの同時起動は2人まで。post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」）。

宮崎県だけのファイル（data/area/miyazaki/、docs/area-writing-spec-miyazaki.md、articles/*-area-miyazaki*.md、data/subsidies/miyazaki.yml）は自由に作る。`data/subsidies/miyazaki.yml` は areas.yml の宮崎県の行と同じコミットで push する。共通ファイルは直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（26市町村。県コード45）
- 一覧は data/area/miyazaki/_brief.md
- 宮崎市 `miyazaki-city`、美郷町 `misato-town-miyazaki`、日南市 `nichinan`（鳥取県日南町と同じ）、都農町 `tsuno`（高知県津野町と同じ）
- 試算の時間: 月の削減時間×4 を7で割った余りが5（1.25, 3, 4.75, 6.5, … 1.75時間刻み）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| cases | cases.md | 25 |
| gov | gov_ai.md | 20 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 20 |
| companies | companies.json / companies.md | 15 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |

## 状態
- [x] _brief.md・wages.md（2026-11-04）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-miyazaki.md
- [ ] 記事 27本（県1＋市町村26）
- [ ] data/subsidies/miyazaki.yml・areas.yml・build
- [ ] 地域ガイド（九州地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-04 ネットワーク確認（pref.miyazaki.lg.jp・soumu.go.jp とも開けた）。shared.md に slug 4件を push。stats・cases を起動
