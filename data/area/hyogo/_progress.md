# 兵庫県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-11。WebSearch はセッションで200回まで（調査は115回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（静岡・愛知・三重・京都〔と北海道〕を別のセッションで同時に作っている）。

兵庫県だけのファイル（data/area/hyogo/、docs/area-writing-spec-hyogo.md、articles/*-area-hyogo*.md）は自由に作る。`data/subsidies/hyogo.yml` は areas.yml の兵庫県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_kinki/shared.md、_tokai/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない（記事は全ページそろうまで `.git/info/exclude` で未追跡のまま置き、書き終えた担当の分は別ブランチ area-hyogo-wip に退避する）。

## 市町と slug（41市町。県コード28）
- 一覧は data/area/hyogo/_brief.md
- 神戸市 `kobe`（1ページ）。他県と同じ・似た名前は slug を分けた（芦屋市 ashiya-city・豊岡市 toyooka-city・三木市 miki-city・川西市 kawanishi-city・小野市 ono-city・たつの市 tatsuno-city・稲美町 inami-town-hyogo・香美町 kami-town-hyogo）
- 試算は「月の削減時間・時間換算額」だけの形。**兵庫は時間の端数を限らない**（_tokai/shared.md）。静岡・愛知・三重・京都の PLAN（push されていれば）と全県の記事・全県の _calc.py の PLAN と照合し、**重なったら兵庫側が直す**

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| cases | cases.md | 20 |
| gov | gov_ai.md（県・国の出先機関・総務省表の全41行・県の補助金と支援機関・商工会議所/商工会の一覧） | 10 |
| govsub_1 | gov_ai_1.md / subsidy_1.yml / subsidy_1_areas.md（神戸・阪神: 神戸・尼崎・西宮・芦屋・伊丹・宝塚・川西・三田・猪名川町） | 8 |
| govsub_2 | gov_ai_2.md / subsidy_2.yml / subsidy_2_areas.md（東播磨・北播磨: 明石・加古川・高砂・稲美町・播磨町・西脇・三木・小野・加西・加東・多可町） | 8 |
| govsub_3 | gov_ai_3.md / subsidy_3.yml / subsidy_3_areas.md（中播磨・西播磨: 姫路・市川町・福崎町・神河町・相生・赤穂・たつの・宍粟・太子町・上郡町・佐用町） | 8 |
| govsub_4 | gov_ai_4.md / subsidy_4.yml / subsidy_4_areas.md（但馬・丹波・淡路: 豊岡・養父・朝来・香美町・新温泉町・丹波篠山・丹波・洲本・南あわじ・淡路） | 8 |
| companies | companies.json / companies.md | 10 |
| outside | cases_outside.md / serp.md | 12 |
| cases2 | cases2.md（補充） | 10 |
| 合計 | | 106 |

## 状態
- [x] _brief.md・wages.md・area_uniq.py に hyogo（2026-11-11）
- [ ] 調査（10担当）
- [ ] 試算の PLAN（_calc.py）を push
- [ ] 執筆仕様 docs/area-writing-spec-hyogo.md
- [ ] 記事 42本（県1＋市町41）
- [ ] data/subsidies/hyogo.yml・areas.yml・build
- [ ] 地域ガイド（近畿の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック（check_article・area_uniq・_calc.py・試算の結果表・書いてはいけない局名）
- [ ] main に push（投稿・デプロイはユーザーが Mac で「投稿して」）

## 実績メモ
- 2026-11-11 ネットワーク確認（web.pref.hyogo.lg.jp・soumu.go.jp とも開けた）。ローカルが detached だったので main を origin/main に合わせた
- stats（WS12）・cases（WS20）起動
- cases 20（完了: cases.md。**未使用で AI の効果の数値つきの県内事例は2件**: 神戸規志税理士事務所（明石市、Gemini で記帳の CSV 作成、月70時間減〔代表の発言、エフアンドエムの表彰の配信 2026-03-31〕）・川西リハビリテーション病院（川西市、medimo で診療録 約66%短縮〔大阪の病院と合わせた値〕・グループ3か月約2,000時間。法人の本店は猪名川町）。神戸市「DX推進事例集」11社は AI の数値0件（神戸化成の年約900時間は AI 前の作業時間）、数値なしで1文なら: 北神地域振興・旭光電機・御所坊・フォレスト・日高食品工業・ネオスタイル・ミツテック。関経連の事例集86本の兵庫5本は他県で使用済み。KANSAI DX AWARD 2026 金賞 エヌエスケーケー（使用済み）。オオナガの本店は神戸市西区（事例集の「稲美町」と違う）、ロザイ工業は本店県外・赤穂市は工場。見つからない: 清酒・播州織・皮革・金物・素麺・かばん・漁業・運送。中小企業家同友会の調査（19.4%・36.6%、神戸新聞 2026-02-27）→ stats。JR西日本カスタマーリレーションズ→ outside で照合）
- gov（WS10）起動
- stats 11（完了: stats.md 約230KB・stats_labor.md。41市町・コード一致、県民局10（2026-04-01 の組織改正後も所管は同じ）。R7国調確定 5,317,792人（▲2.69%、増えたのは明石市だけ）、県の推計人口は R7 基準。県外就業 13.1%（91%が大阪）: 川西市40.6%・猪名川町32.1%・芦屋市/宝塚市31.5%。出荷額 19.49兆円（2024）、化学・鉄鋼 13.7%ずつ、臨海8市区で61.1%。なめし革 事業所の42.6%・手引のこぎり34.1%・清酒 出荷額22.1%（公表県の合計比）。有効求人倍率 0.93倍（2026-09、近畿最低）・就業地別1.06、地域別 淡路1.65〜阪神0.73。一般事務 0.24・介護 3.60。HW 神戸市は5所、姫路市・赤穂市は2所に分かれる（WebFetch の要約で読んだ→使う前に原典）。最低賃金 1,172円（2026-10-01）。TDB 兵庫県版: 休廃業 2,144件・生成AI 32.2%（357社）。後継者不在率47.2%・社長年齢60.7歳は近畿版の兵庫の行。2026年の災害: 災害救助法の適用なし、災害警戒本部のみ（台風6号 姫路市 軽傷1・相生市 床下2）。阪神・淡路大震災は内閣府の資料（消防庁の確定値 兵庫 6,402人）。見つからない: HW 別の倍率・TDB の後継者/社長年齢/人手不足の県版・ほかの県内 AI 調査・漁港の水揚げ・淡路の交通の所要時間）
- govsub_1（WS8）起動
