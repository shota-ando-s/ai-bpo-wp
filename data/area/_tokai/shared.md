# 静岡・愛知・三重・京都・兵庫の同時作成の共有メモ（2026-11-11）

静岡・愛知・三重・京都の地域ページを、別々のセッションで同時に作るための共有メモ。書き足したらすぐ push する（`git pull --rebase origin main` のあと。衝突したら両方の行を残す）。

- 静岡県は**関東経済産業局**の管内（長野・山梨・新潟・北関東3県と同じ。北関東の共有メモは `data/area/_batch5/shared.md`）
- 愛知県・三重県は**中部経済産業局**の管内（岐阜・富山・石川と同じ。`data/area/gifu/` に資料がある）
- 京都府・兵庫県は**近畿経済産業局**の管内（福井・奈良・和歌山・滋賀と同じ。近畿の共有メモは `data/area/_kinki/shared.md`）

## 試算の時間の割り当て

月の削減時間（0.25時間刻み）×4 を4で割った余り（＝0.25時間単位の端数）で、府県ごとに使う時間を分ける。既存の全県の記事・`data/area/*/_calc.py` の PLAN（北海道など作成中の県は push されていれば）とは `_calc.py` で照合する。金額が重なったら、先に PLAN を push した府県を優先する。

| 余り | 時間の端数 | 府県 |
|---|---|---|
| 0 | ちょうど（.00） | 静岡県 |
| 1 | .25 | 愛知県 |
| 2 | .50 | 三重県 |
| 3 | .75 | 京都府 |

兵庫県（2026-11-11 に追加）は端数を限らない。上の4府県の PLAN（push されていれば）と既存の全県と照合し、重なったら**兵庫側が直す**（あとから始めたため）。

## 管轄ごとの資料

調べた資料を書き足す（資料名・URL・確かめた日・どの府県の値があるか・書いた府県）。

| 資料 | URL | 確かめた日 | 府県の値 | 書いた府県 |
|---|---|---|---|---|
| 中部経済産業局のサイト（一覧・事例・セミナーのチラシ） | https://www.chubu.meti.go.jp/ | 2026-11-11 | 403 で開けない（クラウド）。管轄は農水省の経済産業局の窓口のページ（data/area/gifu/gov_ai.md） | 愛知 |
| NAGOYA DX アワード2024 | （愛知の cases.md） | 2026-11-11 | 愛知・岐阜・三重の会社（三重電子・北勢ダイキャスト工業など）。受賞者インタビューPDFは文字が取れない | 愛知 |
| 東海農政局 スマート農業フォーラム2024 成果報告 | （愛知の cases.md） | 2026-11-11 | 三重（熊野）と岐阜だけ、愛知はない | 愛知 |
| 国のデジタル化・AI導入補助金 7次締切 | https://it-shien.smrj.go.jp/schedule/ | 2026-11-11 | 2026-12-01（火）17:00、交付決定 2027-01-19 予定 | 愛知 |
| TDB 四日市支店の三重県版（後継者不在率・社長年齢・休廃業・人手不足・生成AI の5テーマ） | `https://www.tdb.co.jp/report/{economic,industry}/YYYYMMDD-<テーマ>-mie/`（詳細は data/area/mie/stats_labor.md） | 2026-11-11 | 三重（愛知・静岡も同じ URL の形で県版を試す価値あり） | 三重 |
| 中部経済産業局のサイト（chubu.meti.go.jp） | 中部DX推進コミュニティ 企業の取組事例ほか | 2026-11-11（curl・WebFetch とも 403、Internet Archive も開けず） | 未確認 | 三重 |

## 事例の割り当て

4府県の間で同じ事例を使いそうなら、先にここに書いて push する。先に書いた府県が使う。

| 事例 | 使う府県・市町村 | 書いた日 |
|---|---|---|
| 三重県環境保全事業団（みえDXトライアルサポート事例集） | 三重県 | 2026-11-11 |

## slug

他県とぶつかりそうな slug と扱い。

