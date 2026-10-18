# 岩手県15町4村の補助金（AI・IT・DX・研修・創業・設備投資向け）2026年度

確認日: 2026-10-18。町村の公式サイトの産業・商工・事業者向けページ、補助金の要綱・募集要領・チラシのPDFで確認した。YAML は `subsidy_b.yml`（32制度）。岩手町（`iwate/iwate-town`）は県と同名のため、岩手町役場の制度だけを載せ、岩手県の制度は入れていない。

- 19町村とも、生成AIやAI研修を名指しで補助する町村独自の制度はない。
- 既存の中小企業がソフトウェア・システム・デジタル機器の導入に使える町村独自の制度を確認できたのは3町。
  - **山田町**「省力化対策支援事業費補助金」（令和8年度新規）。国の「デジタル化・AI導入補助金」または「中小企業省力化投資補助金」に2026-04-01以降に交付決定を受けた案件に、国の補助対象事業費の**1/5・上限60万円を上乗せ**。申請期限の記載なし（予算の範囲内）。
  - **葛巻町**「くずまき型持続可能な産業づくり支援事業費補助金」の**電子化推進事業**（1/2・上限50万円。ウェブコンテンツの強化、タブレット端末等の導入、電子マネー対応。1事業主体1回）。令和8年度の補助金一覧に「継続」で掲載。要綱の「商工業」に情報通信業は含まれない。
  - **大槌町**「地域基幹産業人材確保支援事業費補助金」の**DX推進事業**（1/2・上限1,000万円。データ管理システムの導入、加工ラインの自動化等。専門家謝金・委託料・備品）。**水産加工業に限る**。岩手県の沿岸地域基幹産業人材確保支援事業費補助金（DX推進事業）で事業計画が選定されていることが条件。2026年8月案内開始。
- 研修の受講料を対象にする町村独自の制度は5町村。**葛巻町**（ものづくり人材育成・経営品質向上事業。1/2・上限50万円）、**一戸町**（企業支援事業費補助金の人材育成支援。外部講師の社内研修・外部研修の受講料。2/3・上限30万円）、**岩手町**（新規雇用等研修費補助金。新規雇用者の研修。1/3・1人5万円・1事業所15万円）、**田野畑村**（新規起業等支援補助金の研修会等経費。受講料上限2万円）、**平泉町**（若者等人材育成支援事業補助金。資格取得。1/2・上限5万円）。
- 外部専門家・コンサルタントの費用を対象にするのは**葛巻町**（経営品質向上事業で中小企業診断士・経営コンサルタントの招聘。継業支援でも専門家費用）、**岩手町**（起業チャレンジ補助金の委託料にコンサル料・ホームページ作成料）、**洋野町**（創業支援補助金の専門家謝金・技術コンサルタント料）、**大槌町**（DX推進事業と6次産業化等の専門家謝金）。
- 創業向けの制度は12町村（雫石〔空き店舗〕・葛巻・岩手町・矢巾・西和賀・金ケ崎・平泉・大槌・山田・洋野・田野畑・野田）。岩手町・山田町・洋野町は第二創業・新事業、野田村は新分野進出、田野畑村は業務拡大も対象。山田町の創業サポートは委託・外注費に「システム開発及び運用保守」がある。洋野町・大槌町・山田町はパソコン等の汎用品を対象外と明記（山田町は目的外使用がないと整理できれば対象になり得る）。
- 今申請できる（締切が明示された受付期間中の）制度: **雫石町**のふるさとものづくり事業支援補助金（令和9年度分。2026-10-30締切、ふるさと財団の交付決定が前提）、**山田町**のやまだ創業サポート（商工会相談2026-10-30、町への申込2026-12-18締切）、**大槌町**の地場産業拡大支援施設整備補助金（2026-12-25締切、投資額5,000万円以上）。随時（予算の範囲内）は山田町の省力化対策・催事出展、葛巻町の3制度、岩手町の起業チャレンジ、平泉町の各制度、大槌町の起業人材育成・人材確保DX、洋野町・野田村の創業など。
- 締切済み: 山田町の新商品開発支援（2026-08-31）、軽米町の商品開発等促進（1次2026-06-12、2次2026-08-07）。
- 受付状況がページから判断できない制度（status: unknown）: 岩手町の新規雇用等研修費（ページ2024-11）、一戸町の企業支援事業費（ページ2025-09）、田野畑村の新規起業等支援（ページ2024-12）、矢巾町の創業支援（ページ2025-09、要綱は令和7年度版）、西和賀町の創業支援（対象期間が2026-03-31までの2025年度版のまま）、金ケ崎町の創業等支援（2021）・空き店舗（2019）・展示会出展（2024）、住田町の事業拠点整備（要綱2023）。
- 町村独自の制度（IT・DX・研修・創業向け）を確認できなかった町村: **紫波町**、**岩泉町**、**軽米町**（商品開発の補助だけ）、**九戸村**、**普代村**（起業支援事業補助金が村の助成制度一覧に名前だけある。詳細は二次情報のみ）。**住田町**は町外企業のサテライトオフィス開設の補助だけ。
- 岩手県の制度（物価高騰対策賃上げ支援金、地方創生起業支援金、いわて希望応援ファンドなど）と国の制度（業務改善助成金、地域雇用開発助成金など）は町村のページに案内があっても別担当のため載せていない。県の賃上げ支援金への町の上乗せ（金ケ崎町など）、信用保証料・利子補給、企業立地奨励金も補助金の対象外としてYAMLに入れていない（本文の町村ごとの「IT向けではない制度」に記した）。
- 予算残額を公開している町村はない。
- 商工会の名称・所在地・電話は、全国商工会連合会「全国各地の商工会WEBサーチ」の岩手県の検索結果（26件。https://www.shokokai.or.jp/search/ から岩手県で検索、結果は https://meibo.shokokai.or.jp/hpsearch/top/php/shoko_search.php ）による。URLは岩手県商工会連合会「商工会リンク集」https://www.shokokai.com/?p=shokokai による。19町村ともそれぞれの商工会がある（名簿の表記は「金ヶ崎町商工会」、リンク集の表記は「金ケ崎町商工会」）。
- 洋野町の公式サイトは https://www.town.hirono.iwate.jp/ 。葛巻町は www.town.kuzumaki.iwate.jp から www.town.kuzumaki.lg.jp に転送される。岩手町は town.iwate.iwate.jp（www なしに転送）。
- WebSearch は10回使用（上限16回）。

