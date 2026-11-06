# 沖縄県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-05。WebSearch はセッションで200回まで（調査は120回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（北海道・茨城・栃木・群馬を同時に作っている。アカウントの7日間の利用上限が警告の状態）。

沖縄県だけのファイル（data/area/okinawa/、docs/area-writing-spec-okinawa.md、articles/*-area-okinawa*.md）は自由に作る。`data/subsidies/okinawa.yml` は areas.yml の沖縄県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_batch5/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（41市町村＝11市11町19村。県コード47）
- 一覧は data/area/okinawa/_brief.md（総務省の全国地方公共団体コードで確認）
- 沖縄市 `okinawa-city`、西原町 `nishihara-town`、東村 `higashi-village`
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を5で割った余りが4の時間だけ**（1.0, 2.25, 3.5, … の1.25時間刻み）。全県の記事・全県の _calc.py の PLAN（北海道・北関東3県を含む）と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| gov | gov_ai.md（県・11市・国の出先機関・沖縄振興の制度・総務省表の全41行） | 14 |
| cases | cases.md | 25 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・11市） | 12 |
| choson_a | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（本島の17町村） | 10 |
| choson_b | gov_ai_c.md / subsidy_c.yml / subsidy_c_areas.md（離島の13町村） | 10 |
| companies | companies.json / companies.md | 12 |
| outside | cases_outside.md / serp.md | 15 |
| cases2 | cases2.md（補充） | 8 |
| 合計 | | 120 |

## 状態
- [x] _brief.md・wages.md（2026-11-05）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-okinawa.md
- [ ] 記事 42本（県1＋市町村41）
- [ ] data/subsidies/okinawa.yml・areas.yml・build
- [ ] 地域ガイド・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-05 ネットワーク確認（pref.okinawa.lg.jp・soumu.go.jp とも開けた）。ローカルの HEAD が detached だったので `git checkout -B main origin/main`。市町村41を総務省のコード表で確認。area_uniq.py に okinawa を足した。共有メモに slug を push
- gov 10（完了: gov_ai.md。**知事は古謝玄太（2026-09-30 就任、1期目）**。玉城知事と書かない。**「産業高度化・事業革新促進地域」は今は「産業イノベーション促進地域」**。**商工会議所は5所（那覇・沖縄・宮古島・浦添・宜野湾）**、石垣・名護は商工会。総務省表（41市町村）生成AI 導入済15・実証中8・表にない18（市は宜野湾・糸満）、AI全般 導入済19・実証中2、両方なし14町村。削減時間: 浦添市 1人月10h（実証中）・南城市 年100h見込み・八重瀬町 年120h。県庁は exaBase、県DX推進計画（R4〜R13、第1.4版）・新・沖縄21世紀ビジョン基本計画に「生成AI」の語なし。特措法は2032-03-31 失効。国の出先は沖縄総合事務局（6部）、九州の局は沖縄を管轄しない（運輸部の所掌は九州運輸局の支局一覧からの判断）。県の沖縄DX推進・促進支援事業の採択一覧（R5〜R8、Industlink）→ cases。セミナー: 11/12 那覇市の生成AI講座（無料、11/11締切）・11/19 よろずのAIセミナー・11/19〜20 ResorTech EXPO（沖縄市）・12/2 伊平屋の補助金セミナー。照合: 台風30号の融資の対象5市町村（subsidy）、最低賃金1,086円 2026-12-02 発効（stats）、粟国・渡名喜・北大東・多良間は商工会の名簿にない（choson））
- stats 11（完了: stats.md・stats_labor.md。41市町村一致、人口・事業所・産出額は市町村の合計＝県計。**R7国調確定値 1,466,548人（▲932人・▲0.1%、県は「戦後初の減少」）**、推計人口は R7国調確報基準。**県の概要の表8（R2の年齢3区分）は総人口に28,372人足りず、県本文の「15〜64歳は増加」は不詳補完値で比べると▲1.1%（当社計算）**→ 15〜64歳は不詳補完値で書く・統計課への照会は area-todo。**有効求人倍率 就業地別1.06・受理地別0.93（2026-09）**、ハローワーク5所（宮古1.96が最高）、事務0.46・一般事務0.43。最低賃金 1,023円→**1,086円（2026-12-02 発効）**。**TDB の沖縄県版は全テーマ404**: 九州・沖縄版の沖縄の行（後継者不在率61.0%＝全国6番目に高い、社長年齢59.7歳＝三重と並び全国で最も若い、採用時の最低時給1,180円）、休廃業544件（全国版）、生成AI・人手不足は県別なし。AI利用: おきなわITセンサス（IT企業259社）生成AI業務利用43.2%、県の観光産業実態調査（265事業所）「紙・口頭中心」18.9%。観光収入（R7年度）1兆747億円、入域観光客 2025年 10,756,000人。IT企業 899社・36,004人。離島は県「離島関係資料」（R8-03）。基地は市町村面積に占める割合（嘉手納町82.0%）、時点の食い違い（R6-01-01 と R7-01-01）。地域区分は北部・中部・南部・宮古・八重山。災害: R7台風第8号で南大東・北大東に災害救助法、R8台風第7号のページは404。取れず: 社人研・町村の製造業中分類・本島の漁業・慶良間/久米島/大東の入域客数）
