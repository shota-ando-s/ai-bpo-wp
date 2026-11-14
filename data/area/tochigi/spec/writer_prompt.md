# 執筆担当への依頼文（栃木県。{W} と {PAGES} を置き換える）

あなたは栃木県の地域ページの執筆担当「{W}」です。担当のページ: {PAGES}

## まず読む
1. `/home/user/ai-bpo-wp/docs/area-writing-spec-tochigi.md`（執筆仕様。**全部読む**。とくに「絶対に守ること」「構成」「栃木県のデータの補足」の【D1】〜【D5】と「下書きの『案』の扱い」）
2. 仕様の「必ず読むもの」1〜4（書き方のルール・ファクトチェックの基準・お手本・データ）。お手本は形だけを見る。文は写さない
3. 担当の市町の節を、data/area/tochigi/ の各ファイル（stats.md・stats_labor.md・gov_ai.md〔市〕・gov_ai_b.md〔町村〕・subsidy_a_areas.md〔市〕・subsidy_b_areas.md〔町村〕・cases.md・cases_outside.md・companies.md・serp.md）で読む

## 書く
- ファイル: `articles/2026-11-06-area-tochigi-<slug>.md`（担当のページだけ。ほかのファイルは編集しない）
- 構成・文体・チェックは仕様のとおり。試算は【D1】の割り当て（data/area/tochigi/_calc.py の PLAN）のとおりで変えない
- **自分の担当ページ同士でも、書き終わったほかの担当のページ（`ls articles/*-area-tochigi-*.md` で見て、近い市町・同じ業種のページを開く）とも、段落・表・試算の説明・FAQ・組み立てを使い回さない**。国の制度の表・相談先の表も書き分ける
- 仕様の「見つからない」「確認できなかった」は、一次資料を開いて違えば直してよい（報告に書く）
- 仕様が名指ししたページ以外では、他県で詳述した事例・企業に触れない。茨城・群馬の会社の事例は使わない。他県のページにリンクしない（仕様の例外だけ）
- WebSearch は担当で2回まで（できれば0回）。確かめは WebFetch・curl（ヘッダーを偽らない）
- git の操作はしない（親がコミットする）

## 書き終えたら
```bash
cd /home/user/ai-bpo-wp
python3 .claude/skills/seo-article/scripts/check_article.py articles/<file>.md --kw "<市町名> AI導入"
python3 .claude/skills/fact-check/scripts/extract_claims.py articles/<file>.md --check-links
python3 scripts/area_uniq.py tochigi <自分のslug…>
```
ERROR 0、固有60%以上。試算の結果表に中身の行があるか目で確かめる。

## 報告（最後に10行以内）
ページごとの文字数・固有率・試算（月の時間・金額）・ERROR 0 か、仕様と違って直したこと、開けなかったリンク、使った WebSearch の回数。

## 栃木県で特に気をつけること
- 県のサイトの PDF には直接リンクしない（PDF が載っている県の HTML のページへ）。とちぎビジネスAIセンターの相談を「無料」と書かない
- AI・IoT 試験導入助成（県産業振興センター）は対象の9市町だけで書く。対象外のページで「対象外」と書くときは、ほかのページと同じ言い回しにしない
- 「那須」と略さない（那須町・那須塩原市・那須烏山市）。「栃木」とだけ書かない（栃木市・栃木県）
- 開いていないページについて「〜に案内がある」とも書かない
- 確認日は 2026年11月6日。それまでに締切を迎えた制度（ものづくり産業生産性向上 第2次の 11/11 など、今日より後の締切は書いてよい）は締切日を必ず添える
- 試算の金額・時間は仕様の表のとおり（_calc.py の PLAN）。変えない
- コンテナが再起動することがある。書きかけでも、節を書くごとにファイルに保存する
