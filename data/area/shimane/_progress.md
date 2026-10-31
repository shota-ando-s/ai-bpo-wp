# 島根県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の「chore(area): 山梨県の調査の準備」〔eb16f7c〕の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-10-31。新しいセッションなので WebSearch の残りは200回（調査は125回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

**同じ時間に別のセッションが山梨県を作っている。** 島根県だけのファイル（data/area/shimane/、docs/area-writing-spec-shimane.md、articles/*-area-shimane*.md、data/subsidies/shimane.yml）は自由に作る。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json）は最後に `git pull --rebase origin main` してから直す。衝突したら両方の追加を残し、subsidies.json は build し直す。force push はしない。

## 市町村と slug（19市町村。県コード32）
- 一覧は data/area/shimane/_brief.md
- 美郷町（邑智郡）は `misato-town-shimane`（秋田県美郷町 misato・宮城県美里町 misato-town と重なるため。長野県池田町 ikeda-town-nagano と同じ形）。投稿後に3つのページが別々にあることを確かめる
- 試算は「月の削減時間・時間換算額」だけの形（ヒキツギAIの月額・回収期間は書かない）
- 島根県は中国経済産業局の管内の見込み（要確認）。これまでの17県のどれとも違う

## 調査の分担と WebSearch の配分（このセッションの残り200）
| 担当 | 書くファイル | 対象 | WebSearch |
|---|---|---|---|
| stats | stats.md / stats_labor.md | 人口・経済センサス・製造業・農林水産業・主要産業の候補・地域区分・観光・離島／島根労働局・TDB松江支店の県版・県内企業のAI利用の調査 | 15 |
| gov | gov_ai.md | 総務省の表の県と19市町村、各市町村のAI・実証・DX計画、県の企業向けDX支援・Ruby、国の出先機関、商工会議所・商工会、知事、原子力の事実 | 22 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 県・県域の機関と8市（a）、10町1村（b） | 20 |
| cases | cases.md | 県内企業のAI事例（しまね産業振興財団・県・市町村の補助金の成果報告・商工会議所・産業技術センター・島根大学・中国経産局・地元IT企業の事例を最初から） | 28 |
| companies | companies.json / companies.md | 19市町村に本社があるシステム開発・Web開発の会社 | 15 |
| cases_outside・serp | cases_outside.md / serp.md | 同じ業種の県外の中小企業の事例（未使用の出典）、検索結果・FAQ候補 | 22 |
| 合計 | | | 122（残り78を補充・仕様・確認に） |

## 状態
- [x] _brief.md・wages.md（2026-10-31）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-shimane.md
- [ ] 記事 20本（県1＋市町村19）
- [ ] data/subsidies/shimane.yml、areas.yml、build_shindan_data.py
- [ ] 地域ガイド（中国地方の段を新しく作る）、area_uniq.py、area-todo.md、area-new-prefecture.md、memory
- [ ] チェック（check_article・area_uniq・試算の重なり・見出し行だけの表）
- [ ] main に push（投稿・デプロイはユーザーが Mac で）

## 実績メモ
- 2026-10-31 調査開始。stats・gov・subsidy・cases の4人を起動（同時4人まで）
- 調査4人を起動（ID: stats acbf860df89a85c95 / gov af0c1a2df58a9caf5 / subsidy a243408d7e4c79c96 / cases a38bee7f9f82565d8）。companies・cases_outside+serp は空きが出たら起動
