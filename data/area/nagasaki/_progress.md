# 長崎県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション。main の e82e897 の次から）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-04。WebSearch は調査で110回まで。post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」）。**九州7県を別セッションで同時に作っている**。サブエージェントの同時起動は2人まで。

長崎県だけのファイル（data/area/nagasaki/、docs/area-writing-spec-nagasaki.md、articles/*-area-nagasaki*.md、data/subsidies/nagasaki.yml）は自由に作る。`data/subsidies/nagasaki.yml` は areas.yml の長崎県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、data/area/_kyushu/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町と slug（21市町。県コード42）
- 一覧は data/area/nagasaki/_brief.md。長崎市 `nagasaki-city`
- 試算: 月の削減時間×4 を7で割った余りが2の時間だけ。全県の記事・全県の _calc.py の PLAN（九州の他県も）と照合
- scripts/area_uniq.py の県の選択肢に nagasaki を足す（未コミット。共通ファイルと一緒に最後にコミット）

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 25 |
| gov | gov_ai.md | 20 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md | 18 |
| companies | companies.json / companies.md | 12 |
| cases_outside・serp | cases_outside.md / serp.md | 15 |
| 合計 | | 104 |

## 状態
- [x] _brief.md・wages.md（2026-11-04）
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-nagasaki.md
- [ ] 記事 22本（県1＋市町21）
- [ ] data/subsidies/nagasaki.yml・areas.yml・build
- [ ] 地域ガイド（九州地方の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-04 ネットワーク確認（pref.nagasaki.jp・soumu.go.jp とも curl 200）。slug 21個は既存と重ならない
- cases 25（完了: cases.md。数値つき3件〔橋梁診断の実証 約57%＝県・大村市、南島原スマート農業研究会 アスパラのAIプレ選別 24→4.3分/kg、ジャパネットHD 年約2,400h（大企業）〕。県内中小企業の自社の実績は0件。数値なし: みんなシステムズ×ムラセ、クラスタス×白洋社、西海市商工会・佐世保市北部商工会のAI-OCR、滲透工業。使用済み: ホテル長崎〔高知県四万十市〕・かとりストアー〔山形県三川町〕・柑橘2部会〔山口〕・窯業技術センター〔岐阜県瑞浪市〕。事例なし: 諫早・平戸・対馬・壱岐、東彼杵・川棚・小値賀・佐々・新上五島。橋梁診断は shared.md の事例の割り当てに書いた）
- gov 起動（WS20）
