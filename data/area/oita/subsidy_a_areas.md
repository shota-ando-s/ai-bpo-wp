# 大分県（県・県域の機関）と14市の AI・IT 向け補助金（2026-11-04 確認）

データ本体は `subsidy_a.yml`（18件。すべて県・市・ツーリズムおおいたの公式ページ・交付要綱・募集要領・委託仕様書で確認。市のページを WebFetch の要約で読んだもの〔臼杵市〕は yml の note に書いた）。「受付中」「随時」でも予算に達すると締め切られる。一覧の手がかりに、県の「先端技術・DX推進支援制度」https://www.pref.oita.jp/site/tyusyodx/ （4分類: クラウドサービス導入等による業務デジタル化支援／DXコーディネーターによる課題整理・施策提案等の相談支援／国補助金への県独自の上乗せ支援／データ活用を推進する支援者向け人材育成支援）、県の「助成金・補助金」一覧 https://www.pref.oita.jp/life/sub/6/ （工業・科学技術、経営・金融）、商工観光労働部の各課（先端技術挑戦課・工業振興課・産業GX推進室・経営創造・金融課・商業・サービス業振興課・産業人材政策課・観光政策課）の記事一覧、公益財団法人大分県産業創造機構の補助金一覧 https://columbus.or.jp/subsidy/ 、県の「おおいた中小企業支援ポータル」の公募中一覧 https://oita-chusho.jp/support/ （2026-11-04 現在）を使い、**そのうえで14市すべての商工担当課の記事一覧・事業者向けの分類ページを開いて確かめた**。

2026-11-04時点で受付中（open）・随時（rolling）は次の12件。
- 受付中（県）: **大分県省力化・生産性向上支援補助金（省力化投資）**（国の省力化投資補助金〔カタログ注文型・一般型〕の確定額の1/3〔大幅な賃上げは1/2〕、上限750万円、**県への申請〜2027/1/29**〔事前登録はチラシで1/22〕）、**同（デジタル化）**（国のデジタル化・AI導入補助金のインボイス対応類型に経費の1/12・上限52.5万円、賃上げ要件、**〜2027/1/29**。**通常枠は対象外**）、**先端技術挑戦プロジェクト産学連携創出支援事業費補助金（可能性調査枠）**（テーマ「ロボティクス・ＡＩ（人工知能）」ほか、1/2・100万円、**〜2026/11/13 17時**）、**宿泊事業者ＤＸ推進事業費補助金**（2/3・300万円〔賃上げ枠3/4・340万円〕、**2026/8/3〜12/28**、月額利用料は対象外）、**大分県宿泊業経営力強化加速化事業費補助金**（ツーリズムおおいた。観光庁の省力化投資補助事業への上乗せ 1/6・340万円〔賃上げ枠1/4・500万円〕、**7/1〜12/25**）
- 随時（県）: **大分県中小企業等デジタルツール導入補助金**（SaaS・ソフトウェア・連携構築、2/3・25万円〔賃上げ枠3/4・30万円〕。**県の DX総合支援事業〔ONE OITA〕の DX コンサルタントの支援を受けた企業だけ**）、**大分県副業・兼業人材活用事業費補助金**（県のプロフェッショナル人材活用センター経由の初回、8/10・50万円）
- 受付中（市）: **津久見市 小規模事業者等物価高騰対策環境整備支援事業補助金**（IT導入・システム経費・キャッシュレスなど、4/5・20万円、**〜2027/1/29**。商工会議所の支援が要件）
- 随時（市）: **大分市 中小企業者経営力強化促進補助金（人材育成応援事業）**（研修1/2、**DX研修は2/3**、1人10万円・1者30万円。**2026-10-28に「予算が残りわずか」**）、**大分市 中小企業者設備投資補助金**（生産工程の設備、1/2・150万円。生産管理システムの新規導入は条件付きで対象。小規模企業者は対象外）、**日田市 中小企業等賃上げ環境整備支援助成金**（国の業務改善助成金・持続化補助金などの自己負担の1/2・50万円）、**由布市 魅力ある職場づくり支援事業補助金**（研修受講・資格取得など、1/2・10万円〔特別枠4/5・30万円〕）

