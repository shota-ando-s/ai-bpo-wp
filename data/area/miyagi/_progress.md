# 宮城県 地域ページ 作業状態（再開用）

ブランチ: area-miyagi（main 4a7feb0 の次のコミットから）。ファイル名の日付 2026-10-23。本文の確認日 2026年10月23日。東北で4番目の県。

## 市町村と slug（35市町村。県コード04）
- 一覧は data/area/miyagi/_brief.md
- 仙台市は1ページだけ（5区のページは作らない。2026-10-23 ユーザー決定）
- 川崎町は kawasaki-town、美里町は misato-town（他県に同名の自治体がある）

## WebSearch の配分（上限200）
- 調査: stats_a 10 / stats_b 14 / gov_a 14 / gov_b 14 / gov_c 14 / subsidy_a 14 / subsidy_b 12 / companies 14 / cases 18 / cases_outside 16 / serp 5 = 145
- 残り（執筆・確認）: 55

## 状態
- [x] data/area/miyagi/wages.md（秋田版の全国値をコピー）
- [x] scripts/area_uniq.py に miyagi を追加
- [ ] 調査（data/area/miyagi/。担当11人を 2026-10-23 に起動）
- [ ] 執筆仕様 docs/area-writing-spec-miyagi.md
- [ ] 記事 36本（県1＋市町村35）
- [ ] data/subsidies/miyagi.yml、areas.yml、build_shindan_data.py
- [ ] 地域ガイド、area-todo.md
- [ ] チェック（check_article・extract_claims --check-links ERROR 0、area_uniq 固有60%以上）
- [ ] コミット・投稿・デプロイ

## 実績メモ
