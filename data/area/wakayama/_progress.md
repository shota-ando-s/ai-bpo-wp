# 和歌山県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-07。WebSearch はセッションで200回まで（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（奈良・滋賀〔と北海道〕を別々のセッションで同時に作っている）。

和歌山県だけのファイル（data/area/wakayama/、docs/area-writing-spec-wakayama.md、articles/*-area-wakayama*.md）は自由に作る。`data/subsidies/wakayama.yml` は areas.yml の和歌山県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_kinki/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（30市町村＝9市20町1村。県コード30）
- 一覧は data/area/wakayama/_brief.md（総務省の全国地方公共団体コードで確認、2026-11-07）
- 和歌山市 `wakayama-city`、かつらぎ町 `katsuragi-town`、美浜町 `mihama-town`、日高町 `hidaka-town-wakayama`、新宮市 `shingu-city`、広川町 `hirogawa`、北山村 `kitayama-village`（共有メモに push 済み）
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を3で割った余りが1の時間だけ**（0.25, 1.0, 1.75, … の0.75時間刻み）。全県の記事・全県の _calc.py の PLAN（奈良・滋賀・北海道を含む）と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 25 |
| gov | gov_ai.md（県・9市・国の出先機関・総務省表の全30行・支援機関） | 12 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・9市） | 10 |
| choson | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（20町1村） | 12 |
| companies | companies.json / companies.md | 12 |
| outside | cases_outside.md / serp.md | 15 |
| cases2 | cases2.md（補充） | 10 |
| 合計 | | 110 |

## 状態
- [x] _brief.md・wages.md・_calc.py の枠（2026-11-07）
- [ ] 調査
- [ ] PLAN を決めて push
- [ ] 執筆仕様 docs/area-writing-spec-wakayama.md
- [ ] 記事 31本（県1＋市町村30）
- [ ] data/subsidies/wakayama.yml・areas.yml・build（同じコミット）
- [ ] 地域ガイド（近畿地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック（check_article・extract_claims・area_uniq・_calc.py）
- [ ] main に push

## 実績メモ
- 2026-11-07 ネットワーク確認（pref.wakayama.lg.jp・soumu.go.jp とも開けた）。HEAD が detached だったので `git checkout -B main origin/main`。市町村30を総務省のコード表で確認。area_uniq.py に wakayama を足し、共有メモに slug を push
- stats・cases を起動
- cases 24（完了: cases.md 368行。**数値つきの県内事例0件**。数値なしの一次事例6社〔カナプレスト 紀の川市・ダートコーヒー 和歌山市・菱岡工業 和歌山市・組込ＡＩ研究所 和歌山市・河合石灰工業 和歌山工場・中田食品 田辺市〕。AI でない数値: たにぐち〔画像処理〕・ニッティド〔Airtable〕・わかやまAi助〔ベンダーの期待値〕・TechnologyDock〔検証段階〕。県の DX 導入事例集 PDF は pypdfium2 で読めた。近畿財務局の107社調査〔県別なし〕→共有メモ。近畿経産局は403）
- stats 9（完了: stats.md・stats_labor.md。R7国調確報 863,757人〔▲6.38%〕、30市町村すべて減。15〜64歳は不詳補完値から当社計算〔日高町だけ+1.3%〕。推計人口 2026-10-01 852,674人。製造品出荷額 24,993.6億円〔全国35位〕、和歌山市・海南市の鉄鋼・化学・石油は大企業として分けた〔日本製鉄・花王は公式で確認、ENEOS は404で未確認〕。果実906億円〔70.5%〕。観光 R7、白浜町が宿泊の33.5%。振興局7区分〔条例〕、紀北・紀中・紀南は使わない。有効求人倍率 2026-09 受理地別0.98・就業地別1.07、湯浅1.77、一般事務0.26・介護2.68。最低賃金 1,101円〔2026-10-03 発効〕。**TDB 和歌山支店の県版なし**→近畿版〔後継者不在率45.3%・社長年齢61.6歳 近畿最高・休廃業382件・生成AI 34.2%〕。県内企業の AI 利用率の調査なし。2026年の災害救助法の適用なし、SN保証4号は確かめられず）
- gov を起動。subsidy を起動
- subsidy 4（完了: subsidy_a.yml 13件・subsidy_a_areas.md。受付中・随時10: **和歌山市 生産性向上ツール導入補助金〔AI又はIT・IoTツール、1/2・50万、10/1〜予算到達まで、11/6 で300万のうち234万申請済み〕**・**紀の川市 DX推進支援補助金〔随時、AI名指し、1/2・50万〕**・財団 成長企業支援〔紹介手数料、〜2027-02-01〕・副業兼業2・タクシー〔〜12/25〕・スマート水産業〔〜12/18〕・EC 和歌山市・橋本市〔〜1/29〕・紀の川市 副業プロ人材。終了: 県 中小企業成長促進補助金〔予算到達〕・えるぼし〔9/30〕・業務改善促進助成金〔9/30〕。addon なし。独自なし6市。SN1号〔全東信〕・中東情勢の融資。7次 12/1 17時を事務局で確認。成長促進の交付決定560件にAI名指し10件→cases2）
- choson を起動
- gov 10（完了: gov_ai.md 558行。総務省表: 生成AI 導入済12・実証中5〔海南・田辺・新宮・みなべ・那智勝浦〕・表にない13〔市は岩出市だけ。AI全般にはある〕、両方なし8町村。生成AIの削減時間は0、AI全般は県 4,670h/年・184h、九度山町130h、古座川町90h、かつらぎ町133h・387h〔見込み〕。**知事は宮﨑泉〔2025-06〜〕**。県に「DX推進計画」なし（官民データ利活用推進計画 R5〜R8）。県庁 Exa Enterprise AI 全庁 2026-04〜。県＋9市で生活保護 AI〔WAISE〕2025-10〜。**リンクの条件: 海南・御坊・田辺・紀の川は営利サイトからのリンク不可、県は個別ページへのリンクに事前連絡、有田・御坊・田辺・紀の川はトップページのみ→ユーザー判断〔area-todo〕**。商工会議所7〔和歌山・海南・田辺・新宮・御坊・橋本・紀州有田〕、商工会31、太地町に商工会の所在なし。国の出先5機関を確認。セミナー: 工業技術センター 生成AI 11/13・データ利活用シンポ 11/26・12/4。Jin の約2,000hは市の見込み、Ai助は期待値）
- companies を起動
- PLAN 30行（_assign.py の出力。規模の小さい順に、既存1,078本・21県 660行〔滋賀19を含む、奈良はまだ〕と重ならない最小の時間）: 月61.75〜317.5h・約21.7万〜108.5万円・18〜165名。医療福祉6・製造9・卸小売6・建設4・宿泊飲食3・運輸2。小さい町村は「県内の事業所の例」の規模〔北山村24名・太地町18名など。村内にこの規模の会社があるという意味ではない〕。湯浅町はダートコーヒー〔33名・食料品〕に近かったので48名に。1人の月の業務量が40h超が12ページ
