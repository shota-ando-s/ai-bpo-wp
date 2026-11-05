# 北海道 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。WebSearch はセッションで200回まで。**残りが30回を切ったら区切る**。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（茨城・栃木・群馬・沖縄を別のセッションで同時に作っている。アカウントの7日間の利用上限が警告の状態）。共有メモは `data/area/_batch5/shared.md`。

北海道だけのファイル（data/area/hokkaido/、docs/area-writing-spec-hokkaido.md、articles/*-area-hokkaido*.md）は自由に作る。`data/subsidies/hokkaido.yml` は areas.yml の北海道の行と同じコミットで push する（振興局ごとに足すなら、そのつど一緒に）。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_batch5/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 段階（179市町村＝35市129町15村、14振興局。一覧と slug は _brief.md）

| 段階 | 範囲 | 状態 |
|---|---|---|
| 1 | 道全体の調査・道のページ・石狩振興局（8） | 作業中（2026-11-05） |
| 2〜 | 残りの13振興局（171） | 未着手 |

残りの振興局の順番（案。人口の多い局から）: 胆振（11）→ 渡島（11）→ 上川（23）→ 十勝（19）→ 空知（24）→ 後志（20）→ オホーツク（18）→ 釧路（8）→ 日高（7）→ 根室（5）→ 檜山（7）→ 宗谷（10）→ 留萌（8）

## 試算の割り当て
月の削減時間×4 を5で割った余りが **0**（＝1.25時間の倍数）の時間だけ（共有メモの表）。全県の記事・全県の `_calc.py` の PLAN と照合する（`python3 data/area/hokkaido/_calc.py`）。

## 実績メモ
- 2026-11-05 ネットワーク確認（pref.hokkaido.lg.jp・soumu.go.jp とも開けた）。ローカルの main が detached だったので origin/main に合わせ直した。_brief.md（179市町村・14振興局・コード・slug 案）。栃木県那珂川町が `nakagawa-town` を先に使ったので、中川町は `nakagawa-town-hokkaido`。共有メモに slug を push
- stats（WS15）・govsub（WS18）起動。WebSearch 累計 1（親）
