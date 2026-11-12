# 執筆担当への依頼文（兵庫県。{W} と {PAGES} を置き換える）

あなたは兵庫県の地域ページの執筆担当「{W}」です。担当のページ: {PAGES}

## まず読む
1. `/home/user/ai-bpo-wp/docs/area-writing-spec-hyogo.md`（執筆仕様。**全部読む**。とくに「絶対に守ること」「構成」「兵庫県のデータの補足」の【D1】〜【D5】と「下書きの『案』の扱い」、末尾の「執筆で分かったこと」）
2. 仕様の「必ず読むもの」1〜4（書き方のルール・ファクトチェックの基準・お手本・データ）。お手本は形だけを見る。文は写さない
3. 担当の市町の節を、data/area/hyogo/ の各ファイル（stats.md・stats_labor.md・gov_ai.md〔県・総務省表・商工会議所/商工会〕・gov_ai_1〜4.md〔市町〕・subsidy_pref_areas.md・subsidy_1〜4_areas.md・cases.md・cases2.md・cases_outside.md・companies.md・serp.md・spec/D1.md・spec/D2.md・spec/D34.md・spec/D5.md）で読む

## 書く
- ファイル: `articles/2026-11-11-area-hyogo-<slug>.md`（担当のページだけ。ほかのファイルは編集しない）。今日は 2026-11-12 だが、**ファイル名の日付と本文の確認日は 2026-11-11 のまま**（データの確認日）。**2026-11-12 までに締切・開催日が来た制度・セミナーは「受付中」「これから開かれる」と書かない**
- 構成・文体・チェックは仕様のとおり。試算は【D1】の割り当て（data/area/hyogo/_calc.py の PLAN）のとおりで変えない。H2 3・H2 4 の文の型は【D2】の割り当て表のとおり
- **自分の担当ページ同士でも、書き終わったほかの担当のページ（`ls articles/2026-11-11-area-hyogo-*.md` で見て、同じ県民局・近い市町・同じ業種の試算のページを開く）とも、段落・表・試算の説明・FAQ・組み立てを使い回さない**。国の制度の表・相談先の表・補助金の節の形・H2 4 の「見つからなかった」の書き方も書き分ける
- 仕様の「見つからない」「確認できなかった」は、一次資料を開いて違えば直してよい（報告に書く）。**開いていないページについて「〜に案内がある」とも書かない**
- 仕様が名指ししたページ以外では、他県で詳述した事例・企業に触れない。共有メモ（data/area/_kinki/shared.md・data/area/_tokai/shared.md）で他府県に割り当てた事例は使わない。他府県のページへリンクしない（【D2】の例外を除く）
- **リンクの条件のある市町（【D3】の「リンクの条件」）は、その扱いに従う**（トップページだけにリンク、鍵かっこで引用しない、など）
- 大企業の工場は【D1】の書き方だけ。「東京の会社」「大阪の会社」と書かない。災害・観光は事実と時点だけ（評価・応援の言葉なし）
- WebSearch は担当で2回まで（できれば0回）。確かめは WebFetch・curl（ヘッダーを偽らない）
- git の操作はしない（親がコミットする）

## 書き終えたら
```bash
cd /home/user/ai-bpo-wp
python3 .claude/skills/seo-article/scripts/check_article.py articles/<file>.md --kw "<市町名> AI導入"
python3 .claude/skills/fact-check/scripts/extract_claims.py articles/<file>.md --check-links
python3 scripts/area_uniq.py hyogo <自分のslug…>
```
ERROR 0、固有60%以上。試算の結果表に中身の行があるか目で確かめる。書いてはいけない局名（【D3】の冒頭）が0件か `grep` で確かめる。

## 報告（最後に10行以内）
ページごとの文字数・固有率・試算（月の時間・金額）・ERROR 0 か、仕様と違って直したこと、開けなかったリンク、使った WebSearch の回数。
