# 島根県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の「chore(area): 山梨県の調査の準備」〔eb16f7c〕の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-10-31。新しいセッションなので WebSearch の残りは200回（調査は125回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

**同じ時間に別のセッションが山梨県を作っている。** 島根県だけのファイル（data/area/shimane/、docs/area-writing-spec-shimane.md、articles/*-area-shimane*.md、data/subsidies/shimane.yml）は自由に作る。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json）は最後に `git pull --rebase origin main` してから直す。衝突したら両方の追加を残し、subsidies.json は build し直す。force push はしない。

## 市町村と slug（19市町村。県コード32）
- 一覧は data/area/shimane/_brief.md
- 美郷町（邑智郡）は `misato-town-shimane`（秋田県美郷町 misato・宮城県美里町 misato-town と重なるため。長野県池田町 ikeda-town-nagano と同じ形）。投稿後に3つのページが別々にあることを確かめる
- 試算は「月の削減時間・時間換算額」だけの形（ヒキツギAIの月額・回収期間は書かない）
- 島根県は中国経済産業局の管内の見込み（要確認）。これまでの17県のどれとも違う

## 調査の分担と WebSearch の配分（このセッションの残り200）
| 担当 | 書くファイル | 対象 | WebSearch |
|---|---|---|---|
| stats | stats.md / stats_labor.md | 人口・経済センサス・製造業・農林水産業・主要産業の候補・地域区分・観光・離島／島根労働局・TDB松江支店の県版・県内企業のAI利用の調査 | 15 |
| gov | gov_ai.md | 総務省の表の県と19市町村、各市町村のAI・実証・DX計画、県の企業向けDX支援・Ruby、国の出先機関、商工会議所・商工会、知事、原子力の事実 | 22 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 県・県域の機関と8市（a）、10町1村（b） | 20 |
| cases | cases.md | 県内企業のAI事例（しまね産業振興財団・県・市町村の補助金の成果報告・商工会議所・産業技術センター・島根大学・中国経産局・地元IT企業の事例を最初から） | 28 |
| companies | companies.json / companies.md | 19市町村に本社があるシステム開発・Web開発の会社 | 15 |
| cases_outside・serp | cases_outside.md / serp.md | 同じ業種の県外の中小企業の事例（未使用の出典）、検索結果・FAQ候補 | 22 |
| 合計 | | | 122（残り78を補充・仕様・確認に） |

## 状態
- [x] _brief.md・wages.md（2026-10-31）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-shimane.md
- [ ] 記事 20本（県1＋市町村19）
- [ ] data/subsidies/shimane.yml、areas.yml、build_shindan_data.py
- [ ] 地域ガイド（中国地方の段を新しく作る）、area_uniq.py、area-todo.md、area-new-prefecture.md、memory
- [ ] チェック（check_article・area_uniq・試算の重なり・見出し行だけの表）
- [ ] main に push（投稿・デプロイはユーザーが Mac で）

## 実績メモ
- 2026-10-31 調査開始。stats・gov・subsidy・cases の4人を起動（同時4人まで）
- 調査4人を起動（ID: stats acbf860df89a85c95 / gov af0c1a2df58a9caf5 / subsidy a243408d7e4c79c96 / cases a38bee7f9f82565d8）。companies・cases_outside+serp は空きが出たら起動
- subsidy 17（完了: subsidy_a.yml 18件〔県・県域・市〕・subsidy_b.yml 2件〔奥出雲町 IT・飯南町 専門家〕。**AI名指しの県域の補助なし・addon なし**。受付中: しまね産業振興財団 ITOC デジタル導入モデル支援助成金〔1/3〜1/2・400万、締切 2026-11-27・2027-01-29、プレゼン審査〕、県 在職者リスキリング支援〔Udemy Business 受講者負担半額〕、財団 ウェブ販路拡大助成〔随時〕、プロ人材拠点 副業・兼業〔随時〕。県 中小企業デジタル導入加速化補助金は第4回 10/16 で終了。市のAI名指しは安来市〔1/2・100万、10/30終了〕のみ。出雲市〔10/30〕・雲南市〔10/16〕終了。受付中の市: 松江市 デジタル化〔製造業のみ、2027-03-31〕・人材育成〔製造業・情報通信業、2/3・30万〕、浜田市 第2次〔11/13〕、益田市 ITパスポート受験料〔個人〕。町村にAI名指しなし。大田市・知夫村はサイトが開けず「断定しない」、津和野町は要綱が開けず。吉賀町の「デジタル技術・機器導入支援補助金」は町の歳入で事業者向けでない）
- gov 21（完了: gov_ai.md 632行、19市町村を1ファイル。生成AI 導入済6〔出雲 zevo・益田・飯南 ChatGPT無料版・安来・江津 GOV AI・奥出雲〕・実証中3〔松江 exaBase・大田・美郷〕、県は exaBase 導入済。両方の表にない7〔雲南・津和野・吉賀・隠岐4町村〕。AI全般: 松江 議事録 年6,092h（70%減）・県 1,610.93h・安来 1,467h〔市の計画の会議時間と意味が違う〕・川本町 AI音声 264h。**しまねソフト研究開発センターは2026-04に「ITイノベーションセンター」に改称（ITOC）**。「大人の島留学」〔海士町〕。国の出先機関: **中国経済産業局**〔農水省の窓口一覧で確認、局サイト403〕・島根労働局・中国財務局 松江財務事務所・中国四国農政局・中国運輸局。**知事 丸山達也〔2019-04-30 初就任〕**。原発: しまねの原子力2026〔2026-09〕、2号機 2025-01-10 営業運転再開、1号機 廃止措置第2段階、3号機「審査は終盤」。商工会議所8・商工会21。照合: 日本システム開発〔徳島県のページの同名会社か〕→cases、最低賃金1,092円→stats）
- companies 起動（a5fdd6dcc649a2498、WS15）・cases_outside+serp 起動（ac448ee8f1587d0cb、WS22）
- 大田市のサイト（www.city.oda.lg.jp）はこのコンテナの curl で 200（gov・subsidy は開けなかった）。執筆で確かめ直す
- 知夫村: http://www.chibu.jp/ は観光協会の観光サイト（村役場のサイトではない）。村役場 www.vill.chibu.lg.jp は https がプロキシで拒否、http はリダイレクト
- cases_outside+serp 22（完了: 未使用の出典 山口県「DXの手引き」〔R3-03〕・広島県「ひろしまサンドボックスのこれまでの成果」〔R6-07-19〕。**未使用で数値つき3件**: カワトT.P.C.〔山口県岩国市、AI施工図 作業時間90%減、実績、2021年・配管図面〕・内能美漁協ほか〔広島県江田島市、かき幼生AI検出 約70→90%、実証の精度、代表は東大〕・アイグラン〔広島市、保育、1園 月20〜30h減、実証、正社員3,188名〕。使えない: ひびき精機〔年5,700h はIoT・保全込み〕・美東電子〔目標〕。予備: 鳥取県 生成AIモデル企業6社・中国芝浦電子・サニー・シーリング〔数値なし〕。瓦・鋳造・しじみ・酒蔵・農業・旅館・運送・介護・林業は0件。serp: 「島根県 AI 補助金」上位は補助金DBだけ〔終了と受付中を区別せず〕、FAQ候補22。11月以降の講座4件〔11/5 AIエージェント入門（松江）・11/9・18・27 ITOC AI・データ活用相談会・12/4 AI利用の社内ルール（出雲市）・12/15 Python・AI構築入門〕。中国経産局サイト403）
- WebSearch 累計 60（subsidy 17・gov 21・cases_outside+serp 22）
- 仕様の下書き D34（行政＋補助金、shimane.yml も）起動（af8154f73b686ed9b、WS0）
