# 神奈川・埼玉・千葉（と北海道の続き）の同時作成の共有メモ（2026-11-13）

神奈川・埼玉・千葉の地域ページと北海道の続きを、別々のセッションで同時に作るための共有メモ。書き足したらすぐ push する（`git pull --rebase origin main` のあと。衝突したら両方の行を残す）。

- 3県とも**関東経済産業局**の管内（長野・山梨・新潟・北関東3県・静岡と同じ。北関東の共有メモは `data/area/_batch5/shared.md`）。
- 3県には 2026-10-14 のパイロット（首都圏4都県）のデータがある: `data/subsidies/kanagawa.yml`・`saitama.yml`・`chiba.yml`、`areas.yml` の一部の市、`docs/area-local-subsidies.md`・`docs/area-local-data.md`・`docs/area-industry-model.md`、`docs/area-ai-media-brief.md`（企画書。首都圏の位置づけ）。**消さずに、今の形に直して足す**。
- 試算は**他県との重なりを許容**し、同じ県の中だけ時間・金額・規模を重ねない（2026-11-11 ユーザー決定。`docs/area-new-prefecture.md`）。

## 関東経済産業局・首都圏の資料

調べた資料を書き足す（資料名・URL・確かめた日・どの県の値があるか・書いた県）。

| 資料 | URL | 確かめた日 | 県の値 | 書いた県 |
|---|---|---|---|---|
| 埼玉県「中小企業人手不足対応支援事業 事例集」（80本、所在地・従業員数つき）。神奈川・千葉にも同じ形の県の資料がないか探す価値あり | 埼玉県のサイト（data/area/saitama/cases.md に URL） | 2026-11-12 | 埼玉 | 埼玉 |
| 中小機構「省力化ナビ」事例84本（兵庫で使用）。埼玉の行で AI は川島製作所だけ。神奈川・千葉の行は未確認 | data/area/hyogo/ を参照 | 2026-11-12 | 埼玉 | 埼玉 |

## 事例の割り当て

3県の間で同じ事例を使いそうなら、先にここに書いて push する。先に書いた県が使う。

| 事例 | 使う県・市町村 | 書いた日 |
|---|---|---|
| 萩原建設工業（北海道帯広市、AI・RPAで資材管理を自社開発、約240時間→13.36時間）・鹿追町ICT研究会ほかのキャベツのAI収穫機の実証（国の実証、令和2〜3年度） | 北海道（帯広市・鹿追町） | 2026-11-12 |
| meviy（ミスミ）の導入事例（川島製作所〔草加市〕・谷野製作所〔日高市〕など）は似た話になるので、3県で1〜2件にとどめる。埼玉はどちらか1社 | 埼玉 | 2026-11-12 |

## slug

他県とぶつかりそうな slug と扱い。

| slug | 県・市町村 | 扱い |
|---|---|---|
| kamikawa | 北海道上川郡上川町（公開済み `/area/hokkaido/kamikawa/`） | 埼玉県児玉郡神川町は `kamikawa` 以外で（北海道） |
| hidaka-town | 北海道沙流郡日高町（予定） | 高知県日高村が `hidaka` を使用済み。埼玉県日高市は `hidaka` 以外で（北海道） |
| taiki-town-hokkaido・numata-town-hokkaido・shimizu・ikeda-town-hokkaido | 北海道の大樹町・沼田町・清水町（十勝）・池田町（予定） | 三重県大紀町 `taiki`・群馬県沼田市 `numata` があるので県名を付けた。清水町は `shimizu`（静岡県清水町は `shimizu-town-shizuoka`）（北海道） |
| saitama / saitama-city | 埼玉県 / さいたま市 | 県は `saitama`、さいたま市は `saitama-city`（区のページは作らない） |
| misato-city | 埼玉県三郷市 | 秋田県美郷町 `misato`・宮城県美里町 `misato-town` と重ならない形 |
| misato-town-saitama | 埼玉県美里町（児玉郡） | 島根・熊本・宮崎の `misato-town-<県>` に合わせた |
| fujimi-city / fujimino | 埼玉県富士見市 / ふじみ野市 | 長野県富士見町 `fujimi` |
| hidaka-city | 埼玉県日高市 | 高知県日高村 `hidaka`・和歌山県日高町 `hidaka-town-wakayama` |
| ina-town | 埼玉県伊奈町（北足立郡） | 長野県伊那市 `ina` |
| miyoshi-town | 埼玉県三芳町（入間郡） | 徳島県三好市・広島県三次市 `miyoshi`、愛知県みよし市 `miyoshi-city` |
| ogawa-town | 埼玉県小川町（比企郡） | 長野県小川村 `ogawa` |
| kamikawa-town | 埼玉県神川町（児玉郡） | 北海道上川町・兵庫県神河町 `kamikawa` |
| yokohama | 神奈川県横浜市（既存ページ、parent area/kanagawa） | 変えない。青森県横浜町は `yokohama-town` |
| kawasaki | 神奈川県川崎市 | 宮城県・福岡県の川崎町は `kawasaki-town` なので `kawasaki` を使う |
| yamato-city | 神奈川県大和市 | 熊本県山都町 `yamato`・鹿児島県大和村 `yamato-village` と分ける |
| chiba-city | 千葉県千葉市（県と同じ名前。県ページは chiba） | 千葉 |
| ichikawa-city / tateyama-city / noda-city / sakura-city / katsuura-city / yachiyo-city / asahi-city | 千葉県の市川市・館山市・野田市・佐倉市・勝浦市・八千代市・旭市（既存の兵庫県市川町・富山県立山町・岩手県野田村・栃木県さくら市・徳島県勝浦町・茨城県八千代町と同じ slug、富山・山形の朝日町と紛らわしい） | 千葉 |
| sakae-town / tonosho-town / ichinomiya-town / otaki-town | 千葉県の栄町・東庄町・一宮町・大多喜町（既存の長野県栄村・香川県土庄町・愛知県一宮市・長野県王滝村と同じ slug） | 千葉 |
| tako / shibayama / nagara / shirako / yokoshibahikari / kozaki / sammu / chosei ほか | 千葉県の町村（2026-11-12 時点で既存の slug と重ならない。神奈川・埼玉で同じ slug を使うときはここに書く） | 千葉 |
