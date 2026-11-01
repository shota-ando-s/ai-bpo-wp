# 山口県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の「feat(area): 鳥取県の県ページ」〔6bf32a4〕の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-01。新しいセッションなので WebSearch の残りは200回（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

**同じ main に鳥取県のセッションが書いている（山梨県・島根県は作成済み）。** 山口県だけのファイル（data/area/yamaguchi/、docs/area-writing-spec-yamaguchi.md、articles/*-area-yamaguchi*.md、data/subsidies/yamaguchi.yml）は自由に作る。`data/subsidies/yamaguchi.yml` は areas.yml の山口県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json）は最後に `git pull --rebase origin main` してから直す。衝突したら両方の追加を残し、subsidies.json は build し直す。force push はしない。

## 市町と slug（19市町。県コード35）
- 一覧は data/area/yamaguchi/_brief.md
- 山口市は `yamaguchi-city`（青森市 aomori-city と同じ形）。既存609本の slug と照合して衝突なし
- 試算は「月の削減時間・時間換算額」だけの形。山梨・島根・鳥取の _calc.py の PLAN と照合する
- scripts/area_uniq.py の県の選択肢に yamaguchi を足した（執筆前に。コミットは共通ファイルと一緒に最後）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 12 |
| gov | gov_ai.md | 20 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 20 |
| cases | cases.md | 28 |
| companies | companies.json / companies.md | 12 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |
| 合計 | | 107 |

## 状態
- [x] _brief.md・wages.md（2026-11-01）
- [ ] 調査（6担当）
- [ ] 執筆仕様 docs/area-writing-spec-yamaguchi.md
- [ ] 記事 20本（県1＋市町19）
- [ ] data/subsidies/yamaguchi.yml・areas.yml・build
- [ ] 地域ガイド（中国地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-01 ネットワーク確認（pref.yamaguchi.lg.jp・soumu.go.jp とも開けた）。HEAD が detached だったので main を origin/main に合わせた。調査4人を起動（stats・gov・subsidy・cases）
- 中継の連絡（鳥取県のセッション）: 鳥取は 6bf32a4 で作業終了。tottori/_calc.py の PLAN 確定版あり（月58.75〜185h）。エーアンドエス（→北栄町）・グリーンハートティーアンドケイ（→琴浦町）は鳥取で詳述済み→山口では使わない
- 中継の連絡: **広島県（23市町）のセッションが同じ main で開始**。広島側が yamaguchi/_calc.py の PLAN と照合するので、PLAN が固まったら早めに push する。県外事例の割り当ても広島と重ならないよう、山口で使う事例を早めに記録・push する
- gov 20（完了: gov_ai.md。19団体=13市6町を確認。生成AI 16〔導入済13・実証中3＝下松・光・和木〕、表にない防府・柳井・阿武。AI全般17〔ない和木・上関〕。両方にない市町なし。岩国・光は詳細表に行なし。生成AIの削減数値: 萩市1,435h〔R6.11〜R7.10 実績〕・上関町30h・平生町5h〔見込み〕。AI全般: 下関 議会会議録 年2,367h〔約98%減〕・防府6件〔橋梁診断 年約800万円 試算〕。県: 2023-04-28 試行→2023-11-24 ガイドライン Ver1.0、Azure OpenAI〔Y-BASE〕→R8 tsuzumi・GaiXer 19,730千円、RPA等 年15,700h〔R8.1末、生成AIではない〕、生成AI目標13,000h〔R8〕。AIデマンド交通: 県資料「3年間で10市町12件の実証」、山陽小野田・周防大島が本格運行、長門市実証〔R7.10〜R8.1〕。知事 村岡嗣政〔2014-02就任・2026-02 4期目、日は未確認〕。Y-BASE 利用者10,648人・DXコンサル630件〔R8.1末〕、運営主体は未確認〔サイト503〕。商工会議所14〔美祢市なし〕・商工会20。九州運輸局の管轄あり〔下関・宇部・長門・山陽小野田の倉庫業等〕。DX計画なし/不明: 下関・防府・光・山陽小野田・周防大島・和木・上関・田布施。産業技術センターは証明書エラー。最低賃金1,101円〔R8.10.8〕→stats と照合）
- companies 起動（WS12）
- stats 6（完了: stats.md・stats_labor.md。コード19件一致〔35201〜35216・35305・35321・35341・35343・35344・35502〕。**R7国調確定値 1,262,770人〔−5.9%〕**、減少大 上関−19.3%・美祢−13.4%・周防大島−13.2%、15〜64歳の減少最小 下松−0.6%。推計人口 2026-10-01 1,245,629人〔R7基準〕。社人研403。製造業出荷額 7兆3,491.5億〔2024年〕、化学・石油・鉄鋼・輸送機械で70.9%、防府23.0%〔輸送機械80.0%〕・周南20.2%〔化学78.7%〕・和木5事業所6,301.9億〔中分類なし〕。農業産出額 山口市170.1億・下関161.0億。漁業は市町別の表なし。**観光は市町別あり**〔2025年 県計33,420,958人〕。地域区分: 観光4地域〔東部・中部・北部・西部〕・保健所9区分〔美祢市は観光=中部・保健所=宇部〕。**有効求人倍率 2026-09 受理地別1.23倍・就業地別1.40倍**、HW9所〔下関1.51・防府0.96・岩国0.99〕、職業別は県全体版で確認〔一般事務0.32・建設採掘6.65〕。**TDB山口支店 県版3本: 後継者不在率53.4%〔全国19位〕・社長60.9歳〔26位〕・休廃業618件〔全国版619と1件差→県版〕**。中国地方版の山口の行: 生成AI活用36.9%〔122社〕・正社員不足42.9%〔112社〕。最低賃金1,101円〔2026-10-08〕。県のAI利用率調査なし、中央会DX調査59.4%〔AI設問なし〕。山口経済研究所502）
- cases_outside・serp 起動（WS15）
