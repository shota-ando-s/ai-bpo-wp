# 秋田県（県・あきた企業活性化センター・中央会）と13市の AI・IT 向け補助金（2026-10-18 確認）

データ本体は `subsidy_a.yml`（21件、すべて公式で確認。県の食のリーディングカンパニー育成支援事業だけは県の手引きで確認し、受付状況は unknown）。「受付中」「随時」でも予算に達すると締め切られる。

2026-10-18時点で受付中（open）・随時（rolling）は次の15件。
- 受付中: 県 中小企業デジタル化導入支援事業費補助金（4次、10/23締切）、秋田市 賃上げ基盤強化支援（11/30まで）、能代市 ICT技術等導入支援（2027/1/31まで）、大館市 DX推進（事業承認10/30まで）、由利本荘市 イノベーション創出支援（2027/3/31まで）、潟上市 稼げる力創出（年4回、次は10月末）、潟上市 ワーキングスキルアップ（2027/2/28まで）
- 随時: 県 中核人材育成支援、能代市 地元企業人材育成、横手市 設備導入支援、鹿角市 DX推進、鹿角市 産業人材育成（2027/3/12まで）、由利本荘市 働きやすいまちづくり（職場環境改善）、大仙市 生産性向上支援、北秋田市 資格取得支援

**国の補助金（デジタル化・AI導入補助金など）への県・市の上乗せ**: 見つからない。県のデジタル化補助金は「国又は県の他の補助金等の採択を受けていないこと」（実施要領 第5条）、秋田市は同様の目的の補助金と併用不可、大仙市は他の補助金で交付決定を受けていない事業が対象、北秋田市（終了）は国・県の補助分を経費から引く方式で、いずれも上乗せではない。

## 秋田県（県・あきた企業活性化センター・中央会）

見たページ:
- 県「【4次募集のお知らせ】中小企業デジタル化導入支援事業費補助金」https://www.pref.akita.lg.jp/pages/archive/94185 （2026-09-04更新）、実施要領・Q&A（2026-09-04版）・3次募集チラシ
- 県「令和8年度 中小企業等支援施策の手引き」https://www.pref.akita.lg.jp/pages/archive/41735 （2026-07-15更新、PDFは2026年7月版。県とあきた企業活性化センターの令和8年度の施策の一覧）。県の補助金はこの手引きと、各ページの「経営基盤、競争力の強化を図りたい」の一覧、商工業振興課 https://www.pref.akita.lg.jp/pages/genre/18801 、産業人材育成 https://www.pref.akita.lg.jp/pages/genre/11683 から拾った
- 中核人材育成支援事業 https://www.pref.akita.lg.jp/pages/archive/80891 、ものづくり経営戦略強化支援事業 https://www.pref.akita.lg.jp/pages/archive/63563 と採択 https://www.pref.akita.lg.jp/pages/archive/98739 、商業・サービス産業省エネ化等推進事業費補助金 https://www.pref.akita.lg.jp/pages/archive/94135

**今年度受付中**
- 中小企業デジタル化導入支援事業費補助金（yml: akita-digital-donyu）: 4次募集 2026-09-04〜10-23 17時必着。2/3以内、30万〜100万円。会計・顧客管理・RPA・グループウェアなどのクラウドサービス、ソフトウェア、セキュリティ対策。サブスク・リースは補助対象期間（2026-11-01〜2027-02-28）分のみ
  - **対象外の業種**（実施要領 第3条・別表1）: 製造業（大分類E）全部、農業・林業（農業サービス業・園芸サービス業・素材生産業・林業サービス業は対象）、漁業、金融業・保険業（保険媒介代理業・保険サービス業は対象）、病院・一般診療所・歯科診療所、社会保険・社会福祉・介護事業（中分類85）、風俗営業・競輪競馬等・興信所・集金業・易断所・宗教・政治経済文化団体
  - **AIについて**: 県のページ・実施要領・Q&Aに「AI」の語はない。対象は「クラウドサービス等を利用して業務効率化や生産性向上を図ろうとする事業」（Q&A A9）で、SaaS型のAIツールは当たりうるが、記事では「AIツールが対象になるかは県に確認」と書く
  - 今年度は追加募集・3次募集（2026-07-07〜08-31）に続く4回目。要領の別表2の補助対象期間「令和８年２月２８日まで」はページの令和9年2月28日と食い違う（要領の誤記とみられる）