**今年度の募集を終えたAI・デジタル向けの補助**（6件）: 県の**先端技術挑戦プロジェクト（研究開発枠）**（2/3・1,500万円、**〜4/10**）、**大分市 小規模事業者競争力強化支援事業補助金（DX推進枠）**（2/3・40万円、後期の申請**〜10/23**、エントリー多数で抽選）、**臼杵市 産業・雇用促進事業補助金**（機械装置・システム構築費、1/2・150万円、**〜6/10**）、**豊後高田市 小規模事業者等物価高騰対策支援事業補助金**（1/2・25万円、**9/14 予算到達**）、**豊後大野市 中小企業者生産性向上設備等導入補助金**（導入例に「AI検査・計測装置」、2/3・200万円、**4/1〜6/30**）、**由布市 中小企業等経営力強化支援事業**（DXを用いた取組2/3・30万円、**予算到達で終了**）。

**国の補助金への上乗せ（addon）は県に2本ある**。省力化投資補助金（national.yml の shoryokuka-ippan）への上乗せは addon（cost_ratio 0.167＝国1/2のときの経費の1/6）を書いた。デジタル化・AI導入補助金の上乗せはインボイス対応類型だけが対象で、national.yml の digital-ai-donyu（通常枠）は対象外のため addon を書いていない。日田市の賃上げ環境整備支援助成金、ツーリズムおおいたの宿泊業経営力強化加速化補助金も上乗せだが、上乗せ先（業務改善助成金・持続化補助金、観光庁の省力化投資補助事業）が national.yml にないため addon を書いていない。

**AI を要件・テーマ・例示に書いた制度は4つ**: 県の先端技術挑戦プロジェクト産学連携創出支援事業費補助金（5テーマの1つが「ロボティクス・ＡＩ（人工知能）」）、県の上乗せ補助金（上乗せ先が国の「デジタル化・AI導入補助金」）、豊後大野市 生産性向上設備等導入補助金（導入例「AI検査・計測装置」）、大分市 人材育成応援事業（DX研修＝経済産業省・IPA のデジタルスキル標準の項目。AI の語はない）。

**経済産業局**: 九州経済産業局（kyushu.meti.go.jp）はこの環境から 403（shared.md）。県産業創造機構の告知で、九州経済産業局・NEDO・中小機構九州本部・INPIT・機構の共催「研究開発等支援制度説明会 in 大分」（2026-12-17）がある（Go-Tech 事業など。AI 導入の補助ではない）。

## 大分県（県・県域の機関）

