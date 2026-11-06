# 北海道・北関東3県・沖縄の同時作成の共有メモ（2026-11-05）

北海道・茨城・栃木・群馬・沖縄の地域ページを、別々のセッションで同時に作るための共有メモ。書き足したらすぐ push する（`git pull --rebase origin main` のあと。衝突したら両方の行を残す）。

## 試算の時間の割り当て

月の削減時間（0.25時間刻み）×4 を5で割った余りで、県ごとに使う時間を分ける。既存の全県の記事・`data/area/*/_calc.py` の PLAN とは、これまでどおり `_calc.py` で照合する。金額が重なったら、先に PLAN を push した県を優先する。

| 余り | 県 |
|---|---|
| 0 | 北海道 |
| 1 | 茨城県 |
| 2 | 栃木県 |
| 3 | 群馬県 |
| 4 | 沖縄県 |

## 関東経済産業局の資料（北関東3県で共有）

調べた資料を書き足す（資料名・URL・確かめた日・どの県の値があるか・書いた県）。長野・山梨・新潟の `data/area/*/` に、関東経済産業局の資料がすでにある。

| 資料 | URL | 確かめた日 | 県の値 | 書いた県 |
|---|---|---|---|---|
| e-Stat 令和7年国勢調査 第3-3表（県ごと） | statInfId 茨城 000040517850・栃木 000040517851・群馬 000040517852 | 2026-11-06 | 各県 | 栃木 |
| 令和3年経済センサス 第14表(2)（茨城〜神奈川） | statInfId 000040067897 | 2026-11-06 | 茨城・栃木・群馬ほか | 栃木 |
| TDB のレポート検索（地域=関東。curl は --compressed が要る） | https://www.tdb.co.jp/report/ | 2026-11-06 | 宇都宮支店の栃木県版は5テーマとも（後継者・社長年齢・人手不足・休廃業・生成AI）。茨城・群馬版の URL も stats.md の末尾にある（栃木の担当は開いていない） | 栃木 |
| 関東経済産業局（kanto.meti.go.jp） | — | 2026-11-06 | クラウドから 403。Internet Archive も遮断 | 栃木 |
| e-Stat 令和7年国調 第3-3表（不詳補完値）の県別 statInfId | 茨城 000040517850（開いて確認）。栃木 000040517851・群馬 000040517852・北海道 000040517843 は県コードの差で推した値（未確認） | 2026-11-06 | 県・市町村 | 茨城 |
| e-Stat 令和3年経済センサス 第14表 関東のファイル（b1_014_2、茨城〜神奈川） | statInfId 000040067897 | 2026-11-06 | 市町村別 | 茨城 |
| TDB 関東の地域で絞ったレポート一覧 | https://www.tdb.co.jp/report/search/?area=%E9%96%A2%E6%9D%B1&page=1 〜 page=10（2026年6月以降。前は URL の日付を1日ずつ試す）。茨城は水戸支店の県版が5テーマともあった | 2026-11-06 | 県版 | 茨城 |
| 農水省 都道府県の農業の概要 | todouhuken_gaiyou2026-08.pdf（ファイル名の末尾が県コード） | 2026-11-06 | 県 | 茨城 |
| 消防庁 令和8年の災害情報一覧 | https://www.fdma.go.jp/disaster/info/2026/ （8/23 茨城県南部の地震は埼玉・千葉・神奈川でも負傷者。茨城は軽傷1・住家被害なし） | 2026-11-06 | 県別 | 茨城 |

## 事例の割り当て

5県の間で同じ事例を使いそうなら、先にここに書いて push する。先に書いた県が使う。

| 事例 | 使う県・市町村 | 書いた日 |
|---|---|---|

## slug

他県とぶつかりそうな slug と扱い。

