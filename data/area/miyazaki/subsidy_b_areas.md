# 宮崎県 14町3村の補助金（AI・IT・DX・設備・研修・販路）2026年度

確認日: 2026-11-04。17町村の公式サイトで、事業者向け・しごと・産業・商工業の分類ページと商工担当課の記事一覧を開き（curl でページのリンクと題名を一覧にし、補助・助成・支援の記事は本文を curl か WebFetch で読んだ）、都農町は例規集の交付要綱、五ヶ瀬町は「令和8年度五ヶ瀬町補助金等一覧」PDF で確かめた。**県の支援施策データベースや補助金ポータルだけでは判断していない。**

- 17町村とも、**AI・生成AI・IT導入・DX研修を名指しして補助する町村独自の制度は見つからなかった**。
- IT・デジタルに使える可能性がある町村の制度（`subsidy_b.yml`、5件）:
  - **美郷町（宮崎県東臼杵郡）商工業設備投資支援事業**: 対象事業に「生産性向上／ICT活用事業」、2/3・100万円（町内の業者からの購入、美郷町商工会の会員）。**既存事業者の令和8年度の要望調査は終了**（新規開業者は随時）
  - **都農町 商工業振興対策基金事業補助金**: 新技術導入支援事業（業務の効率化・省力化の技術導入、固定資産税の課税対象の設備・機械類で100万円超、1/2・300万円）、販路開拓支援事業（ホームページ等作成費を含む、1/2・50万円）。都農町商工会の会員が要件。**町のサイトが JavaScript だけで描かれ、募集案内・受付期間を確かめられなかった（unknown）**
  - 高原町 中小企業大学校の受講料補助（補助額・期間の記載なし、2020年のページ）、川南町 商工業振興支援事業補助金（店舗・設備・備品 1/2・50万円、2020年のページ、受付期間の記載なし）
- 町村の制度はあるが IT 向けではないもの: 三股町（融資・退職金共済・先端設備等導入計画・デジタルスタンプラリー〔町の事業〕）、国富町（融資・創業・住宅リフォーム）、綾町（空き家・空き店舗活用型チャレンジ支援・介護人材）、高鍋町（事業承継・引継ぎ応援・物価高騰対策〔医療・福祉施設〕）、木城町（事業承継・プレミアム商品券）、門川町（融資・企業立地・地域ブランド認定）、高千穂町（店舗改修・新規開業、2022年のページ）、五ヶ瀬町（新規開業・特産品開発・事業所改修 1/3・20万円・事業継承・人づくり支援〔研修会・視察〕）、西米良村（事業者向けは入札・農林業だけ）、諸塚村（商工業事業者育成支援〔新規開業・後継者の施設整備・新規雇用〕）
- **国・県の補助金への上乗せ（addon）: 17町村とも該当なし。**
- 町村の事業者も使える県の制度（産業DX推進事業費補助金・「稼ぐ力」強化支援など）は2026年度分がすべて終了（`subsidy_a.yml`）。無料の相談は宮崎県よろず支援拠点（生産性向上支援センター・よろずAI相談会）、産業DXサポートセンター。

## 三股町（mimata）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 行政情報 https://www.town.mimata.lg.jp/main 、しごと・産業 https://www.town.mimata.lg.jp/categories/index/shigoto_sangyou
- 商工 https://www.town.mimata.lg.jp/categories/index/syoukou （10件）: セーフティネット保証、みまたん創業スクール、中小企業等特別融資制度、生活応援商品券、中小企業・小規模企業振興基本条例、道の駅・物産館周遊デジタルスタンプラリー、先端設備等導入制度、企業立地の特別措置、中小企業退職金等共済制度加入促進事業、飲食店応援プロジェクト
- 労働 https://www.town.mimata.lg.jp/categories/index/roudou （5件、最低賃金・合同就職説明会）、就職（2件）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 三股町役場（商工担当課の名前は確かめていない）

## 高原町（takaharu）

**IT向けの制度**
- 中小企業大学校の受講料補助だけ（yml: miyazaki-takaharu-chusho-daigakko。補助額・期間の記載なし）。

