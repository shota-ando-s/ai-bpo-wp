# 鹿児島県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-04。WebSearch はセッションで200回まで（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（九州7県を同時に作っている）。

鹿児島県だけのファイル（data/area/kagoshima/、docs/area-writing-spec-kagoshima.md、articles/*-area-kagoshima*.md）は自由に作る。`data/subsidies/kagoshima.yml` は areas.yml の鹿児島県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_kyushu/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（43市町村。県コード46）
- 一覧は data/area/kagoshima/_brief.md
- 鹿児島市 `kagoshima-city`、大崎町 `osaki-town`、瀬戸内町 `setouchi-town`、大和村 `yamato-village`、十島村 `toshima-village`、三島村 `mishima-village`
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を7で割った余りが6の時間だけ**。全県の記事・全県の _calc.py の PLAN（九州の他県を含む）と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 25 |
| gov | gov_ai.md（県・19市・国の出先機関・総務省表の全43行） | 14 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・19市） | 12 |
| choson | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（20町4村） | 14 |
| companies | companies.json / companies.md | 12 |
| outside | cases_outside.md / serp.md | 15 |
| 合計 | | 106 |

## 状態
- [x] _brief.md・wages.md（2026-11-04）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-kagoshima.md
- [ ] 記事 44本（県1＋市町村43）
- [ ] data/subsidies/kagoshima.yml・areas.yml・build
- [ ] 地域ガイド（九州地方の段）・area_uniq.py・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-04 ネットワーク確認（pref.kagoshima.jp・soumu.go.jp とも開けた）。ローカルの main が古い履歴のまま detached だったので、origin/main に合わせ直した。共有メモに slug を push
- cases 25（完了: cases.md 281行。**事業者自身が実績で公表した県内のAI事例は0件**。数値つき: 轟木税理士事務所〔2名、AI自動仕訳で入力作業50%減・自己申告、県のDX事例集、**所在の市町村が不明**〕・鹿児島堀口製茶〔志布志市、AIの葉期判定 巡回21分→11分は農研機構の実証の試算。33%・56%はAIではない〕。数値なし: 鹿児島市（JA鹿児島県中央会の生成AI実証 2026-10-28開始・現場サポート126名・フタマタ開発〔日経の要約だけ〕）、霧島市（キリシマ精工53名、AIスケジューラー、情報KISC）、曽於市（子牛の疾病予兆AIの研究・Eco-Pork）、大崎町（ジャパンファーム、ベンダー発表）。使用済み: 薩摩酒造（枕崎市→長野県伊那市）・うしの中山（鹿屋市→青森県七戸町）。九州経産局は403。照合: 轟木の所在（companies）、鹿児島銀行・九州経済研究所の AI 調査（stats）、薩摩川内市のAIデータセンター（gov）。赤潮AI予報は長崎の会社なので使わない。**税理士法人さくら優和パートナーズは熊本が使う（鹿児島で使わない）**）
- 共有メモに九州経産局の3資料・農研機構・鹿児島堀口製茶の割り当てを追加。**「南九州財務局」はない**（九州財務局〔熊本市〕が鹿児島財務事務所を所管、大分のセッションが確認）→ _brief.md を直した
- gov（WS14）起動
