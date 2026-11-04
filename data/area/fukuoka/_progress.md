# 福岡県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-04。WebSearch はセッション全体で200回（調査は115回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。九州7県を別々のセッションで同時に作っている（共有メモ data/area/_kyushu/shared.md）。サブエージェントは同時3人まで。

福岡県だけのファイル（data/area/fukuoka/、docs/area-writing-spec-fukuoka.md、articles/*-area-fukuoka*.md、data/subsidies/fukuoka.yml）は自由に作る。`data/subsidies/fukuoka.yml` は areas.yml の福岡県の行と同じコミットで push する。共通ファイルは直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（60市町村。県コード40）
- 一覧は data/area/fukuoka/_brief.md。福岡市 `fukuoka-city`・北九州市 `kitakyushu`（区のページは作らない）
- 他県と同じ slug: okawa（高知 大川村）・nakagawa（長野 中川村）・miyako（岩手 宮古市）・kawasaki-town（宮城 川崎町）→ area-todo に投稿後の確認
- 試算: 月の削減時間×4 を7で割った余りが 0 の時間だけ（九州7県の割り当て）。全県の記事・全県の _calc.py の PLAN と照合
- scripts/area_uniq.py の県の選択肢に fukuoka を足した（push 済み）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md | 8 |
| stats_labor | stats_labor.md | 6 |
| gov_a | gov_ai.md（県・29市・総務省表60行・国の出先機関） | 15 |
| gov_b | gov_ai_b.md（31町村） | 8 |
| subsidy_a | subsidy_a.yml / subsidy_a_areas.md（県・29市） | 12 |
| subsidy_b | subsidy_b.yml / subsidy_b_areas.md（31町村） | 6 |
| cases | cases.md | 25 |
| companies | companies.json / companies.md | 15 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |
| 合計 | | 110 |

## 状態
- [x] _brief.md・wages.md・area_uniq.py（2026-11-04）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-fukuoka.md
- [ ] 記事 61本（県1＋市町村60）
- [ ] data/subsidies/fukuoka.yml・areas.yml・build
- [ ] 地域ガイド（九州地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-04 ネットワーク確認（pref.fukuoka.lg.jp・soumu.go.jp とも開けた）。調査3人を起動（stats・cases・gov_a）
- cases 25（完了: cases.md。未使用の数値つきは2件だけ: **九州鉄道機器製造**〔北九州市門司区、AIビジョンカメラ付きバリ取りロボット、労働生産性1.5倍・3名→2名、FAIS 相談事例、ロボット全体の効果〕・**ペンシル**〔福岡市中央区、約140人、生成AI 1か月テストで月28時間相当、労働新聞 2024-07-31。年2000時間は目標〕。数値なし: 大川家具ドットコム〔大川市〕・糸島みるくぷらんと×Regnio〔糸島市、実証、結果未公表〕・山本工作所〔北九州市、計画〕・ハピクロ〔同名2社〕。大企業: デンソー九州・福岡銀行・九州日立システムズ。リキマンは同一会社か不明で使わない。使用済みだけ: 直方・久留米・八女・篠栗・久山・粕屋。50市町村は事例なし。県・IST・九州経産局（403）の AI 事例集なし、福岡商工会議所 fcci.or.jp 不通。他県の記録と所在の食い違い: やまやコミュニケーションズ〔愛媛 松前町の記事は福岡市、法人番号は篠栗町〕・嘉穂無線HD〔青森の cases_outside は那珂川市、法人番号は福岡市中央区〕・東福運送〔山形市の記事は「福岡県」、法人番号は粕屋町〕→ area-todo。手がかり: 福岡県中小企業DX推進センター（2025-10-20開所）・北九州市DX推進補助金・福岡市 実証実験フルサポート）
- companies 起動（WS15）
- gov_a 13（完了: gov_ai.md 714行。総務省表 60団体確認、生成AI 36〔導入済23・実証中13〕、政令市を除く58で導入済21＝36.2%〔全国その他市区町村45.6%〕、両表にない12〔市は那珂川市だけ〕。県・北九州市・糸島市 QT-GenAI、県ガイドライン第2.2版、町村は zevo 10。北九州市 AI議事録 13,300h（R6実績）・AI活用推進都市宣言（2025-07、OpenAI 連携）、福岡市 AI-OCR 年50,202h は RPA 合計、久留米市 AI-OCR 年4,189h。直方市は報道のみ（2030年度 年3.5万h 目標、市長 CAIO）。のるーと中間 2026-10-01、宗像市大島 のるーと 2025-10。企業向け: 県「中小企業“稼ぐ力”応援センター（旧 DX推進支援センター）」〔名前が3通り〕・よろず「生産性向上支援センター」（2026-04、無料）・北九州市ロボット・DX推進センター（FAIS）・福岡市 mirai@／実証実験フルサポート／ふくおかデジタルプラス。セミナー 11/24 九州商工会議所連合会（無料80名）・12/3・12/8 北九州市ロボDXセンター（無料20名）。知事 服部誠太郎（R3 1期目・R7 2期目、就任日は公式で未確認）。**財務局は福岡財務支局（福岡・佐賀・長崎）／九州財務局（熊本・大分・宮崎・鹿児島）**、九州運輸局（福岡運輸支局 東区みなと香椎）、九州農政局 福岡県拠点 092-281-8261、福岡労働局 最低賃金1,114円（2026-10-04）。DX計画は県の DX戦略 2025-2027 以外未確認。開けず: 九州経産局403・よろず502・稼ぐ力センター メンテ・田川/柳川/春日 curl 不可）
- gov_b 起動（WS8）
