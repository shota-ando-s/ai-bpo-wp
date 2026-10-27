# 石川県 地域ページ 作業状態（再開用）

ブランチ: area-ishikawa（main の「docs(area): 富山県のデプロイ済みを記録」の次から）。作業ツリーは `.claude/worktrees/area-ishikawa/`（`.env` は main の作業フォルダへの symlink）。北陸で2つ目の県。ファイル名の日付と本文の確認日は 2026-10-27。

## 市町と slug（19市町。県コード17）
- 一覧は data/area/ishikawa/_brief.md
- 政令市はない（金沢市は中核市）。かほく市 kahoku は山形県河北町と同じ slug（post.py は親ごとに照合するので重複しない。朝日町 asahi-town と同じ）。能登町 noto-town
- 試算は山形県以降と同じ「月の削減時間・時間換算額」だけの形（ヒキツギAIの月額・回収期間は書かない）
- 能登半島地震・奥能登豪雨は、福島県の原子力災害と同じ扱い（事実と時点だけ、評価・感想・応援の言葉は書かない）

## 新しいセッションでの始め方
1. このファイルと docs/area-new-prefecture.md（「富山県で分かったこと」まで）を読む
2. 作業はこの作業ツリーで行う（`cd /Users/ando/Dropbox/allsrc/ai-bpo-wp/.claude/worktrees/area-ishikawa`）。消えていたら `git worktree add .claude/worktrees/area-ishikawa area-ishikawa`
3. 下の「状態」の続きから

## 調査の分担と WebSearch の配分（上限200）
| 担当 | 書くファイル | 対象 | WebSearch |
|---|---|---|---|
| stats_a | stats.md | 人口（社人研R5・地震後の推計人口・令和7年国勢調査の速報）・経済センサス・製造業（経済構造実態調査。中分類・秘匿）・農林漁業（農政局の市町村別農業産出額、漁業センサス）・主要産業の候補・県の地域区分 | 10 |
| stats_b | stats_labor.md | 石川労働局の有効求人倍率（HW別・職業別・管轄）、TDB金沢支店の県版（なければ北陸版・全国版）、県内企業のAI利用の調査、観光（地震の前後） | 12 |
| gov_a | gov_ai.md | 総務省の生成AI・AI導入調査の県と19市町の表、県と11市、県内の商工会議所・商工会の一覧 | 14 |
| gov_b | gov_ai_b.md | 8町と、県の企業向けDX・AI支援（ISICO・工業試験場など） | 8 |
| subsidy_a | subsidy_a.yml / subsidy_a_areas.md | 県・県域の機関と11市（能登半島地震・豪雨の支援制度は分けて書く） | 14 |
| subsidy_b | subsidy_b.yml / subsidy_b_areas.md | 8町 | 6 |
| companies | companies.json / companies.md | 19市町に本社があるシステム開発・Web開発の会社（公式で本社と従業員数の両方を確かめた会社だけを本表に、従業員数順に5社まで） | 14 |
| cases | cases.md | 県内企業のAI事例 | 18 |
| cases_outside | cases_outside.md | 同じ業種の県外の中小企業の事例（既存の data/area と articles に出る事例は使わない） | 14 |
| serp | serp.md | 検索結果・競合・FAQ候補 | 5 |
| 合計 | | | 115（残り85を補充・執筆と確認に） |

## 状態
- [x] 作業ツリー、_brief.md・wages.md、scripts/area_uniq.py に ishikawa を追加（2026-10-27）
- [ ] 調査（担当10人）
- [ ] 執筆仕様 docs/area-writing-spec-ishikawa.md
- [ ] 記事 20本（県1＋市町19）
- [ ] data/subsidies/ishikawa.yml、areas.yml、build_shindan_data.py
- [ ] 地域ガイド、area-todo.md、area-new-prefecture.md
- [ ] チェック（check_article・area_uniq・試算の重なり・見出し行だけの表）
- [ ] main への反映・投稿・デプロイ・画像の確認

## 実績メモ
