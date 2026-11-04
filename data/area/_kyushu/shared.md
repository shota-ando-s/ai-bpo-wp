# 九州7県の共有メモ

九州7県（福岡・佐賀・長崎・熊本・大分・宮崎・鹿児島）の地域ページを、別々のセッションで同時に作るための共有メモ（2026-11-04）。書き足したらすぐ push する（`git pull --rebase origin main` のあと。衝突したら両方の行を残す）。

## 試算の時間の割り当て

月の削減時間（0.25時間刻み）×4 を7で割った余りで、県ごとに使う時間を分ける。金額が重なったら、先に PLAN を push した県を優先する。

| 余り | 県 |
|---|---|
| 0 | 福岡県 |
| 1 | 佐賀県 |
| 2 | 長崎県 |
| 3 | 熊本県 |
| 4 | 大分県 |
| 5 | 宮崎県 |
| 6 | 鹿児島県 |

## 九州全体の資料

調べた資料を書き足す（資料名・URL・確かめた日・どの県の値があるか・書いた県）。

| 資料 | URL | 確かめた日 | 県の値 | 書いた県 |
|---|---|---|---|---|
| よろず支援拠点全国本部の拠点一覧（九州7県の設置機関と電話） | https://yorozu.smrj.go.jp/base/ | 2026-11-04 | 九州7県 | 大分 |
| 日商の商工会議所一覧 | https://ab.jcci.or.jp/cci-list/ | 2026-11-04 | 九州7県 | 大分 |
| 全国商工会連合会の名簿（shoko_search.php に kencd[]=県コードで POST、Cookie を付けて search.php の startNo でページ送り） | https://www.shokokai.or.jp/ | 2026-11-04 | 九州7県 | 大分 |
| 令和7年国勢調査 不詳補完値 第3-3表（e-Stat） | statInfId 福岡 000040517882・佐賀 …883・長崎 …884・熊本 …885・大分 …886（宮崎 …887・鹿児島 …888 は未確認） | 2026-11-04 | 各県 | 長崎 |
| 令和3年経済センサス‐活動調査 第14表（福岡県〜沖縄県） | e-Stat statInfId=000040067901 | 2026-11-04 | 九州7県 | 長崎 |
| 長崎労働局 雇用失業情勢 令和8年9月分 p.9（九州7県の有効求人倍率・季調） | https://jsite.mhlw.go.jp/nagasaki-roudoukyoku/content/contents/koyo-tokei-1-26103001.pdf | 2026-11-04 | 九州7県 | 長崎 |
| TDB 全国「後継者不在率」2025 の都道府県表 | https://www.tdb.co.jp/report/economic/20251121-successor25y/ | 2026-11-04 | 九州7県 | 長崎 |
| TDB 全国「社長年齢」2025 の都道府県表 | https://www.tdb.co.jp/report/economic/20260216-presidentage2025/ | 2026-11-04 | 九州7県 | 長崎 |
| TDB 全国「休廃業・解散」2025（2026-01-09 の PDF）の都道府県表 | TDB のレポート（2026-01-09） | 2026-11-04 | 九州7県 | 長崎 |
| TDB 福岡県版「後継者不在率」 | https://www.tdb.co.jp/report/economic/20251209-successor25y-fukuoka/ | 2026-11-04 | 福岡 | 長崎 |
| TDB の九州版（-kyushu など）は生成AI・人手不足・後継者不在率で見つからなかった | — | 2026-11-04 | — | 長崎 |
| 有人国境離島法 別表（特定有人国境離島地域。長崎3地域・鹿児島5地域） | https://laws.e-gov.go.jp/api/1/lawdata/428AC1000000033 | 2026-11-04 | 長崎・鹿児島 | 長崎 |
| 九州財務局「地域におけるAI活用を巡る現状」（令和8年1月。管内100社ヒアリング、AI活用72.0%） | https://lfb.mof.go.jp/kyusyu/content/kyusyu_kaigi_2601.pdf | 2026-11-04 | 熊本・大分・宮崎・鹿児島の計。県別の値はない | 大分 |
| 大分労働局「大分県の雇用情勢（令和8年9月分）」p.7（九州8県の有効求人倍率、季節調整値） | https://jsite.mhlw.go.jp/oita-roudoukyoku/content/contents/002874828.pdf | 2026-11-04 | 九州8県 | 大分 |
| TDB 大分県版「休廃業・解散」p.7（47都道府県の2021〜2025年の件数） | https://www.tdb.co.jp/report/industry/20260217-closedown25y-oita/ | 2026-11-04 | 47都道府県（九州各県を含む） | 大分 |
| TDB の人手不足・生成AIの九州版・大分県版（2026年） | URL の日付を変えて試し、すべて404 | 2026-11-04 | 見つからない | 大分 |
| TDB福岡支店「九州・沖縄『後継者不在率』動向調査（2025年）」 | https://www.tdb.co.jp/report/economic/20251203-successor25y-kyusyu/ | 2026-11-04 | 九州・沖縄8県の不在率（PDF p.4・p.9）。県別の社数なし | 佐賀 |
| TDB福岡支店「九州・沖縄『社長年齢』分析調査（2025年）」 | https://www.tdb.co.jp/report/economic/20260310-presidentage2025-kyusyu/ | 2026-11-04 | 8県の平均年齢と全国順位（p.5・p.6） | 佐賀 |
| TDB福岡支店「九州・沖縄 人手不足に対する企業の動向調査」2026年1月・4月・7月 | …/20260306-laborshortage202601-kyusyu/ ・ …/20260603-laborshortage202604-kyusyu/ ・ …/20260827-laborshortage202607-kyusyu/ | 2026-11-04 | 九州・沖縄全体の値だけ（県別なし） | 佐賀 |
| TDB福岡支店「九州・沖縄 生成AIに関する企業の動向調査（2026年3月）」 | https://www.tdb.co.jp/report/economic/20260528-genai-kyusyu/ | 2026-11-04 | 983社・活用35.9%。県別なし | 佐賀 |
| TDB「全国企業『休廃業・解散』動向調査（2025年）」 | https://www.tdb.co.jp/report/industry/20260109-kyuhaigyo25y/ | 2026-11-04 | 47都道府県の件数（p.8） | 佐賀 |
| 農水省「令和８年版 都道府県の農林水産業の概要」 | https://www.maff.go.jp/j/kanbo/tiho/15sonota/2026PDF/todouhuken_gaiyou2026-41.pdf （末尾40〜47で九州各県） | 2026-11-04 | 県ごと | 佐賀 |
| e-Stat 経済センサス‐活動調査 令和3年 第14表（福岡県～沖縄県） | statInfId=000040067901 | 2026-11-04 | 九州7県・沖縄 | 佐賀 |
| TDB の佐賀県版 | `-saga` の URL を約1,100通り | 2026-11-04 | 佐賀支店の県版は見つからなかった | 佐賀 |
| 宮崎労働局「一般職業紹介状況（令和8年9月分）」別表5（九州7県と沖縄の有効求人倍率、季節調整値） | https://jsite.mhlw.go.jp/miyazaki-roudoukyoku/content/contents/002871435.pdf | 2026-11-04 | 九州7県・沖縄 | 宮崎 |
| e-Stat 令和3年経済センサス‐活動調査 第14表（福岡〜沖縄の8県が1ファイル） | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040067901&fileKind=0 | 2026-11-04 | 九州7県・沖縄 | 宮崎 |
| 経産省 2025年経済構造実態調査 地域別 第1表（都道府県の製造品出荷額） | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040480531&fileKind=0 | 2026-11-04 | 九州7県 | 宮崎 |
| TDB 全国版 休廃業・解散（2026-01-09）p.8 の都道府県表 | （TDB のレポート一覧） | 2026-11-04 | 九州7県 | 宮崎 |
| TDB 鹿児島県版 人手不足（2026年4月調査） | https://www.tdb.co.jp/report/economic/20260717-laborshortage202604-kagoshima/ | 2026-11-04 | 鹿児島（宮崎県版・九州版の人手不足は見つからない） | 宮崎 |
| 九州財務局 大分財務事務所「おおいた活性化フォーラム」（第9回 2026-05-29。県の ONE OITA 事業、信金・商議所・商工会の担当者のAI活用） | https://lfb.mof.go.jp/kyusyu/oita/oita_forum.html | 2026-11-04 | 大分 | 大分 |
| 農林水産技術会議 スマート農業実証プロジェクト R4 パンフレット（4-17 長崎県東彼杵町の茶〔AIではなくドローン空撮の生育予測〕p.199、4-18 大分県国東市の白ねぎ p.200） | https://www.affrc.maff.go.jp/docs/smart_agri_pro/pdf/pamphlet/r4/R4_4-18.pdf | 2026-11-04 | 長崎・大分 | 大分 |
| 九州農政局「九州農政局管内のスマート農業取組事例」（令和8年9月、47事例） | https://www.maff.go.jp/kyusyu/seisan/gizyutu/attach/pdf/smart-24.pdf （一覧 https://www.maff.go.jp/kyusyu/seisan/gizyutu/smart.html 。旧版 smart-17.pdf は404） | 2026-11-04 | 九州7県。AIの語があるのは 長崎県壱岐市 松嶋農場（No.20 ゼロアグリ）、大分県竹田市 古澤畜産（No.36）、鹿児島県肝付町 中野ファーム（No.45）、鹿児島県薩摩郡 永江陽平（No.46）。熊本県の2件はAIの語なし | 熊本 |
| 九州農政局「九州農政局管内の農業支援サービス取組事例」（令和8年9月） | https://www.maff.go.jp/kyusyu/seisan/gizyutu/attach/pdf/smart-25.pdf | 2026-11-04 | AIの語があるのは 宮崎県新富町 AGRIST（No.27）、鹿児島県 ファーマーズサポート（No.29）、長崎県 ルートレック・ネットワークス（No.31）。熊本県のAIの事例なし | 熊本 |
| くまもと産業支援財団のサイト | www.kmt-ia.or.jp | 2026-11-04 | クラウドのセッションから名前解決できない | 熊本 |
| 九州財務局「第6回みやざき活性化フォーラム」結果概要・講演資料2（2023-12-19） | https://lfb.mof.go.jp/kyusyu/content/list/028/miyafo-ramu_kekkagaiyou20231219.pdf ・ https://lfb.mof.go.jp/kyusyu/content/list/028/miyafo-ramu_kouennsiryou_2_20231219.pdf | 2026-11-04 | 宮崎県だけ（県内事業者アンケート 回答474者） | 宮崎 |
| 九州経済産業局「DXクエスト」2024年度 事例 PDF（番号ごと。7.pdf は鹿児島のオービジョン） | https://www.kyushu.meti.go.jp/seisaku/jyoho/jirei/dx_quest/2024/7.pdf | 2026-11-04（403。検索の要約だけ） | 九州各県の会社（番号ごと） | 鹿児島 |
| 九州経済産業局「DX・サイバーセキュリティ対策に取り組む事例」 | https://www.kyushu.meti.go.jp/seisaku/jyoho/jirei/dx/top.html | 2026-11-04（403） | 九州各県 | 鹿児島 |
| 九州経済産業局「社会のデータ・AI等活用事例動画」（2024-05-09） | https://www.kyushu.meti.go.jp/seisaku/jyoho/oshirase/240509_1.html | 2026-11-04（403） | 鹿児島堀口製茶×テラスマイル（検索の要約）ほか | 鹿児島 |
| 農研機構 スマート農業実証プロジェクトの成果 PDF（r2_*） | https://www.naro.go.jp/smart-nogyo/r2/files/r2_5g_H03.pdf （鹿児島県志布志市 鹿児島堀口製茶。AIの葉期判定 巡回21分→11分は試算） | 2026-11-04 | 九州各県の実証が番号で並ぶ | 鹿児島 |
| 九州経済産業局「2025年度マナビDX Quest 地域企業協働プログラム参加企業」 | https://www.kyushu.meti.go.jp/seisaku/jyoho/jirei/dx_quest/2025/260302_1.html | 2026-11-04 | curl・WebFetch とも 403。検索の要約だけで、佐賀はバイオテックス・サンエスライン（未確認）。他県の会社は見られず | 佐賀 |
| 九州経済産業局 事例集・ガイドライン | https://www.kyushu.meti.go.jp/seisaku/jyoho/pamph.html | 2026-11-04 | 403。九州の AI 事例集で佐賀の会社名つきのものは見つからなかった | 佐賀 |
| e-Stat 令和3年経済センサス 第14表(6)「福岡県～沖縄県」 | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040067901&fileKind=0 | 2026-11-04 | 九州7県と沖縄の市町村 | 福岡 |
| e-Stat 令和7年国勢調査 第3-3表（不詳補完値、県別ファイル） | statInfId=000040517842+県コード（福岡 000040517882、佐賀 000040517883） | 2026-11-04 | 県ごと | 福岡 |
| e-Stat 令和2年国勢調査 不詳補完値 第2-7表（2020年の年齢3区分） | statInfId=000040317626 | 2026-11-04 | 全国の全市町村（15〜64歳の2020→2025増減を自分で計算するのに使う） | 福岡 |
| e-Stat 2023年漁業センサス 販売金額1位の漁業種類別経営体数（市区町村・漁業地区） | statInfId=000040252844 | 2026-11-04 | 全国 | 福岡 |
| 経産省 2025年経済構造実態調査 製造業「地域別」第1表 | statInfId=000040480531 | 2026-11-04 | 九州7県の出荷額（福岡1位・大分2位） | 福岡 |
| 内閣府 平成29年7月九州北部豪雨の被害状況・気象庁 令和5年7月10日の大雨（R050710）の PDF | （stats.md の出典） | 2026-11-04 | 福岡県・大分県 | 福岡 |
| BODIK オープンデータ（data.bodik.jp） | https://data.bodik.jp/ | 2026-11-04 | 福岡県の推計人口・農林業センサス・漁業センサス。熊本県・鹿児島県のデータもある | 福岡 |
| TDB福岡支店「九州・沖縄『後継者不在率』動向調査（2025年）」2025-12-03（**URLは `-kyusyu`。`-kyushu` ではない**） | https://www.tdb.co.jp/report/economic/20251203-successor25y-kyusyu/ | 2026-11-04 | 九州・沖縄8県の県別（PDF p.4・p.9）。鹿児島37.6% | 鹿児島 |
| TDB福岡支店「九州・沖縄 人手不足に対する企業の動向調査（2026年7月）」2026-08-27 | https://www.tdb.co.jp/report/economic/20260827-laborshortage202607-kyusyu/ | 2026-11-04 | **県別の値はない**（九州・沖縄計と業種別だけ） | 鹿児島 |
| TDB福岡支店「九州・沖縄 生成AIに関する企業の動向調査（2026年3月）」2026-05-28 | https://www.tdb.co.jp/report/economic/20260528-genai-kyusyu/ | 2026-11-04 | 県別の値は見つからない（九州・沖縄計35.9%、983社）。鹿児島は県版あり | 鹿児島 |
| 令和3年経済センサス 第14表（常用雇用者規模別）九州・沖縄のファイル b1_014_6 | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040067901&fileKind=0 | 2026-11-04 | 福岡〜沖縄の全市区町村 | 鹿児島 |
| 令和7年国勢調査 不詳補完値 第3-3表（県別ファイル。鹿児島 000040517888・宮崎 000040517887） | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040517888&fileKind=0 | 2026-11-04 | 県ごと | 鹿児島 |
| 令和2年国勢調査 不詳補完結果 第1-4表（全市区町村） | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032144437&fileKind=0 | 2026-11-04 | 九州7県の全市町村 | 鹿児島 |
| 農水省「令和８年版 都道府県の農林水産業の概要」（末尾が県コード） | https://www.maff.go.jp/j/kanbo/tiho/15sonota/2026PDF/todouhuken_gaiyou2026-46.pdf | 2026-11-04 | 県ごと（46=鹿児島） | 鹿児島 |
| TDB福岡支店「九州・沖縄『後継者不在率』動向調査（2025年）」2025-12-03 PDF（URLは data/area/kumamoto/stats_labor.md） | https://www.tdb.co.jp/ （PDFのURLは stats_labor.md） | 2026-11-04 | 沖縄を含む8県の値 | 熊本 |
| TDB福岡支店「九州・沖縄『社長年齢』分析調査（2025年）」2026-03-10 PDF | 同上 | 2026-11-04 | 沖縄を含む8県の値 | 熊本 |
| 経済センサス‐活動調査（令和3年）第14表 福岡〜沖縄のファイル | e-Stat statInfId=000040067901 | 2026-11-04 | 九州7県が同じファイル | 熊本 |
| 熊本労働局「最近の雇用失業情勢」p.4 の「九州」の有効求人倍率 1.08倍（2026年9月） | 熊本労働局のサイト（stats_labor.md） | 2026-11-04 | 九州（沖縄を含むかは表に書かれていない） | 熊本 |