- 中核人材育成支援事業（yml: akita-chukaku-jinzai）: 入社5年以内・35歳未満の大卒者等の高度な研修・資格取得に1/2・上限100万円。2026-07-17に通年（随時）受付に変更、予算到達で終了

**今年度は終了**
- ものづくり経営戦略強化支援事業（yml: akita-monodukuri-senryaku）: 製造業。システム構築費・研修費を含む。2026-05-26〜07-16、10者採択
- 商業・サービス産業省エネ化等推進事業費補助金（yml: akita-shoene-shoryoku）: 非製造業の省エネ・省力化設備。2/3、100万〜1,000万円。2026-03-09〜04-30
- ものづくり革新総合支援事業（省エネ生産設備更新型）: 製造業の省エネ・省力化設備、2/3・200万〜1,000万円、2026-03-09〜04-30、56者採択 https://www.pref.akita.lg.jp/pages/archive/66756 。生産設備の更新で、AI・ITの導入向けではないためymlに入れていない

**受付状況が分からない**
- デジタルを活用した食のリーディングカンパニー育成支援事業（yml: akita-shoku-leading）: 食品製造・卸の中小企業。2/3・年1,000万円。事業経費の10％以上をAI・IoT等に投資することが条件。手引きでは募集「令和8年5月〜（予定）」。募集ページ（archive/95788）と募集要項PDFは2026-10-18時点で開けない（ページが見つからない・404）

**ymlに入れなかった県の制度**
- 商業・サービス産業経営革新事業費補助金 https://www.pref.akita.lg.jp/pages/archive/64856 は令和6年度（2024-04-22〜05-31）のページしかなく、令和8年度の手引きにも載っていない
- はばたく中小企業投資促進事業補助金 https://www.pref.akita.lg.jp/pages/archive/33190 は工場立地・増設の設備投資（1億円以上）向け
- 秋田県スキルアップ促進奨励金 https://www.pref.akita.lg.jp/pages/archive/94456 は国の専門実践教育訓練を受講する個人向け（1/4・上限5万円、2026-04-01〜2027-03-19）で、企業向けではない
- プロフェッショナル人材活用（DX人材枠は人材紹介手数料の1/2・上限100万円、2026-04-01〜2027年2月末）・副業兼業人材活用（DX枠1/2・上限30万円）は人材の採用・受入れの費用で、手引きでのみ確認（個別ページは開いていない）
- 賃上げ緊急支援事業は最低賃金引上げへの支援金（受付は令和8年1月〜6月〔予定〕と県のチラシ）。AI・IT向けではなく、中身は開いていない
- 地域商業販売力強化プロジェクト補助金 https://www.pref.akita.lg.jp/pages/archive/94818 は商業団体のプレミアム商品券・集客事業向け（窓口は中央会、2026-10-08〜11-30）