見たページ:
- 県「先端技術・DX推進支援制度」https://www.pref.oita.jp/site/tyusyodx/ と4分類の一覧（list22448-29350／29353／29351／29352）。「クラウドサービス導入等による業務デジタル化支援」の一覧には「R7年度デジタルスキル向上支援事業事例集」だけ、「DXコーディネーター」の一覧には「【終了しました】ゼロから始める「AI×DX戦略」セミナー」だけ、「人材育成支援」の一覧には R7 年度の ONE OITA 経営バディ育成プログラムだけ
- 県「大分県省力化・生産性向上支援補助金」https://www.pref.oita.jp/site/tyusyodx/uwanosehojokin2026.html （2026-09-09更新）、チラシ https://www.pref.oita.jp/uploaded/attachment/2269739.pdf 、交付要綱（省力化投資、2026-08-07施行）https://www.pref.oita.jp/uploaded/attachment/2274613.pdf 、交付要綱（デジタル化、2026-04-01施行）https://www.pref.oita.jp/uploaded/attachment/2263184.pdf 、委託の仕様書 https://www.pref.oita.jp/uploaded/attachment/2260220.pdf 、事務局 https://oita-nta-hojo.jp （WebFetch）（yml: oita-shoryokuka-uwanose・oita-digital-uwanose）
- 県「大分県中小企業等デジタルツール導入補助金について」https://www.pref.oita.jp/site/tyusyodx/dx-toolhojyo.html （2026-08-21更新）、交付要綱 https://www.pref.oita.jp/uploaded/attachment/2279217.pdf 、「中小企業向けDX総合支援窓口の開設について」https://www.pref.oita.jp/soshiki/14270/dx-sogo.html （2026-06-23更新。手続きサポート窓口は大分銀行コワーキングスペース「ビジカム」〔大分市萩原〕。事業紹介チラシ 2271509.pdf は画像で本文を取れなかった）、委託仕様書「令和8年度中小企業等ＤＸ総合支援事業委託業務仕様書」https://www.pref.oita.jp/uploaded/attachment/2261466.pdf （窓口 2026-06-01目安〜2027-03-31、DXコンサルタント年間150件程度、補助金100社程度・2027年1月末までに補助事業完了の想定）。専用サイト https://one-oita.jp/dx-2026 は WebFetch でタイトル「ONE OITA 令和8年度 中小企業等DX総合支援プログラム」しか取れなかった（yml: oita-dx-tool）
- 県 先端技術挑戦課の記事一覧 https://www.pref.oita.jp/soshiki/14270/ : 「令和８年度先端技術挑戦プロジェクト産学連携創出支援事業費補助金 公募のお知らせ」https://www.pref.oita.jp/soshiki/14270/sentan-sangakurenkei2026.html （yml: oita-sentan-sangaku-kanousei・oita-sentan-sangaku-kenkyu）。ほかに「イノベーション創出人材育成プログラム」https://www.pref.oita.jp/soshiki/14270/senpuroinobezinzai2026.html （AI・ロボットなど先端技術を背景にした人材育成。県内中小企業4社、2名以上で参加、事務局は三菱UFJリサーチ＆コンサルティング。補助金ではない・費用の記載なし）、「Digital & AI Innovation Bridge（DAIB）」https://www.pref.oita.jp/soshiki/14270/daib.html （2026-07-24更新。ベンダーと県内事業者のマッチングのプラットフォーム。補助金ではない＝gov 担当）、DAIBセミナー「AIエージェント最前線」、ドローン産業研究開発事業費補助金（第2次公募）、宇宙・次世代空モビリティの補助金（AI 導入向けではない）
- **デジタルものづくり補助（cases 担当の照合依頼）**: 「ものづくり中小企業デジタル化推進事業費補助金」（IoT化250万円・AI化/ロボット化500万円、1/2）は令和5年度（2023-04-07〜05-26）・令和6年度（2024-04-08〜05-24）の制度（WebSearch の要約。R6 公募要領 https://www.pref.oita.jp/uploaded/attachment/2212005.pdf は2026-11-04に 404）。令和7年度は「大分県スマートものづくり加速化推進事業費補助金」（通常枠1/2・400万円、賃上げ枠2/3・600万円、2025-04-07〜05-23。WebSearch の要約で、公募要領 https://pref.oita.jp/uploaded/life/2296978_4463758_misc.pdf は 404）。**令和8年度の公募は、工業振興課の記事一覧 https://www.pref.oita.jp/soshiki/14200/ （2ページ）・県の「助成金・補助金」の工業・科学技術の一覧・おおいた商工労働ポータル「補助金（製造業）」https://www.pref.oita.jp/site/sme/list21659-25675.html （空）で見つからなかった**。yml に入れていない（`confidence: secondary` の過年度の値は記事で使わない）
- **DXコーディネーター事業・ONE OITA（cases 担当の照合依頼）**: 令和7年度の「中小企業等の課題解決に向けたDXコーディネーター事業」は事例集（cases.md）が残るが、令和8年度の募集ページは見つからなかった。令和8年度は「中小企業等DX総合支援事業」（窓口・DXコンサルタント・デジタルツール導入補助金）に変わったと読める（仕様書と県のページ。同じ事業の後継とは県のページに書いていない）。ONE OITA は令和7年度の「経営バディ育成プログラム」（支援者向け研修、運営はイジゲングループ株式会社、https://www.pref.oita.jp/site/tyusyodx/oneoita2025.html ）と、令和8年度の DX総合支援事業の専用サイトの名前の両方に使われている
- 県 産業人材政策課「大分県副業・兼業人材活用事業費補助金のご案内」https://www.pref.oita.jp/soshiki/14320/hukugyoukengyou.html （2026-03-27更新）、詳細版 2296238_4709206_misc.pdf（yml: oita-fukugyo-jinzai）。「人材確保支援メニューのご案内」2026年度版 https://www.pref.oita.jp/uploaded/life/2298222_4720147_misc.pdf （県の人材確保の補助は面接旅費・外国人労働者等就業環境等整備促進補助金〔中小企業団体中央会、2026-11-02〜11-30 に延長〕など。DX・AI 向けの補助はない）
- 県 観光政策課 https://www.pref.oita.jp/soshiki/14180/ : 「宿泊事業者ＤＸ推進事業費補助金」https://www.pref.oita.jp/site/shukuhakuzei/syukuhakudxhojo2026.html （yml: oita-shukuhaku-dx）、「宿泊税対応システム改修事業費補助金」（宿泊税のためのシステム改修。AI・DX 向けではないので yml に入れていない。臼杵市のページの要約で10/10・200万円）、ツーリズムおおいた「令和８年度大分県宿泊業経営力強化加速化事業費補助金」https://www.visit-oita.jp/news/detail/1234 （yml: oita-shukuhaku-keieiryoku）、「宿泊施設の清掃業務効率化のためのガイドブック」
- 県 商業・サービス業振興課 https://www.pref.oita.jp/soshiki/14300/ : 「Instagram×生成AI活用スクール」https://www.pref.oita.jp/soshiki/14300/sns-ai.html （大分市・佐伯市・宇佐市で全3回＋導入編、各地域15事業者程度。補助金ではない）。おおいた商工労働ポータルの「観光関連産業の業務効率化を支援します！（〆切10/31）」https://www.pref.oita.jp/soshiki/14300/sa-bishojo.html は 404（ページ削除）で、年度・内容を確かめられなかった
- 県 経営創造・金融課 https://www.pref.oita.jp/soshiki/14040/ : 「大分県新価値創出支援補助金」（クリエイターとの協働、1/3・30万円〔賃上げ1/2・40万円〕、6/8〜8/28で終了）、経営革新計画の承認制度。WebSearch の要約に「経営革新加速化支援事業費補助金（上限200万円、公募終了）」が出たが、県のページは開いていない（`confidence: secondary`、yml に入れていない）
- 県 産業GX推進室・工業振興課: エコエネルギー導入（終了）、GX投資促進、グリーン・コンビナート、ものづくり循環経済、特別高圧電気料金（いずれも AI・IT 向けではない）
- 公益財団法人大分県産業創造機構 https://columbus.or.jp/ ・補助金一覧 https://columbus.or.jp/subsidy/ : 「第18回おおいた中小企業活力創出基金助成金（かがやき）」（商品開発、2/3・200万円、2026-09-09〜**11-04 17時必着**。AI・IT 向けではないので yml に入れていない）と「研究開発等支援制度説明会 in 大分」（12/17）の2件だけ。研修は「AI活用戦略研修」（採用戦略・経営戦略・営業戦略の3講座、有料〔講座ごとに受講料〕。12/1「AIを活用した新たな営業戦略策定」）
- おおいた中小企業支援ポータル（県）https://oita-chusho.jp/ の公募中一覧（2026-11-04）: 上の制度のほか、大分県工業連合会「令和８年度中小製造業向けDX人材育成講座」（無料、第5回 11/20「外観検査業務の自動化、AIの活用」、申込は 8/6〜9/4 で終了）

