# 群馬県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の 31f0f02「docs(area): 北海道・北関東3県・沖縄の同時作成のための共有メモ」の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-05。WebSearch はセッション全体で200回まで（調査は120回までにする）。サブエージェントの同時起動は2人まで。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

同時に茨城・栃木・北海道・沖縄を別のセッションで作っている。共有メモは `data/area/_batch5/shared.md`。試算は「月の削減時間×4 を5で割った余りが3」の時間だけを使う。

## 市町村と slug（35市町村。県コード10）
- 一覧は data/area/gunma/_brief.md
- 高山村 `takayama-village-gunma`・昭和村 `showa-village-gunma`（長野・福島に同名の村）。南牧村は `nanmoku`（長野は `minamimaki`）
- 試算は「月の削減時間・時間換算額」だけの形（ヒキツギAIの月額・回収期間は書かない）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | 対象 | WebSearch |
|---|---|---|---|
| stats | stats.md / stats_labor.md | 人口・経済センサス・製造業・農業・主要産業・地域区分・観光・外国人住民／群馬労働局・TDB前橋支店の県版・県内企業のAI利用の調査 | 15 |
| gov | gov_ai.md | 総務省の表の県と35市町村、12市のAI・実証・DX計画、県の企業向けDX支援、国の出先機関、商工会議所、知事 | 15 |
| gov_b | gov_ai_b.md | 15町8村のAI・実証・DX計画、商工会 | 8 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 県・県域の機関と12市（a）、15町8村（b） | 15 |
| cases | cases.md | 県内企業のAI事例（産業支援機構・県・市町村の成果報告・県議会・商工会議所・産業技術センター） | 25 |
| companies | companies.json / companies.md | 35市町村に本社があるシステム開発・Web開発の会社 | 12 |
| outside | cases_outside.md / serp.md | 同じ業種の県外の中小企業の事例（未使用の出典）、検索結果・FAQ候補 | 20 |
| 合計 | | | 110 |

## 状態
- [x] _brief.md・wages.md、scripts/area_uniq.py に gunma を追加、共有メモに slug（2026-11-05）
- [ ] 調査
- [ ] 試算の PLAN（_calc.py）を push
- [ ] 執筆仕様 docs/area-writing-spec-gunma.md
- [ ] 記事 36本（県1＋市町村35）
- [ ] data/subsidies/gunma.yml、areas.yml、build_shindan_data.py（同じコミット）
- [ ] 地域ガイド（北関東の段）、area-todo.md、area-new-prefecture.md、memory
- [ ] チェック（check_article・area_uniq・試算の重なり・見出し行だけの表）
- [ ] main に push

## 実績メモ
- 2026-11-05 ネットワークの確認: pref.gunma.jp・soumu.go.jp とも WebFetch で開けた
- stats（WS15まで）・cases（WS25まで）を起動（同時2人）
- _calc.py を鹿児島の形から作った（余り3、PLAN は空。`python3 -B data/area/gunma/_calc.py free <業種> <最小> <最大>` で空きを並べる）。2026-11-05 の空きは製造業で月95.75h〜、医療・福祉 70.75h〜、情報通信業 65.75h〜（それより小さい値はほぼ埋まっている）
- cases 18（完了: cases.md。**数値つきの県内の中小企業のAI事例は0件**。数値つきは群馬大学医学部附属病院〔前橋市、生成AIで説明同意文書のチェック、約1時間→1/2程度、2025-01-15 リリース〕と県農業技術センター・JA全農ぐんまのキュウリ自動収穫ロボット〔AI画像認識、64分/10a減、ロボット＋整枝方法の効果〕だけ。**澤藤電機〔太田市854名〕の「90%以上削減」は業務フローとツールの自動化でAIではない**。生成AI（数値なし）: 栄工業〔太田市〕・大西ライト工業所〔出典は伊勢崎市、法人番号の本店は桐生市で食い違い〕・エルグ〔富岡市65名〕・藤田デバイス〔高崎市100名〕・Calm Living Design〔高崎市、訪問看護13人、議事録「大幅に短縮」〕・雪ほたか〔川場村、AIチャット試験運用〕。県の補助金の採択（中一陸運 AI-OCR・山崎酒造 AI杜氏・糸井商会 LLM）は計画まで。他県で使用済み: サイテックス〔岐阜県恵那市〕・ヒロイ〔可児市〕・大道産業〔安八町〕・内田病院〔山形県庄内町〕。よろずのサイト不通・産業支援機構の事例集1・2巻404。照合依頼: gov←県庁 ChatSense〔約30%〕・R8 リスキリング事例集〔R9-03予定〕、gov_b←嬬恋村の内閣府資料、companies←石川建設・C&T・数理設計研究所・FUTURENAUT・LUC の法人番号）
- gov 起動（WS15まで）
