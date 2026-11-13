# 熊本県 23町8村の補助金（AI・IT・DX・研修・省力化）2026年度

確認日: 2026-11-04。31町村の公式サイトで、事業者向け・商工業の分類ページと記事一覧（商工担当課の記事一覧、補助金一覧のあるところはそれも）を開き、補助・助成・支援の名前の記事は本文を確かめた。curl で読み、curl が 403・接続リセット・JavaScript の一覧のサイトは WebFetch で読んだ（要約）。町村の公式サイトのドメインは県の「市町村の給与・定員管理等」のリンク集 https://www.pref.kumamoto.jp/soshiki/12/80566.html で確かめた（依頼メモの見込みと違うもの: 玉東町 town.gyokuto.kumamoto.jp、小国町 town.kumamoto-oguni.lg.jp、高森町 town.kumamoto-takamori.lg.jp、御船町 town.mifune.kumamoto.jp、山都町 town.kumamoto-yamato.lg.jp、芦北町 town.ashikita.lg.jp、錦町 town.kumamoto-nishiki.lg.jp、産山村 ubuyama-v.jp、球磨村 kumamura.com、苓北町 reihoku-kumamoto.jp。45市町村〔14市23町8村〕もこのリンク集で確認）。

- **AI・生成AIを名指しで補助する町村独自の制度は、確かめた町村では見つからなかった。**
- **IT・省力化に使える町村独自の制度（`subsidy_b.yml`）**: 大津町「中小企業省力化機器等導入支援補助金」（小売・宿泊・飲食・生活関連サービス業、セルフレジ・配膳ロボット・セルフオーダーシステム・人の業務を代替できる機器・ソフトウェア等、購入1/2・30万円／リース・利用1/2・10万円、毎年2月末まで）、津奈木町「小規模事業者総合支援補助金」（業務効率化の設備1/2・50万円、専門家活用2/3・20万円など）、あさぎり町「商工業振興補助金」（機械・設備1/2・50万円。ITの名指しはない）と「中小企業大学校人吉校研修費助成」（受講料1/2）。
- **独自の制度を確かめられなかった町村（5）**: 嘉島町・甲佐町・小国町・相良村（公式サイトが curl・WebFetch とも 403〔Incapsula の画面〕か文字化け）、芦北町（商工業のページの記事一覧が取れず、WebFetch は 403）。「制度なし」と断定していない。
- **2026-11-11 再確認**: 上の5町村の公式サイトを curl で開き直した。嘉島町・甲佐町・小国町・相良村は独自の AI・IT導入・研修の制度が見つからなかった。芦北町は「中小企業人材育成・副業人材活用支援補助金」（研修・副業人材、1/2・年度10万円）と「中小企業者等持続化事業補助金」（販路開拓等に伴う業務効率化も対象、2/3・50万円）があった（各町村の節）。
- **独自のAI・IT導入・研修の制度がない町村（23）**: 美里町・玉東町・南関町・長洲町・和水町・菊陽町・南小国町・高森町・御船町・益城町・山都町・氷川町・錦町・多良木町・湯前町・苓北町、産山村・西原村・南阿蘇村・水上村・五木村・山江村・球磨村。
- **近隣・県の制度で町村の事業者も使えるもの**: 県の後押し補助金【第2弾】（国のデジタル化・AI導入補助金などの自己負担の上乗せ）、県のリスキリング応援補助金（10時間未満の外部研修の3/4・50万円）、県の副業・兼業人材活用促進事業費補助金、くまもと中小企業デジタル相談窓口（無料、商工会からも申し込める）、熊本県よろず支援拠点（無料）。詳細は subsidy_a_areas.md。市の制度（熊本市・天草市など）は市内の事業者が対象で、町村の事業者は使えない。
- **国・県の補助金への上乗せ（addon）**: 31町村とも該当なし。
- **災害の制度**（令和8年熊本地震・令和7年8月豪雨）は subsidy_a_areas.md の「災害の復旧の制度（AI導入向けとは別）」の節。町村の地震の利子補給・被災証明などはこのファイルの各町村の節に名前だけ書いた。

## 美里町（misato-town-kumamoto）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- しごと・産業 https://www.town.kumamoto-misato.lg.jp/shigoto_sangyo/index.html （下位分類8つ）、産業振興 https://www.town.kumamoto-misato.lg.jp/shigoto_sangyo/sangyoshinko/index.html （企業誘致・企業立地だけ、WebFetch）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

