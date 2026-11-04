# 熊本県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-04。WebSearch はセッション全体で200回まで（調査は120回まで）。サブエージェントの同時起動は2人まで（九州7県を同時に作っているため）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

九州7県を別々のセッションで同時に作っている。共有メモは `data/area/_kyushu/shared.md`。試算の時間は「月の削減時間×4 を7で割った余りが 3」だけを使う。金額が九州の他県と重なったら、先に PLAN を push した県を優先する。

熊本県だけのファイル（data/area/kumamoto/、docs/area-writing-spec-kumamoto.md、articles/*-area-kumamoto*.md、data/subsidies/kumamoto.yml）は自由に作る。`data/subsidies/kumamoto.yml` は areas.yml の熊本県の行と同じコミットで push する。共通ファイルは直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（45市町村。県コード43）
- 一覧は data/area/kumamoto/_brief.md
- 熊本市 `kumamoto-city`（区のページは作らない）、美里町 `misato-town-kumamoto`、嘉島町 `kashima-town`（佐賀県鹿島市 `kashima`）、大津町 `ozu`（愛媛県大洲市と同じ）、高森町 `takamori`（長野県高森町と同じ）、小国町 `oguni`（山形県小国町は `oguni-town`）
- scripts/area_uniq.py の県の選択肢に kumamoto を足した（push 済み 629a105）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 26 |
| gov | gov_ai.md | 22 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 22 |
| companies | companies.json / companies.md | 14 |
| cases_outside・serp | cases_outside.md / serp.md | 16 |
| 合計 | | 114 |

## 状態
- [x] _brief.md・wages.md（2026-11-04）、shared.md に slug
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-kumamoto.md
- [ ] 記事 46本（県1＋市町村45）
- [ ] data/subsidies/kumamoto.yml・areas.yml・build
- [ ] 地域ガイド（九州地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-04 ネットワーク確認（pref.kumamoto.jp・soumu.go.jp とも開けた）。WebSearch 1回（市町村数の確認）。stats・cases を起動
