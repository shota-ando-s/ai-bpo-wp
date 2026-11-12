# 調査担当への依頼文（北海道の段階5〜。{R}〔振興局名〕・{RK}〔ファイル名のキー〕・{ROLE}〔A か B〕・{WS}〔WebSearch の上限〕・{LIST}〔市町村・コード・slug〕を置き換える）

あなたは北海道の地域ページの調査担当「{RK}-{ROLE}」です。範囲は **{R}の市町村**（下の表）。今日は 2026-11-12。作業場所はリポジトリ `/home/user/ai-bpo-wp/`（ブランチ main）。**git のコミット・push・pull・checkout・stash はしない**（親がする）。一時ファイルは `/tmp/claude-0/-home-user-ai-bpo-wp/39a0019e-d7a6-50c7-b5fc-2f8811464a84/scratchpad/{RK}-{ROLE}/` に置く（ダウンロードしたファイルはその中の新しいフォルダに。Python で読むときは `python3 -I`、スクリプトはダウンロードしたフォルダの外に置く）。

{LIST}

## まず読む
1. `data/area/hokkaido/_brief.md` の「国の出先機関・道の機関」「北海道で特に気をつけること」「形式」「守ること」（**守ることは全部守る**）
2. `data/area/hokkaido/_progress.md` の実績メモ（道全体で分かっていること）
3. **形のお手本は上川のファイル**（同じ名前の `_kamikawa` のもの）。見出しの構成・表の形・出典の書き方を合わせる。上川の値は使わない
4. 道全体の値（TDB の北海道版・最低賃金・道の制度・国の出先機関・総務省の表の読み方）は段階1の stats.md・stats_labor.md・gov_ai.md・subsidy_a.yml にある。**道の値を調べ直さない**

## 担当 A（統計・行政・補助金）: 書くファイル
- `data/area/hokkaido/stats_{RK}.md` — 人口（令和7年国勢調査の確定値・15〜64歳の2020→2025の増減）、令和3年経済センサス（業種構成）、製造業（中分類）、農業産出額、観光入込（令和7年度）、ハローワーク別の有効求人倍率（2026年9月。管轄の市町村も）、市町村ごとの主要産業の候補（根拠つき）。**値は `data/area/hokkaido/_work/stats/` の CSV から**（コードで照合）。農業・観光・労働局の原典は stats.md の「出典一覧」の URL から取り直す（前のセッションの scratchpad は残っていない）
- `data/area/hokkaido/gov_{RK}.md` — 総務省の表の各市町村の行（`_work/govsub/hk.json`）、市町村ごとの DX計画・AI の実証・導入（公式の資料）、商工会議所・商工会（`_work/govsub/hokkaido_meibo.tsv`）、振興局の地域の支援機関（財団・センター）、無料の相談窓口、2026年11月12日以降のセミナー。各市町村の節は `## 市町村名（slug）`
- `data/area/hokkaido/subsidy_{RK}.yml`・`subsidy_{RK}_areas.md` — 市町村・地域の財団の AI・IT・デジタル化・研修に使える独自の制度（2026年度）。yml の形は subsidy_kamikawa.yml と data/subsidies/README.md。受付状況（open/closed/rolling/unknown）、国の補助との併用、上乗せ（addon）の有無。**見つからない市町村は、確かめたページを areas.md に書く**（「ない」と断定しない）
- WebSearch は **{WS}回まで**。自治体のページは WebFetch・curl（ヘッダーを偽らない）で開く

## 担当 B（事例・地元のIT企業・検索）: 書くファイル
- `data/area/hokkaido/cases_{RK}.md` — 振興局の市町村の企業の AI の事例（一次情報。数値つきか、AI の中身、誰の発表か〔ベンダー・支援した側・社長の申告〕）。**他県・北海道の既存ページで使った事例は使わない**（`grep -rn "<社名>" articles/ data/area/` で確かめる）。振興局の産業支援機関・商工会議所・地元の報道・道の事例集・北海道農政事務所・道総研・大学（帯広畜産大学など）の共同研究も探す。自治体・大企業の話は分けて書く。道外の同業種の未使用の事例があれば別の節に（共有メモ data/area/_shutoken/shared.md と data/area/_batch5/shared.md の「事例の割り当て」を見て、他県が確保した事例は使わない）
- `data/area/hokkaido/companies_{RK}.md`・`companies_{RK}.json` — 市町村に**本社**があり、公式サイトでシステム開発・Web開発の事業と従業員数（時点）が確かめられる会社。形は companies_kamikawa.*。支店・営業所だけの会社は入れない
- `data/area/hokkaido/serp_{RK}.md` — 主な市町村の「◯◯市 AI導入」「◯◯町 AI」の検索の上位の状況、競合の弱点、FAQ 候補、地元のセミナー（2026年11月12日以降）。**検索結果から拾った事実は使わない**（FAQ の質問文だけ）
- WebSearch は **{WS}回まで**

## 報告（最後に10行以内）
主な発見、見つからなかったもの、使った WebSearch の回数、執筆で気をつけること（取り違えやすい地名・郡名、書いてはいけないもの）、他の担当・他県と照らしたいこと。
