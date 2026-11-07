# 滋賀県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-07。WebSearch はセッションで200回まで（調査は105回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（奈良・和歌山〔と北海道〕を別々のセッションで同時に作っている）。

滋賀県だけのファイル（data/area/shiga/、docs/area-writing-spec-shiga.md、articles/*-area-shiga*.md）は自由に作る。`data/subsidies/shiga.yml` は areas.yml の滋賀県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_kinki/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町と slug（19市町。県コード25）
- 一覧は data/area/shiga/_brief.md
- 草津市 `kusatsu-city`（群馬県草津町が kusatsu）、日野町 `hino-town-shiga`（鳥取県日野町が hino）、湖南市 `konan-shiga`（高知県香南市が konan）
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を3で割った余りが2の時間だけ**（_kinki/shared.md。0.5, 1.25, 2.0, … の0.75時間刻み）。全県の記事・全県の _calc.py の PLAN と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 25 |
| gov | gov_ai.md（県・13市・国の出先機関・総務省表の全19行） | 14 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・13市） | 12 |
| choson | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（6町） | 8 |
| companies | companies.json / companies.md | 10 |
| outside | cases_outside.md / serp.md | 15 |
| 合計 | | 98 |

## 状態
- [x] _brief.md・wages.md・area_uniq.py に shiga（2026-11-07）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-shiga.md
- [ ] 記事 20本（県1＋市町19）
- [ ] data/subsidies/shiga.yml・areas.yml・build
- [ ] 地域ガイド（近畿の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-07 ネットワーク確認（pref.shiga.lg.jp・soumu.go.jp とも開けた）。ローカルが detached だったので `git checkout -B main origin/main`
- cases 22（完了: cases.md 138行。**県内の中小企業で AI の効果の数値が一次情報にあって他県で未使用の事例は0件**（産業支援プラザの成果報告58本の AI の数値は富山・岩手などで使用済み。青祥会・湯元舘・フクハラファーム・能勢鋼材も使用済み）。新規・数値なし: 県「ものづくりAIパイロット事業」の5社（2026-08-21 決定。ハヤミ工産・原馬化成〔長浜市〕・江州計器工業〔大津市〕・廣瀬バルブ工業〔彦根市〕・日光精器〔登記は大阪府枚方市〕、成果未公表）、県のデジタル化取組事例5（草津商工会議所が支援した警備会社の AI 交通誘導、社名・数値なし）、プラザ R7 成果報告（Auto-IDフロンティア〔守山市〕・ワボウ電子〔長浜市〕）、作る側（MotorAI〔草津市〕・アヤハエンジニアリング）、大企業 ダイハツ竜王工場の AI 検査（報道、会社名なし1文）。見つからない: 運輸・農業・漁業・介護・医療・建設・宿泊・伝統産業。**工業技術総合センターのサイトは 502/DNS で開けない**。県のサイトは 2026-09-07 にリニューアル、古い /ippan/ の URL は一部404）
