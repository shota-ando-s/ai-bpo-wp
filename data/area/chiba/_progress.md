# 千葉県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-12。WebSearch はセッションで200回まで（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」）。サブエージェントの同時起動は2人まで。

**同時に神奈川・埼玉の地域ページと北海道の続きを別々のセッションで作っている**。共有メモは `data/area/_shutoken/shared.md`。千葉県だけのファイル（data/area/chiba/、docs/area-writing-spec-chiba.md、articles/*-area-chiba*.md）は自由に作る。`data/subsidies/chiba.yml` は areas.yml の千葉県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_shutoken/shared.md）は直す直前に `git pull --rebase origin main`。書きかけの記事は main に入れない（post_changed.py が公開する）。.git/info/exclude で未追跡のまま置き、書き終えた分は area-chiba-wip ブランチに退避する。

## 市町村と slug（54市町村＝37市16町1村。県コード12）
- 一覧は data/area/chiba/_brief.md
- 千葉市は1ページ（区のページは作らない）。slug は chiba-city
- 既存の slug とぶつかるので変えた: 市川市 ichikawa-city（兵庫県市川町 ichikawa）・館山市 tateyama-city（富山県立山町）・野田市 noda-city（岩手県野田村）・佐倉市 sakura-city（栃木県さくら市）・勝浦市 katsuura-city（徳島県勝浦町）・八千代市 yachiyo-city（茨城県八千代町）・栄町 sakae-town（長野県栄村）・東庄町 tonosho-town（香川県土庄町）・一宮町 ichinomiya-town（愛知県一宮市）・大多喜町 otaki-town（長野県王滝村）。旭市 asahi-city（富山県・山形県の朝日町と紛らわしい）
- パイロットの areas.yml の code `chiba/ichikawa` は `chiba/ichikawa-city` に直す（ほかのファイルからの参照は chiba.yml・areas.yml だけ。2026-11-12 grep）
- 試算は「月の削減時間・時間換算額」だけの形。**他県との重なりは許容し、千葉県の中だけ時間・金額・規模を重ねない**（2026-11-11 ユーザー決定）

## 調査の分担と WebSearch の配分（予定）
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 22 |
| gov | gov_ai.md（県・国の出先機関・総務省表の全54行・千葉/葛南/東葛/印旛の市） | 12 |
| gov_b | gov_ai_b.md（そのほかの市） | 8 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・37市） | 10 |
| choson | gov_ai_c.md / subsidy_c.yml / subsidy_c_areas.md（16町1村） | 8 |
| companies | companies.json / companies.md | 8 |
| outside | cases_outside.md / serp.md | 14 |
| cases2 | cases2.md（補充） | 10 |
| 合計 | | 106 |

## 状態
- [x] ネットワーク確認（pref.chiba.lg.jp・soumu.go.jp とも WebFetch で開けた。2026-11-12）
- [x] _brief.md・wages.md・area_uniq.py に chiba
- [ ] 調査（9担当）
- [ ] 試算の PLAN（_calc.py）
- [ ] 執筆仕様 docs/area-writing-spec-chiba.md
- [ ] 記事 55本（県1＋市町村54）
- [ ] data/subsidies/chiba.yml・areas.yml・build
- [ ] 地域ガイド・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-12 開始。WebSearch 0回
- 国のデジタル化・AI導入補助金 7次締切は 2026-12-01（火）17:00、交付決定 2027-01-19（火）予定（事務局 https://it-shien.smrj.go.jp/schedule/ を 2026-11-12 に WebFetch で確認。national.yml と同じ）
- stats（WS14）・cases（WS22）起動
- 行政の分け方: gov＝県・国・総務省表54行・千葉市・葛南5市（市川・船橋・習志野・八千代・浦安）・東葛6市（松戸・野田・柏・流山・我孫子・鎌ケ谷）・印旛7市（成田・佐倉・四街道・八街・印西・白井・富里）、gov_b＝残り18市（銚子・館山・木更津・茂原・東金・旭・勝浦・市原・鴨川・君津・富津・袖ケ浦・南房総・匝瑳・香取・山武・いすみ・大網白里）
- cases 17（完了: cases.md 247行。未使用・数値つき: **松戸運送**（松戸市、運送62名、AIドラレコで映像確認 月260h削減〔5台分、実測か不明〕・事故ゼロ、松戸市デジタル化チャレンジ補助金の活用事例 R4）・**ノバ・メディクス**（君津市、居宅介護支援13名、県の介護事例集 R7、1人13h/月〔noman、AIの語なし〕・約42h〔単位なし〕、導入前後の実測）。数値なし: ホテル三日月（木更津）・吉野機械製作所（千葉市、作る側）・誠馨会・亀田IVFクリニック幕張・リエイ（浦安、試作）・銚子信用金庫。県の先進的デジタル技術活用実証補助金は計画だけ。使用済み: のぞみ会（松戸→和気町）・利衛門・芝山農園（香取）・土屋ライスファーム（東金）・ヤマニ果樹農園（市川）。建設・製造の導入側・水産・農業の未使用・小売は見つからず。関東経産局は 403。**「令和8年8月千葉豪雨」の報道あり→stats で県の被害報を確かめる**
- gov（WS12）起動
- stats 4（完了: stats.md 約1,230行・stats_labor.md。**2026年の災害2件**: 8月千葉豪雨（8/13〜14、死者13・不明1、救助法25市町）・台風第25号（9/20〜21、死者10〔鴨川4〕、救助法24市町村、商工被害380者・25.5億円）、10/29 地震（横芝光町 震度5弱、被害なし）。TDB 千葉県版5本（社長61.4歳・休廃業2,382・生成AI 29.9%/308社・正社員不足52.8%/391社・最賃）、後継者不在率は全国版40.4%。地域区分は常住人口調査の11地域。有効求人倍率1.01倍（2026-09）、一般事務0.18・建設7.15・介護3.40、最賃1,195円、HW13所。出荷額全国6位、石油製品1位（市原・袖ケ浦で98%）。社人研・漁港の水揚げ額・落花生の市町村値・成田空港の従業員（空港会社）は取れず
