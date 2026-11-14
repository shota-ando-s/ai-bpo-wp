# 大阪府 泉北（泉大津市・和泉市・高石市・忠岡町）・泉南（岸和田市・貝塚市・泉佐野市・泉南市・阪南市・熊取町・田尻町・岬町）の12市町の補助金（AI・IT・DX・研修・省力化・生産性向上）2026年度

確認日: 2026-11-14（受付状況はこの日の時点）。12市町の公式サイトで、事業者向けの分類ページ（「事業者の方へ」「ビジネス・産業」「産業振興」「しごと・産業」「補助金一覧」など）・商工担当課の記事一覧・補助金のページを開き、補助・助成の名前の記事は本文を確かめた。商工会議所・商工会のサイト（岸和田・泉大津・和泉・高石・貝塚・泉佐野の各商工会議所、忠岡町・泉南市・阪南市・熊取町・岬町の各商工会）でも漏れを確かめた。府「府内市町村の概要 企業支援」https://www.pref.osaka.lg.jp/o040060/shinko/shichoson_gaiyou/kigyou.html （R7年度予算、更新日 2026-02-24）の市町の事業名も手がかりにした。curl で原文を読んだ（ヘッダーの付け替えはしていない）。

- **AI を名指しした市町独自の補助金**: **岸和田市「がんばる岸和田」企業経営支援補助金（デジタル化促進）**（実施要領に「「デジタル化」「ＩｏＴ」「ＡＩ導入」等であること」。ソフトウェア・クラウドの購入・利用料〔月額は6か月分〕・カスタマイズ・初期設定、ハードは5万円まで。1/2・30万円、既製市販品の総額10万円以上。2027-01-29 必着、予算上限で終了。yml: osaka-kishiwada-ganbaru-digital-2026）。ほかに対象分野に AI がある岸和田市「市内丸ごとラボ」実証事業推進補助金（1/2・100万円、新技術の実証向け。締切不明）
- **IT・DX・省力化・研修に使える制度**（yml に入れた）:
  - 受付中: 岸和田市 デジタル化促進（上）・**岸和田市 人材育成**（公的機関等の研修 1/2・10万円、2027-01-29 必着）・**熊取町 スマート化による生産性向上補助金**（自動化装置・ソフトウエア・パソコン等・専門家の報償費・セミナー受講料、2/3・75万円、熊取町商工会の支援で労働生産性3%以上の計画、商工会の会員・BCP が要件、当該年度内。yml: osaka-kumatori-smart-seisansei-2026）・**貝塚市 中小企業積極的事業展開促進補助金**（国・府の補助金の自己負担分の1/2、上限100万円・下限10万円）
  - 随時（rolling）: **和泉市 中小企業振興対策事業補助金（人材育成支援事業）**（ORIST・近畿職業能力開発大学校・中小企業大学校など指定機関の研修 1/2・20万円、事後申請可）・忠岡町 中小企業イメージアップ推進事業補助金（HP・PR動画・パンフレットの外注 1/2・5万円。AI・業務効率化ではない）
  - 締切不明（unknown）: 岸和田市「市内丸ごとラボ」実証事業推進補助金
