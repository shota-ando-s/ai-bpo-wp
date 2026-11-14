# 宮崎県（県・県域の機関）と9市の AI・IT 向け補助金（2026-11-04 確認）

データ本体は `subsidy_a.yml`（24件。日向市の1件だけ補助金ポータル〔二次情報、confidence: secondary〕、ほかは公式のページ・募集要領・交付要綱・ハンドブックで確認。市のページを WebFetch の要約で読んだものは yml の note に書いた）。「受付中」「随時」でも予算に達すると締め切られる。**県の支援施策データベースや補助金ポータルだけで判断せず、9市すべての商工担当課の記事一覧・事業者向けの分類ページを開いた**（日向市はサイトが 503 で開けなかった）。

2026-11-04時点で受付中（open）・随時（rolling）は次の7件。**県・県域の機関で今申請できる補助金はない。**
- 随時（市）: **延岡市 人材確保支援補助金（人材育成推進事業）**（国の人材開発支援助成金〔人への投資促進コース・事業展開等リスキリング支援コース〕の支給決定を受けた研修の自己負担の1/2・10万円、支給決定から2か月以内。**国の制度への上乗せ＝addon**）、**延岡市 中小企業大学校研修派遣助成事業**（1/2・10万円、研修後30日以内）、**延岡市 ものづくり人材育成派遣研修助成事業**（1/2〜2/3・10万円）、**延岡市 副業・兼業人材マッチング支援事業**（掲載料 10/10・11万円）
- 受付中（市）: **えびの市 中小企業大学校受講料補助**（1人2万円・年4万円、**〜2027/2/26**、受講前に申請）、**串間市 企業支援プロジェクト事業（事業拡大・生産性向上支援／スキルアップ・雇用対策支援）**（3/5・50万円、**申請は〜2026/11/6。ただし必須の事前相談は10/30で締切**で、未相談の事業者は新たに申請できない）

**今年度の募集を終えたAI・デジタル向けの補助**: 県の**産業DX推進事業費補助金**（導入タイプ 1/2・250万円〔下限100万円〕**4/24〜6/12**、発展タイプ 1/2・1,000万円〔下限200万円〕**4/24〜6/30**）、県の**物価高騰対策DX推進事業費補助金**（デジタルツール導入事業 1/2・200万円、戦略的DX推進事業 1/2・500万円、**3/26〜5/15**。二次募集は8/7締切と検索の抜粋にあり、県のページは404）、県の**「稼ぐ力」強化支援事業費補助金**（IT導入関連費・ECサイト関連費を含む、2/3〔賃上げ特例3/4〕・50万/100万円、**5/7〜5/29**、商工会議所・商工会が窓口）、県の**ものづくり企業物価高騰対策設備等改修支援事業補助金**（製造業のみ、生産ラインの自動化など、1/2・1,500万円、二次**〜8/27**）、機構の**企業経営力アップ人材育成支援事業**（研修 1/2・5万〜20万円、「本年度の募集は終了」）、**宮崎市 成長応援!設備投資サポート**（DX支援枠 1/2・30万〜300万円〔**AIツール・AIカメラを名指し**、DX認定の取得・申請予定が要件〕、一般支援枠 1/2・250万円、小規模支援枠 1/2・30万円。一次**〜7/31**、ページに「受付を終了しました」）、**延岡市 元気な中小企業応援事業（DX・IT枠）**（2/3・100万円、事前相談締切）、**延岡市 省力化・事業拡大・新分野進出支援補助金**（1/2・30万/100万円、**9/2〜10/1**）、**日南市 商流開発チャレンジアシスト補助金（販路拡大型）**（ECサイト構築を含む、1/2・50万円、**4/1〜6/1**）、**日向市 DX・生産性向上等設備導入事業補助金**（2/3・1,000万円、**7/3〜7/31**、二次情報）、**えびの市 小規模事業者持続化支援事業補助金**（市の単独事業、1/2・50万円、**6/1〜6/30**）。県の**賃上げ対応緊急支援金**（7万円×人数）も終了。

