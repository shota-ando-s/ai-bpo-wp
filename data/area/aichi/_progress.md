# 愛知県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-11。WebSearch はセッションで200回まで（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」）。サブエージェントの同時起動は2人まで。

**同時に静岡・三重・京都を別々のセッションで作っている**（北海道も作成中のことがある）。共有メモは `data/area/_tokai/shared.md`。愛知県だけのファイル（data/area/aichi/、docs/area-writing-spec-aichi.md、articles/*-area-aichi*.md）は自由に作る。`data/subsidies/aichi.yml` は areas.yml の愛知県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_tokai/shared.md）は直す直前に `git pull --rebase origin main`。書きかけの記事は main に入れない（post_changed.py が公開する）。

## 市町村と slug（54市町村＝38市14町2村。県コード23）
- 一覧は data/area/aichi/_brief.md
- 名古屋市は1ページ（区のページは作らない）
- 他県とぶつかる slug: 津島市 `tsushima-city`・江南市 `konan-city`・東海市 `tokai-city`・高浜市 `takahama-city`・みよし市 `miyoshi-city`・あま市 `ama-city`・美浜町 `mihama-town-aichi`（共有メモに書いた）
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を4で割った余りが1の時間だけ**（◯.25時間）。全県の記事・全県の _calc.py の PLAN と照合する（共有メモ）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 22 |
| gov | gov_ai.md（県・国の出先機関・総務省表の全54行・尾張/名古屋の市） | 12 |
| gov_b | gov_ai_b.md（知多・西三河・東三河の市） | 8 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・38市） | 10 |
| choson | gov_ai_c.md / subsidy_c.yml / subsidy_c_areas.md（14町2村） | 8 |
| companies | companies.json / companies.md | 10 |
| outside | cases_outside.md / serp.md | 14 |
| cases2 | cases2.md（補充） | 10 |
| 合計 | | 108 |

## 状態
- [x] _brief.md・wages.md・area_uniq.py に aichi・共有メモに slug（2026-11-11）
- [ ] 調査（9担当）
- [ ] 試算の PLAN（_calc.py）を push
- [ ] 執筆仕様 docs/area-writing-spec-aichi.md
- [ ] 記事 55本（県1＋市町村54）
- [ ] data/subsidies/aichi.yml・areas.yml・build
- [ ] 地域ガイド・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック（check_article・area_uniq・_calc.py・試算の結果表・書いてはいけない局名）
- [ ] main に push（投稿・デプロイはユーザーが Mac で「投稿して」）

## 実績メモ
- 2026-11-11 ネットワーク確認（pref.aichi.jp・soumu.go.jp とも WebFetch で開けた）。WebSearch 0回
- stats（WS14）・cases（WS22）起動
- 国のデジタル化・AI導入補助金 7次締切は 2026-12-01（火）17:00、交付決定 2027-01-19 予定（事務局 https://it-shien.smrj.go.jp/schedule/ を 2026-11-11 に WebFetch で確認）