## 管轄

確かめたら書き足す（機関・管轄の県・根拠の資料）。

| 機関 | 管轄の県 | 根拠の資料 |
|---|---|---|
| 財務局: 九州財務局（熊本市）＝大分・宮崎・鹿児島財務事務所（熊本県は局が直轄）／福岡財務支局（福岡市）＝福岡県・佐賀財務事務所・長崎財務事務所（小倉・佐世保出張所） | 九州財務局 熊本・大分・宮崎・鹿児島／福岡財務支局 福岡・佐賀・長崎 | 九州財務局 https://lfb.mof.go.jp/kyusyu/ と福岡財務支局 https://lfb.mof.go.jp/fukuoka/ のトップの「財務事務所のご案内」（2026-11-04 大分が確認）。**「南九州財務局」という局はない** |
| 九州農政局（熊本市）。県ごとに「◯◯県拠点」 | 九州7県 | https://www.maff.go.jp/kyusyu/ （大分県拠点 /kyusyu/oita/。2026-11-04 大分が確認） |
| 九州経済産業局（福岡市） | 九州7県（沖縄は内閣府沖縄総合事務局） | kyushu.meti.go.jp はこの環境から 403（2026-11-04 大分が確認）。記事でリンクしない |
| 九州農政局の県拠点の一覧 | 7県拠点（長崎県拠点を含む） | https://www.maff.go.jp/kyusyu/guide/kikan/kenchiiki.html （2026-11-04 長崎が確認。福岡財務支局のページで長崎財務事務所・佐世保出張所も長崎が確認） |
| 九州運輸局（福岡市）。7県の運輸支局＋山口県の下関海事事務所 | 九州7県 | https://wwwtb.mlit.go.jp/kyushu/gyoumu/sikyoku/body.htm （2026-11-04 福岡が確認。福岡運輸支局は東区みなと香椎に移転） |
| 福岡労働局（県単位）。最低賃金 1,114円（2026-10-04 から） | 福岡県 | 福岡労働局の公式（2026-11-04 福岡が確認） |
| 九州経済産業局の管轄の根拠（局のサイトが403のとき） | 九州7県 | 農水省「輸出の相談窓口（経済産業局）」 https://www.maff.go.jp/j/shokusan/export/yusyutsugaido/contact_meti.html （2026-11-04 福岡が確認） |