| slug | 県・市町村 | 扱い |
|---|---|---|
| takayama-village-gunma | 群馬県吾妻郡高山村 | 長野県高山村 `takayama-village`・岐阜県高山市 `takayama` があるので県名を付けた（群馬） |
| showa-village-gunma | 群馬県利根郡昭和村 | 福島県昭和村 `showa-village`・山梨県昭和町 `showa` があるので県名を付けた（群馬） |
| nanmoku | 群馬県甘楽郡南牧村（なんもく） | 長野県南牧村は `minamimaki` で重ならない（群馬） |
| ueno-village / meiwa / chiyoda / oizumi / ota / midori / itakura / tomioka | 群馬県の村・町・市 | 既存の slug と重ならない（福島県富岡町は `tomioka-town`）。茨城・栃木で同じ slug を使う予定があれば知らせてください（群馬） |
| koga | 茨城県古河市（福岡県古賀市と同じ） | 茨城: 同じ slug のまま（親ページが違う）。投稿後に別ページか確かめる |
| kashima | 茨城県鹿嶋市（佐賀県鹿島市と同じ。熊本県嘉島町は kashima-town） | 茨城: 同じ slug のまま |
| naka | 茨城県那珂市（徳島県那賀町と同じ） | 茨城: 同じ slug のまま。栃木県那珂川町は nakagawa 以外で（福岡県那珂川市が nakagawa） |
| sakai-town | 茨城県境町（福井県坂井市 sakai） | 茨城: -town を付ける |
| ibaraki-town | 茨城県茨城町（県と同じ名前） | 茨城: 岩手町 iwate-town と同じ形 |
| tokai / miho / kawachi / yachiyo / goka / tone | 茨城県の東海村・美浦村・河内町・八千代町・五霞町・利根町 | 茨城が使う（既存と重ならない） |
| okinawa-city | 沖縄県沖縄市 | 県ページ `okinawa` と分ける（青森市 `aomori-city` と同じ形） |
| nishihara-town | 沖縄県中頭郡西原町 | 熊本県西原村が `nishihara`。親ページが違うが、町は `-town` を付けて分ける |
| higashi-village | 沖縄県国頭郡東村 | `higashi` だけだと方角の語と紛らわしいので `-village` |
| 沖縄県の41市町村（2026-11-05） | naha ginowan ishigaki urasoe nago itoman okinawa-city tomigusuku uruma miyakojima nanjo / motobu kin kadena chatan nishihara-town yonabaru haebaru kumejima yaese taketomi yonaguni / kunigami ogimi higashi-village nakijin onna ginoza ie yomitan kitanakagusuku nakagusuku tokashiki zamami aguni tonaki minamidaito kitadaito iheya izena tarama | 北海道・北関東3県で同じ slug を使う市町村があれば、この行を見て `-<県>` を付けるか決める |
| tochigi-city | 栃木県栃木市 | 県と同じ名前（青森市・秋田市と同じ形） |
| nakagawa-town | 栃木県那珂川町 | `nakagawa` は長野県中川村・福岡県那珂川市が使用済み。茨城県の那珂市（naka）・那珂川とも別 |
| sakura | 栃木県さくら市 | 既存のページにない。千葉県佐倉市と同じ読み |
| kitahiroshima-city | 北海道北広島市 | 広島県北広島町 `kitahiroshima` と分けた（北海道） |
| date-city | 北海道伊達市（段階2） | 福島県伊達市 `date` と分けた（北海道） |
| hokuto-city | 北海道北斗市（段階2） | 山梨県北杜市 `hokuto` と分けた（北海道） |
| fukushima-town / nakagawa-town-hokkaido / hidaka-town / ikeda-town-hokkaido | 北海道福島町・中川町・日高町・池田町（段階2） | 福島県 `fukushima`・長野県中川村/福岡県那珂川市 `nakagawa`・高知県日高村 `hidaka`・福井/岐阜/長野の池田町・栃木県那珂川町 `nakagawa-town` と分けた（北海道） |
| kushiro-city / kushiro-town、shibetsu-city / shibetsu-town、esashi-hiyama / esashi-soya | 北海道の同じ読みの市町（段階2） | 道内で分けた。**ほかの4県で同じ読みの市町村があれば `-city`・`-town` を付けて分けてください**（北海道） |
| sapporo / ebetsu / chitose / eniwa / ishikari / tobetsu / shinshinotsu | 北海道石狩振興局（段階1） | 既存と重ならない（北海道） |