**見たページ**
- しごとの情報 > 産業振興 https://www.town.takaharu.lg.jp/life/2/10/ 、企業支援 https://www.town.takaharu.lg.jp/life/2/10/42/ （2件：工業団地、中小企業大学校の受講料補助）、雇用・労働支援 https://www.town.takaharu.lg.jp/life/2/10/41/ （企業ガイドブック）、商工観光課の記事一覧 https://www.town.takaharu.lg.jp/soshiki/34/ （観光が中心）
- 「従業員のレベルアップに！中小企業大学校の受講料補助を実施しています！」https://www.town.takaharu.lg.jp/soshiki/34/5208.html （2020-04-01更新）
- 結論: 町独自の AI・IT 導入の補助は見つからなかった

**相談窓口**: 高原町 商工観光課 商工観光係（0984-42-2128）

## 国富町（kunitomi）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 産業・観光 https://www.town.kunitomi.miyazaki.jp/main/tourism/ 、商工業 https://www.town.kunitomi.miyazaki.jp/main/tourism/commerce/ （8件：小規模事業者融資、企業誘致奨励措置、創業支援事業計画、よろず支援拠点、事業承継、創業応援、住宅リフォーム補助、特定技能の共生施策）
- 「宮崎県産業振興機構『生産性向上支援センター：稼ぐ力現場づくりチーム』について」http://www.town.kunitomi.miyazaki.jp/main/tourism//page002544.html : 小規模事業者向けのセミナー・個別相談会。リーフレット4種に「生成AI活用」。補助金ではない（**gov 担当向け**）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 国富町 総合戦略課 企業商工係（0985-75-3126）

## 綾町（aya）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- しごとの情報 https://www.town.aya.miyazaki.jp/life/2/2/ 、商工業 https://www.town.aya.miyazaki.jp/life/2/2/36/ （空き家・空き店舗活用型チャレンジ支援事業補助金、宮崎県UIJターン就活応援補助金、求人案内ほか）
- 総合政策課の記事一覧 https://www.town.aya.miyazaki.jp/soshiki/sougouseisakuka/ （約60件。商工は中小企業退職金共済・空き店舗チャレンジ・企業版ふるさと納税など）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 綾町 総合政策課

## 高鍋町（takanabe）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 事業者・産業・農業 https://www.town.takanabe.lg.jp/jigyosha/index.html 、商工業の振興 https://www.town.takanabe.lg.jp/jigyosha/2874.html 、地域政策課 商工業の記事一覧 https://www.town.takanabe.lg.jp/soshiki/chiikiseisaku/6/syoukougyou/index.html （6件：最低賃金、宮崎県未来成長企業、よろず支援拠点、事業承継・引継ぎ応援事業補助金、よろずコワーキングキャラバン、中小企業退職金共済）
- 手続き・届出・制度 https://www.town.takanabe.lg.jp/jigyosha/tetuzuki_todokede_seido/index.html : 「高鍋町物価高騰対策事業補助金」https://www.town.takanabe.lg.jp/jigyosha/tetuzuki_todokede_seido/4846.html （2026-10-05更新、医療機関・社会福祉施設等の負担軽減、11/30まで）。IT 向けではない
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 高鍋町 地域政策課

## 新富町（shintomi）

**IT向けの制度**
- 見つからなかった（2026年度）。**町のサイトに商工業の分類ページがなく、確認の範囲が狭い。**

**見たページ**
- 産業・ビジネス https://www.town.shintomi.lg.jp/sangyo_business/index.html （開発・建築、広告、農業・林業・水産業、入札・契約だけで、商工業の分類がない）、サイトマップ https://www.town.shintomi.lg.jp/sitemap.html 、組織一覧 https://www.town.shintomi.lg.jp/soshiki/index.html 。産業振興課 https://www.town.shintomi.lg.jp/soshiki/sangyoshinko/index.html の記事一覧は1件（システムメンテナンス）しか出ない（JavaScript で描くとみられる）
- WebSearch（町のドメインに限定、1回）: 事業者向けの令和8年度の補助金のページは出なかった。令和5年度の実施計画書 https://www.town.shintomi.lg.jp/material/files/group/3/40768302.pdf に商工業振興補助金（販路拡大・新商品開発）・創業支援補助金・中小企業退職金共済の掛金助成が載る（抜粋のみ、開いていない）
- 結論: AI・IT 導入・研修の補助は見つからなかったが、**「制度なし」と断定しない**（産業振興課 商工係に確かめる。area-todo 向け）

