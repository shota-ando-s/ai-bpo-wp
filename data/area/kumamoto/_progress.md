# 熊本県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-04。WebSearch はセッション全体で200回まで（調査は120回まで）。サブエージェントの同時起動は2人まで（九州7県を同時に作っているため）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。

九州7県を別々のセッションで同時に作っている。共有メモは `data/area/_kyushu/shared.md`。試算の時間は「月の削減時間×4 を7で割った余りが 3」だけを使う。金額が九州の他県と重なったら、先に PLAN を push した県を優先する。

熊本県だけのファイル（data/area/kumamoto/、docs/area-writing-spec-kumamoto.md、articles/*-area-kumamoto*.md、data/subsidies/kumamoto.yml）は自由に作る。`data/subsidies/kumamoto.yml` は areas.yml の熊本県の行と同じコミットで push する。共通ファイルは直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町村と slug（45市町村。県コード43）
- 一覧は data/area/kumamoto/_brief.md
- 熊本市 `kumamoto-city`（区のページは作らない）、美里町 `misato-town-kumamoto`、嘉島町 `kashima-town`（佐賀県鹿島市 `kashima`）、大津町 `ozu`（愛媛県大洲市と同じ）、高森町 `takamori`（長野県高森町と同じ）、小国町 `oguni`（山形県小国町は `oguni-town`）
- scripts/area_uniq.py の県の選択肢に kumamoto を足した（push 済み 629a105）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 26 |
| gov | gov_ai.md | 22 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md / subsidy_b.yml / subsidy_b_areas.md | 22 |
| companies | companies.json / companies.md | 14 |
| cases_outside・serp | cases_outside.md / serp.md | 16 |
| 合計 | | 114 |

## 状態
- [x] _brief.md・wages.md（2026-11-04）、shared.md に slug
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-kumamoto.md
- [ ] 記事 46本（県1＋市町村45）
- [ ] data/subsidies/kumamoto.yml・areas.yml・build
- [ ] 地域ガイド（九州地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-04 ネットワーク確認（pref.kumamoto.jp・soumu.go.jp とも開けた）。WebSearch 1回（市町村数の確認）。stats・cases を起動
- cases 26（完了: cases.md。**事業者が自ら実績を公表した県内の中小企業の数値つき事例は0件**。数値つきは自己申告・ベンダー・見出しのみ: さくら優和パートナーズ〔熊本市西区、税理士、156名、ChatGPT研修で最大6h/人月、熊日のスポンサード記事・RPA等と混在〕・プロセスコア〔中央区、社労士、デジライズ、コラム1/4〕・未来創造学園〔中央区、学校法人、デジライズ、メール約70%〕・しょうぶ苑〔見守りAI「転倒30%減」は有料記事の見出しだけ、運営法人を特定できず〕・熊本中央病院〔361床、ispec、病棟残業約70%減〕・天草市〔行政の営農状況AI判定 737→194h/年、県DX会議資料 2023-02〕。数値なし: 福田屋〔北区、菓子、75名、AI画像検査、有料記事〕・肥後銀行。熊本市外の企業の数値つき事例なし。建設・運輸・宿泊・焼酎・い草・水産なし。九州農政局の事例集の熊本2件はAIなし。**くまもと産業支援財団 www.kmt-ia.or.jp はこのセッションから名前解決できない**。九経局403。**高知市の記事のロッキーの所在「熊本県益城町」は法人番号の本店（熊本市北区植木町）・プレスリリース「上益城郡」と食い違う → area-todo**。shared.md に事例4件・資料3行を足した）
- gov（WS22）起動
