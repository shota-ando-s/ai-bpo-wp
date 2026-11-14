# 大阪府 北河内・中河内の10市の補助金（AI・IT・DX・研修・省力化・生産性向上）2026年度

確認日: 2026-11-14（受付状況はこの日の時点）。10市（守口市・枚方市・寝屋川市・大東市・門真市・四條畷市・交野市・八尾市・柏原市・東大阪市）の公式サイトで、事業者向けの分類ページ（「産業・商工業」「事業者支援」「ビジネス・産業」「融資・補助金等」など）・商工担当課の記事一覧・補助金のページを開き、補助・助成の名前の記事は本文を確かめた。商工会議所・商工会のサイト（北大阪・守口門真・大東・八尾・東大阪の各商工会議所、四條畷市商工会・柏原市商工会）でも漏れを確かめた。府「府内市町村の概要 企業支援」https://www.pref.osaka.lg.jp/o040060/shinko/shichoson_gaiyou/kigyou.html （R7年度予算、更新日 2026-02-24）の市の事業名も手がかりにした。curl で原文を読んだ（ヘッダーの付け替えはしていない）。

- **AI を名指しした市独自の補助金は0件**
- **IT・DX・省力化・研修に使える制度**（yml に入れた）:
  - 受付中: **四條畷市 なわて事業者チャレンジ支援補助金（設備導入支援）**（先端設備等導入計画の認定が前提、**ソフトウェアの取得費も対象**、50％・100万円、2025-09-01〜。2026-12-31 までに事業完了。事務局は四條畷市商工会。yml: osaka-shijonawate-challenge-setsubi-2026）、**守口市 工業活性化支援補助金**（生産性向上設備 50％・25万円／人材育成 50％・15万円。**鉱業・建設業・製造業等の工業のみ**。予算がなくなり次第締切）、**八尾市 意欲ある事業者経営・技術支援補助金（区分1・人材育成）**（研修受講料・講師謝礼、10万円、〜2027-03-31）、**交野市 産業振興事業補助金（産業人材育成）**（指定研修先の受講料、1件3万円、先着）
  - 随時（rolling）: **寝屋川市 中小企業経営・技術支援補助金（国等補助金の申請サポート）**（国・府の設備投資の補助〔補助額100万円以上〕の申請を外部専門家に頼む費用、1/2・30万円）
  - 受付終了: **八尾市 意欲ある事業者経営・技術支援補助金（区分2・新事業展開/生産性向上）**（1/2〔小規模2/3〕・200万円、〜2026-04-30）、**大東市 中小企業人材スキルアップ支援補助金**（大学・公的機関等の研修受講料 1/2・6万円。「令和８年度予算上限に達したため受付を終了」）
- **国の補助金への上乗せ（addon）**: **見つからない**。寝屋川市の申請サポートは国・府の補助金の申請費用の補助で、補助額への上乗せではない。四條畷市の設備導入支援は国の「先端設備等導入計画」（固定資産税の特例）の認定が前提
- **独自の IT 向け制度が見つからない市**: 枚方市・門真市・柏原市・東大阪市（東大阪市・門真市は製造業向けの制度が多いが、IT・AI を対象にしたものはない。東大阪市は商工会議所の無料の IT 専門家派遣がある）
- 期間の status は data/subsidies/README.md の値（open / closed / rolling / unknown）
- **業種の制限**: 守口市 工業活性化支援補助金は鉱業・建設業・製造業等（卸売・小売・サービスは対象外）。東大阪市の省エネ設備更新・門真市の企業魅力アップは製造業のみ（yml に入れていない）

## 守口市（moriguchi）

**IT向けの制度**
- **守口市工業活性化支援補助金**（生産性向上設備等設置事業 50％・25万円、人材育成支援事業 50％・15万円、ホームページ開設又は改修事業 50％・15万円 ほか）: https://www.city.moriguchi.osaka.jp/kakukanoannai/shiminseikatsubu/chiikishinkoka/sangyoshinkokigyoshien/jigyousyasien/3429.html 。yml: osaka-moriguchi-kogyo-seisansei-2026・osaka-moriguchi-kogyo-jinzai-2026

**確かめたページ**
- 事業者支援の一覧 https://www.city.moriguchi.osaka.jp/kakukanoannai/shiminseikatsubu/chiikishinkoka/sangyoshinkokigyoshien/jigyousyasien/index.html （商業振興事業支援補助金・もりクルート・奨学金返還支援制度導入助成などは IT の補助ではない）
- 守口門真商工会議所 http://www.mk-cci.jp/ （独自の補助金なし。IT課題・解決隊の相談）