---

## 雫石町（iwate/shizukuishi）

**受付中の制度**
- **雫石町ふるさとものづくり事業支援補助金（令和9年度募集）**: 7/10以内（経費上限は新商品開発等1,500万円、販路開拓300万円）。ふるさと財団「ふるさとものづくり支援事業」の交付決定を受けた事業が対象で、町内に事業所を有する法人格のある団体。**2026-10-30（金）までに書類提出**（事前に町へ相談）。対象経費は謝金、旅費、原材料費、機械装置費、工具器具費、委託費、技術指導費、人件費、広報費など。
  https://www.town.shizukuishi.iwate.jp/docs/2026100500026/ 、概要 https://www.town.shizukuishi.iwate.jp/docs/2026100500026/file_contents/gaiyou.pdf
- **雫石町空き店舗活用事業費補助金**（随時・予算の範囲内）: 改装費1/2（商業地域・近隣商業地域は上限100万円、他は75万円）、家賃1/2・月3万円・最長1年。小売・飲食・生活関連サービス業。
  https://www.town.shizukuishi.iwate.jp/docs/2016060900028/
- **雫石町物産展等出展事業費補助金**（随時）: 県外の物産展等の出展料・運搬費・旅費の1/2・上限5万円、年度内2回まで。
  https://www.town.shizukuishi.iwate.jp/docs/2024022700029/

**確認したページ**
- 商工業振興: https://www.town.shizukuishi.iwate.jp/category/bunya/kurashi/sangyo/
- 就業・起業支援について（空き店舗補助と県の起業支援の案内だけ）: https://www.town.shizukuishi.iwate.jp/docs/2016080200078/

**IT向けではない制度**
- 企業の立地支援: https://www.town.shizukuishi.iwate.jp/docs/2023031300039/ （内容は未確認）
- 雫石町移住支援金（県と共同。起業する移住者を含む個人向け）: https://www.town.shizukuishi.iwate.jp/teijyu/docs/2023061500027/

**問い合わせ先**
- 町の窓口: 観光商工課 商工労政係 019-692-6497（直通）、観光商工課 019-692-6407
- 雫石商工会: 〒020-0527 岩手郡雫石町中町7番地4、TEL 019-692-3321、https://www.shokokai.com/shizukuishi/

---

## 葛巻町（iwate/kuzumaki）

**受付中の制度（随時・事業開始前に申請）**
- **くずまき型持続可能な産業づくり支援事業費補助金**: 事業メニュー別。**電子化推進事業 1/2・上限50万円**（ウェブコンテンツの強化、タブレット端末等の導入、電子マネー対応等。通信料金は除く。1事業主体1か年度限り）、ものづくり人材育成事業 1/2・50万円（技術習得の研修会への派遣・開催）、経営品質向上事業 1/2・50万円（サービス向上の研修、マーケティング、中小企業診断士・経営コンサルタントの招聘）、後継者育成事業 2/3・50万円、起業家支援事業 2/3・200万円、新分野開拓・連携支援事業 1/2・100万円、オフィス開設支援事業 1/3・100万円。事業開始の30日前までに申請。
  https://www.town.kuzumaki.lg.jp/docs/2015110600215/ 、要綱 https://www.town.kuzumaki.lg.jp/docs/2015110600215/file_contents/kuzumaki_zizoku_sangyou_shien-kouhuyoukou.pdf
- **葛巻町商店等設備導入支援事業費補助金**: 2/3・上限50万円。小売・飲食・生活関連サービス業を10年以上営む事業者の、販売・営業に直接使用する機器・設備（10万円以上）の導入・更新と店舗改修。
  https://www.town.kuzumaki.lg.jp/docs/2015110600208/
- **葛巻町継業支援事業費補助金**: 2/3・上限20万円。継業の経営診断・事業計画作成の専門家費用、後継者の募集・紹介・交渉、事業所登記。
  https://www.town.kuzumaki.lg.jp/docs/2018040600027
- 3制度とも「令和8年度商工業振興等関係補助金一覧」（2026-04-03公開）に「継続」として掲載: https://www.town.kuzumaki.lg.jp/docs/2025033100013/file_contents/R8_kuzumaki_syoukou_kannkou_hojokin.pdf

**IT向けではない制度**
- まちなかエリア賑わい創出事業費補助金（中心市街地の催事等。2/3・上限10万円）: https://www.town.kuzumaki.lg.jp/docs/2026042400026/
- 中小企業者等物価高騰対策省エネルギー設備導入支援補助金: https://www.town.kuzumaki.lg.jp/docs/2026040200017/ （内容は未確認）
- 中小企業振興資金融資・利子補給（年1.5%）・保証料全額補給（上の一覧PDF）
- 葛巻町いわて若者U・Iターン支援金（県の地方創生起業支援金の交付決定者等）: https://www.town.kuzumaki.lg.jp/docs/2026052600027 （WebSearchの要約で確認。ページ本文は未確認）

