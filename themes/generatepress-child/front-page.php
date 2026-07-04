<?php
/**
 * LP用フロントページテンプレート — オフボード（退職・引き継ぎ業務の引き取りサービス）
 *
 * @package GeneratePress
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/* ===== SEO: フロントページの title / meta description =====
 * functions.php 側にメタ出力が無いため、フロントページに限定して補完する（指示書 2章）。
 */
add_filter( 'pre_get_document_title', function( $title ) {
	if ( is_front_page() ) {
		return '退職・引き継ぎの引き取りサービス｜後任不在でも業務を止めない - オフボード';
	}
	return $title;
} );

add_action( 'wp_head', function() {
	if ( ! is_front_page() ) {
		return;
	}
	?>
	<meta name="description" content="担当者の退職で引き継ぎが不安な方へ。退職者の頭の中をAIと専任スタッフで抜き出し、チェックリスト化・AIチャットボット化・業務自動化まで。後任不在でも最短10日。運営：株式会社ふえん。">
	<?php
}, 1 );

add_action( 'wp_head', function() {
	?>
	<style>
	/* ===== GeneratePress コンテナ解除 ===== */
	body.home #content.site-content,
	body.home .site-content.grid-container,
	body.home .inside-page-wrapper {
		max-width: 100% !important;
		width: 100% !important;
		padding-left: 0 !important;
		padding-right: 0 !important;
		margin-left: 0 !important;
		margin-right: 0 !important;
	}

	/* ===== LP 共通 ===== */
	.lp-wrap { font-family: 'Noto Sans JP', 'Hiragino Sans', 'Yu Gothic', sans-serif; color: #1a1a2e; width: 100%; overflow-x: hidden; }
	.lp-section { padding: 96px 40px; }
	.lp-inner { max-width: 1400px; margin: 0 auto; padding: 0 40px; box-sizing: border-box; position: relative; z-index: 1; }
	.lp-section-label { font-size: 13px; font-weight: 700; letter-spacing: .15em; text-transform: uppercase; color: #1a56db; margin-bottom: 12px; }
	.lp-h2 { font-size: clamp(1.6rem, 3vw, 2.4rem); font-weight: 800; line-height: 1.35; margin: 0 0 20px; }
	.lp-lead { font-size: 1.1rem; color: #4a4a6a; line-height: 1.85; margin-bottom: 0; }
	.lp-bg-white  { background: #fff; }
	.lp-bg-light  { background: #f5f7ff; }

	/* ===== Hero ===== */
	.lp-hero {
		background: linear-gradient(135deg, #0d1b4b 0%, #1a56db 100%);
		color: #fff;
		padding: 116px 40px 100px;
		text-align: center;
		position: relative;
		overflow: hidden;
		width: 100%;
		box-sizing: border-box;
	}
	.lp-hero::before {
		content: '';
		position: absolute; inset: 0;
		background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
		pointer-events: none;
	}
	.lp-hero-eyebrow {
		display: inline-block;
		background: rgba(255,255,255,.15);
		border: 1px solid rgba(255,255,255,.3);
		border-radius: 50px;
		padding: 6px 18px;
		font-size: 13px;
		font-weight: 600;
		letter-spacing: .1em;
		margin-bottom: 24px;
	}
	.lp-hero h1 {
		font-size: clamp(1.9rem, 5.4vw, 3rem);
		font-weight: 900;
		line-height: 1.25;
		margin: 0 0 16px;
		text-shadow: 0 2px 20px rgba(0,0,0,.2);
	}
	.lp-hero h1 em {
		font-style: normal;
		color: #ffd166;
	}
	.lp-hero-sub {
		font-size: clamp(1rem, 2.5vw, 1.18rem);
		opacity: .9;
		margin: 0 auto 36px;
		max-width: 680px;
		line-height: 1.85;
	}
	.lp-hero-cta {
		display: inline-block;
		background: #ff6b35;
		color: #fff !important;
		font-size: 1.1rem;
		font-weight: 700;
		padding: 18px 48px;
		border-radius: 50px;
		text-decoration: none !important;
		box-shadow: 0 8px 30px rgba(255,107,53,.5);
		transition: transform .2s, box-shadow .2s;
	}
	.lp-hero-cta:hover { transform: translateY(-2px); box-shadow: 0 12px 40px rgba(255,107,53,.6); }
	.lp-hero-note { font-size: 12px; opacity: .6; margin-top: 14px; }
	.lp-hero-btns { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }

	/* ===== 緊急バナー ===== */
	.lp-urgent {
		display: inline-flex;
		align-items: center;
		gap: 12px;
		margin: 34px auto 0;
		background: rgba(220,38,38,.18);
		border: 1.5px solid rgba(248,113,113,.6);
		border-radius: 14px;
		padding: 14px 24px;
		font-size: .95rem;
		line-height: 1.6;
		text-align: left;
		max-width: 640px;
	}
	.lp-urgent .lp-urgent-icon { font-size: 1.4rem; flex-shrink: 0; }
	.lp-urgent .lp-urgent-icon i { color: #ffd166; }
	.lp-pain-item-icon i { color: #fff; }
	.lp-urgent a { color: #ffd166 !important; font-weight: 700; text-decoration: underline; }

	/* ===== 対応範囲カード ===== */
	.lp-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 24px; margin-top: 48px; }
	.lp-card {
		background: #fff;
		border-radius: 16px;
		padding: 32px 28px;
		box-shadow: 0 4px 24px rgba(26,86,219,.08);
		border: 1px solid rgba(26,86,219,.08);
		transition: transform .2s, box-shadow .2s;
	}
	.lp-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(26,86,219,.15); }
	.lp-card-icon { font-size: 2.4rem; margin-bottom: 16px; display: block; color: #1a56db; }
	.lp-card h3 { font-size: 1.05rem; font-weight: 800; margin: 0 0 10px; }
	.lp-card p  { font-size: .93rem; color: #5a5a7a; line-height: 1.7; margin: 0; }

	/* ===== 競合比較テーブル ===== */
	.lp-compare { margin-top: 48px; overflow-x: auto; }
	.lp-compare table { width: 100%; border-collapse: separate; border-spacing: 0; min-width: 640px; font-size: .95rem; }
	.lp-compare th, .lp-compare td { padding: 16px 18px; text-align: center; border-bottom: 1px solid #e6e9f5; }
	.lp-compare thead th { font-size: .85rem; color: #6a6a8a; font-weight: 700; }
	.lp-compare tbody th { text-align: left; font-weight: 700; color: #1a1a2e; white-space: nowrap; }
	.lp-compare .col-offboard { background: #eef3ff; border-left: 2px solid #1a56db; border-right: 2px solid #1a56db; font-weight: 800; color: #1a3a8a; }
	.lp-compare thead .col-offboard { border-top: 2px solid #1a56db; border-radius: 12px 12px 0 0; color: #1a56db; }
	.lp-compare tbody tr:last-child .col-offboard { border-bottom: 2px solid #1a56db; border-radius: 0 0 12px 12px; }

	/* ===== 料金 ===== */
	.lp-price-note { font-size: .8rem; color: #999; text-align: center; margin-top: 22px; line-height: 1.7; }

	/* ===== 4段ラダー（サービスと料金） ===== */
	.lp-ladder { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 22px; margin-top: 44px; }
	.lp-ladder-card {
		background: #fff;
		border-radius: 18px;
		padding: 30px 26px 28px;
		border: 1.5px solid rgba(26,86,219,.12);
		box-shadow: 0 4px 20px rgba(26,86,219,.06);
		display: flex;
		flex-direction: column;
	}
	.lp-ladder-card.is-feature { border: 2px solid #ff6b35; box-shadow: 0 10px 34px rgba(255,107,53,.18); }
	.lp-ladder-num {
		width: 44px; height: 44px;
		border-radius: 50%;
		background: linear-gradient(135deg, #1a56db, #4f8ef7);
		color: #fff;
		font-size: 1.4rem;
		font-weight: 900;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 16px;
	}
	.lp-ladder-card.is-feature .lp-ladder-num { background: linear-gradient(135deg, #ff6b35, #e85d04); }
	.lp-ladder-name { font-size: 1.05rem; font-weight: 800; color: #1a1a2e; margin-bottom: 12px; line-height: 1.4; }
	.lp-ladder-desc { font-size: .88rem; color: #5a5a7a; line-height: 1.7; margin: 0 0 18px; flex: 1; }
	.lp-ladder-price { font-size: 1.25rem; font-weight: 900; color: #1a56db; line-height: 1.3; }
	.lp-ladder-card.is-feature .lp-ladder-price { color: #e85d04; }
	.lp-ladder-notes { margin-top: 30px; }
	.lp-ladder-notes p { font-size: .95rem; color: #3a3a5a; line-height: 1.7; margin: 0 0 10px; }
	.lp-ladder-cta { margin-top: 36px; text-align: center; }

	/* ===== FAQ ===== */
	.lp-faq { margin-top: 44px; max-width: 820px; }
	.lp-faq-item {
		background: #fff;
		border-radius: 16px;
		padding: 26px 28px;
		border: 1px solid rgba(26,86,219,.1);
		box-shadow: 0 3px 16px rgba(26,86,219,.06);
		margin-bottom: 18px;
	}
	.lp-faq-q {
		font-size: 1rem;
		font-weight: 800;
		color: #1a1a2e;
		line-height: 1.5;
		margin: 0 0 10px;
		display: flex;
		gap: 10px;
	}
	.lp-faq-q::before { content: 'Q.'; color: #1a56db; font-weight: 900; flex-shrink: 0; }
	.lp-faq-a {
		font-size: .92rem;
		color: #5a5a7a;
		line-height: 1.8;
		margin: 0;
		display: flex;
		gap: 10px;
	}
	.lp-faq-a::before { content: 'A.'; color: #ff6b35; font-weight: 900; flex-shrink: 0; }

	/* ===== 運営プロフィール ===== */
	.lp-profile { display: grid; grid-template-columns: 200px 1fr; gap: 40px; align-items: center; margin-top: 40px; background: #fff; border-radius: 20px; padding: 40px; box-shadow: 0 4px 24px rgba(26,86,219,.08); }
	@media (max-width: 680px) { .lp-profile { grid-template-columns: 1fr; gap: 24px; text-align: center; } }
	.lp-profile-avatar { width: 160px; height: 160px; border-radius: 50%; background: linear-gradient(135deg, #1a56db, #7c3aed); display: flex; align-items: center; justify-content: center; font-size: 4rem; margin: 0 auto; color: #fff; overflow: hidden; }
	.lp-profile-avatar img { width: 100%; height: 100%; object-fit: cover; display: block; }
	.lp-profile h3 { font-size: 1.2rem; font-weight: 800; margin: 0 0 6px; }
	.lp-profile .pf-role { font-size: .9rem; color: #1a56db; font-weight: 700; margin-bottom: 14px; }
	.lp-profile p { font-size: .92rem; color: #5a5a7a; line-height: 1.8; margin: 0 0 10px; }
	.lp-profile .pf-meta { font-size: .85rem; color: #6a6a8a; }
	.lp-profile .pf-meta b { color: #1a1a2e; }

	/* ===== 最終CTA ===== */
	.lp-cta-section {
		background: linear-gradient(135deg, #0d1b4b, #1a56db);
		color: #fff;
		text-align: center;
		padding: 100px 20px;
	}
	.lp-cta-section .lp-h2 { color: #fff; margin-bottom: 12px; }
	.lp-cta-section .lp-lead { color: rgba(255,255,255,.8); margin-bottom: 40px; }
	.lp-cta-btns { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
	.lp-btn-primary {
		display: inline-block;
		background: #ff6b35;
		color: #fff !important;
		font-size: 1.1rem;
		font-weight: 700;
		padding: 18px 48px;
		border-radius: 50px;
		text-decoration: none !important;
		box-shadow: 0 8px 30px rgba(255,107,53,.5);
		transition: transform .2s, box-shadow .2s;
	}
	.lp-btn-primary:hover { transform: translateY(-2px); box-shadow: 0 12px 40px rgba(255,107,53,.6); }

	/* ===== こんな課題ありませんか ===== */
	.lp-pain {
		background: #fff8f5;
		border-top: 4px solid #ff6b35;
		padding: 80px 40px;
	}
	.lp-pain-label {
		font-size: 13px;
		font-weight: 700;
		letter-spacing: .15em;
		text-transform: uppercase;
		color: #ff6b35;
		margin-bottom: 12px;
	}
	.lp-pain-items {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
		gap: 20px;
		margin-top: 40px;
	}
	.lp-pain-item {
		background: #fff;
		border-radius: 16px;
		padding: 28px 24px;
		border: 2px solid #ffe0d0;
		display: flex;
		gap: 16px;
		align-items: flex-start;
		box-shadow: 0 2px 12px rgba(255,107,53,.07);
	}
	.lp-pain-item-icon {
		flex-shrink: 0;
		width: 48px;
		height: 48px;
		background: linear-gradient(135deg, #ff6b35, #e85d04);
		border-radius: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 1.5rem;
	}
	.lp-pain-item-body h3 {
		font-size: 1rem;
		font-weight: 800;
		margin: 0 0 6px;
		color: #1a1a2e;
		line-height: 1.5;
	}
	.lp-pain-item-body p {
		font-size: .88rem;
		color: #6a5a50;
		margin: 0;
		line-height: 1.7;
	}
	.lp-pain-cta {
		margin-top: 40px;
		text-align: center;
		font-size: 1.05rem;
		font-weight: 700;
		color: #1a1a2e;
	}
	.lp-pain-cta span {
		display: inline-block;
		background: linear-gradient(90deg, #ff6b35, #e85d04);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	/* ===== タブレット・モバイル調整 ===== */
	@media (max-width: 768px) {
		.lp-section { padding: 72px 24px; }
		.lp-inner { padding: 0 24px; }
		.lp-hero { padding: 80px 24px 72px; }
		.lp-pain { padding: 60px 24px; }
		.lp-ladder { grid-template-columns: 1fr 1fr; gap: 18px; }
		.lp-ladder-card { padding: 24px 20px 22px; }
	}
	@media (max-width: 480px) {
		.lp-section { padding: 60px 16px; }
		.lp-inner { padding: 0 16px; }
		.lp-hero { padding: 64px 16px 56px; }
		.lp-cta-section { padding: 70px 16px; }
		.lp-pain { padding: 60px 16px; }
		.lp-profile { padding: 28px 20px; }
		.lp-faq-item { padding: 22px 20px; }
		.lp-ladder { grid-template-columns: 1fr; gap: 16px; }
		.lp-ladder-card { padding: 22px 18px 20px; }
		.lp-ladder-price { font-size: 1.1rem; line-height: 1.45; }
		.lp-compare table { font-size: .85rem; }
	}
	</style>
	<?php
} );

// 診断ツールURL（外部・現在未公開）
// offboard.ai-bpo.site のDNS設定・デプロイ完了後、Hero と ④セクション末に
// 「無料で引き継ぎ診断（約60秒）」CTAを復活させる際にこの変数を使う
$offboard_tool_url = 'https://offboard.ai-bpo.site';

get_header();
?>

<div class="lp-wrap">

	<!-- ===== ① Hero ===== -->
	<section class="lp-hero">
		<div class="lp-inner">
			<div class="lp-hero-eyebrow">オフボード ｜ 退職・引き継ぎ業務の引き取りサービス</div>
			<h1>担当者が辞める。<br>その<em>引き継ぎ書</em>、本当に足りていますか？</h1>
			<p class="lp-hero-sub">完璧な引き継ぎ書は、作れない。だからオフボードは、退職・休職する社員の<strong>「頭の中」をAIで抜き出し</strong>、業務が止まらない状態を作って<strong>維持</strong>します。</p>
			<div class="lp-hero-btns">
				<a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>" class="lp-hero-cta">無料相談（30分）→</a>
			</div>
			<p class="lp-hero-note">※ 相談は無料。現状の引き継ぎ資料の簡易診断もその場で行います</p>
			<div class="lp-urgent">
				<span class="lp-urgent-icon"><i class="fa-solid fa-triangle-exclamation"></i></span>
				<span>退職日が迫っていますか？ 最短10日で、辞める前にその人の知識をAIに写し取ります。 <a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">今すぐ無料相談 →</a></span>
			</div>
		</div>
	</section>

	<!-- ===== ② 課題 ===== -->
	<section class="lp-pain">
		<div class="lp-inner">
			<div class="lp-pain-label">Your Challenges</div>
			<h2 class="lp-h2">その引き継ぎ、<br>こんな状態になっていませんか？</h2>

			<div class="lp-pain-items">
				<div class="lp-pain-item">
					<div class="lp-pain-item-icon"><i class="fa-solid fa-hourglass-half"></i></div>
					<div class="lp-pain-item-body">
						<h3>後任が決まらないまま<br>退職日が近づいている</h3>
						<p>採用は1〜2ヶ月、BPOも要件定義に1〜2ヶ月。退職日には間に合わない…</p>
					</div>
				</div>
				<div class="lp-pain-item">
					<div class="lp-pain-item-icon"><i class="fa-solid fa-arrow-trend-down"></i></div>
					<div class="lp-pain-item-body">
						<h3>引き継ぎ精度が<br>9割止まりで抜け漏れる</h3>
						<p>辞める人のモチベは低く、資料は不十分。引き継いだはずの業務が後で噴出…</p>
					</div>
				</div>
				<div class="lp-pain-item">
					<div class="lp-pain-item-icon"><i class="fa-solid fa-lock"></i></div>
					<div class="lp-pain-item-body">
						<h3>「その人しか知らない」<br>属人業務がブラックボックス</h3>
						<p>判断基準も例外対応も本人の頭の中。退職と同時に消えてしまう…</p>
					</div>
				</div>
			</div>

			<p class="lp-pain-cta"><span>その引き継ぎ、「書かせる」のをやめませんか。</span></p>
		</div>
	</section>

	<!-- ===== ③ 解決コンセプト「書かせない引き継ぎ」 ===== -->
	<section class="lp-section lp-bg-white" id="approach">
		<div class="lp-inner">
			<div class="lp-section-label">Our Approach</div>
			<h2 class="lp-h2">引き継ぎ書を書かせない。<br>頭の中を、抜き出す。</h2>
			<p class="lp-lead">引き継ぎが失敗するのは、辞めていく本人に「書かせる」からです。オフボードでは、退職者は <strong>喋る・画面録画する・ファイルを渡す</strong> だけ。文書化はAIが肩代わりし、専任スタッフが抜け漏れを深掘りします。</p>

			<div class="lp-cards">
				<div class="lp-card">
					<span class="lp-card-icon"><i class="fa-solid fa-magnifying-glass"></i></span>
					<h3>抽出</h3>
					<p>AIヒアリングと専任スタッフの深掘りで、手順だけでなく判断基準・例外対応・トラブル事例まで吸い出します。在籍中に実務を試運転し、抜け漏れをその場で潰します。</p>
				</div>
				<div class="lp-card">
					<span class="lp-card-icon"><i class="fa-solid fa-bolt"></i></span>
					<h3>緊急対応</h3>
					<p>後任が決まっていなくても、最短10日で「ボールを落とさない体制」を立ち上げます。派遣の採用にもBPOの要件定義にも1〜2ヶ月。オフボードは退職日に間に合わせます。</p>
				</div>
				<div class="lp-card">
					<span class="lp-card-icon"><i class="fa-solid fa-shield-halved"></i></span>
					<h3>運用責任</h3>
					<p>作って終わりにしません。引き継いだ知識は月次で更新・改善し、AIが答えられないときは専任スタッフが対応。「業務が止まらない」状態に責任を持ちます。</p>
				</div>
			</div>
		</div>
	</section>

	<!-- ===== ④ サービスと料金（4段ラダー） ===== -->
	<section class="lp-section lp-bg-light" id="service">
		<div class="lp-inner">
			<div class="lp-section-label">Service &amp; Price</div>
			<h2 class="lp-h2">小さく始めて、必要な分だけ。<br>4つのステップ</h2>
			<p class="lp-lead">まずは無料相談から。全部を任せる必要はありません。「設計だけ」で終えてもかまいません。AI化が進むほど、月額は下がります。</p>

			<div class="lp-ladder">
				<div class="lp-ladder-card is-feature">
					<div class="lp-ladder-num">①</div>
					<div class="lp-ladder-name">無料相談・引き継ぎ診断</div>
					<p class="lp-ladder-desc">現状の引き継ぎ資料と業務を棚卸しし、抜け漏れリスクを可視化（30分・オンライン）</p>
					<div class="lp-ladder-price">無料</div>
				</div>
				<div class="lp-ladder-card">
					<div class="lp-ladder-num">②</div>
					<div class="lp-ladder-name">引き継ぎ設計</div>
					<p class="lp-ladder-desc">ヒアリングで属人業務まで棚卸しし、個別チェックリスト・SOPに落とし込み（実務は持ちません）</p>
					<div class="lp-ladder-price">15〜30万円</div>
				</div>
				<div class="lp-ladder-card">
					<div class="lp-ladder-num">③</div>
					<div class="lp-ladder-name">AIチャットボット</div>
					<p class="lp-ladder-desc">退職者の知識（資料・録画・ヒアリング）をAIに写し取り、後任・チームがいつでも質問できる「引き継ぎボット」に。月次で知識更新・精度改善＋答えられない時は専任スタッフが対応</p>
					<div class="lp-ladder-price">構築20〜40万円＋月3〜10万円</div>
				</div>
				<div class="lp-ladder-card">
					<div class="lp-ladder-num">④</div>
					<div class="lp-ladder-name">AI自動化アプリ</div>
					<p class="lp-ladder-desc">引き継いだ業務そのものをAIが実行する仕組みへ。構築後は運用まで代行</p>
					<div class="lp-ladder-price">構築30〜80万円＋月5〜15万円</div>
				</div>
			</div>

			<div class="lp-ladder-notes">
				<p>⚡ お急ぎの場合：①〜③を10日に圧縮する緊急プランがあります（無料相談時にお申し出ください）</p>
				<p>現在テスト運用中のため、割引価格（通常の50〜70%）でご案内します。</p>
			</div>
			<p class="lp-price-note">※ 金額は目安であり、業務内容・データ量により変動します。診断・提案はAIによる概算を含み、成果を保証するものではありません。</p>

			<div class="lp-ladder-cta">
				<a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>" class="lp-btn-primary">まずは無料相談（30分）→</a>
			</div>
		</div>
	</section>

	<!-- ===== ⑤ 比較表 ===== -->
	<section class="lp-section lp-bg-white" id="compare">
		<div class="lp-inner">
			<div class="lp-section-label">Compare</div>
			<h2 class="lp-h2">派遣・アシスタント・BPOとの違い</h2>
			<p class="lp-lead">後任がいなくても、属人業務でも、辞めた後も。オフボードは「業務が止まらない状態」を作って維持します。</p>

			<div class="lp-compare">
				<table>
					<thead>
						<tr>
							<th></th>
							<th>派遣</th>
							<th>オンラインアシスタント</th>
							<th>BPO会社</th>
							<th class="col-offboard">オフボード</th>
						</tr>
					</thead>
					<tbody>
						<tr><th>立ち上げ</th><td>✕ 1〜2ヶ月</td><td>○ 1週間</td><td>✕ 1〜2ヶ月</td><td class="col-offboard">◎ 最短10日</td></tr>
						<tr><th>属人知識の抽出</th><td>✕ 後任任せ</td><td>✕ 指示待ち</td><td>△ マニュアル化のみ</td><td class="col-offboard">◎ ヒアリング＋AIで抽出</td></tr>
						<tr><th>辞めた後も維持</th><td>✕ その人次第</td><td>△</td><td>○</td><td class="col-offboard">◎ AI＋専任スタッフで維持</td></tr>
					</tbody>
				</table>
			</div>
		</div>
	</section>

	<!-- ===== ⑥ 運営・信頼 ===== -->
	<section class="lp-section lp-bg-light" id="company">
		<div class="lp-inner">
			<div class="lp-section-label">Company</div>
			<h2 class="lp-h2">運営：株式会社ふえん</h2>
			<p class="lp-lead">AIとノーコードで“エンジニアに頼らない”開発を手がけてきたチームが、退職・引き継ぎの現場を支えます。</p>

			<div class="lp-profile">
				<div>
					<?php
				$avatar_path = get_stylesheet_directory() . '/images/ando.jpg';
				$avatar_uri  = get_stylesheet_directory_uri() . '/images/ando.jpg';
				?>
				<div class="lp-profile-avatar">
					<?php if ( file_exists( $avatar_path ) ) : ?>
						<img src="<?php echo esc_url( $avatar_uri ); ?>" alt="安藤昭太">
					<?php else : ?>
						<i class="fa-solid fa-user"></i>
					<?php endif; ?>
				</div>
				</div>
				<div>
					<h3>安藤昭太 ｜ 株式会社ふえん 代表取締役</h3>
					<div class="pf-role">一般社団法人ノーコード推進協会 副代表理事</div>
					<p>AIとノーコードで「エンジニアに頼らない」アプリ・システム開発を支援。退職・休職する社員の業務をAIで引き継ぐ引き取りサービス「オフボード」を運営しています。</p>
					<p class="pf-meta">著書『<b>ノーコードシフト</b>』『<b>現場が動くDX</b>』／ Podcast『<b>聴くDX</b>』『<b>デジタルの仕組みラジオ</b>』</p>
				</div>
			</div>

			<div class="lp-cards" style="margin-top:32px;">
				<div class="lp-card">
					<span class="lp-card-icon"><i class="fa-solid fa-robot"></i></span>
					<h3>① AI実行＋専任スタッフ補助</h3>
					<p>AIが業務を実行し、専任スタッフが監督・例外対応・品質を担保します。</p>
				</div>
				<div class="lp-card">
					<span class="lp-card-icon"><i class="fa-solid fa-lock"></i></span>
					<h3>② データ取扱</h3>
					<p>お預かりするデータは暗号化し、AIの学習には使いません。処理は国内で完結し、契約終了後30日で削除します。</p>
				</div>
			</div>
		</div>
	</section>

	<!-- ===== ⑦ FAQ ===== -->
	<section class="lp-section lp-bg-white" id="faq">
		<div class="lp-inner">
			<div class="lp-section-label">FAQ</div>
			<h2 class="lp-h2">よくあるご質問</h2>

			<div class="lp-faq">
				<div class="lp-faq-item">
					<p class="lp-faq-q">どんな業務が対象ですか？</p>
					<p class="lp-faq-a">経理・営業事務・カスタマーサポート・EC運営など、PC上で完結する業務が対象です。職種は問いません。物理的な作業（現場対応・紙の処理など）は対象外です。</p>
				</div>
				<div class="lp-faq-item">
					<p class="lp-faq-q">担当者がすでに辞めてしまいました。間に合いますか？</p>
					<p class="lp-faq-a">残された資料・メール・データからの復元も可能です。ただし在籍中に始めるのが最も効果的です。退職日が決まった時点で、まずご相談ください。</p>
				</div>
				<div class="lp-faq-item">
					<p class="lp-faq-q">預けたデータの扱いが心配です。</p>
					<p class="lp-faq-a">暗号化して保管し、AIの学習には一切使いません。AI処理は国内のデータセンターで完結し、契約終了後30日ですべて削除します。</p>
				</div>
				<div class="lp-faq-item">
					<p class="lp-faq-q">小さく試せますか？</p>
					<p class="lp-faq-a">はい。②の引き継ぎ設計（チェックリスト・SOP化）だけのご利用も可能です。その後のボット化・自動化は、必要になった時にご検討ください。</p>
				</div>
			</div>
		</div>
	</section>

	<!-- ===== ⑧ 最終CTA ===== -->
	<section class="lp-cta-section" id="contact">
		<div class="lp-inner">
			<h2 class="lp-h2">担当者の退職、<br>引き継ぎは間に合います。</h2>
			<p class="lp-lead">退職日が決まったら、それが始めどきです。30分の無料相談で、何が抜けそうかを一緒に棚卸しします。</p>
			<div class="lp-cta-btns">
				<a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>" class="lp-btn-primary">無料相談（30分）→</a>
			</div>
		</div>
	</section>

</div><!-- .lp-wrap -->

<?php
get_footer();
