# 広島県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の「feat(area): 鳥取県の県ページ」〔6bf32a4〕の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-01。新しいセッションなので WebSearch の残りは200回（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

**同じ main に山口県のセッションが書いている（山梨・島根・鳥取は作成済み）。** 広島県だけのファイル（data/area/hiroshima/、docs/area-writing-spec-hiroshima.md、articles/*-area-hiroshima*.md、data/subsidies/hiroshima.yml）は自由に作る。`data/subsidies/hiroshima.yml` は areas.yml の広島県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json）は最後に `git pull --rebase origin main` してから直す。衝突したら両方の追加を残し、subsidies.json は build し直す。force push はしない。

## 市町と slug（23市町。県コード34）
- 一覧は data/area/hiroshima/_brief.md
- 府中市 `fuchu-city`・府中町 `fuchu-town`、広島市 `hiroshima-city`（区のページは作らない）
- 他県と同じ slug: 三原市 mihara（高知県三原村）・三次市 miyoshi（徳島県三好市）。投稿後に確かめる項目を area-todo に残す
- 試算は「月の削減時間・時間換算額」だけの形。山梨・島根・鳥取（と push されていれば山口）の _calc.py の PLAN と照合する
- scripts/area_uniq.py の県の選択肢に hiroshima を足す差分は scratchpad/area_uniq.patch に退避（共通ファイルは最後に直す取り決め）。**執筆担当を起動する前に git apply する**

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| gov | gov_ai.md | 20 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 20 |
| cases | cases.md | 25 |
| companies | companies.json / companies.md | 15 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |
| 合計 | | 107 |

## 状態
- [x] _brief.md・wages.md（2026-11-01）
- [ ] 調査（6担当）
- [ ] 執筆仕様 docs/area-writing-spec-hiroshima.md
- [ ] 記事 24本（県1＋市町23）
- [ ] data/subsidies/hiroshima.yml・areas.yml・build
- [ ] 地域ガイド（中国地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-01 ネットワーク確認（pref.hiroshima.lg.jp・soumu.go.jp とも開けた）。調査4人を起動（stats・gov・subsidy・cases）
- cases 24（完了: cases.md 350行。**県の「DX取組事例」サイト dx-hiroshima.jp/jirei/（未使用の出典）135件を全件取得**、「広島県内事例」52件のうちAI記述8件を照合。数値つき7件: ツーセル〔広島市南区、契約書レビュー 1件2〜3h→10〜30分・弁護士費用 年約75%減〕・レリーフ〔広島市西区、市場調査 3カ月→10日程度〕・en.company〔広島市安佐南区、宿泊、チャットボット 問い合わせ約9割・対応時間約30%減〕・オオケン〔広島市南区、ビル管理、301〜900人＝中小企業の基準超、検針の転記 約6割短縮〕・尾道さつき会〔尾道市、特養、議事録 平均35分→10分、県の介護DXモデル事業、出典 総務省 001088286.pdf〕・晃祐堂〔熊野町、熊野筆の検品 精度90%以上、ブレインパッド2020〕・大崎上島町のレモン農家3者〔AIかん水施肥 作業時間80%減、農研機構の実証、同資料に「費用対効果が低い」〕。数値なし: ひろしまAIサンドボックス第1期20件〔鳴滝工業・門井商店ほか、開発・実証中〕・県のバックオフィスDX〔社名なし〕。他県で使用済み: 常石造船・アヲハタ・山陽病院・クラハシ・地御前漁協・世羅幸水農園・チチヤス→1〜2文。**事例なし11市町**: 府中市・三次市・庄原市・大竹市・安芸高田市・江田島市・府中町・坂町・安芸太田町・北広島町・神石高原町。0件の業種: 造船・デニム・家具・かき・建設・運送。403: 中国経産局・ひろしま産業振興機構・DXセレクション。県の事例集の見出しなし83件（県外とみられる）→cases_outside へ。一覧は scratchpad/cases/dl/classify.txt）
- companies 起動（WS15）
