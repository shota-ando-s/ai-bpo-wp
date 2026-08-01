# Handoff: ヒキツギAI ランディングページ

> **このドキュメントについて（2026-08-01 追記）**
>
> Claude Design が出力したデザイン仕様書。元は `_ai_lp/README.md` として
> HTMLプロトタイプ・スクリーンショットと一緒に受け取ったもので、
> **実装完了後にこの仕様書だけを残した**（プロトタイプ一式は削除済み）。
>
> 実装先：
> - マークアップ … `themes/generatepress-child/lp/lp-markup.php`
> - CSS … `themes/generatepress-child/assets/lp.css`（手書き。ビルド不要）
> - 画像 … `themes/generatepress-child/images/lp/`（旧 `uploads/`）
>
> 以下の本文にある `uploads/…` は `images/lp/…` に、末尾「Files」節の
> `ヒキツギAI LP.dc.html` / `support.js` / `screenshots/` は現存しない。
> **値（色・余白・フォントサイズ・レイアウトの意図）を参照するための資料**として残している。
> LPを改修するときは、ここに書かれた制約（使わない語・煽り演出の禁止・
> 「詰めないこと」と指定された余白など）を先に読むこと。

## Overview

BtoB SaaS「ヒキツギAI」（産休・育休・退職時の業務引き継ぎをAIが代行するサービス／運営：株式会社ふえん）のランディングページ。

- **ページのゴール**：業務チェックリストの請求＝商談機会の獲得（SLG型・営業主導）
- **ターゲット**：産休・育休の引き継ぎを控えた中小企業の総務担当者・経営者。ITに詳しくない層
- **販売モデル**：無料トライアル／セルフサーブ登録は存在しない。CTAはすべて資料請求・相談へ

## About the Design Files

このバンドルに含まれるHTMLは **デザインリファレンス（プロトタイプ）** です。意図した見た目と挙動を示すためのもので、そのまま本番コードとして貼り付けるためのものではありません。

実装タスクは、**このHTMLデザインを対象コードベースの既存環境（Next.js / React / Astro / 静的HTML など）で、その環境の確立されたパターン・ライブラリを使って再現すること**です。まだ環境が無い場合は、LPという性質（静的・SEO・表示速度重視）に合うフレームワーク（例：Astro もしくは Next.js の静的出力）を選定して実装してください。

デザインファイルは「Design Component」という独自ランタイム（`support.js`）上で動く形式です。`support.js` 自体は移植不要で、`<x-dc>` 内のマークアップと `<script data-dc-script>` 内のロジック（スクロール連動の2つの状態のみ）を対象環境の書き方に置き換えてください。

**元の要件で明示されていた制約（実装時も維持すること）**

- 「DX」「業務効率化」「生産性向上」「属人化」という語は使わない
- 誇張表現（「必ず」「100%」「業界No.1」など）を使わない
- 導入企業ロゴ・導入社数・「◯%削減」などの実績数値を置かない
- ファーストビューに信頼バッジやアイキャッチ行を追加しない
- スクロールを促す矢印やアニメーションを置かない
- 指定コピーを言い換え・膨らませない

## Fidelity

**High-fidelity（ハイファイ）**。色・タイポグラフィ・余白・インタラクションは確定値です。ピクセル単位で再現してください。ただしフォントサイズ・余白の大半は `clamp()` による流体値であり、固定px値ではありません（下記「Design Tokens」参照）。

## Layout Foundation

- コンテンツ最大幅：`1080px`、中央寄せ
- セクション左右パディング：`clamp(20px, 5vw, 40px)`
- セクション上下パディング：`clamp(56px, 11vw, 112px)`
- 全体は **モバイルファースト**。多カラムは `repeat(auto-fit, minmax(min(100%, Npx), 1fr))` で、幅が足りなくなると自動で縦積みになる
- ルート要素に `overflow-x: clip`
- `text-wrap: pretty`（body）

## Screens / Views

単一ページ。上から順に以下のセクション。

---

### 1. ヘッダー（sticky）

**Purpose**：常時CTAを提示する。

**Layout**：`position: sticky; top: 0; z-index: 40`。内側は `max-width:1080px`、`padding: 14px clamp(20px,5vw,40px)`、`display:flex; justify-content:space-between; align-items:center; gap:16px`。

**背景の2状態（重要な挙動）**
- 初期（ページ最上部）：背景 `#E4EEFB` ＋ ファーストビューと同じ**動くドット柄**（下記アニメーション参照）。透過して見える状態
- スクロール `> 24px`：その上に `rgba(255,255,255,0.8)` ＋ `backdrop-filter: blur(8px)` ＋ 下罫線 `1px solid #DFE7F3` のレイヤーを `opacity` で重ねる。`transition: opacity 220ms ease`

**Components**
- 左：ロゴ画像 `uploads/logo-trim.png`（`alt="ヒキツギAI"`、`height: clamp(21px,5.6vw,30px)`、`max-width: min(48vw,180px)`、`object-fit: contain`）。透明余白をトリム済みのため、コンテンツ左端と光学的に揃う
- 右：テキストリンク「相談する」（`#5A6376` → hover `#333333`、`clamp(12.5px,3.3vw,14.5px)`、`font-weight:500`、リンク先 `#form`）
- 右：ボタン「資料をダウンロードする」（背景 `#0F2961` → hover `#1C4295`、文字 `#FFFFFF`、`clamp(13px,3.4vw,15.5px)`、`font-weight:700`、`border-radius:6px`、`padding:13px 24px`、リンク先 `#materials`）

---

### 2. ファーストビュー（`id="top"`）

**Purpose**：一言で価値を伝え、資料請求へ送る。

**背景**：`linear-gradient(180deg, #E4EEFB 0%, #F1F6FD 52%, #FFFFFF 100%)`。上に装飾レイヤー3つ（下記アニメーション参照）。`position:relative; overflow:hidden`。

**Layout**：`display:flex; flex-wrap:wrap; align-items:center; gap:clamp(32px,6vw,56px)`。
- 左カラム（テキスト）：`flex: 1 1 400px`、`container-type: inline-size`
- 右カラム（画像）：`flex: 1.25 1 420px`
- 縦パディング：`clamp(40px,9vw,88px)` 上 / `clamp(48px,10vw,96px)` 下

