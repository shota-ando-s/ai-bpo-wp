# 大阪府 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-14。WebSearch はセッションで200回まで（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」）。サブエージェントの同時起動は2人まで（週の利用上限が警告の状態）。

**同時に東京都の地域ページを別のセッションで作っている**。近畿の共有メモは `data/area/_kinki/shared.md`。大阪府だけのファイル（data/area/osaka/、docs/area-writing-spec-osaka.md、articles/*-area-osaka*.md）は自由に作る。`data/subsidies/osaka.yml` は areas.yml の大阪府の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_kinki/shared.md）は直す直前に `git pull --rebase origin main`。書きかけの記事は main に入れない（post_changed.py が公開する）。force push はしない。

## 市町村と slug（43市町村＝33市9町1村。府コード27）
- 一覧は data/area/osaka/_brief.md
- 大阪市・堺市は各1ページ（区のページは作らない）。府 `osaka`、市 `osaka-city`・`sakai-city`
- 他県とぶつかる slug を変えた: 堺市 `sakai-city`・池田市 `ikeda-city`・茨木市 `ibaraki-city`・和泉市 `izumi-city`・岬町 `misaki-town`・太子町 `taishi-town-osaka`（共有メモに書いた）
- 試算は「月の削減時間・時間換算額」だけの形。**他県との重なりは許容し、大阪府の中だけ時間・金額・規模を重ねない**（2026-11-11 ユーザー決定）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 20 |
| gov | gov_ai.md / subsidy_pref.yml / subsidy_pref_areas.md（府・国の出先機関・総務省表の全43行・府域の補助金・商工会議所/商工会の名簿・府のリンク条件・万博/IR の一次資料） | 10 |
| govsub_1 | gov_ai_1.md / subsidy_1.yml / subsidy_1_areas.md（大阪市・堺市・豊能・三島 12市町） | 7 |
| govsub_2 | gov_ai_2.md / subsidy_2.yml / subsidy_2_areas.md（北河内・中河内 10市） | 7 |
| govsub_3 | gov_ai_3.md / subsidy_3.yml / subsidy_3_areas.md（南河内 9市町村） | 7 |
| govsub_4 | gov_ai_4.md / subsidy_4.yml / subsidy_4_areas.md（泉北・泉南 12市町） | 7 |
| companies | companies.json / companies.md | 10 |
| outside | cases_outside.md / serp.md | 12 |
| cases2 | cases2.md（補充） | 10 |
| 合計 | | 104 |

## 状態
- [x] _brief.md・wages.md・area_uniq.py に osaka・共有メモに slug（2026-11-14）
- [ ] 調査（10担当）
- [ ] 試算の PLAN（_calc.py）
- [ ] 執筆仕様 docs/area-writing-spec-osaka.md
- [ ] 記事 44本（府1＋市町村43）
- [ ] data/subsidies/osaka.yml・areas.yml・build
- [ ] 地域ガイド・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック（check_article・area_uniq・_calc.py・試算の結果表・書いてはいけない局名）
- [ ] main に push（投稿・デプロイはユーザーが Mac で「投稿して」）

## 再開するとき
- 調査の担当が止まったら、ファイルの続きから書くよう新しい担当に頼む（ファイルは節ごとに書き足してある）
- 書きかけの記事は .git/info/exclude（`articles/2026-11-14-area-osaka*.md`）で未追跡のまま置き、書き終えた分は `bash data/area/osaka/_wip_push.sh` で area-osaka-wip ブランチに退避する（再起動で消えたら `git fetch origin area-osaka-wip && git checkout FETCH_HEAD -- 'articles/2026-11-14-area-osaka*.md'` で戻し、exclude を足し直す）

## 実績メモ
- 2026-11-14 ネットワーク確認（pref.osaka.lg.jp・soumu.go.jp とも WebFetch・curl で開けた）。WebSearch 0回