## 事例の割り当て

九州の他県と同じ事例を使いそうなら、先にここに書いて push する。先に書いた県が使う。

| 事例 | 使う県・市町村 | 書いた日 |
|---|---|---|
| 生成AIの橋梁診断の実証（NTTコムウェア・長崎大学・溝田設計事務所〔福岡県久留米市〕・長崎県建設技術研究センター、長崎県内13橋、約57%削減） | 長崎県（県ページ・大村市） | 2026-11-04 |
| 鹿児島堀口製茶（志布志市、AIの葉期判定・農研機構の実証） | 鹿児島県志布志市 | 2026-11-04 |
| 社会保険労務士法人プロセスコア（デジライズの事例。生成AIでコラム制作「1/4程の作業時間」） | 熊本県 熊本市 | 2026-11-04 |
| 学校法人未来創造学園（デジライズの事例。メール作成約70%減） | 熊本県 熊本市 | 2026-11-04 |
| 税理士法人さくら優和パートナーズ（熊日のスポンサード記事。熊本・福岡・鹿児島に拠点。ChatGPT 研修で労働時間 最大6時間/月減） | 熊本県 熊本市（福岡・鹿児島は使わないでください） | 2026-11-04 |
| 熊本中央病院の Sail AI（ispec のプレスリリース） | 熊本県 熊本市 | 2026-11-04 |

