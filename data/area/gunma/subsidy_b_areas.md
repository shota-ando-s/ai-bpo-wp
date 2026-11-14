# 群馬県 15町8村の補助金（AI・IT・DX・研修・業務改善・販路開拓）2026年度

確認日: 2026-11-06。町村の公式サイトの事業者向け・商工業・補助金のページを開いて確認した（curl で開けたサイトは curl、メニューが読めないサイトは WebFetch も使った）。YAML は `subsidy_b.yml`（2制度）。対象は吉岡町（yoshioka）・神流町（kanna）・下仁田町（shimonita）・甘楽町（kanra）・中之条町（nakanojo）・長野原町（naganohara）・草津町（kusatsu）・東吾妻町（higashiagatsuma）・みなかみ町（minakami）・玉村町（tamamura）・板倉町（itakura）・明和町（meiwa）・千代田町（chiyoda）・大泉町（oizumi）・邑楽町（ora）・榛東村（shinto）・上野村（ueno-village）・南牧村（nanmoku）・嬬恋村（tsumagoi）・高山村（takayama-village-gunma）・片品村（katashina）・川場村（kawaba）・昭和村（showa-village-gunma）。県の制度・県域の機関・国の制度・12市は subsidy_a。

- 23町村とも、**生成AI・AI導入・IT導入・DX・研修を名指しで補助する町村独自の制度はない**。
- **IT・業務効率化・ホームページに使える町村独自の制度**（yml 2件）:
  - **東吾妻町**「令和8年度東吾妻町中小事業者持続化及びSDGs推進補助金」（キャッシュレス・インボイス対応レジ、設計用CADソフト、新たなネット販売システムの構築・WEBサイト作成の委託など。町内業者50%・町外業者30%、上限20万〜30万円。事業期間 2026-04-01〜12-31、**申請 2027-01-29 必着まで受付中**）。国の小規模事業者持続化補助金等と重複可（国の交付額を差し引いた後の経費が対象）
  - **嬬恋村**「売上アップ事業補助金」（小規模企業者の販売促進・業務効率化、機械装置・開発費・委託外注費・専門家謝金など、1/2・50万円、受付期間の記載なし＝随時として記録。嬬恋村商工会経由、他の補助金と併用不可）
- **国の補助金への上乗せ（addon）**: 23町村とも見つからない（東吾妻町は「国の補助額を差し引いた残りが対象」の形で、上乗せ先に連動する補助率ではない）。
- **ぐんま技術革新チャレンジ補助金**（県と市町村の共同、1/2〔小規模4/5〕・80万円、令和8年度は 2026-05-15 で終了・二次募集なし）の実施町村は 榛東村・下仁田町・甘楽町・東吾妻町・みなかみ町・玉村町・板倉町・明和町・千代田町・大泉町・邑楽町（県のページ https://www.pref.gunma.jp/site/hojokin/10642.html の「6 実施市町村一覧」）。町村独自の制度ではないので、各町村の節では「県と共同」と書く。
- 独自の IT・研修向けの制度を確認できなかった町村: **東吾妻町・嬬恋村以外の21町村**（うち上野村は公式サイトが開けず未確認）。
- 予算残額を公開している町村はない。
- **リンクの条件**: 長野原町は「当サイトへのリンク設定を希望される場合は、本基準の内容に同意のうえ、所定の手続きに従ってお申し込みください」（申込制・審査あり）https://www.town.naganohara.gunma.jp/development/?content=214 。明和町は「当町HPへのリンクは自由とします。特段申請は不要です」https://www.town.meiwa.gunma.jp/4954.html 。ほかの町村のリンクの条件は今回確かめていない。

### 二次情報のみ（secondary、記事では使わない）
- 補助金エージェント https://hojokin-agent.jp/subsidy/gunma/nanmoku （検索結果に出ただけ、開いていない）

## 吉岡町（yoshioka）
確認したページ: 産業・ビジネス https://www.town.yoshioka.lg.jp/business/ 、商工業 https://www.town.yoshioka.lg.jp/business/shoukougyou/
- 商工業のページは企業版ふるさと納税・プレミアム商品券・事業承継・引継ぎ支援センター・計量だけ。**独自の事業者向け補助金は見つからない**。ぐんま技術革新チャレンジ補助金の実施町村ではない
- 公式サイトのドメインは www.town.yoshioka.lg.jp（town.yoshioka.gunma.jp から転送）

