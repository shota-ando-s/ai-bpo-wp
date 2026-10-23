# 山形県 地域ページ 作業状態（再開用）

ブランチ: area-yamagata（main の「docs(area): 宮城県の投稿とデプロイを記録」の次から）。東北で5番目の県。**ファイル名の日付と本文の確認日は、調査を始める日にする**（2026-10-24 に準備だけして、調査は新しいセッションで始める。宮城で WebSearch を使い切りかけたため）。

## 市町村と slug（35市町村。県コード06）
- 一覧は data/area/yamagata/_brief.md
- 政令市はない。山形市は yamagata-city。朝日町 asahi-town・金山町 kaneyama-town・川西町 kawanishi-town・小国町 oguni-town（他県に同名の自治体がある）

## 新しいセッションでの始め方
1. このファイルと docs/area-new-prefecture.md（「宮城県で分かったこと」まで）を読む
2. 下の「調査の分担」の11人を同時に起動する。各担当への依頼は、data/area/yamagata/_brief.md を読ませ、形式は data/area/miyagi/ の同じ名前のファイルに合わせるよう書く（宮城の依頼文は data/area/miyagi/_progress.md の実績メモから分かる）
3. 全員の結果を受け取ってファイルに書いてから、執筆仕様（docs/area-writing-spec-miyagi.md をコピー）に進む

## 調査の分担と WebSearch の配分（上限200）
| 担当 | 書くファイル | 対象 | WebSearch |
|---|---|---|---|
| stats_a | stats.md | 人口（社人研）・経済センサス・製造業（2025年経済構造実態調査）・農林漁業（東北農政局の市町村別農業産出額）・主要産業の候補・県の地域区分（村山・最上・置賜・庄内の4地域。総合支庁の管轄を県資料で確認） | 10 |
| stats_b | stats_labor.md | 山形労働局の有効求人倍率（ハローワーク別・職業別・管轄）、TDB山形支店の県版（なければ東北版・全国版）、県内企業のAI利用の調査、観光 | 14 |
| gov_a | gov_ai.md | 総務省の生成AI・AI導入調査の県と35市町村の表、県と6市（山形・米沢・鶴岡・酒田・新庄・寒河江）、県内の商工会議所・商工会の一覧 | 14 |
| gov_b | gov_ai_b.md | 上山・村山・長井・天童・東根・尾花沢・南陽と、村山地方の7町（山辺・中山・河北・西川・朝日・大江・大石田） | 14 |
| gov_c | gov_ai_c.md | 最上地方（金山・最上・舟形・真室川・大蔵・鮭川・戸沢）、置賜地方（高畠・川西・小国・白鷹・飯豊）、庄内地方（三川・庄内・遊佐）の15町村 | 14 |
| subsidy_a | subsidy_a.yml / subsidy_a_areas.md | 県・県域の機関（やまがた産業支援機構など）と13市 | 14 |
| subsidy_b | subsidy_b.yml / subsidy_b_areas.md | 22町村 | 12 |
| companies | companies.json / companies.md | 35市町村に本社があるシステム開発・Web開発の会社（公式サイトの従業員数順に5社まで） | 14 |
| cases | cases.md | 県内企業のAI事例。さくらんぼ・ラ・フランス・米（つや姫）・米沢牛・電子部品・精密機械（米沢・天童・東根・寒河江）・鋳物（山形市）・家具（天童）・繊維（米沢織）・日本酒・温泉旅館（蔵王・銀山・上山・湯野浜）・水産（酒田・鶴岡）・木材（金山）・地銀（山形銀行・荘内銀行・きらやか銀行） | 18 |
| cases_outside | cases_outside.md | 同じ業種の県外の中小企業の事例。**data/area/ の各県の cases_outside.md・cases.md と articles/*area*.md に出る事例は使わない** | 16 |
| serp | serp.md | 「山形県 AI導入」「山形市 AI導入」などの検索結果・競合・FAQ候補 | 5 |
| 合計 | | | 145（残り55を執筆と確認に） |

## 宮城県で分かった進め方（必ず守る）
- 執筆担当は同時に4人まで。1人終わるごとに次を起動する
- コミットは書き終えた担当のファイルだけを git add する（ワイルドカードで足さない）
- 執筆担当への依頼に「書き終わったページの試算の表を見て、時間・金額が同じにならないよう前提を変える」と書く。最後に全ページの試算を並べて確かめる
- 投稿後、地図の自動判定（scripts/fix_map_images.py）に加えて、全画像を一覧にして目で確かめる（宮城では自動判定が0枚でも、地図・位置のピンが2枚あった）
- 画像生成のモデルは gpt-image-1.5（gpt-image-1 は使えなくなった）

## 状態
- [x] ブランチ area-yamagata、data/area/yamagata/_brief.md・wages.md、scripts/area_uniq.py に yamagata を追加（2026-10-24）
- [ ] 調査（11人）
- [ ] 執筆仕様 docs/area-writing-spec-yamagata.md
- [ ] 記事 36本（県1＋市町村35）
- [ ] data/subsidies/yamagata.yml、areas.yml、build_shindan_data.py
- [ ] 地域ガイド、area-todo.md、area-new-prefecture.md
- [ ] チェック（check_article・extract_claims --check-links ERROR 0、area_uniq 固有60%以上、試算の重なり）
- [ ] コミット・投稿・デプロイ・画像の確認

## 実績メモ