## 玉東町（gyokuto）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 事業者向け支援情報 https://www.town.gyokuto.kumamoto.jp/list00140.html : 町内買物券取扱事業者の募集、農業者向けの金融支援（新型コロナ）だけ
- 農林水産・商工業 https://www.town.gyokuto.kumamoto.jp/list00104.html （事業承継連携支援の協定、8月豪雨の電気柵の補助）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

## 南関町（nankan）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 補助金・助成金 https://www.town.nankan.lg.jp/tyosei/hojokinjoseikin/ と「南関町補助金･助成金等一覧表【令和8年度版】」https://www.town.nankan.lg.jp/tyosei/hojokinjoseikin/joseikin/ の「農林商工関連」https://www.town.nankan.lg.jp/tyosei/hojokinjoseikin/joseikin/hojokin-norinshoko.html （2025-07-09。国・県の農業の補助が中心、町の制度は狩猟免許取得費補助金など）
- 南関町空き店舗等活用開業支援事業助成金 https://www.town.nankan.lg.jp/sangyo/chiikishinko/4400.html （開業向け）
- 人材育成基金 https://www.town.nankan.lg.jp/tyosei/hojokinjoseikin/page1862.html （2021-03-16）: 町に住所か勤務先がある人・グループの先進地視察研修などに費用の70%以内。地域・産業のリーダー育成の基金で、事業者のIT研修の補助ではないため yml に入れていない
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 南関町 まちづくり課（0968-57-8501、人材育成基金）

## 長洲町（nagasu）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- まちづくり課 商工観光係 https://www.town.nagasu.lg.jp/soshiki/machizukuri/shoko/ （92件、WebFetch）: イベント・観光PR・企業紹介冊子・創業セミナー・企業立地協定・新型コロナの支援策の案内
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

## 和水町（nagomi）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- まちづくり課 農林商工業 https://www.town.nagomi.lg.jp/soshiki/machidukuri/nourin/ （32件、WebFetch。日付は一覧にない）: 商品開発事業補助金の募集 /soshiki/machidukuri/nourin/3_4543/、創業・新分野進出に対する補助金 /soshiki/machidukuri/nourin/3_4526/ （いずれも開いていない）、企業立地の優遇措置、先端設備等導入計画、「【参加者募集】AI×Canva×SNSでつくる「わたしたちのマルシェプロジェクト」を開催します！」/soshiki/machidukuri/nourin/17823663901245638/ （参加者募集の講座。補助金ではない、開いていない）、ライブコマース講座、和水町ビジネス交流会、令和7年8月豪雨の県の再建支援補助金の案内
- 町のサイトは JavaScript で一覧を出すため curl で読めず、WebFetch で読んだ
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった（商品開発・創業向けの補助はある）

## 大津町（ozu）

**町独自の制度あり（省力化の機器・ソフトウェア、毎年2月末まで）**
- 「大津町中小企業省力化機器等導入支援補助金のご案内」https://www.town.ozu.kumamoto.jp/page/24589.html （2026-07-14更新）（yml: kumamoto-ozu-shoryokuka）
- 「中小企業人材育成事業補助金のご案内」https://www.town.ozu.kumamoto.jp/page/14193.html （2026-08-19更新）: 中小企業大学校人吉校が町内で開くサテライト・ゼミ「成果と育成を両立する！チームマネジメント力養成研修」（2026-09-08〜09、受講料22,000円）の受講料の半額11,000円を補助。今年度の対象研修は終わったため yml に入れていない（要綱 https://www.town.ozu.kumamoto.jp/uploaded/life/20102_80308_misc.pdf は開いていない）
- 根拠として見た一覧: 商工業 https://www.town.ozu.kumamoto.jp/life/4/19/79/ （先端設備等導入計画、省力化補助、創業サポート補助金、中小企業・小規模企業活性化会議）
- 半導体の大企業の立地に関する事項はこのファイルの範囲外

**相談窓口**: 大津町 産業振興部 商業観光課 商業観光係（096-293-3115）

## 菊陽町（kikuyo）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 商工業 https://www.town.kikuyo.lg.jp/list00130.html : 創業・スタートアップ支援資金利子補給、中小企業近代化融資金利子補給、特定創業支援の証明、先端設備等導入計画、中小企業・小規模企業振興条例、ふるさと納税の協賛事業者募集
- 産業・企業 https://www.town.kikuyo.lg.jp/list00104.html 、補助・助成 https://www.town.kikuyo.lg.jp/list00221.html （子育て・医療が中心）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった。半導体の大企業（JASM など）の立地に関する事項はこのファイルの範囲外

