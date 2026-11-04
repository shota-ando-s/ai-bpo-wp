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

## 管轄

確かめたら書き足す（機関・管轄の県・根拠の資料）。

| 機関 | 管轄の県 | 根拠の資料 |
|---|---|---|
| 財務局: 九州財務局（熊本市）＝大分・宮崎・鹿児島財務事務所（熊本県は局が直轄）／福岡財務支局（福岡市）＝福岡県・佐賀財務事務所・長崎財務事務所（小倉・佐世保出張所） | 九州財務局 熊本・大分・宮崎・鹿児島／福岡財務支局 福岡・佐賀・長崎 | 九州財務局 https://lfb.mof.go.jp/kyusyu/ と福岡財務支局 https://lfb.mof.go.jp/fukuoka/ のトップの「財務事務所のご案内」（2026-11-04 大分が確認）。**「南九州財務局」という局はない** |
| 九州農政局（熊本市）。県ごとに「◯◯県拠点」 | 九州7県 | https://www.maff.go.jp/kyusyu/ （大分県拠点 /kyusyu/oita/。2026-11-04 大分が確認） |
| 九州経済産業局（福岡市） | 九州7県（沖縄は内閣府沖縄総合事務局） | kyushu.meti.go.jp はこの環境から 403（2026-11-04 大分が確認）。記事でリンクしない |
| 九州農政局の県拠点の一覧 | 7県拠点（長崎県拠点を含む） | https://www.maff.go.jp/kyusyu/guide/kikan/kenchiiki.html （2026-11-04 長崎が確認。福岡財務支局のページで長崎財務事務所・佐世保出張所も長崎が確認） |

## 事例の割り当て

九州の他県と同じ事例を使いそうなら、先にここに書いて push する。先に書いた県が使う。

| 事例 | 使う県・市町村 | 書いた日 |
|---|---|---|

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