**無料の支援・研修（補助金ではない）**
- 地域密着型DX支援事業（県 産業DX推進チーム）: ICT企業・商工団体・金融機関と連携し、課題分析・DX戦略策定・アクションプランの作成と実行を伴走支援。募集 2026-06-02〜11-30（予定数に達し次第終了）。手引き45ページ
- 先進デジタル技術活用促進プログラム事業（県 産業DX推進チーム）: 生成AI等の基礎研修（オンライン）と実践研修（対面）、無料、2026年10〜11月予定（手引き43ページ）。行政AIの担当からの情報では、県の生成AI活用セミナー（10/23〜11/6）は受付終了
- 画像認識AIプログラミング研修 https://www.pref.akita.lg.jp/pages/archive/95947 : 2026-10-22（木）9:00〜15:00、秋田県産業技術センター、県内中小企業9社（1社2名まで）、無料（2026-09-03更新）
- 県産品振興課の食品事業者向け「テーマ別セミナー」（AI活用による事務効率化など、2回予定）（手引き）
- あきた企業活性化センター https://www.bic-akita.or.jp/ : 令和8年度の補助金はあきた農商工応援ファンド（農林漁業者との連携による新商品開発、申請 2026-10-13〜11-30）https://www.bic-akita.or.jp/subsidy/1755/ と海外出願支援だけで、AI・IT導入向けはない（助成金一覧 https://www.bic-akita.or.jp/subsidy/ ）。県内企業未来共創チャレンジ支援プログラム（モデル企業募集 2026-10-13〜11-10、外部との共創による新事業の3か年支援）https://www.bic-akita.or.jp/other/9382/ 、専門家派遣、設備貸与あり
- 秋田県中小企業団体中央会 https://www.chuokai-akita.or.jp/ : 助成事業 https://www.chuokai-akita.or.jp/jyosei は組合向け（組合等情報ネットワークシステム等開発事業〔全国中央会、6/10以内・上限1,158万8千円〕、活路開拓事業など）。令和9年度の助成事業の希望申請は2026-09-18で締切。「アカデミック・ブリッジ講座」（DX入門講座を含む）の案内あり（中身は開いていない）。1社で申請できるAI・IT導入の補助金はない

## 秋田市（akita/akita-city）

**市独自の制度あり（受付中）**: 秋田市中小企業賃上げ基盤強化支援事業費補助金（yml: akita-city-chinage）
- https://www.city.akita.lg.jp/jigyosha/keieisogyo-support/1034826.html （2026-05-18更新）。申請 2026-04-01〜11-30、予算上限で終了
- 申請要領 https://www.city.akita.lg.jp/_res/projects/default_project/_page_/001/034/826/8yoryo.pdf ・交付要綱 https://www.city.akita.lg.jp/_res/projects/default_project/_page_/001/034/826/8yoko.pdf ・よくあるご質問 https://www.city.akita.lg.jp/_res/projects/default_project/_page_/001/034/826/8qa.pdf で確認: 目的は「設備導入およびＡＩなどを活用したＤＸ推進」。補助率1/2以内、上限は設備導入事業100万円・デジタル推進事業50万円。デジタル推進事業の例は「ＡＩを活用して原材料の発注・在庫管理を行い業務効率化を図る」。対象経費はソフトウェア等（単価3万円以上）、専門業者（アドバイザー）への委託費、DX推進のための研修費。サブスク・リースは対象外。要件は2025-09-10以降の時給80円以上の引上げなど
- 根拠として見た一覧: 「経営・創業サポート」https://www.city.akita.lg.jp/jigyosha/keieisogyo-support/index.html 、「雇用・労働支援」https://www.city.akita.lg.jp/jigyosha/koyo-rodo-support/index.html
- 秋田市資格取得助成事業補助金 https://www.city.akita.lg.jp/jigyosha/koyo-rodo-support/1007124.html は個人向けが中心で、正規雇用者の事業所申請は建設運輸関係資格と技能検定だけ。AI・IT向けではないためymlに入れていない

**相談窓口**: 秋田市 産業振興部 商工貿易振興課（秋田市山王一丁目1番1号 本庁舎3階、018-888-5726、商工振興担当 018-888-5728）

## 能代市（akita/noshiro）

**市独自の制度あり（2件とも受付中・随時）**
- 能代市中小企業等ICT技術等導入支援補助金（yml: noshiro-ict）: 市の専門家（無料）の診断を踏まえたICT導入（ソフトウェア・クラウド・機器）に1/2・上限100万円。2026-04-01〜2027-01-31の随時募集、プレゼン審査あり https://www.city.noshiro.lg.jp/sangyo/shogyo/hojo/21434 （2026-10-16更新）
- 能代市地元企業人材育成支援事業費補助金（yml: noshiro-jinzai）: 従業員の資格取得の受講料・受験料の1/2、年20万円まで https://www.city.noshiro.lg.jp/sangyo/shogyo/hojo/12461
- 根拠として見た一覧: 「各種補助制度について」https://www.city.noshiro.lg.jp/sangyo/shogyo/hojo/ 、「産業・まちづくり」https://www.city.noshiro.lg.jp/sangyo/
- 能代市事業者生産性向上等支援事業 https://www.city.noshiro.lg.jp/sangyo/shogyo/hojo/26814 は市内の製造業の製造設備の導入・改修（1/2、導入200万円・改修100万円）で、事務用機器は対象外。AI・IT向けではないためymlに入れていない（申請期間は開いていない。実績報告は2026-12-28まで）