## 南小国町（minamioguni）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 商工業 https://www.town.minamioguni.lg.jp/gyousei/shou-kougyou/ （住宅リフォーム助成事業だけ）、まちづくり情報（町内事業者向け）https://www.town.minamioguni.lg.jp/living/post_41.html
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

## 小国町（oguni）

**確かめられなかった**
- 公式サイト https://www.town.kumamoto-oguni.lg.jp/ は curl・WebFetch とも 403。ヘッダーの付け替えはしていない
- 「制度なし」と断定していない

**2026-11-11 再確認: 町独自の AI・IT導入・研修の補助金は見つからなかった**（curl で読んだ。ヘッダーの付け替えはしていない。Incapsula の 403 がおよそ2回に1回出たので、45〜60秒の間隔を空けて読み直した）
- 町のサイトには事業者向け・商工業の分類がない。サイトマップ https://www.town.kumamoto-oguni.lg.jp/sitemap/ から、産業課のお知らせ https://www.town.kumamoto-oguni.lg.jp/gyoseijyoho/gyosei_kakukanojyoho/gyosei_sangyoka/gyosei_sangyoka_oshirase （2ページとも）、産業課の暮らしの情報 https://www.town.kumamoto-oguni.lg.jp/gyoseijyoho/gyosei_kakukanojyoho/gyosei_sangyoka/gyosei_sangyoka_kurashi 、しごと情報 https://www.town.kumamoto-oguni.lg.jp/kurashinojyoho/kurashi_work 、SDGs未来都市の各種事業・補助金 https://www.town.kumamoto-oguni.lg.jp/sdgsmiraitoshi/sdgs_kakusyujigyo を開いた
- 事業者向けは「町内商工事業者の支援について（経済対策給付金）」（題名だけ。開いていない）、県の感染防止対策認証店の衛生管理設備の補助（題名だけ）、住宅リフォーム助成・町産材の住宅への助成（住宅向け）。AI・IT・DX・研修・省力化の補助は一覧になかった
- 国・県の補助金への町の上乗せも一覧になかった

## 高森町（takamori）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- しごと・産業 https://www.town.kumamoto-takamori.lg.jp/life/4/ 、商工業 https://www.town.kumamoto-takamori.lg.jp/life/4/15/60/ （くまもと都市圏合同就職説明会の参加企業募集〔2025-04-18〕だけ、WebFetch）。求人情報誌「AriSO~だ」の記事
- 依頼メモの見込みのドメイン www.town.takamori.kumamoto.jp は名前解決できない（正しくは town.kumamoto-takamori.lg.jp）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

## 御船町（mifune）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 支援制度について（事業者様向け）https://www.town.mifune.kumamoto.jp/hpkiji/pub/List.aspx?c_id=3&class_set_id=1&class_id=6086 : 新型コロナの利子補給制度、セーフティネット保証4号・5号、先端設備等導入計画
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

## 嘉島町（kashima-town）

**確かめられなかった**
- 公式サイト https://www.town.kumamoto-kashima.lg.jp/ は curl で 403、WebFetch はトップが文字化けでリンク文字が読めなかった
- 「制度なし」と断定していない

**2026-11-11 再確認: 町独自の AI・IT導入・研修の補助金は見つからなかった**（curl で読んだ。ヘッダーの付け替えはしていない。Incapsula の 403 がおよそ2回に1回出たので、45〜60秒の間隔を空けて読み直した）
- しごと・産業 https://www.town.kumamoto-kashima.lg.jp/q/list/169.html → 商業・工業 https://www.town.kumamoto-kashima.lg.jp/q/list/170.html → 商業 https://www.town.kumamoto-kashima.lg.jp/q/list/171.html （2ページとも）、その他 https://www.town.kumamoto-kashima.lg.jp/q/list/173.html と /q/list/192.html を開いた
- 事業者向けの記事は、セーフティネット保証2・4・5号、先端設備等導入計画、企業立地の優遇措置、創業支援等事業、企業版ふるさと納税、くまもと事業者再出発支援補助金（県）・持続化補助金〈災害支援枠〉（国）、事業者支援施策説明会、「かしま事業者応援メール便」、新型コロナの利子補給、中小企業・小規模事業者向けサイバーセキュリティ特別相談窓口（題名だけ）。AI・IT・DX・研修・省力化の町の補助はなかった