## slug

九州の各県で決めた slug のうち、他県とぶつかりそうなもの。

| slug | 県・市町村 | 扱い |
|---|---|---|
| miyazaki-city | 宮崎県宮崎市（県ページ `/area/miyazaki/` と別） | 青森市 `aomori-city` と同じ形 |
| misato-town-miyazaki | 宮崎県美郷町（東臼杵郡） | 秋田県美郷町 `misato`・宮城県美里町 `misato-town`・島根県美郷町 `misato-town-shimane` と重ならない形。熊本県美里町は別の slug にしてください |
| nichinan | 宮崎県日南市（鳥取県日南町 `nichinan` と同じ） | 親ページが違うので同じ slug のまま（若桜町・大山町と同じ扱い）。投稿後に別ページか確かめる |
| tsuno | 宮崎県都農町（高知県津野町 `tsuno` と同じ） | 同上 |
| kagoshima-city | 鹿児島県鹿児島市 | 県と同じ名前（青森市・岡山市と同じ形） |
| osaki-town | 鹿児島県曽於郡大崎町 | 宮城県大崎市 `osaki` |
| setouchi-town | 鹿児島県大島郡瀬戸内町 | 岡山県瀬戸内市 `setouchi` |
| yamato-village | 鹿児島県大島郡大和村 | 熊本県上益城郡山都町と同じ読み（熊本は `yamato` を使ってよい） |
| toshima-village | 鹿児島県鹿児島郡十島村 | 東京都の利島村・豊島区と同じ読み |
| mishima-village | 鹿児島県鹿児島郡三島村 | 静岡県三島市と同じ読み |
| saga-city | 佐賀県佐賀市 | 県と同じ名前（青森市・岡山市と同じ形） |
| omachi-town | 佐賀県杵島郡大町町 | 長野県大町市 `omachi` |
| shiroishi-town | 佐賀県杵島郡白石町 | 宮城県白石市 `shiroishi` |
| kashima | 佐賀県鹿島市 | 熊本県上益城郡嘉島町と同じ読み（熊本は `kashima-town` などにしてください）。茨城県鹿嶋市は未作成 |
| kohoku | 佐賀県杵島郡江北町 | 既存なし |
| arita / imari / karatsu / tosu / takeo / ureshino / ogi / taku / kanzaki / yoshinogari / kiyama / kamimine / miyaki / genkai / tara | 佐賀県の市町 | 既存なし（佐賀が使う） |
| fukuoka-city | 福岡県福岡市 | 県と同名の市（青森市 aomori-city と同じ形）。福岡県のページは fukuoka |
| kitakyushu | 福岡県北九州市 | 政令市。区のページは作らない |
| okawa | 福岡県大川市 | 高知県大川村と同じ slug（親ページが違う）。投稿後に別ページか確かめる |
| nakagawa | 福岡県那珂川市 | 長野県中川村と同じ slug。投稿後に確かめる |
| miyako | 福岡県みやこ町 | 岩手県宮古市と同じ slug。投稿後に確かめる |
| kawasaki-town | 福岡県川崎町（田川郡） | 宮城県川崎町と同じ slug。投稿後に確かめる |
| 福岡県の60市町村の slug 一覧 | data/area/fukuoka/_brief.md | 九州の他県で同じ slug を使うときは見比べる（例: misato・oguni-town など既存の slug も） |
| oita-city | 大分県大分市（県ページ `/area/oita/` と別） | 青森市 `aomori-city` と同じ形。大分県の18市町村のほかの slug（beppu, nakatsu, hita, saiki, usuki, tsukumi, taketa, bungotakada, kitsuki, usa, bungoono, yufu, kunisaki, hiji, kokonoe, kusu, himeshima）は既存のページと重ならない |
| `kumamoto-city` | 熊本県 熊本市 | 政令指定都市、1ページ（青森市 `aomori-city` の形） |
| `misato-town-kumamoto` | 熊本県 美里町（下益城郡） | 秋田 `misato`・宮城 `misato-town`・島根 `misato-town-shimane`・宮崎 `misato-town-miyazaki` と別 |
| `kashima-town` | 熊本県 嘉島町（上益城郡） | 佐賀県鹿島市 `kashima` と重ならない形（佐賀の依頼どおり） |
| `ozu` / `takamori` | 熊本県 大津町・高森町 | 愛媛県大洲市・長野県高森町と同じ slug（親ページが違う） |
