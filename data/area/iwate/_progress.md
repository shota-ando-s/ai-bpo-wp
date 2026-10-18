# 岩手県 地域ページ 作業状態（再開用）

ブランチ: area-iwate（origin/main 52ea55f から）。ファイル名の日付 2026-10-18。本文の確認日 2026年10月18日。

## WebSearch の配分（上限200）
- 調査: stats_a 15 / stats_b 15 / gov_a 20 / gov_b 18 / subsidy_a 16 / subsidy_b 16 / companies 12 / cases 20 / cases_outside 18 / serp 5 = 155
- 残り（執筆・確認）: 45（執筆担当ごとに2回まで＋親）

## 状態
- [x] data/area/iwate/wages.md（青森版の全国値をコピー）
- [x] scripts/area_uniq.py に iwate を追加（glob を日付非依存に。aomori で動作確認）
- [x] 調査（data/area/iwate/）: stats.md, stats_labor.md, gov_ai.md, gov_ai_b.md, subsidy_a.yml, subsidy_a_areas.md, subsidy_b.yml, subsidy_b_areas.md, companies.json, companies.md, cases.md, cases_outside.md, serp.md
- [x] 執筆仕様 docs/area-writing-spec-iwate.md
- [x] 記事 34本（県1＋市町村33）
- [x] data/subsidies/iwate.yml（46制度）、areas.yml、build_shindan_data.py
- [x] 地域ガイド（commit済）、[x] area-todo.md
- [x] チェック（全34ページ check_article・extract_claims --check-links ERROR 0、area_uniq 固有64.4%以上）
- [ ] コミット・push（area-iwate）

## 実績メモ
- serp 5（完了: serp.md。競合 uravation.com 等あり、県の賃上げ補助金2.0・北上市のものづくり補助・5者の生成AI連携協定・洋野町の養鶏AI実証が候補。すべて未照合）
- 調査担当 stats_a/stats_b/gov_a/gov_b/subsidy_a/subsidy_b/companies/cases/cases_outside はバックグラウンドで実行中に親セッションが中断。未完了のファイルは担当を再起動して作る
- cases 20（完了: 県内の企業事例は盛岡市の4件だけ〔岩手銀行×2・北日本銀行と龍澤学館・タヤマスタジオ〕。他地域・他業種は見つからず）
- stats_a 5（完了: stats.md。岩手町のコードは03303〔03302は葛巻町〕。広域振興局4つは現存〔2026-04-01組織図〕）
- gov_a 20（完了: gov_ai.md。生成AI 導入済14・実証中4・掲載なし15。5者協定は二次情報のみ）
- subsidy_b 10（完了: 32制度 official。ソフト等が対象: 山田町 省力化対策支援〔国の補助金の1/5上乗せ・60万円〕、葛巻町 電子化推進、大槌町 DX推進〔水産加工業者〕）
- stats_b 13（完了: 県1.21倍〔2026年8月季調〕、休廃業511件、後継者不在率50.0%は東北版の表の県の値、社長62.5歳全国2位、中分類の有効求人倍率あり〔一般事務0.24〕。県の企業AI利用調査はなし）
- cases_outside 18（完了: 本文用16件＋予備5件。電子部品・半導体・わかめ/かき養殖・定置網・林業・スキー場は見つからず）
- subsidy_a 9（完了: 14制度 official。受付中5〔花巻×2・遠野・一関・奥州〕。県の賃上げ補助金2.0 デジタル活用枠は1/2・100万円で9/30終了。北上市は10/13予算到達で受付終了。県の上乗せ制度なし）
- companies 7（完了: 30社。盛岡13・滝沢5・北上4・一関3・大船渡3・奥州2・釜石1・二戸1・紫波1。他24市町村はなし）
- gov_b 16（完了: gov_ai_b.md）
- WebSearch 調査合計 123（serp5 cases20 stats_a5 gov_a20 subsidy_b10 stats_b13 cases_outside18 subsidy_a9 companies7 gov_b16）。残り77
- 執筆開始: W1 盛岡・滝沢／W2 八幡平・雫石・紫波・矢巾／W3 二戸・一戸・葛巻・岩手町／W4 久慈・洋野・軽米・九戸／W5 岩泉・田野畑・普代・野田／W6 宮古・釜石・山田・大槌／W7 大船渡・陸前高田・遠野・住田／W8 北上・花巻・西和賀／W9 一関・奥州・金ケ崎・平泉／W10 県ページ（各WebSearch 2回まで）
- 13:48 利用上限で執筆担当が全員停止。21本できた（未着手: yahaba kuzumaki iwate-town karumai kunohe fudai noda yamada otsuchi sumita tono kanegasaki hiraizumi）。WIPコミットして担当を再開
- W10 県ページ完了（17,064字、ERROR 0、WS0）／W1 盛岡10,787字・滝沢8,687字 完了（ERROR 0、WS0）
- W8（北上・花巻・西和賀）・W2（八幡平・雫石・紫波・矢巾）・W7（大船渡・陸前高田・遠野・住田、WS2）・W5（岩泉・田野畑・普代・野田）完了。残りW3・W4・W6・W9
- 全34ページ執筆完了（W3・W4〔WS1〕・W6・W9〔WS2〕）。WebSearch 合計128（調査123＋W7 2＋W9 2＋W4 1、親0）
- 2026-10-18: 仕上げ（市町→市町村の表記修正3か所、area-todo.md・area-new-prefecture.md 更新）。origin/main を取り込んで push
