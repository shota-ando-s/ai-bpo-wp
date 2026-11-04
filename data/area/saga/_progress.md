# 佐賀県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-04。WebSearch はセッションで200回まで（調査は110回までにする）。サブエージェントの同時起動は2人まで（九州7県を同時に作っている）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

佐賀県だけのファイル（data/area/saga/、docs/area-writing-spec-saga.md、articles/*-area-saga*.md、data/subsidies/saga.yml）は自由に作る。`data/subsidies/saga.yml` は areas.yml の佐賀県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area-todo.md、area-new-prefecture.md、memory、subsidies.json、data/area/_kyushu/shared.md）は直す直前に `git pull --rebase origin main`。他県の行は消さない。force push はしない。書きかけの記事は main に入れない。

## 市町と slug（20市町。県コード41）
- 一覧は data/area/saga/_brief.md
- 佐賀市 `saga-city`、大町町 `omachi-town`（長野県大町市 `omachi`）、白石町 `shiroishi-town`（宮城県白石市 `shiroishi`）、鹿島市 `kashima`（熊本県嘉島町に注意）。九州の共有メモの slug に書いた（push 済み）
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を7で割った余りが1の時間だけ**（0.25, 2, 3.75, 5.5, … 1.75時間刻み）。既存の全県の記事・全県の _calc.py の PLAN（九州の他県は push されていれば）と照合
- scripts/area_uniq.py の県の選択肢に saga を足した（push 済み 9536963）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| cases | cases.md | 30 |
| gov | gov_ai.md | 20 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 20 |
| companies | companies.json / companies.md | 12 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |
| 合計 | | 109 |

## 状態
- [x] _brief.md・wages.md（2026-11-04）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-saga.md
- [ ] 記事 21本（県1＋市町20）
- [ ] data/subsidies/saga.yml・areas.yml・build
- [ ] 地域ガイド（九州地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-04 ネットワーク確認（pref.saga.lg.jp・soumu.go.jp とも開けた）。市町一覧は県の資料（検索1回）で10市10町。stats・cases を起動
- cases 29（完了: cases.md。数値つきは3市町だけ: **ビープラスト**〔佐賀市、生成AIで「コンテンツ制作時間 約60％削減」、佐賀市「DX推進支援事業 事例紹介資料」R8-02 p.21、測り方は不明。同じページの約90%は Teams 電話で AI ではない〕・**セイブ**〔有田町、碍子、検査 40秒/個→19秒・検出率100%、県 H30 実証の報告〔2019-01の5日間〕。報告はAIと書かず、AIは社長のインタビューだけ〕・**アシス**〔多久市、AIカメラのレジ、2人→1人は計画、結果は店長の「1人で十分」だけ〕。数値なし: まるきん・東方会〔伊万里市〕・山口産業〔多久市〕・レグナテック・佐賀玉屋〔佐賀市〕・山本農園〔太良町、テストのみ〕・九動〔鳥栖市、計画〕・森鉄工〔鹿島市、構築中〕・井上製麺〔神埼市、デモ〕。県の実証（2017〜21）。中野建設の1,400時間は RPA。事例なし: 小城・嬉野・武雄・基山・上峰・みやき・玄海・大町・江北。主な出典は佐賀県産業スマート化センター（saga-smart.jp/column/、106本）・佐賀市事例集・県の実証報告書20本。九州経産局のサイトは 403）
- gov 起動（WS20。手がかり: みやき町×オプティム 2018・佐賀市の生成AI相談の実証・吉野ヶ里町×ロケモ 2020）
- 申し送り: stats へ 佐賀新聞社の県内企業アンケート（2026-09-10、69社、82.6%）。subsidy へ 佐賀市デジタル技術導入補助・県のフラッグシップ事業・DXアクセラレータ事業。companies へ オプティム・木村情報技術・SDCソリューションズ・福博印刷・BottoK