**相談窓口**: 新富町 産業振興課

## 木城町（kijo）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- しごと・産業 https://www.town.kijo.lg.jp/sigoto_sangyou/index.html 、商工業 https://www.town.kijo.lg.jp/sigoto_sangyou/sangyousinkou/index.html （事業承継に要する費用の補助、プレミアム商品券、かしのみ2階の市場調査、企業誘致、新型コロナの中小企業支援策）、雇用・就業 https://www.town.kijo.lg.jp/sigoto_sangyou/koyou_syuugyou/index.html （介護職員等人材確保・育成、ハローワーク求人）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 木城町 産業振興課

## 川南町（kawaminami）

**IT向けの制度**
- 商工業振興支援事業補助金（店舗・設備・備品、1/2・50万円。2020年のページで受付期間の記載なし。yml: miyazaki-kawaminami-shoko-shinko）だけ。IT・AIの記載はない。

**見たページ**
- しごと https://www.town.kawaminami.miyazaki.jp/life/2/ 、産業振興 https://www.town.kawaminami.miyazaki.jp/life/2/15/ 、就労支援 https://www.town.kawaminami.miyazaki.jp/life/2/15/74/
- 産業推進課の記事一覧 https://www.town.kawaminami.miyazaki.jp/soshiki/7/ （約60件）: 「重点支援地方交付金活用事業：川南町商工業振興支援事業補助金について」https://www.town.kawaminami.miyazaki.jp/soshiki/7/1442.html （2020-12-22更新）、企業立地促進制度、事業承継支援、特産品送料助成金（2026-03-31で終了、「類似の町単独事業の予定はない」）、プレミアム付地域通貨、中小企業退職金共済、ポリテクセンター延岡の案内
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 川南町 産業推進課 商工水産係（0983-27-8011）

## 都農町（tsuno）

**IT向けの制度**
- 商工業振興対策基金事業補助金の新技術導入支援事業（業務の効率化・省力化の設備、1/2・300万円）・販路開拓支援事業（ホームページ等作成費を含む、1/2・50万円）（yml: miyazaki-tsuno-shingijutsu / miyazaki-tsuno-hanro）。受付状況は確かめられなかった。

**見たページ**
- 公式サイト https://www.town.tsuno.lg.jp/ （宮崎県都農町。高知県津野町とは別）は Angular の単一ページアプリで、curl で取れる HTML に本文・リンクがなく（接続リセットも1回）、WebFetch でもタイトルしか取れなかった。**募集案内のページは開けなかった**
- WebSearch（町のドメインに限定、1回）で例規集の要綱を見つけ、curl で本文を読んだ: 「都農町商工業振興対策基金事業補助金交付要綱」https://www.town.tsuno.lg.jp/reiki/reiki_honbun/q632RG00000541.html （平成26年要綱第28号、最新の改正は令和7年4月1日施行、令和9年3月31日限り失効。別表第1：規模拡大・販路開拓・新技術導入・新規起業）、「都農町農業・商工業リーダー育成支援事業補助金交付要綱」https://www.town.tsuno.lg.jp/reiki/reiki_honbun/q632RG00000655.html （住民・住民の団体の視察研修の交通費・宿泊費・研修費の50％。事業者の社員研修向けではないので yml に入れていない）。ほかに中小企業保証料補助、ローカルスタートアップ支援（WALT計画の採択事業者）、地域おこし協力隊起業支援（いずれも IT 向けではない）
- 結論: 町独自の AI 導入の補助はない。業務効率化・省力化の設備と HP 作成に使える基金事業がある（受付時期は町・都農町商工会に確かめる。area-todo 向け）