| slug | 府県・市町村 | 扱い |
|---|---|---|
| tsushima-city | 愛知県津島市 | 長崎県対馬市が `tsushima`。投稿後に別ページか確かめる（area-todo） |
| konan-city | 愛知県江南市 | 高知県香南市 `konan`・滋賀県湖南市 `konan-shiga` |
| tokai-city | 愛知県東海市 | 茨城県東海村が `tokai` |
| takahama-city | 愛知県高浜市 | 福井県高浜町が `takahama` |
| miyoshi-city | 愛知県みよし市 | 徳島県三好市・広島県三次市が `miyoshi` |
| ama-city | 愛知県あま市 | 島根県海士町が `ama` |
| mihama-town-aichi | 愛知県知多郡美浜町 | 福井県美浜町 `mihama`・和歌山県美浜町 `mihama-town`。**三重県の御浜町（みはま）は `mihama` 系を避けて別の形に**（例 `mihama-town-mie`） |
| nagoya | 愛知県名古屋市 | 政令指定都市は1ページ（区のページは作らない） |
| shizuoka-city | 静岡県静岡市 | 県ページ `shizuoka` と分けた（秋田市 `akita-city` と同じ）（静岡） |
| oyama-town | 静岡県駿東郡小山町 | `oyama` は栃木県小山市が使用済み（静岡） |
| mori-town-shizuoka | 静岡県周智郡森町 | `mori` は北海道森町（段階2の案）（静岡） |
| shimizu-town-shizuoka | 静岡県駿東郡清水町 | `shimizu` は北海道清水町（段階2の案）（静岡） |
| mishima / yoshida / ito / izu / fuji | 静岡県三島市・吉田町・伊東市・伊豆市・富士市 | 既存と重ならない（福島県三島町は `mishima-town`）（静岡） |
| asahi-town | 三重県朝日町 | 富山・山形と同じ slug（親ページが違う。area-todo の朝日町の記録どおり）。三重が使う |
| meiwa | 三重県明和町 | 群馬県明和町と同じ slug（親が違う）。三重が使う |
| kihoku | 三重県紀北町 | 愛媛県鬼北町と同じ slug（親が違う）。三重が使う |
| kumano-city | 三重県熊野市 | 広島県熊野町が `kumano` |
| mihama-town-mie | 三重県御浜町 | 福井 `mihama`・和歌山 `mihama-town` |
| kawagoe-town | 三重県川越町 | 埼玉県川越市を見越して |
| kobe | 兵庫県神戸市 | 政令指定都市は1ページ（区のページは作らない）（兵庫） |
| ashiya-city / toyooka-city / miki-city / kawanishi-city / ono-city / tatsuno-city | 兵庫県芦屋市・豊岡市・三木市・川西市・小野市・たつの市 | 福岡県芦屋町 `ashiya`・長野県豊丘村 `toyooka`・香川県三木町 `miki`・山形/奈良の川西町 `kawanishi-town`・福井県大野市 `ono`・長野県辰野町 `tatsuno` と分けた（兵庫） |
| inami-town-hyogo / kami-town-hyogo | 兵庫県稲美町・香美町 | 和歌山県印南町 `inami`、高知県香美市・宮城県加美町 `kami` と分けた（兵庫） |
| taishi / taka / harima / ichikawa / kamikawa / fukusaki / kamigori / sayo / shinonsen / inagawa | 兵庫県の町 | 既存と重ならない（2026-11-11）。**大阪府太子町・千葉県市川市・北海道上川町（段階2）・埼玉県神川町を作るときは別の形に**（兵庫） |
| tamba / tambasasayama | 兵庫県丹波市・丹波篠山市 | **京都府の京丹波町は `tamba` 系を避けて** `kyotamba` などに（兵庫） |
| kyoto / kyoto-city | 京都府 / 京都市 | 府ページは `kyoto`、京都市は `kyoto-city`（政令指定都市は1ページ。区のページは作らない）。府内26市町村の slug は data/area/kyoto/_brief.md。既存1,170本と衝突なし（京都） |
| yawata / kyotanabe / kyotamba | 京都府八幡市・京田辺市・京丹波町 | 愛媛県八幡浜市 `yawatahama`・和歌山県田辺市・兵庫県丹波市と別。**兵庫県の丹波市・丹波篠山市は `kyotamba` を避ける**（京都） |