**Components**

1. **見出し（h1）** — 2行のベタ塗りボックス。`font-size: clamp(16px, 6cqw, 32px)`（※ビューポート幅ではなく**テキスト列の幅**基準＝コンテナクエリ単位）、`line-height:1.62`、`font-weight:900`、`letter-spacing:-0.01em`
   - 各行は `<span>` に `background:#0F2961; color:#FFFFFF; padding:0.16em 0.26em; box-decoration-break:clone; white-space:nowrap`
   - 1行目：`うまくいかない業務の引き継ぎ、`
   - 2行目：`私たちにお任せください！`
2. **余白** — `height: clamp(48px, 11vw, 88px)` の空div（**断定と解説を視覚的に分離するための最重要の余白**。詰めないこと）
3. **本文** — `font-size: clamp(16px,4.3vw,22px)`、`line-height:1.75`、`font-weight:500`、`color:#333333`
   - 冒頭にロゴ画像 `uploads/logo-hikitsugiai.png`（`alt="ヒキツギAI"`、`height:1.5em`、`vertical-align:-0.35em`）＋ `は`
   - その直後に `display:block` の強調行：`人よりも速く、正確に`（`font-size: clamp(24px, 8.8cqw, 50px)`、`font-weight:900`、`line-height:1.3`、`color:#333333`、`white-space:nowrap`）
   - 続けて `知識と作業を引き継ぎます。`
4. **CTA（縦積み・左寄せ、`gap:16px`）**
   - 主：`無料で業務チェックリストを受け取る`（背景 `#0F2961` → hover `#1C4295`、`clamp(15px,4vw,18px)`、`font-weight:700`、`padding:20px 30px`、`border-radius:6px`、`box-shadow:0 10px 24px rgba(15,41,97,0.24)`、リンク先 `#form`）
   - 副：`または3分でわかる資料をダウンロード`（`#5A6376` → hover `#333333`、`clamp(13px,3.5vw,15px)`、下線 `1px solid #BFCBDE`、`padding-bottom:2px`、リンク先 `#materials`）
5. **メインビジュアル** — `uploads/schreen.png`（`width:100%; height:auto`、枠なし）。alt：`ヒキツギAIが過去のやり取りをもとに質問に答えている画面`

**注意**：見出しと強調行が折り返すと崩れるため `white-space:nowrap` ＋ `cqw` 単位で必ず1行に収める設計になっています。実装時もこの関係を維持してください。

---

### 3. 課題提起（背景 `#EDF3FC`）

**Purpose**：ターゲットの絞り込み。スマホで1スクロール以内に到達させる。

**見出し（h2、中央寄せ）**：`引き継ぎ、こうなっていませんか？`（`clamp(24px,6.4vw,40px)`、`line-height:1.45`、`font-weight:900`）

**Layout**：`grid`、`repeat(auto-fit, minmax(min(100%,280px),1fr))`、`gap:14px`

**カード（6枚）**：背景 `#FFFFFF`、`1px solid #DFE7F3`、`border-radius:8px`、`padding:24px`、`display:flex; gap:14px; align-items:flex-start`
- 左に丸番号：`26×26px`、`border-radius:999px`、背景 `#0C1E3F`、文字 `#FFFFFF`、`13px/700`
- テキスト：`clamp(14px,3.9vw,16px)`、`line-height:1.75`、`font-weight:500`

**コピー（一字一句）**
1. 休職中や退職後の本人に、連絡してしまっている
2. 「前任者しか知らない」取引先の事情がある
3. 過去のやり取りは残っているが、探せない
4. 月次や年次の作業を見落とし、クレームになる
5. 後任の業務が倍になり、組織が疲弊している
6. 引き継ぐ本人が、産休直前まで残業している

---

### 4. 課題→解決の図式（背景 `#FFFFFF`）

**見出し（h2、中央寄せ）**：`休・退職者の引き継ぎ問題は、<br>AIで解決できます。`

**Layout（重要）**：3列 × 3行の grid。親は
```
display:grid;
grid-template-columns: repeat(auto-fit, minmax(min(100%,260px),1fr));
grid-template-rows: auto auto auto;
column-gap: clamp(16px,3vw,20px);
row-gap: 0;
```
各列は `display:grid; grid-row: span 3; grid-template-rows: subgrid; margin-bottom: clamp(16px,3vw,20px)` で **3列の課題カード／矢印帯／解決カードの高さが揃う**。スマホの1列表示でも各ペアは必ず隣接する。

**行1：課題カード**（グレー面）
`border-radius:8px; box-shadow: inset 0 0 0 1px #DCE0E7; background:#EFF1F4; padding:clamp(21px,4.6vw,27px)`、中身は `flex-direction:column; align-items:center; text-align:center; gap:14px`
- アイコン画像（円形、`width: clamp(72px,18vw,92px)`、`border-radius:999px`）
- 見出し：`clamp(15px,4.2vw,18px)/700`、`#333333`
- 本文：`clamp(13px,3.5vw,14.5px)`、`line-height:1.85`、`#5A6376`

| 画像 | 見出し | 本文 |
|---|---|---|
| `uploads/ico-p1.png` | 後任がいない | 後任の人材がいない。採用も派遣も退職日には間に合わない |
| `uploads/ico-p2.png` | 担当者しか知らない | 担当者以外やったことのない作業がたくさんある |
| `uploads/ico-p3.png` | 引き継ぎ書がない | 急な休職や離職により、引き継ぎ書がない |

**行2：スペーサー**（`height: clamp(28px,6vw,44px)`）
中央の列にのみ CSS三角形の下向き矢印を配置（`border-left/right: clamp(12px,3vw,16px) solid transparent; border-top: clamp(13px,3.2vw,17px) solid #0F2961`）。左右の列は空のスペーサー。