## 神流町（kanna）
確認したページ: しごと・産業 https://www.town.kanna.gunma.jp/shigoto_sanngyou/index.html （求職・就業、土木公共物使用、開発・建築、農業・林業、入札・契約だけ）、くらし・手続き https://www.town.kanna.gunma.jp/kurashi_tetsuduki/index.html
- **商工業・事業者向け補助金のページが見当たらない**。チャレンジ補助金の実施町村ではない

## 下仁田町（shimonita）
確認したページ: 産業・事業者 https://www.town.shimonita.lg.jp/m05/index.html 、商工業・観光業 https://www.town.shimonita.lg.jp/m05/m02/index.html 、創業支援 https://www.town.shimonita.lg.jp/m05/m06/index.html
- あるのは 令和8年度下仁田町ねぎとこんにゃく食材料費支援事業、下仁田町推奨品の認定、創業支援事業補助金制度、チャレンジショップ。**独自の IT 導入・研修の補助は見つからない**。チャレンジ補助金は県と共同（商工観光課商工観光係 0274-64-8805）

## 甘楽町（kanra）
確認したページ: 各課の案内 https://www.town.kanra.lg.jp/annai/index.html から 産業課 商工観光係 https://www.town.kanra.lg.jp/sansin/kankou/index.html 、そのお知らせの一覧（WebFetch で https://www.town.kanra.lg.jp/sansin/kankou/news/index.html を読んだ）
- 甘楽町店舗継続・拡大サポート事業補助金 https://www.town.kanra.lg.jp/sansin/kankou/news/20230329125359.html （最終更新2025-08-28）: 町内で2年以上営業する小売業・宿泊業・飲食サービス業・生活関連サービス業、器具購入費・改装費・看板・ポスター・チラシ、1/4・上限30万円。IT・ソフトウェアの記載はないので yml に入れていない
- ほかは 創業支援塾（2026-10-19）、先端設備等導入計画、若年者ふるさと就職支援事業補助金（雇用系）。チャレンジ補助金は県と共同（産業課商工観光係 0274-64-8320）
- 公式サイトのドメインは www.town.kanra.lg.jp（town.kanra.gunma.jp は接続できない）

## 中之条町（nakanojo）
確認したページ: しごとの情報＞起業・経営・事業者支援 https://www.town.nakanojo.gunma.jp/life/2/19/86/
- あるのは サテライトオフィス開設支援補助金（誘致）、チャレンジショップ出店支援事業、起業支援事業、先端設備等導入制度、地域商品券（令和7年度）。**独自の IT 導入・研修の補助は見つからない**。チャレンジ補助金の実施町村ではない

## 長野原町（naganohara）
確認したページ: 仕事・就労支援 https://www.town.naganohara.gunma.jp/business/?category=65 、補助・助成・給付金等 https://www.town.naganohara.gunma.jp/life/?category=18 、商工業に係る各種制度 https://www.town.naganohara.gunma.jp/business/?content=191 （更新日2026-03-07、小口資金融資と利子補給だけ）
- あるのは 起業者への補助金（life/?content=194）、まちづくり活性化補助金（団体向け）、地方就職支援金。**独自の IT 導入・研修の補助は見つからない**。チャレンジ補助金の実施町村ではない
- **リンクは申込制**（上の要約）

## 草津町（kusatsu）
確認したページ: くらしの情報・まちづくり環境・観光とスポーツ・健康福祉・行政情報・申請書ダウンロードの各一覧（https://www.town.kusatsu.gunma.jp/li/010/index.html 、/li/030/ 、/li/040/ 、/li/060/ 、/li/070/ 、/li/090/）。事業者向けの分類がなく、各一覧の題名に「商工・事業者・補助・助成・奨励・産業・企業・店舗・創業・起業」を含むものを全部拾った
- 拾えたのは 不妊治療・犬猫の避妊・木造住宅耐震・空家除却・街なみ環境整備事業補助金（受付終了）・骨髄移植ドナー助成だけ。**事業者向けの補助金は見つからない**。チャレンジ補助金の実施町村ではない