**相談窓口**: 都農町役場（担当課の名前は確かめていない）、都農町商工会（0983-25-0200、要綱の別表第2）

## 門川町（kadogawa）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 観光・産業 > 産業 https://www.town.kadogawa.lg.jp/industry/industry/ （25件：中小企業特別融資制度、企業立地促進制度、先端設備等導入制度、よろず支援拠点、地域ブランド認定商品、水産・林業）、事業者向けのお知らせ https://www.town.kadogawa.lg.jp/news/business/ （10件）
- 「第２期チャレンジ・応援門川ラボ事業（令和８～１０年度）業務委託 公募型プロポーザル」https://www.town.kadogawa.lg.jp/news/business/page005592.html : 町の委託事業の募集で、内容（事業者支援・デジタル支援の有無）はページに書かれていない（仕様書 PDF は開いていない）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 門川町 企画戦略課（まちづくり政策係 0982-63-1140）

## 美郷町（misato-town-miyazaki）

宮崎県東臼杵郡美郷町（秋田県美郷町・島根県美郷町・宮城県美里町・熊本県美里町とは別）。

**IT向けの制度**
- 美郷町商工業設備投資支援事業補助事業（対象事業に「生産性向上／ICT活用事業」、2/3・100万円。既存事業者の令和8年度の要望調査は終了。yml: miyazaki-misato-setsubi-toshi）。

**見たページ**
- 入札・契約・産業・就労・事業 https://www.town.miyazaki-misato.lg.jp/list00104.html 、農林水産業・商工業 https://www.town.miyazaki-misato.lg.jp/list00125.html 、商工業 https://www.town.miyazaki-misato.lg.jp/list00460.html 、雇用・労働 https://www.town.miyazaki-misato.lg.jp/list00124.html
- 「商工振興」https://www.town.miyazaki-misato.lg.jp/kiji003353/index.html （最終更新2025-12-02）: 1 商工会設備資金利子補給、2 中小企業退職金共済制度補助、3 商工業制度資金利子補給、4 移動販売運営補助（1kmあたり37円・上限50万円）、5 商工業設備投資支援事業
- ほかに過疎地域の特別償却・固定資産税の課税免除、創業支援等事業計画、よろず支援拠点
- 結論: AI を名指しした補助はないが、ICT活用の設備投資の補助がある（今年度の既存事業者分は終了）

**相談窓口**: 美郷町商工会（本所 0982-66-2023、南郷支所 0982-59-0106、北郷支所 0982-62-5895。町の委託事業者）

## 高千穂町（takachiho）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 産業 https://www.town-takachiho.jp/top/sangyo/index.html 、商工業 https://www.town-takachiho.jp/top/sangyo/shoko/index.html （4件：既存店舗改修支援と新規開業支援の補助事業〔2022-11-24更新〕、特別融資制度、たかちほ再生支援利子補給金、国土利用計画法の届出）、しごと・雇用 https://www.town-takachiho.jp/top/sangyo/shigoto/index.html （2件）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 高千穂町役場（商工担当課の名前は確かめていない）

## 日之影町（hinokage）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 産業・まちづくり https://www.town.hinokage.lg.jp/categories/sangyou-machidukuri/ 、商工 https://www.town.hinokage.lg.jp/categories/sangyou-machidukuri/shoukou/ （2件：企業立地の優遇措置、ひのかげ渓谷まつり2026）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 日之影町役場（商工担当課の名前は確かめていない）

