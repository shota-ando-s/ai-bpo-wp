# 群馬県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の 31f0f02「docs(area): 北海道・北関東3県・沖縄の同時作成のための共有メモ」の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-05。WebSearch はセッション全体で200回まで（調査は120回までにする）。サブエージェントの同時起動は2人まで。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

同時に茨城・栃木・北海道・沖縄を別のセッションで作っている。共有メモは `data/area/_batch5/shared.md`。試算は「月の削減時間×4 を5で割った余りが3」の時間だけを使う。

## 市町村と slug（35市町村。県コード10）
- 一覧は data/area/gunma/_brief.md
- 高山村 `takayama-village-gunma`・昭和村 `showa-village-gunma`（長野・福島に同名の村）。南牧村は `nanmoku`（長野は `minamimaki`）
- 試算は「月の削減時間・時間換算額」だけの形（ヒキツギAIの月額・回収期間は書かない）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | 対象 | WebSearch |
|---|---|---|---|
| stats | stats.md / stats_labor.md | 人口・経済センサス・製造業・農業・主要産業・地域区分・観光・外国人住民／群馬労働局・TDB前橋支店の県版・県内企業のAI利用の調査 | 15 |
| gov | gov_ai.md | 総務省の表の県と35市町村、12市のAI・実証・DX計画、県の企業向けDX支援、国の出先機関、商工会議所、知事 | 15 |
| gov_b | gov_ai_b.md | 15町8村のAI・実証・DX計画、商工会 | 8 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 県・県域の機関と12市（a）、15町8村（b） | 15 |
| cases | cases.md | 県内企業のAI事例（産業支援機構・県・市町村の成果報告・県議会・商工会議所・産業技術センター） | 25 |
| companies | companies.json / companies.md | 35市町村に本社があるシステム開発・Web開発の会社 | 12 |
| outside | cases_outside.md / serp.md | 同じ業種の県外の中小企業の事例（未使用の出典）、検索結果・FAQ候補 | 20 |
| 合計 | | | 110 |

## 状態
- [x] _brief.md・wages.md、scripts/area_uniq.py に gunma を追加、共有メモに slug（2026-11-05）
- [ ] 調査
- [ ] 試算の PLAN（_calc.py）を push
- [ ] 執筆仕様 docs/area-writing-spec-gunma.md
- [ ] 記事 36本（県1＋市町村35）
- [ ] data/subsidies/gunma.yml、areas.yml、build_shindan_data.py（同じコミット）
- [ ] 地域ガイド（北関東の段）、area-todo.md、area-new-prefecture.md、memory
- [ ] チェック（check_article・area_uniq・試算の重なり・見出し行だけの表）
- [ ] main に push

## 実績メモ
- 2026-11-05 ネットワークの確認: pref.gunma.jp・soumu.go.jp とも WebFetch で開けた
