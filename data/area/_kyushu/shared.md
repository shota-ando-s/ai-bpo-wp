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
