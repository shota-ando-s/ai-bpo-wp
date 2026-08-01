<?php
/**
 * ヒキツギAI ランディングページ 本体マークアップ
 *
 * front-page.php から include される。
 * tools/build-lp-preview.php / tools/serve-lp.php からも同じファイルを読み込むため、
 * WordPress 関数には依存せず、呼び出し側が渡す変数だけを使う。
 *
 * デザイン仕様書：docs/hikitsugi-lp-design.md（Claude Design の出力）
 * 元デザインが全面インラインスタイルのため、ピクセル単位の再現性を優先して
 * その方式を維持している。インラインで書けないもの（@keyframes・:hover・
 * スクロール連動の状態・prefers-reduced-motion）だけが assets/lp.css にある。
 *
 * @var string $lp_home        サイトルートURL
 * @var string $lp_img         LP画像ディレクトリのURL（末尾スラッシュなし）
 * @var string $lp_privacy     プライバシーポリシーURL
 * @var string $lp_tokusho     特定商取引法に基づく表記URL
 * @var string $lp_company     運営会社サイトURL
 * @var string $lp_archives    記事一覧URL
 * @var string $lp_form_action フォームの送信先（未接続なので既定は '#'）
 * @var array  $lp_pickup      ピックアップ記事（空なら該当セクションごと出さない）
 * @var array  $lp_latest      新着記事（空なら該当セクションごと出さない）
 * @var string $lp_form_html   Contact Form 7 が出力したフォームHTML。
 *                             空なら静的フォーム（送信不可）にフォールバックする。
 *
 * $lp_pickup / $lp_latest の各要素は次の形。WP依存を持ち込まないよう、
 * WP_Query の結果は front-page.php 側でこの配列に均してから渡す。
 *   [ 'title', 'url', 'cat', 'date'（表示用 2026.06.21）,
 *     'datetime'（属性用 2026-06-21）, 'thumb', 'thumb_w', 'thumb_h' ]
 */

if ( ! isset( $lp_home ) )        { $lp_home        = '/'; }
if ( ! isset( $lp_img ) )         { $lp_img         = '/wp-content/themes/generatepress-child/images/lp'; }
if ( ! isset( $lp_privacy ) )     { $lp_privacy     = '/privacy-policy/'; }
if ( ! isset( $lp_tokusho ) )     { $lp_tokusho     = '/tokushoho/'; }
if ( ! isset( $lp_company ) )     { $lp_company     = 'https://fuenn.co.jp/'; }
if ( ! isset( $lp_archives ) )    { $lp_archives    = '/archives/'; }
if ( ! isset( $lp_form_action ) ) { $lp_form_action = '#'; }
if ( ! isset( $lp_pickup ) )      { $lp_pickup      = array(); }
if ( ! isset( $lp_latest ) )      { $lp_latest      = array(); }
if ( ! isset( $lp_form_html ) )   { $lp_form_html   = ""; }

$u_home     = htmlspecialchars( $lp_home, ENT_QUOTES );
$u_img      = htmlspecialchars( rtrim( $lp_img, '/' ), ENT_QUOTES );
$u_privacy  = htmlspecialchars( $lp_privacy, ENT_QUOTES );
$u_tokusho  = htmlspecialchars( $lp_tokusho, ENT_QUOTES );
$u_company  = htmlspecialchars( $lp_company, ENT_QUOTES );
$u_archives = htmlspecialchars( $lp_archives, ENT_QUOTES );
$u_form     = htmlspecialchars( $lp_form_action, ENT_QUOTES );

/* ------------------------------------------------------------------
   繰り返し要素のスタイル断片（同じ文字列を何度も書かないため）
   ------------------------------------------------------------------ */
$s_card_problem  = 'border-radius:8px; box-shadow:inset 0 0 0 1px #DCE0E7; padding:clamp(21px,4.6vw,27px); background:#EFF1F4; display:flex; flex-direction:column; align-items:center; text-align:center; gap:14px; flex:1 1 auto';
$s_card_solution = 'border-radius:8px; box-shadow:inset 0 0 0 1.5px #0F2961; padding:clamp(21px,4.6vw,27px); background:#DCE8FA; color:#333333; display:flex; flex-direction:column; align-items:center; text-align:center; gap:14px; flex:1 1 auto';
$s_card_icon     = 'width:clamp(72px,18vw,92px); height:auto; border-radius:999px; display:block';
$s_card_title    = 'margin:0; font-size:clamp(15px,4.2vw,18px); font-weight:700; line-height:1.6';
$s_card_body     = 'margin:0; font-size:clamp(13px,3.5vw,14.5px); line-height:1.85; color:#5A6376';
$s_flow_row      = 'display:flex; flex-wrap:wrap; gap:6px 24px; align-items:baseline; border-radius:6px; padding:clamp(18px,4vw,24px) clamp(20px,4.5vw,28px)';
$s_flow_label    = 'margin:0; font-size:clamp(15px,4.2vw,18px); font-weight:900; flex:0 0 auto; width:clamp(7em,22%,10em)';
$s_flow_desc     = 'margin:0; font-size:clamp(13.5px,3.7vw,15px); line-height:1.85; flex:1 1 240px; min-width:0';
$s_price_item    = 'margin:0; display:flex; gap:10px; align-items:flex-start; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.7';
$s_price_check   = 'flex:0 0 auto; width:19px; height:19px; border-radius:999px; font-size:11px; font-weight:700; display:flex; align-items:center; justify-content:center; margin-top:3px';
$s_faq_summary   = 'cursor:pointer; padding:20px 4px; font-size:clamp(14px,3.8vw,16px); line-height:1.7; font-weight:500';
$s_faq_answer    = 'margin:0; padding:20px clamp(16px,4vw,24px); background:#EDF3FC; border-radius:6px; font-size:clamp(13.5px,3.7vw,15px); line-height:1.9; color:#5A6376';
$s_field         = 'width:100%; padding:14px; font-size:16px; border:1px solid #BFCBDE; border-radius:6px; background:#FBFCFE; min-height:48px';
$s_field_label   = 'font-size:14px; font-weight:700';
$s_corp_row      = 'display:flex; flex-wrap:wrap; gap:6px 24px; padding:clamp(16px,3.4vw,22px) 0';
$s_corp_label    = 'margin:0; flex:0 0 auto; width:clamp(6em,26%,9em); font-size:clamp(13px,3.5vw,14.5px); font-weight:700; color:#5A6376';
$s_corp_value    = 'margin:0; flex:1 1 240px; min-width:0; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.8';
$s_dots          = 'position:absolute; left:-4%; top:-4%; width:108%; height:108%; background-image:radial-gradient(circle,rgba(15,41,97,0.2) 1.4px,transparent 1.6px); background-size:34px 34px; will-change:transform; animation:geoDotA 24s ease-in-out infinite alternate';
$s_h2            = 'font-size:clamp(24px,6.4vw,42px); line-height:1.45; font-weight:900; text-align:center';

/* 02 課題提起 */
$lp_problems = array(
	'休職中や退職後の本人に、連絡してしまっている',
	'「前任者しか知らない」取引先の事情がある',
	'過去のやり取りは残っているが、探せない',
	'月次や年次の作業を見落とし、クレームになる',
	'後任の業務が倍になり、組織が疲弊している',
	'引き継ぐ本人が、産休直前まで残業している',
);

/* 03 課題→解決の図式（課題カード／解決カードを1列としてペアで持つ） */
$lp_pairs = array(
	array(
		'p_img'   => 'ico-p1.png',
		'p_title' => '後任がいない',
		'p_body'  => '後任の人材がいない。採用も派遣も退職日には間に合わない',
		's_img'   => 'icon-solution-1.png',
		's_title' => 'AI＋人で後任代行',
		's_body'  => 'AIでできるだけ業務を圧縮しつつ、当社のAIパートナーが後任代行としてサポートします。',
	),
	array(
		'p_img'   => 'ico-p2.png',
		'p_title' => '担当者しか知らない',
		'p_body'  => '担当者以外やったことのない作業がたくさんある',
		's_img'   => 'icon-solution-2.png',
		's_title' => 'ヒアリングとデータで補完',
		's_body'  => '担当者へのヒアリング内容と過去のメールやチャットをもとに、明文化されていない業務を再現します。',
	),
	array(
		'p_img'   => 'ico-p3.png',
		'p_title' => '引き継ぎ書がない',
		'p_body'  => '急な休職や離職により、引き継ぎ書がない',
		's_img'   => 'icon-solution-3.png',
		's_title' => 'AIが引き継ぎ書を作成',
		's_body'  => '過去のデータからAIが回答するため、書類を読むことなく質問をするだけです。',
	),
);

/* 06 ご利用の流れ（最終行のみ強調） */
$lp_flow = array(
	array( 'ご提案', 'AIに任せる業務、人が引き継ぐ業務に分けて進め方をご提案します。', false ),
	array( 'ご契約', '範囲と料金にご納得いただいたうえで開始します。最低利用期間の縛りはありません。', false ),
	array( 'ヒアリング', '前任者から業務の状況をお聞きします。資料の作成は不要です。', false ),
	array( 'データ提供', 'チャットやメール、資料をお渡しいただき、AIに読み込ませます。', false ),
	array( 'サービス利用開始', '引き継ぎ当日から、後任の方がそのままお使いいただけます。', true ),
);

/* 06-25 価格（$highlight はAIチャットのみ） */
$lp_plans = array(
	array(
		'name'      => '活用診断',
		'price'     => '無料',
		'note'      => '',
		'highlight' => false,
		'items'     => array( 'AIによる業務ヒアリング', 'AIオペレーターによる操作デモ', 'ヒキツギAI活用診断' ),
	),
	array(
		'name'      => 'AIチャット',
		'price'     => '¥50,000〜',
		'note'      => '税抜／月額／3ヶ月契約',
		'highlight' => true,
		'items'     => array( 'AIチャットボット', '業務データのAI化', '回答精度改善サービス', 'メールサポート' ),
	),
	array(
		'name'      => 'AI自動化',
		'price'     => '¥200,000〜',
		'note'      => '税抜／月額／3ヶ月契約',
		'highlight' => false,
		'items'     => array( 'AI自動化アプリ', 'AIオペレーター（5時間〜）', '自動化改善サービス', '専任担当者メールサポート' ),
	),
);

