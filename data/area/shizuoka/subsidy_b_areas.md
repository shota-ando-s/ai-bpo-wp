# 静岡県 12町の補助金（AI・IT・DX・研修・創業・設備・販路開拓）2026年度

確認日: 2026-11-11。町の公式サイトの事業者向け・商工業・補助金のページを開いて確認した（12町とも curl で開けた。巡回の記録は scratchpad/choson/crawl/<町>/）。YAML は `subsidy_b.yml`（12制度）。対象は東伊豆町（higashiizu）・河津町（kawazu）・南伊豆町（minamiizu）・松崎町（matsuzaki）・西伊豆町（nishiizu）・函南町（kannami）・清水町（shimizu-town-shizuoka）・長泉町（nagaizumi）・小山町（oyama-town）・吉田町（yoshida）・川根本町（kawanehon）・森町（mori-town-shizuoka）。県の制度・県域の機関・国の制度・23市は subsidy_a。

- 12町とも、**生成AI・AI導入・IT導入・DX を名指しで補助する町独自の制度はない**。
- **国の補助金への上乗せ（addon）**: 12町とも見つからない（国のデジタル化・AI導入補助金〔旧IT導入補助金〕への上乗せの制度はない）。清水町 経営革新計画支援補助金は「当該補助金以外の補助金を差し引いた」額の1/2で、上乗せ先に連動する補助率ではないので addon は書いていない。
- **IT・ホームページ・研修に使える町独自の制度**（yml）:
  - **清水町**「中小企業支援補助金」（販売力促進支援: ホームページ作成費などの広報費 1/2・年5万円、県外販路拡大支援: 展示会の出展料 1/2・年10万円。随時、2026年4月1日更新）と「経営革新計画支援補助金」（経営革新計画の承認が前提。研修費・外注費・技術コンサルタント料・ホームページ作成費など 1/2・50万円、随時）
  - **河津町**「小規模事業者強化事業費補助金」（ホームページ制作・リニューアル、ネット注文・メール配信システム整備など 1/2・5万〜30万円。「申請後10月末までに事業開始」とあり、受付期間の表示なし＝unknown）
  - **長泉町**「中小企業産学共同研究支援補助金」（大学等とのソフトウェアの開発・改良の研究を含む、1/2・20万円。ページ冒頭の「令和8年度の受付を終了」がこの制度にも当たるか不明＝unknown）
- **創業・設備（備品）に使える町の制度**（yml）: 東伊豆町 創業支援事業補助金（町内者2/3・100万円〔飲食業120万円〕、随時）、松崎町 起業等支援事業補助金（設備等導入 1/2・100万円、既存事業者の新事業も対象、随時）、清水町 産業創出支援事業費補助金（1/2・30万円、随時）、小山町 賑わい商業創出支援事業助成金（卸小売・宿泊飲食、起業 最大200万円、期間不明）、吉田町 産業振興事業費補助金（新規創業 1/2・50万円、随時）、川根本町 起業及び事業継続チャレンジ補助金（起業 1/2・100万円、随時）、長泉町 起業・創業支援事業費補助金（**令和8年度受付終了**）。いずれもソフトウェア・クラウド利用料は対象として書かれていない（長泉町は PC・タブレットを対象外と明記）。
- **宿泊業**: 河津町 宿泊業の経営力基盤強化事業費補助金（町1/4＋県1/4、対象経費20万〜300万円。公開されているのは令和6年度分の手続きで、令和8年度は unknown）。
- **今申請できる（随時・受付中）とみられる町の制度（2026-11-11）**: 清水町の3制度（中小企業支援・経営革新計画支援・産業創出支援）、東伊豆町 創業支援、松崎町 起業等支援、吉田町 新規創業、川根本町 起業チャレンジ（起業の区分）。どれも受付期間の表示がなく「予算の範囲内」で、予算残額は公開されていない。
- **受付終了**: 長泉町 起業・創業支援（予算上限に達した）、長泉町 新製品等開発事業補助金（同じページの冒頭の表示）、森町 遠州の小京都ブランド向上支援事業補助金（【受付終了】、2023年3月1日更新）、清水町 物価高騰事業者支援給付金（受付終了）。
- **町が案内している国・県・広域の機会**: 森町のページで国の業務改善助成金（令和8年度の申請 2026-09-01〜10-14、終了）・静岡県よろず支援拠点。松崎町・西伊豆町の事業者向け **Instagramリール講座**（無料・抽選10名、2026-12-04・12-11、**申込 11/20 まで受付中**。補助金ではない。主催 賀茂地域『伊豆'sライフスタイル』創造エリア推進協議会）。
- 独自の事業者向け補助（IT・創業・設備・研修）が見つからなかった町: **南伊豆町・西伊豆町・函南町・森町**（各町の節に確認したページ）。
- **リンクの条件**は gov_ai_b.md の表（南伊豆町は申請制の規定あり、小山町・西伊豆町はトップページのみ、函南町・森町は条件のページが見つからない）。