**問い合わせ先**
- 町の窓口: いらっしゃい葛巻推進課 商工観光担当 0195-65-8983
- 葛巻町商工会: 〒028-5402 岩手郡葛巻町葛巻第16地割1番地1、TEL 0195-66-2658、https://kuzumaki-shokokai.com/

---

## 岩手町（iwate/iwate-town）

※県と同名。以下は岩手町役場の制度。

**受付中の制度（随時）**
- **岩手町起業チャレンジ補助金**: 2/3（税抜）・上限100万円。新たに起業する人、第二創業、本店を岩手町に移転する町外事業者。委託料に**コンサル料、デザイン料、ホームページ作成料**、負担金に研修会参加費、備品購入費、店舗工事など。交付決定日からその年度の3月末まで。事業着手前に事前相談が必要。
  https://town.iwate.iwate.jp/town/business/challenge_busin/?v=cat-business&w=entrepreneurship&x=kigyo_subsidy 、要綱 https://town.iwate.iwate.jp/town/wp-content/uploads/2020/03/kigyou_charenge_youkou20260511.pdf

**受付状況が不明の制度**
- **岩手町新規雇用等研修費補助金**: 1/3・対象者1人5万円・1事業所15万円。従業員20名以下（商業・サービス業5名以下）の小規模事業者が、雇用3年以内の新規雇用者に受けさせる資格取得・研修の受講料・テキスト代・交通費・宿泊費。ページ更新2024-11-15。
  https://town.iwate.iwate.jp/town/business/shinkikenshu/?v=cat-business&w=koyou&x=subsidy

**確認したページ**
- 事業者向け: https://www.town.iwate.iwate.jp/town/business 、起業支援: https://town.iwate.iwate.jp/town/cat-business/entrepreneurship/ 、雇用（補助金・奨励金等）: https://town.iwate.iwate.jp/town/cat-business/koyou/ 、その他: https://town.iwate.iwate.jp/town/cat-business/others-jigyoshamuke/

**IT向けではない制度**
- 若年者雇用奨励金: https://town.iwate.iwate.jp/town/business/jakunenshoreikin-2/?v=cat-business&w=koyou&x=subsidy （内容は未確認）
- 企業誘致: https://town.iwate.iwate.jp/town/cat-business/kigyoyuchi/

**問い合わせ先**
- 町の窓口: みらい創造課 政策推進係（起業チャレンジ。内線218・219）、企画商工課 商工観光係（研修費。内線213・214）、岩手町役場 0195-62-2111（代表）
- 岩手町商工会: 〒028-4303 岩手郡岩手町大字江刈内第9地割65番地1、TEL 0195-62-2760、https://iwatemachishokokai.com/

---

## 紫波町（iwate/shiwa）

**受付中の制度**: なし（IT・DX・研修・創業向けの町独自の補助金は確認できなかった）

**確認したページ**
- 産業・仕事: https://www.town.shiwa.iwate.jp/sangyo/
- 企業支援・誘致（融資制度、セーフティネット保証、先端設備等導入計画、企業立地奨励条例、いわて産業振興センターの設備貸与制度の紹介など）: https://www.town.shiwa.iwate.jp/scene/121/122/2317.html/
- 起業（もりおかSDGsファンドへの出資、起業家塾＠もりおか、盛岡広域8市町の創業支援等事業計画の案内。町の補助金はない）: https://www.town.shiwa.iwate.jp/sangyo/kigyo_nariwai1/kigyo_nariwai2/9211.html/
- 雇用（職業訓練情報、就職活動交通費支援、中退共、雇用調整助成金）: https://www.town.shiwa.iwate.jp/sangyo/koyo1/koyo2/
- 産業・労働振興: https://www.town.shiwa.iwate.jp/sangyo/sinkou1/sinkou2/

**IT向けではない制度**
- 企業立地に対する奨励金等制度（紫波町企業立地奨励条例）: https://www.town.shiwa.iwate.jp/sangyo/kigyo1/kigyo2/7836.html
- 紫波町中小企業振興資金融資制度（「企業支援・誘致」のページ内）

**問い合わせ先**
- 町の窓口: 商工観光課 商工観光係 019-672-6913（直通）
- 紫波町商工会: 〒028-3305 紫波郡紫波町日詰字東裏85番地4 紫波町商工会館、TEL 019-672-2244、https://www.shokokai.com/shiwa/

---

## 矢巾町（iwate/yahaba）

**受付状況が不明の制度**
- **矢巾町創業支援事業補助金**: 家賃1/2（月4万円まで）、地代1/2（月6万円まで）、最長2年。開業2年以内。いわて産業振興センターか矢巾町商工会の起業指導が必要。ページ更新2025-09-18、要綱のファイル名は令和7年度。
  https://www.town.yahaba.iwate.jp/soshiki/sangyou/kankousangyou/2018042000054/

**確認したページ**
- 産業観光課「観光・産業」: https://www.town.yahaba.iwate.jp/soshiki/sangyou/kankousangyou/

