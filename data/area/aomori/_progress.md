# 青森県 地域ページ 作業状態（再開用）

ブランチ: area-aomori（origin/main 3287697 から）。日付 2026-10-17。

## WebSearch の配分（上限200）
- 調査: stats_a 15 / stats_b 20 / gov_a 20 / gov_b 20 / subsidy_a 18 / subsidy_b 18 / companies 12 / cases 20 / cases_outside 18 / serp 5 = 166（上限の配分。実績は各担当の報告で更新）
- 残り（執筆・確認）: 34

## 状態
- [x] scripts/area_uniq.py に aomori を追加
- [x] 調査（data/area/aomori/）: stats.md, stats_labor.md, wages.md, gov_ai.md, gov_ai_b.md, subsidy_a.yml, subsidy_a_areas.md, subsidy_b.yml, subsidy_b_areas.md, companies.json, companies.md, cases.md, cases_outside.md, serp.md
- [x] 執筆仕様 docs/area-writing-spec-aomori.md
- [ ] 記事 41本
- [ ] data/subsidies/aomori.yml、areas.yml、build_shindan_data.py
- [ ] 地域ガイド、area-todo.md、area-new-prefecture.md
- [ ] チェック（check_article / extract_claims / area_uniq）
- [ ] コミット・push
- 実績: serp 5 / cases 20
- 実績: stats_a 4 / gov_b 10 / subsidy_a 17
- 実績: stats_b 11 / gov_a 16 / cases_outside 18 / companies 8 / cases2 ≤15 起動
- 実績: subsidy_b 8（調査合計 117 + cases2）
- WebSearch 調査合計 132（serp5 cases20 stats_a4 gov_b10 subsidy_a17 stats_b11 gov_a16 cases_outside18 companies8 subsidy_b8 cases2 15）。執筆は担当ごと2回まで（11担当で最大22）
