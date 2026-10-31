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