**相談窓口**: 県 先端技術挑戦課 先端技術・DX推進班（097-506-2892）、DX総合支援窓口（ONE OITA、oita-dx＠oec.co.jp、手続きサポート窓口は大分銀行「ビジカム」）、大分県省力化・生産性向上支援補助金事務局（050-8882-4219）、大分県よろず支援拠点（産業創造機構）、各地の商工会議所・商工会（名前は gov_ai.md の対応表を正とする）

## 大分市（oita-city）

**市独自の制度あり（DX研修が随時。予算残りわずか）**
- 「令和8年度大分市中小企業者経営力強化促進補助金(人材育成応援事業)」（yml: oita-oita-city-jinzai-ikusei）https://www.city.oita.oita.jp/o155/shigotosangyo/kigyoshien/keieiryokukyouka.html （2026-10-28更新「予算が残りわずか」）、募集要領 r8zinzaiyouryou.pdf（DX研修の定義）
- 「【令和8年度】小規模事業者のDXへの対応など販路開拓・業務効率化の取り組みを支援します」（yml: oita-oita-city-shokibo-dx）https://www.city.oita.oita.jp/o154/shigotosangyo/shokogyo/r8syokibo.html （2026-08-20更新）、後期の抽選 https://www.city.oita.oita.jp/o154/shigotosangyo/shokogyo/r8shoukibohojokinchusenn.html （2026-09-04）
- 「令和8年度 大分市中小企業者設備投資補助金」（yml: oita-oita-city-setsubi）https://www.city.oita.oita.jp/o155/shigotosangyo/shokogyo/setsubi2020_2nd.html （2026-08-20更新）
- 「大分市中小企業応援メニュー一覧」2026年度版（令和8年4月）https://www.city.oita.oita.jp/o154/shigotosangyo/kigyoshien/documents/ouenmenyu.pdf （全メニュー。ほかに創業者応援、販路拡大チャレンジ、知的財産権取得・事業承継・BCP策定〔経営力強化促進補助金の他の事業〕、おおいたの幸ブランド化、中心市街地出店など。AI・IT 向けは上の3つ）
- 根拠として見た一覧: 「創業・経営支援」https://www.city.oita.oita.jp/shigotosangyo/kigyoshien/kigyoshien/index.html 、「経営支援（補助金）」https://www.city.oita.oita.jp/shigotosangyo/kigyoshien/kigyoshien/hojokin/index.html 、「設備投資」「セミナー・スキルアップ講習」「事業主・勤労者・求職者」の一覧
- 補助金ではないもの: 産業活性化プラザセミナー「生成AI活用セミナー第2回」（2026-11-01登録）、「大分市ビジネスオンライン講座」（後期募集 2026-10-21）、「イノベーションを活用した実証実験をサポートします」（実証する側の事業者向け）