**相談窓口**: 能代市 環境産業部 商工労働課（能代市上町1番3号、商工労働係 0185-89-2186、産業立地推進室 0185-89-2924、syokou@city.noshiro.lg.jp）

## 横手市（akita/yokote）

**AI・IT導入に特化した市独自の補助金はない。生産設備に付随するソフトウェアが対象になる設備導入補助がある**
- 横手市中小企業活性化支援事業（中小企業設備導入支援補助金）（yml: yokote-setsubi）: 先端設備等導入計画に基づく生産設備と付随ソフトウェア（10万円以上）の1/2・上限200万円、随時 https://www.city.yokote.lg.jp/syoukougyo/1004371/1004474.html
- 根拠: 令和8年度版「横手市商工業関係の助成制度」https://www.city.yokote.lg.jp/syoukougyo/1001356/1009246.html （2026-08-31更新、14制度。DX・AI・研修向けの補助金はない）、「企業向け支援・助成金」https://www.city.yokote.lg.jp/syoukougyo/1004371/index.html
- IT・ソフトウエア関連企業立地優遇制度助成金は立地企業向けで、中身は開いていない

**相談窓口**: 横手市 商工観光部 商工労働課（横手市中央町8番12号 かまくら館5階、0182-32-2115、shoko@city.yokote.lg.jp）

## 大館市（akita/odate）

**市独自の制度あり（受付中）**: 物価高騰対策 中小事業者DX推進事業費補助金（yml: odate-dx）
- ソフトウェア・クラウドの購入費・利用料（初年1年分）、専門家経費。コンサル指導なし1/2・上限100万円、指導あり3/4・上限150万円、工場の通信機器1/2・上限300万円 https://www.city.odate.lg.jp/city/soshiki/shokou/p10744
- 事業承認申請は2026-10-30まで、交付申請は11-30まで。2026-10-18時点でページと令和8年4月のチラシに受付終了の記載はない。令和8年度のチラシには「予算枠に達した段階で受付を終了」の文言がない（同じページの令和6年1月のチラシにはある）。行政AIの担当が見た検索結果の要約の「予算到達で終了」は、令和6年のチラシの文言か二次情報とみられ、一次情報で今年度の予算到達は確認できない

**相談窓口**: 大館市 産業部 商工課 商工係（大館市字中城20番地、0186-43-7071、syoko@city.odate.lg.jp）

## 男鹿市（akita/oga）

**市独自のAI・IT導入・DX・研修向けの補助金は見つからない**
- 根拠: 「商工業」https://www.city.oga.akita.jp/living_information/shigoto_sangyo/shokogyo/index.html （融資あっせん、空き店舗、販路拡大支援、先端設備等導入計画、立地企業サポート、中小企業省エネ対策等支援）、「各種制度・申請」https://www.city.oga.akita.jp/living_information/shigoto_sangyo/kakushuseido_shinsei/index.html
- 中小企業省エネ対策等支援事業 https://www.city.oga.akita.jp/living_information/shigoto_sangyo/shokogyo/7347.html （2026-04-17更新）は省エネ設備の更新か新事業の設備の購入費の2/3（製造業200万円・非製造業100万円）で、ソフトウェアは対象に書かれていない。ymlに入れていない
- 男鹿市就業資格取得支援助成金 https://www.city.oga.akita.jp/living_information/shigoto_sangyo/kakushuseido_shinsei/1603.html は個人（求職者・学生・在職者・個人事業主）と旅客運送事業者の二種免許向け

**相談窓口**: 男鹿市 男鹿まるごと売込課 エネルギー・商工港湾班（男鹿市船川港船川字泉台66-1、0185-24-9143）

## 湯沢市（akita/yuzawa）