- **国の補助金への上乗せ（addon）**: **貝塚市 中小企業積極的事業展開促進補助金**（「国・府等の補助対象経費の合計額から、国・府等の補助金額を除いた経費の2分の1以内（上限100万円、下限10万円）」、国・府等の交付決定から3カ月以内に申請。対象は「国（経済産業省）・大阪府（商工労働部）又はその関係団体が所管する支援（補助金事業）を活用した事業」）。addon {kind: remaining, ratio: 0.5}。**対象になる国の補助金の名前はページにない**（「支援の種類によっては対象にならない場合がございます」）ので、addon_to（digital-ai-donyu・shoryokuka-ippan・shinjigyo-monodukuri）は見込み。記事で使う前に貝塚市 産業戦略課（072-433-7193）に確認が要る。岸和田市・熊取町は国の補助金と併用できるが、国の補助額を差し引いた残りに市町の補助率を掛ける形（上乗せの制度ではない）
- **独自の IT・AI 向け制度が見つからない市町**: 泉大津市・高石市・泉佐野市・泉南市・阪南市・田尻町・岬町（忠岡町は HP 作成補助だけ）。泉大津市はプロ人材活用（市の委託の伴走支援、補助金ではない）、泉佐野市は無料の経営相談（よろず支援拠点と連携）と商工会議所の AI×RPA セミナー（12/15 無料）
- 期間の status は data/subsidies/README.md の値（open / closed / rolling / unknown）
- **業種の制限**: 岸和田市（デジタル化促進・人材育成）は対象外業種（風俗営業等・政治経済文化団体・宗教・バー等・投機目的の土地売買・連鎖販売業・競輪競馬等・興信所ほか）。医療法人等は対象に含む。熊取町は大規模小売店・コンビニ等のフランチャイズチェーン店舗は対象外。泉大津市の創業時設備導入支援は医療機関・介護サービス・調剤薬局など保険適用の事業とフランチャイズは対象外（yml に入れていない）
- **府の機関と市の制度の区別**: ORIST（地方独立行政法人大阪産業技術研究所。本部・和泉センターは和泉市）は府の機関。和泉市の補助金は ORIST の研修・試験の費用の1/2を出す（市の制度）。大阪府よろず支援拠点（泉佐野市・貝塚市が案内）は国の事業。貝塚商工会議所の生成AI セミナーの事業計画は府のサイトに載る（市の事業ではない）

## 岸和田市（kishiwada）

**IT向けの制度**
- **「がんばる岸和田」企業経営支援補助金（デジタル化促進）**: https://www.city.kishiwada.lg.jp/page/43-digital-hozyokinn.html 。yml: osaka-kishiwada-ganbaru-digital-2026
- **「がんばる岸和田」企業経営支援補助金（人材育成）**: https://www.city.kishiwada.lg.jp/page/43-jinzaiikusei.html 。yml: osaka-kishiwada-ganbaru-jinzai-2026
- **岸和田市「市内丸ごとラボ」実証事業推進補助金**: https://www.city.kishiwada.lg.jp/page/43-sinaimarugotorabohojokin.html 。yml: osaka-kishiwada-marugoto-lab-2026

**確かめたページ**
- 産業振興 https://www.city.kishiwada.lg.jp/life/4/25/ 、起業・経営支援 /life/4/25/116/ （がんばる岸和田の販路拡大・創業起業・省エネ診断・省エネ設備導入〔AI・IT ではない〕、中小企業サポート融資、新規オフィス開設補助、企業誘致）
- 岸和田商工会議所 https://www.kishiwada-cci.or.jp/ （独自の補助金なし。府の「大阪府業務改善・賃上げ促進補助金」の案内を 2026-08-18 に掲載＝府の制度。gov 担当の範囲）

## 泉大津市（izumiotsu）

**IT向けの制度: 見つからない**
- 確かめたページ: 補助金一覧（事業者・団体・自治会向け）https://www.city.izumiotsu.lg.jp/hojyokin/zigyousyamukehozyo/index.html 、地域経済課 補助金・助成金 https://www.city.izumiotsu.lg.jp/kakuka/koushitsu/tiikikeizaika/syoukou/hojyokin/index.html 、中小企業支援 /kakuka/koushitsu/tiikikeizaika/syoukou/tyuusyoukigyousien/index.html 。市の制度は商店街エリア活性化・創業支援事業（家賃）・創業時設備導入支援（1/2・20万円、パソコン等の汎用品は対象外）・ふるさと納税返礼品開発等支援・インバウンド等受入環境整備・港湾エリア活性化・中小企業退職金共済加入促進・利子補給で、IT・AI の補助ではない
- **プロフェッショナル人材活用支援事業**（市の委託事業者による外部プロ人材のマッチング・伴走、DX推進の分野も）https://www.city.izumiotsu.lg.jp/kakuka/koushitsu/tiikikeizaika/syoukou/professional/index.html 。補助金ではない。令和8年度のモデル事業者6社は決定済み
- 泉大津商工会議所 https://www.izumiotsu-cci.or.jp/ （独自の補助金なし。AI の SNS 動画セミナー 12/16 無料）

