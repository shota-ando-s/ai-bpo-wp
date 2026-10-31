# 鳥取県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の「docs(area): 島根県を地域ガイド・残作業・手順書・memory に追加」〔1b6552a〕の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-10-31。新しいセッションなので WebSearch の残りは200回（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

**同じ main に島根県のセッションが書いている（山梨県も同日）。** 鳥取県だけのファイル（data/area/tottori/、docs/area-writing-spec-tottori.md、articles/*-area-tottori*.md、data/subsidies/tottori.yml）は自由に作る。`data/subsidies/tottori.yml` は areas.yml の鳥取県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json）は最後に `git pull --rebase origin main` してから直す。衝突したら両方の追加を残し、subsidies.json は build し直す。force push はしない。

## 市町村と slug（19市町村。県コード31）
- 一覧は data/area/tottori/_brief.md
- 他県と同じ slug: 若桜町 wakasa（福井県若狭町）・大山町 daisen（秋田県大仙市）・南部町 nanbu（青森県・山梨県）・江府町 kofu（山梨県甲府市）。親ページが違うので別ページになる前提（朝日町・かほく市と同じ）。投稿後に確かめる項目を area-todo に残す
- 試算は「月の削減時間・時間換算額」だけの形。山梨・島根の _calc.py の PLAN と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| gov | gov_ai.md | 18 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 18 |
| cases | cases.md | 25 |
| companies | companies.json / companies.md | 12 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |
| 合計 | | 100 |

## 状態
- [x] _brief.md・wages.md（2026-10-31）
- [ ] 調査
- [ ] 執筆仕様
- [ ] 記事 20本
- [ ] data/subsidies/tottori.yml・areas.yml・build
- [ ] 共通ファイル
- [ ] チェック・push

## 実績メモ
- 2026-10-31 ネットワーク確認（pref.tottori.lg.jp・soumu.go.jp とも開けた）。調査4人を起動（stats・gov・subsidy・cases）
