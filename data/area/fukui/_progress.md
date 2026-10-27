# 福井県 地域ページ 作業状態（再開用）

ブランチ: area-fukui（main の「docs(area): 石川県の投稿・デプロイと画像の確認を記録」の次から）。作業ツリーは `.claude/worktrees/area-fukui/`（`.env` は main の作業フォルダへの symlink）。北陸で3つ目の県。ファイル名の日付と本文の確認日は 2026-10-27。**石川県と同じセッションで始めたので WebSearch の残りは113回**（調査は95回までにする）。

## 市町と slug（17市町。県コード18）
- 一覧は data/area/fukui/_brief.md
- 政令市・村はない。福井市は fukui-city。越前市 echizen-city と越前町 echizen-town は別
- 試算は「月の削減時間・時間換算額」だけの形（ヒキツギAIの月額・回収期間は書かない）
- 原子力発電所（敦賀市・美浜町・高浜町・おおい町）は事実だけ、評価しない、AIの事例にしない

## 新しいセッションでの始め方
1. このファイルと docs/area-new-prefecture.md（「石川県で分かったこと」まで）を読む
2. 作業はこの作業ツリーで行う（`cd /Users/ando/Dropbox/allsrc/ai-bpo-wp/.claude/worktrees/area-fukui`）。消えていたら `git worktree add .claude/worktrees/area-fukui area-fukui`
3. 下の「状態」の続きから

## 調査の分担と WebSearch の配分（このセッションの残り113）
| 担当 | 書くファイル | 対象 | WebSearch |
|---|---|---|---|
| stats_a | stats.md | 人口・経済センサス・製造業（中分類・秘匿）・農林漁業・主要産業の候補・県の地域区分 | 8 |
| stats_b | stats_labor.md | 福井労働局の有効求人倍率、TDB福井支店の県版（なければ全国版）、県内企業のAI利用の調査、観光 | 10 |
| gov_a | gov_ai.md | 総務省の表の県と17市町、県と9市、商工会議所・商工会の一覧 | 12 |
| gov_b | gov_ai_b.md | 8町と、県の企業向けDX・AI支援 | 7 |
| subsidy_a | subsidy_a.yml / subsidy_a_areas.md | 県・県域の機関と9市 | 12 |
| subsidy_b | subsidy_b.yml / subsidy_b_areas.md | 8町 | 5 |
| companies | companies.json / companies.md | 17市町に本社があるシステム開発・Web開発の会社 | 10 |
| cases | cases.md | 県内企業のAI事例 | 16 |
| cases_outside | cases_outside.md | 同じ業種の県外の中小企業の事例（各県の産業支援機関・補助金の成果報告を最初から探す） | 12 |
| serp | serp.md | 検索結果・競合・FAQ候補 | 3 |
| 合計 | | | 95（残り18を執筆と確認に） |

## 状態
- [x] 作業ツリー、_brief.md・wages.md、scripts/area_uniq.py に fukui を追加（2026-10-27）
- [ ] 調査（担当10人）
- [ ] 執筆仕様 docs/area-writing-spec-fukui.md
- [ ] 記事 18本（県1＋市町17）
- [ ] data/subsidies/fukui.yml、areas.yml、build_shindan_data.py
- [ ] 地域ガイド、area-todo.md、area-new-prefecture.md
- [ ] チェック（check_article・area_uniq・試算の重なり・見出し行だけの表）
- [ ] main への反映・投稿・デプロイ・画像の確認

## 実績メモ
- 2026-10-27 調査開始。1陣6人（stats_a・stats_b・gov_a・subsidy_a・companies・cases）を起動
