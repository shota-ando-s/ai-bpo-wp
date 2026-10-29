# 岐阜県 地域ページ 作業状態（再開用）

ブランチ: area-gifu（main の「feat: 「投稿して」で変わった記事をまとめて投稿する」〔d47d6c1〕の次から）。作業ツリーは `.claude/worktrees/area-gifu/`（`.env` は main の作業フォルダへの symlink）。東海で最初の県。ファイル名の日付と本文の確認日は 2026-10-29。新しいセッションなので WebSearch の残りは200回（調査は135回までにする）。

## 市町村と slug（42市町村。県コード21）
- 一覧は data/area/gifu/_brief.md
- 岐阜市は gifu-city、山県市は yamagata-city、大野町は ono-town、池田町は ikeda-town、白川町は shirakawa-town、白川村は shirakawa-village
- 試算は「月の削減時間・時間換算額」だけの形（ヒキツギAIの月額・回収期間は書かない）

## 新しいセッションでの始め方
1. このファイルと docs/area-new-prefecture.md（「福井県で分かったこと」まで）を読む
2. 作業はこの作業ツリーで行う（`cd /Users/ando/Dropbox/allsrc/ai-bpo-wp/.claude/worktrees/area-gifu`）。消えていたら `git worktree add .claude/worktrees/area-gifu area-gifu`
3. 下の「状態」の続きから

## 調査の分担と WebSearch の配分（このセッションの残り200）
| 担当 | 書くファイル | 対象 | WebSearch |
|---|---|---|---|
| stats_a | stats.md | 人口・経済センサス・製造業（中分類・秘匿）・農林漁業・主要産業の候補・県の地域区分 | 10 |
| stats_b | stats_labor.md | 岐阜労働局の有効求人倍率、TDB岐阜支店の県版（なければ東海・全国版）、県内企業のAI利用の調査、観光 | 10 |
| gov_a | gov_ai.md | 総務省の表の県と42市町村、県と21市、商工会議所・商工会の一覧 | 18 |
| gov_b | gov_ai_b.md | 19町2村と、県の企業向けDX・AI支援 | 12 |
| subsidy_a | subsidy_a.yml / subsidy_a_areas.md | 県・県域の機関と21市 | 18 |
| subsidy_b | subsidy_b.yml / subsidy_b_areas.md | 19町2村 | 12 |
| companies | companies.json / companies.md | 42市町村に本社があるシステム開発・Web開発の会社 | 16 |
| cases | cases.md | 県内企業のAI事例（岐阜県DX推進コンソーシアム・ソフトピアジャパンの成果報告を含む） | 20 |
| cases_outside | cases_outside.md | 同じ業種の県外の中小企業の事例（各県の産業支援機関・商工会議所・補助金の成果報告） | 15 |
| serp | serp.md | 検索結果・競合・FAQ候補 | 4 |
| 合計 | | | 135（残り65を執筆と確認に） |

## 状態
- [x] 作業ツリー、_brief.md・wages.md、scripts/area_uniq.py に gifu を追加（2026-10-29）
- [ ] 調査（担当10人）
- [ ] 執筆仕様 docs/area-writing-spec-gifu.md
- [ ] 記事 43本（県1＋市町村42）
- [ ] data/subsidies/gifu.yml、areas.yml、build_shindan_data.py
- [ ] 地域ガイド、area-todo.md、area-new-prefecture.md
- [ ] チェック（check_article・area_uniq・試算の重なり・見出し行だけの表）
- [ ] main への反映・投稿・デプロイ・画像の確認

## 実績メモ
- 2026-10-29 調査開始
