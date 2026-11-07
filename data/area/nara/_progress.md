# 奈良県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-07。WebSearch はセッションで200回まで（調査は110回までにする。準備で1回使用）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（和歌山・滋賀〔と北海道〕を別のセッションで同時に作っている）。

奈良県だけのファイル（data/area/nara/、docs/area-writing-spec-nara.md、articles/*-area-nara*.md）は自由に作る。`data/subsidies/nara.yml` は areas.yml の奈良県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_kinki/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（39市町村。県コード29）
- 一覧は data/area/nara/_brief.md
- 奈良市 `nara-city`。川西町 `kawanishi-town`（山形県川西町と同じ slug）・川上村 `kawakami`（長野県川上村と同じ slug）は親ページが違う（post.py は親ごとに slug を照合する）。投稿後に別ページか確かめる（area-todo）
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を3で割った余りが0の時間だけ**（0.75, 1.5, 2.25, …の0.75時間刻み）。全県の記事・全県の _calc.py の PLAN と照合する（共有メモ）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 22 |
| gov | gov_ai.md（県・12市・国の出先機関・総務省表の全39行） | 12 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・12市） | 10 |
| choson_a | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（15町） | 8 |
| choson_b | gov_ai_c.md / subsidy_c.yml / subsidy_c_areas.md（12村） | 8 |
| companies | companies.json / companies.md | 10 |
| outside | cases_outside.md / serp.md | 14 |
| cases2 | cases2.md（補充） | 10 |
| 合計 | | 108 |

## 状態
- [x] _brief.md・wages.md・area_uniq.py に nara（2026-11-07）
- [ ] 調査（9担当）
- [ ] 執筆仕様 docs/area-writing-spec-nara.md
- [ ] 記事 40本（県1＋市町村39）
- [ ] data/subsidies/nara.yml・areas.yml・build
- [ ] 地域ガイド（近畿の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック（check_article・area_uniq・_calc.py・試算の結果表・書いてはいけない局名）
- [ ] main に push（投稿・デプロイはユーザーが Mac で「投稿して」）

## 実績メモ
- 2026-11-07 ネットワーク確認（pref.nara.lg.jp・soumu.go.jp とも開けた）。ローカルが detached だったので main を origin/main に合わせた
- stats（WS14）・cases（WS22）起動
- cases 22（完了: cases.md。**県内の数値つきAI事例4件は4件とも他県で使用済み**: アイニコグループ（奈良市→福島5本）・史明会 特養Lino（奈良市→徳島）・ワキ製薬（大和高田市→香川。法人番号で大和高田市本郷町）・JAならけん西吉野柿部会（五條市→愛媛）。未使用の数値つきはAIの効果と書けない2件（大峰堂薬品工業 入力約8割削減はAIの記述なし、赤松ハウス柿 約27%は栽培管理システム）。関経連の事例集 PDF 78本（pymupdf）・奈良新聞の県内プレスリリース3,360件を調べた。**県の産業振興総合センターは 2026-04-01 から「奈良県工業振興センター」**（gov で確かめる）。www.pref.nara.jp の PDF は 403。共有メモに関経連の事例集・和歌山/滋賀の候補を書いた）
- gov（WS12）起動