## 東吾妻町（higashiagatsuma）
確認したページ: 各課案内＞まちづくり推進課＞商工業事業者（企業者）支援 https://www.town.higashiagatsuma.gunma.jp/www/genre/1430102969535/index.html
- **中小事業者持続化及びSDGs推進補助金**（yml: gunma-higashiagatsuma-jizokuka-sdgs）https://www.town.higashiagatsuma.gunma.jp/www/contents/1774511247401/index.html : 受付中・2027-01-29必着まで
- ほかは 空き店舗利活用支援事業、企業立地促進条例、先端設備等導入計画、商工業・労働政策。チャレンジ補助金は県と共同（まちづくり推進課地域振興係 0279-68-2111）
- 雇用・賃上げ系（AI導入の補助と分ける）: 東吾妻町賃上げ促進支援金 https://www.town.higashiagatsuma.gunma.jp/www/contents/1767853240171/index.html （未読）

## みなかみ町（minakami）
確認したページ: 産業 しごと＞補助金・支援制度 https://www.town.minakami.gunma.jp/industry/hojyokin_shienseido/index.html 、観光商工課 https://www.town.minakami.gunma.jp/politics/03soshiki/kankoushoukouka_index.html
- あるのは 観光活性化補助金（観光団体・観光的団体向け、2/3・50万円）https://www.town.minakami.gunma.jp/industry/hojyokin_shienseido/2024-0125-1027-71.html 、中小企業融資制度利子補給金、起業支援事業補助金、地場産品普及開発事業補助制度、ローカル10,000プロジェクト。**個々の事業者の IT 導入・研修の補助は見つからない**。チャレンジ補助金は県と共同（観光商工課商工振興係 0278-25-5018）
- 町の「補助金等ポータル」（LoGoフォーム https://logoform.jp/procedure/tzTd/subsidy-list ）は 2026-11-06 に curl・WebFetch とも 403 で開けなかった

## 玉村町（tamamura）
確認したページ: 事業者向け情報 https://www.town.tamamura.lg.jp/navi/jigyosha/ 、産業・労働 https://www.town.tamamura.lg.jp/category/bunya/sangyo_rodo/ 、経済産業課の新着一覧 https://www.town.tamamura.lg.jp/soshiki/keizai/more.html
- あるのは 企業立地促進奨励金、制度資金、セーフティネット保証、「玉村町ぐんま技術革新チャレンジ補助金」募集のお知らせ（/docs/2023031500033/）。**独自の IT 導入・研修の補助は見つからない**

## 板倉町（itakura）
確認したページ: 観光・産業＞商工業 https://www.town.itakura.gunma.jp/d000040/d000080/index.html
- あるのは 創業支援事業計画、住宅リフォーム支援、小規模事業者持続化補助金（一般型）の紹介（全国商工会連合会へのリンクだけ、町の上乗せはない。更新日2025-07-18）、先端設備等導入計画、令和8年度板倉町ぐんま技術革新チャレンジ補助金（県と共同）。**独自の IT 導入・研修の補助は見つからない**

## 明和町（meiwa）
確認したページ: 事業者の方＞商工 https://www.town.meiwa.gunma.jp/life/taishosha/6/4893.html
- あるのは 創業支援事業計画、先端設備等導入計画、新型コロナの支援措置（古い）、『梨の雫めいわ』。**独自の IT 導入・研修の補助は見つからない**。チャレンジ補助金は県と共同だが、町のページはこの範囲では見つからなかった
- リンクは自由（上の要約）

## 千代田町（chiyoda）
確認したページ: 事業者向け https://www.town.chiyoda.gunma.jp/jigyou/index.html 、商工 https://www.town.chiyoda.gunma.jp/keizai/syoko/index.html
- 千代田町店舗リニューアル補助金 https://www.town.chiyoda.gunma.jp/keizai/syoko/post-466.html : 町内の店舗・事業所の改装工事（町内施工業者、税抜10万円以上）と「当該店舗等において専ら事業の用に供する設備類の導入」、1/2・上限20万円、補助対象期間 2026-04-01〜2027-03-31（予算上限で終了）。IT の明記がないので yml に入れていない
- ほかは ISO認証取得支援事業奨励金、創業支援事業補助金、融資、千代田町ぐんま技術革新チャレンジ補助金（県と共同、syoko016.html）