**AIを名指しした制度**: 県の産業DX推進（発展タイプ）の審査項目「先進性」（20点）が「ＡＩ等を活用した新たなビジネスモデルの構築」、導入タイプの Jグランツの参考例が「AI-OCRやRPAを活用した文書事務の効率化」。宮崎市 成長応援!設備投資サポート（DX支援枠）の対象経費に「AIツール」「AIカメラ（不良品検知、来客分析等）」。いずれも2026年度は終了。県の DX推進モデル企業創出プロジェクト（伴走支援、補助金ではない）は第2回「AIを活用した分析・ビジネスモデル」・第4回「AIリスキリング」。

**国の補助金への上乗せ（addon）は延岡市の1件だけ**（人材育成推進事業 → national.yml の `jinzai-reskilling`、`{kind: remaining, ratio: 0.5}`、上限10万円）。国のデジタル化・AI導入補助金・省力化投資補助金・ものづくり補助金への県・9市の上乗せは見つからない。県の産業DX推進は国庫・公的制度との二重受給を対象外にしている。えびの市の小規模事業者持続化支援事業補助金は「国の『小規模事業者持続化補助金』とは異なる、市の単独事業」。

**経済産業局**: このファイルでは確かめていない（gov 担当の確認と照合が要る。shared.md では九州経済産業局のサイトがこの環境から403）。

## 宮崎県（県・県域の機関）

見たページ:
- 県 産業政策課（総合政策部）「令和8年度産業DX推進事業費補助金について」https://www.pref.miyazaki.lg.jp/sangyoseisaku/kense/johotsushin/20260420190300.html （掲載2026-04-24、更新2026-05-01）、チラシ https://www.pref.miyazaki.lg.jp/documents/108409/108409_20260428162949-1.pdf 、発展タイプ募集要領 https://www.pref.miyazaki.lg.jp/documents/108409/108409_20260423173324-1.pdf （p1 受付期間・追加募集の可能性、p4 対象外、p5〜6 経費・補助率・予算5,000万円、p8 審査項目・加点）、交付要綱 https://www.pref.miyazaki.lg.jp/documents/108409/108409_20260423174329-1.pdf （保存したが本文は読んでいない）。導入タイプは事務局の宮崎県情報産業協会 https://misa45.jp/2026/04/23/20260424dxhoj/ （「終了しました」）と Jグランツ公開API（id a0WJ200000CDVyTMAX、受付終了2026-06-12、事業完了期限2027-01-31）。ページは導入タイプのリンク文で「一般社団法人宮崎県産業協会」と書き、問い合わせ欄は「一般社団法人宮崎県情報産業協会」（misa45.jp）で表記が揺れる（yml: miyazaki-sangyo-dx-donyu / miyazaki-sangyo-dx-hatten）
- 県「物価高騰対策DX推進事業費補助金（令和7年度補正予算）について」https://www.pref.miyazaki.lg.jp/sangyoseisaku/kense/johotsushin/20260309112425.html 、チラシ https://www.pref.miyazaki.lg.jp/documents/107384/107384_20260326160957-1.pdf 、戦略的DX推進事業の募集要領 https://www.pref.miyazaki.lg.jp/documents/107384/107384_20260326155758-1.pdf （p6）。「【二次募集のご案内】…」https://www.pref.miyazaki.lg.jp/sangyoseisaku/kense/johotsushin/20260706162312.html は2026-11-04に WebFetch で2回とも404（WebSearch の抜粋で受付締切 2026-08-07）（yml: miyazaki-bukka-dx-tool / miyazaki-bukka-dx-senryaku）
- 県 産業政策課の記事一覧「その他（情報通信）」https://www.pref.miyazaki.lg.jp/kense/johotsushin/sonota/index.html （24件）と「新着情報-産業政策課」https://www.pref.miyazaki.lg.jp/sangyoseisaku/shinchaku/index.html （50件）を全件見た。補助金以外の事業:
  - 「みやざきDXけん引人材育成事業」https://www.pref.miyazaki.lg.jp/sangyoseisaku/kense/johotsushin/20260805142158.html （無料。戦略策定コース 定員70社・8/26締切・9/2〜10/14、実践コース 20社・選考・11/6キックオフ〜2027年2月末。事務局 FunTre株式会社。AIの記載なし）
  - 「みやざきDX推進モデル企業創出プロジェクトについて」https://www.pref.miyazaki.lg.jp/sangyoseisaku/shigoto/chushokigyo/20260701165725.html （5社程度、8/7締切、DX認定の取得を目指す。第2回「AIを活用した分析・ビジネスモデル」第4回「AIリスキリング（業務効率化及びデータ分析）」。運営は有限責任監査法人トーマツ。費用の記載なし）。**gov 担当向け**
  - 「ひなたデジタルアカデミア2026」https://www.pref.miyazaki.lg.jp/sangyoseisaku/kense/johotsushin/20260710132317.html （高校生・大学生・若手求職者向けの無料講座、AI開発講座など。企業向けではない）、「みやざきデジタル人材育成事業」（未経験からIT人材を目指す個人向け）
  - 「宮崎県内事業者のデジタル化・DX現状調査アンケート」https://www.pref.miyazaki.lg.jp/sangyoseisaku/kense/johotsushin/20260813153551.html （2026-08-19掲載。開いていない。**stats・gov 担当向け**：結果が公表されていれば県内のAI活用率の一次資料になる）
  - 「【令和6年度版】デジタル技術活用事例集」https://www.pref.miyazaki.lg.jp/sangyoseisaku/kense/johotsushin/20230414132435.html （12分野のPDF。下の「事例の手がかり」）
  - 「令和8年度みやざき未来人財確保・定着事業補助金」https://www.pref.miyazaki.lg.jp/sangyoseisaku/shigoto/sangyo/20260601204259.html は対象が県内の高等教育機関・高等教育コンソーシアム宮崎で、企業向けではない（yml に入れていない）
