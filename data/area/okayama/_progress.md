# 岡山県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の 0af9416 の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-03。新しいセッションなので WebSearch の残りは200回（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

岡山県だけのファイル（data/area/okayama/、docs/area-writing-spec-okayama.md、articles/*-area-okayama*.md、data/subsidies/okayama.yml）は自由に作る。`data/subsidies/okayama.yml` は areas.yml の岡山県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json）は最後に `git pull --rebase origin main` してから直す。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（27市町村。県コード33）
- 一覧は data/area/okayama/_brief.md
- 岡山市 `okayama-city`（区のページは作らない）、新庄村 `shinjo-village`（山形県新庄市 `shinjo` と区別）
- 試算は「月の削減時間・時間換算額」だけの形。山梨・島根・鳥取・山口・広島の _calc.py の PLAN と照合する
- scripts/area_uniq.py の県の選択肢に okayama を足した（未コミット。共通ファイルと一緒に最後にコミット）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| gov | gov_ai.md | 20 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 20 |
| cases | cases.md | 25 |
| companies | companies.json / companies.md | 15 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |
| 合計 | | 107 |

## 状態
- [x] _brief.md・wages.md（2026-11-03）
- [ ] 調査（6担当）
- [ ] 執筆仕様 docs/area-writing-spec-okayama.md
- [ ] 記事 28本（県1＋市町村27）
- [ ] data/subsidies/okayama.yml・areas.yml・build
- [ ] 地域ガイド（中国地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-03 ネットワーク確認（pref.okayama.jp・soumu.go.jp とも開けた）。調査4人を起動（stats・gov・subsidy・cases）
- cases 25（完了: cases.md。県内の数値つきは岡山市の3社だけで、どれも見込み・自己申告: **水内ゴム**〔岡山市中区、AIカメラの良否判定つき自動圧入装置、1分4.2個→5〜6個「約50％UP」は見込み・装置全体の効果、岡山市のデジタル化・DX事例報告会 2025-11-17、市のIoT・AI等先端技術導入支援補助金〕・**ピコシステム**〔岡山市南区、IT・161名、生成AI研修で週の削減 2.0→約3.0h、受講者の自己申告、デジライズの事例〕・**イタミアート**〔岡山市南区、印刷・上場、「約90%近い業務の効率化が見込めて」、ソウルドアウトのPR〕。数値なし: サンホーム岡山・日笠商事〔津山市〕・トスコ〔県警と協定〕。県の研究開発補助の採択だけ: 協同〔倉敷市、所在は県資料の表記だけ〕・ビジュアルサーボ〔備前市〕・白獅子・ゴフェルテック。安信工業・協電田中工業は AI ではない。使用済み5件は確認済み（久米南町は 2019年度8.7千人→2023年度19.2千人が新しい）。マルイ・エーアンドエスは同名の別会社あり。事例を置けるのは岡山市・津山市・倉敷市・備前市、使用済みだけ笠岡市・久米南町、21市町村は事例なし。財団・県・中国経産局・商工会議所の事例集はウェブになし。岡山市の補助上限 1,000万/750万 の違いは subsidy で確認）
- companies 起動（WS15）
