# 栃木県 地域ページ 作業状態（再開用）

ブランチ: main（クラウドのセッション）。作業場所は `/home/user/ai-bpo-wp/`。ファイル名の日付と本文の確認日は 2026-11-05。WebSearch はセッションで200回まで（調査は110回までにする）。このセッションでは post.py・deploy.sh・post_changed.py は実行しない（投稿はユーザーが Mac で「投稿して」と言って行う）。**サブエージェントの同時起動は2人まで**（北海道・北関東3県・沖縄を同時に作っている。アカウントの7日間の利用上限が警告の状態）。

栃木県だけのファイル（data/area/tochigi/、docs/area-writing-spec-tochigi.md、articles/*-area-tochigi*.md）は自由に作る。`data/subsidies/tochigi.yml` は areas.yml の栃木県の行と同じコミットで push する。共通ファイル（areas.yml、地域ガイド、area_uniq.py、area-todo.md、area-new-prefecture.md、memory、subsidies.json、_batch5/shared.md）は直す直前に `git pull --rebase origin main`。force push はしない。書きかけの記事は main に入れない。

## 市町と slug（25市町。県コード09）
- 一覧は data/area/tochigi/_brief.md
- 栃木市 `tochigi-city`、那珂川町 `nakagawa-town`
- 試算は「月の削減時間・時間換算額」だけの形。**月の削減時間×4 を5で割った余りが2の時間だけ**（_batch5/shared.md）。全県の記事・全県の _calc.py の PLAN と照合する

## 調査の分担と WebSearch の配分
| 担当 | 書くファイル | WebSearch |
|---|---|---|
| stats | stats.md / stats_labor.md | 14 |
| cases | cases.md | 25 |
| gov | gov_ai.md（県・14市・国の出先機関・総務省表の全25行） | 14 |
| subsidy | subsidy_a.yml / subsidy_a_areas.md（県・14市） | 12 |
| choson | gov_ai_b.md / subsidy_b.yml / subsidy_b_areas.md（11町） | 12 |
| companies | companies.json / companies.md | 10 |
| outside | cases_outside.md / serp.md | 15 |
| 合計 | | 102 |

## 状態
- [x] _brief.md・wages.md（2026-11-05）・area_uniq.py に tochigi
- [ ] 調査
- [ ] 執筆仕様 docs/area-writing-spec-tochigi.md
- [ ] 記事 26本（県1＋市町25）
- [ ] data/subsidies/tochigi.yml・areas.yml・build
- [ ] 地域ガイド（北関東の段）・area-todo.md・area-new-prefecture.md・memory
- [ ] チェック
- [ ] main に push

## 実績メモ
- 2026-11-05 ネットワーク確認（pref.tochigi.lg.jp・soumu.go.jp とも開けた）。ローカルが detached だったので `git checkout -B main origin/main`
- 2026-11-06 コンテナの再起動で stats・cases が止まった（ファイル0行）→ SendMessage で再開
- cases 22（完了: cases.md 299行。**新しい出典: 県 産業政策課の事例集**〔産業データ共有・利活用PF R5・R6、未来技術企業実証 R5・R6、社会実装 R7。f01/2026miraigizyutu.html〕・**とちぎビジネスAIセンター**〔県設置、運営 公益財団法人栃木県産業振興センター。事例5件〕・県工業振興課のスマートファクトリー実証（R7）・ものづくり革新技術導入実証（R8）の交付決定と成果発表会。数値つき（所在は法人番号で確認、他県で未使用）: トチシュー〔鹿沼市、木材加工、AI画像検査で目視 16h→12h/日・不良率3→2.5%、2023-11〜2024-02 実績。月50万円は想定〕・アップデート〔宇都宮市、IT。日光市の自販機の AI カメラで客層分析→デザイン変更で注目率39→64%、効果はデザイン〕・吉澤石灰工業〔佐野市238名、キルン部品の劣化 AI 画像診断 検知率80%超〕・那須赤十字病院〔大田原市、生成AIの退院サマリ カバー率52.8%、年3,168.6h は試算〕・フォーカス〔宇都宮市、ベンダー自社の工数1件1,020分減〕。実証・採択のみ: オプトニクス精密・藤成測量・下野新聞社×デジタル・ナレッジ・晃和・竹中・明治鋼業（本社東京）・大和鋼管工業・轟・宇大農場・県農試のいちご病害虫AI。**正式名は「公益財団法人栃木県産業振興センター」**。見つからない: 建設・運輸・宿泊・介護・いちご以外の農業・伝統産業・自動車部品の下請け。**栃木県産業技術センターのサイトは2日とも接続できず**、関東経産局403。照合: 県の指標「AI等を導入する事業所の割合 R4 19.5%→R7末 30.0%」の原典（gov/stats）、フォーカス・アップデート・下野新聞（companies）、宇大農場の所在）
