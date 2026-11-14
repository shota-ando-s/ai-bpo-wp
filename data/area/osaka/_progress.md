# 大阪府 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-14。WebSearch はセッションで200回まで（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」）。サブエージェントの同時起動は2人まで（週の利用上限が警告の状態）。

**同時に東京都の地域ページを別のセッションで作っている**。近畿の共有メモは `data/area/_kinki/shared.md`。大阪府だけのファイル（data/area/osaka/、docs/area-writing-spec-osaka.md、articles/*-area-osaka*.md）は自由に作る。`data/subsidies/osaka.yml` は areas.yml の大阪府の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_kinki/shared.md）は直す直前に `git pull --rebase origin main`。書きかけの記事は main に入れない（post_changed.py が公開する）。force push はしない。

## 市町村と slug（43市町村＝33市9町1村。府コード27）
- 一覧は data/area/osaka/_brief.md
- 大阪市・堺市は各1ページ（区のページは作らない）。府 `osaka`、市 `osaka-city`・`sakai-city`
- 他県とぶつかる slug を変えた: 堺市 `sakai-city`・池田市 `ikeda-city`・茨木市 `ibaraki-city`・和泉市 `izumi-city`・岬町 `misaki-town`・太子町 `taishi-town-osaka`（共有メモに書いた）
- 試算は「月の削減時間・時間換算額」だけの形。**他県との重なりは許容し、大阪府の中だけ時間・金額・規模を重ねない**（2026-11-11 ユーザー決定）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 20 |
| gov | gov_ai.md / subsidy_pref.yml / subsidy_pref_areas.md（府・国の出先機関・総務省表の全43行・府域の補助金・商工会議所/商工会の名簿・府のリンク条件・万博/IR の一次資料） | 10 |
| govsub_1 | gov_ai_1.md / subsidy_1.yml / subsidy_1_areas.md（大阪市・堺市・豊能・三島 12市町） | 7 |
| govsub_2 | gov_ai_2.md / subsidy_2.yml / subsidy_2_areas.md（北河内・中河内 10市） | 7 |
| govsub_3 | gov_ai_3.md / subsidy_3.yml / subsidy_3_areas.md（南河内 9市町村） | 7 |
| govsub_4 | gov_ai_4.md / subsidy_4.yml / subsidy_4_areas.md（泉北・泉南 12市町） | 7 |
| companies | companies.json / companies.md | 10 |
| outside | cases_outside.md / serp.md | 12 |
| cases2 | cases2.md（補充） | 10 |
| 合計 | | 104 |

## 状態
- [x] _brief.md・wages.md・area_uniq.py に osaka・共有メモに slug（2026-11-14）
- [ ] 調査（10担当）
- [ ] 試算の PLAN（_calc.py）
- [ ] 執筆仕様 docs/area-writing-spec-osaka.md
- [ ] 記事 44本（府1＋市町村43）
- [ ] data/subsidies/osaka.yml・areas.yml・build
- [ ] 地域ガイド・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック（check_article・area_uniq・_calc.py・試算の結果表・書いてはいけない局名）
- [ ] main に push（投稿・デプロイはユーザーが Mac で「投稿して」）

## 再開するとき
- 調査の担当が止まったら、ファイルの続きから書くよう新しい担当に頼む（ファイルは節ごとに書き足してある）
- 書きかけの記事は .git/info/exclude（`articles/2026-11-14-area-osaka*.md`）で未追跡のまま置き、書き終えた分は `bash data/area/osaka/_wip_push.sh` で area-osaka-wip ブランチに退避する（再起動で消えたら `git fetch origin area-osaka-wip && git checkout FETCH_HEAD -- 'articles/2026-11-14-area-osaka*.md'` で戻し、exclude を足し直す）

## 実績メモ
- 2026-11-14 ネットワーク確認（pref.osaka.lg.jp・soumu.go.jp とも WebFetch・curl で開けた）。WebSearch 0回
- 国のデジタル化・AI導入補助金 7次締切 2026-12-01（火）17:00・交付決定 2027-01-19 予定（事務局 schedule を 2026-11-14 に curl で確認。8次は日程なし、複数者連携枠4次 2027-01-07）
- stats（WS14）・cases（WS20）起動
- cases 18（完了: cases.md 446行。**未使用・数値つきの府内6件**: 正幸会病院（門真市56床、退院サマリ 約40分→約4分〔実測〕、月386hは試算、ベンダー ヘンリーの PR TIMES 2026-06-29）・シー・ビィ・エィ（岸和田市の拠点・本社大阪市中央区、化粧品、AI-OCR 1か月で受注の約50%正読、府「大阪デジタル・AI活用促進プロジェクト」〔大阪産業局運営〕）・日本電設資材（守口市218名、年約1,000h は見込み、TOKIUM）・だんらん住宅（大阪市北区、査定書 約1/4、Speee。前の時間が30分と60分で食い違う）・エムケー（門真市、廃棄物収集、受付3→1人は計画、アルパカ）・伸栄商事（大阪市、JAPAN AI、約40h は検索の抜粋だけ verified:false）。公的事例集は AI の数値ほぼ0（obdx 43社中1・ORIST 事例集6年・堺DX推進事例集・大阪ものづくり優良企業賞・MOBIO）。中央会の成果事例集なし。関経連86本の大阪の AI はすべて使用済み。他県で使用: 和田精工・竹中製作所・彩都リハビリ（兵庫川西）・合通カシロジ・進栄化工・旭工精。0件の市町村18、数値つき未使用なしは39/43。繊維・鉄鋼化学・介護・運送・小売飲食宿泊・農業の AI は0件。省力化ナビは 11/16 09:00 までメンテナンス）
- gov（WS10）起動
- stats 4（完了: stats.md 1,244行・stats_labor.md 160行。33市9町1村・町はすべて「ちょう」。**府の統計の地域区分で吹田市は三島、堺市は泉北**。R7国勢調査 8,759,312人（▲0.9%）、高齢化 豊能町51.7%・千早赤阪村49.1%・能勢町47.0%。社人研は 403。大阪市の昼夜間人口比率128.4、大阪市外の府内在住者の22.5%が大阪市で従業（吹田33.7・豊中30.3）、島本町は府外26.0%。製造: 東大阪・八尾の金属製品、堺西区の石油（府の96.7%）、高石の化学（81.2%）、泉州のタオル（全国の事業所の31.8%）・毛布82.1%、**門真は生産用機械51.2%・電機8.7%**。医薬・タオルは市町村×細分類の表なし。農業センサス2025概数・漁業センサス2023。**災害救助法の適用なし**、6/24〜の大雨 床上39・床下68（消防庁第9報）。有効求人倍率 2026-09 受理地別1.12・就業地別0.96、HW16所（大阪東1.92〜池田0.56）、一般事務0.16・介護4.27。最低賃金1,231円（+54、2026-10-01）。TDB 府版は倒産リスク・本社移転・メインバンクだけ→近畿版の大阪の行（後継者不在率46.8%・社長年齢59.9歳〔43位〕・休廃業4,414〔付表4,411〕・生成AI 36.1%）。府内の AI 調査は大阪シティ信金（2024-11、1,262社、デジタル化している373社の1.3%が生成AI）だけ）
- govsub_1（WS7）起動（大阪市・堺市・豊能・三島の12市町）