### 二次情報のみ（secondary、記事では使わない）
- なし（補助金のまとめサイトは使っていない）

## 東伊豆町（higashiizu）
静岡県賀茂郡東伊豆町。確認したページ: しごと・産業 https://www.town.higashiizu.lg.jp/shigoto_sangyo/index.html 、産業振興 https://www.town.higashiizu.lg.jp/shigoto_sangyo/sangyo_shinkou/index.html 、起業・創業支援 …/sangyo_shinkou/1/index.html 、中小企業等支援 …/sangyo_shinkou/2/index.html
- **創業支援事業補助金**（yml）https://www.town.higashiizu.lg.jp/shigoto_sangyo/sangyo_shinkou/1/1181.html （更新日 2024年12月02日、観光産業課 観光商工係 0557-95-6301）: 町内者2/3・町外者1/2、上限 飲食業120万円・その他100万円。内外装・設備工事、什器備品、登記費用。特定創業支援事業の証明が要る
- 中小企業等支援は「東伊豆町短期経営改善資金」（融資）https://www.town.higashiizu.lg.jp/shigoto_sangyo/sangyo_shinkou/2/1180.html 、先端設備等導入計画、セーフティネット保証5号だけ
- ロケの補助（観光）、移住・住宅の補助は事業者の IT 向けではない
- **IT・DX・研修向けの独自の制度は見つからない**

## 河津町（kawazu）
静岡県賀茂郡河津町。確認したページ: 事業者のみなさま https://www.town.kawazu.shizuoka.jp/jigyousha/ 、産業・事業者の一覧 https://www.town.kawazu.shizuoka.jp/choumin/purpose06/
- **小規模事業者強化事業費補助金**（yml）https://www.town.kawazu.shizuoka.jp/jigyousha/kouri/ : 「事業費10万円以上60万円以内の 2分の1 （補助金額5万円以上30万円以内）」「※申請後10月末までに事業開始し、翌年3月25日までに完了すること」。対象に「ホームページ等の制作」「インターネットを活用した販路整備（ネットからの注文やメール配信システム整備するための費用）」。年度・受付期間の表示なし
- **宿泊業の経営力基盤強化事業費補助金**（yml）https://www.town.kawazu.shizuoka.jp/jigyousha/keieiryokukibankyoukajigyou/ : 「業務効率化や生産性向上の取組、社員寮の整備について支援」「※令和６年４月に静岡県が創設した「宿泊業の経営力基盤強化事業費補助金」との並行補助」。案内（観光サイト、更新日 2024-12-20）と要綱（令和６年７月29日要綱第25号）。令和8年度の受付は不明
- そのほか: 地域課題解決連携事業に関する補助制度 https://www.town.kawazu.shizuoka.jp/jigyousha/chiikikadaikaiketurenkeihojokin/ ・クラウドファンディング活用支援事業補助金 https://www.town.kawazu.shizuoka.jp/jigyousha/kuraudofandexingukatsuyousienn/ （要綱 PDF のみ、中身は未読）、創業及び経営改善対策貸付金利子補給金、インターンシップ交通費助成金、先端設備等導入計画
- **AI・DX を名指しした独自の制度は見つからない**

