# 熊本県 執筆担当への依頼（共通）

あなたは hikitsugi.jp の熊本県の地域ページの執筆担当 **{W}** です。担当のページ: **{PAGES}**。

## 作業場所と読むもの
- リポジトリ `/home/user/ai-bpo-wp/`（ブランチ main。クラウドのセッション）。今日は 2026-11-04
- **執筆仕様 `docs/area-writing-spec-kumamoto.md` を最初から最後まで読む**（【D1】〜【D5】の担当ページの行を必ず見る。主要産業・試算の割り当て・事例の割り当て・行政・補助金・地元IT企業・災害・近隣リンク）
- 仕様の「必ず読むもの」とデータ（data/area/kumamoto/）。試算は `data/area/kumamoto/_calc.py` の PLAN の担当ページの行
- 保存先は `articles/2026-11-04-area-kumamoto-<slug>.md`

## 守ること
- 書くのは担当のファイルだけ。**git の操作（commit・push・pull・checkout・stash）はしない**（親がする）
- 自分の担当ページ同士でも、書き終わったほかの担当のページ（`ls articles/2026-11-04-area-kumamoto-*.md`）とも、段落・表・試算の説明・FAQ・組み立てを使い回さない。国の制度の表・相談先の表・試算の説明・FAQの回答も書き分ける。お手本は形だけを見て文は写さない
- 試算は【D1】の割り当て（_calc.py の PLAN）のとおり。変えない。計算は python で確かめ、結果表に2行の中身を必ず入れる
- 仕様の「見つからない」「確認できなかった」は、一次資料を開いて違えば直してよい（報告に書く）
- 仕様が名指ししたページ以外では、他県で詳述した事例・企業に触れない
- 令和8年熊本地震などの災害は【D1】【D4】が名指ししたページだけに、事実と時点だけを書く。評価・応援の言葉は書かない。災害とAIを結び付けない
- データにない数値・事実は書かない。足すときは一次情報を WebFetch / curl（ヘッダーを偽らない）で開いて確かめ、出典リンクを付ける。**WebSearch は合計2回まで、できれば0回**
- 地図の画像・地図の説明は書かない

## 書き終えたら（各ページ）
```bash
cd /home/user/ai-bpo-wp
python3 .claude/skills/seo-article/scripts/check_article.py articles/<file>.md --kw "<市町村名> AI導入"
python3 .claude/skills/fact-check/scripts/extract_claims.py articles/<file>.md --check-links
python3 -B scripts/area_uniq.py kumamoto <自分のslug…>
```
ERROR 0、固有60%以上になるまで直す（仕様の「書き終えたら」）。リンク確認の ERROR は、curl で切断・404・403 になる県・市町村のサイトを WebFetch で開けるか確かめ、開ければよい（報告に書く）。

## 報告（15行以内）
ページごとに「文字数・固有率・試算の結果（月の時間・金額）・check の ERROR 数」、仕様と違ったこと（直した事実と出典）、開けなかったリンク、使った WebSearch の回数。