**相談窓口**: 大分市 創業経営支援課 経営支援担当班（097-537-5875）、商工労政課 商業にぎわい担当班（097-537-7294）、大分市産業活性化プラザ、大分商工会議所・野津原町商工会（gov_ai.md）

## 別府市（beppu）

**市独自の AI・IT 導入・研修の補助は見つからなかった**
- 「中小企業者向け支援」https://www.city.beppu.oita.jp/sangyou/sangyousinkou/sonota/ と「別府市中小企業向け施策一覧」（令和8年度、R8.4.1現在）https://www.city.beppu.oita.jp/doc/sangyou/sangyousinkou/sonota/sesakulist.pdf : 補助は知的財産権取得促進（1/2・20万円）、創業支援（2/3・100万円、5/1〜6/30）、会社設立支援、ソーシャルスタートアップ、新湯治・ウェルネス産業創出支援、事業承継支援、空き店舗等利活用、商店街活性化、竹産業販路拡大（インターネットの活用 2/3・20万円）など。AI・IT 導入・研修の補助はない
- **事業者向けDX相談窓口**（別府市まちなか交流館、毎週日曜、無料・何度でも。PC・スマホ・SNS・キャッシュレスの相談）https://www.city.beppu.oita.jp/sangyou/sangyousinkou/sonota/dxsoudan.html （2026-09-03更新）。補助金ではない
- 「労働就労支援」https://www.city.beppu.oita.jp/sangyou/sangyousinkou/syugyou_sonota/ 、「新湯治・ウェルネス 事業者支援」https://www.city.beppu.oita.jp/sangyou/wellness/sien/ も見た

**相談窓口**: 別府市 産業政策課（0977-21-1132）、別府商工会議所

## 中津市（nakatsu）

**市独自の AI・IT 導入・研修の補助は見つからなかった**
- 「企業支援・創業支援」https://www.city-nakatsu.jp/categories/bunya/sangyokoyo/kigyoshien/ ・「商業・工業」https://www.city-nakatsu.jp/categories/bunya/sangyokoyo/shokogyo/ の記事: 中山間地域創業・事業承継支援、女性創業・起業支援、商店街空き店舗活用、商店街等共同設備、**勤労者資格取得支援事業補助金**（技能検定の受検手数料の2/3・1人1万円・1事業所20万円まで、2027-03-31まで。IT 資格ではなく職業能力開発促進法の技能検定と自動車整備士検定）https://www.city-nakatsu.jp/doc/2026092400083/
- 「人手不足、業務効率化のための省力化投資補助金について」https://www.city-nakatsu.jp/doc/2024092400065/ は国の省力化投資補助金の案内（2024年の内容）で、市の制度ではない

**相談窓口**: 中津市 商工担当課（ページの課名は未確認）、中津商工会議所・中津市しもげ商工会

## 日田市（hita）

**市独自の制度あり（国の助成金への上乗せ。随時）**
- 「中小企業等賃上げ環境整備支援助成金」（yml: oita-hita-chinage）https://www.city.hita.oita.jp/soshiki/31/14307.html （2026-04-10更新）、交付要綱 14971_30498_misc.pdf
- 「生産性向上のための設備投資、販路開拓、IT導入等を応援します！」https://www.city.hita.oita.jp/soshiki/31/2631.html （2025-12-08更新）は国の制度（ものづくり・IT導入・持続化・事業承継）の案内で、市の制度ではない
- 無料ワークショップ「DX-Friday」（日田市ビジネスサポートセンター、毎週金曜、SNS・Canva など）https://www.city.hita.oita.jp/soshiki/31/15813.html （2026-06-02更新）。補助金ではない
- 根拠として見た一覧: 商工労政課 https://www.city.hita.oita.jp/soshiki/31/ 、「中小企業向け支援」https://www.city.hita.oita.jp/life/4/20/78/ （新規創業・事業承継支援、育児休業制度推進、子の看護等休暇制度導入奨励金、融資など）

**相談窓口**: 日田市 商工労政課、日田市ビジネスサポートセンター（0973-28-5520）、日田商工会議所・日田地区商工会

## 佐伯市（saiki）