- 県 商工政策課「物価高及び中東情勢の影響を受ける県内中小企業者等への支援策について」https://www.pref.miyazaki.lg.jp/chusyo_portal/shigoto/chushokigyo/shien.html （2026-11-04更新）: 「稼ぐ力」強化支援・ものづくり物価高騰・賃上げ対応緊急支援金の3件とも「受付終了」（yml: miyazaki-kasegu-chikara / miyazaki-monozukuri-bukka / miyazaki-chinage-kinkyu）。「稼ぐ力」の公募開始 https://www.pref.miyazaki.lg.jp/shokoseisaku/press/2026/05/20260427095937.html 、ものづくり（二次）https://www.pref.miyazaki.lg.jp/kigyoshinko/shigoto/shokogyo/20260424145248.html 、賃上げ支援金 https://www.pref.miyazaki.lg.jp/koyorodoseisaku/press/2026/05/20260423145617.html 。**賃上げ支援金の締切がプレスリリース（9/30）と支援策ページ（10/31）で食い違う**
- 県の「ひなたゼロカーボン加速化事業補助金」（法人は2026-06-18〜12-04、太陽光・蓄電池・LED等）は WebSearch の抜粋で見ただけ。省エネ設備向けで AI・IT ではないので yml に入れていない
- **公益財団法人宮崎県産業振興機構の公式サイトは https://www.mepo.or.jp/ **（トップの組織名で確認。www.i-port.or.jp は無関係の比較サイトだった）。トップの公募情報（受付中は中小企業特許出願等支援事業・ものづくり取引拡大商談会・Web商談だけ）、「企業経営力アップ人材育成支援事業」https://www.mepo.or.jp/shiensaku/724.html （「本年度の募集は終了しました」、実施要領は令和7年版のスキャン画像）（yml: miyazaki-mepo-keieiryoku-jinzai）、「日本のひなた宮崎人材育成事業に係る研究開発等テーマの採択結果」https://www.mepo.or.jp/news/8207.html （2026-10-23、公募9/1〜9/30、応募6件・採択5件。研究開発テーマでAIの語はない）。補助金ポータル（二次情報）の抜粋では機構の令和8年度の助成にフードビジネス商品開発・ブラッシュアップ支援（2/3・100万円、5/29締切）、環境イノベーション支援、地域産業技術研究開発支援（F/S、150万円）、女性・若者応援!起業チャレンジ支援があり、いずれも AI 導入向けではない（機構のページは開いていない）
- 宮崎県よろず支援拠点 https://yorozu-miyazaki.go.jp/ （実施機関は機構、宮崎市佐土原町東上那珂16500番地2、0985-74-0786）: トップのセミナー欄に「第5回 AIビジネス活用セミナー」「よろずAI相談会」「AI活用×集客改善ワークショップ」、相談分野「IT・AI・WEB活用」。「生産性向上支援センター」https://yorozu-miyazaki.go.jp/productivity は5S・業務の見える化・標準化を無料で現場訪問して支援（生成AIの記載なし。省力化投資補助金〔一般型〕の審査で加点の見込みと記載）。国富町のページ（下記）は同センターの「稼ぐ力現場づくりチーム」のリーフレットに「生成AI活用」があると書く。**gov 担当向け**
- 産業DXサポートセンター https://www.dx-miyazaki.com/ （実施機関 宮崎県情報産業協会、運営 株式会社宮崎県ソフトウェアセンター）: 無料相談（Zoom・LINE・電話）、国・県の補助金の説明、2026-07 SaaS活用講座、2026-09 DXセミナー、2026-10 都城市「DXセミナー・展示会」に参加
- 宮崎県工業技術センター: 延岡市のハンドブックが示す https://www.iri.pref.miyazaki.jp/?page_id=24 は、curl で接続できず（000）、WebFetch は 503。県のサイトの /kogyogijutsu/ は404。**開けなかった**
- 県の「中小企業支援施策ガイド」の一部とみられる PDF https://www.pref.miyazaki.lg.jp/documents/110822/110822_20260709205258-1.pdf （よろず支援拠点の頁）: 機構の経営情報課 0985-74-3850