## 益城町（mashiki）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- しごと・産業 https://www.town.mashiki.lg.jp/list00504.html （WebFetch）、農林・商工業の「助成金・補助金」https://www.town.mashiki.lg.jp/list00626.html （12件: 令和8年度益城町起業創業事業費補助金 https://www.town.mashiki.lg.jp/kiji0037304/index.html 、創業の紹介、地震の被災農地・農業機械の補助、中小企業融資金利子補給、中小企業退職金共済）、各種支援施策・補助金 https://www.town.mashiki.lg.jp/list00617.html （産業支援サービス業等立地促進補助金〔オフィス系企業の誘致〕）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

## 甲佐町（kosa）

**確かめられなかった**
- 公式サイト https://www.town.kosa.lg.jp/ は WebFetch でトップが文字化け、https://www.town.kosa.lg.jp/q/toppage.html は curl で 403（Incapsula の画面）
- 「制度なし」と断定していない

**2026-11-11 再確認: 町独自の AI・IT導入・研修の補助金は見つからなかった**（curl で読んだ。ヘッダーの付け替えはしていない。Incapsula の 403 がおよそ2回に1回出たので、45〜60秒の間隔を空けて読み直した）
- しごと・産業 https://www.town.kosa.lg.jp/q/list/127.html → 商業・工業 https://www.town.kosa.lg.jp/q/list/129.html （2ページとも）を開いた。融資の一覧 /q/list/228.html は3回とも 403 で開けなかった（題名は商業・工業の一覧にも出る利子補給・セーフティネット保証）
- 町独自の事業者向けの制度は「甲佐町創業支援補助金」https://www.town.kosa.lg.jp/q/aview/129/13566.html （町内で創業・新分野に進出する者、1/2〔その他の経費1/4〕・上限100万円、受付は4/1〜12/1、2026-07-27更新）、「甲佐町物価高騰事業者応援金」https://www.town.kosa.lg.jp/q/aview/129/13500.html （個人6万円・法人12万円の定額、受付 2026-09-17〜11-30）、空き店舗での開業の補助、緊急支援資金・中小企業の利子補給。AI・IT・研修の名指しの補助はない＝記事・診断には創業支援補助金を入れない（益城町の起業創業と同じ扱い）

## 山都町（yamato）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 商工業 https://www.town.kumamoto-yamato.lg.jp/list00334.html : 山都町販路開拓事業補助金（追加募集）https://www.town.kumamoto-yamato.lg.jp/kiji00310873/index.html 、山都町商品開発事業補助金（受付中）https://www.town.kumamoto-yamato.lg.jp/kiji0039790/index.html （いずれも開いていない。販路・商品開発向け）、後継者募集、くまもと事業者再出発支援補助金の案内
- 【事業者向け】各種支援制度 https://www.town.kumamoto-yamato.lg.jp/list01088.html （記事の一覧は取れなかった）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

## 氷川町（hikawa）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 商工業 https://www.town.hikawa.kumamoto.jp/list00195.html （17件、WebFetch）: 短期間・短時間雇用応援助成事業 https://www.town.hikawa.kumamoto.jp/kiji0036875/index.html （開いていない）、令和8年熊本地震に伴う中小企業資金繰り支援（利子補給）、企業誘致の優遇制度、県のリスキリング応援補助金の案内 https://www.town.hikawa.kumamoto.jp/kiji0036709/index.html 、令和7年8月豪雨の県の再建支援補助金の案内、「創業予定者・事業者の皆様への補助制度があります。」https://www.town.hikawa.kumamoto.jp/kiji0033088/index.html （2019-06-11。空き店舗等での開設、事業所の修繕・改築、事業に必要な機械・器具の購入の補助。概要 PDF を開いておらず、率・上限・今年度も続いているかは確かめていない）
- 【氷川町商工会】令和8年熊本地震に係る中小企業・小規模事業者向け特別相談窓口 https://www.town.hikawa.kumamoto.jp/kiji0036804/index.html （開いていない）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった（機械・器具の購入を含む2019年の補助制度は今年度の状況を確かめていない）

## 芦北町（ashikita）