## 和泉市（izumi-city）

**IT向けの制度**
- **和泉市中小企業振興対策事業補助金（人材育成支援事業）**: https://www.city.osaka-izumi.lg.jp/kakukano/sangyoubu/sangyosinkositu/syoukoukanko/gyoumu/tyuushoukigyou/chusho_shien.html 。yml: osaka-izumi-jinzai-ikusei-2026

**確かめたページ**
- 【事業者向け】市補助制度のご案内（まとめページ）https://www.city.osaka-izumi.lg.jp/bizisan/18849.html 。ほかの制度（研究・開発支援 1/2・20万円、工業所有権、ものづくり技術・商品開発事業補助金〔大学等との共同研究開発、初年度100万円〕、創業等支援、産業集積促進、ホテル誘致、融資・利子補給）は IT・AI の導入費ではない
- 和泉商工会議所 https://www.izumicci.jp/ （独自の補助金なし。DX セミナー 9/15 は終了）

## 高石市（takaishi）

**IT向けの制度: 見つからない**
- 確かめたページ: 事業者の方へ https://www.city.takaishi.lg.jp/business/index.html 、産業競争課 商工 https://www.city.takaishi.lg.jp/kakuka/sougouseisaku/sangyoukyousou_ka/syoukou/index.html （地域商品券・創業支援・企業立地等促進制度〔市税優遇〕・工場立地法の緑地規制緩和・利子補給）
- 高石商工会議所 http://takaishicci.or.jp （独自の補助金なし。持続化補助金の案内）

## 忠岡町（tadaoka）

**IT向けの制度**
- 忠岡町中小企業イメージアップ推進事業補助金（HP・PR動画・パンフレットの外注 1/2・5万円）: https://www.town.tadaoka.osaka.jp/shigoto_sangyou/sangyou_shinkou/cyushou_shien/2540.html 。yml: osaka-tadaoka-imageup-2026（AI・業務効率化の補助ではない）

**確かめたページ**
- 中小企業等支援 https://www.town.tadaoka.osaka.jp/shigoto_sangyou/sangyou_shinkou/cyushou_shien/index.html （中小企業退職金共済加入補助・在住者正規雇用事業者支援補助金・先端設備等導入計画など）、商工業 /shigoto_sangyou/sangyou_shinkou/shoukougyou/index.html
- 府の表（R7）の「レベルアップ支援事業」450千円のリンク先は「ご指定のページは見つかりませんでした」
- 忠岡町商工会 https://www.tadaoka.or.jp （独自の補助金は見当たらない）

## 貝塚市（kaizuka）

**IT向けの制度**
- **貝塚市中小企業積極的事業展開促進補助金（国・府等の補助金事業を活用した事業）**: https://www.city.kaizuka.lg.jp/kakuka/sogoseisaku/sangyo/menu/syohogyosya_no_kata/kakusyu_hojokinseido.html 。yml: osaka-kaizuka-sekkyoku-tenkai-2026（上乗せ）

**確かめたページ**
- 商工業者のかたへ https://www.city.kaizuka.lg.jp/kakuka/sogoseisaku/sangyo/menu/syohogyosya_no_kata/index.html （融資・信用保証料補給・マル経利子補給・産業財産権取得促進・中小企業退職金共済掛金補助・ローカル10,000プロジェクト・先端設備等導入計画）、事業者の方 https://www.city.kaizuka.lg.jp/kigyo_jigyosha/index.html
- 貝塚商工会議所 https://kaizuka-cci.or.jp/ （独自の補助金なし。国・府の補助金の案内）

## 泉佐野市（izumisano）