**相談窓口**: 県 産業政策課 産業デジタル担当（0985-26-7682）、宮崎県情報産業協会（0985-30-5010）、産業DXサポートセンター、宮崎県よろず支援拠点（0985-74-0786）、宮崎県産業振興機構（0985-74-3850）、県 商工政策課（0985-26-7094）。商工会議所・商工会の名前と数は gov 担当の確認を正とする（「稼ぐ力」の窓口一覧 PDF は開いていない）

## 宮崎市（miyazaki-city）

**市独自の制度あり（AIツール・AIカメラを名指ししたDX支援枠は受付終了）**
- 「成長応援!設備投資サポート」https://www.city.miyazaki.miyazaki.jp/business/loan/409734.html （2026-10-22表示、「受付を終了しました」）、公募要領（令和8年10月改定）https://www.city.miyazaki.miyazaki.jp/fs/8/9/8/4/8/6/_/_261001_______________________.pdf （DX支援枠の対象経費 p7、一般・DX枠の一次締切 7/31、小規模枠は随時で予算到達で停止）（yml: miyazaki-city-seicho-setsubi-dx / miyazaki-city-seicho-setsubi-shokibo）
- 根拠として見た一覧: 「産業・事業者」https://www.city.miyazaki.miyazaki.jp/business/ （14分類）、「融資・補助金」https://www.city.miyazaki.miyazaki.jp/business/loan/ （28件）、「お知らせ」https://www.city.miyazaki.miyazaki.jp/business/info/ の1ページ目（20件、18ページ中）。ほかは融資・先端設備等導入計画・奨学金返還支援企業応援奨励金・地域のにぎわい創出・認定職業訓練企業者補助金・特定技能人材雇用促進・地域貢献学術研究助成金（大学向け）で、IT・研修向けではない
- 「宮崎市が行う企業支援制度集 2025」https://www.city.miyazaki.miyazaki.jp/fs/8/4/9/5/5/5/_/849555.pdf （2025-07-01）は開いていない

**相談窓口**: 宮崎市 経済部 産業政策課（0985-21-1792）

## 都城市（miyakonojo）

