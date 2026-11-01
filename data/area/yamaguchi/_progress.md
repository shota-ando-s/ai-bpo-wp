# 山口県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の「feat(area): 鳥取県の県ページ」〔6bf32a4〕の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-01。新しいセッションなので WebSearch の残りは200回（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

**同じ main に鳥取県のセッションが書いている（山梨県・島根県は作成済み）。** 山口県だけのファイル（data/area/yamaguchi/、docs/area-writing-spec-yamaguchi.md、articles/*-area-yamaguchi*.md、data/subsidies/yamaguchi.yml）は自由に作る。`data/subsidies/yamaguchi.yml` は areas.yml の山口県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json）は最後に `git pull --rebase origin main` してから直す。衝突したら両方の追加を残し、subsidies.json は build し直す。force push はしない。

## 市町と slug（19市町。県コード35）
- 一覧は data/area/yamaguchi/_brief.md
- 山口市は `yamaguchi-city`（青森市 aomori-city と同じ形）。既存609本の slug と照合して衝突なし
- 試算は「月の削減時間・時間換算額」だけの形。山梨・島根・鳥取の _calc.py の PLAN と照合する
- scripts/area_uniq.py の県の選択肢に yamaguchi を足した（執筆前に。コミットは共通ファイルと一緒に最後）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| gov | gov_ai.md | 20 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 20 |
| cases | cases.md | 28 |
| companies | companies.json / companies.md | 12 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |
| 合計 | | 107 |

## 状態
- [x] _brief.md・wages.md（2026-11-01）
- [ ] 調査（6担当）
- [ ] 執筆仕様 docs/area-writing-spec-yamaguchi.md
- [ ] 記事 20本（県1＋市町19）
- [ ] data/subsidies/yamaguchi.yml・areas.yml・build
- [ ] 地域ガイド（中国地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-01 ネットワーク確認（pref.yamaguchi.lg.jp・soumu.go.jp とも開けた）。HEAD が detached だったので main を origin/main に合わせた。調査4人を起動（stats・gov・subsidy・cases）
