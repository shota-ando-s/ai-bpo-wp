# 神奈川県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-12。WebSearch はセッション全体で200回まで（調査は120回までにする）。サブエージェントの同時起動は2人まで。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

同時に埼玉・千葉（と北海道の続き）を別のセッションで作っている。共有メモは `data/area/_shutoken/shared.md`。試算は他県との重なりを許容し、神奈川県の中だけ時間・金額・規模を重ねない（2026-11-11 ユーザー決定）。

## 市町村と slug（33市町村。県コード14）
- 一覧は data/area/kanagawa/_brief.md。**既存ページ2つはファイル名・slug・parent を変えない**: 県 `articles/2026-10-14-area-kanagawa.md`（slug `kanagawa`、parent `area`）、横浜市 `articles/2026-10-17-area-yokohama.md`（slug `yokohama`、parent `area/kanagawa`）。新しい31ページは `articles/2026-11-12-area-kanagawa-<slug>.md`
- 大和市 `yamato-city`（熊本県山都町 `yamato`、鹿児島県大和村 `yamato-village` と分ける）、川崎市 `kawasaki`（宮城・福岡の川崎町は `kawasaki-town`）
- scripts/area_uniq.py に kanagawa を足した（横浜市の旧ファイル名も拾う）

## 進み具合
- 2026-11-12: ネットワーク確認（県・総務省とも開けた）、_brief.md・area_uniq.py・共有メモに slug
- 調査: stats（4回）完了・cases（25回まで）・gov（15回まで）を起動
- 試算の PLAN を決めた（_calc.py、表は _plan_table.md）。33ページで月30〜107.25時間・約9.4〜44.7万円・12〜70名。神奈川の中だけ重ねない（他県とは参考表示）
- cases 完了（18回）。数値つきで未使用は5件（ガレージカメイ・コイワイ・インフォマティクス・RAMXEED・横浜綜合法律事務所）。subsidy（15回まで）を起動
- **次にやること**: gov（県・19市・総務省表・国の出先・リンク条件）・subsidy（県・19市）→ choson（13町1村の行政＋補助金）・companies → outside/serp・cases2。そのあと _calc.py の PLAN、仕様、執筆

## 再開するとき
1. `git pull origin main`、この _progress.md の「次にやること」から
2. 調査担当が止まっていたら SendMessage で再開を頼む（ファイルは節ごとに書き足してある）
