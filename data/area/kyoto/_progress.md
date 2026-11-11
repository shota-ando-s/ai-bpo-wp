# 京都府 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-11。WebSearch はセッションで200回まで（調査は106回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（静岡・愛知・三重〔と北海道〕を別々のセッションで同時に作っている）。

京都府だけのファイル（data/area/kyoto/、docs/area-writing-spec-kyoto.md、articles/*-area-kyoto*.md）は自由に作る。`data/subsidies/kyoto.yml` は areas.yml の京都府の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_kinki/shared.md、_tokai/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。**書きかけの記事は全ページそろうまで main に入れない**（滋賀と同じ。途中で「投稿して」と言われると親ページなしで子ページが出る）。

## 市町村と slug（26市町村。府コード26）
- 一覧は data/area/kyoto/_brief.md。府は `kyoto`、京都市は `kyoto-city`（区のページは作らない）
- 既存の slug（1,170本）と衝突なし（2026-11-11 に grep で確認）
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を4で割った余りが3（端数 .75）の時間だけ**（_tokai/shared.md）。全県の記事・全県の _calc.py の PLAN と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 25 |
| gov | gov_ai.md（府・15市・国の出先機関・総務省表の全26行） | 14 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（府・15市） | 12 |
| choson | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（10町1村） | 10 |
| companies | companies.json / companies.md | 10 |
| outside | cases_outside.md / serp.md | 15 |
| 予備（cases2 など） | | 6 |
| 合計 | | 106 |

## 状態
- [x] ネットワーク確認（pref.kyoto.jp・soumu.go.jp とも WebFetch で開けた。2026-11-11）
- [x] _brief.md・wages.md
- [ ] area_uniq.py に kyoto
- [ ] 調査
- [ ] _calc.py の PLAN（push）
- [ ] 執筆仕様 docs/area-writing-spec-kyoto.md
- [ ] 記事 27本（府1＋市町村26）
- [ ] data/subsidies/kyoto.yml・areas.yml・build
- [ ] 地域ガイド（近畿の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