## 南伊豆町（minamiizu）
静岡県賀茂郡南伊豆町。確認したページ: 商工業 https://www.town.minamiizu.shizuoka.jp/category/bunya/gyoseimachizukuri/syoukougyou/ 、産業・しごと https://www.town.minamiizu.shizuoka.jp/category/bunya/sangyoshigoto/ 、商工観光課 商工振興係 https://www.town.minamiizu.shizuoka.jp/soshiki/minamiizu/shoukou/shoukou02/ 、タグ「補助金」https://www.town.minamiizu.shizuoka.jp/tag/%E8%A3%9C%E5%8A%A9%E9%87%91/
- 事業者向けは「南伊豆町中小企業事業資金融資制度」https://www.town.minamiizu.shizuoka.jp/docs/2013031300337/ （融資）、小規模事業参加登録制度、合宿等誘致補助金（観光）だけ
- 「令和４年度 南伊豆ビジネスセミナー『SNSを使った集客の基礎講座』」（過去の講座）
- **事業者向けの独自の補助金は見つからない**

## 松崎町（matsuzaki）
静岡県賀茂郡松崎町。確認したページ: 商工業支援 https://www.town.matsuzaki.shizuoka.jp/categories/guide/sangyo/shokogyo/ 、助成・手当 https://www.town.matsuzaki.shizuoka.jp/categories/quicksearch/joseiteate/
- **起業等支援事業補助金**（yml）https://www.town.matsuzaki.shizuoka.jp/docs/2018060500055/ : 事業所等整備・設備等導入 1/2・100万円（20万円以上）、借上 1/2・月3万円。起業者と事業展開者（既存事業者の新事業）
- 地域産業活性化対策事業補助 https://www.town.matsuzaki.shizuoka.jp/docs/2016020400056/ （地区・起業者3人以上の団体、事業費50万円以上の1/2・100万円、公開日 2016年）、地域産業振興助成 https://www.town.matsuzaki.shizuoka.jp/docs/2016020400063/ （団体の視察・研究会〔専門講師の研修〕、限度額7〜10万円・1/2〜2/3）。団体向けで、個々の企業の IT 導入向けではない
- 中小企業事業資金融資制度、先端設備等導入計画、セーフティネット保証
- **【事業者向け】Instagramリール講座**（無料、申込 11/20 まで）https://www.town.matsuzaki.shizuoka.jp/docs/2026102100019/ （gov_ai_b.md の松崎町の節）
- **IT・DX 向けの独自の補助金は見つからない**

## 西伊豆町（nishiizu）
静岡県賀茂郡西伊豆町。確認したページ: 西伊豆町の補助金・助成金等 https://www.town.nishiizu.shizuoka.jp/gyousei/hojo_josei.html （分野ごとの一覧）、中小企業者への経営支援 https://www.town.nishiizu.shizuoka.jp/kakuka/sangyou/kankou/business_support.html
- 経営支援は制度融資の一覧、償却資産の固定資産税の軽減、利子補給（事業資金等・事業場の新増設資金）、セーフティネット保証4号・5号だけ
- 補助金の一覧の事業者向けは「耐震化への経費補助(個人・企業)」など
- 電子地域通貨「サンセットコイン」https://www.town.nishiizu.shizuoka.jp/kakuka/sangyou/kankou/sunsetcoin.html
- **事業者向けの独自の補助金（IT・創業・設備）は見つからない**。松崎町と共同の Instagram リール講座（12/11 は西伊豆町保健センター）

