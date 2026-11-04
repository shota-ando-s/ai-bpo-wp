# 大分県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-04。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**九州7県を別々のセッションで同時に作っている**（共有メモ data/area/_kyushu/shared.md）。サブエージェントの同時起動は2人まで。

大分県だけのファイル（data/area/oita/、docs/area-writing-spec-oita.md、articles/*-area-oita*.md、data/subsidies/oita.yml）は自由に作る。`data/subsidies/oita.yml` は areas.yml の大分県の行と同じコミットで push する。共通ファイルは直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（18市町村。県コード44）
- 一覧は data/area/oita/_brief.md。大分市 `oita-city`
- 試算は data/area/oita/_calc.py（九州の割り当て: 月の削減時間×4 を7で割った余り4）

## 状態
- [x] _brief.md（2026-11-04）、area_uniq.py に oita を追加、共有メモに管轄の行
- [x] 調査（stats・cases・gov・subsidy・companies/serp・cases_outside・cases2）
- [x] 試算の PLAN（push 済み）
- [x] 執筆仕様 docs/area-writing-spec-oita.md
- [x] 記事 19本（県1＋市町村18）
- [x] data/subsidies/oita.yml・areas.yml・build
- [x] 地域ガイド（九州地方の段）・area-todo.md・area-new-prefecture.md・memory
- [x] チェック・main に push

## 実績メモ
- WebSearch: cases 24・stats 9・gov 19・subsidy 5・companies/serp 14・cases2 10・cases_outside 21＝102回
- 事業者自身がAIの効果を数値で公表した県内の中小企業の事例は0件。県外の未使用の数値つきは4件（古屋旅館→別府市、但馬屋→由布市、マキフーズ→豊後大野市、ホリエ→中津市）
- 財務局は九州財務局 大分財務事務所（「南九州財務局」はない）
- 執筆: W1〜W6（各3ページ）・W7（県ページ）。WebSearch 0回。check_article 19ページ ERROR 0、area_uniq 70.4〜97.1%、試算の結果表は18ページとも2行・PLAN と一致、_calc.py OK（佐賀・長崎・宮崎の PLAN とも重ならない。福岡は PLAN が空、熊本・鹿児島はまだない）
- 県ページの地域区分は6振興局（W7 が県の各振興局のページで管轄を確かめた。北部は観光・税制の欄の記述から読み取り）
- 親が直した点: 九重町の「町のサイトにも案内がある」（開いていない）を削除、大分市の他県の会社名の注記を削除
- 補助金診断: data/subsidies/oita.yml と areas.yml を同じコミットで入れ build（779制度）