**行3：解決カード**（青面）
`border-radius:8px; box-shadow: inset 0 0 0 1.5px #0F2961; background:#DCE8FA; padding:clamp(21px,4.6vw,27px)`
- 上部に小ラベル `ヒキツギAI`（`11px/700`、`letter-spacing:0.12em`、`#0F2961`）
- アイコン画像 → 見出し → 本文（本文色 `#5A6376`）

| 画像 | 見出し | 本文 |
|---|---|---|
| `uploads/icon-solution-1.png` | AI＋人で後任代行 | AIでできるだけ業務を圧縮しつつ、当社のAIパートナーが後任代行としてサポートします。 |
| `uploads/icon-solution-2.png` | ヒアリングとデータで補完 | 担当者へのヒアリング内容と過去のメールやチャットをもとに、明文化されていない業務を再現します。 |
| `uploads/icon-solution-3.png` | AIが引き継ぎ書を作成 | 過去のデータからAIが回答するため、書類を読むことなく質問をするだけです。 |

---

### 5. ヒキツギAIとは（背景 `#E4ECF9`、上下罫線 `1px solid #C9D6EE`）

**見出し（h2、中央寄せ）**：ロゴ画像（`height:1.5em; vertical-align:-0.34em`）＋ `とは`。`clamp(24px,6.4vw,42px)`、`#333333`
**リード（中央寄せ）**：`AIチャットとAI自動化アプリで知識と作業を引き受けます。`（`clamp(14px,3.9vw,17px)`、`line-height:1.85`、`#333333`）

**Layout**：`grid`、`repeat(auto-fit, minmax(min(100%,320px),1fr))`、`gap:clamp(16px,3vw,24px)`

#### 5-1. AIチャット（動くモック）
外枠：`background:#FFFFFF; box-shadow: inset 0 0 0 1px #C9D6EE; border-radius:10px; padding:clamp(20px,4.5vw,28px)`
- タイトル `AIチャット`（`clamp(15px,4.2vw,18px)/700`）／補足 `過去のやり取りをもとに、聞けば答えます。`（`clamp(12.5px,3.4vw,14px)`、`#5A6376`）
- 内側の画面枠：`background:#FFFFFF; box-shadow: inset 0 0 0 1px #DFE7F3; border-radius:8px; padding:14px; overflow:hidden`
- ユーザー吹き出し（右寄せ、`max-width:82%`、背景 `#E8EFFB`、`border-radius:8px`、`padding:9px 12px`、`12px`）：`株式会社ふえんさまとの契約金額の経緯を教えてください。`
- AI側：`24px` の紺円アバター ＋ 回答カラム
  - **入力中インジケーター**：`5px` の円 ×3（`#A9BCE0`）。**`position:absolute` で重ねること**（通常フローに置くと表示・非表示で枠の高さが変わりガタつく）
  - `以下のように整理しました。`（`12px/700`）
  - 箇条書き3行（`11.5px`、`line-height:1.7`、`#5A6376`）
    - `・ご提案（2024年11月下旬）` / `月額のご提案を提示`
    - `・ご調整（2024年12月上旬）` / `支援範囲と支払条件を再相談`
    - `・契約締結（2024年12月15日）` / `翌月よりプロジェクト開始`

#### 5-2. AI自動化アプリ（動くモック）
- タイトル `AI自動化アプリ`／補足 `決めた手順どおりに、毎回自動で実行します。`
- 4ステップを縦に並べ、間を `18px` の縦罫（`1px`、`#BFCBDE`）で接続。各ステップは `background:#EDF3FC; box-shadow: inset 0 0 0 1px #DFE7F3; border-radius:6px; padding:10px 12px`、右端に `16px` の緑丸（`#1F7A4D`）
  1. スプレッドシートに新しい行が追加されたら
  2. 条件で振り分ける（担当部署ごと）
  3. AIが内容を要約する
  4. 担当チャンネルに通知する ← このステップのみ `background:#EDF3FC; box-shadow: inset 0 0 0 1px #A9BCE0`
- 最後に `実行完了 0.8秒`（`11px`、`#79839A`）

---

### 6. サービスの特長（背景 `#FFFFFF`）

**見出し（h2、中央寄せ）**：`サービスの特長`

**Layout**：4ブロックを `gap: clamp(36px,8vw,64px)` で縦に並べる。各ブロックは `grid`、`repeat(auto-fit, minmax(min(100%,300px),1fr))`、`gap:clamp(20px,4vw,40px)`、`align-items:center`。**左にテキスト・右に図解**（スマホでは縦積み）。

各テキスト：h3 `clamp(17px,4.6vw,23px)/900`、`line-height:1.6` ／ 本文 `clamp(14px,3.8vw,16px)`、`line-height:1.95`、`#5A6376`

各図解の共通枠：`border-radius:10px; background:#F4F8FD; box-shadow: inset 0 0 0 1px #D3DDEC; aspect-ratio:16/10; padding:clamp(16px,3.4vw,28px)`（すべてHTML/CSSで描いた図。画像ではない）

| # | 見出し | 本文 | 図解の内容 |
|---|---|---|---|
| 1 | 前任者が使用した業務データをAIデータベースとして保存 | TeamsやSlackなどのビジネスチャットやメール、オフィス文書を一括保存してチャットにします。 | 左に3つの取り込み元カード（ビジネスチャット／メール／オフィス文書、白＋`#D3DDEC`枠、中身はグレーのダミー行）→ 紺の右向き三角 → 右に紺（`#0F2961`）のパネル「AIデータベース」＋青系のバー4本＋`聞けば答えられる状態で保存` |
| 2 | 前任者は打ち合わせをするだけ | 一番面倒で大変なのは、前任者が業務を可視化・構造化して資料にするところ。AIとデータで私たちが可視化します。 | 上：「前任者による資料作成」の白カードに赤（`#B4322A`）の斜め取り消し線＋「不要」バッジ → 罫線＋下向き三角 → 下：「打ち合わせ」「既存データ」の小チップ → 右向き三角 → 紺パネル「AIが業務を可視化」＋バー3本 |
| 3 | 月次や年次の作業も忘れずに実施 | 後任者が忘れがちな期間が空く定常業務もAIが覚えて自動で実行します。 | 「実行カレンダー」＋`AIが自動で実行`。3行（毎月：請求書の発行と送付／四半期：定例レポートの作成／毎年：年次の更新手続き）。前2行は緑丸（`#1F7A4D`）、3行目のみ `inset 0 0 0 1.5px #0F2961` の枠＋紺バッジ＋`3日後`。下に `1年に一度の作業も、期日どおりに実行します` |
| 4 | AIなのに安心の定額制 | 後任者の方が安心して必要なだけ使っていただけます。 | 上「依頼した作業の量」＝右肩上がりの棒6本（`#93AEDD`→`#6C8CC4`→`#3D5786`→`#0F2961`）／下「お支払い」＝同じ高さのバー6本（`#DCE8FA`＋`#A9BCE0`枠）。下に `量が増えても毎月同じ料金です`（`#0F2961`/700） |