**AI・IT導入に特化した市独自の補助金はない。設備投資の補助は今年度の受付終了**
- 湯沢市ふるさと企業振興補助金（yml: yuzawa-furusato-kigyo）: 先端設備等導入計画に基づく設備・ソフトウェアの1/2・上限200万円、資格取得支援など。見出しが「（申請受付は終了しました）」（2026-10-01更新）https://www.city-yuzawa.jp/soshiki/46/4650.html
- 根拠: 【令和8年度版】湯沢市商工業者のための事業支援ガイドブック https://www.city-yuzawa.jp/soshiki/45/4808.html （目次にDX・IT導入の補助金はない）、「補助金等支援」https://www.city-yuzawa.jp/life/2/16/120/
- つくる力売る力向上支援事業補助金 https://www.city-yuzawa.jp/soshiki/45/1622.html は経営革新計画等に基づく新商品開発・販路開拓向け（ページの更新は2024-04-01）。ふるさと企業基幹技術継承支援補助金 https://www.city-yuzawa.jp/soshiki/45/4838.html は基幹技術者の給与の補助。ゆざわTECH WOMAN Plus（IT人材育成事業）https://www.city-yuzawa.jp/soshiki/46/6005.html は募集終了（中身は開いていない）

**相談窓口**: 湯沢市 産業振興部 商工課（湯沢市佐竹町1番1号 本庁舎2階、0183-73-2135、0183-55-8186）

## 鹿角市（akita/kazuno）

**市独自の制度あり（2件とも随時）**
- 鹿角市中小企業DX推進事業費補助金（yml: kazuno-dx）: 市の中小企業魅力開発アドバイザーの指導でDX実行計画を策定する事業者のソフトウェア購入・利用料・専門家経費を1/2、20万〜50万円 https://www.city.kazuno.lg.jp/shigoto_sangyo/chusyokigyo/1/11691.html
- 鹿角市産業人材育成支援事業費補助金（yml: kazuno-jinzai）: 資格試験・研修の受講料等の1/2、年20万円まで、2027-03-12まで https://www.city.kazuno.lg.jp/shigoto_sangyo/chusyokigyo/1/3538.html
- **「中小企業魅力向上事業」（行政AIの担当からの問い合わせ）について**: 市のページでは「女性・若者魅力ある企業づくり支援事業」https://www.city.kazuno.lg.jp/shigoto_sangyo/chusyokigyo/1/11693.html （2026-04-10更新）。市（鹿角工業振興会）が中小企業魅力開発アドバイザーを置いて行う事業で、①かづの産業未来創造会の「中小企業魅力向上戦略」に基づくモデル事業、②かづの人づくり塾、③生成AIを活用した業務改善の個別伴走支援とコミュニティ形成。**企業に交付する補助金ではなく、市が直接行う支援事業**。企業への補助は、この事業で指導を受けた企業が使う上記のDX推進事業費補助金。2026年度の事業費400万円とふるさと納税（企業版を含む）の財源は、このページでは確認できなかった
- 根拠として見た一覧: 「企業支援・人材育成」https://www.city.kazuno.lg.jp/shigoto_sangyo/chusyokigyo/1/index.html

**相談窓口**: 鹿角市 商工振興課 商工班（鹿角市花輪字荒田4番地1、0186-30-0250）

## 由利本荘市（akita/yurihonjo）

**市独自の制度あり（受付中・随時）**
- イノベーション創出支援事業（yml: yurihonjo-innovation）: 新分野参入・既存技術の新結合などのシステム構築・クラウド利用料・専門家・研修の1/2・上限50万円、2026-04-01〜2027-03-31 https://www.city.yurihonjo.lg.jp/1001504/1002137/1003477.html
- 働きやすいまちづくり支援事業費補助金（yml: yurihonjo-hatarakiyasui）: 職場環境改善の「業務効率化ツールの導入」（ソフトウェア・クラウドサービスの料金）などに1/3・上限50万円 https://www.city.yurihonjo.lg.jp/1001504/1002136/1003367.html
- 根拠として見た一覧: 「商工業」https://www.city.yurihonjo.lg.jp/1001504/1002137/index.html 、「雇用・労働」https://www.city.yurihonjo.lg.jp/1001504/1002136/index.html 、「産業・ビジネス」https://www.city.yurihonjo.lg.jp/1001504/index.html
- 資格取得支援助成金 https://www.city.yurihonjo.lg.jp/1001504/1002136/1003369.html は市民個人向け（特定一般教育訓練・介護・自動車免許等、1/3・上限4万円）