## 五ヶ瀬町（gokase）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- サイトマップ https://www.town.gokase.miyazaki.jp/sitemap.html 、事業者の方へ https://www.town.gokase.miyazaki.jp/jigyousha/index.html （税・介護保険の様式だけ）
- 「令和8年度五ヶ瀬町補助金一覧」https://www.town.gokase.miyazaki.jp/chousei/hozyokin/2227.html （2026-04-20更新）の PDF https://www.town.gokase.miyazaki.jp/material/files/group/2/hojyokin.pdf （約70制度）: 事業者向けは新規開業支援（1/2、工事費100万円・備品40万円・広告宣伝費30万円）、特産品開発（1/2・40万円、返礼品開発50万円）、事業所改修支援（1/3・20万円）、事業継承・引継ぎ応援（2/3・50万円）、人づくり支援事業（研修会・講演会 10/10・50万円、視察研修 2/3。団体向けとみられる）、介護人材確保。IT 機器の語は園芸農業支援（農業向け）にだけ出る
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 五ヶ瀬町役場（商工担当課の名前は確かめていない）

## 西米良村（nishimera）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 事業者の皆さまへ https://www.vill.nishimera.lg.jp/village/category/b-00-businessperson （入札・農業・林業・様式ダウンロード。商工の分類はない。記事は森林整備計画・農地法・入札・木質バイオマス・企業版ふるさと納税など）
- 結論: 村独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 西米良村役場

## 諸塚村（morotsuka）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- しごと・産業 https://www.vill.morotsuka.miyazaki.jp/shigoto-sangyo/index.html 、商工業 https://www.vill.morotsuka.miyazaki.jp/shigoto-sangyo/shokogyo/index.html （1件）
- 「諸塚村商工業事業者育成支援事業について」https://www.vill.morotsuka.miyazaki.jp/shigoto-sangyo/shokogyo/521.html （2026-01-29更新）: 新規開業支援（1/2・300万円）、後継者商業基盤支援（1/2・50万円）、新規雇用促進（給与等 1/3・30万円）。店舗の新築・改築・設備の更新が対象で、IT・研修・販路の記載はない（受付期間の記載なし）。要綱 https://www.vill.morotsuka.miyazaki.jp/material/files/group/3/125.pdf は開いていない
- ほかに「ForestNotes×諸塚村」の Web サイト公開、もろっこはうすのオンラインショップ（村の物産施設）
- 結論: 村独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 諸塚村 企画創生課（地域DX・情報発信室、0982-65-1116）

## 椎葉村（shiiba）

**IT向けの制度**
- 見つからなかった（2026年度）。**村のサイトに事業者向けの分類ページがなく、確認の範囲が狭い。**

**見たページ**
- トップ https://www.vill.shiiba.miyazaki.jp/ 、行政情報 https://www.vill.shiiba.miyazaki.jp/admin.php （計画・財政の一覧。商工業の補助の記事はない）、申請書ダウンロード https://www.vill.shiiba.miyazaki.jp/promote/download.php （住民向けの様式だけ）
- 例規集（https://public1.legalcrud.com/shiiba_vill/reiki/index.html ）は開いていない
- 結論: AI・IT 導入・研修の補助は見つからなかったが、**「制度なし」と断定しない**（村役場に確かめる。area-todo 向け）

**相談窓口**: 椎葉村役場

---

## 取れなかった項目・注意点

- WebSearch は subsidy_a と合わせて12回（このファイルの分は新富町・都農町の2回）。町村のサイトは curl（間隔を空けた）と WebFetch で読んだ。ヘッダーの付け替えはしていない
- **都農町**: 公式サイトが JavaScript だけで描かれ、募集案内・受付期間・担当課を確かめられなかった（要綱だけで書いた）
- **新富町**: 商工業の分類ページがなく、産業振興課の記事一覧も1件しか出ない。町の商工業振興補助金の令和8年度の内容は分からない
- **椎葉村**: 事業者向けの分類ページがなく、例規集も開いていない
- **高原町・川南町**: 制度のページが2020年のままで、今年度の実施・受付は分からない
- 三股町・綾町・高鍋町・木城町・高千穂町・日之影町・五ヶ瀬町・西米良村は、商工担当課の名前を確かめていないところがある（相談窓口の欄）
- 町村の商工会の独自の補助金・セミナーは確かめていない。商工会の名前は町村のページに出たもの（美郷町商工会、都農町商工会）だけで、ほかは gov 担当の確認を正とする
- 自治体コードは照合していない（stats 担当を正とする）