---

### 7. 資料ダウンロード（`id="materials"`、背景 `#0F2961` ＝ 唯一の反転面）

- 縦パディング：`clamp(48px,9vw,88px)`。中央寄せ
- h2 `特長や進め方がわかる資料はこちら`（`clamp(20px,5.2vw,30px)/900`、`#FFFFFF`）
- ボタン `サービス資料をダウンロードする`：背景 `#FFFFFF` → hover `#E4ECF9`、文字 `#0F2961`、`clamp(15px,4vw,17px)/700`、`padding:19px 34px`、`border-radius:6px`
- 下にリンク `お問い合わせ`（`#C6D3EA` → hover `#FFFFFF`、下線 `1px solid #4A6394`）

---

### 8. ご利用の流れ（背景 `#FFFFFF`）

**見出し（h2、中央寄せ）**：`ご利用の流れ`

4ステップ。各行は `display:flex; flex-wrap:wrap; gap:6px 24px; align-items:baseline; background:#EDF3FC; border-radius:6px; padding:clamp(18px,4vw,24px) clamp(20px,4.5vw,28px)`
- ラベル：`flex: 0 0 auto; width: clamp(7em, 22%, 10em)`、`clamp(15px,4.2vw,18px)/900`
- 説明：`flex: 1 1 240px; min-width:0`、`clamp(13.5px,3.7vw,15px)`、`line-height:1.85`、`#5A6376`
- 行間に `▼`（`#0F2961`、`16px`、`padding:12px 0`、中央寄せ）

| ラベル | 説明 |
|---|---|
| ご提案 | AIに任せる業務、人が引き継ぐ業務に分けて進め方をご提案します。 |
| ご契約 | 範囲と料金にご納得いただいたうえで開始します。最低利用期間の縛りはありません。 |
| ヒアリング | 前任者から業務の状況をお聞きします。資料の作成は不要です。 |
| データ提供 | チャットやメール、資料をお渡しいただき、AIに読み込ませます。 |
| **サービス利用開始** | 引き継ぎ当日から、後任の方がそのままお使いいただけます。 |

最終行「サービス利用開始」のみ強調：`background:#DCE8FA; box-shadow: inset 0 0 0 1.5px #0F2961`、ラベル色 `#0F2961`、説明色 `#333333`

---

### 9. お客様事例（背景 `#EDF3FC`）

**見出し（h2、中央寄せ）**：`お客様事例`

事例カード2枚（`gap: clamp(20px,4vw,32px)`）。各カード：`background:#FFFFFF; box-shadow: inset 0 0 0 1px #D3DDEC; border-radius:10px; padding:clamp(24px,5vw,40px)`
- ラベル `事例 01` / `事例 02`（`clamp(11.5px,3.1vw,13px)/700`、`letter-spacing:0.12em`、`#0F2961`）
- h3（`clamp(17px,4.6vw,24px)/900`）
- 概要文（`clamp(13.5px,3.7vw,15.5px)`、`line-height:1.95`、`#5A6376`。**`max-width` は付けないこと** — 中途半端な位置で折り返す）
- 下に2カラム（`repeat(auto-fit, minmax(min(100%,260px),1fr))`、`gap:clamp(14px,3vw,20px)`）
  - **導入前**：`background:#EFF1F4; box-shadow: inset 0 0 0 1px #DCE0E7; border-radius:8px; padding:clamp(20px,4.4vw,28px)`。ラベル `導入前`（`#79839A`）、本文 `#5A6376`、太字部分は `font-weight:700; color:#333333`
  - **導入後**：`background:#DCE8FA; box-shadow: inset 0 0 0 1.5px #0F2961`。ラベル `導入後`（`#0F2961`）、本文 `#333333`、太字は `font-weight:700`

**事例01**
- タイトル：`採用も派遣も時間がかかりすぎて間に合わない`
- 概要：`会社規程では退職前通知は1ヶ月なので、外部人材を探すのは時間的に無理がありました。`
- 導入前（2段落）：
  - `退職が決まってから後任を探すも、**採用は最低3ヶ月、派遣でも1ヶ月かかり、**引継書で一時的に同僚が業務を肩代わりしていた。`
  - `引継書だけではカバーできず、後任が入ったときは前任者に聞くことはできず、**同僚社員の業務負荷も高くなる。**`
- 導入後（2段落）：
  - `当社ヒアリングで、前任者は**退職日ぎりぎりまで通常業務を行なっており**、引き継ぎ時間がほとんどないことが原因と特定した。`
  - `前任者が使う業務データをAI化しながら、業務内容をヒアリング。**通常業務と並行してヒキツギAIの試運転**を実施し、3ヶ月後に決まった後任社員が運用開始。`

**事例02**
- タイトル：`現場の業務過多で連鎖退職になり管理職が現場に`
- 概要：`後任不在で現場社員が引き継ぎ業務も兼務することで、労働環境が悪化し、組織が崩壊の危機にありました。`
- 導入前（2段落）：
  - `業界的に離職率が高く、**常に人員の補填が間に合っておらず**、現場社員が肩代わりすることが続いていた。`
  - `有給休暇を入れると引き継ぎ期間は約1週間でほぼ引き継ぎはなし。信頼関係の欠如からお客様からはのクレームは増え、**現場か疲弊し退職者が続出しました。**`
