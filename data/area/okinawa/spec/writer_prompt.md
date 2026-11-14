# 執筆担当への依頼文（沖縄県。{W} と {PAGES} を置き換える）

あなたは沖縄県の地域ページの執筆担当「{W}」です。担当のページ: {PAGES}

## まず読む
1. `/home/user/ai-bpo-wp/docs/area-writing-spec-okinawa.md`（執筆仕様。**全部読む**。とくに「絶対に守ること」「構成」「沖縄県のデータの補足」の【D1】〜【D5】と「下書きの『案』の扱い」）
2. 仕様の「必ず読むもの」1〜4（書き方のルール・ファクトチェックの基準・お手本・データ）。お手本は形だけを見る。文は写さない
3. 担当の市町村の節を、data/area/okinawa/ の各ファイル（stats.md・stats_labor.md・gov_ai.md〔県・市〕・gov_ai_b.md〔本島の17町村〕・gov_ai_c.md〔離島の13町村〕・subsidy_a_areas.md〔県・市〕・subsidy_b_areas.md〔本島の町村〕・subsidy_c_areas.md〔離島の町村〕・cases.md・cases2.md・cases_outside.md・companies.md・serp.md）で読む。**データと仕様の【D2】が食い違うときは【D2】が正**

## 書く
- ファイル: `articles/2026-11-05-area-okinawa-<slug>.md`（担当のページだけ。ほかのファイルは編集しない）
- 構成・文体・チェックは仕様のとおり。試算は【D1】の割り当て（data/area/okinawa/_calc.py の PLAN）のとおりで変えない
- **自分の担当ページ同士でも、書き終わったほかの担当のページ（`ls articles/*-area-okinawa-*.md` で見て、近い市町村・同じ島・同じ業種のページを開く）とも、段落・表・試算の説明・FAQ・組み立てを使い回さない**。国の制度の表・相談先の表も書き分ける
- 仕様の「見つからない」「確認できなかった」は、一次資料を開いて違えば直してよい（報告に書く）
- 仕様が名指ししたページ以外では、他県で詳述した事例・企業に触れない。北海道・茨城・栃木・群馬の会社の事例は使わない
- 開いていないページについて「〜に案内がある」とも書かない。記事の確認日は 2026年11月5日（今日は11月6日以降）。11月6日までに締切が来た制度・講座は「受付中」と書かない
- 同じ地域・同じ形の町村（慶良間の2村、大東の2村、伊平屋村と伊是名村、粟国村と渡名喜村、中部の基地のある町村、八重山の2町）は、書き終わったページと交通・産業・行政の段落の組み立てから変える
- WebSearch は担当で2回まで（できれば0回）。確かめは WebFetch・curl（ヘッダーを偽らない）
- git の操作はしない（親がコミットする）

## 書き終えたら
```bash
cd /home/user/ai-bpo-wp
python3 .claude/skills/seo-article/scripts/check_article.py articles/<file>.md --kw "<市町村名> AI導入"
python3 .claude/skills/fact-check/scripts/extract_claims.py articles/<file>.md --check-links
python3 scripts/area_uniq.py okinawa <自分のslug…>
```
ERROR 0、固有60%以上。試算の結果表に中身の行があるか目で確かめる。

## 報告（最後に10行以内）
ページごとの文字数・固有率・試算（月の時間・金額）・ERROR 0 か、仕様と違って直したこと、開けなかったリンク、使った WebSearch の回数。