**確かめられなかった（一部だけ）**
- 公式サイト https://www.town.ashikita.lg.jp/ のトップ（WebFetch）に「水俣・芦北地域振興財団助成事業」（令和9年度募集、2026-10-01）https://www.town.ashikita.lg.jp/toppage/bosyu/2120287 と集合住宅建設支援事業補助金の募集がある（開いていない）
- 商工業 https://www.town.ashikita.lg.jp/sangyo_shigoto/sangyo/shokogyo は curl で記事の一覧が取れず、WebFetch で /sangyo_shigoto/sangyo が 403
- 依頼メモの見込みのドメイン www.ashikita-t.jp は接続できない（正しくは town.ashikita.lg.jp）
- 「制度なし」と断定していない

**2026-11-11 再確認: 町独自の研修・副業人材の補助と、販路開拓に伴う業務効率化も対象の補助がある（AI・ITの名指しはない）**（curl で読んだ。ヘッダーの付け替えはしていない。Incapsula の 403 がおよそ2回に1回出たので、45〜60秒の間隔を空けて読み直した）
- 商工業 https://www.town.ashikita.lg.jp/sangyo_shigoto/sangyo/shokogyo （2ページとも）と商工観光課の記事一覧 https://www.town.ashikita.lg.jp/chosei/soshiki/shokoka （3ページとも）を開いた
- **芦北町中小企業人材育成・副業人材活用支援補助金** https://www.town.ashikita.lg.jp/sangyo_shigoto/sangyo/shokogyo/2083698 （更新日2025-07-25）: 町内に登記のある事業所を有する法人か、町内に事業所と住所がある商工業の個人事業主。研修は中小企業大学校（人吉校に限る）・中小機構が県内で実施する研修・町長が特に認める研修の受講料、副業人材は募集のメディア掲載費・委託料・旅費など。1/2、研修は上限5万円・副業人材は上限10万円、年度内の総額10万円。受付期間の記載なし（rolling）。問い合わせは商工観光課（代表 0966-82-2511）。DX・AIの名指しなし
- **芦北町中小企業者等持続化事業補助金** https://www.town.ashikita.lg.jp/sangyo_shigoto/sangyo/shokogyo/2083742 （更新日2026-04-28）: 町内に住所か本店がある中小企業者等で、芦北町商工会の支援を受けて事業計画書等を作り、販路開拓・売上拡大につながる事業。生産性向上等の業務効率化の事業は「前号の事業に伴うものであること」＝販路開拓等に伴うものに限る。施設整備費1/2・その他2/3、上限50万円（創業150万円、空き地・空き店舗活用200万円）。一度受給すると3年間は受給不可。受付期間の記載なし（rolling）。問い合わせは商工観光課 商工振興係 0966-83-9677。ソフトウェア・ITツールが対象かは書かれていない
- ほかは創業等資金・設備投資資金・災害時等特別資金の利子補給、先端設備等導入計画、セーフティネット保証、【受講者募集】生成AIを活用した業務効率化実践講座（町の講座。補助金ではない＝D3）
- 2026-11-04 の「水俣・芦北地域振興財団助成事業」は今回も開いていない
- 両制度を `data/subsidies/kumamoto.yml` に追加（kumamoto-ashikita-jinzai-fukugyo・kumamoto-ashikita-jizokuka）

## 津奈木町（tsunagi）

**町独自の制度あり（業務効率化の設備・専門家活用）**
- 「津奈木町小規模事業者総合支援補助金の募集について」https://www.town.tsunagi.lg.jp/page4097.html （最終更新2026-06-01）（yml: kumamoto-tsunagi-shokibo-sogo）

**相談窓口**: 津奈木町 商工観光班（0966-83-8066）

## 錦町（nishiki）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 事業者・起業者支援 https://www.town.kumamoto-nishiki.lg.jp/list00191.html 、事業者向け支援 https://www.town.kumamoto-nishiki.lg.jp/list00136.html 、商工業 https://www.town.kumamoto-nishiki.lg.jp/list00192.html : 錦町企業立地促進補助金、錦町商工業後継者支援給付金、起業者支援、錦町情報技術推進協議会、県の後押し補助金・くまもと型応援補助金の案内
- 令和8年度錦町資材価格高騰対策支援補助金 https://www.town.kumamoto-nishiki.lg.jp/kiji0031208/index.html （2026-08-20）: 農業者向け（肥料費・飼料費など）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

## 多良木町（taragi）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 商工業 https://www.town.taragi.lg.jp/gyousei/shigoto_sangyo/shokogyoshinko/shokogyo/index.html : 先端設備等導入計画だけ。しごと・産業 https://www.town.taragi.lg.jp/gyousei/shigoto_sangyo/index.html
- トップは WebFetch で 503、curl の default.html から分類を取った
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