- 導入後（3段落）：
  - `退職者のデータを預けると、**まるで退職者と会話しているようなチャット**が利用できる。`
  - `退職代行で即日退職があっても、過去の情報をもとにお客様に確認できるため、**信頼関係が維持できた。**`
  - `一番のメリットは、社員の精神衛生環境が向上したことで**直近の離職数が0である。**`

（`**…**` は `<strong>` 相当の太字箇所）

---

### 10. 価格（背景 `#FFFFFF`）

**見出し（h2、中央寄せ）**：`価格`

**Layout（重要）**：3枚を subgrid で揃える。
```
親: display:grid; grid-template-columns: repeat(auto-fit, minmax(min(100%,280px),1fr));
    grid-template-rows: auto auto; gap: clamp(16px,3vw,24px); align-items:stretch;
各カード: display:grid; grid-row: span 2; grid-template-rows: subgrid;
```
カードは行1＝ヘッダー部（プラン名・価格・注記）、行2＝機能リスト。これにより**罫線の位置が3枚で一致する**（無料プランには注記行が無いため、subgrid なしだと段差ができる）。

カード共通：`border-radius:14px; padding: clamp(26px,5vw,36px) clamp(22px,4.4vw,32px)`
- 通常：`box-shadow: inset 0 0 0 1px #D3DDEC, 0 6px 18px rgba(15,41,97,0.05)`
- 強調（AIチャット）：`box-shadow: inset 0 0 0 2px #0F2961, 0 10px 26px rgba(15,41,97,0.12)`

ヘッダー部：プラン名（`clamp(13px,3.4vw,15px)/700`、`letter-spacing:0.1em`、中央寄せ）／価格（`clamp(30px,7.6vw,42px)/900`、中央寄せ）／注記 `税抜／月額／3ヶ月契約`（`clamp(12px,3.2vw,13.5px)`、`#79839A`、中央寄せ）

機能リスト：`border-top:1px solid #DFE7F3; padding-top:clamp(20px,4.2vw,28px); display:flex; flex-direction:column; gap:14px`。各項目は `19px` の丸チェック（通常＝背景 `#DCE8FA`・文字 `#0F2961`／強調カード＝背景 `#0F2961`・文字 `#FFFFFF`）＋テキスト（`clamp(13.5px,3.7vw,15.5px)`）。末尾に `など`（`#79839A`、左に `29px` インデント）

| プラン | 価格 | 注記 | 項目 |
|---|---|---|---|
| 活用診断 | 無料 | なし | AIによる業務ヒアリング／AIオペレーターによる操作デモ／ヒキツギAI活用診断／など |
| **AIチャット**（強調・プラン名は `#0F2961`） | ¥50,000〜 | あり | AIチャットボット／業務データのAI化／回答精度改善サービス／メールサポート／など |
| AI自動化 | ¥200,000〜 | あり | AI自動化アプリ／AIオペレーター（5時間〜）／自動化改善サービス／専任担当者メールサポート／など |

注記（中央寄せ、`clamp(13.5px,3.7vw,16px)/700`）：`※初期導入費用（AIチャットセットアップ／AI自動化アプリ設計）が別途かかります。個別のお見積となります。`

---

### 11. よくある質問（背景 `#FFFFFF`）

**見出し（h2、中央寄せ）**：`よくある質問`

`<details>` によるアコーディオン。リスト全体に `border-top: 1px solid #D3DDEC`、各項目に `border-bottom: 1px solid #D3DDEC`
- `<summary>`：`padding:20px 4px`、`clamp(14px,3.8vw,16px)`、`line-height:1.7`、`font-weight:500`、`cursor:pointer`
- 回答：`padding:20px clamp(16px,4vw,24px)`、`background:#EDF3FC`、`border-radius:6px`、`clamp(13.5px,3.7vw,15px)`、`line-height:1.9`、`#5A6376`

| 質問 | 回答 |
|---|---|
| ITに詳しい担当者がいなくても使えますか。 | 設計はすべて当社が行います。ご利用は、普段お使いのチャットに質問を書くだけです。 |
| 社内のやり取りを読ませることに不安があります。 | 入力されたデータをAIの学習には使用しません。データはすべて国内で保管し、どの情報にアクセスできるかはチャンネル・フォルダ単位で制御します。 |
| 引き継ぎまで日数がありません。間に合いますか。 | まず業務の洗い出しから着手し、優先度の高いものから順に引き継ぎます。残り日数に合わせて範囲を決めますので、まずはご相談ください。 |
| 途中でやめることはできますか。 | 最低利用期間の縛りはありません。ご相談・お見積もりも無料です。 |

---

### 12. 先行導入募集（背景 `#EDF3FC`）

内側の囲み：`border:1px solid #0C1E3F; border-radius:10px; background:#FFFFFF; padding:clamp(28px,6.5vw,56px)`
- h2 `先行導入3社を募集しています。`（`clamp(22px,5.8vw,36px)/900`）
- `初期設計費を半額でご提供します。`（`clamp(16px,4.4vw,20px)/700`）
- `その代わり、導入後の効果を事例として公開させていただきます。`（`clamp(14px,3.9vw,16px)`、`#333333`、`max-width:34em`）
- 区切り線（`1px solid #DFE7F3`）の下に2項目：`対象 3社` / `条件 導入プロセスと効果測定へのご協力`（ラベルは `#79839A`）

**カウントダウン・点滅・赤背景などの煽り演出は使わないこと。**

---

### 13. クロージング・フォーム（`id="form"`、背景 `#0C1E3F`）

- h2（`clamp(22px,5.6vw,40px)/900`、`#FFFFFF`）：`うまくいかない業務の引き継ぎ、<br>私たちにお任せください！`
- 余白 `clamp(40px,9vw,72px)`
- 本文（`clamp(15px,4.2vw,20px)`、`line-height:1.9`、`#C6D3EA`、`font-weight:500`）：`ヒキツギAIは人よりも速く、正確に<br>知識と作業を引き継ぎます。`

**フォーム**：`action="/thanks" method="post"`（送信先は未接続。実装時に差し替え）
`background:#FFFFFF; color:#333333; border-radius:10px; padding:clamp(24px,6vw,44px); max-width:640px; display:flex; flex-direction:column; gap:22px`

