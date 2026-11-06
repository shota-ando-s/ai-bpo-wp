# 茨城県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-05。WebSearch はセッションで200回まで（調査は115回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（北海道・北関東3県・沖縄を同時に作っている。アカウントの7日間の利用上限が警告の状態）。

茨城県だけのファイル（data/area/ibaraki/、docs/area-writing-spec-ibaraki.md、articles/*-area-ibaraki*.md）は自由に作る。`data/subsidies/ibaraki.yml` は areas.yml の茨城県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_batch5/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（44市町村。県コード08）
- 一覧は data/area/ibaraki/_brief.md
- 茨城町 `ibaraki-town`、境町 `sakai-town`。古河市 `koga`・鹿嶋市 `kashima`・那珂市 `naka` は他県と同じ slug（親ページが違う）
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を5で割った余りが1の時間だけ**（0.25, 1.5, 2.75, …の1.25時間刻み）。全県の記事・全県の _calc.py の PLAN と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 25 |
| gov | gov_ai.md（県・32市・国の出先機関・総務省表の全44行） | 14 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・32市） | 12 |
| choson | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（10町2村） | 10 |
| companies | companies.json / companies.md | 12 |
| outside | cases_outside.md / serp.md | 15 |
| cases2 | cases2.md（補充） | 10 |
| 合計 | | 112 |

## 状態
- [x] _brief.md・wages.md（2026-11-05）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-ibaraki.md
- [ ] 記事 45本（県1＋市町村44）
- [ ] data/subsidies/ibaraki.yml・areas.yml・build
- [ ] 地域ガイド（北関東の段）・area_uniq.py・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-05 ネットワーク確認（pref.ibaraki.jp・soumu.go.jp とも開けた）。ローカルの main が detached だったので origin/main に合わせ直した
- stats（WS14）・cases（WS25）起動
- stats 4（完了: stats.md・stats_labor.md。44市町村一致。**2026年の大きな災害なし**（8/23 茨城県南部の地震 軽傷1・住家被害なし、台風・大雨4件）。R7国調確定値 2,789,856人（▲2.7%、第3-3表 000040517850）、県の推計人口は R7国調確定値が基準。15〜64歳は当社計算（つくば市+12.4%・大子町▲20.6%）。5地域の所属は県の国調ページの注。製造品出荷額 全国8位、農業産出額 5,494億円 全国3位（当社で並べると鉾田市の野菜・いも類、小美玉市の鶏卵が市町村1位）。**有効求人倍率 1.15倍（2026-09、全国26番目）・就業地別1.36**、ハローワーク13所。**TDB水戸支店の県版 5テーマとも**: 後継者不在率41.0%（4,771社）・社長年齢61.7歳（全国6位）・休廃業1,155件（32市・7郡の値）・人手不足（正社員）53.5%（146社）・生成AI 27.9%（147社）。最低賃金1,136円（2026-10-18）。見つからない: 社人研・職業別求人倍率・品目と市町村の対応・漁港別水揚げ・県内のAI利用率調査。労働局の表は常陸大宮所を県央に入れる（県の区分は県北））
- gov（WS14）起動
- cases 22（完了: cases.md 273行。**事業者自身が実績で公表したAI事例は0件**。数値つき: 川崎製作所（ひたちなか市、AIで工具摩耗予測「工具の使用期間が50%長く」、ITIC R5成果集 p.6、国の補助の共同研究。同じ文の「加工時間50%削減」は自動計測でAIではない）・アーストラベル水戸（水戸市、Gemini+GAS で名簿照合、ベンダー〔ユードム〕の PR TIMES 2026-05-12、本文の「数分」を使う）・トヨタモビリティパーツ茨城支社（水戸市、AI-OCR 1日約3.7時間、ベンダー、大企業グループ）・日立製作所 大みか事業所（大企業、AI外観検査 PoC）。数値なし: ハリガイ工業（常総市、見込み）・ヒューマンサポートテクノロジー（東海村、AIを作る側）・県の戦略分野新製品開発 R8 の AI テーマ4社（採択まで）・ITIC 生産性向上研究会（5社、中間報告 2026-11-20）。**使用済み: つづく農園（常陸大宮市→宮城県亘理町で詳述）**。茨城新聞のサイトは 2026-10-23 から停止。関東経産局は開けない）
- subsidy（WS12）起動