**IT向けではない制度**
- 矢巾町インターンシップ促進助成金（町内企業でインターンシップを行う学生個人への交通費・宿泊費。事業者向けではない）: https://www.town.yahaba.iwate.jp/soshiki/sangyou/kankousangyou/2021100100016/
- 矢巾町中小企業者物価高騰対策支援金（法人向け。申請期限を12月まで延長）: https://www.town.yahaba.iwate.jp/soshiki/sangyou/kankousangyou/176974149828137/ （内容は未確認）
- 矢巾町中小企業振興資金融資制度: https://www.town.yahaba.iwate.jp/soshiki/sangyou/kankousangyou/2016021000156/
- 補助金ではないが、矢巾町地域産業育成お役立ちセンターの事業者向けセミナー「中小企業若手・中堅職員向け研修（2026年11月〜2027年2月）」と起業・新事業相談窓口がある: https://www.town.yahaba.iwate.jp/soshiki/sangyou/kankousangyou/17684363922615/ 、https://www.town.yahaba.iwate.jp/soshiki/sangyou/kankousangyou/175740711027894/

**問い合わせ先**
- 町の窓口: 産業観光課 商工振興係 019-611-2602
- 矢巾町商工会: 〒028-3615 紫波郡矢巾町大字南矢幅第8地割261番地、TEL 019-697-5111、https://www.shokokai.com/yahaba/

---

## 西和賀町（iwate/nishiwaga）

**受付状況が不明の制度**
- **西和賀町創業支援事業費補助金**: 2/3（創業支援塾修了者は3/4）・上限150万円。施設設備等の取得（建物の改修を含む）。年度内創業か創業1年以内、西和賀商工会または金融機関の指導を受けた事業計画。ページ更新2025-04-28で、対象期間が「令和8年3月31日まで」（2025年度分）のまま。
  https://www.town.nishiwaga.lg.jp/gyosei_shigoto_sangyo/sangyoshinko/2/3344.html 、要綱 https://www.town.nishiwaga.lg.jp/material/files/group/11/_1.pdf

**確認したページ**
- 行政・しごと・産業: https://www.town.nishiwaga.lg.jp/gyosei_shigoto_sangyo/index.html
- 産業振興: https://www.town.nishiwaga.lg.jp/gyosei_shigoto_sangyo/sangyoshinko/index.html 、起業・創業支援（上の1件だけ）: https://www.town.nishiwaga.lg.jp/gyosei_shigoto_sangyo/sangyoshinko/2/index.html

**問い合わせ先**
- 町の窓口: 観光商工課（湯田庁舎）0197-82-3290
- 西和賀商工会: 〒029-5512 和賀郡西和賀町川尻40地割73番地11 西和賀町複合型商工会館2階、TEL 0197-82-2270、https://www.shokokai.com/nishiwaga/

---

## 金ケ崎町（iwate/kanegasaki）

**受付状況が不明の制度**（いずれも予算の範囲内、ページに受付期間の記載なし）
- **金ケ崎町創業等支援事業補助金**: 2/3（39歳以下の若者・女性は9/10）・上限50万円。土地・建物の賃借・購入、増改築・改修、設備・備品の購入・賃借、広告宣伝。既存事業者の町内新事業所設置も「創業等」に含む。商工会の事業計画確認書と商工会加入が必要。ページは2021-04-01のまま。
  https://www.town.kanegasaki.iwate.jp/articles/2021040100039/
- **金ケ崎町空き店舗活用補助金**: 改装・設備工事の1/2・上限100万円。対象業種に**情報通信業**を含む。ページは2019年のまま。
  https://www.town.kanegasaki.iwate.jp/docs/2019031500036/
- **金ケ崎町展示会出展事業費補助金**: 製造業の展示会出展の1/2・1件10万円、年度内2回まで。ページ更新2024-04-01。
  https://www.town.kanegasaki.iwate.jp/docs/2018011200065/

**確認したページ**
- 商業・工業: https://www.town.kanegasaki.iwate.jp/categories/bunya/sangyou/shokogyo/ 、創業支援: https://www.town.kanegasaki.iwate.jp/categories/bunya/sangyou/sogyosien/

**IT向けではない制度**
- 中小企業者等物価高騰対策賃上げ支援事業補助金（県の物価高騰対策賃上げ支援金の交付決定者への町の上乗せ。申請先は金ケ崎町商工会、受付2026-06-01〜12-28）: https://www.town.kanegasaki.iwate.jp/articles/2026021600027/
- 自動車産業振興（車両購入）事業補助金: https://www.town.kanegasaki.iwate.jp/articles/2022052000034/ （内容は未確認）
- 補助金ではないが、令和8年度「かねがさき創業塾」: https://www.town.kanegasaki.iwate.jp/articles/2026083100015/

**問い合わせ先**
- 町の窓口: 商工観光課 0197-42-2111（代表）
- 金ケ崎町商工会: 〒029-4503 胆沢郡金ケ崎町西根伊勢分23番地5 JR金ケ崎駅2階、TEL 0197-42-2710、https://www.shokokai.com/kanegasaki/

---

## 平泉町（iwate/hiraizumi）