/* 06-3 よくある質問 */
$lp_faq = array(
	array( 'ITに詳しい担当者がいなくても使えますか。', '設計はすべて当社が行います。ご利用は、普段お使いのチャットに質問を書くだけです。' ),
	array( '社内のやり取りを読ませることに不安があります。', '入力されたデータをAIの学習には使用しません。データはすべて国内で保管し、どの情報にアクセスできるかはチャンネル・フォルダ単位で制御します。' ),
	array( '引き継ぎまで日数がありません。間に合いますか。', 'まず業務の洗い出しから着手し、優先度の高いものから順に引き継ぎます。残り日数に合わせて範囲を決めますので、まずはご相談ください。' ),
	array( '途中でやめることはできますか。', '最低利用期間の縛りはありません。ご相談・お見積もりも無料です。' ),
);

/* 10・11 記事カード
   ピックアップ／新着で同じ見た目を使うので1箇所にまとめる。
   require が2回走っても落ちないよう function_exists で囲う。 */
if ( ! function_exists( 'lp_render_post_card' ) ) {
	function lp_render_post_card( array $item ) {
		$title = isset( $item['title'] ) ? $item['title'] : '';
		$url   = isset( $item['url'] ) ? $item['url'] : '#';
		$cat   = isset( $item['cat'] ) ? $item['cat'] : '';
		$date  = isset( $item['date'] ) ? $item['date'] : '';
		$dt    = isset( $item['datetime'] ) ? $item['datetime'] : '';
		$thumb = isset( $item['thumb'] ) ? $item['thumb'] : '';
		$tw    = isset( $item['thumb_w'] ) ? (int) $item['thumb_w'] : 1280;
		$th    = isset( $item['thumb_h'] ) ? (int) $item['thumb_h'] : 670;
		?>
		<a href="<?php echo htmlspecialchars( $url, ENT_QUOTES ); ?>" class="lp-card-post" style="display:flex; flex-direction:column; background:#FFFFFF; box-shadow:inset 0 0 0 1px #D3DDEC; border-radius:10px; overflow:hidden; color:#333333">
			<span style="display:block; aspect-ratio:1280/670; background:#EFF1F4; overflow:hidden">
				<?php if ( '' !== $thumb ) : ?>
					<img src="<?php echo htmlspecialchars( $thumb, ENT_QUOTES ); ?>" alt="" width="<?php echo $tw; ?>" height="<?php echo $th; ?>" loading="lazy" decoding="async" style="width:100%; height:100%; object-fit:cover; display:block">
				<?php endif; ?>
			</span>
			<span style="flex:1 1 auto; display:flex; flex-direction:column; gap:9px; padding:clamp(16px,3.4vw,20px)">
				<?php if ( '' !== $cat ) : ?>
					<span style="font-size:clamp(10.5px,2.9vw,12px); font-weight:700; letter-spacing:0.12em; color:#0F2961"><?php echo htmlspecialchars( $cat, ENT_QUOTES ); ?></span>
				<?php endif; ?>
				<span style="font-size:clamp(14px,3.8vw,16px); font-weight:700; line-height:1.65"><?php echo htmlspecialchars( $title, ENT_QUOTES ); ?></span>
				<?php if ( '' !== $date ) : ?>
					<time datetime="<?php echo htmlspecialchars( $dt, ENT_QUOTES ); ?>" style="margin-top:auto; padding-top:4px; font-size:clamp(11.5px,3.1vw,12.5px); color:#79839A"><?php echo htmlspecialchars( $date, ENT_QUOTES ); ?></time>
				<?php endif; ?>
			</span>
		</a>
		<?php
	}
}

$s_post_grid = 'display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr)); gap:clamp(16px,3vw,24px)';

/* ピックアップが無いときは新着セクションが会社概要（白面）の直下に来るので、
   面の色と上罫線を引き継いで境目が消えないようにする */
$lp_has_pickup  = ! empty( $lp_pickup );
$s_latest_shell = $lp_has_pickup
	? 'background:#FFFFFF'
	: 'background:#EDF3FC; border-top:1px solid #DFE7F3';

/* 09 会社概要（値は改行タグを含むので出力時にエスケープしない） */
$lp_corp = array(
	array( '商号', '株式会社 ふえん' ),
	array( '代表', '安藤 昭太' ),
	array( '顧問弁護士', '小野田総合法律事務所　代表弁護士　小野田峻' ),
	array( '所在地', '〒2230051<br />神奈川県横浜市港北区箕輪町２−７−６０−２−E' ),
	array( '事業内容', 'DX内製化支援・市民開発／プロコード開発・AIシステム実装／DX推進・業務再設計コンサルティング' ),
	array( '設立', '2023年 8月 8日' ),
);
?>