**市独自の AI・IT 導入の補助は見つからなかった（研修は中小企業大学校の受講料補助だけ）**
- 「中小企業の人材育成のための費用の一部を補助しています」（人材育成事業費補助金）https://www.city.miyakonojo.miyazaki.jp/soshiki/77/3270.html （2025-06-17更新、補助率・上限・今年度の受付の記載なし）（yml: miyazaki-miyakonojo-jinzai-ikusei）
- 根拠として見た一覧: 「産業・事業者」https://www.city.miyakonojo.miyazaki.jp/life/4/ 、商工業 > 経営支援 https://www.city.miyakonojo.miyazaki.jp/life/4/41/218/ （お知らせ14件・おすすめ3件）、支援・助成の一覧（8件）。ほかは省エネルギー設備導入支援（1/2・100万円、2026-04-01〜12-28、10/1から複数回申請可）、事業承継及びM&A支援、もえ産品開発、創業支援、先端設備等導入計画、賃金引き上げの支援策（厚生労働省の紹介）。「中小企業の設備投資や技術開発を支援しています」https://www.city.miyakonojo.miyazaki.jp/soshiki/77/3235.html （2019-10-29更新）は国・県・市の制度のリンク集で、業務改善助成金の案内がある
- 都城うまいものネットショップの「ネットショップ事業者支援」https://www.city.miyakonojo.miyazaki.jp/life/4/50/259/ はネットショップの紹介ページ（2019）で補助ではない
- 「都城市DXチャレンジプロジェクト」の公募型コンペ https://www.city.miyakonojo.miyazaki.jp/soshiki/99/45531.html （2026-10-13更新）: 市の課題（「AIの活用」を含む5テーマ）をAI・IoTで解決する企業の提案を募る市の発注（業務委託とみられる。提案上限501万円〔8/1時点〕、参加表明11/6まで、企画提案書は12月まで毎月15日締切）。**中小企業の AI 導入を補助する制度ではない**ので yml に入れていない。「過去採択事例」のページは開いていない（**gov・cases 担当向け**）
- WebSearch（都城市のドメインに限定、1回）で令和8年度当初予算のデジタル化関連 179事業・11億6,865万円（予算のポイント PDF https://www.city.miyakonojo.miyazaki.jp/uploaded/attachment/44097.pdf 、抜粋のみ。開いていない）

**相談窓口**: 都城市 商工政策課 商工担当（0986-23-2983）

## 延岡市（nobeoka）

**市独自の制度あり（研修系4件が随時受付中。国の人材開発支援助成金への上乗せあり）**
- 「事業者の皆様へ」https://www.city.nobeoka.miyazaki.jp/soshiki/43/48670.html （2026-04-01更新）と「延岡市中小企業支援ハンドブック」令和8年度版（令和8年9月版）https://www.city.nobeoka.miyazaki.jp/uploaded/attachment/28883.pdf （p12 元気な中小企業応援事業、p13 販路開拓支援、p18 中小企業大学校研修派遣、p19 ものづくり人材育成派遣研修）（yml: miyazaki-nobeoka-genki-dx-it / -chusho-daigakko / -monozukuri-haken / -fukugyo-matching）
- 「【補助金案内】延岡市人材確保支援補助事業」https://www.city.nobeoka.miyazaki.jp/soshiki/40/2622.html （2026-05-19更新）、実施要領（5/19以降の申請）https://www.city.nobeoka.miyazaki.jp/uploaded/attachment/27304.pdf 、リーフレット https://www.city.nobeoka.miyazaki.jp/uploaded/attachment/27302.pdf （yml: miyazaki-nobeoka-jinzai-ikusei-suishin）
- 「省力化・事業拡大・新分野進出を支援します」https://www.city.nobeoka.miyazaki.jp/soshiki/40/51775.html （2026-09-02更新、9/2〜10/1）（yml: miyazaki-nobeoka-shoryokuka）
- 「令和8年度 延岡の元気な中小企業応援事業 公募開始について」https://www.city.nobeoka.miyazaki.jp/soshiki/43/49250.html は WebFetch で404。公募期間 5/22〜6/22 は補助金ポータル（二次情報）の値
- 販路開拓支援事業（県外見本市 1/2・10万円など、随時）は見本市・商談会の出展・参加・海外調査で、EC・Web は対象にない（yml に入れていない）
- 根拠として見た一覧: 事業者向け https://www.city.nobeoka.miyazaki.jp/life/2/ 、中小企業 https://www.city.nobeoka.miyazaki.jp/life/2/17/77/ （22件）、工業 https://www.city.nobeoka.miyazaki.jp/life/2/19/83/ （30件）、産業政策課 https://www.city.nobeoka.miyazaki.jp/soshiki/40/ 。「延岡ITカレッジ」（2026-08受講生募集、10月開講）は個人向けの講座で事業者への補助ではない。改善インストラクタースクール延岡（県工業会）のカリキュラム第7回に「IOTと生産性／ＡＩ活用の効用」（令和7年度の例、ハンドブック p17）

**相談窓口**: 延岡市 商工観光文化部 工業振興課 工業振興係（0982-22-7035）、産業政策課 地域経済係（0982-22-7350）、地域産業連携プロモーター（宮崎県工業会 県北分室）

## 日南市（nichinan）