**受付中の制度（随時）**: 町の「R8年度 商工業者融資・補助金制度チラシ（R8.4.1〜）」による。要綱はサイトで公開されていない。
- **起業・事業承継支援事業補助金**: 1/2・上限50万円（U・I・Jターン者は100万円）。単価10万円以上の設備・備品、法人登記、知的財産登録、広告宣伝、技術指導受入。
- **空き店舗等対策事業補助金（R8拡充）**: 賃借料1/2・月3万円・最大12か月、改修1/2・上限300万円（中尊寺通り・毛越寺通りで特に寄与する場合3/4）。
- **特産品開発支援事業補助金**: 1/2・上限50万円。商品名に「平泉」を冠すること。
- **取引支援促進事業費補助金**: 県外の展示会・見本市の出展経費、上限20万円（補助率の記載なし）。
- **人材育成支援事業補助金**（若者等人材育成支援事業補助金）: 資格取得の受講料・受験料・初回登録料の1/2・上限5万円。https://www.town.hiraizumi.iwate.jp/%E5%B9%B3%E6%B3%89%E7%94%BA%E8%8B%A5%E8%80%85%E7%AD%89%E4%BA%BA%E6%9D%90%E8%82%B2%E6%88%90%E6%94%AF%E6%8F%B4%E4%BA%8B%E6%A5%AD%E8%A3%9C%E5%8A%A9%E9%87%91-24114/
  ページ「中小企業支援・創業支援」（更新2026-04-20）: https://www.town.hiraizumi.iwate.jp/%e4%b8%ad%e5%b0%8f%e4%bc%81%e6%a5%ad%e6%94%af%e6%8f%b4%e3%83%bb%e5%89%b5%e6%a5%ad%e6%94%af%e6%8f%b4-20620/ 、チラシPDF https://hi-hp-production.s3.ap-northeast-1.amazonaws.com/wp-content/uploads/2025/05/18145530/%E3%80%90%E9%85%8D%E6%9E%B6%E4%BE%9D%E9%A0%BC%E3%80%91R8%E7%94%BA%E8%9E%8D%E8%B3%87%E3%83%BB%E8%A3%9C%E5%8A%A9%E9%87%91%E3%83%81%E3%83%A9%E3%82%B7%EF%BC%88%E4%BF%AE%E6%AD%A3%EF%BC%89.pdf

**確認したページ**
- 商工業振興: https://www.town.hiraizumi.iwate.jp/category/tourism-industry/commerce-industry-promotion/

**IT向けではない制度**（同じチラシ）
- 店舗等リフォーム促進支援事業補助金（1/2・上限50万円）
- 地域企業経営強化支援事業費補助金（工場・事業所の増設。固定資産投資額の5%以内・上限2,000万円）
- 働き方改革企業支援奨励金（働き方改革の認定を新たに受けた企業に10万円）: https://www.town.hiraizumi.iwate.jp/%E5%B9%B3%E6%B3%89%E7%94%BA%E5%83%8D%E3%81%8D%E6%96%B9%E6%94%B9%E9%9D%A9%E4%BC%81%E6%A5%AD%E6%94%AF%E6%8F%B4%E5%A5%A8%E5%8A%B1%E9%87%91-23868/
- 移住定住促進家賃補助金（従業員個人向け）、平泉町中小企業振興資金（融資・利子補給2%）

**問い合わせ先**
- 町の窓口: 観光商工課 0191-46-5572、kanko@town.hiraizumi.iwate.jp
- 平泉商工会: 〒029-4102 西磐井郡平泉町平泉字志羅山152番地2、TEL 0191-46-3560、https://www.shokokai.com/hiraizumi/

---

## 住田町（iwate/sumita）

**受付状況が不明の制度**
- **住田町事業拠点整備支援事業費補助金**: 限度額100万円（要綱に補助率の記載なし）。**町内に本社・事業所を持たない**法人・個人事業主が、空き物件でテレワーク用のサテライトオフィス等を開設する経費（改装、通信機器の敷設、パソコン・電話機・複合機等の取得または12か月分の借用、12か月分の家賃）。町内の既存事業者は対象外。要綱は令和5年4月1日施行。
  https://www.town.sumita.iwate.jp/ijyu/support.html 、要綱 https://www.town.sumita.iwate.jp/_files/00002219/jigyoukyoten.pdf

**確認したページ**
- 事業者の方へ（入札・税・広告募集など。補助金の掲載なし）: https://www.town.sumita.iwate.jp/bunya/jigyousha/
- 事業者へのお知らせ: https://www.town.sumita.iwate.jp/bunya/jigyoshanews/
- 観光・産業（林業・農業の補助が中心）: https://www.town.sumita.iwate.jp/bunya/kanko/
- 農林商工課（農政商工）: https://www.town.sumita.iwate.jp/soshiki/nousei/ 、企画財政課: https://www.town.sumita.iwate.jp/soshiki/kikaku/

**IT向けではない制度**
- 住田町企業立地優遇制度（企業設置奨励金＝固定資産税相当額、雇用促進奨励金＝新規雇用1人10万円・上限1,000万円）: 上の移住・定住サポートのページ
- 地域活性化起業人（企業派遣型）の募集（町が企業から人材を受け入れる制度で、補助金ではない）: https://www.town.sumita.iwate.jp/docs/2026071700012/

**問い合わせ先**
- 町の窓口: 農林商工課（農政商工）、住田町役場 0192-46-2111（代表）
- 住田町商工会: 〒029-2311 気仙郡住田町世田米字世田米駅33番地、TEL 0192-46-2311、https://www.shokokai.com/sumita/

---

## 大槌町（iwate/otsuchi）

**受付中の制度**
- **大槌町地域基幹産業人材確保支援事業費補助金**（2026年8月案内開始、随時）: **DX推進事業 1/2・上限1,000万円**（DX推進の設備投資に係る専門家謝金・委託料・備品。データ管理システムの導入等）、女性が働きやすい職場環境整備事業 1/2・上限200万円。**水産加工業**の事業者に限る。DX推進事業は県の沿岸地域DX推進事業の計画選定が条件。
  https://www.town.otsuchi.iwate.jp/gyosei/docs/463636.html
- **大槌町起業人材育成支援補助金**（随時）: 1/2・上限100万円（備品は25万円まで）。起業・出店・事業承継。許可取得・検査、**講習受講料**、専門家報酬（司法書士等）、広告宣伝、備品（汎用品は除く）。
  https://www.town.otsuchi.iwate.jp/gyosei/docs/437830.html
