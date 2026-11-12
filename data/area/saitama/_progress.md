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
- stats 4（完了: stats.md 1,385行・stats_labor.md 193行。63市町村・コード一致、県計と一致、地域振興センターの所管も _brief と一致〔さいたま市はどのセンターにも属さない〕。町はすべて「まち」。**2026年の大きな災害はなし**（秩父市浦山の林野火災 約143ha〔2/27鎮火〕、8/23 地震 川口・蕨・戸田・宮代 震度5弱 軽傷9、6/16 地震 加須・本庄・美里 震度5弱 一部破損20棟、台風6号 床上12棟、1月の大雪 負傷29）。都内で従業 県24.1%（和光54.5・朝霞42.0・新座41.6・蕨40.4・戸田39.9、秩父は1%前後。本庄・上里・神川は群馬へが多い）、昼夜間人口比率89.6。製造品出荷額15.3兆円（7位）、食料品・印刷は全国2位。熊谷市は化学が52.8%、寄居町は内訳なし。TDB大宮支店の県版: 後継者不在率54.0%・社長年齢61.1歳・生成AI 32.3%（378社）・人手不足（2026-07、正社員51.7%）。有効求人倍率 就業地別 1.14・受理地別 0.97（2026-09）、一般事務0.20・介護4.36。最低賃金 1,196円（2026-10-01）。取れず: HW別倍率・社人研・秩父の交通・本田の工場の現状）
- govsub_1（WS7）起動
- gov 2（完了: gov_ai.md・subsidy_pref.yml 3件・subsidy_pref_areas.md。総務省表 生成AI 導入済34・実証中9・表にない20、生成AIもAI全般もないのは8町（越生・嵐山・吉見・ときがわ・皆野・長瀞・神川・松伏）。ツール LoGoAI 15・QommonsAI 11・マサルくん9・zevo 8。zevo 共同利用は県の発表 2026-03-30「令和8年4月から」15団体（県は入っていない）。DX推進計画 第2期 R6.4.1〜R9.3.31（R8.3一部変更）。知事 大野元裕（2期目）。**国: 関東経済産業局（さいたま市、サイト403）・関東財務局（本局が担当、財務事務所なし）・埼玉労働局・関東農政局 埼玉県拠点・関東運輸局 埼玉運輸支局（本局は横浜市）**。**県域で今申請できる企業向けIT・AI補助金はない**（県DX導入支援 10/30終了〔条件は「本店又は主たる事業所」〕・省力化 7/17終了・公社の人材育成講座補助は団体向け 2027-01-12まで）。県の上乗せなし。リンク: 県・公社とも連絡不要（リンクと明記・フレーム不可、転載は承認）。saitamadx.com は公社DX推進支援グループ運営（27団体、R3.10設立）。第4回埼玉DX大賞 表彰 R9.1予定。公社 AI基礎講座〔2〕11/27・12/4、無料DX推進セミナー 12/4。商工会議所16・商工会52＋県連（横瀬町は名簿になし→govsub_4 で確認））
- govsub_2（WS7）起動
