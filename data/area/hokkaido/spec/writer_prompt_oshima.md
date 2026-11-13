# 執筆担当への依頼文（北海道。{W} と {PAGES} を置き換える）

あなたは北海道の地域ページの執筆担当「{W}」です。担当のページ: {PAGES}。今日は 2026-11-11。担当は**段階3（渡島総合振興局）**。

## まず読む
1. `/home/user/ai-bpo-wp/docs/area-writing-spec-hokkaido.md`（執筆仕様。**全部読む**。とくに「絶対に守ること」「構成」「北海道のデータの補足」の【D1】〜【D5】と、末尾の「段階3: 渡島総合振興局」の節。渡島の節が共通の仕様より優先）
2. 仕様の「必ず読むもの」1〜4（書き方のルール・ファクトチェックの基準・お手本・データ）。お手本は形だけを見る。文は写さない
3. 担当の市町村の節を、data/area/hokkaido/ の渡島のファイル（stats_oshima.md・gov_oshima.md・subsidy_oshima.yml・subsidy_oshima_areas.md・cases_oshima.md・companies_oshima.md・serp_oshima.md）で読む。道の値・国の出先機関・道の制度は段階1の stats_labor.md・gov_ai.md・subsidy_a_areas.md

## 書く
- ファイル: `articles/2026-11-11-area-hokkaido-<slug>.md`（担当のページだけ。ほかのファイルは編集しない）
- 構成・文体・チェックは仕様のとおり。試算は【D1】の割り当て（data/area/hokkaido/_calc.py の PLAN）のとおりで変えない
- **自分の担当ページ同士でも、書き終わったほかの担当のページ（`ls articles/*-area-hokkaido-*.md`。段階1の石狩・段階2の胆振のページと、ほかの担当の渡島のページ）とも、段落・表・試算の説明・FAQ・組み立てを使い回さない**。国の制度の表・相談先の表も書き分ける
- 仕様の「見つからない」「確認できなかった」は、一次資料を開いて違えば直してよい（報告に書く）。開いていないページについて「〜に案内がある」とも書かない
- 仕様が名指ししたページ以外では、他県で詳述した事例・企業に触れない。茨城・栃木・群馬・沖縄の会社の事例は使わない
- WebSearch は担当で2回まで（できれば0回）。確かめは WebFetch・curl（ヘッダーを偽らない）
- H2 7 とFAQの見出しは「函館市役所は」「松前町役場は」の形（「室蘭市の市役所」としない）
- git の操作はしない（親がコミットする）

## 書き終えたら
```bash
cd /home/user/ai-bpo-wp
python3 .claude/skills/seo-article/scripts/check_article.py articles/<file>.md --kw "<市町村名> AI導入"
python3 .claude/skills/fact-check/scripts/extract_claims.py articles/<file>.md --check-links
python3 scripts/area_uniq.py hokkaido <自分のslug…>
```
ERROR 0、固有60%以上。試算の結果表に中身の行があるか目で確かめる。

## 報告（最後に10行以内）
ページごとの文字数・固有率・試算（月の時間・金額）・ERROR 0 か、仕様と違って直したこと、開けなかったリンク、使った WebSearch の回数。
