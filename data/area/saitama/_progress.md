# 埼玉県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-12。WebSearch はセッションで200回まで（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」）。サブエージェントの同時起動は2人まで。

**同時に神奈川・千葉と北海道の続きを別々のセッションで作っている**。共有メモは `data/area/_shutoken/shared.md`。埼玉県だけのファイル（data/area/saitama/、docs/area-writing-spec-saitama.md、articles/*-area-saitama*.md）は自由に作る。`data/subsidies/saitama.yml` は areas.yml の埼玉県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_shutoken/shared.md）は直す直前に `git pull --rebase origin main`。書きかけの記事は main に入れない（post_changed.py が公開する）。force push はしない。

## 市町村と slug（63市町村＝40市22町1村。県コード11）
- 一覧は data/area/saitama/_brief.md
- さいたま市は1ページ（区のページは作らない）。県 `saitama`、市 `saitama-city`
- 他県とぶつかる slug を変えた: 三郷市 `misato-city`・美里町 `misato-town-saitama`・富士見市 `fujimi-city`・日高市 `hidaka-city`・伊奈町 `ina-town`・三芳町 `miyoshi-town`・小川町 `ogawa-town`・神川町 `kamikawa-town`（共有メモに書いた）
- 試算は「月の削減時間・時間換算額」だけの形。**他県との重なりは許容し、埼玉県の中だけ時間・金額・規模を重ねない**（2026-11-11 ユーザー決定）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 20 |
| gov | gov_ai.md / subsidy_pref.yml / subsidy_pref_areas.md（県・国の出先機関・総務省表の全63行・県域の補助金・商工会議所/商工会の名簿・県のリンク条件） | 10 |
| govsub_1 | gov_ai_1.md / subsidy_1.yml / subsidy_1_areas.md（さいたま市・南部・南西部・県央 16市町。兵庫と同じ形） | 7 |
| govsub_2 | gov_ai_2.md / subsidy_2.yml / subsidy_2_areas.md（東部・利根 16市町。兵庫と同じ形） | 7 |
| govsub_3 | gov_ai_3.md / subsidy_3.yml / subsidy_3_areas.md（川越比企・西部 19市町村。兵庫と同じ形） | 7 |
| govsub_4 | gov_ai_4.md / subsidy_4.yml / subsidy_4_areas.md（北部・秩父 12市町。兵庫と同じ形） | 7 |
| companies | companies.json / companies.md | 10 |
| outside | cases_outside.md / serp.md | 12 |
| cases2 | cases2.md（補充） | 10 |
| 合計 | | 104 |

## 状態
- [x] _brief.md・wages.md・area_uniq.py に saitama・共有メモに slug（2026-11-12）
- [ ] 調査（10担当）
- [ ] 試算の PLAN（_calc.py）を push
- [ ] 執筆仕様 docs/area-writing-spec-saitama.md
- [ ] 記事 64本（県1＋市町村63）
- [ ] data/subsidies/saitama.yml・areas.yml・build
- [ ] 地域ガイド・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック（check_article・area_uniq・_calc.py・試算の結果表・書いてはいけない局名）
- [ ] main に push（投稿・デプロイはユーザーが Mac で「投稿して」）

## 再開するとき
- 調査の担当が止まったら、ファイルの続きから書くよう新しい担当に頼む（ファイルは節ごとに書き足してある）
- 書きかけの記事は .git/info/exclude で未追跡のまま置き、書き終えた分は area-saitama-wip ブランチに退避する

## 実績メモ
- 2026-11-12 ネットワーク確認（pref.saitama.lg.jp・soumu.go.jp とも WebFetch で開けた）。WebSearch 0回
- stats（WS14）・cases（WS20）起動
- 国のデジタル化・AI導入補助金 7次締切は 2026-12-01（火）17:00、交付決定 2027-01-19 予定（事務局 https://it-shien.smrj.go.jp/schedule/ を 2026-11-12 に WebFetch で確認。8次は日程未掲載）
- コンテナが再起動し stats・cases が止まった（cases.md 116行は残った）。SendMessage で再開
- cases 14（完了: cases.md 319行。**未使用・数値つきの県内中小3件**: 日本精密金型（川口市44名、AIビジョンで外観検査 月120h→約1/6）・セントラルサービス（行田市15人、AI清掃ロボットで7人→1台+5人）〔出典は県「中小企業人手不足対応支援事業 事例集」80本〕、らしく（さいたま市3名、生成AI文書検索で生産性約2倍、さいたま市産業創造財団の事例集）。いずれも事業者の申告。ベンダー発表: 川島製作所（草加、meviy、兵庫県稲美町で使用済み）・谷野製作所（日高、meviy）→どちらか片方、山田食品産業（所沢）・旭産業（戸田）・向山工場（川口、AIは久喜工場）・長瀞町観光協会（試験導入）。他県で使用済み: ヤマザキライス（杉戸）・比企オプティクス（秩父）・ライフタイムサポート（越谷）・伊田テクノス（東松山）・ニッシン・パーテクチュアル（春日部）・元気村グループ。(A): 済生会川口総合病院・鈴与カーゴサービス北関東（川越）ほか。食料品・印刷・物流・介護・輸送機械の中小、南西部・県央・利根・西部・比企の町村・北部・秩父の町は0件）
- gov（WS10）起動