**市独自の AI・IT 導入・研修の補助は見つからなかった**
- 「商工業」https://www.city.saiki.oita.jp/list00365.html 、「企業支援・企業誘致」list00366、「就職・労働・雇用」list05220、「創業支援」list05478 の記事: 中小企業向け制度資金、事業承継、創業等支援事業補助金（創業向け）、よろず支援拠点、コワーキングスペース
- 市議会資料「補助交付金一覧表（令和８年度当初予算〔案〕の概要）」https://www.city.saiki.oita.jp/gikai/kiji00311305/3_11305_49601_up_gd4yco5j.pdf の商工振興課の補助: 商工会議所・商工会への補助、創業支援、地域商業維持支援、利子補給、企業立地助成金など。DX・IT・研修の事業者向け補助はない
- 補助金ではないもの: 県の「Instagram×生成AI活用スクール」の佐伯地区（佐伯市保健福祉総合センター和楽）

**相談窓口**: 佐伯市 商工振興課（0972-22-4597〔企業誘致係の資料の番号〕）、佐伯商工会議所・佐伯市番匠商工会・佐伯市あまべ商工会

## 臼杵市（usuki）

**市独自の制度あり（今年度は終了）**
- 「令和8年度 臼杵市産業・雇用促進事業補助金」（yml: oita-usuki-sangyo-koyo）https://www.city.usuki.oita.jp/docs/2022032200010/ （WebFetch。6/10で終了）
- 「宿泊事業者向けシステム改修・DX補助金のご案内」https://www.city.usuki.oita.jp/article/2026090800038/ （公開2026-09-09）は**県の制度**（宿泊事業者ＤＸ推進事業費補助金・宿泊税対応システム改修費補助金）の案内。市独自の上乗せの記載はない（gov 担当の「臼杵市の宿泊事業者向け DX 補助金」はこれ）
- 「事業者向け」https://www.city.usuki.oita.jp/categories/jigyosha/ ・「企業支援」https://www.city.usuki.oita.jp/categories/jigyosha/kigyoshien/ の記事（WebFetch）: 創業支援事業補助金、空き店舗活用支援事業補助金、企業立地促進助成金、先端設備等導入計画、融資、「令和８年度 中小企業支援施策ガイドブック」https://www.city.usuki.oita.jp/docs/2025070900027/ （開いていない）
- 市のサイトは curl が接続リセットで、すべて WebFetch で読んだ

**相談窓口**: 臼杵市 産業観光課、臼杵商工会議所・野津町商工会

## 津久見市（tsukumi）

**市独自の制度あり（IT導入も対象、2027/1/29まで受付中）**
- 「津久見市小規模事業者等物価高騰対策環境整備支援事業補助金」（yml: oita-tsukumi-shokibo）https://www.city.tsukumi.oita.jp/soshiki/6/20467.html （2026-05-01更新）、要綱 https://www.city.tsukumi.oita.jp/uploaded/attachment/17922.pdf （開いていない）
- 根拠として見た一覧: 商工観光・定住推進課 https://www.city.tsukumi.oita.jp/soshiki/6/ 、「商工業」https://www.city.tsukumi.oita.jp/life/2/17/76/ 、「企業支援・誘致・広告」/life/2/17/79/ （創業支援事業補助金、企業立地促進助成、先端設備等導入計画、融資の利子補給〔受付終了〕）

**相談窓口**: 津久見市 商工観光・定住推進課（市役所2階）、津久見商工会議所（この補助金の事業計画書の相談支援先）

## 竹田市（taketa）

**市独自の AI・IT 導入・研修の補助は見つからなかった**
- 「産業・事業者向け情報」https://www.city.taketa.oita.jp/sangyo_jigyosha/index.html 、「中小企業向け支援」/sangyo_jigyosha/kigyo/ （3件: 事業承継支援事業補助金〔令和8年度創設、9/30まで〕、事業承継の出張相談会、「賃上げに関する事業者支援制度について」〔国の制度の案内〕）、「就労支援」/sangyo_jigyosha/syuro/ （外国人労働者等就業環境等整備促進補助金〔県〕、奨学金返還支援）

**相談窓口**: 竹田市 商工振興課（0974-63-1111 内線237・238）、竹田商工会議所・九州アルプス商工会

## 豊後高田市（bungotakada）

**市独自の制度あり（今年度は終了）**
- 「豊後高田市小規模事業者等物価高騰支援事業補助金」（yml: oita-bungotakada-shokibo）https://www.city.bungotakada.oita.jp/soshiki/14/41466.html （9/14 予算到達で終了）
- 商工観光課の記事一覧 https://www.city.bungotakada.oita.jp/soshiki/14/ : インターンシップ支援、起業チャレンジ（ウェルカム・若者）、事業承継等支援、若年者就職支援など。県・大分銀行に委託した「中小事業者向けセミナー」（ICT・DX、クラウド選定術など、無料）https://www.city.bungotakada.oita.jp/soshiki/14/40883.html は補助金ではない