- **大槌町6次産業化推進事業等補助金**（随時、ページは2020年更新）: 新商品開発・既存商品改良は50%・上限30万円、6次産業化は80%・上限40万円、農商工連携80%・上限30万円。専門家等への謝金も対象。
  https://www.town.otsuchi.iwate.jp/gyosei/docs/433404.html
- **大槌町地場産業拡大支援施設整備補助金**: 施設整備費5,000万円以上（農業・水産養殖業は2,000万円以上）の施設新設・増設。製造業・ソフトウェアは1/4・上限1億5千万円。**公募2026-09-03〜12-25**。
  https://www.town.otsuchi.iwate.jp/gyosei/docs/442671.html

**確認したページ**
- 企業支援・企業立地: https://www.town.otsuchi.iwate.jp/gyosei/sangyo/keiei/ 、商工業: https://www.town.otsuchi.iwate.jp/gyosei/sangyo/shoko/

**IT向けではない制度**
- 建設業応援補助金（令和8年度）: https://www.town.otsuchi.iwate.jp/gyosei/docs/461442.html （内容は未確認）
- 大槌町産木材流通促進事業補助金: https://www.town.otsuchi.iwate.jp/gyosei/docs/374565.html
- 復興特区法の開発研究用資産減税（税制）: https://www.town.otsuchi.iwate.jp/gyosei/docs/448016.html

**問い合わせ先**
- 町の窓口: 産業振興課 商工観光係 0193-42-8725
- 大槌商工会: 〒028-1111 上閉伊郡大槌町新町38番1、TEL 0193-42-2536、https://www.shokokai.com/otsuchi

---

## 山田町（iwate/yamada）

**受付中の制度**
- **山田町省力化対策支援事業費補助金**（令和8年度新規、随時）: 国の「デジタル化・AI導入補助金」「中小企業省力化投資補助金」の採択案件（2026-04-01以降の交付決定）に、補助対象事業費の**1/5・上限60万円**を上乗せ。
  https://www.town.yamada.iwate.jp/docs/10124.html 、要綱 https://www.town.yamada.iwate.jp/fs/1/3/9/3/8/5/_/syouryokukataisaku_youryou.pdf
- **令和8年度やまだ創業サポート事業費補助金**: 2/3（若者・女性5/6）・上限50万円。起業、第二創業、新事業。備品（3万円以上50万円未満、汎用事務備品は除く）、広告宣伝、印刷製本、**委託・外注費（システム開発及び運用保守を含む）**、出展、旅費。**商工会への相談期限2026-10-30、町への申込期限2026-12-18**。
  https://www.town.yamada.iwate.jp/docs/2549.html
- **やまだの特産品販路拡大事業（催事等出展支援補助金）**（令和8年度新規、随時）: 町外の商談会・物産展等の出展費の1/2・通算20万円。
  https://www.town.yamada.iwate.jp/docs/9961.html

**締切済み**
- **山田町新商品開発支援事業費補助金**: 新商品開発・改良1/2（返礼品登録3/4）・上限50万円、設備導入1/3・上限500万円。募集2026-04-24〜08-31。
  https://www.town.yamada.iwate.jp/docs/7344.html

**確認したページ**
- 事業者支援: https://www.town.yamada.iwate.jp/jigyousya/jigyousyashien/

**IT向けではない制度**
- 山田町運輸事業者運行支援緊急対策事業: https://www.town.yamada.iwate.jp/docs/8652.html
- 移住支援金の対象法人募集: https://www.town.yamada.iwate.jp/docs/1972.html

**問い合わせ先**
- 町の窓口: 商工観光課 0193-82-3111（代表）
- 山田町商工会: 〒028-1351 下閉伊郡山田町長崎三丁目6番18号、TEL 0193-82-2515、https://www.shokokai.com/yamadamachi/

---

## 岩泉町（iwate/iwaizumi）

**受付中の制度**: なし（IT・DX・研修・創業向けの町独自の補助金は確認できなかった）

**確認したページ**
- 事業者向け: https://www.town.iwaizumi.lg.jp/category/attribute/business/
- 商工業（創業支援等事業計画、特定創業支援等事業の証明、機械類貸与補給補助金の3件）: https://www.town.iwaizumi.lg.jp/category/attribute/business/syoukou/
- その他事業者向け情報: https://www.town.iwaizumi.lg.jp/category/attribute/business/other/ 、補助金・助成金: https://www.town.iwaizumi.lg.jp/category/attribute/life/hojo-josei/
- 町のサイトに掲載されている創業向けの案内は岩手県の地方創生起業支援金（https://www.town.iwaizumi.lg.jp/docs/2026042300074 、2次公募 https://www.town.iwaizumi.lg.jp/docs/2026062900025 ）といわて希望応援ファンド（https://www.town.iwaizumi.lg.jp/docs/2026052500013 ）で、町の制度ではない（WebSearchの結果で確認）

**IT向けではない制度**
- 中小企業整備機械類貸与補給補助金（いわて産業振興センターの設備貸与の貸付損料に5年間2.0%以内の利子補給）: https://www.town.iwaizumi.lg.jp/docs/2016021700049/
- 中小企業者等業務用省エネ電気製品買替支援事業補助金（エアコン・冷蔵庫等の買替1/2・上限15万円。買替2026-04-01〜10-31、申請2026-11-30まで）: https://www.town.iwaizumi.lg.jp/docs/2026031800011
- 創業支援等事業計画: https://www.town.iwaizumi.lg.jp/docs/2019122600010/