## 函南町（kannami）
静岡県田方郡函南町。確認したページ: 事業者向け情報 https://www.town.kannami.shizuoka.jp/jigyosha/index.html 、補助金（事業者向け）https://www.town.kannami.shizuoka.jp/kurashi_tetsuzuki/hojokin/2/index.html 、商工業 https://www.town.kannami.shizuoka.jp/sangyo_machizukuri/sangyoshinko/4/index.html 、起業・創業支援 …/sangyoshinko/4/1/index.html
- 事業者向けの補助金の一覧は省エネ家電購入費補助金・こどもの居場所支援事業費補助金・国の省エネ支援パッケージの案内だけ
- 函南町企業立地設備投資奨励金 https://www.town.kannami.shizuoka.jp/sangyo_machizukuri/sangyoshinko/4/2932.html （工場・物流施設・研究所等〔ソフトウェア業を含む〕の立地、更新日 2024年03月01日）。中小企業の IT 導入向けではない
- 起業・創業の支援 https://www.town.kannami.shizuoka.jp/sangyo_machizukuri/sangyoshinko/4/1/2995.html （更新日 2025年03月10日。特定創業支援等事業の証明による登録免許税の減免・保証の特例など。町の補助金ではない）、**創業相談CAFE**（無料、函南町商工会）https://www.town.kannami.shizuoka.jp/sangyo_machizukuri/sangyoshinko/4/1/5600.html
- 函南町中小企業事業資金融資制度、BCP の支援紹介、県の中小企業支援策の案内 https://www.town.kannami.shizuoka.jp/jigyosha/5250.html 、令和8年度リフォーム助成事業（受付終了）
- **IT・DX・創業向けの独自の補助金は見つからない**

## 清水町（shimizu-town-shizuoka）
静岡県駿東郡清水町（静岡市清水区とは別）。確認したページ: 事業者向け情報 https://www.town.shimizu.shizuoka.jp/category00000004.html 、融資・助成 https://www.town.shimizu.shizuoka.jp/category00000049.html 、起業・進出 https://www.town.shimizu.shizuoka.jp/category00000047.html 。担当は産業観光課 産業振興係（055-981-8239）
- **中小企業支援補助金**（yml）https://www.town.shimizu.shizuoka.jp/chiiki/chiiki00262.html （2026年4月1日 更新）: 県外販路拡大支援 1/2以内・10万円/年、販売力促進支援（広報費。ホームページ作成費を含む）1/2以内・5万円/年
- **経営革新計画支援補助金**（yml）https://www.town.shimizu.shizuoka.jp/chiiki/chiiki00291.html : 1/2・50万円（要綱 第6条）。経費の例に「新技術の導入における社員育成に係る研修費」「新販路開拓に係る調査方法等を、職員に習得させるための研修費」
- **産業創出支援事業費補助金**（yml）https://www.town.shimizu.shizuoka.jp/chiiki/chiiki00384.html （2026年4月1日 更新）: 創業等 1/2・30万円、ホームページ作成費・設備費・備品購入費を含む
- 共同開発事業支援補助金 https://www.town.shimizu.shizuoka.jp/chiiki/chiiki00292.html : 異なる分野の2社以上の中小企業の共同の新商品等開発、要綱 https://www.town.shimizu.shizuoka.jp/content/300345538.pdf p2「２分の１以内とし、上限を50万円」（yml には入れていない。経費の例は機械等の購入・レンタル、広報宣伝費、原材料費、設計費）
- 清水町地域未来牽引事業費補助金 https://www.town.shimizu.shizuoka.jp/chiiki/chiiki00215.html （地域未来牽引企業の工場等の設置、7%・15,000千円。中小企業の IT 向けではない）、職業訓練校入校支援補助金（個人向け）、物価高騰事業者支援給付金（受付終了）
- **AI・DX を名指しした制度はないが、経営革新計画支援補助金は研修費・外注費・技術コンサルタント料が対象で、経営革新計画に AI 活用を入れれば使える可能性がある**（町に確認が要る）

