# 福島県 地域ページ 作業状態（再開用）

ブランチ: area-fukushima（main の「docs(area): 山形県の WebSearch の回数を直す」の次から）。作業ツリーは `.claude/worktrees/area-fukushima/`（main では山形県の投稿が並行して動いていたため、ブランチを切り替えずに別の作業ツリーにした）。東北で最後の県。59市町村で、これまでで最も多い。ファイル名の日付と本文の確認日は 2026-10-24。

## 市町村と slug（59市町村。県コード07）
- 一覧は data/area/fukushima/_brief.md
- 政令市はない。福島市は fukushima-city。金山町 kaneyama-town・三島町 mishima-town・昭和村 showa-village・富岡町 tomioka-town・石川町 ishikawa-town・小野町 ono-town（他県に同名・紛らわしい自治体がある）
- 試算は山形県と同じ「月の削減時間・時間換算額」だけの形（ヒキツギAIの月額・回収期間は書かない）

## 調査の分担と WebSearch の配分（上限200）
| 担当 | 書くファイル | 対象 | WebSearch |
|---|---|---|---|
| stats_a | stats.md | 人口（社人研。福島県の市町村別推計の有無）・住民登録と居住人口・経済センサス・製造業（経済構造実態調査）・農林漁業（東北農政局の市町村別農業産出額）・主要産業の候補・県の地域区分 | 12 |
| stats_b | stats_labor.md | 福島労働局の有効求人倍率（HW別・職業別・管轄）、TDB福島支店の県版（なければ東北版・全国版）、県内企業のAI利用の調査、観光 | 12 |
| gov_a | gov_ai.md | 総務省の生成AI・AI導入調査の県と59市町村の表、県と13市、県内の商工会議所・商工会の一覧 | 14 |
| gov_b | gov_ai_b.md | 県北・県中・県南の町村（桑折・国見・川俣・大玉・鏡石・天栄・石川・玉川・平田・浅川・古殿・三春・小野・西郷・泉崎・中島・矢吹・棚倉・矢祭・塙・鮫川）21町村 | 12 |
| gov_c | gov_ai_c.md | 会津・南会津の町村（下郷・檜枝岐・只見・南会津・北塩原・西会津・磐梯・猪苗代・会津坂下・湯川・柳津・三島・金山・昭和・会津美里）15町村 | 10 |
| gov_d | gov_ai_d.md | 相双の町村（広野・楢葉・富岡・川内・大熊・双葉・浪江・葛尾・新地・飯舘）10町村。避難指示の解除・役場の所在地・居住人口の事実も | 10 |
| subsidy_a | subsidy_a.yml / subsidy_a_areas.md | 県・県域の機関（福島県産業振興センターなど）・イノベーション・コースト構想関連と13市 | 14 |
| subsidy_b | subsidy_b.yml / subsidy_b_areas.md | 県北・県中・県南の21町村 | 10 |
| subsidy_c | subsidy_c.yml / subsidy_c_areas.md | 会津・南会津の15町村と相双の10町村 | 12 |
| companies | companies.json / companies.md | 59市町村に本社があるシステム開発・Web開発の会社（公式サイトの従業員数順に5社まで） | 16 |
| cases | cases.md | 県内企業のAI事例 | 18 |
| cases_outside | cases_outside.md | 同じ業種の県外の中小企業の事例。data/area/ の各県の cases_outside.md・cases.md と articles/*area*.md に出る事例は使わない | 14 |
| serp | serp.md | 「福島県 AI導入」「郡山市 AI導入」などの検索結果・競合・FAQ候補 | 5 |
| 合計 | | | 159（残り41を執筆と確認に） |

## 進め方（宮城・山形で分かったこと）
- 調査担当は同時に6人まで。1人終わるごとに次を起動する
- 執筆担当は同時に4人まで。1人終わるごとに次を起動する
- コミットは書き終えた担当のファイルだけを git add する（ワイルドカードで足さない）
- 執筆担当への依頼に「書き終わったページの試算の表を見て、時間・金額が同じにならないよう前提を変える」「お手本は形だけを見る。文は写さない」「仕様が名指ししたページ以外では、他県で詳述した企業に触れない」と書く
- 投稿後、地図の自動判定（scripts/fix_map_images.py）に加えて、全画像を一覧にして目で確かめる
- 画像生成のモデルは gpt-image-1.5

## 状態
- [x] ブランチ area-fukushima、data/area/fukushima/_brief.md・wages.md、scripts/area_uniq.py に fukushima を追加（2026-10-24）
- [ ] 調査（data/area/fukushima/。担当13人）
- [ ] 執筆仕様 docs/area-writing-spec-fukushima.md
- [ ] 記事 60本（県1＋市町村59）
- [ ] data/subsidies/fukushima.yml、areas.yml、build_shindan_data.py
- [ ] 地域ガイド、area-todo.md、area-new-prefecture.md
- [ ] チェック（check_article・area_uniq・試算の重なり）
- [ ] main へのマージ・投稿・デプロイ・画像の確認

## 実績メモ
