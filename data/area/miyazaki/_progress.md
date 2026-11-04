# 宮崎県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-04。九州7県を別セッションで同時に作成中（共有メモ data/area/_kyushu/shared.md）。WebSearch はセッションで200回まで（調査は110回まで）。サブエージェントの同時起動は2人まで。post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」）。

宮崎県だけのファイル（data/area/miyazaki/、docs/area-writing-spec-miyazaki.md、articles/*-area-miyazaki*.md、data/subsidies/miyazaki.yml）は自由に作る。`data/subsidies/miyazaki.yml` は areas.yml の宮崎県の行と同じコミットで push する。共通ファイルは直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（26市町村。県コード45）
- 一覧は data/area/miyazaki/_brief.md
- 宮崎市 `miyazaki-city`、美郷町 `misato-town-miyazaki`、日南市 `nichinan`（鳥取県日南町と同じ）、都農町 `tsuno`（高知県津野町と同じ）
- 試算の時間: 月の削減時間×4 を7で割った余りが5（1.25, 3, 4.75, 6.5, … 1.75時間刻み）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| cases | cases.md | 25 |
| gov | gov_ai.md | 20 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 20 |
| companies | companies.json / companies.md | 15 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |

## 状態
- [x] _brief.md・wages.md（2026-11-04）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-miyazaki.md
- [ ] 記事 27本（県1＋市町村26）
- [ ] data/subsidies/miyazaki.yml・areas.yml・build
- [ ] 地域ガイド（九州地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-04 ネットワーク確認（pref.miyazaki.lg.jp・soumu.go.jp とも開けた）。shared.md に slug 4件を push。stats・cases を起動
- cases 25（完了: cases.md。**県内の数値つきは2件だけ、どちらも中小企業の実績ではない**: 宮崎銀行〔宮崎市・大企業、生成AIの稟議書アプリで作成時間95%短縮、一部店舗、IT Leaders 2024-06-13〕・AGRIST〔新富町、自社農場のピーマン 14.3t＝県指標9.6tの1.5倍、養液・環境制御・ロボットを合わせた結果で AI 単独ではない〕。数値なし: 坂下組〔小林市・建設、県の事例集②〕・スマイリング・パーク〔都城市・社福、介護記録の音声入力〕・アルバック機工〔西都市〕。研究中: 牛の顔認証AI（宮崎大学・デンサン・JA宮崎経済連、目標95%）。**使用済み**: 山田第二農場→青森県十和田市、新富町農業研究会→高知県芸西村、川野畜産→山形県尾花沢市、サニー・シーリング→島根県出雲市、霧島酒造→香川県直島町、黒瀬水産→愛媛県愛南町、諸塚村の森林DX→愛媛県久万高原町。機構の成果報告にAIなし。九州全体: 九州財務局「みやざき活性化フォーラム」（宮崎県のみ、アンケート474者））
- gov 起動（WS20）
- stats 5（完了: stats.md・stats_labor.md。コード26件一致（45201〜45443）。**R7国調確定値 1,017,628人（▲4.9%）**、全市町村で減少。15〜64歳は不詳補完値から計算（県▲6.2%）。**県の推計人口は令和7年国調確定値が基準**（2026-10-01 1,005,974人）。製造品出荷額 2024年 19,139.8億円（都城・延岡・宮崎で64.1%）、町村の中分類は県の令和6年調査（2023年実績）で補った（年を混ぜない）。都城市の農業産出額 920.7億円＝全国の市町村で2位（当社で並べた順位）、肉用牛・豚は都城市、ブロイラーは日向市が1位（同）。林業は市町村内総生産の林業の割合（美郷町10.65%・諸塚村10.42%）。観光の市町村別は令和6年まで。**有効求人倍率 1.15倍（2026-09）・就業地別1.22**、7所のうち日向・日南・高鍋は1倍未満、事務0.43・一般事務0.35。最低賃金1,085円（2026-10-24発効）。**TDB宮崎県版4本: 後継者不在率49.9%・社長年齢60.4歳・休廃業576件（全国版577）・生成AI活用27.6%（76社）**。人手不足は県版・九州版なし。地銀の利用率調査なし。**知事 河野俊嗣（令和5年1月21日 4期目就任）**。地域区分は県統計の8地域）
- subsidy 起動（WS20）。**WebSearch 累計 30**