**相談窓口**: 由利本荘市 産業振興部 商工振興課（由利本荘市尾崎17番地 本庁舎3階、0184-24-6372）

## 潟上市（akita/katagami）

**市独自の制度あり（2件とも受付中）**
- 中小企業等稼げる力創出補助金（yml: katagami-kasegeru）: 売上10％以上向上の多角化等の取組（システム購入費を含む）に1/2・単独上限500万円。年4回受付（4月末・7月末・10月末・1月末）https://www.city.katagami.lg.jp/soshiki/sangyoushinkoubu/shoukoukankoushinkouka/kigyoushien/tyuusyoukigyoutoushien/4091.html
- ワーキングスキルアップ支援助成金（yml: katagami-skillup）: 従業員の資格取得の受講料等（情報処理技術者などを含む）を1人5万〜8万円、2027-02-28まで https://www.city.katagami.lg.jp/soshiki/sangyoushinkoubu/shoukoukankoushinkouka/kigyoushien/tyuusyoukigyoutoushien/4117.html
- 根拠として見た一覧: 「補助金・助成金支援」https://www.city.katagami.lg.jp/soshiki/sangyoushinkoubu/shoukoukankoushinkouka/kigyoushien/tyuusyoukigyoutoushien/index.html 、「企業支援班」https://www.city.katagami.lg.jp/soshiki/sangyoushinkoubu/shoukoukankoushinkouka/kigyoushien/index.html
- 事業者ECサイト活用補助金は中身を開いていない

**相談窓口**: 潟上市 産業振興部 商工観光振興課 企業支援班（〒010-0201、018-853-5350）

## 大仙市（akita/daisen）

**市独自の制度あり（随時）**: 大仙市事業者生産性向上支援事業（yml: daisen-seisansei）
- デジタル導入型はデジタルツール・ITソリューションの導入経費（対象経費5万〜50万円未満）の1/2、省エネ・省力化型は設備（10万〜300万円未満）の1/2。月額利用料などのランニングコストは対象外 https://www.city.daisen.lg.jp/archive/p20260430115858 （2026-08-03更新）、Q&A
- 受付期間・締切の記載はなく、事前相談制。2026-04-27以後に着手、2027-01-31までに完了
- 根拠として見た一覧: 「助成・支援」https://www.city.daisen.lg.jp/genre/business/grant 、「商工業助成制度」https://www.city.daisen.lg.jp/archive/contents-7727 （若者チャレンジ応援、がんばる商店等支援、若者求職者資格取得補助金、雇用助成金など。AI・IT向けは上記だけ）
- 大仙市中小企業等物価高騰対策支援給付金（2026-09-04掲載）は中身を開いていない

**相談窓口**: 大仙市 経済産業部 商工業・若者チャレンジ振興課（0187-63-1111 内線266・276、shoko@city.daisen.lg.jp）

## 北秋田市（akita/kitaakita）

**市独自の制度あり（省力化ITツールは今年度終了、資格取得は随時）**
- 北秋田市省力化・生産性向上投資応援補助金（yml: kitaakita-shoryoku）: クラウド会計・顧客管理・業務自動化ソフトなど製品分類リストの機器・ITツールに1/2、10万〜100万円。募集 2026-04-01〜05-15 https://www.city.kitaakita.akita.jp/archive/p20250306103430
- 北秋田市資格取得支援助成金（yml: kitaakita-shikaku）: 従業員・内定者の資格取得費用の1/2、1人10万円まで https://www.city.kitaakita.akita.jp/archive/contents-5872
- 根拠として見た一覧: 「商工」https://www.city.kitaakita.akita.jp/genre/sangyou/syoukou_kigyou/syoko 、「商工・企業」https://www.city.kitaakita.akita.jp/genre/sangyou/syoukou_kigyou 、商工政策係 https://www.city.kitaakita.akita.jp/genre/shigoto/p17057/shoukouroudou
- 新商品等開発支援事業、販売促進事業補助金、起業支援事業補助金は中身を開いていない