**市独自の AI・IT 導入・研修の補助は見つからなかった（ECサイト構築を含む販路拡大型は終了）**
- 「商流開発促進事業を活用しませんか?」https://www.city.nichinan.lg.jp/shigoto_sangyo/sangyoshinko_jigyoshien/2/3572.html （2026-04-01更新、4/1〜6/1）（yml: miyazaki-nichinan-shoryu-hanro）
- 根拠として見た一覧: しごと・産業 https://www.city.nichinan.lg.jp/shigoto_sangyo/index.html 、事業支援・補助金・控除等 https://www.city.nichinan.lg.jp/shigoto_sangyo/sangyoshinko_jigyoshien/2/index.html （17件：融資・利子補給・ひなまちツアー造成・先端設備等導入計画・地域課題解決型創業・油津港海上物流・防災士養成・事業承継前後・飫肥杉・LPガス）、雇用・就業 https://www.city.nichinan.lg.jp/shigoto_sangyo/koyo_shugyo/index.html （7件）、事業者向け https://www.city.nichinan.lg.jp/shigoto_sangyo/680.html （7件）

**相談窓口**: 日南市 商工政策課（ふるさと応援係 0987-31-1165）

## 小林市（kobayashi）

**市独自の AI・IT 導入の補助は見つからなかった（研修は中小企業大学校の受講料補助だけ）**
- 「小林市中小企業大学校受講補助金」https://www.city.kobayashi.lg.jp/shigoto_sangyo/sangyo/chushokigyonadoshien/3473.html （2024-03-14更新）（yml: miyazaki-kobayashi-chusho-daigakko）
- 根拠として見た一覧: 産業 https://www.city.kobayashi.lg.jp/shigoto_sangyo/sangyo/index.html （6分類・25件）、中小企業等支援 https://www.city.kobayashi.lg.jp/shigoto_sangyo/sangyo/chushokigyonadoshien/index.html （4件：共済・中小企業大学校2件・先端設備等導入計画）、原油価格・物価高騰対策支援（利子補給だけ）

**相談窓口**: 小林市 経済建設部 商工観光課（0984-23-1174）

## 日向市（hyuga）

**公式サイトが開けなかった（制度は二次情報だけ）**
- 日向市の公式サイト https://www.hyugacity.jp/ は2026-11-04に curl・WebFetch とも 503（3回試した）。www.city.hyuga.miyazaki.jp・www.city.hyuga.lg.jp は接続できない
- 「日向市DX・生産性向上等設備導入事業補助金」（2/3・1,000万円、7/3〜7/31）は補助金ポータル https://hojyokin-portal.jp/subsidies/78317 （二次情報）と WebSearch の抜粋（市の公募ページ https://www.hyugacity.jp/display.php?cont=260629154017 ）だけ（yml: miyazaki-hyuga-dx-seisansei、confidence: secondary）
- **「制度なし」とも「これだけ」とも断定しない**。執筆の前にサイトの復旧後に商工港湾課（課の名前は未確認）のページを確かめる（area-todo 向け）

**相談窓口**: 日向市役所（担当課の名前は確かめていない）

## 串間市（kushima）

**市独自の制度あり（事業拡大・生産性向上と研修・資格取得、申請は11/6まで・事前相談は10/30で締切）**
- 「令和8年度企業支援プロジェクト事業」https://www.city.kushima.lg.jp/main/business/cat4/cat/post-583.html （創業・事業拡大/生産性向上・スキルアップ/雇用対策は3/5・50万円、販路拡大〔商談会出店〕は3/5・25万円。商工会議所の会員が要件）（yml: miyazaki-kushima-kigyo-shien-seisansei / -skillup）
- 根拠として見た一覧: 事業者の方へ https://www.city.kushima.lg.jp/main/business/index.html （19分類）、商工業 > 制度・お知らせ・創業支援（cat4/cat2・cat4/cat・cat4/cat1）、雇用・労働・賃金（cat7、記事なし）、情報政策（cat10、サーバー室の入室だけ）。ほかは商工業にぎわい創出（団体向け、3/5・10万円）・経営バトンタッチ推進・店舗等活性化・利子補給・融資・先端設備等導入計画

**相談窓口**: 串間市 商工観光スポーツランド推進課 商工係（0987-55-1127）

## 西都市（saito）

