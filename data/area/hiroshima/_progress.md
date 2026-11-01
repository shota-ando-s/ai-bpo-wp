# 広島県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の「feat(area): 鳥取県の県ページ」〔6bf32a4〕の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-01。新しいセッションなので WebSearch の残りは200回（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

**同じ main に山口県のセッションが書いている（山梨・島根・鳥取は作成済み）。** 広島県だけのファイル（data/area/hiroshima/、docs/area-writing-spec-hiroshima.md、articles/*-area-hiroshima*.md、data/subsidies/hiroshima.yml）は自由に作る。`data/subsidies/hiroshima.yml` は areas.yml の広島県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json）は最後に `git pull --rebase origin main` してから直す。衝突したら両方の追加を残し、subsidies.json は build し直す。force push はしない。

## 市町と slug（23市町。県コード34）
- 一覧は data/area/hiroshima/_brief.md
- 府中市 `fuchu-city`・府中町 `fuchu-town`、広島市 `hiroshima-city`（区のページは作らない）
- 他県と同じ slug: 三原市 mihara（高知県三原村）・三次市 miyoshi（徳島県三好市）。投稿後に確かめる項目を area-todo に残す
- 試算は「月の削減時間・時間換算額」だけの形。山梨・島根・鳥取（と push されていれば山口）の _calc.py の PLAN と照合する
- scripts/area_uniq.py の県の選択肢に hiroshima を足した（未コミット。共通ファイルと一緒にコミット）

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
- [x] _brief.md・wages.md（2026-11-01）
- [ ] 調査（6担当）
- [ ] 執筆仕様 docs/area-writing-spec-hiroshima.md
- [ ] 記事 24本（県1＋市町23）
- [ ] data/subsidies/hiroshima.yml・areas.yml・build
- [ ] 地域ガイド（中国地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-01 ネットワーク確認（pref.hiroshima.lg.jp・soumu.go.jp とも開けた）。調査4人を起動（stats・gov・subsidy・cases）