**相談窓口**: 豊後高田市 商工観光課、豊後高田商工会議所・西国東商工会

## 杵築市（kitsuki）

**市独自の AI・IT 導入・研修の補助は見つからなかった**
- 「産業振興」https://www.city.kitsuki.lg.jp/sangyobijinesu/sangyoushinkou/index.html 、「補助金・助成金一覧」/sangyoushinkou/3/index.html （企業誘致促進補助金、中小企業振興資金、県の外国人労働者等就業環境等整備促進補助金）、「企業（中小企業等）向け支援情報」/sangyoushinkou/6775.html （おおいた中小企業支援ポータル、産業雇用安定センター、杵築市求人活動支援事業補助金）、きつき特産品開発支援事業

**相談窓口**: 杵築市 商工観光課（ページのリンク先の課名 syoukou_kankou）、杵築市商工会

## 宇佐市（usa）

**市独自の AI・IT 導入・研修の補助は見つからなかった**
- 「補助制度」の商工観光 https://www.city.usa.oita.jp/sougo/hozyo/syoukoukankou/index.html （9件: 利子補助、創業者の利子・保証料、先端設備等導入計画、中小企業振興資金、企業誘致の優遇、高校生等地元就職応援、出店の家賃補助、終了した宿泊施設感染予防・ツアー造成）、「事業者の方へ」https://www.city.usa.oita.jp/sougo/jigyosha/index.html
- 補助金ではないもの: 県の「Instagram×生成AI活用スクール」の宇佐地区

**相談窓口**: 宇佐市 商工観光課（課名はページの分類名による）、宇佐商工会議所・宇佐両院商工会

## 豊後大野市（bungoono）

**市独自の制度あり（今年度は終了。導入例に AI検査装置）**
- 「中小企業者生産性向上設備等導入補助金の募集について」（yml: oita-bungoono-seisansei）https://www.bungo-ohno.jp/article/2026020500038/ 、実績報告等 https://www.bungo-ohno.jp/article/2026081200038/
- 「商工・労働・消費者行政」https://www.bungo-ohno.jp/categories/bunyabetsu/syoukou_roudou/ の「創業・中小企業支援」: 特定創業支援等事業、先端設備等導入計画、中小企業振興資金、マル経融資の利子補給

**相談窓口**: 豊後大野市 商工観光課 経済振興係、豊後大野市商工会

## 由布市（yufu）

**市独自の制度あり（研修は随時。DX の経営力強化は予算到達で終了）**
- 「由布市中小企業等経営力強化支援事業について」（yml: oita-yufu-keieiryoku）https://www.city.yufu.oita.jp/article_82227
- 「魅力ある職場づくり支援事業補助金」（yml: oita-yufu-shokuba）https://www.city.yufu.oita.jp/kurashi/syoukougyo/syoukougyo_cate_2/syoukouroudou/jinnzaikakuhonadoshiennjigyouhojokin
- 「事業者の皆さまへ」https://www.city.yufu.oita.jp/biz 、「商工労働」https://www.city.yufu.oita.jp/article_link/syoukouroudou の記事: 創業支援事業補助金（追加募集2回目）、異業種交流グループ活動支援、店舗等整備改善融資の利子補給、ゆふマッチボックス、国の事業再構築補助金・生産性革命補助金の案内

**相談窓口**: 由布市 商工観光課（本庁舎新館2階）、由布市商工会（庄内本所 097-582-0094・挾間支所 097-583-0235・湯布院支所 0977-84-2445）

## 国東市（kunisaki）

**市独自の AI・IT 導入・研修の補助は見つからなかった**
- 観光・地域産業創造課 https://www.city.kunisaki.oita.jp/soshiki/shinko/ と「企業・雇用・分譲」https://www.city.kunisaki.oita.jp/site/shinko/ の記事: 創業支援公募補助金、外国人材育成支援補助金、中小企業設備投資利子補給等補助金、サテライトオフィス等誘致促進補助金、商品開発・改良支援補助金、若者定着奨学金返還支援
- **「くにさきNEXT経営塾」**（令和8年度 国東市プロフェッショナル人材を活用した伴走支援事業。テーマの1つが「AI・デジタル活用による生産性・組織力向上」、2026年9月〜2027年1月の全3回、無料、15社程度）https://www.city.kunisaki.oita.jp/soshiki/shinko/kunisaki-business-seminar.html （2026-07-06更新）。補助金ではない

**相談窓口**: 国東市 観光・地域産業創造課、国東市商工会

---