**相談窓口**: 北秋田市 産業部 産業政策課 産業戦略係（北秋田市花園町19番4号、0186-84-8104）

## にかほ市（akita/nikaho）

**市独自のAI・IT導入・DX向けの補助金は見つからない。在職者訓練の受講料負担がある（今年度は未確認）**
- 在職者向け職業訓練の受講料負担（yml: nikaho-zaishokusha-kunren）: ポリテクセンター秋田・秋田技術専門校の在職者訓練の受講料・教材費を市が全額負担 https://www.city.nikaho.akita.jp/gyosei/shigoto_sangyo/koyo_shugyo/shien_josei/2747.html （更新2025-04-08のため status: unknown）
- 根拠: 商工政策課「補助金・助成金」https://www.city.nikaho.akita.jp/soshikikarasagasu/shokoseisakuka/hojokin_joseikin/index.html （融資あっせん、創業アシスト補助金だけ）、「中小企業等支援」https://www.city.nikaho.akita.jp/gyosei/shigoto_sangyo/sangyoshinko/chushokigyonadoshien/index.html 、「産業振興」https://www.city.nikaho.akita.jp/gyosei/shigoto_sangyo/sangyoshinko/index.html

**相談窓口**: にかほ市 商工観光部 商工政策課（にかほ市象潟町字浜ノ田1番地、0184-43-7600）

## 仙北市（akita/semboku）

**市独自のAI・IT導入・DX・研修向けの補助金は確認できない**
- 根拠: 「産業」https://www.city.semboku.akita.jp/citizens/15.php に「仙北市中小企業活性化支援事業」「仙北市職業訓練事業費補助金」「仙北市勤労者対策補助金」などの項目があるが、リンク先（https://www.city.semboku.akita.jp/news_topics/whatsnew.php?id=2081 、id=2080、id=2316）は2026-10-18時点でいずれも「指定されたデータがありません」で、内容・年度を確認できなかった
- WebSearch（site:city.semboku.akita.jp）でも令和8年度のデジタル・設備の補助金は見つからず、出てきたのは導入促進基本計画と令和7年度の県の施策説明会のチラシだけ
- 中小企業活性化支援事業・職業訓練事業費補助金の今年度の有無は、市に確認が要る（docs/area-todo.md 候補）

**相談窓口**: 仙北市役所（仙北市田沢湖生保内字宮ノ後30、0187-43-1111 代表）。仙北市商工会のサイト https://r.goope.jp/srb-05-22 （市のページのリンク、開いていない）

## 県全体の相談窓口（無料）
- 秋田県 産業労働部 商工業振興課 産業DX推進チーム（デジタル化補助金、地域密着型DX支援、生成AI・AIの研修）: 〒010-8572 秋田市山王三丁目1番1号、018-860-2245、induprom@pref.akita.lg.jp
- 公益財団法人あきた企業活性化センター: 〒010-8572 秋田市山王三丁目1-1（県庁第二庁舎）、018-860-5610 https://www.bic-akita.or.jp/ 。秋田県よろず支援拠点（総合相談課 018-860-5610、akita.yorozu@bic-akita.or.jp）https://akita-yorozu.go.jp/ 、よろず支援拠点内の生産性向上の相談窓口（デジタル活用・省力化、手引き）、専門家派遣
- 秋田県中小企業団体中央会: 〒010-0923 秋田市旭北錦町1-47、018-863-8701（大館支所 0186-43-1644）https://www.chuokai-akita.or.jp/

## 注記
- WebSearch は上限14回のうち5回を使った。県・センター・中央会・各市の公式サイトは curl でたどった。
- 町村（9町3村）の補助金は担当外で調べていない。
- 県の業種別の補助金（介護・医療・農林水産業のデジタル化など）は調べていない。
- 県の食のリーディングカンパニー育成支援事業の今年度の募集ページ、仙北市の制度ページは開けなかった。
- 各市の商工会議所・商工会の連絡先は確認していない。