## 大泉町（oizumi）
確認したページ: 事業者＞融資・助成 https://www.town.oizumi.gunma.jp/li/jigyo/020/index.html 、「各種補助制度をご案内します」https://www.town.oizumi.gunma.jp/s019/040/20210506164537.html （更新日2026-04-08、令和8年度各種補助制度のパンフレット）
- 設備導入奨励金 https://www.town.oizumi.gunma.jp/s020/jigyo/020/090/20200825153401.html （更新日2026-04-01）: 町内の製造業、生産能力拡大・合理化・省力化・研究開発の設備（償却資産）の固定資産税額の9/10・上限500万円。令和8年度は2025年1〜12月に取得した設備が対象。設備の補助で IT 導入ではないので yml に入れていない
- ほかは 産業立地振興奨励金、空き店舗等活用・創業促進事業（予算残りわずか）、新技術・新製品の研究開発に係る補助金（チャレンジ補助金と思われる、未読）、店舗リニューアル補助、ふるさと納税返礼品開発等支援補助金、融資
- 雇用・賃上げ系: 大泉町賃上げ促進支援金、働きやすい職場づくり奨励金（予算残りわずか）、雇用奨励金（新規認定終了）、女性キャリアアップ奨励金（題名だけ）

## 邑楽町（ora）
確認したページ: 産業・企業 https://www.town.ora.gunma.jp/li/060/150/index.html
- あるのは 創業支援事業補助金、工場立地法、セーフティネット保証、邑楽町・商工会連携原油価格物価高騰対策支援（2023年）。**独自の IT 導入・研修の補助は見つからない**。チャレンジ補助金は県と共同
- 「令和8年度SDS電子化補助金事業の実施」https://www.town.ora.gunma.jp/s030/SDS-joseikin.html （更新日2026-08-24）は町の制度ではなく、厚生労働省の標準フォーマットの SDS（安全データシート）を出入力できるシステムの導入への補助（1/2・上限100万円、問い合わせは全国労働衛生団体連合会）の紹介。国の制度なので yml に入れていない（national.yml の担当に情報として回す）

## 榛東村（shinto）
確認したページ: 産業・仕事＞商工業 https://www.vill.shinto.gunma.jp/business/000197/index.html と その下の お知らせ・商業関連支援制度・工業関連支援制度・地域企業支援
- あるのは 地域未来投資促進法、セーフティネット保証、物価高騰対策（お買い物券）。**独自の IT 導入・研修の補助は見つからない**。チャレンジ補助金は県と共同（産業振興課商工観光係 0279-54-2211）だが、村のページはこの範囲では見つからなかった

## 上野村（ueno-village）
- 公式サイト https://www.vill.ueno.gunma.jp/ は 2026-11-06 に 503（curl は接続リセット、WebFetch は 503）。Internet Archive（2026-06-17 の保存）は curl で 403、WebFetch は不可。**確かめられていない**。チャレンジ補助金の実施町村ではない

## 南牧村（nanmoku）
確認したページ: 公式サイトのドメインは **https://nanmoku.ne.jp/** （題名「群馬県なんもく村」、所在地「甘楽郡南牧村大字大日向1098」。www.vill.nanmoku.gunma.jp は名前解決できない）。サイトマップ https://nanmoku.ne.jp/sitemap 、各種補助金 https://nanmoku.ne.jp/lifehealth/life/various_subsidy/ （結婚・出産祝金、行政区集会施設、高校通学、転入・定住奨励金だけ）、産業情報 https://nanmoku.ne.jp/kanko/sangyo/ （生産組合・農業人材育成）
- **事業者向けの補助金は見つからない**。チャレンジ補助金の実施町村ではない
- 注意: 検索で出る「南牧村商工会」「南牧村（地方公共団体コード 203050）」の経営発達支援計画（中小企業庁の PDF）は**長野県南佐久郡南牧村**で、群馬県甘楽郡南牧村ではない