**問い合わせ先**
- 町の窓口: 経済観光交流課 経済商工室 0194-22-2111（内線553）
- 岩泉商工会: 〒027-0501 下閉伊郡岩泉町岩泉字中野40番地42 岩泉観光センター、TEL 0194-22-3245、https://www.shokokai.com/iwaizumi/

---

## 軽米町（iwate/karumai）

**締切済み**
- **軽米町商品開発等促進事業補助金**: 2/3・商品開発／ブラッシュアップ上限20万円、販路開拓上限10万円。1次2026-04-13〜06-12、2次2026-07-08〜08-07（審査会8-25）。
  https://www.town.karumai.iwate.jp/article/jigyosha/entry-basename-11.html 、1次 https://www.town.karumai.iwate.jp/article/jigyosha/entry-basename-6.html

IT・DX・研修・創業向けの町独自の制度は確認できなかった。

**確認したページ**
- 事業者の方へ: https://www.town.karumai.iwate.jp/article/jigyosha/index.html

**IT向けではない制度**
- 町中小企業振興資金融資制度: https://www.town.karumai.iwate.jp/article/jigyosha/sangyoyuchi/entry-basename-10.html
- 軽米町新規求職者等地域雇用促進奨励金: https://www.town.karumai.iwate.jp/article/jigyosha/sangyoyuchi/entry-basename-5.html
- 軽米町物価高騰対策賃上げ支援金、中小企業者等エネルギー価格高騰対策支援金、運輸事業者等緊急対策支援金（いずれも物価高騰対策。受付状況は未確認）

**問い合わせ先**
- 町の窓口: 産業振興課 商工観光担当 0195-46-4746
- 軽米町商工会: 〒028-6302 九戸郡軽米町大字軽米第4地割47番地 軽米町商工会館、TEL 0195-46-2711、https://www.shokokai.com/karumai/

---

## 洋野町（iwate/hirono）

**受付中の制度（随時）**
- **洋野町創業支援補助金**: 4/5・創業は上限80万円、新事業の創出は上限50万円。設備等購入・借用（2万円以上）、**専門家謝金**、旅費、印刷製本、研究開発費（**技術コンサルタント料**を含む）、委託費（デザイン、調査）、広告宣伝。**パソコン、プリンタ、タブレット、モニター等は対象外**。2026-04-01に要綱改正。
  https://www.town.hirono.iwate.jp/doc/2021020500033/

**確認したページ**
- 事業者・生産者の方へ: https://www.town.hirono.iwate.jp/navi/jigyosha/
- 商工業: https://www.town.hirono.iwate.jp/category/bunya/sangyo/shokogyo/ 、企業立地・雇用支援: https://www.town.hirono.iwate.jp/category/bunya/sangyo/shien/ 、デジタル（事業者向けの補助金はない）: https://www.town.hirono.iwate.jp/category/bunya/digital/

**IT向けではない制度**
- 中小企業退職金共済掛金補助金: https://www.town.hirono.iwate.jp/doc/2020041300080/
- 新卒者ふるさと定着奨励金: https://www.town.hirono.iwate.jp/doc/2020040700027/
- 業務改善助成金（国の制度の案内）: https://www.town.hirono.iwate.jp/doc/2021020800034/

**問い合わせ先**
- 町の窓口: 特定政策推進室（種市庁舎）0194-65-2102（創業支援）、洋野町役場 種市庁舎 0194-65-2111（代表）
- 洋野町商工会: 〒028-7914 九戸郡洋野町種市第23地割27番地1、TEL 0194-65-4111、https://www.shokokai.com/hirono/

---

## 一戸町（iwate/ichinohe）

**受付状況が不明の制度**
- **一戸町企業支援事業費補助金**: 2/3・上限30万円。人材育成支援＝**外部講師による社内研修の謝金・旅費、外部研修の受講料・旅費**。人材確保支援＝就職イベント出展、企業PRパンフレット、**ホームページの作成・更新**、企業紹介動画、求人掲載、就職活動旅費の補助。ページ更新2025-09-25で受付期間の記載なし。
  https://www.town.ichinohe.iwate.jp/shigoto_sangyo/koyo_shugyo/3692.html

**確認したページ**
- しごと・産業: https://www.town.ichinohe.iwate.jp/shigoto_sangyo/index.html
- 中小企業等支援（町中小企業振興資金融資制度の1件だけ）: https://www.town.ichinohe.iwate.jp/shigoto_sangyo/sangyoshinko/2/index.html

**IT向けではない制度**
- 一戸町奨学金返還支援補助金【事業者向け】: https://www.town.ichinohe.iwate.jp/shigoto_sangyo/koyo_shugyo/6400.html （内容は未確認）
- 税制優遇: https://www.town.ichinohe.iwate.jp/shigoto_sangyo/kaihatsu_toshikeikaku/1361.html

**問い合わせ先**
- 町の窓口: 産業建設部 商工観光課 0195-33-4855
- 一戸町商工会: 〒028-5312 二戸郡一戸町一戸字砂森119番地3 一戸町商工会館、TEL 0195-33-2354、https://www.shokokai.com/ichinohe/

---

## 田野畑村（iwate/tanohata）

**受付状況が不明の制度**
- **田野畑村新規起業等支援補助金**: 新規起業等経費（施設改修、設備備品〔汎用品は除く〕、広告費等）は2/3・上限50万円。**研修会等経費（資格取得・スキルアップの研修の受講料・テキスト代は上限2万円、交通費・宿泊費は1/2・上限3万円）**。村内に住所がある、新規起業意欲のある人・起業／事業承継3年以内の人・新たな事業展開や業務拡大に意欲のある人など。ページの日付2024-12-01で受付期間の記載なし。要綱は非公開。
  https://www.vill.tanohata.iwate.jp/docs/2023040200047/
  - 補助金ポータル（https://hojyokin-portal.jp/subsidies/69062 等）は令和8年度分を2026-04-01から受付と掲載しているが二次情報（secondary、記事では使わない）。