## 長泉町（nagaizumi）
静岡県駿東郡長泉町。確認したページ: しごと・産業 https://www.town.nagaizumi.lg.jp/work_industry/index.html 、補助金・支援金・奨励金 https://www.town.nagaizumi.lg.jp/work_industry/co_support/2/index.html 、中小企業支援補助制度 https://www.town.nagaizumi.lg.jp/work_industry/co_support/2/9676.html （更新日 2026年10月09日）
- 中小企業支援補助制度のページ冒頭「【予算上限に達したため、令和8年度の受付を終了させていただきました】」。続く制度: 新製品等開発事業補助金（経営革新計画、2/3・100万円）、販路拡大事業補助金（展示会・宣伝材料、2/3・20万円、展示会の10日前までに申請）、**産学共同研究支援補助金**（yml。ソフトウェアの開発・改良を含む、1/2・20万円）、中小企業緊急時事業継続計画策定等補助金（10万円）、中小企業産業財産権取得補助金（1/2・30万円）。**冒頭の「受付終了」がどの制度に当たるかはページから読み取れない**
- **起業・創業支援事業費補助金**（yml）https://www.town.nagaizumi.lg.jp/work_industry/for_enterprises/9677.html （更新日 2026年07月02日）: 「※予算上限に達したため、令和8年度の受付を終了させていただきました」。上限 一般区域100万円・商業機能の誘導区域か特定創業支援の証明あり200万円。備品は10万円以上（PC端末・タブレット端末は含まない）、ウェブサイト作成費等は補助限度額の1/4以内
- 中小企業者等人材確保支援事業費補助金 https://www.town.nagaizumi.lg.jp/work_industry/for_enterprises/11348.html （更新日 2025年03月25日。職業紹介事業者への手数料、1/3・最大20万円）。研修・IT 向けではない
- サテライトオフィス等設置事業費補助金（R6で終了）、企業立地の補助金（3種）
- **AI・IT 導入・研修向けの独自の制度は見つからない**

## 小山町（oyama-town）
静岡県駿東郡小山町（栃木県小山市とは別）。確認したページ: 商工業 https://www.fuji-oyama.jp/life/4/15/74/ 、商工観光課 https://www.fuji-oyama.jp/soshiki/14/ 、各種補助金等について https://www.fuji-oyama.jp/page/4501.html （更新日 2026年3月19日。「中小企業・小規模企業を支援する各種補助金については、下記の中小企業庁のホームページをご覧ください。」とリンクだけ）
- **賑わい商業創出支援事業助成金**（yml）https://www.fuji-oyama.jp/page/4511.html : 卸売・小売・宿泊・飲食。起業 最大200万円、事業承継・第二創業・新分野進出 最大133万円、新商品開発 最大20万円（1/2〜2/3）。商工会の会員が条件。要綱（8.13MB）は未読
- 創業を志す方へ https://www.fuji-oyama.jp/page/3535.html （県の開業パワーアップ支援資金の案内。融資）、先端設備等導入計画、小山町地域まちづくり事業費補助金（地域団体、【受付終了】令和8年度）
- 第２次小山町中小企業・小規模企業振興基本計画（2026〜2030年度）の基本的施策に「（３）情報通信技術等の導入及び活用の支援」（計画の施策名。対応する補助金は見つからない）
- **IT・DX 向けの独自の補助金は見つからない**

## 吉田町（yoshida）
静岡県榛原郡吉田町。確認したページ: 事業者向け情報 https://www.town.yoshida.shizuoka.jp/business/ 、補助金 https://www.town.yoshida.shizuoka.jp/8137.htm
- **産業振興事業費補助金**（yml）https://www.town.yoshida.shizuoka.jp/3610.htm : 新規創業 1/2・50万円（飲食店舗 2/3・100万円）、団体の特産品開発・6次産業化（2/3・100万円）・イベント交流（1/2・100万円）
- 小規模事業者持続化補助金のページ https://www.town.yoshida.shizuoka.jp/6146.htm はコロナ特別対応型の売上減少証明の案内（古い。町の上乗せではない）
- 吉田町中小企業等奨学金返還支援事業費補助金 https://www.town.yoshida.shizuoka.jp/9844.htm （従業員の奨学金返還の支援。中身は未読）、地域活性化大規模イベント事業補助金（吉田カムカム補助金）
- **IT・DX・研修向けの独自の補助金は見つからない**