## 事例の手がかり（cases 担当へ）

社名の扱い・他県で使ったかの確認は事例の担当の判断。`grep -rn "<社名>" articles/ data/area/` は事例担当で。

- **県 先端技術挑戦プロジェクト産学連携創出支援事業の採択結果**: 令和8年度 https://www.pref.oita.jp/site/sme/2026-sangakurenkei.html 、令和7年度 https://www.pref.oita.jp/site/sme/senpurohozyokin2025.html 、令和6年度 /site/sme/2024-sangakurenkei.html （いずれも開いていない。テーマ「ロボティクス・ＡＩ」の採択があれば県内企業×大学の AI 事例）。過去の「大分県IoT推進ラボ認定一覧」https://www.pref.oita.jp/site/sme/heisei29-ninteikekka.html も
- **県「R7年度デジタルスキル向上支援事業事例集」** https://www.pref.oita.jp/site/tyusyodx/dezisuki-zirei-r7.html （開いていない。「クラウドサービス導入等による業務デジタル化支援」の一覧の唯一の記事）
- **県「先端技術研究会」の開催レポート**（令和7年度第1〜5回、令和8年度第1回）https://www.pref.oita.jp/site/sme/sentan-kenkyukai20261.html ほか（開いていない）
- **ONE OITA 経営バディ育成プログラム 成果発表会** https://www.pref.oita.jp/site/tyusyodx/oneoita2025seikahoukoku.html （先端技術挑戦課の記事一覧にある。開いていない。cases.md の「27人分の支援事例」の手がかり）
- **大分市「イノベーションを活用した実証実験プロジェクトを紹介します！」** https://www.city.oita.oita.jp/o155/trial/innovation_introduction.html （2026-10-20登録、開いていない）
- **県 宿泊事業者ＤＸ推進補助金・宿泊業経営力強化加速化補助金**: ツーリズムおおいたは「採択された取組については、概要を…ホームページ等で」公表すると公募要領に書く（今年度分はまだ）
- **大分県経営革新承認企業紹介ページ** https://www.pref.oita.jp/soshiki/14040/keieikakusinnjireashuu06.html （開いていない）

## 取れなかった項目・注意点

- WebSearch は担当全体で5回（上限18回）。県・市のページは curl で開き（同じサイトは間隔を空けた）、臼杵市は curl が接続リセットのため WebFetch で読んだ。大分市・日田市でも一部 curl が接続リセット・タイムアウトになり、間隔を空けて開き直した。ヘッダーの付け替えはしていない。PDF は scratchpad に保存して pdftotext で読んだ（九重町の PDF は画像のため Read で目視）
- **ONE OITA の専用サイト**（one-oita.jp/dx-2026）は JavaScript で本文が取れず、DX総合支援事業の相談の費用（無料か）・受付の締切・デジタルツール導入補助金の申請期限は確かめていない（仕様書の「補助事業は2027年1月末までに完了の想定」だけ）
- **デジタルものづくり補助・スマートものづくり補助**: 過年度の値は WebSearch の要約で、県の PDF は 404。令和8年度は「県の公式で見つからなかった」で、制度がないと断定していない（工業振興課 097-506-3267 に確かめる）
- **県の上乗せ補助金**: 省力化投資の上限は従業員数・区分で異なる（yml の max_yen は最大の750万円）。addon の ratio（1/6）は通常・国1/2の場合で、大幅な賃上げ（1/4）や小規模事業者2/3の場合は合わない
- **「観光関連産業の業務効率化を支援します！（〆切10/31）」**（県 商業・サービス業振興課）はページが 404 で、年度・内容を確かめられなかった
- **大分市 設備投資補助金**: ページの「令和8年3月31日までに補助対象経費が支払われるもの」は誤記の可能性があるが、確かめていない
- **由布市**: 経営力強化支援事業の「DXを用いた取組」の定義・対象経費、受付終了日は商工会扱いで確かめていない
- **日田市**: 賃上げ環境整備支援助成金の対象に国のデジタル化・AI導入補助金が入るか（「市長が認める」助成金）は確かめていない
- **臼杵市**: 産業・雇用促進事業補助金の人件費の対象期間（WebFetch の要約で「令和７年１２月３１日」）は要約の値で、要綱は見ていない。「中小企業支援施策ガイドブック」は開いていない
- **中津市・宇佐市・杵築市**: 商工担当課の正式名は確かめていない（ページの分類名・リンクの名前で書いた）
- 商工会議所・商工会の独自の補助金は確かめていない。名前は gov_ai.md の対応表を正とする
- 振興局の区分・自治体コードは照合していない（stats 担当を正とする）