**確認したページ**
- 行政情報TOP: https://www.vill.tanohata.iwate.jp/top.html 、各課からのお知らせ: https://www.vill.tanohata.iwate.jp/bunya/kakuka/ 、行政情報: https://www.vill.tanohata.iwate.jp/bunya/gyousei/ 、サイトマップ: https://www.vill.tanohata.iwate.jp/sitemap/ （事業者向けのカテゴリがなく、上の制度はWebSearchで見つけた）

**問い合わせ先**
- 村の窓口: 企画観光課（ページの所管）、田野畑村役場 0194-34-2111（代表）
- 田野畑村商工会: 〒028-8407 下閉伊郡田野畑村和野532番地13、TEL 0194-34-2304、https://www.shokokai.com/tanohata/

---

## 普代村（iwate/fudai）

**受付中の制度**: なし（村のページで詳細を確認できる制度はない）

**確認したページ**
- 普代村の助成制度（ページの日付2021-04-19）: https://www.vill.fudai.iwate.jp/docs/306.html 。「起業・雇用・事業者支援」に「起業支援事業補助金：村内で新規に起業する商工業者に対し、補助します」とあるが、補助率・上限・受付期間の記載はない。同じ欄に新卒者等雇用促進奨励金、小規模企業経営改善資金利子補給、中小企業振興資金利子補給、信用保証料補給。
- 農林商工課: https://www.vill.fudai.iwate.jp/soshiki/nourin/ （2ページとも商工の補助金の記事なし）、行政情報: https://www.vill.fudai.iwate.jp/gyousei/

**二次情報のみ（secondary、記事では使わない）**
- 普代村起業支援事業補助金: 補助金ポータル https://hojyokin-portal.jp/subsidies/53570 によると、商工分野の起業・第二創業が対象で2/3・上限200万円、対象経費は委託費・借料・設備購入費、申請期間は2024-04-01〜2025-03-31（公募終了）。2026年度の実施は未確認。

**問い合わせ先**
- 村の窓口: 農林商工課 0194-35-2115
- 普代商工会: 〒028-8332 下閉伊郡普代村第9地割字銅屋13番2 普代村役場内、TEL 0194-35-2132、https://www.shokokai.com/fudai/

---

## 野田村（iwate/noda）

**受付中の制度（随時）**
- **野田村地域新事業チャレンジ応援補助金**: 2/3・個人／団体は上限50万円、法人は上限300万円。村内の農林漁業・商工業での起業・事業の再生・創出・新分野進出。販売促進、施設の整備・改修、**機械・器具等の導入**、営業許可、特産品開発。要綱・受付期間の記載なし。
  ページ「企業向け支援について」（更新2026-08-14）: https://www.vill.noda.iwate.jp/soshiki/sangyoshinkoka/suisanshokohan/chushokigyoshien/680.html

**確認したページ**
- 産業・仕事: https://www.vill.noda.iwate.jp/sangyo_shigoto/index.html 、中小企業支援: https://www.vill.noda.iwate.jp/sangyo_shigoto/chushokigyoshien/index.html
- 各種補助事業のお知らせ: https://www.vill.noda.iwate.jp/gyoseijoho/kakusyuhozyozigyounoosirase/index.html （WebSearchの結果で確認。本文は未確認）

**IT向けではない制度**（同じ「企業向け支援について」のページ）
- 野田村企業立地補助金（製造業・ソフトウェア業等の工場新増設。投資額500万円以上・新規雇用5人以上等）、企業・立地奨励補助金（ソフトウェア業等の賃借料1/2・月5万円）、新卒者ふるさと雇用支援奨励金、工場設置奨励、広域連携雇用促進補助金
- 中小企業被災資産復旧事業費補助金: https://www.vill.noda.iwate.jp/sangyo_shigoto/chushokigyoshien/963.html

**問い合わせ先**
- 村の窓口: 産業振興課 水産商工班 0194-78-2926
- 野田村商工会: 〒028-8201 九戸郡野田村大字野田第19地割117番地、TEL 0194-78-2012、https://www.shokokai.com/noda/

---

## 九戸村（iwate/kunohe）

**受付中の制度**: なし（IT・DX・研修・創業向けの村独自の補助金は確認できなかった）

**確認したページ**
- 九戸で仕事（農業支援・林業の村単独補助・薪ストーブ等）: https://www.vill.kunohe.iwate.jp/work/
- 産業振興課（農林業の補助、漬物製造業継続支援など）: https://www.vill.kunohe.iwate.jp/gyousei/40_nourin/
- 企業誘致: https://www.vill.kunohe.iwate.jp/docs/91.html （内容は未確認）

**IT向けではない制度**
- 九戸村移住支援金（県と共同。東京圏からの移住者で、県の起業支援金の交付決定を受けた人等。個人向け）: https://www.vill.kunohe.iwate.jp/docs/1071.html （補助金ポータルの掲載で確認。ページ本文は未確認）
- 漬物製造業継続支援: https://www.vill.kunohe.iwate.jp/docs/2210.html （内容は未確認）

**問い合わせ先**
- 村の窓口: 産業振興課、九戸村役場 0195-42-2111
- 九戸村商工会: 〒028-6502 九戸郡九戸村大字伊保内第11地割47番地1、TEL 0195-42-2230、https://www.shokokai.com/kunohe/