| 項目 | name | 必須 | 形式 | autocomplete |
|---|---|---|---|---|
| 会社名 | company | ● | text | organization |
| 氏名 | name | ● | text | name |
| ビジネスメール | email | ● | email | email |
| 従業員数 | size | ● | select（〜10名 `10`／11〜50名 `50`／51〜100名 `100`／101名以上 `101+`） | — |
| 引き継ぎ予定時期 | timing | ● | select（1ヶ月以内 `1m`／3ヶ月以内 `3m`／半年以内 `6m`／未定 `undecided`） | — |
| 先行導入3社への応募を希望する | pilot | － | checkbox（value `yes`） | — |

- ラベル：`14px/700`。必須は `<span style="color:#0F2961">必須</span>`
- 入力欄：`width:100%; padding:14px; font-size:16px; border:1px solid #BFCBDE; border-radius:6px; background:#FBFCFE; min-height:48px`
  - **`font-size:16px` は必須**（iOS Safariで入力時に自動ズームさせないため）
- select の先頭に `選択してください`（value 空）
- チェックボックス：`20×20px`、`accent-color:#0F2961`。ラベル全体を `1px solid #DFE7F3` の枠＋`background:#FBFCFE`＋`border-radius:6px`＋`padding:14px` で囲みクリック可能に
- 送信ボタン：`業務チェックリストを受け取る`（`width:100%`、背景 `#0F2961` → hover `#1C4295`、`clamp(15px,4vw,18px)/700`、`padding:20px`、`border-radius:6px`、`min-height:56px`）
- ボタン下：`※ しつこい営業は行いません。まずは可否のご相談だけでも歓迎です。`（`12.5px`、`#5A6376`）

---

### 14. 会社概要（背景 `#FFFFFF`）

**見出し（h2、中央寄せ）**：`会社概要`

**本文**（`max-width:44em`、中央寄せ配置、`clamp(14px,3.9vw,16.5px)`、`line-height:2.05`、`#333333`）：

> 株式会社ふえんは、これまでDX内製化支援、とくにノーコードで従業員が自分で業務アプリを開発する「市民開発」の導入研修を行なってきました。ノーコードからAIにツールが変化する中で、AIを活用したいものの、技術進歩が早くなかなか自社で活用できないというお悩みやご相談を多くいただき、業務の一部を私たちのヒキツギAIで行うことで、AIを業務で活用でき、より本業に注力することができると考えています。

**会社情報テーブル**：`background:#F4F8FD; box-shadow: inset 0 0 0 1px #D3DDEC; border-radius:10px; padding:clamp(20px,4.4vw,32px) clamp(20px,4.4vw,40px)`。各行 `display:flex; flex-wrap:wrap; gap:6px 24px; padding:clamp(16px,3.4vw,22px) 0`、2行目以降 `border-top:1px solid #DFE7F3`
- ラベル：`width: clamp(6em,26%,9em)`、`clamp(13px,3.5vw,14.5px)/700`、`#5A6376`
- 値：`flex:1 1 240px`、`clamp(13.5px,3.7vw,15.5px)`、`line-height:1.8`

| ラベル | 値 |
|---|---|
| 商号 | 株式会社 ふえん |
| 代表 | 安藤 昭太 |
| 顧問弁護士 | 小野田総合法律事務所　代表弁護士　小野田峻 |
| 所在地 | 〒2230051<br>神奈川県横浜市港北区箕輪町２−７−６０−２−E |
| 事業内容 | DX内製化支援・市民開発／プロコード開発・AIシステム実装／DX推進・業務再設計コンサルティング |
| 設立 | 2023年 8月 8日 |

**書籍出版**（h3 `clamp(15px,4.2vw,18px)/900`、`letter-spacing:0.06em`）
2枚のカード（`repeat(auto-fit, minmax(min(100%,320px),1fr))`、`gap:clamp(16px,3vw,24px)`）。`background:#F4F8FD; box-shadow: inset 0 0 0 1px #D3DDEC; border-radius:10px; padding:clamp(20px,4.4vw,28px)`。左に表紙画像（`width: clamp(76px,17vw,104px)`、`border-radius:3px`、`box-shadow:0 4px 12px rgba(15,41,97,0.14)`）

| 画像 | 日付バッジ | タイトル | 説明 |
|---|---|---|---|
| `uploads/book-nocodeshift.png` | 2021.06 | ノーコードシフト | 日本で初のノーコードをテーマにしたビジネス書。Amazonビジネス＋ITカテゴリで1位。 |
| `uploads/book-genba-dx.png` | 2026.03 | 現場が動くDX<br>ノーコードから始める市民開発実践ガイド | 「ふえん式 市民開発フレームワーク」に基づき、市民開発を企業内に浸透・定着させるための実践知と体系的アプローチ。 |

日付バッジ：`11.5px/700`、`color:#0F2961`、`background:#DCE8FA`、`border-radius:4px`、`padding:4px 9px`、`display:inline-block`

---

### 15. フッター（背景 `#081428`、文字 `#A3AFC4`）

`padding: clamp(40px,8vw,64px) clamp(20px,5vw,40px) clamp(96px,18vw,120px)`（下パディングが大きいのは固定CTAバーに隠れないため）。`display:flex; flex-wrap:wrap; gap:32px; justify-content:space-between`
- 左：ロゴ画像 `uploads/logo-trim.png`（`height:28px`、`filter: brightness(0) invert(1)` で白抜き）／`株式会社ふえん`（`13px`）
- 右：リンク（`13px`、`#A3AFC4` → hover `#FFFFFF`、`gap:12px` の縦並び）
  - プライバシーポリシー（`/privacy`）
  - 会社概要（`/company`）

---

### 16. 固定CTAバー（スクロール連動）

