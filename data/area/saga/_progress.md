# 佐賀県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-04。WebSearch はセッションで200回まで（調査は110回までにする）。サブエージェントの同時起動は2人まで（九州7県を同時に作っている）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

佐賀県だけのファイル（data/area/saga/、docs/area-writing-spec-saga.md、articles/*-area-saga*.md、data/subsidies/saga.yml）は自由に作る。`data/subsidies/saga.yml` は areas.yml の佐賀県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area-todo.md、area-new-prefecture.md、memory、subsidies.json、data/area/_kyushu/shared.md）は直す直前に `git pull --rebase origin main`。他県の行は消さない。force push はしない。書きかけの記事は main に入れない。

## 市町と slug（20市町。県コード41）
- 一覧は data/area/saga/_brief.md
- 佐賀市 `saga-city`、大町町 `omachi-town`（長野県大町市 `omachi`）、白石町 `shiroishi-town`（宮城県白石市 `shiroishi`）、鹿島市 `kashima`（熊本県嘉島町に注意）。九州の共有メモの slug に書いた（push 済み）
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を7で割った余りが1の時間だけ**（0.25, 2, 3.75, 5.5, … 1.75時間刻み）。既存の全県の記事・全県の _calc.py の PLAN（九州の他県は push されていれば）と照合
- scripts/area_uniq.py の県の選択肢に saga を足した（push 済み 9536963）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| cases | cases.md | 30 |
| gov | gov_ai.md | 20 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 20 |
| companies | companies.json / companies.md | 12 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |
| 合計 | | 109 |

## 状態
- [x] _brief.md・wages.md（2026-11-04）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-saga.md
- [ ] 記事 21本（県1＋市町20）
- [ ] data/subsidies/saga.yml・areas.yml・build
- [ ] 地域ガイド（九州地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-04 ネットワーク確認（pref.saga.lg.jp・soumu.go.jp とも開けた）。市町一覧は県の資料（検索1回）で10市10町。stats・cases を起動
