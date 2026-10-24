# 富山県 地域ページ 作業状態（再開用）

ブランチ: area-toyama（main の「docs(area): 福島県の投稿とデプロイ、画像の確認を記録」の次から）。作業ツリーは `.claude/worktrees/area-toyama/`（main の作業フォルダでは新潟県の作業が area-niigata ブランチで動いているため、別の作業ツリーにした）。北陸で最初の県。**ファイル名の日付と本文の確認日は、調査を始める日にする**（2026-10-25 に準備だけした。準備したセッションは福島で WebSearch を136回使っていたため、調査は新しいセッションで始める）。

## 市町村と slug（15市町村。県コード16）
- 一覧は data/area/toyama/_brief.md
- 政令市はない。富山市は toyama-city。朝日町 asahi-town（山形県・三重県にも同名の町がある）
- 試算は山形県・福島県と同じ「月の削減時間・時間換算額」だけの形（ヒキツギAIの月額・回収期間は書かない）

## 新しいセッションでの始め方
1. このファイルと docs/area-new-prefecture.md（「福島県で分かったこと」まで）を読む
2. 作業はこの作業ツリーで行う（`cd /Users/ando/Dropbox/allsrc/ai-bpo-wp/.claude/worktrees/area-toyama`）。消えていたら `git worktree add .claude/worktrees/area-toyama area-toyama`
3. 下の「調査の分担」の担当を起動する（同時に6人まで、1人終わるごとに次）。各担当への依頼は、data/area/toyama/_brief.md を読ませ、形式は data/area/fukushima/ の同じ名前のファイルに合わせるよう書く（福島の依頼文の要点は data/area/fukushima/_progress.md の実績メモから分かる）
4. 全員の結果を受け取ってファイルに書いてから、執筆仕様（docs/area-writing-spec-fukushima.md をコピー）に進む

## 調査の分担と WebSearch の配分（上限200）
| 担当 | 書くファイル | 対象 | WebSearch |
|---|---|---|---|
| stats_a | stats.md | 人口（社人研）・経済センサス・製造業（経済構造実態調査。中分類・秘匿）・農林漁業（北陸農政局の市町村別農業産出額、漁業センサス）・主要産業の候補・県の地域区分（4広域圏） | 10 |
| stats_b | stats_labor.md | 富山労働局の有効求人倍率（HW別・職業別・管轄）、TDB富山支店の県版（なければ北陸版・全国版）、県内企業のAI利用の調査、観光（立山黒部の定義に注意） | 12 |
| gov_a | gov_ai.md | 総務省の生成AI・AI導入調査の県と15市町村の表、県と10市、県内の商工会議所・商工会の一覧 | 14 |
| gov_b | gov_ai_b.md | 5町村（舟橋・上市・立山・入善・朝日）と、県の企業向けDX・AI支援（富山県新世紀産業機構・ものづくり研究開発センターなど） | 8 |
| subsidy_a | subsidy_a.yml / subsidy_a_areas.md | 県・県域の機関と10市（能登半島地震の支援制度は分けて書く） | 14 |
| subsidy_b | subsidy_b.yml / subsidy_b_areas.md | 5町村 | 6 |
| companies | companies.json / companies.md | 15市町村に本社があるシステム開発・Web開発の会社（公式サイトの従業員数順に5社まで。福島と同じく、公式で本社と従業員数の両方を確かめた会社だけを本表に） | 14 |
| cases | cases.md | 県内企業のAI事例（医薬品・アルミ・化学・金属・電子部品・機械・高岡銅器・ます寿司などの食品・水産〔氷見・魚津・滑川〕・米・チューリップ・地銀〔北陸銀行・富山銀行・富山第一銀行〕） | 18 |
| cases_outside | cases_outside.md | 同じ業種の県外の中小企業の事例。**data/area/ の各県の cases_outside.md・cases.md・cases2.md と articles/*area*.md に出る事例は使わない** | 14 |
| serp | serp.md | 「富山県 AI導入」「富山市 AI導入」「高岡市 AI」などの検索結果・競合・FAQ候補 | 5 |
| 合計 | | | 115（残り85を補充・執筆と確認に） |

## 進め方（宮城・山形・福島で分かったこと）
- 調査担当は同時に6人まで、執筆担当は同時に4人まで。1人終わるごとに次を起動する
- コミットは書き終えた担当のファイルだけを git add する（ワイルドカードで足さない）
- 執筆担当への依頼に「お手本は形だけを見る。文は写さない」「書き終わったページの試算の表を見て時間・金額が同じにならないよう前提を変える」「仕様が名指ししたページ以外では、他県で詳述した企業に触れない」「自分の担当のページ同士でも段落を使い回さない（国の制度の表・相談先の表・試算の説明・FAQも）」と書く
- 書き終わったら全ページで「見出し行だけで中身の行がない表」を探す（福島で4ページあった。check_article では出ない）
- area_uniq.py の全ページ実行は時間がかかる。担当には自分のページだけを指定させる
- 投稿は作業ツリーに .env を symlink して post.py を実行する。main への反映は `git fetch . area-toyama:main`（main の作業フォルダが別のブランチのとき）。地域ガイド・areas.yml・subsidies.json・area-todo.md・area-new-prefecture.md・scripts/area_uniq.py は新潟の作業とも触るので、main を取り込んでから反映する（subsidies.json は build をやり直す）
- 投稿後、地図の自動判定（scripts/fix_map_images.py）に加えて、全画像を一覧にして目で確かめる
- 画像生成のモデルは gpt-image-1.5

## 状態
- [x] ブランチ area-toyama、data/area/toyama/_brief.md・wages.md、scripts/area_uniq.py に toyama を追加（2026-10-25）
- [ ] 調査（data/area/toyama/。担当10人）
- [ ] 執筆仕様 docs/area-writing-spec-toyama.md
- [ ] 記事 16本（県1＋市町村15）
- [ ] data/subsidies/toyama.yml、areas.yml、build_shindan_data.py
- [ ] 地域ガイド、area-todo.md、area-new-prefecture.md
- [ ] チェック（check_article・area_uniq・試算の重なり・見出し行だけの表）
- [ ] main への反映・投稿・デプロイ・画像の確認

## 実績メモ
