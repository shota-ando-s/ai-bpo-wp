# 東京都 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付は 2026-11-14。WebSearch はセッションで200回まで。**残りが30回を切ったら区切る**。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（大阪府を別のセッションで同時に作っている。アカウントの週の利用上限が警告の状態）。

東京都だけのファイル（data/area/tokyo/、docs/area-writing-spec-tokyo.md、articles/*-area-tokyo*.md）は自由に作る。`data/subsidies/tokyo.yml` は areas.yml の東京の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_shutoken/shared.md）は直す直前に `git pull --rebase origin main`。他県の行は消さない。force push はしない。書きかけの記事は main に入れない。

## 段階（62区市町村＝23区・26市・5町・8村。一覧と slug は _brief.md）

| 段階 | 範囲 | 状態 |
|---|---|---|
| 1 | 都全体の調査・都のページ | 調査中 |
| 2 | 23区 | 未 |
| 3 | 多摩（26市・3町・1村） | 未 |
| 4 | 島しょ（2町・7村） | 未 |

## 実績メモ
- 2026-11-14 ネットワーク確認（metro.tokyo.lg.jp・soumu.go.jp とも開けた）。ローカルが detached だったので origin/main に合わせ直した。_brief.md（62区市町村・slug）。既存 slug とぶつかる 千代田区 chiyoda-ku・中央区 chuo-ku・大田区 ota-ku・中野区 nakano-ku・府中市 fuchu-city-tokyo・日野市 hino-city・瑞穂町 mizuho-town・三宅村 miyake-village・利島村 toshima-village-tokyo、紛らわしい 豊島区 toshima-ku・北区 kita-ku
- WebSearch 累計 0（親）

## 次にやること
- 段階1の調査（stats・gov/都の補助金）→ 段階2の調査（23区の行政・補助金・事例・IT企業）
