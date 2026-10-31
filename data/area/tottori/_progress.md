# 鳥取県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の「docs(area): 島根県を地域ガイド・残作業・手順書・memory に追加」〔1b6552a〕の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-10-31。新しいセッションなので WebSearch の残りは200回（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

**同じ main に島根県のセッションが書いている（山梨県も同日）。** 鳥取県だけのファイル（data/area/tottori/、docs/area-writing-spec-tottori.md、articles/*-area-tottori*.md、data/subsidies/tottori.yml）は自由に作る。`data/subsidies/tottori.yml` は areas.yml の鳥取県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json）は最後に `git pull --rebase origin main` してから直す。衝突したら両方の追加を残し、subsidies.json は build し直す。force push はしない。

## 市町村と slug（19市町村。県コード31）
- 一覧は data/area/tottori/_brief.md
- 他県と同じ slug: 若桜町 wakasa（福井県若狭町）・大山町 daisen（秋田県大仙市）・南部町 nanbu（青森県・山梨県）・江府町 kofu（山梨県甲府市）。親ページが違うので別ページになる前提（朝日町・かほく市と同じ）。投稿後に確かめる項目を area-todo に残す
- 試算は「月の削減時間・時間換算額」だけの形。山梨・島根の _calc.py の PLAN と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| gov | gov_ai.md | 18 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 18 |
| cases | cases.md | 25 |
| companies | companies.json / companies.md | 12 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |
| 合計 | | 100 |

## 状態
- [x] _brief.md・wages.md（2026-10-31）
- [ ] 調査
- [ ] 執筆仕様
- [ ] 記事 20本
- [ ] data/subsidies/tottori.yml・areas.yml・build
- [ ] 共通ファイル
- [ ] チェック・push

## 実績メモ
- 2026-10-31 ネットワーク確認（pref.tottori.lg.jp・soumu.go.jp とも開けた）。調査4人を起動（stats・gov・subsidy・cases）
- 島根県のセッションから連絡（中継）: 島根は 1b6552a で作業終了。地域ガイドの「## 中国地方の地域ページ」の表に行を足し、段の一文目を両県に合わせて直す。県外事例の内能美漁協ほか・アイグラン（島根）・カワトT.P.C.（山梨）は使わない。試算は shimane/_calc.py の PLAN と照合
- gov 16（完了: gov_ai.md 522行。生成AI 導入済9〔米子・倉吉・智頭・三朝・北栄・伯耆・日南・日野・江府〕・実証中3〔鳥取・境港・八頭〕。両方の表にないのは岩美・南部。ログミーツGPT 5町。江府町は詳細表に行なし。県: 議事録 年16,560h・AI-OCR 5,709h・チャットボット 2,300h〔「創出」〕、2023-06 国への提案書で議会答弁等の使用禁止→2023-08 暫定版→2024-06「人間主導AI（えぇ愛）ガイドライン」→2026-09 第2.0版、CAIO＝知事。**知事 平井伸治〔2007-04-13 初就任〕**。企業向け: 生成AI補助金〔7/31締切の表示〕・モデル企業6社・とっとりAI・AX実践プログラム〔アンドドット〕・とっとりDXラボ・機構と産技センターの研修。よろず＝県商工会連合会内。AI交通: 智頭町のりりん〔2023-04本格〕・境港市みなとーる〔2025-04-01〕・鳥取駅南とりmobi〔2023-10実証〕。DX計画: 米子市 第2期 R8〜12「AX」・鳥取市 DX推進方針 第8版・三朝町 R8〜11。国の出先5機関確認〔中国経産局は農水省の窓口一覧〕。商工会議所4・商工会18〔倉吉市・境港市は商工会なし〕。**気高電機は山梨県西桂町で詳述済み→鳥取では1〜2文**。接続不可: 倉吉市・八頭町・南部町・米子商工会議所。最低賃金1,090円〔労働局の見出し〕→stats と照合）
- companies 起動（WS12）
- subsidy 3（完了: subsidy_a.yml 11件〔県・鳥取市〕・subsidy_b.yml 4件〔琴浦町・伯耆町2・日南町〕。県の支援施策DB「とっとり産業支援ナビ」で19市町村を一覧。**県の中小企業DX推進支援補助金【生成AIの利活用】は 6/12〜7/31 で終了**〔戦略策定型 1/2・100万、実装型 製造業のみ 1/2・1,000万〕。受付中: 県 持続的な賃上げ・生産性向上支援補助金〔3型、12/18締切、賃上げ3%以上〕・産業未来共創補助金 生産性向上・新技術導入推進型〔1/2・500万、事業認定 11/2〜11/30・2027-01-04〜01-29〕・工学エキスパート育成・週1副社長〔随時〕。市のAI名指しは鳥取市 中小企業人材育成補助金〔AI等の講習、1/2・1人5万・1社20万、9/24 再開〕・リモートワーカー等外部人材〔1/2・30万〕。琴浦町 DX推進〔20万、10/30 終了〕。**addon は伯耆町だけ**〔国・県の補助の自己負担の1/2・年50万、デジタル化・AI導入補助金が対象かは要綱に記載なし→注記〕。米子市の補助金一覧が開けず、9町村は DB だけで判断。機構の生成AI実践活用研修 12/10・12/17 無料 申込11/30）
- cases_outside・serp 起動（WS15）