## 枚方市（hirakata）

**IT向けの制度: 見つからない**
- 確かめたページ: 産業・商工業 https://www.city.hirakata.osaka.jp/category/4-12-0-0-0-0-0-0-0-0.html 、事業者支援・補助金・税制優遇等 https://www.city.hirakata.osaka.jp/soshiki/22-4-0-0-0_3.html 。市独自の制度はテイクオフ補助金（創業の賃料）、展示商談会出展支援、商店街等活性化促進、住工共生環境対策（工場の騒音等対策）、商品開発支援（クラウドファンディング）、地域産業基盤強化奨励金、若手人材の奨学金返還補助（2026-10-01 受付開始）で、IT・AI の補助ではない
- プロ人材活用（ひらっく）は**府の「大阪府副業・兼業人材活用促進補助金」**を案内（府の制度。HP の SEO 強化の事例）
- 北大阪商工会議所 https://kocci.or.jp/ （独自の補助金なし。持続化補助金の案内）

## 寝屋川市（neyagawa）

**IT向けの制度**
- **寝屋川市中小企業経営・技術支援補助金**（国等補助金の申請サポート 1/2・30万円、展示会出展 1/2・20万円、産学・企業間の交流促進）: https://www.city.neyagawa.osaka.jp/organization_list/toshidesign/toshiikka/syoukougyou/notice/kougyou-hojyokin.html 。yml: osaka-neyagawa-keiei-gijutsu-2026

**確かめたページ**
- ビジネス・産業 https://www.city.neyagawa.osaka.jp/Industry_business/index.html 、商工業関係のお知らせ /Industry_business/syoukougyou/26651.html （中小企業経営・技術支援補助金・BCP・府の商店街等モデル創出普及事業・インボイス・工場立地法）

## 大東市（daito）

**IT向けの制度**
- **大東市中小企業人材スキルアップ支援補助金**（**受付終了**、予算上限）: https://www.city.daito.lg.jp/soshiki/5/1779.html 。yml: osaka-daito-skillup-2026

**確かめたページ**
- 市補助制度のご案内 /soshiki/5/1779.html（スキルアップ・事業資金融資活用サポート・起業応援・企業立地）、商工業の一覧 https://www.city.daito.lg.jp/life/5/24/99/ 。大東市物価高騰対策融資活用補助金（/soshiki/5/73362.html。大東商工会議所トップ「融資活用で最大10万円が交付される大東市の補助金」）は融資の補助で IT 向けではない
- 大東商工会議所 https://www.daito-cci.or.jp/

## 門真市（kadoma）

**IT向けの制度: 見つからない**
- 確かめたページ: まちづくり・産業・労働 https://www.city.kadoma.osaka.jp/machizukuri_rodo/index.html 、工業 /machizukuri_rodo/kogyo/index.html 、中小企業等関連 /machizukuri_rodo/chushokigyo/index.html
- 市独自の制度（IT 向けではないので yml に入れていない）:
  - **門真市「職住近接のまち」実現のための企業魅力アップ事業補助金**（https://www.city.kadoma.osaka.jp/machizukuri_rodo/kogyo/24357.html 、更新 2026-04-20「令和8(2026)年度の申請受付を開始」）: 市内の中小ものづくり企業（**製造業のみ**）。労働環境整備事業【一般】「休憩室及び食堂の整備、アシストツール等の導入、福利厚生等に要する経費」1/2（カドマイスター認定企業は2/3）・20万円 ほか、企業の魅力向上・発信、インターンシップ、カーボンニュートラル。交付決定後に着手、2月末日までに完了。受付終了の告知はページにない
  - 門真市産業誘導区域移転補助金（/kogyo/25831.html）、ものづくり企業立地促進制度奨励金、商業振興対策事業補助金（/shogyo/5094.html）
- 守口門真商工会議所 http://www.mk-cci.jp/ （トップに府の「業務改善・賃上げ促進補助金」の案内〔府の制度〕）

## 四條畷市（shijonawate）

**IT向けの制度**
- **（新）なわて事業者チャレンジ支援補助金（設備導入支援補助金）**: https://www.city.shijonawate.lg.jp/page/14-48750.html ・商工会 https://nawate-sci.or.jp/nawatechallenge_2025/index.htm 。yml: osaka-shijonawate-challenge-setsubi-2026。同じ制度の事業計画策定支援補助金（中小企業診断士・税理士・認定支援機関の報酬、80％・15万円）・企業価値向上支援補助金（ホームページ開設・人材確保など 50％・20万円）は yml の note に書いた
- 前の制度（令和5年6月〜令和7年5月）は「受付を終了しました」（商工会トップ 2025-06-01）。結果 /page/107862.html

