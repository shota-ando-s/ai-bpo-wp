# 東京都 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付は 2026-11-14。WebSearch はセッションで200回まで。**残りが30回を切ったら区切る**。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（大阪府を別のセッションで同時に作っている。アカウントの週の利用上限が警告の状態）。

東京都だけのファイル（data/area/tokyo/、docs/area-writing-spec-tokyo.md、articles/*-area-tokyo*.md）は自由に作る。`data/subsidies/tokyo.yml` は areas.yml の東京の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_shutoken/shared.md）は直す直前に `git pull --rebase origin main`。他県の行は消さない。force push はしない。書きかけの記事は main に入れない。

## 段階（62区市町村＝23区・26市・5町・8村。一覧と slug は _brief.md）

| 段階 | 範囲 | 状態 |
|---|---|---|
| 1 | 都全体の調査・都のページ | 調査は完了（stats・gov）。**都のページは段階2の23区と一緒に書く**（23区へのリンクを入れるため） |
| 2 | 23区 | 調査中（govsub_1・govsub_2・cases 完了、companies・cases2 作業中）。PLAN push 済み。診断データ push 済み |
| 3 | 多摩（26市・3町・1村） | 未 |
| 4 | 島しょ（2町・7村） | 未 |

## 実績メモ
- 2026-11-14 ネットワーク確認（metro.tokyo.lg.jp・soumu.go.jp とも開けた）。ローカルが detached だったので origin/main に合わせ直した。_brief.md（62区市町村・slug）。既存 slug とぶつかる 千代田区 chiyoda-ku・中央区 chuo-ku・大田区 ota-ku・中野区 nakano-ku・府中市 fuchu-city-tokyo・日野市 hino-city・瑞穂町 mizuho-town・三宅村 miyake-village・利島村 toshima-village-tokyo、紛らわしい 豊島区 toshima-ku・北区 kita-ku
- WebSearch 累計 0（親）
- stats（4回）・gov（5回）完了。都の人口 14,236,627人（R7国調）、有効求人倍率 1.71倍（受理地別）・1.08倍（就業地別）、TDB東京都版5本（後継者不在率47.9%・社長年齢60.2歳・休廃業15,806件・正社員不足51.5%・生成AI 44.6%）、知事 小池百合子。都の DX推進トータルサポートの派遣の募集は終了（パイロットの「受付中」は古い）
- govsub_1（12回、12区）・govsub_2（10回、11区）完了。生成AIを名指しする区の制度は江東区・中野区・豊島区、品川区は「ＡＩを活用したシステム」。国の補助への上乗せは港区（ものづくり・省力化）・葛飾区（人材開発支援助成金）、都の助成への上乗せは品川区。区の公社・財団は板橋区・練馬区（ほかはまちみらい千代田など区の団体）
- 23区の PLAN を _calc.py に（月36.25〜112時間・約11.4万〜43.1万円・15〜65名）。push
- 補助金診断: tokyo.yml を都8制度＋23区41制度＋多摩のパイロット2制度（51制度）、areas.yml の東京を23区＋多摩のパイロット5市に。build 1,390→1,425制度（他県不変）。push。区の「公社の専門家派遣の利用料の補助」（1回あたりの定額）は addon の計算式にないので addon を付けずに載せた
- cases（17回）完了。数値つきで未使用の公的な事例はサカツ（豊島区）・NextNinja（品川区）だけ。事例のない区5つ → cases2（12回まで）を起動
- WebSearch 累計 48＋companies・cases2

## 次にやること
- companies・cases2 の結果を受け取る → 仕様の下書き D12・D345 → 執筆（23区を3ページずつ＋都のページ）