## 湯前町（yunomae）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 補助金ナビ「事業者向けの補助金など」https://www.town.yunomae.lg.jp/dynamic/procnavi/pub/List.aspx?c_id=36&class_id=2 : 「ただいま、準備中です。」（WebFetch）
- 商工業 https://www.town.yunomae.lg.jp/dynamic/hpkiji/pub/List.aspx?c_id=3&class_set_id=1&class_id=394 （6件: サテライトオフィス「ユノラボ」、事業承継セミナー、立地協定、新型コロナの資金繰り支援）
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

## あさぎり町（asagiri）

**町独自の制度あり（機械・設備の導入と研修の補助、随時）**
- 「あさぎり町商工業振興補助金」https://www.town.asagiri.lg.jp/kiji0033867/index.html （最終更新2024-06-24、令和8年度からの変更を記載）（yml: kumamoto-asagiri-shokogyo-shinko）
- 「中小企業大学校人吉校研修費助成について」https://www.town.asagiri.lg.jp/kiji0033883/index.html （最終更新2021-10-04）（yml: kumamoto-asagiri-hitoyoshi-kenshu）
- 根拠として見た一覧: 商工業 https://www.town.asagiri.lg.jp/list00237.html （9件、WebFetch。ほかに店舗新増築及び改装助成事業、制度資金利子補給、先端設備等導入計画、くまもと型応援補助金の案内）、各種支援施策（補助金等）https://www.town.asagiri.lg.jp/list00233.html （記事の一覧は動的で取れなかった）

## 苓北町（reihoku）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 事業者・起業者支援 https://reihoku-kumamoto.jp/list00196.html 、商工業 https://reihoku-kumamoto.jp/list00197.html : 苓北町小規模事業者等支援補助金 https://reihoku-kumamoto.jp/kiji003957/index.html （2025-03-27。3か月以内に新規に小規模事業者となる者に最大50万円、後継者に最大20万円。創業・承継向け）、中小企業振興資金利子補給、富岡城二の丸東角櫓のワーキングスペース
- 結論: 町独自の AI・IT 導入・研修の補助は見つからなかった

**相談窓口**: 苓北町 商工観光課（0969-35-3332）

## 産山村（ubuyama）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- しごと・産業 http://www.ubuyama-v.jp/shigoto_sangyo/index.html （新規就農支援）、各種補助金 http://www.ubuyama-v.jp/kurashinojoho/kakushuhozyokin/index.html （コミュニティ・住宅・暮らし・就学・福祉の補助）
- 結論: 村独自の AI・IT 導入・研修の補助は見つからなかった

## 西原村（nishihara）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 事業者・起業者支援 https://www.vill.nishihara.kumamoto.jp/list00197.html （2件: セーフティネット保証5号、特定創業支援等事業の証明書。WebFetch）。分類は産業・商工・農林 https://www.vill.nishihara.kumamoto.jp/list00121.html の下に企業立地・支援 list00196、商工業 list00198（開いていない）
- 結論: 村独自の AI・IT 導入・研修の補助は見つからなかった

## 南阿蘇村（minamiaso）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 事業者向け支援情報 https://www.vill.minamiaso.lg.jp/list00148.html （地域振興券、おこめギフト券、小売店等の買物支援対策補助事業、有機JAS認証推進事業補助金）、商工業 https://www.vill.minamiaso.lg.jp/list00208.html （持続化補助金〈災害支援枠〉の証明書の発行、セーフティネット保証4号、創業者の応援・創業支援事業計画）
- 結論: 村独自の AI・IT 導入・研修の補助は見つからなかった

## 水上村（mizukami）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 農林商工業 https://www.vill.mizukami.lg.jp/list00170.html : 令和9年度農林商工業関係補助事業の要望調査 https://www.vill.mizukami.lg.jp/kiji0031372/index.html （開いていない）、森林・農地の手続き
- 結論: 村独自の AI・IT 導入・研修の補助は見つからなかった

## 相良村（sagara）

**確かめられなかった**
- 公式サイト https://www.vill.sagara.lg.jp/ は curl で 403、WebFetch はトップが文字化け
- 「制度なし」と断定していない