## 嬬恋村（tsumagoi）
確認したページ: 観光商工課 https://www.vill.tsumagoi.gunma.jp/www/section/1647248287833/index.html
- **売上アップ事業補助金**（yml: gunma-tsumagoi-uriage-up）https://www.vill.tsumagoi.gunma.jp/www/contents/1000000000246/index.html
- ほかは 住宅改修等助成金、融資制度、中小企業退職金共済制度加入促進補助金。チャレンジ補助金の実施町村ではない

## 高山村（takayama-village-gunma）
群馬県吾妻郡高山村。確認したページ: 産業 https://www.vill.takayama.gunma.jp/sangyo.html （文字コード cp932）、地域振興課 https://www.vill.takayama.gunma.jp/soshiki/02chiiki.html
- 産業のページは農業（新規就農・有機農業・6次産業推進事業補助金・農作物被害対策）、住宅リフォーム補助金、生産性向上特別措置法、地域づくり支援事業。**商工業の事業者向け補助金は見つからない**。チャレンジ補助金の実施町村ではない

## 片品村（katashina）
確認したページ: 商工観光係 https://www.vill.katashina.gunma.jp/gaiyou/kakuka/kanko/index.html 、産業と労働 https://www.vill.katashina.gunma.jp/gyousei/sangyou/index.html
- あるのは 片品村合宿・研修等支援事業補助金（2次募集、https://www.vill.katashina.gunma.jp/gaiyou/kakuka/kanko/gassyuku.html 、合宿の誘致、未読）、起業支援事業補助金、地域イベント等開催支援事業補助金、移住支援金・地方就職支援金など。**事業者の IT 導入・研修の補助は見つからない**。チャレンジ補助金の実施町村ではない

## 川場村（kawaba）
確認したページ: 事業・産業情報＞産業 https://www.vill.kawaba.gunma.jp/kurashi/sanno/sangyou/
- あるのは 山村振興計画、セーフティネット保証、先端設備等導入計画、土砂埋立て規制条例。**事業者向けの補助金は見つからない**。チャレンジ補助金の実施町村ではない

## 昭和村（showa-village-gunma）
群馬県利根郡昭和村。確認したページ: 観光・産業＞産業 https://www.vill.showa.gunma.jp/kurashi/kankou/sangyo/index.html
- あるのは 工場用地のご案内、特定間伐等促進計画、農業振興地域整備計画、セーフティーネット保証、導入促進基本計画。**事業者向けの補助金は見つからない**。チャレンジ補助金の実施町村ではない

## 事例の手がかり（cases 担当へ）
- 群馬県DX推進・AI活用リスキリング事業の令和8年度モデル企業に、**株式会社尾瀬岩鞍リゾート（片品村、30人以上100人未満、複合サービス事業）**と**東毛福祉事業協同組合（大泉町）**（https://www.pref.gunma.jp/site/reskilling/753811.html 。成果はまだない。取組報告会は2027年1〜3月）
- 町村の補助金のページに採択企業の成果・事例の紹介はなかった

## 取れなかった項目・注意点
- 上野村は公式サイトが開けず未確認
- みなかみ町の LoGoフォームの補助金ポータルは 403 で開けなかった（町のページの一覧で判断）
- 草津町・高山村はサイトに事業者向けの分類がなく、一覧の題名からの判断
- 嬬恋村 売上アップ事業補助金は受付期間・今年度の予算の記載がなく rolling として記録した（村に確認が要る）
- 東吾妻町の別表の広報費の欄に「令和６年度内なら○」と古い年度が残っている（別表の PDF 作成は2026-06-12）
- 商工会の IT・AI セミナー（町村）は今回探していない
- 町村の災害復旧の制度・雇用増が要件の制度は、題名を見た範囲（東吾妻町 賃上げ促進支援金、大泉町 賃上げ促進支援金ほか）だけ記録した
- WebSearch はこのファイルの担当分で1回（南牧村のドメイン。subsidy 担当の合計は3回、上限15回）