**確かめたページ**
- しごと・産業 https://www.city.shijonawate.lg.jp/life/7/ 、商工業 /life/7/39/183/ （国・府・大阪産業局の制度の案内が多い）

## 交野市（katano）

**IT向けの制度**
- **交野市産業振興事業補助金（産業人材育成事業）**（受付中）: https://www.city.katano.osaka.jp/docs/2014062500017/ 。yml: osaka-katano-jinzai-ikusei-2026

**確かめたページ**
- 事業者の方へ https://www.city.katano.osaka.jp/navi/jigyosha/ 、産業振興 /categories/bunya/chiikishinko/sangyo/

## 八尾市（yao）

**IT向けの制度**
- **八尾市意欲ある事業者経営・技術支援補助金**: 一覧 https://www.city.yao.osaka.jp/sangyou_business/yuushi_hojokin/1012107/index.html 。区分2（新事業展開・生産性向上、**公募終了**）yml: osaka-yao-iyoku-kubun2-2026、区分1（人材育成など、受付中）yml: osaka-yao-iyoku-kubun1-jinzai-2026

**確かめたページ**
- 融資・補助金等 https://www.city.yao.osaka.jp/sangyou_business/yuushi_hojokin/index.html 、産業振興・企業支援 /sangyou_business/sangyoushinkou_kigyoushien/index.html 。八尾市・シティ信金提携ものづくり支援ローン（融資）
- 八尾商工会議所 https://www.yaocci.or.jp/ （デジタルツールお悩み相談〔無料〕。独自の補助金は見当たらない）

## 柏原市（kashiwara）

**IT向けの制度: 見つからない**
- 確かめたページ: 産業 https://www.city.kashiwara.lg.jp/category/bunya/kurashi_tetsuzuki/sangyo/ と記事一覧（創業支援事業・空き店舗）
- 柏原市商工会 http://www.kashiwara-sci.org/ （トップに市の補助金の案内はない。柏原市地域応援商品券）

## 東大阪市（higashiosaka）

**IT向けの制度: 見つからない**（IT 化は東大阪商工会議所の無料の IT 専門家派遣「ITなんでも相談窓口」で支援。gov_ai_2.md）
- 市独自の制度（IT 向けではないので yml に入れていない）:
  - **令和8年度東大阪市省エネ設備更新事業補助金**（https://www.city.higashiosaka.lg.jp/0000035654.html 、更新 2026-11-06、「【申請受付中】」）: 先端設備等導入計画（令和7年4月以降の認定）の**製造業者**が、sii の「生産設備」（旋盤・マシニングセンタ・レーザー加工機・射出成形機・プレス機械など）に更新する費用、1/2・300万円。申請期間 令和8年6月1日〜令和9年2月28日（予算がなくなり次第終了）。国の省エネ・非化石転換補助金（生産設備）と府の脱炭素の補助金とは併用可、それ以外の国・府の補助金とは併用不可。ページに「補助金の申込状況について(令和8年10月30日10時時点)」の見出しがあるが、割合は画像で読めていない
  - 「【受付終了のお知らせ】最大500万円補助！省エネ設備導入でコスト削減と賃上げを後押し」（/0000044708.html）
  - 高付加価値化促進事業助成金（研究開発・経営力向上）、医工連携事業化促進事業助成金、国内・海外展示会出展支援助成金、産業財産権活用事業助成金、創業促進インキュベートルーム賃料助成金（分類「高付加価値化」https://www.city.higashiosaka.lg.jp/category/19-1-6-0-0-0-0-0-0-0.html 。製造業向け、IT 向けではない）
- 確かめたページ: 事業者の方へ https://www.city.higashiosaka.lg.jp/category/19-0-0-0-0-0-0-0-0-0.html 、経済対策 /category/19-1-2-...、人材育成 /category/19-1-7-...、製造業向け支援施策 /0000037662.html と支援施策ガイド（令和8年5月）

## 府の制度と取り違えやすいもの（このファイルには入れていない）

- 府「大阪府副業・兼業人材活用促進補助金」（枚方市のページが案内）、府「業務改善・賃上げ促進補助金」（守口門真商工会議所が案内）、府「中小企業の高効率空調機の導入」「中小企業展示商談会出展支援事業」（枚方市のページが【大阪府】と明記）、大阪産業局「小規模企業者等設備貸与制度」（四條畷市のページ）。府域の補助金は gov 担当（subsidy_pref.yml）
- 東大阪商工会議所の「生成AI業務活用ワークショップ」は「令和 8 年度大阪府地域活性化事業」（府の財源）
