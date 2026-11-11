# 静岡県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-11。WebSearch はセッション全体で200回まで（調査は120回までにする）。サブエージェントの同時起動は2人まで。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

同時に愛知・三重・京都・兵庫（と北海道）を別のセッションで作っている。共有メモは `data/area/_tokai/shared.md`。試算は「月の削減時間×4 を4で割った余りが0」＝ちょうどの時間だけを使う。

## 市町と slug（35市町。県コード22）
- 一覧は data/area/shizuoka/_brief.md。静岡市 `shizuoka-city`・小山町 `oyama-town`・森町 `mori-town-shizuoka`・清水町 `shimizu-town-shizuoka`

## 進み具合
- 2026-11-11: ネットワーク確認（県・総務省とも開けた）、_brief.md・wages.md・area_uniq.py に shizuoka・共有メモに slug を push
- 調査: stats・cases を起動（WebSearch 各25回まで）
- _calc.py を nara から作った（PLAN は stats の結果で決める）。2026-11-11 時点で、ちょうどの時間の空きはほとんど月300時間以上（医療・福祉 199/229/239/257/271h、卸 197h、運輸 199/211h、建設 229/233/257h、不動産 71/166h、情報通信 197/223h など）
- cases 完了（WebSearch 23回）・stats 完了（5回）。gov（15回まで）・subsidy（15回まで）を起動
- PLAN を決めて push（a771c47）。_assign.py で規模の小さい順に当てた。月166〜372時間・約62.9〜127.4万円・42〜180名。町でも月318時間以上（1人の月の業務量が40時間を超えるページ: 川根本町44・小山町40.75・西伊豆町40.25・東伊豆町41.5 など）。熱海市の STAT（不動産業の中分類の従業者）は未確認
- 残りの調査: choson（12町）・companies・outside/serp・cases2