- **スクロール進捗が 30% 以上**で画面下部に表示（`position:fixed; left:0; right:0; bottom:0; z-index:50`）
- `background: rgba(255,255,255,0.97); backdrop-filter: blur(8px); border-top:1px solid #D3DDEC`
- `padding: 12px clamp(16px,5vw,40px) calc(12px + env(safe-area-inset-bottom))`（iOSのホームインジケーター対応）
- 中身は1ボタンのみ：`無料で業務チェックリストを受け取る`（`display:block; text-align:center`、背景 `#0F2961` → hover `#1C4295`、`clamp(14.5px,3.9vw,17px)/700`、`padding:17px 20px`、`border-radius:6px`、リンク先 `#form`）

## Interactions & Behavior

### スクロール連動（JSが必要な唯一の箇所）

`scroll` と `resize` を `{ passive: true }` で監視し、以下2つの真偽値を持つ：

```js
const doc = document.documentElement;
const max = (doc.scrollHeight - doc.clientHeight) || 1;
const y   = window.scrollY || doc.scrollTop || 0;

showBar       = (y / max) >= 0.30;  // 固定CTAバーの表示
headerScrolled = y > 24;            // ヘッダー背景の切り替え
```

- `showBar` … 固定CTAバーのマウント／アンマウント
- `headerScrolled` … ヘッダーの白レイヤーの `opacity` を 0 → 1（`transition: opacity 220ms ease`）

React/Vue で実装する場合は、値が変化したときだけ state を更新すること（毎フレーム setState しない）。

### アニメーション（すべてCSS `transform` / `opacity` のみ）

ファーストビューとヘッダーの装飾。GPU合成のみで動くため軽量。

```css
@keyframes geoDotA   { from { transform: translate3d(-7px, 4px, 0); }
                       to   { transform: translate3d(7px, -4px, 0); } }
@keyframes geoSpin   { from { transform: rotate(0deg); }
                       to   { transform: rotate(360deg); } }
@keyframes geoFloat  { from { transform: translate3d(0, -14px, 0) rotate(45deg); }
                       to   { transform: translate3d(0, 14px, 0) rotate(45deg); } }
```

ファーストビュー内の装飾レイヤー（`aria-hidden="true"` の絶対配置コンテナ、`pointer-events:none`）：
1. **ドットのタイル** — `background-image: radial-gradient(circle, rgba(15,41,97,0.2) 1.4px, transparent 1.6px); background-size: 34px 34px`。`geoDotA 24s ease-in-out infinite alternate`
2. **回る円** — `width: min(46vw,420px); aspect-ratio:1; border:1px solid rgba(15,41,97,0.14); border-radius:999px`。上端に `9px` の紺の点。`geoSpin 90s linear infinite`
3. **浮く四角** — `width: min(16vw,104px); border:1px solid rgba(15,41,97,0.14); background: rgba(255,255,255,0.55)`。`geoFloat 14s ease-in-out infinite alternate`
4. 最下部に `linear-gradient(180deg, rgba(255,255,255,0) 58%, #FFFFFF 100%)` のフェード

ヘッダーは 1 のドットタイルのみを流用（`height:220%` で切り出し）。

**モックのループアニメーション**（AIチャット／AI自動化アプリ、いずれも 6秒ループ）：

```css
@keyframes mockIn    { 0%,4% { opacity:0; transform: translateY(6px); }
                       12%,88% { opacity:1; transform:none; }
                       96%,100% { opacity:0; transform:none; } }
@keyframes mockCheck { 0%,4% { opacity:0; transform: scale(0.5); }
                       12%,88% { opacity:1; transform: scale(1); }
                       96%,100% { opacity:0; transform: scale(1); } }
@keyframes mockDots  { 0%,3% { opacity:0; } 5% { opacity:1; }
                       16% { opacity:0.35; } 17%,100% { opacity:0; } }
```

`animation-delay` で順番に出現させる：
- AIチャット：入力中ドット `0s` → `以下のように整理しました。` `1.1s` → 箇条書き `1.5s` / `1.9s` / `2.3s`
- AI自動化：チェック `0.2s` / `0.8s` / `1.4s` / `2s` → `実行完了 0.8秒` `2.5s`

### アクセシビリティ

```css
@media (prefers-reduced-motion: reduce) {
  .sky-layer { animation: none !important; }
  [style*="animation:mock"] { animation: none !important; opacity: 1 !important; transform: none !important; }
}
```
装飾レイヤーは `aria-hidden="true"`。ロゴ画像はすべて `alt="ヒキツギAI"`。

### アンカーリンク

`html { scroll-behavior: smooth; }`。`#top` / `#materials`（資料ダウンロードのセクション） / `#form`（フォーム）。ヘッダーが sticky なので、実装環境によっては `scroll-margin-top` の調整が必要な場合あり。

## State Management

外部データ取得なし。状態は上記2つの真偽値（`showBar` / `headerScrolled`）と、FAQの `<details>` の開閉（ネイティブ挙動）のみ。フォームは未接続（`action="/thanks"` はダミー）。

**実装時に接続が必要なもの**
- フォームの送信先（MA / CRM / メール送信のエンドポイント）
- 「資料をダウンロードする」「サービス資料をダウンロードする」「3分でわかる資料」のリンク先（現状はすべて `#materials` / `#form` へのアンカー）
- フッターの `/privacy` `/company`

## Design Tokens

### Colors

| 用途 | 値 |
|---|---|
| アクセント（唯一の強調色） | `#0F2961` — rgb(15,41,97) |
| アクセント hover | `#1C4295` |
| 反転面の背景（クロージング等） | `#0C1E3F` |
| フッター背景 | `#081428` |
| 本文 | `#333333` |
| 補助テキスト | `#5A6376` |
| 弱い補助テキスト | `#79839A` |
| 反転面の補助テキスト | `#C6D3EA` / `#A3AFC4` |
| ページ背景 | `#FFFFFF` |
| 面1（課題・FAQ回答など） | `#EDF3FC` |
| 面2（ヒキツギAIとは） | `#E4ECF9` |
| 面3（図解の枠） | `#F4F8FD` |
| 強調面（解決カード・価格チェック） | `#DCE8FA` |
| 中立面（課題カード） | `#EFF1F4` |
| 罫線・弱 | `#DFE7F3` |
| 罫線・標準 | `#D3DDEC` |
| 罫線・中立 | `#DCE0E7` |
| 罫線・強 | `#BFCBDE` / `#C9D6EE` |
| 反転面上の罫線 | `#4A6394` |
| 成功（チェック） | `#1F7A4D` |
| 警告（取り消し線） | `#B4322A` |
| 図解のバー（淡→濃） | `#93AEDD` → `#6C8CC4` → `#3D5786` → `#0F2961` |