**市独自の AI・IT 導入・研修の補助は見つからなかった**
- 市のサイトは新しい CMS で事業者向けの分類ページがないため、サイトマップ https://www.city.saito.lg.jp/sitemap.xml （415件）の「補助金・助成金・（一部）免除」https://www.city.saito.lg.jp/kurashi/hojokin/ の39件すべての題名を取得して確かめた。事業者向けは「西都市地場産業販路拡大事業補助金」https://www.city.saito.lg.jp/kurashi/hojokin/post_1818 （地場産品の事業者の団体が市内で開く物産展等、2/3・25万円。EC・Webの記載なし）、「【第4期申請】西都市創業等支援事業補助金」https://www.city.saito.lg.jp/kurashi/hojokin/3_24 （創業・承継者の新事業、2/3・基本50万円＋加算、10/1〜10/31）、「西都市事業継続力強化事業補助金」https://www.city.saito.lg.jp/kurashi/hojokin/post_1797 （止水板・発電機など、2/3・20万円）、先端設備等導入計画、インターンシップ奨励金、スマート農業推進・農業関係
- 商工観光課（産業振興係 0983-32-1011）の課のページ /organization/post-8.html は404

**相談窓口**: 西都市 商工観光課 産業振興係（0983-32-1011）

## えびの市（ebino）

**市独自の制度あり（研修は中小企業大学校の受講料補助が2/26まで受付中）**
- 「中小企業大学校受講料補助に関するお知らせ」https://www.city.ebino.lg.jp/sangyo_business/sangyoshinko/shokogyo/3/1993.html （2026-04-01更新）（yml: miyazaki-ebino-chusho-daigakko）
- 「えびの市小規模事業者持続化支援事業補助金について」https://www.city.ebino.lg.jp/sangyo_business/sangyoshinko/shokogyo/3/5049.html （2026-05-21更新、6/1〜6/30）（yml: miyazaki-ebino-jizokuka）
- 「建設産業技術者の資格取得を支援します」https://www.city.ebino.lg.jp/sangyo_business/kensetsu_hojokin/hojokinshinsei/2644.html （2026-05-01更新）: 市内に本店がある建設業者等の技術者の施工管理技士・建築士・電気工事士・測量士などの受験料・講座受講料 1/2・1人5万円、2026-07-01〜2027-01-31（財政課 入札・契約係）。IT・AIの資格は対象外なので yml に入れていない
- 根拠として見た一覧: 産業・ビジネス https://www.city.ebino.lg.jp/sangyo_business/index.html 、商工業 https://www.city.ebino.lg.jp/sangyo_business/sangyoshinko/shokogyo/index.html （「女性のためのデジタル人材育成支援セミナー」などの個人向け講座、国の助成金制度の案内）、中小企業支援 https://www.city.ebino.lg.jp/sangyo_business/sangyoshinko/shokogyo/3/index.html （6件）。「助成情報」一覧 https://www.city.ebino.lg.jp/josei_list.html は「現在、一覧はございません」（2022-02-28更新のまま）

**相談窓口**: えびの市 観光商工課 商工係（0984-35-3728）

## 事例の手がかり（cases 担当へ）