**IT向けの制度: 見つからない**
- 確かめたページ: 事業所の方へ https://www.city.izumisano.lg.jp/business/jigyosyo.html （中小企業総合支援制度〔利子補給・保証料・中退共〕、経営相談〔無料〕、スモールスタートビジネス支援補助金〔オフィス整備、募集終了〕、企業等の奨学金返還支援）
- **泉佐野市中小企業者支援事業補助金**（ふるさと納税のクラウドファンディングで返礼品にもなる新商品開発・生産性向上の設備投資を補助、公募採択制、5年以上パートナー企業として返礼品を提供する意思が要件）https://www.city.izumisano.lg.jp/kakuka/seicyou/furusato/menu/shienhojokin/cyusyokigyo.html （更新日 2024年12月09日）。府の表（R7）877,657千円。2026年度の公募は確かめていない。AI・IT の導入費の補助ではないので yml に入れていない
- 泉佐野共創プロジェクト Sano FRONTIER（スタートアップ向け、令和8年度の募集終了）
- 泉佐野商工会議所 https://izumisano-cci.or.jp/ （独自の補助金なし。トップに「令和4年度 新事業展開テイクオフ補助金 ご案内」の古い記事。AI×RPA セミナー 12/15 無料）

## 泉南市（sennan）

**IT向けの制度: 見つからない**
- 確かめたページ: 産業振興課 商工労働係 https://www.city.sennan.lg.jp/kakuka/shiminseikatu/sangyoushinkou/shokorodokakari/index.html 、中小企業支援 /town/chuushoukigyiousien/index.html 、まちづくり /town/index.html （先端設備等導入計画・利子補給・中小企業退職金共済掛金補助・空き店舗等活用対策・＃ふるさと納税3.0）
- 泉南市商工会 https://sennan-sci.or.jp/ （独自の補助金なし。持続化補助金の案内）

## 阪南市（hannan）

**IT向けの制度: 見つからない**
- 確かめたページ: 事業者の方へ https://www.city.hannan.lg.jp/business/index.html 、商工業 /business/syoukougyou/index.html 、起業創業支援事業(バウチャー)補助金 /business/kigyo_sogyoshien/7516.html （新築・広告宣伝・登記 1/2・25万円）
- 阪南市商工会 http://hannan-sci.jp （独自の補助金なし）

## 熊取町（kumatori）

**IT向けの制度**
- **産業活性化基金事業補助金（スマート化による生産性向上補助金）**: https://www.town.kumatori.lg.jp/sangyo_kanko/sangyo_shinko/jigyosha_kojinmukeshien/13797.html 。yml: osaka-kumatori-smart-seisansei-2026

**確かめたページ**
- 事業者・個人向け支援 https://www.town.kumatori.lg.jp/sangyo_kanko/sangyo_shinko/jigyosha_kojinmukeshien/index.html 、商工業 /sangyo_kanko/sangyo_shinko/shokogyo/index.html 、補助金・給付金・助成金等 /moraeruokane/index.html （事業者・団体向けの欄は空）。産業活性化基金事業補助金のほかのメニュー（熊取ブランド・創業支援・キャッシュレス 2/3・5万円・6次産業化・農業者のスマート化 2/3・100万円）
- 熊取町商工会 https://kumatori-sci.com/ （町の補助金の前提の支援をする）

## 田尻町（tajiri）

**IT向けの制度: 見つからない**
- 確かめたページ: しごと・産業 https://www.town.tajiri.osaka.jp/shigoto_sangyo/index.html 、商工業 /shigoto_sangyo/shokogyo/index.html （記事は出前講座の募集だけ）、各種補助金 /gyoseijoho/kakushuhojokin/index.html （事業者向けはローカル10,000プロジェクトだけ）
- 商工会はない（泉佐野商工会議所の地区）

## 岬町（misaki-town）

**IT向けの制度: 見つからない**
- 確かめたページ: 産業観光促進課 商工業 https://www.town.misaki.osaka.jp/soshiki/toshi_seibi/sangyo/shoukougyou/index.html （先端設備等導入計画・セーフティネット保証）、お知らせ /soshiki/toshi_seibi/sangyo/oshirase/index.html
- 第2次岬町DX基本計画 PDF p.11 で第1次の「町内の事業者等のデジタル化相談体制の整備」「事業者の電子決済システムの導入支援」は「未実施」
- 岬町商工会 http://misaki-sci.main.jp/ （創業支援セミナー。独自の補助金なし）
