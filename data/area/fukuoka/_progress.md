# 福岡県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-04。WebSearch はセッション全体で200回（調査は115回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。九州7県を別々のセッションで同時に作っている（共有メモ data/area/_kyushu/shared.md）。サブエージェントは同時3人まで。

福岡県だけのファイル（data/area/fukuoka/、docs/area-writing-spec-fukuoka.md、articles/*-area-fukuoka*.md、data/subsidies/fukuoka.yml）は自由に作る。`data/subsidies/fukuoka.yml` は areas.yml の福岡県の行と同じコミットで push する。共通ファイルは直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（60市町村。県コード40）
- 一覧は data/area/fukuoka/_brief.md。福岡市 `fukuoka-city`・北九州市 `kitakyushu`（区のページは作らない）
- 他県と同じ slug: okawa（高知 大川村）・nakagawa（長野 中川村）・miyako（岩手 宮古市）・kawasaki-town（宮城 川崎町）→ area-todo に投稿後の確認
- 試算: 月の削減時間×4 を7で割った余りが 0 の時間だけ（九州7県の割り当て）。全県の記事・全県の _calc.py の PLAN と照合
- scripts/area_uniq.py の県の選択肢に fukuoka を足した（push 済み）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md | 8 |
| stats_labor | stats_labor.md | 6 |
| gov_a | gov_ai.md（県・29市・総務省表60行・国の出先機関） | 15 |
| gov_b | gov_ai_b.md（31町村） | 8 |
| subsidy_a | subsidy_a.yml / subsidy_a_areas.md（県・29市） | 12 |
| subsidy_b | subsidy_b.yml / subsidy_b_areas.md（31町村） | 6 |
| cases | cases.md | 25 |
| companies | companies.json / companies.md | 15 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |
| 合計 | | 110 |

## 状態
- [x] _brief.md・wages.md・area_uniq.py（2026-11-04）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-fukuoka.md
- [ ] 記事 61本（県1＋市町村60）
- [ ] data/subsidies/fukuoka.yml・areas.yml・build
- [ ] 地域ガイド（九州地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-04 ネットワーク確認（pref.fukuoka.lg.jp・soumu.go.jp とも開けた）。調査3人を起動（stats・cases・gov_a）