**2026-11-11 再確認: 村独自の AI・IT導入・研修の補助金は見つからなかった**（curl で読んだ。ヘッダーの付け替えはしていない。Incapsula の 403 がおよそ2回に1回出たので、45〜60秒の間隔を空けて読み直した）
- しごと・産業 https://www.vill.sagara.lg.jp/q/list/100.html 、農林商工業 https://www.vill.sagara.lg.jp/q/list/101.html （3ページとも）、補助金・減免 https://www.vill.sagara.lg.jp/q/list/106.html を開いた
- 事業者向けの村の補助は「相良村サテライトオフィス等誘致事業補助金」https://www.vill.sagara.lg.jp/q/aview/106/2946.html （2026-06-04、村と立地協定を結んでサテライトオフィス等を新設する事業者。開設1/2・上限100万円、運営〔賃借料・通信回線料〕1/2・上限100万円、雇用1人10万〜15万円、年間100万円まで。企画商工課 商工観光係 0966-35-1036）だけ。村内の既存の事業者の AI・IT導入・研修向けではない＝記事・診断に入れない
- ほかは企業立地・企業誘致、なりわい再建支援補助金の相談窓口（令和2年7月豪雨）、県の SDGs 普及啓発事業補助金・ブライト企業の募集など

## 五木村（itsuki）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 商工業・企業誘致 https://www.vill.itsuki.lg.jp/list00574.html （記事なし）、補助金 https://www.vill.itsuki.lg.jp/list00720.html （重点支援地方交付金の活用状況の公表だけ）
- 結論: 村独自の AI・IT 導入・研修の補助は見つからなかった

## 山江村（yamae）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 事業者・起業者支援 https://www.vill.yamae.lg.jp/list00195.html : 小さな産業づくり事業（村民3名以上の団体の特産物開発など、2019-09-25）、特産品等出展事業助成金、就農・酪農・畜産・狩猟・林業の助成、新型コロナの利子補給・雇用調整助成金交付事業
- 結論: 村独自の AI・IT 導入・研修の補助は見つからなかった

## 球磨村（kuma）

**IT向けの制度**
- なし（2026年度）。

**見たページ**
- 商工 https://www.kumamura.com/list00128.html 、事業者・起業者支援 https://www.kumamura.com/list00204.html
- 球磨村商工業者物価高騰対策支援補助金 https://www.kumamura.com/kiji0031842/index.html （2026-05-25）: 球磨村商工会員の商工業者、2026年中の仕入れ・備品購入費・消耗品・修繕料・電気料などの1/2・上限10万円、受付2026-05-11〜2027-01-29（球磨村商工会）。物価高騰の負担軽減で、IT・AI向けではないため yml に入れていない（備品購入費は対象）
- 結論: 村独自の AI・IT 導入・研修の補助は見つからなかった

---

## 取れなかった項目・注意点

- WebSearch は使っていない（町村の分。県・市と合わせた回数は subsidy_a_areas.md）。町村のページは curl で開き（間隔を空けた）、403・接続リセット・JavaScript の一覧は WebFetch で読んだ。WebFetch は要約を返すので、補助率・上限・期限は curl で取った本文で確かめたもの（大津町・津奈木町・あさぎり町・球磨村）を書いた。ヘッダーの付け替えはしていない。
- **嘉島町・甲佐町・小国町・相良村**: Incapsula の 403 か WebFetch の文字化けで、どのページも読めなかった。**芦北町**は商工業の一覧が取れなかった。Mac で開いて確かめ直す。
- **大津町**: 省力化補助の要綱を開いておらず、ソフトウェアの月額利用料が「リース・利用」の区分に入るかを要綱で確かめていない。予算の残は書かれていない。
- **津奈木町**: 受付期間・予算・事業ごとの回数の制限がページにない（要綱 PDF は開いていない）。
- **あさぎり町**: 商工業振興補助金の「機械・設備」にソフトウェアが入るか、研修費助成の上限・令和8年度も続いているかは要綱で確かめていない。担当課の名前を確かめていない。
- **氷川町**: 2019年の「創業支援・事業所等整備促進事業」（機械・器具の購入を含む）の率・上限・今年度の状況を確かめていない。
- **和水町・山都町**: 商品開発・販路開拓・創業向けの補助のページを開いていない（IT向けではないと題名で判断）。
- 各町村の商工会の独自の補助・専門家派遣は確かめていない（名前は gov 担当の確認を正とする）。
- 自治体コード・管轄は照合していない（stats・gov 担当を正とする）。
