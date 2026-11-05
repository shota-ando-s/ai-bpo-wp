# 沖縄県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-05。WebSearch はセッションで200回まで（調査は120回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（北海道・茨城・栃木・群馬を同時に作っている。アカウントの7日間の利用上限が警告の状態）。

沖縄県だけのファイル（data/area/okinawa/、docs/area-writing-spec-okinawa.md、articles/*-area-okinawa*.md）は自由に作る。`data/subsidies/okinawa.yml` は areas.yml の沖縄県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_batch5/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（41市町村＝11市11町19村。県コード47）
- 一覧は data/area/okinawa/_brief.md（総務省の全国地方公共団体コードで確認）
- 沖縄市 `okinawa-city`、西原町 `nishihara-town`、東村 `higashi-village`
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を5で割った余りが4の時間だけ**（1.0, 2.25, 3.5, … の1.25時間刻み）。全県の記事・全県の _calc.py の PLAN（北海道・北関東3県を含む）と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| gov | gov_ai.md（県・11市・国の出先機関・沖縄振興の制度・総務省表の全41行） | 14 |
| cases | cases.md | 25 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・11市） | 12 |
| choson_a | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（本島の17町村） | 10 |
| choson_b | gov_ai_c.md / subsidy_c.yml / subsidy_c_areas.md（離島の13町村） | 10 |
| companies | companies.json / companies.md | 12 |
| outside | cases_outside.md / serp.md | 15 |
| cases2 | cases2.md（補充） | 8 |
| 合計 | | 120 |

## 状態
- [x] _brief.md・wages.md（2026-11-05）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-okinawa.md
- [ ] 記事 42本（県1＋市町村41）
- [ ] data/subsidies/okinawa.yml・areas.yml・build
- [ ] 地域ガイド・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-05 ネットワーク確認（pref.okinawa.lg.jp・soumu.go.jp とも開けた）。ローカルの HEAD が detached だったので `git checkout -B main origin/main`。市町村41を総務省のコード表で確認。area_uniq.py に okinawa を足した。共有メモに slug を push