**リンクのデフォルト**：`a { color: #0F2961 }` / `a:hover { color: #1C4295 }`

### Typography

- 本文：`"Noto Sans JP", "Hiragino Kaku Gothic ProN", sans-serif`（weights 400 / 500 / 700 / 900）
- 明朝（現状は未使用だが読み込み済み）：`"Zen Old Mincho", serif`（400 / 600）
- Google Fonts：`https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Zen+Old+Mincho:wght@400;600&display=swap`（`preconnect` 2本つき）
- `-webkit-font-smoothing: antialiased`

| 役割 | サイズ | ウェイト | 行間 |
|---|---|---|---|
| h1（ベタ塗り） | `clamp(16px, 6cqw, 32px)` | 900 | 1.62 |
| h1 強調行 | `clamp(24px, 8.8cqw, 50px)` | 900 | 1.3 |
| セクション h2 | `clamp(24px, 6.4vw, 42px)` | 900 | 1.45 |
| 特長 h3 | `clamp(17px, 4.6vw, 23px)` | 900 | 1.6 |
| リード | `clamp(14px, 3.9vw, 17px)` | 400 | 1.85 |
| 本文 | `clamp(13.5px, 3.7vw, 15.5px)` | 400 | 1.85–1.95 |
| 小ラベル | `clamp(11.5px, 3.1vw, 13px)` | 700 | — |
| CTA | `clamp(15px, 4vw, 18px)` | 700 | 1.4 |

`6cqw` / `8.8cqw` は **コンテナクエリ単位**（親に `container-type: inline-size`）。ビューポート幅ではなくテキスト列の幅に追従させることで、2カラム時にも1行に収まる。

### Spacing

- セクション縦：`clamp(56px, 11vw, 112px)`（反転面のみ `clamp(48px, 9vw, 88px)`）
- セクション横：`clamp(20px, 5vw, 40px)`
- h2 下：`clamp(32px, 7vw, 56px)`
- カード内：`clamp(20px, 4.4vw, 28px)` 〜 `clamp(24px, 5vw, 40px)`
- グリッド gap：`14px` 〜 `clamp(16px, 3vw, 24px)`
- ヒーローの分離余白：`clamp(48px, 11vw, 88px)`（**縮めないこと**）

### Radius

`6px`（ボタン・小要素） / `8px`（カード） / `10px`（大カード・図解） / `14px`（価格カード） / `999px`（丸）

### Shadows

| 用途 | 値 |
|---|---|
| 主CTA | `0 10px 24px rgba(15,41,97,0.24)` |
| 価格カード（通常） | `inset 0 0 0 1px #D3DDEC, 0 6px 18px rgba(15,41,97,0.05)` |
| 価格カード（強調） | `inset 0 0 0 2px #0F2961, 0 10px 26px rgba(15,41,97,0.12)` |
| 書籍表紙 | `0 4px 12px rgba(15,41,97,0.14)` |

**枠線は `border` ではなく `box-shadow: inset 0 0 0 1px <color>` を多用しています。** これは高DPI環境でサブピクセルにより枠線が部分的に欠ける現象を回避するためです。実装時もこの方式を維持してください。

## Assets

すべて `uploads/` に同梱。ユーザー提供素材からの切り出し・加工済み。

| ファイル | 用途 | 備考 |
|---|---|---|
| `logo-trim.png` | ヘッダー・フッターのロゴ | 透明余白をトリム済み。フッターでは `filter: brightness(0) invert(1)` で白抜き |
| `logo-hikitsugiai.png` | 本文中インラインのロゴ | トリム前の版 |
| `schreen.png` | ファーストビューのメインビジュアル | サービス画面のスクリーンショット |
| `ico-p1.png` / `ico-p2.png` / `ico-p3.png` | 課題アイコン3点 | 提供画像からの切り出し |
| `icon-solution-1.png` / `-2.png` / `-3.png` | 解決アイコン3点 | 同上 |
| `book-nocodeshift.png` | 書籍表紙 | 同上 |
| `book-genba-dx.png` | 書籍表紙 | 同上 |

**画像ではない図解**：サービスの特長4点の図、AIチャット／AI自動化のモックは、すべてHTML/CSSで描画しています（文字が鮮明・後から文言変更可能・パレットに完全一致するため）。写真素材に差し替える方針であれば、この部分は置き換え対象です。

## Performance

- LCP 2.5秒以内が目標。LCP要素は**ファーストビューの見出し（テキスト）またはメインビジュアル `schreen.png`**
- ヒーロー画像は `width` / `height` 属性を明示してCLSを防ぐ。`fetchpriority="high"` の付与を推奨（現状は未付与）
- 外部JSライブラリはゼロ。外部依存はGoogle Fontsのみ
- 元プロトタイプでは初期描画優先のため**すべてインラインスタイル**で書かれています。実装環境では通常のCSS（CSS Modules / Tailwind など既存の方式）に移してかまいません
- 装飾アニメーションは `transform` / `opacity` のみ。`filter: blur()` を使う実装は避けてください（過去に描画負荷で問題が出たため撤去済み）

## Files

| パス | 内容 |
|---|---|
| `ヒキツギAI LP.dc.html` | デザイン本体。`<x-dc>` 内のCDATAがマークアップ、`<script data-dc-script>` がロジック |
| `support.js` | プロトタイプ用ランタイム。**移植不要**（参照用） |
| `uploads/` | 画像アセット |
| `screenshots/` | デザインのスクリーンショット（`01`〜`14` が上から順にページ全体をスクロールしたもの。デスクトップ幅） |

ブラウザで `ヒキツギAI LP.dc.html` を直接開けば動作します（同階層に `support.js` と `uploads/` が必要）。