## 川根本町（kawanehon）
静岡県榛原郡川根本町。確認したページ: 補助金一覧 https://www.town.kawanehon.shizuoka.jp/kurashi_tetsuduki/hojokinitiran/index.html 、事業者 …/hojokinitiran/jigyousya/index.html 、事業者支援・補助金制度 https://www.town.kawanehon.shizuoka.jp/sangyoushigoto/shienhojo/index.html
- **起業及び事業継続チャレンジ補助金**（yml）https://www.town.kawanehon.shizuoka.jp/kurashi_tetsuduki/hojokinitiran/jigyousya/12399.html （更新日 2026年04月14日、産業振興課 商工業室 0547-56-2226）: 起業 1/2・100万円（備品・設備を含む）、事業継続 1/3・50万円（建物の改築・増築のみ）
- 地域産業立地事業費補助金（企業立地）、地域建設業経営強化融資制度、ネクストリーダーズプロジェクト（学生と事業者の登録）、茶業施設等整備強化事業費補助金・特産物振興事業費補助金（農業）
- 「初めてのスマホデビューを応援します」https://www.town.kawanehon.shizuoka.jp/kurashi_tetsuduki/hojokinitiran/kurashi/13966.html は町民向け（事業者向けではない）
- **IT・DX・研修向けの独自の補助金は見つからない**

## 森町（mori-town-shizuoka）
静岡県周智郡森町（北海道茅部郡森町とは別）。確認したページ: 企業立地・企業支援 https://www.town.morimachi.shizuoka.jp/gyosei/sangyo_shigoto/kigyoshien/index.html 、産業・しごと https://www.town.morimachi.shizuoka.jp/gyosei/sangyo_shigoto/index.html
- 森町遠州の小京都ブランド向上支援事業補助金 https://www.town.morimachi.shizuoka.jp/gyosei/sangyo_shigoto/kigyoshien/4474.html （**【受付終了】**、更新日 2023年03月01日。「遠州の小京都・森町」をキーワードとした新商品・新サービスの開発、機械装置等費・開発費・委託料・外注費など）
- 森町産業立地事業費補助金・産業立地奨励事業費補助金（製造業・ソフトウェア業・研究所・物流施設の工場等の新増設、固定資産税相当を奨励金、1年あたり300万円）https://www.town.morimachi.shizuoka.jp/gyosei/sangyo_shigoto/kigyoshien/1471.html 。中小企業の IT 導入向けではない
- 賃金引上げ及び中小企業・小規模事業者への各種支援施策 https://www.town.morimachi.shizuoka.jp/gyosei/sangyo_shigoto/kigyoshien/7021.html （国の業務改善助成金〔令和8年度 9/1〜10/14、終了〕・よろず支援拠点などの案内）
- 創業支援等事業計画、先端設備等導入計画、被災中小企業再建支援（令和4年台風15号、県の補助金）、令和7年台風15号の県制度融資
- **事業者向けの独自の補助金（IT・創業・設備）で受付中のものは見つからない**

## 事例の手がかり（cases 担当へ）
- 12町の補助金のページに、採択企業の成果・事例の紹介はなかった
- 河津町 DX推進計画の「河津桜まつり駐車場の AIカメラ」、森町の「AIを活用したオンラインワークショップ（D-Agree）」は行政の事例（gov_ai_b.md）

## 取れなかった項目・注意点
- **受付期間を書いていない制度が多い**（東伊豆町・松崎町・清水町・吉田町・川根本町・河津町・小山町）。「随時」は「ページに期間の表示がなく予算の範囲内」の意味で、予算残額はどの町も公開していない
- **長泉町の中小企業支援補助制度のページ冒頭の「令和8年度の受付を終了」が、どの制度に当たるか読み取れない**（町に確認が要る）
- 長泉町 起業・創業支援の補助率は表の見出しにあるとみられ、テキストで取れなかった（上限額だけ記録）
- 小山町 賑わい商業創出支援事業助成金の要綱（8.13MB）、川根本町の申請の手引き、河津町の地域課題解決連携事業・クラウドファンディング活用支援の要綱は読んでいない
- 河津町 宿泊業の経営力基盤強化は令和6年度分の資料だけで、令和8年度の実施は不明。**東伊豆町・南伊豆町・松崎町・西伊豆町では、県の宿泊業の経営力基盤強化の並行補助（町の要綱）が巡回の範囲で見つからなかった**
- 商工会の IT・AI セミナー・補助（町ごと）は今回探していない
- WebSearch はこのファイルの担当分で0回（gov_ai_b.md の4回が担当全体の回数）
