# 京都府 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-11。WebSearch はセッションで200回まで（調査は106回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（静岡・愛知・三重〔と北海道〕を別々のセッションで同時に作っている）。

京都府だけのファイル（data/area/kyoto/、docs/area-writing-spec-kyoto.md、articles/*-area-kyoto*.md）は自由に作る。`data/subsidies/kyoto.yml` は areas.yml の京都府の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_kinki/shared.md、_tokai/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。**書きかけの記事は全ページそろうまで main に入れない**（滋賀と同じ。途中で「投稿して」と言われると親ページなしで子ページが出る）。

## 市町村と slug（26市町村。府コード26）
- 一覧は data/area/kyoto/_brief.md。府は `kyoto`、京都市は `kyoto-city`（区のページは作らない）
- 既存の slug（1,170本）と衝突なし（2026-11-11 に grep で確認）
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を4で割った余りが3（端数 .75）の時間だけ**（_tokai/shared.md）。全県の記事・全県の _calc.py の PLAN と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 25 |
| gov | gov_ai.md（府・15市・国の出先機関・総務省表の全26行） | 14 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（府・15市） | 12 |
| choson | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（10町1村） | 10 |
| companies | companies.json / companies.md | 10 |
| outside | cases_outside.md / serp.md | 15 |
| 予備（cases2 など） | | 6 |
| 合計 | | 106 |

## 状態
- [x] ネットワーク確認（pref.kyoto.jp・soumu.go.jp とも WebFetch で開けた。2026-11-11）
- [x] _brief.md・wages.md
- [ ] area_uniq.py に kyoto
- [ ] 調査
- [ ] _calc.py の PLAN（push）
- [ ] 執筆仕様 docs/area-writing-spec-kyoto.md
- [ ] 記事 27本（府1＋市町村26）
- [ ] data/subsidies/kyoto.yml・areas.yml・build
- [ ] 地域ガイド（近畿の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-11 ネットワーク確認・_brief.md・_calc.py の枠・area_uniq.py に kyoto（push）。共有メモに kyoto の slug
- stats 6（完了: 26市町村コードは依頼どおり。府2,500,173人〔2020年から▲3.0%〕。府の推計人口は令和7年国調で置き換え済み。製造品出荷額6兆3,929億円・京都市43.7%。細分類（当社で並べて）和装製品・織物手加工染色整理は全国1位、清酒・製茶・絹織物3位。宇治田原町の製造業54.3%は府内最高。有効求人倍率1.21倍（2026-09）、宮津2.13〜木津0.71、一般事務0.28倍。最低賃金1,180円（11-16 発効）。TDB 京都府版: 後継者不在率44.8%・社長年齢60.9歳・休廃業1,259件、生成AIは近畿版の京都37.1%。地域は府の推計人口の参考の地域（丹後・中丹・南丹・京都市域・山城）。2026年の災害救助法の適用なし）
- 親: PLAN（26行、月231.75〜372.75時間・約76.0〜148.6万円・35〜128名、端数 .75）を _assign.py で決めて push。**端数 .75 で月230時間未満は空きがほぼない**（4h が素数の値しか残らない）ので、小さい町村は規模を上げた（伊根町35名・笠置町37名など。「府内の同じ業種の事業所の例」と書く）。1人の月の業務量40時間超が7ページ
- cases 19（完了: cases.md 333行。府内で未使用・数値つき4件: 伊東板金工業〔京都市南区88人、AI でプログラムを作る曲げ機、総リードタイム59.4%減は機械全体〕、京都電機器〔宇治市235名、AI 外観検査「10分の1くらい」は検証段階の見込み、JBCC の事例〕、HILLTOP〔宇治市123人、55.4%改善、AI と明記なし〕、井上株式会社〔福知山市、ブドウの摘粒 AI、実証 36→24秒、2021〕。中央会の成果事例集7冊・府の京都企業紹介395社・府の建設DX好事例31本・京都市/ASTEM の AI・ロボティクス PoC 補助金 R8 採択6社。使用済み: 月桂冠・FUKUDA・蘇生会・最中屋・CRAFT BANK・サンフーズジャパン・アイニコ。北部・山城南部の町村は事例なし）
- gov・subsidy 起動