<div style="width:100%; overflow-x:clip">

	<!-- ============================================================
	     ヘッダー（sticky・スクロール24px超で白レイヤーをかぶせる）
	     ============================================================ -->
	<header style="position:sticky; top:0; z-index:40; background:#E4EEFB">
		<div aria-hidden="true" style="position:absolute; inset:0; overflow:hidden; pointer-events:none">
			<div class="sky-layer" style="position:absolute; left:-4%; top:-40%; width:108%; height:220%; background-image:radial-gradient(circle,rgba(15,41,97,0.2) 1.4px,transparent 1.6px); background-size:34px 34px; will-change:transform; animation:geoDotA 24s ease-in-out infinite alternate"></div>
			<div class="lp-header-veil" style="position:absolute; inset:0; background:rgba(255,255,255,0.8); backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); border-bottom:1px solid #DFE7F3"></div>
		</div>
		<div style="position:relative; max-width:1080px; margin:0 auto; padding:14px clamp(20px,5vw,40px); display:flex; align-items:center; justify-content:space-between; gap:16px">
			<a href="#top" style="display:flex; align-items:center"><img src="<?php echo $u_img; ?>/logo-trim.png" alt="ヒキツギAI" width="889" height="155" style="height:clamp(21px,5.6vw,30px); width:auto; max-width:min(48vw,180px); object-fit:contain; display:block"></a>
			<div style="display:flex; align-items:center; gap:clamp(12px,3vw,24px)">
				<a href="#form" class="lp-hv-ink" style="color:#5A6376; font-size:clamp(12.5px,3.3vw,14.5px); font-weight:500">相談する</a>
				<a href="#materials" class="lp-hv-navy" style="background:#0F2961; color:#FFFFFF; font-size:clamp(13px,3.4vw,15.5px); font-weight:700; border-radius:6px; padding:13px 24px; line-height:1.4">資料をダウンロードする</a>
			</div>
		</div>
	</header>

	<!-- ============================================================
	     01 ファーストビュー
	     ============================================================ -->
	<section id="top" style="position:relative; overflow:hidden; background:linear-gradient(180deg,#E4EEFB 0%,#F1F6FD 52%,#FFFFFF 100%)">
		<div aria-hidden="true" style="position:absolute; inset:0; pointer-events:none; overflow:hidden">
			<div class="sky-layer" style="<?php echo $s_dots; ?>"></div>
			<div class="sky-layer" style="position:absolute; right:-6%; top:6%; width:min(46vw,420px); aspect-ratio:1; border:1px solid rgba(15,41,97,0.14); border-radius:999px; will-change:transform; animation:geoSpin 90s linear infinite"><span style="position:absolute; left:50%; top:-5px; width:9px; height:9px; margin-left:-4.5px; background:#0F2961; opacity:0.4; border-radius:999px; display:block"></span></div>
			<div class="sky-layer" style="position:absolute; left:5%; bottom:14%; width:min(16vw,104px); aspect-ratio:1; border:1px solid rgba(15,41,97,0.14); background:rgba(255,255,255,0.55); will-change:transform; animation:geoFloat 14s ease-in-out infinite alternate"></div>
			<div style="position:absolute; inset:0; background:linear-gradient(180deg,rgba(255,255,255,0) 58%,#FFFFFF 100%)"></div>
		</div>
		<div style="position:relative; max-width:1080px; margin:0 auto; padding:clamp(40px,9vw,88px) clamp(20px,5vw,40px) clamp(48px,10vw,96px); display:flex; flex-wrap:wrap; align-items:center; gap:clamp(32px,6vw,56px)">

			<!-- container-type: 見出しの cqw 単位はこのテキスト列の幅を基準にする -->
			<div style="flex:1 1 400px; min-width:0; container-type:inline-size">
				<h1 style="margin:0; font-size:clamp(16px,6cqw,32px); line-height:1.62; font-weight:900; letter-spacing:-0.01em"><span style="background:#0F2961; color:#FFFFFF; padding:0.16em 0.26em; box-decoration-break:clone; -webkit-box-decoration-break:clone; white-space:nowrap">うまくいかない業務の引き継ぎ、</span><br><span style="background:#0F2961; color:#FFFFFF; padding:0.16em 0.26em; box-decoration-break:clone; -webkit-box-decoration-break:clone; white-space:nowrap">私たちにお任せください！</span></h1>

				<!-- 断定と解説を切り離すための余白。詰めないこと -->
				<div style="height:clamp(48px,11vw,88px)" aria-hidden="true"></div>

				<p style="margin:0; font-size:clamp(16px,4.3vw,22px); line-height:1.75; font-weight:500; color:#333333"><img src="<?php echo $u_img; ?>/logo-hikitsugiai.png" alt="ヒキツギAI" width="1000" height="250" style="height:1.5em; width:auto; vertical-align:-0.35em; margin-right:0.05em">は<span style="display:block; font-size:clamp(24px,8.8cqw,50px); font-weight:900; line-height:1.3; color:#333333; white-space:nowrap; letter-spacing:-0.01em; margin:0.1em 0">人よりも速く、正確に</span>知識と作業を引き継ぎます。</p>

				<div style="margin-top:clamp(32px,7vw,48px); display:flex; flex-direction:column; align-items:flex-start; gap:16px">
					<a href="#form" class="lp-hv-navy" style="background:#0F2961; color:#FFFFFF; font-weight:700; font-size:clamp(15px,4vw,18px); padding:20px 30px; border-radius:6px; box-shadow:0 10px 24px rgba(15,41,97,0.24); line-height:1.4">無料で業務チェックリストを受け取る</a>
					<a href="#materials" class="lp-hv-ink" style="color:#5A6376; font-size:clamp(13px,3.5vw,15px); font-weight:500; border-bottom:1px solid #BFCBDE; padding-bottom:2px">または3分でわかる資料をダウンロード</a>
				</div>
			</div>

			<div style="flex:1.25 1 420px; min-width:0">
				<img src="<?php echo $u_img; ?>/schreen.png" alt="ヒキツギAIが過去のやり取りをもとに質問に答えている画面" width="1920" height="1080" fetchpriority="high" decoding="async" style="width:100%; height:auto; display:block">
			</div>

		</div>
	</section>

	<!-- ============================================================
	     02 課題提起
	     ============================================================ -->
	<section style="border-top:1px solid #DFE7F3; background:#EDF3FC">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(48px,10vw,96px) clamp(20px,5vw,40px)">
			<h2 style="margin:0 0 clamp(28px,6vw,48px); font-size:clamp(24px,6.4vw,40px); line-height:1.45; font-weight:900; text-align:center">引き継ぎ、こうなっていませんか？</h2>
			<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr)); gap:14px">
				<?php foreach ( $lp_problems as $i => $text ) : ?>
					<div style="background:#FFFFFF; border:1px solid #DFE7F3; border-radius:8px; padding:24px; display:flex; gap:14px; align-items:flex-start">
						<span style="flex:0 0 auto; width:26px; height:26px; border-radius:999px; background:#0C1E3F; color:#FFFFFF; font-size:13px; font-weight:700; display:flex; align-items:center; justify-content:center"><?php echo (int) $i + 1; ?></span>
						<p style="margin:0; font-size:clamp(14px,3.9vw,16px); line-height:1.75; font-weight:500"><?php echo htmlspecialchars( $text, ENT_QUOTES ); ?></p>
					</div>
				<?php endforeach; ?>
			</div>
		</div>
	</section>

	<!-- ============================================================
	     03 課題→解決の図式
	     subgrid で「課題カード／矢印帯／解決カード」の高さを3列で揃える。
	     スマホの1列表示でも各ペアは必ず隣接する。
	     ============================================================ -->
	<section style="background:#FFFFFF; color:#333333; border-top:1px solid #DFE7F3; border-bottom:1px solid #DFE7F3">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px)">
			<h2 style="margin:0 0 clamp(32px,7vw,56px); <?php echo $s_h2; ?>; color:#333333">休・退職者の引き継ぎ問題は、<br>AIで解決できます。</h2>

			<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr)); grid-template-rows:auto auto auto; column-gap:clamp(16px,3vw,20px); row-gap:0">
				<?php foreach ( $lp_pairs as $i => $pair ) : ?>
					<div style="display:grid; grid-row:span 3; grid-template-rows:subgrid; margin-bottom:clamp(16px,3vw,20px)">
						<div style="<?php echo $s_card_problem; ?>">
							<img src="<?php echo $u_img . '/' . $pair['p_img']; ?>" alt="<?php echo htmlspecialchars( $pair['p_title'], ENT_QUOTES ); ?>" width="194" height="194" loading="lazy" decoding="async" style="<?php echo $s_card_icon; ?>">
							<p style="<?php echo $s_card_title; ?>; color:#333333"><?php echo htmlspecialchars( $pair['p_title'], ENT_QUOTES ); ?></p>
							<p style="<?php echo $s_card_body; ?>"><?php echo htmlspecialchars( $pair['p_body'], ENT_QUOTES ); ?></p>
						</div>

						<?php if ( 1 === $i ) : /* 中央の列だけ下向き矢印。左右は高さを合わせるだけのスペーサー */ ?>
							<div style="height:clamp(28px,6vw,44px); display:flex; align-items:center; justify-content:center" aria-hidden="true"><span style="width:0; height:0; border-left:clamp(12px,3vw,16px) solid transparent; border-right:clamp(12px,3vw,16px) solid transparent; border-top:clamp(13px,3.2vw,17px) solid #0F2961; display:block"></span></div>
						<?php else : ?>
							<div style="height:clamp(28px,6vw,44px)" aria-hidden="true"></div>
						<?php endif; ?>

						<div style="<?php echo $s_card_solution; ?>">
							<span style="font-size:11px; font-weight:700; letter-spacing:0.12em; color:#0F2961">ヒキツギAI</span>
							<img src="<?php echo $u_img . '/' . $pair['s_img']; ?>" alt="<?php echo htmlspecialchars( $pair['s_title'], ENT_QUOTES ); ?>" width="194" height="194" loading="lazy" decoding="async" style="<?php echo $s_card_icon; ?>">
							<p style="<?php echo $s_card_title; ?>"><?php echo htmlspecialchars( $pair['s_title'], ENT_QUOTES ); ?></p>
							<p style="<?php echo $s_card_body; ?>"><?php echo htmlspecialchars( $pair['s_body'], ENT_QUOTES ); ?></p>
						</div>
					</div>
				<?php endforeach; ?>
			</div>
		</div>
	</section>

	<!-- ============================================================
	     03-2 ヒキツギAIとは（動くモック2点。すべてHTML/CSSで描画）
	     ============================================================ -->
	<section style="background:#E4ECF9; border-top:1px solid #C9D6EE; border-bottom:1px solid #C9D6EE">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px)">
			<h2 style="margin:0 0 14px; <?php echo $s_h2; ?>; color:#333333"><img src="<?php echo $u_img; ?>/logo-hikitsugiai.png" alt="ヒキツギAI" width="1000" height="250" loading="lazy" decoding="async" style="height:1.5em; width:auto; vertical-align:-0.34em; margin-right:0.06em">とは</h2>
			<p style="margin:0 0 clamp(28px,6vw,44px); font-size:clamp(14px,3.9vw,17px); line-height:1.85; color:#333333; text-align:center">AIチャットとAI自動化アプリで知識と作業を引き受けます。</p>

			<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr)); gap:clamp(16px,3vw,24px)">

				<!-- AIチャット -->
				<div style="border-radius:10px; box-shadow:inset 0 0 0 1px #C9D6EE; padding:clamp(20px,4.5vw,28px); background:#FFFFFF">
					<p style="margin:0 0 6px; font-size:clamp(15px,4.2vw,18px); font-weight:700">AIチャット</p>
					<p style="margin:0 0 18px; font-size:clamp(12.5px,3.4vw,14px); line-height:1.8; color:#5A6376">過去のやり取りをもとに、聞けば答えます。</p>
					<div style="border-radius:8px; background:#FFFFFF; box-shadow:inset 0 0 0 1px #DFE7F3; padding:14px; overflow:hidden">
						<div style="display:flex; justify-content:flex-end; margin-bottom:12px">
							<span style="max-width:82%; background:#E8EFFB; color:#333333; border-radius:8px; padding:9px 12px; font-size:12px; line-height:1.65; animation:mockIn 6s ease-out infinite; animation-delay:0s">株式会社ふえんさまとの契約金額の経緯を教えてください。</span>
						</div>
						<div style="display:flex; gap:9px; align-items:flex-start">
							<span style="flex:0 0 auto; width:24px; height:24px; border-radius:999px; background:#0F2961; display:block"></span>
							<div style="flex:1 1 0; min-width:0; position:relative; display:flex; flex-direction:column; gap:7px">
								<!-- 入力中インジケーターは absolute。通常フローに置くと表示・非表示で枠がガタつく -->
								<span aria-hidden="true" style="position:absolute; left:0; top:2px; display:flex; gap:4px; align-items:center; height:14px; animation:mockDots 6s linear infinite">
									<span style="width:5px; height:5px; border-radius:999px; background:#A9BCE0; display:block"></span>
									<span style="width:5px; height:5px; border-radius:999px; background:#A9BCE0; display:block"></span>
									<span style="width:5px; height:5px; border-radius:999px; background:#A9BCE0; display:block"></span>
								</span>
								<span style="font-size:12px; line-height:1.65; font-weight:700; animation:mockIn 6s ease-out infinite; animation-delay:1.1s">以下のように整理しました。</span>
								<span style="font-size:11.5px; line-height:1.7; color:#5A6376; animation:mockIn 6s ease-out infinite; animation-delay:1.5s">・ご提案（2024年11月下旬）<br>月額のご提案を提示</span>
								<span style="font-size:11.5px; line-height:1.7; color:#5A6376; animation:mockIn 6s ease-out infinite; animation-delay:1.9s">・ご調整（2024年12月上旬）<br>支援範囲と支払条件を再相談</span>
								<span style="font-size:11.5px; line-height:1.7; color:#5A6376; animation:mockIn 6s ease-out infinite; animation-delay:2.3s">・契約締結（2024年12月15日）<br>翌月よりプロジェクト開始</span>
							</div>
						</div>
					</div>
				</div>

				<!-- AI自動化アプリ -->
				<div style="border-radius:10px; box-shadow:inset 0 0 0 1px #C9D6EE; padding:clamp(20px,4.5vw,28px); background:#FFFFFF">
					<p style="margin:0 0 6px; font-size:clamp(15px,4.2vw,18px); font-weight:700">AI自動化アプリ</p>
					<p style="margin:0 0 18px; font-size:clamp(12.5px,3.4vw,14px); line-height:1.8; color:#5A6376">決めた手順どおりに、毎回自動で実行します。</p>
					<div style="border-radius:8px; background:#FFFFFF; box-shadow:inset 0 0 0 1px #DFE7F3; padding:14px; overflow:hidden; display:flex; flex-direction:column; gap:0">
						<div style="display:flex; align-items:center; gap:10px; padding:10px 12px; border-radius:6px; background:#EDF3FC; box-shadow:inset 0 0 0 1px #DFE7F3">
							<span style="flex:1 1 0; min-width:0; font-size:11.5px; line-height:1.6; color:#333333">スプレッドシートに新しい行が追加されたら</span>
							<span aria-hidden="true" style="flex:0 0 auto; width:16px; height:16px; border-radius:999px; background:#1F7A4D; animation:mockCheck 6s ease-out infinite; animation-delay:0.2s; display:block"></span>
						</div>
						<span aria-hidden="true" style="height:18px; width:1px; margin:0 auto; background:#BFCBDE; display:block"></span>
						<div style="display:flex; align-items:center; gap:10px; padding:10px 12px; border-radius:6px; background:#EDF3FC; box-shadow:inset 0 0 0 1px #DFE7F3">
							<span style="flex:1 1 0; min-width:0; font-size:11.5px; line-height:1.6; color:#333333">条件で振り分ける（担当部署ごと）</span>
							<span aria-hidden="true" style="flex:0 0 auto; width:16px; height:16px; border-radius:999px; background:#1F7A4D; animation:mockCheck 6s ease-out infinite; animation-delay:0.8s; display:block"></span>
						</div>
						<span aria-hidden="true" style="height:18px; width:1px; margin:0 auto; background:#BFCBDE; display:block"></span>
						<div style="display:flex; align-items:center; gap:10px; padding:10px 12px; border-radius:6px; background:#EDF3FC; box-shadow:inset 0 0 0 1px #DFE7F3">
							<span style="flex:1 1 0; min-width:0; font-size:11.5px; line-height:1.6; color:#333333">AIが内容を要約する</span>
							<span aria-hidden="true" style="flex:0 0 auto; width:16px; height:16px; border-radius:999px; background:#1F7A4D; animation:mockCheck 6s ease-out infinite; animation-delay:1.4s; display:block"></span>
						</div>
						<span aria-hidden="true" style="height:18px; width:1px; margin:0 auto; background:#BFCBDE; display:block"></span>
						<div style="display:flex; align-items:center; gap:10px; padding:10px 12px; border-radius:6px; background:#F1F5FD; box-shadow:inset 0 0 0 1px #A9BCE0">
							<span style="flex:1 1 0; min-width:0; font-size:11.5px; line-height:1.6; color:#333333">担当チャンネルに通知する</span>
							<span aria-hidden="true" style="flex:0 0 auto; width:16px; height:16px; border-radius:999px; background:#1F7A4D; animation:mockCheck 6s ease-out infinite; animation-delay:2s; display:block"></span>
						</div>
						<p style="margin:14px 0 0; font-size:11px; line-height:1.6; color:#79839A; animation:mockIn 6s ease-out infinite; animation-delay:2.5s">実行完了 0.8秒</p>
					</div>
				</div>

			</div>
		</div>
	</section>

	<!-- ============================================================
	     04 サービスの特長（図解はすべてHTML/CSS。画像ではない）
	     ============================================================ -->
	<section style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px)">
		<h2 style="margin:0 0 clamp(36px,8vw,64px); <?php echo $s_h2; ?>">サービスの特長</h2>

		<div style="display:flex; flex-direction:column; gap:clamp(36px,8vw,64px)">

			<!-- 特長1：業務データをAIデータベースに -->
			<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr)); gap:clamp(20px,4vw,40px); align-items:center">
				<div>
					<h3 style="margin:0 0 14px; font-size:clamp(17px,4.6vw,23px); font-weight:900; line-height:1.6">前任者が使用した業務データをAIデータベースとして保存</h3>
					<p style="margin:0; font-size:clamp(14px,3.8vw,16px); line-height:1.95; color:#5A6376">TeamsやSlackなどのビジネスチャットやメール、オフィス文書を一括保存してチャットにします。</p>
				</div>
				<div aria-hidden="true" style="border-radius:10px; background:#F4F8FD; box-shadow:inset 0 0 0 1px #D3DDEC; aspect-ratio:16/10; display:flex; align-items:center; gap:clamp(10px,2.4vw,20px); padding:clamp(16px,3.4vw,28px)">
					<div style="flex:1 1 0; min-width:0; display:flex; flex-direction:column; gap:clamp(7px,1.6vw,11px)">
						<div style="background:#FFFFFF; box-shadow:inset 0 0 0 1px #D3DDEC; border-radius:6px; padding:clamp(8px,1.8vw,12px) clamp(9px,2vw,13px)">
							<p style="margin:0 0 5px; font-size:clamp(9px,2vw,11.5px); font-weight:700; color:#0F2961">ビジネスチャット</p>
							<span style="display:block; height:3px; border-radius:2px; background:#DFE7F3; margin-bottom:4px"></span>
							<span style="display:block; height:3px; width:64%; border-radius:2px; background:#DFE7F3"></span>
						</div>
						<div style="background:#FFFFFF; box-shadow:inset 0 0 0 1px #D3DDEC; border-radius:6px; padding:clamp(8px,1.8vw,12px) clamp(9px,2vw,13px)">
							<p style="margin:0 0 5px; font-size:clamp(9px,2vw,11.5px); font-weight:700; color:#0F2961">メール</p>
							<span style="display:block; height:3px; border-radius:2px; background:#DFE7F3; margin-bottom:4px"></span>
							<span style="display:block; height:3px; width:48%; border-radius:2px; background:#DFE7F3"></span>
						</div>
						<div style="background:#FFFFFF; box-shadow:inset 0 0 0 1px #D3DDEC; border-radius:6px; padding:clamp(8px,1.8vw,12px) clamp(9px,2vw,13px)">
							<p style="margin:0 0 5px; font-size:clamp(9px,2vw,11.5px); font-weight:700; color:#0F2961">オフィス文書</p>
							<span style="display:block; height:3px; border-radius:2px; background:#DFE7F3; margin-bottom:4px"></span>
							<span style="display:block; height:3px; width:72%; border-radius:2px; background:#DFE7F3"></span>
						</div>
					</div>
					<span style="flex:0 0 auto; width:0; height:0; border-top:clamp(7px,1.5vw,10px) solid transparent; border-bottom:clamp(7px,1.5vw,10px) solid transparent; border-left:clamp(9px,1.9vw,13px) solid #0F2961; display:block"></span>
					<div style="flex:1 1 0; min-width:0; background:#0F2961; border-radius:8px; padding:clamp(12px,2.6vw,20px); display:flex; flex-direction:column; gap:clamp(7px,1.5vw,10px)">
						<p style="margin:0; font-size:clamp(10px,2.2vw,13px); font-weight:700; color:#FFFFFF; line-height:1.5">AIデータベース</p>
						<span style="display:block; height:1px; background:#3D5786"></span>
						<div style="display:flex; flex-direction:column; gap:clamp(5px,1.2vw,8px)">
							<span style="display:block; height:clamp(7px,1.5vw,10px); border-radius:3px; background:#93AEDD"></span>
							<span style="display:block; height:clamp(7px,1.5vw,10px); border-radius:3px; background:#6C8CC4; width:88%"></span>
							<span style="display:block; height:clamp(7px,1.5vw,10px); border-radius:3px; background:#93AEDD; width:72%"></span>
							<span style="display:block; height:clamp(7px,1.5vw,10px); border-radius:3px; background:#6C8CC4; width:94%"></span>
						</div>
						<p style="margin:auto 0 0; font-size:clamp(8.5px,1.9vw,11px); color:#C6D3EA; line-height:1.5">聞けば答えられる状態で保存</p>
					</div>
				</div>
			</div>

			<!-- 特長2：前任者は打ち合わせをするだけ -->
			<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr)); gap:clamp(20px,4vw,40px); align-items:center">
				<div>
					<h3 style="margin:0 0 14px; font-size:clamp(17px,4.6vw,23px); font-weight:900; line-height:1.6">前任者は打ち合わせをするだけ</h3>
					<p style="margin:0; font-size:clamp(14px,3.8vw,16px); line-height:1.95; color:#5A6376">一番面倒で大変なのは、前任者が業務を可視化・構造化して資料にするところ。AIとデータで私たちが可視化します。</p>
				</div>
				<div aria-hidden="true" style="border-radius:10px; background:#F4F8FD; box-shadow:inset 0 0 0 1px #D3DDEC; aspect-ratio:16/10; display:flex; flex-direction:column; gap:clamp(10px,2.2vw,16px); padding:clamp(16px,3.4vw,28px)">
					<div style="position:relative; background:#FFFFFF; box-shadow:inset 0 0 0 1px #DFE7F3; border-radius:6px; padding:clamp(10px,2.2vw,15px) clamp(11px,2.4vw,16px); overflow:hidden">
						<p style="margin:0 0 7px; font-size:clamp(9px,2vw,11.5px); font-weight:700; color:#79839A">前任者による資料作成</p>
						<span style="display:block; height:3px; border-radius:2px; background:#E8ECF2; margin-bottom:4px"></span>
						<span style="display:block; height:3px; width:76%; border-radius:2px; background:#E8ECF2; margin-bottom:4px"></span>
						<span style="display:block; height:3px; width:58%; border-radius:2px; background:#E8ECF2"></span>
						<span style="position:absolute; left:8%; right:8%; top:50%; height:1.5px; background:#B4322A; transform:rotate(-9deg); display:block"></span>
						<span style="position:absolute; right:clamp(9px,2vw,14px); top:50%; transform:translateY(-50%); font-size:clamp(8.5px,1.9vw,11px); font-weight:700; color:#B4322A; background:#FFFFFF; padding:2px 5px; border-radius:3px">不要</span>
					</div>
					<div style="display:flex; align-items:center; gap:clamp(8px,1.8vw,12px)">
						<span style="flex:1 1 0; height:1px; background:#D3DDEC; display:block"></span>
						<span style="flex:0 0 auto; width:0; height:0; border-left:clamp(6px,1.3vw,9px) solid transparent; border-right:clamp(6px,1.3vw,9px) solid transparent; border-top:clamp(8px,1.7vw,11px) solid #0F2961; display:block"></span>
						<span style="flex:1 1 0; height:1px; background:#D3DDEC; display:block"></span>
					</div>
					<div style="flex:1 1 auto; display:flex; gap:clamp(9px,2vw,14px); align-items:stretch">
						<div style="flex:0 0 auto; width:clamp(58px,13vw,84px); display:flex; flex-direction:column; gap:clamp(5px,1.1vw,7px); justify-content:center">
							<span style="display:block; font-size:clamp(8px,1.8vw,10.5px); color:#5A6376; background:#FFFFFF; box-shadow:inset 0 0 0 1px #DFE7F3; border-radius:4px; padding:4px 6px; text-align:center">打ち合わせ</span>
							<span style="display:block; font-size:clamp(8px,1.8vw,10.5px); color:#5A6376; background:#FFFFFF; box-shadow:inset 0 0 0 1px #DFE7F3; border-radius:4px; padding:4px 6px; text-align:center">既存データ</span>
						</div>
						<span style="flex:0 0 auto; align-self:center; width:0; height:0; border-top:clamp(6px,1.3vw,9px) solid transparent; border-bottom:clamp(6px,1.3vw,9px) solid transparent; border-left:clamp(8px,1.7vw,11px) solid #0F2961; display:block"></span>
						<div style="flex:1 1 0; min-width:0; background:#0F2961; border-radius:8px; padding:clamp(11px,2.4vw,17px); display:flex; flex-direction:column; gap:clamp(6px,1.3vw,9px)">
							<p style="margin:0; font-size:clamp(9.5px,2.1vw,12.5px); font-weight:700; color:#FFFFFF; line-height:1.5">AIが業務を可視化</p>
							<div style="display:flex; flex-direction:column; gap:clamp(4px,1vw,6px)">
								<span style="display:block; height:clamp(6px,1.3vw,9px); border-radius:3px; background:#93AEDD"></span>
								<span style="display:block; height:clamp(6px,1.3vw,9px); border-radius:3px; background:#6C8CC4; width:84%"></span>
								<span style="display:block; height:clamp(6px,1.3vw,9px); border-radius:3px; background:#93AEDD; width:66%"></span>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- 特長3：月次・年次の作業も忘れずに -->
			<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr)); gap:clamp(20px,4vw,40px); align-items:center">
				<div>
					<h3 style="margin:0 0 14px; font-size:clamp(17px,4.6vw,23px); font-weight:900; line-height:1.6">月次や年次の作業も忘れずに実施</h3>
					<p style="margin:0; font-size:clamp(14px,3.8vw,16px); line-height:1.95; color:#5A6376">後任者が忘れがちな期間が空く定常業務もAIが覚えて自動で実行します。</p>
				</div>
				<div aria-hidden="true" style="border-radius:10px; background:#F4F8FD; box-shadow:inset 0 0 0 1px #D3DDEC; aspect-ratio:16/10; display:flex; flex-direction:column; gap:clamp(8px,1.8vw,12px); padding:clamp(16px,3.4vw,28px)">
					<div style="display:flex; align-items:center; justify-content:space-between; gap:10px">
						<p style="margin:0; font-size:clamp(10px,2.2vw,13px); font-weight:700; color:#0F2961">実行カレンダー</p>
						<span style="font-size:clamp(8.5px,1.9vw,11px); color:#5A6376">AIが自動で実行</span>
					</div>
					<div style="flex:1 1 auto; display:flex; flex-direction:column; gap:clamp(7px,1.6vw,11px)">
						<div style="display:flex; align-items:center; gap:clamp(8px,1.8vw,12px); background:#FFFFFF; box-shadow:inset 0 0 0 1px #D3DDEC; border-radius:6px; padding:clamp(8px,1.8vw,12px) clamp(9px,2vw,13px)">
							<span style="flex:0 0 auto; font-size:clamp(8.5px,1.9vw,11px); font-weight:700; color:#0F2961; background:#DCE8FA; border-radius:4px; padding:3px 7px">毎月</span>
							<span style="flex:1 1 0; min-width:0; font-size:clamp(9px,2vw,11.5px); color:#333333; line-height:1.5">請求書の発行と送付</span>
							<span style="flex:0 0 auto; width:clamp(12px,2.6vw,16px); height:clamp(12px,2.6vw,16px); border-radius:999px; background:#1F7A4D; display:block"></span>
						</div>
						<div style="display:flex; align-items:center; gap:clamp(8px,1.8vw,12px); background:#FFFFFF; box-shadow:inset 0 0 0 1px #D3DDEC; border-radius:6px; padding:clamp(8px,1.8vw,12px) clamp(9px,2vw,13px)">
							<span style="flex:0 0 auto; font-size:clamp(8.5px,1.9vw,11px); font-weight:700; color:#0F2961; background:#DCE8FA; border-radius:4px; padding:3px 7px">四半期</span>
							<span style="flex:1 1 0; min-width:0; font-size:clamp(9px,2vw,11.5px); color:#333333; line-height:1.5">定例レポートの作成</span>
							<span style="flex:0 0 auto; width:clamp(12px,2.6vw,16px); height:clamp(12px,2.6vw,16px); border-radius:999px; background:#1F7A4D; display:block"></span>
						</div>
						<div style="display:flex; align-items:center; gap:clamp(8px,1.8vw,12px); background:#FFFFFF; box-shadow:inset 0 0 0 1.5px #0F2961; border-radius:6px; padding:clamp(8px,1.8vw,12px) clamp(9px,2vw,13px)">
							<span style="flex:0 0 auto; font-size:clamp(8.5px,1.9vw,11px); font-weight:700; color:#FFFFFF; background:#0F2961; border-radius:4px; padding:3px 7px">毎年</span>
							<span style="flex:1 1 0; min-width:0; font-size:clamp(9px,2vw,11.5px); color:#333333; line-height:1.5; font-weight:700">年次の更新手続き</span>
							<span style="flex:0 0 auto; font-size:clamp(8px,1.8vw,10.5px); font-weight:700; color:#0F2961; white-space:nowrap">3日後</span>
						</div>
					</div>
					<p style="margin:0; font-size:clamp(8.5px,1.9vw,11px); color:#5A6376; line-height:1.5">1年に一度の作業も、期日どおりに実行します</p>
				</div>
			</div>

			<!-- 特長4：定額制 -->
			<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr)); gap:clamp(20px,4vw,40px); align-items:center">
				<div>
					<h3 style="margin:0 0 14px; font-size:clamp(17px,4.6vw,23px); font-weight:900; line-height:1.6">AIなのに安心の定額制</h3>
					<p style="margin:0; font-size:clamp(14px,3.8vw,16px); line-height:1.95; color:#5A6376">後任者の方が安心して必要なだけ使っていただけます。</p>
				</div>
				<div aria-hidden="true" style="border-radius:10px; background:#F4F8FD; box-shadow:inset 0 0 0 1px #D3DDEC; aspect-ratio:16/10; display:flex; flex-direction:column; gap:clamp(10px,2.2vw,16px); padding:clamp(16px,3.4vw,28px)">
					<div style="display:flex; align-items:baseline; justify-content:space-between; gap:10px">
						<p style="margin:0; font-size:clamp(10px,2.2vw,13px); font-weight:700; color:#0F2961">使う量と料金</p>
						<span style="font-size:clamp(8.5px,1.9vw,11px); color:#5A6376">1ヶ月目 → 6ヶ月目</span>
					</div>
					<div style="flex:1 1 auto; display:flex; flex-direction:column; gap:clamp(12px,2.6vw,18px); justify-content:center">
						<div>
							<p style="margin:0 0 6px; font-size:clamp(8.5px,1.9vw,11px); color:#5A6376; line-height:1.5">依頼した作業の量</p>
							<div style="display:flex; align-items:flex-end; gap:clamp(4px,1vw,7px); height:clamp(34px,7.5vw,56px)">
								<span style="flex:1 1 0; height:32%; background:#93AEDD; border-radius:3px 3px 0 0; display:block"></span>
								<span style="flex:1 1 0; height:46%; background:#93AEDD; border-radius:3px 3px 0 0; display:block"></span>
								<span style="flex:1 1 0; height:58%; background:#6C8CC4; border-radius:3px 3px 0 0; display:block"></span>
								<span style="flex:1 1 0; height:72%; background:#6C8CC4; border-radius:3px 3px 0 0; display:block"></span>
								<span style="flex:1 1 0; height:88%; background:#3D5786; border-radius:3px 3px 0 0; display:block"></span>
								<span style="flex:1 1 0; height:100%; background:#0F2961; border-radius:3px 3px 0 0; display:block"></span>
							</div>
						</div>
						<div>
							<p style="margin:0 0 6px; font-size:clamp(8.5px,1.9vw,11px); color:#5A6376; line-height:1.5">お支払い</p>
							<div style="display:flex; align-items:center; gap:clamp(4px,1vw,7px)">
								<?php for ( $i = 0; $i < 6; $i++ ) : ?>
									<span style="flex:1 1 0; height:clamp(9px,2vw,13px); background:#DCE8FA; box-shadow:inset 0 0 0 1px #A9BCE0; border-radius:3px; display:block"></span>
								<?php endfor; ?>
							</div>
						</div>
					</div>
					<p style="margin:0; font-size:clamp(8.5px,1.9vw,11px); font-weight:700; color:#0F2961; line-height:1.5">量が増えても毎月同じ料金です</p>
				</div>
			</div>

		</div>
	</section>

	<!-- ============================================================
	     05 資料ダウンロード（唯一の反転面）
	     ============================================================ -->
	<section id="materials" style="background:#0F2961; color:#FFFFFF">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(48px,9vw,88px) clamp(20px,5vw,40px)">
			<div style="text-align:center">
				<h2 style="margin:0 0 clamp(24px,5vw,36px); font-size:clamp(20px,5.2vw,30px); line-height:1.6; font-weight:900; color:#FFFFFF">特長や進め方がわかる資料はこちら</h2>
				<!-- 資料PDFを用意したら href を差し替える -->
				<a href="#form" class="lp-hv-navy-pale" style="display:inline-block; background:#FFFFFF; color:#0F2961; font-weight:700; font-size:clamp(15px,4vw,17px); padding:19px 34px; border-radius:6px; line-height:1.4">サービス資料をダウンロードする</a>
				<p style="margin:clamp(18px,4vw,24px) 0 0"><a href="#form" class="lp-hv-white" style="font-size:clamp(13px,3.5vw,14.5px); color:#C6D3EA; border-bottom:1px solid #4A6394; padding-bottom:2px">お問い合わせ</a></p>
			</div>
		</div>
	</section>

	<!-- ============================================================
	     06 ご利用の流れ
	     ============================================================ -->
	<section style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px)">
		<h2 style="margin:0 0 clamp(32px,7vw,56px); <?php echo $s_h2; ?>">ご利用の流れ</h2>
		<div style="display:flex; flex-direction:column; gap:0">
			<?php foreach ( $lp_flow as $i => $step ) : ?>
				<?php if ( $i > 0 ) : ?>
					<span aria-hidden="true" style="display:block; text-align:center; color:#0F2961; font-size:16px; line-height:1; padding:12px 0">▼</span>
				<?php endif; ?>
				<div style="<?php echo $s_flow_row; ?>; <?php echo $step[2] ? 'background:#DCE8FA; box-shadow:inset 0 0 0 1.5px #0F2961' : 'background:#EDF3FC'; ?>">
					<p style="<?php echo $s_flow_label; ?><?php echo $step[2] ? '; color:#0F2961' : ''; ?>"><?php echo htmlspecialchars( $step[0], ENT_QUOTES ); ?></p>
					<p style="<?php echo $s_flow_desc; ?>; color:<?php echo $step[2] ? '#333333' : '#5A6376'; ?>"><?php echo htmlspecialchars( $step[1], ENT_QUOTES ); ?></p>
				</div>
			<?php endforeach; ?>
		</div>
	</section>

	<!-- ============================================================
	     06-2 お客様事例
	     ============================================================ -->
	<section style="border-top:1px solid #DFE7F3; background:#EDF3FC">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px)">
			<h2 style="margin:0 0 clamp(32px,7vw,56px); <?php echo $s_h2; ?>">お客様事例</h2>

			<div style="display:flex; flex-direction:column; gap:clamp(20px,4vw,32px)">

				<div style="background:#FFFFFF; box-shadow:inset 0 0 0 1px #D3DDEC; border-radius:10px; padding:clamp(24px,5vw,40px)">
					<p style="margin:0 0 10px; font-size:clamp(11.5px,3.1vw,13px); font-weight:700; letter-spacing:0.12em; color:#0F2961">事例 01</p>
					<h3 style="margin:0 0 14px; font-size:clamp(17px,4.6vw,24px); font-weight:900; line-height:1.6">採用も派遣も時間がかかりすぎて間に合わない</h3>
					<!-- max-width は付けないこと（中途半端な位置で折り返す） -->
					<p style="margin:0 0 clamp(22px,4.6vw,32px); font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.95; color:#5A6376">会社規程では退職前通知は1ヶ月なので、外部人材を探すのは時間的に無理がありました。</p>
					<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr)); gap:clamp(14px,3vw,20px)">
						<div style="background:#EFF1F4; box-shadow:inset 0 0 0 1px #DCE0E7; border-radius:8px; padding:clamp(20px,4.4vw,28px)">
							<p style="margin:0 0 14px; font-size:clamp(12px,3.2vw,13.5px); font-weight:700; letter-spacing:0.1em; color:#79839A">導入前</p>
							<p style="margin:0 0 16px; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.95; color:#5A6376">退職が決まってから後任を探すも、<strong style="font-weight:700; color:#333333">採用は最低3ヶ月、派遣でも1ヶ月かかり、</strong>引継書で一時的に同僚が業務を肩代わりしていた。</p>
							<p style="margin:0; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.95; color:#5A6376">引継書だけではカバーできず、後任が入ったときは前任者に聞くことはできず、<strong style="font-weight:700; color:#333333">同僚社員の業務負荷も高くなる。</strong></p>
						</div>
						<div style="background:#DCE8FA; box-shadow:inset 0 0 0 1.5px #0F2961; border-radius:8px; padding:clamp(20px,4.4vw,28px)">
							<p style="margin:0 0 14px; font-size:clamp(12px,3.2vw,13.5px); font-weight:700; letter-spacing:0.1em; color:#0F2961">導入後</p>
							<p style="margin:0 0 16px; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.95; color:#333333">当社ヒアリングで、前任者は<strong style="font-weight:700">退職日ぎりぎりまで通常業務を行なっており</strong>、引き継ぎ時間がほとんどないことが原因と特定した。</p>
							<p style="margin:0; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.95; color:#333333">前任者が使う業務データをAI化しながら、業務内容をヒアリング。<strong style="font-weight:700">通常業務と並行してヒキツギAIの試運転</strong>を実施し、3ヶ月後に決まった後任社員が運用開始。</p>
						</div>
					</div>
				</div>

				<div style="background:#FFFFFF; box-shadow:inset 0 0 0 1px #D3DDEC; border-radius:10px; padding:clamp(24px,5vw,40px)">
					<p style="margin:0 0 10px; font-size:clamp(11.5px,3.1vw,13px); font-weight:700; letter-spacing:0.12em; color:#0F2961">事例 02</p>
					<h3 style="margin:0 0 14px; font-size:clamp(17px,4.6vw,24px); font-weight:900; line-height:1.6">現場の業務過多で連鎖退職になり管理職が現場に</h3>
					<p style="margin:0 0 clamp(22px,4.6vw,32px); font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.95; color:#5A6376">後任不在で現場社員が引き継ぎ業務も兼務することで、労働環境が悪化し、組織が崩壊の危機にありました。</p>
					<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr)); gap:clamp(14px,3vw,20px)">
						<div style="background:#EFF1F4; box-shadow:inset 0 0 0 1px #DCE0E7; border-radius:8px; padding:clamp(20px,4.4vw,28px)">
							<p style="margin:0 0 14px; font-size:clamp(12px,3.2vw,13.5px); font-weight:700; letter-spacing:0.1em; color:#79839A">導入前</p>
							<p style="margin:0 0 16px; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.95; color:#5A6376">業界的に離職率が高く、<strong style="font-weight:700; color:#333333">常に人員の補填が間に合っておらず</strong>、現場社員が肩代わりすることが続いていた。</p>
							<p style="margin:0; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.95; color:#5A6376">有給休暇を入れると引き継ぎ期間は約1週間でほぼ引き継ぎはなし。信頼関係の欠如からお客様からはのクレームは増え、<strong style="font-weight:700; color:#333333">現場か疲弊し退職者が続出しました。</strong></p>
						</div>
						<div style="background:#DCE8FA; box-shadow:inset 0 0 0 1.5px #0F2961; border-radius:8px; padding:clamp(20px,4.4vw,28px)">
							<p style="margin:0 0 14px; font-size:clamp(12px,3.2vw,13.5px); font-weight:700; letter-spacing:0.1em; color:#0F2961">導入後</p>
							<p style="margin:0 0 16px; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.95; color:#333333">退職者のデータを預けると、<strong style="font-weight:700">まるで退職者と会話しているようなチャット</strong>が利用できる。</p>
							<p style="margin:0 0 16px; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.95; color:#333333">退職代行で即日退職があっても、過去の情報をもとにお客様に確認できるため、<strong style="font-weight:700">信頼関係が維持できた。</strong></p>
							<p style="margin:0; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.95; color:#333333">一番のメリットは、社員の精神衛生環境が向上したことで<strong style="font-weight:700">直近の離職数が0である。</strong></p>
						</div>
					</div>
				</div>

			</div>
		</div>
	</section>

	<!-- ============================================================
	     06-25 価格
	     subgrid でヘッダー部／機能リストの境界を3枚で揃える
	     （無料プランには注記行が無いので、subgrid なしだと段差ができる）
	     ============================================================ -->
	<section style="background:#FFFFFF">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px)">
			<h2 style="margin:0 0 clamp(32px,7vw,56px); <?php echo $s_h2; ?>">価格</h2>

			<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr)); grid-template-rows:auto auto; gap:clamp(16px,3vw,24px); align-items:stretch">
				<?php foreach ( $lp_plans as $plan ) : ?>
					<div style="background:#FFFFFF; box-shadow:<?php echo $plan['highlight'] ? 'inset 0 0 0 2px #0F2961, 0 10px 26px rgba(15,41,97,0.12)' : 'inset 0 0 0 1px #D3DDEC, 0 6px 18px rgba(15,41,97,0.05)'; ?>; border-radius:14px; padding:clamp(26px,5vw,36px) clamp(22px,4.4vw,32px); display:grid; grid-row:span 2; grid-template-rows:subgrid">
						<div>
							<p style="margin:0 0 16px; font-size:clamp(13px,3.4vw,15px); font-weight:700; letter-spacing:0.1em; text-align:center; color:<?php echo $plan['highlight'] ? '#0F2961' : '#333333'; ?>"><?php echo htmlspecialchars( $plan['name'], ENT_QUOTES ); ?></p>
							<p style="margin:0 0 <?php echo '' === $plan['note'] ? 'clamp(22px,4.4vw,30px)' : '12px'; ?>; font-size:clamp(30px,7.6vw,42px); font-weight:900; line-height:1.2; text-align:center"><?php echo htmlspecialchars( $plan['price'], ENT_QUOTES ); ?></p>
							<?php if ( '' !== $plan['note'] ) : ?>
								<p style="margin:0 0 clamp(22px,4.4vw,30px); font-size:clamp(12px,3.2vw,13.5px); color:#79839A; text-align:center"><?php echo htmlspecialchars( $plan['note'], ENT_QUOTES ); ?></p>
							<?php endif; ?>
						</div>
						<div style="border-top:1px solid #DFE7F3; padding-top:clamp(20px,4.2vw,28px); display:flex; flex-direction:column; gap:14px">
							<?php foreach ( $plan['items'] as $item ) : ?>
								<p style="<?php echo $s_price_item; ?>"><span aria-hidden="true" style="<?php echo $s_price_check; ?>; <?php echo $plan['highlight'] ? 'background:#0F2961; color:#FFFFFF' : 'background:#DCE8FA; color:#0F2961'; ?>">✓</span><?php echo htmlspecialchars( $item, ENT_QUOTES ); ?></p>
							<?php endforeach; ?>
							<p style="margin:0 0 0 29px; font-size:clamp(13.5px,3.7vw,15.5px); line-height:1.7; color:#79839A">など</p>
						</div>
					</div>
				<?php endforeach; ?>
			</div>

			<p style="margin:clamp(28px,6vw,44px) 0 0; font-size:clamp(13.5px,3.7vw,16px); font-weight:700; line-height:1.85; text-align:center">※初期導入費用（AIチャットセットアップ／AI自動化アプリ設計）が別途かかります。個別のお見積となります。</p>
		</div>
	</section>

	<!-- ============================================================
	     06-3 よくある質問
	     ============================================================ -->
	<section style="background:#FFFFFF">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px)">
			<h2 style="margin:0 0 clamp(24px,5vw,40px); <?php echo $s_h2; ?>">よくある質問</h2>
			<div style="display:flex; flex-direction:column; border-top:1px solid #D3DDEC">
				<?php foreach ( $lp_faq as $qa ) : ?>
					<details style="border-bottom:1px solid #D3DDEC">
						<summary style="<?php echo $s_faq_summary; ?>"><?php echo htmlspecialchars( $qa[0], ENT_QUOTES ); ?></summary>
						<p style="<?php echo $s_faq_answer; ?>"><?php echo htmlspecialchars( $qa[1], ENT_QUOTES ); ?></p>
					</details>
				<?php endforeach; ?>
			</div>
		</div>
	</section>

	<!-- ============================================================
	     07 先行導入募集（カウントダウン・点滅などの煽り演出は使わない）
	     ============================================================ -->
	<section style="border-top:1px solid #DFE7F3; background:#EDF3FC">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px)">
			<div style="border:1px solid #0C1E3F; border-radius:10px; background:#FFFFFF; padding:clamp(28px,6.5vw,56px)">
				<h2 style="margin:0 0 clamp(24px,5vw,36px); font-size:clamp(22px,5.8vw,36px); line-height:1.5; font-weight:900">先行導入3社を募集しています。</h2>
				<p style="margin:0 0 18px; font-size:clamp(16px,4.4vw,20px); line-height:1.8; font-weight:700">初期設計費を半額でご提供します。</p>
				<p style="margin:0 0 clamp(24px,5vw,36px); font-size:clamp(14px,3.9vw,16px); line-height:1.95; color:#333333; max-width:34em">その代わり、導入後の効果を事例として公開させていただきます。</p>
				<div style="display:flex; flex-wrap:wrap; gap:12px 32px; border-top:1px solid #DFE7F3; padding-top:clamp(20px,4.5vw,28px)">
					<p style="margin:0; font-size:clamp(13.5px,3.7vw,15px); line-height:1.8"><span style="color:#79839A; margin-right:10px">対象</span>3社</p>
					<p style="margin:0; font-size:clamp(13.5px,3.7vw,15px); line-height:1.8"><span style="color:#79839A; margin-right:10px">条件</span>導入プロセスと効果測定へのご協力</p>
				</div>
			</div>
		</div>
	</section>

	<!-- ============================================================
	     08-3 クロージング・フォーム
	     ============================================================ -->
	<section id="form" style="background:#0C1E3F; color:#FFFFFF">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px); text-align:center">
			<h2 style="margin:0; font-size:clamp(22px,5.6vw,40px); line-height:1.45; font-weight:900; color:#FFFFFF">うまくいかない業務の引き継ぎ、<br>私たちにお任せください！</h2>
			<div style="height:clamp(40px,9vw,72px)" aria-hidden="true"></div>
			<p style="margin:0; font-size:clamp(15px,4.2vw,20px); line-height:1.9; color:#C6D3EA; font-weight:500">ヒキツギAIは人よりも速く、正確に<br>知識と作業を引き継ぎます。</p>

			<?php if ( '' !== $lp_form_html ) : ?>

				<?php
				/* 本番：Contact Form 7 が出力する。見た目は assets/lp.css の
				   「3-2. クロージングフォーム」で design に合わせ直している。 */
				echo $lp_form_html;
				?>

			<?php else : ?>

			<!-- フォールバック：CF7が使えない環境（tools/ のプレビュー等）向けの静的フォーム。
			     送信はできない。項目・見た目はCF7版と揃えてある。 -->
			<form action="<?php echo $u_form; ?>" method="post" style="margin:clamp(36px,8vw,64px) auto 0; text-align:left; background:#FFFFFF; color:#333333; border-radius:10px; padding:clamp(24px,6vw,44px); width:100%; max-width:640px; display:flex; flex-direction:column; gap:22px">

				<div style="display:flex; flex-direction:column; gap:8px">
					<label for="lp-company" style="<?php echo $s_field_label; ?>">会社名 <span style="color:#0F2961">必須</span></label>
					<input id="lp-company" name="company" type="text" required autocomplete="organization" style="<?php echo $s_field; ?>">
				</div>

				<div style="display:flex; flex-direction:column; gap:8px">
					<label for="lp-name" style="<?php echo $s_field_label; ?>">氏名 <span style="color:#0F2961">必須</span></label>
					<input id="lp-name" name="name" type="text" required autocomplete="name" style="<?php echo $s_field; ?>">
				</div>

				<div style="display:flex; flex-direction:column; gap:8px">
					<label for="lp-email" style="<?php echo $s_field_label; ?>">ビジネスメール <span style="color:#0F2961">必須</span></label>
					<!-- font-size:16px は必須（iOS Safari の自動ズーム防止） -->
					<input id="lp-email" name="email" type="email" required autocomplete="email" inputmode="email" style="<?php echo $s_field; ?>">
				</div>

				<div style="display:flex; flex-direction:column; gap:8px">
					<label for="lp-size" style="<?php echo $s_field_label; ?>">従業員数 <span style="color:#0F2961">必須</span></label>
					<select id="lp-size" name="size" required style="<?php echo $s_field; ?>">
						<option value="">選択してください</option>
						<option value="10">〜10名</option>
						<option value="50">11〜50名</option>
						<option value="100">51〜100名</option>
						<option value="101+">101名以上</option>
					</select>
				</div>

				<div style="display:flex; flex-direction:column; gap:8px">
					<label for="lp-timing" style="<?php echo $s_field_label; ?>">引き継ぎ予定時期 <span style="color:#0F2961">必須</span></label>
					<select id="lp-timing" name="timing" required style="<?php echo $s_field; ?>">
						<option value="">選択してください</option>
						<option value="1m">1ヶ月以内</option>
						<option value="3m">3ヶ月以内</option>
						<option value="6m">半年以内</option>
						<option value="undecided">未定</option>
					</select>
				</div>

				<label for="lp-pilot" style="display:flex; align-items:flex-start; gap:12px; font-size:15px; line-height:1.7; padding:14px; border:1px solid #DFE7F3; border-radius:6px; background:#FBFCFE; cursor:pointer">
					<input id="lp-pilot" name="pilot" type="checkbox" value="yes" style="width:20px; height:20px; margin:2px 0 0; accent-color:#0F2961">
					<span>先行導入3社への応募を希望する</span>
				</label>

				<label for="lp-acceptance" style="display:flex; align-items:flex-start; gap:12px; font-size:15px; line-height:1.7; padding:14px; border:1px solid #DFE7F3; border-radius:6px; background:#FBFCFE; cursor:pointer">
					<input id="lp-acceptance" name="acceptance" type="checkbox" value="1" required style="width:20px; height:20px; margin:2px 0 0; accent-color:#0F2961">
					<span><a href="<?php echo $u_privacy; ?>" target="_blank" rel="noopener">個人情報保護方針</a>に同意する</span>
				</label>

				<button type="submit" class="lp-hv-navy" style="width:100%; background:#0F2961; color:#FFFFFF; font-weight:700; font-size:clamp(15px,4vw,18px); padding:20px; border:none; border-radius:6px; cursor:pointer; min-height:56px">業務チェックリストを受け取る</button>
				<p style="margin:0; font-size:12.5px; line-height:1.8; color:#5A6376">※ しつこい営業は行いません。まずは可否のご相談だけでも歓迎です。</p>
			</form>

			<?php endif; ?>
		</div>
	</section>

	<!-- ============================================================
	     09 会社概要
	     ============================================================ -->
	<section id="company" style="background:#FFFFFF">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px)">
			<h2 style="margin:0 0 clamp(28px,6vw,44px); <?php echo $s_h2; ?>">会社概要</h2>
			<p style="margin:0 auto; max-width:44em; font-size:clamp(14px,3.9vw,16.5px); line-height:2.05; color:#333333">株式会社ふえんは、これまでDX内製化支援、とくにノーコードで従業員が自分で業務アプリを開発する「市民開発」の導入研修を行なってきました。ノーコードからAIにツールが変化する中で、AIを活用したいものの、技術進歩が早くなかなか自社で活用できないというお悩みやご相談を多くいただき、業務の一部を私たちのヒキツギAIで行うことで、AIを業務で活用でき、より本業に注力することができると考えています。</p>

			<div style="margin:clamp(40px,8vw,72px) 0 0; background:#F4F8FD; box-shadow:inset 0 0 0 1px #D3DDEC; border-radius:10px; padding:clamp(20px,4.4vw,32px) clamp(20px,4.4vw,40px)">
				<?php foreach ( $lp_corp as $i => $row ) : ?>
					<div style="<?php echo $s_corp_row; ?><?php echo $i > 0 ? '; border-top:1px solid #DFE7F3' : ''; ?>">
						<p style="<?php echo $s_corp_label; ?>"><?php echo htmlspecialchars( $row[0], ENT_QUOTES ); ?></p>
						<p style="<?php echo $s_corp_value; ?>"><?php echo $row[1]; /* 改行タグを含むので意図的にエスケープしない */ ?></p>
					</div>
				<?php endforeach; ?>
			</div>

			<h3 style="margin:clamp(40px,8vw,72px) 0 clamp(18px,4vw,26px); font-size:clamp(15px,4.2vw,18px); font-weight:900; letter-spacing:0.06em">書籍出版</h3>
			<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr)); gap:clamp(16px,3vw,24px)">
				<div style="display:flex; gap:clamp(16px,3.4vw,24px); align-items:flex-start; background:#F4F8FD; box-shadow:inset 0 0 0 1px #D3DDEC; border-radius:10px; padding:clamp(20px,4.4vw,28px)">
					<img src="<?php echo $u_img; ?>/book-nocodeshift.png" alt="ノーコードシフト" width="204" height="296" loading="lazy" decoding="async" style="flex:0 0 auto; width:clamp(76px,17vw,104px); height:auto; border-radius:3px; box-shadow:0 4px 12px rgba(15,41,97,0.14); display:block">
					<div style="flex:1 1 0; min-width:0">
						<p style="margin:0 0 10px; font-size:11.5px; font-weight:700; color:#0F2961; background:#DCE8FA; border-radius:4px; padding:4px 9px; display:inline-block">2021.06</p>
						<p style="margin:0 0 10px; font-size:clamp(15px,4vw,17px); font-weight:700; line-height:1.6">ノーコードシフト</p>
						<p style="margin:0; font-size:clamp(13px,3.5vw,14.5px); line-height:1.85; color:#5A6376">日本で初のノーコードをテーマにしたビジネス書。Amazonビジネス＋ITカテゴリで1位。</p>
					</div>
				</div>
				<div style="display:flex; gap:clamp(16px,3.4vw,24px); align-items:flex-start; background:#F4F8FD; box-shadow:inset 0 0 0 1px #D3DDEC; border-radius:10px; padding:clamp(20px,4.4vw,28px)">
					<img src="<?php echo $u_img; ?>/book-genba-dx.png" alt="現場が動くDX ノーコードから始める市民開発実践ガイド" width="224" height="296" loading="lazy" decoding="async" style="flex:0 0 auto; width:clamp(76px,17vw,104px); height:auto; border-radius:3px; box-shadow:0 4px 12px rgba(15,41,97,0.14); display:block">
					<div style="flex:1 1 0; min-width:0">
						<p style="margin:0 0 10px; font-size:11.5px; font-weight:700; color:#0F2961; background:#DCE8FA; border-radius:4px; padding:4px 9px; display:inline-block">2026.03</p>
						<p style="margin:0 0 10px; font-size:clamp(15px,4vw,17px); font-weight:700; line-height:1.6">現場が動くDX<br>ノーコードから始める市民開発実践ガイド</p>
						<p style="margin:0; font-size:clamp(13px,3.5vw,14.5px); line-height:1.85; color:#5A6376">「ふえん式 市民開発フレームワーク」に基づき、市民開発を企業内に浸透・定着させるための実践知と体系的アプローチ。</p>
					</div>
				</div>
			</div>
		</div>
	</section>

	<?php if ( $lp_has_pickup ) : ?>
	<!-- ============================================================
	     10 ピックアップ記事
	     プラグイン ai-bpo-pickup で指定した投稿。0件なら丸ごと出さない。
	     ============================================================ -->
	<section style="background:#EDF3FC; border-top:1px solid #DFE7F3">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px)">
			<h2 style="margin:0 0 clamp(32px,7vw,56px); <?php echo $s_h2; ?>">ピックアップ記事</h2>
			<div style="<?php echo $s_post_grid; ?>">
				<?php foreach ( $lp_pickup as $item ) : ?>
					<?php lp_render_post_card( $item ); ?>
				<?php endforeach; ?>
			</div>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( ! empty( $lp_latest ) ) : ?>
	<!-- ============================================================
	     11 新着記事
	     ============================================================ -->
	<section style="<?php echo $s_latest_shell; ?>">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(56px,11vw,112px) clamp(20px,5vw,40px)">
			<h2 style="margin:0 0 clamp(32px,7vw,56px); <?php echo $s_h2; ?>">新着記事</h2>
			<div style="<?php echo $s_post_grid; ?>">
				<?php foreach ( $lp_latest as $item ) : ?>
					<?php lp_render_post_card( $item ); ?>
				<?php endforeach; ?>
			</div>
			<p style="margin:clamp(32px,7vw,52px) 0 0; text-align:center">
				<a href="<?php echo $u_archives; ?>" class="lp-hv-navy-pale" style="display:inline-block; background:#FFFFFF; color:#0F2961; box-shadow:inset 0 0 0 1.5px #0F2961; border-radius:6px; padding:17px 34px; font-weight:700; font-size:clamp(14px,3.8vw,16px); line-height:1.4">記事一覧を見る</a>
			</p>
		</div>
	</section>
	<?php endif; ?>

	<!-- ============================================================
	     08-4 フッター
	     下パディングが大きいのは追従CTAバーに隠れないため
	     ============================================================ -->
	<footer style="background:#081428; color:#A3AFC4">
		<div style="max-width:1080px; margin:0 auto; padding:clamp(40px,8vw,64px) clamp(20px,5vw,40px) clamp(96px,18vw,120px); display:flex; flex-wrap:wrap; gap:32px; justify-content:space-between">
			<div>
				<p style="margin:0 0 16px"><img src="<?php echo $u_img; ?>/logo-trim.png" alt="ヒキツギAI" width="889" height="155" loading="lazy" decoding="async" style="height:28px; width:auto; display:block; filter:brightness(0) invert(1)"></p>
				<p style="margin:0 0 6px; font-size:13px; line-height:1.9">株式会社ふえん</p>
			</div>
			<div style="display:flex; flex-direction:column; gap:12px">
				<a href="<?php echo $u_privacy; ?>" class="lp-hv-white" style="color:#A3AFC4; font-size:13px">プライバシーポリシー</a>
				<a href="<?php echo $u_tokusho; ?>" class="lp-hv-white" style="color:#A3AFC4; font-size:13px">特定商取引法に基づく表記</a>
				<a href="#company" class="lp-hv-white" style="color:#A3AFC4; font-size:13px">会社概要</a>
				<a href="<?php echo $u_archives; ?>" class="lp-hv-white" style="color:#A3AFC4; font-size:13px">記事一覧</a>
				<a href="<?php echo $u_company; ?>" class="lp-hv-white" style="color:#A3AFC4; font-size:13px">運営会社サイト</a>
			</div>
		</div>
	</footer>

	<!-- ============================================================
	     追従CTAバー（スクロール進捗30%以上で表示）
	     ============================================================ -->
	<div class="lp-sticky-cta" style="position:fixed; left:0; right:0; bottom:0; z-index:50; background:rgba(255,255,255,0.97); backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); border-top:1px solid #D3DDEC; padding:12px clamp(16px,5vw,40px) calc(12px + env(safe-area-inset-bottom))">
		<div style="max-width:1080px; margin:0 auto">
			<a href="#form" class="lp-hv-navy" style="display:block; text-align:center; background:#0F2961; color:#FFFFFF; font-weight:700; font-size:clamp(14.5px,3.9vw,17px); padding:17px 20px; border-radius:6px; line-height:1.4">無料で業務チェックリストを受け取る</a>
		</div>
	</div>

</div>

<script>
/* スクロール連動はこの2つの真偽値だけ。値が変わったときだけ class を書き換える。
     scrolled … ヘッダーの白レイヤーの opacity（> 24px）
     showBar  … 追従CTAバーの表示（スクロール進捗 >= 30%） */
(function () {
	var body = document.body;
	var scrolled = null;
	var showBar = null;
	var ticking = false;

	function update() {
		var d = document.documentElement;
		var max = (d.scrollHeight - d.clientHeight) || 1;
		var y = window.pageYOffset || d.scrollTop || 0;
		var nextScrolled = y > 24;
		var nextShowBar = (y / max) >= 0.3;

		if (nextScrolled !== scrolled) {
			scrolled = nextScrolled;
			body.classList.toggle('lp-is-scrolled', scrolled);
		}
		if (nextShowBar !== showBar) {
			showBar = nextShowBar;
			body.classList.toggle('lp-is-cta', showBar);
		}
	}

	function onScroll() {
		if (ticking) return;
		ticking = true;
		window.requestAnimationFrame(function () {
			ticking = false;
			update();
		});
	}

	window.addEventListener('scroll', onScroll, { passive: true });
	window.addEventListener('resize', onScroll, { passive: true });
	update();
})();
</script>