- **県「【令和6年度版】デジタル技術活用事例集」**（12分野、2025-06-10更新）https://www.pref.miyazaki.lg.jp/sangyoseisaku/kense/johotsushin/20230414132435.html 。「事業名：」の形の頁は県の補助金（産業デジタル実装支援事業費補助金など）の実装事例とみられる（補助金名は事例集に書かれていない）。AIの語がある県内の事業者（PDF の頁は pdftotext の改頁で数えた）:
  - **有限会社前田包装容器（宮崎市、包装資材卸、従業員20名）** 卸売・小売 p6（R加事例）https://www.pref.miyazaki.lg.jp/documents/76534/76534_20250604084432-1.pdf : 事業名「①ＲＰＡ、②イラストAI、ChatGPT導入、③ＳＮＳ活用・自動化推進事業」。Midjourney・ChatGPT Plus でデザインのたたき台・画像生成、RPA（ROBOTANGO）で伝票チェック。定量目標欄に「作業効率が上がり、実働4時間→1時間75％の時間が削減された」（どの作業の値かは RPA 寄りの書き方で、生成AI 単独の効果とは書いていない）。**他県・宮崎の cases で未使用**（grep で確認）
  - **有限会社都城医科機器（都城市、卸売、従業員12名）** 卸売・小売 p7（R5事例）: 統合販売管理システム導入で労働生産性33.3％向上。AIは「3年目：AIによる適正在庫管理システム構築」の計画だけ。未使用
  - **三桜電設株式会社（延岡市、電気工事、従業員80名）** 建設 p5（R5事例）https://www.pref.miyazaki.lg.jp/documents/76534/76534_20250604084118-1.pdf : 年末調整・ワークフロー・電帳法対応、印刷コスト約50％削減。AI-OCRは今後の展望だけ。未使用
  - **株式会社アシストユウ（宮崎市、ベンダー）** 建設 p11（R2・R3事例）: AI移動式監視カメラ、監視員 1日3人→1人。ベンダー自身の事例。未使用
  - **スパークジャパン株式会社（宮崎市、ベンダー）** 情報通信 p6（R2・R3事例）https://www.pref.miyazaki.lg.jp/documents/76534/76534_20250604084332-1.pdf : RPA＆AI-OCRで手書き帳票の自動登録。数値なし。未使用
  - **株式会社ジェイエイフーズみやざき（西都市）** 農畜産 p11: 空撮データで「今後は…AIでの収量予測」（計画）。未使用
  - フェニックスリゾート株式会社（宮崎市、大企業とみられる）観光 p3: AIの語あり（料理残量の確認など、詳細は読んでいない）。未使用
  - すでに cases.md にあるもの: ＬＣトランス（都城市）・サニー・シーリング（都城市、2件）・丸栄宮崎・クリエイティブマシン（宮崎市）・アルバック機工（西都市）・坂下組（小林市）・浅野水産（日南市）・教育情報サービス（宮崎市、生成AIの添削動画）・スマイリング・パーク・宮崎トヨタ・クリエート（門川町）・ヤマエ食品工業・中園工業所・ニチワ・AGRIST
- **機構「日本のひなた宮崎人材育成事業」の採択（2026-10-23）**: モンド・コダマ・ムカサ企画室（ドローン・レーザーの鳥獣害対策）・サニー・シーリング・ミクロエース。AIの語はない
- 県の産業DX推進事業費補助金・物価高騰対策DX推進事業費補助金の**採択事業者の一覧は見つからなかった**（発展タイプの要領は「県のホームページで公開」と書くが、2026-11-04時点で掲載なし）。県のチラシの実装事例（勤怠・給与連携で関連業務 38時間/月→1時間/月、バス車両整備・管理システムで年1,573時間削減、計測作業の省力化80％、EC・在庫・販売連携で受注工数 24→16時間/日、商品登録自動化で年4,410時間）は事業者名なし
- 都城市 DXチャレンジプロジェクトの「過去採択事例」ページ（未見）

## 取れなかった項目・注意点

- WebSearch は subsidy_a・subsidy_b を合わせて12回（このファイルの分は県・機構・工業技術センター・都城市・日向市・採択一覧の10回）。自治体のサイトは curl（間隔を空けた）と WebFetch で開いた。ヘッダーの付け替えはしていない
- **日向市**: 公式サイトが 503 で、市の制度はすべて未確認（DX・生産性向上等設備導入事業補助金は二次情報）
- **宮崎県工業技術センター**: サイトに接続できず（curl 000・WebFetch 503）。技術相談・機器開放・AIの支援の有無を確かめていない
- **県の物価高騰対策DX推進事業費補助金の二次募集**: ページが404で、対象の事業と期間（8/7締切は検索の抜粋）を確かめられなかった
- **宮崎県賃上げ対応緊急支援金の締切**: プレスリリース 9/30 と県の支援策ページ 10/31 が食い違う
- **延岡市 元気な中小企業応援事業**: 公募期間のページが404（5/22〜6/22は二次情報）。DX・IT枠の対象経費の細目は要領を見ていない
- **都城市・小林市の中小企業大学校の受講料補助**: 補助率（都城市）・今年度の受付（両市）がページにない
- **機構の企業経営力アップ人材育成支援事業**: 令和8年度の要領が掲載されておらず、令和7年版の別表の率・上限で書いた。令和8年度の受付期間も分からない
- **宮崎市**: 「お知らせ」は18ページ中1ページ目だけ見た。企業支援制度集2025（PDF）は開いていない
- 九州経済産業局（kyushu.meti.go.jp）は shared.md のとおり403のため開いていない。国の出先機関・商工会議所の名前は gov 担当の確認を正とする
- 自治体コードは照合していない（stats 担当のコード26件一致を正とする）
