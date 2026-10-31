# 山梨県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の「docs(area): 長野県の投稿・デプロイと画像の確認を記録」〔1321d4b〕の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-10-31。新しいセッションなので WebSearch の残りは200回（調査は130回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

## 市町村と slug（27市町村。県コード19）
- 一覧は data/area/yamanashi/_brief.md
- 山梨市は yamanashi-city。大月市 `otsuki`（高知県大月町と同じ slug）・南部町 `nanbu`（青森県南部町と同じ slug）は親ページが違うのでそのまま使う（post.py は親ごとに slug を照合する。朝日町・かほく市と同じ扱い）。投稿後に両方のページが別々にあることを確かめる
- 試算は「月の削減時間・時間換算額」だけの形（ヒキツギAIの月額・回収期間は書かない）

## 調査の分担と WebSearch の配分（このセッションの残り200）
| 担当 | 書くファイル | 対象 | WebSearch |
|---|---|---|---|
| stats | stats.md / stats_labor.md | 人口・経済センサス・製造業・農業・主要産業の候補・地域区分・観光／山梨労働局・TDB甲府支店の県版・県内企業のAI利用の調査 | 15 |
| gov | gov_ai.md | 総務省の表の県と27市町村、各市町村のAI・実証・DX計画、県の企業向けDX支援、国の出先機関、商工会議所・商工会、知事 | 22 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 県・県域の機関と13市（a）、8町6村（b） | 20 |
| cases | cases.md | 県内企業のAI事例（産業支援機構・県・市町村の補助金の成果報告・商工会議所・産業技術センターを最初から） | 25 |
| companies | companies.json / companies.md | 27市町村に本社があるシステム開発・Web開発の会社 | 15 |
| cases_outside・serp | cases_outside.md / serp.md | 同じ業種の県外の中小企業の事例（未使用の出典）、検索結果・FAQ候補 | 22 |
| 合計 | | | 119（残り81を補充・仕様・確認に） |

## 状態
- [x] _brief.md・wages.md、scripts/area_uniq.py に yamanashi を追加（2026-10-31）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-yamanashi.md
- [ ] 記事 28本（県1＋市町村27）
- [ ] data/subsidies/yamanashi.yml、areas.yml、build_shindan_data.py
- [ ] 地域ガイド、area-todo.md、area-new-prefecture.md、memory
- [ ] チェック（check_article・area_uniq・試算の重なり・見出し行だけの表）
- [ ] main に push（投稿・デプロイはユーザーが Mac で）

## 実績メモ
- 2026-10-31 調査開始。stats・gov・subsidy・cases の4人を起動（同時4人まで）
