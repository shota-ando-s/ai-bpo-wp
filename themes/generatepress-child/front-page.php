<?php
/**
 * LP用フロントページテンプレート — オフボード（退職・引き継ぎ業務の引き取りサービス）
 *
 * @package GeneratePress
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

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
	.lp-bg-dark   { background: #0d1b4b; color: #fff; }

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
	.lp-hero-cta-sub {
		display: inline-block;
		background: rgba(255,255,255,.12);
		color: #fff !important;
		font-size: 1rem;
		font-weight: 600;
		padding: 17px 36px;
		border-radius: 50px;
		text-decoration: none !important;
		border: 2px solid rgba(255,255,255,.45);
		transition: background .2s, border-color .2s;
	}
	.lp-hero-cta-sub:hover { background: rgba(255,255,255,.22); border-color: rgba(255,255,255,.8); }

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

	/* ===== 立ち上げスピード比較グラフ ===== */
	.lp-chart { margin: 48px 0 32px; }
	.lp-chart-row { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
	.lp-chart-label { flex: 0 0 150px; font-size: 14px; font-weight: 700; text-align: right; color: #1a1a2e; }
	.lp-chart-bar-wrap { flex: 1; background: #e8ecff; border-radius: 8px; overflow: hidden; height: 52px; position: relative; }
	.lp-chart-bar {
		height: 100%;
		border-radius: 8px;
		display: flex;
		align-items: center;
		padding-left: 16px;
		font-size: 15px;
		font-weight: 700;
		color: #fff;
		width: 0;
		white-space: nowrap;
		transition: width 1.2s cubic-bezier(.22,1,.36,1);
	}
	.lp-chart-bar.bar-before { background: linear-gradient(90deg, #6b7bb8, #9aa0c8); }
	.lp-chart-bar.bar-after  { background: linear-gradient(90deg, #1a56db, #4f8ef7); }
	.lp-chart-bar.animated   { width: var(--bar-w); }
	.lp-chart-saving {
		margin-top: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 16px;
		background: linear-gradient(135deg, #fff4e0, #ffedd0);
		border: 2px solid #ffd166;
		border-radius: 16px;
		padding: 24px 32px;
	}
	.lp-chart-saving-num {
		font-size: clamp(2.2rem, 6vw, 3.3rem);
		font-weight: 900;
		color: #e85d04;
		line-height: 1;
		white-space: nowrap;
	}
	.lp-chart-saving-text { font-size: 1rem; line-height: 1.5; color: #4a4a6a; }
	.lp-chart-saving-text strong { display: block; font-size: 1.1rem; color: #1a1a2e; }

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

	/* ===== 2カラムセクション ===== */
	.lp-two-col {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 60px;
		align-items: center;
	}
	@media (max-width: 680px) {
		.lp-two-col { grid-template-columns: 1fr; gap: 36px; }
		.lp-two-col .lp-two-col-img { order: -1; }
	}
	.lp-two-col-img {
		background: linear-gradient(135deg, #e8ecff, #c7d2fe);
		border-radius: 20px;
		aspect-ratio: 4/3;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 5rem;
	}
	.lp-two-col .lp-h2 { margin-bottom: 16px; }
	.lp-step-list { list-style: none; padding: 0; margin: 24px 0 0; }
	.lp-step-list li {
		display: flex;
		gap: 14px;
		margin-bottom: 14px;
		font-size: .96rem;
		color: #3a3a5a;
		line-height: 1.6;
	}
	.lp-step-list li::before {
		content: '✓';
		flex-shrink: 0;
		width: 24px;
		height: 24px;
		background: #1a56db;
		color: #fff;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 13px;
		font-weight: 700;
		margin-top: 1px;
	}

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
	.lp-price-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 22px; margin-top: 44px; }
	.lp-price-card { background: #fff; border-radius: 18px; padding: 30px 26px; border: 1.5px solid rgba(26,86,219,.12); box-shadow: 0 4px 20px rgba(26,86,219,.06); text-align: center; }
	.lp-price-card.is-feature { border: 2px solid #ff6b35; box-shadow: 0 10px 34px rgba(255,107,53,.18); }
	.lp-price-card .pc-name { font-size: 1rem; font-weight: 800; color: #1a1a2e; margin-bottom: 10px; }
	.lp-price-card .pc-amt { font-size: 1.8rem; font-weight: 900; color: #1a56db; line-height: 1.2; }
	.lp-price-card.is-feature .pc-amt { color: #e85d04; }
	.lp-price-card .pc-unit { font-size: .8rem; color: #8a8aa0; font-weight: 700; }
	.lp-price-card .pc-desc { font-size: .85rem; color: #5a5a7a; line-height: 1.65; margin-top: 12px; }
	.lp-price-note { font-size: .8rem; color: #999; text-align: center; margin-top: 22px; line-height: 1.7; }

	/* ===== 運営プロフィール ===== */
	.lp-profile { display: grid; grid-template-columns: 200px 1fr; gap: 40px; align-items: center; margin-top: 40px; background: #fff; border-radius: 20px; padding: 40px; box-shadow: 0 4px 24px rgba(26,86,219,.08); }
	@media (max-width: 680px) { .lp-profile { grid-template-columns: 1fr; gap: 24px; text-align: center; } }
	.lp-profile-avatar { width: 160px; height: 160px; border-radius: 50%; background: linear-gradient(135deg, #1a56db, #7c3aed); display: flex; align-items: center; justify-content: center; font-size: 4rem; margin: 0 auto; color: #fff; }
	.lp-profile h3 { font-size: 1.2rem; font-weight: 800; margin: 0 0 6px; }
	.lp-profile .pf-role { font-size: .9rem; color: #1a56db; font-weight: 700; margin-bottom: 14px; }
	.lp-profile p { font-size: .92rem; color: #5a5a7a; line-height: 1.8; margin: 0 0 10px; }
	.lp-profile .pf-meta { font-size: .85rem; color: #6a6a8a; }
	.lp-profile .pf-meta b { color: #1a1a2e; }

	/* ===== 3原則ミニ ===== */
	.lp-principles { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; margin-top: 36px; }
	.lp-principle { background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.14); border-radius: 14px; padding: 22px; }
	.lp-principle h4 { font-size: .95rem; font-weight: 800; margin: 0 0 8px; color: #ffd166; }
	.lp-principle p { font-size: .85rem; line-height: 1.7; margin: 0; color: rgba(255,255,255,.82); }

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
	.lp-btn-secondary {
		display: inline-block;
		background: rgba(255,255,255,.1);
		color: #fff !important;
		font-size: 1rem;
		font-weight: 600;
		padding: 17px 40px;
		border-radius: 50px;
		text-decoration: none !important;
		border: 2px solid rgba(255,255,255,.4);
		transition: background .2s, border-color .2s;
	}
	.lp-btn-secondary:hover { background: rgba(255,255,255,.2); border-color: rgba(255,255,255,.7); }

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
	}
	@media (max-width: 480px) {
		.lp-section { padding: 60px 16px; }
		.lp-inner { padding: 0 16px; }
		.lp-hero { padding: 64px 16px 56px; }
		.lp-chart-label { flex: 0 0 96px; font-size: 12px; }
		.lp-cta-section { padding: 70px 16px; }
		.lp-pain { padding: 60px 16px; }
		.lp-profile { padding: 28px 20px; }
	}
	</style>
	<?php
} );

// 診断ツールURL（外部）
$offboard_tool_url = 'https://offboard.ai-bpo.site';

get_header();
?>

<div class="lp-wrap">

	<!-- ===== Hero ===== -->
	<section class="lp-hero">
		<div class="lp-inner">
			<div class="lp-hero-eyebrow">オフボード ｜ 退職・引き継ぎ業務の引き取りサービス</div>
			<h1>担当者が辞める。<br>その<em>引き継ぎ書</em>、本当に足りていますか？</h1>
			<p class="lp-hero-sub">完璧な引き継ぎ書は、作れない。<br>だからオフボードは、退職・休職する社員の業務を<strong>AIで引き継ぎ、そのまま巻き取り</strong>ます。</p>
			<div class="lp-hero-btns">
				<a href="<?php echo esc_url( $offboard_tool_url ); ?>" target="_blank" rel="noopener" class="lp-hero-cta">無料で引き継ぎ診断（約60秒）→</a>
				<a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>" class="lp-hero-cta-sub">無料相談（30分）</a>
			</div>
			<p class="lp-hero-note">※ 診断は無料・登録不要。タスク一覧表がダウンロードできます</p>
			<div class="lp-urgent">
				<span class="lp-urgent-icon"><i class="fa-solid fa-triangle-exclamation"></i></span>
				<span>退職日が迫っていますか？ 最短<strong>10日で“ボールを落とさない体制”</strong>を作ります。<a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">今すぐ無料相談 →</a></span>
			</div>
		</div>
	</section>

	<!-- ===== こんな課題ありませんか ===== -->
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

			<p class="lp-pain-cta">その引き継ぎ、<span>AIと専任スタッフの組み合わせ</span>で巻き取れます。</p>
		</div>
	</section>

	<!-- ===== Section 1: 立ち上げスピード比較 ===== -->
	<section class="lp-section lp-bg-white" id="speed">
		<div class="lp-inner">
			<div class="lp-section-label">Speed</div>
			<h2 class="lp-h2">後任不在でも、<br>最短<span style="color:#1a56db;">10日</span>で巻き取り開始</h2>
			<p class="lp-lead">派遣の採用にもBPOの要件定義にも1〜2ヶ月。退職日には間に合いません。オフボードはAI＋専任スタッフで、最短10日で「ボールを落とさない体制」を立ち上げます。</p>

			<div class="lp-chart" id="lp-cost-chart">
				<div class="lp-chart-row">
					<div class="lp-chart-label">派遣・BPO</div>
					<div class="lp-chart-bar-wrap">
						<div class="lp-chart-bar bar-before" style="--bar-w:100%">採用・要件定義で 1〜2ヶ月</div>
					</div>
				</div>
				<div class="lp-chart-row">
					<div class="lp-chart-label">オフボード</div>
					<div class="lp-chart-bar-wrap">
						<div class="lp-chart-bar bar-after" style="--bar-w:18%">最短10日</div>
					</div>
				</div>
				<div class="lp-chart-saving">
					<div class="lp-chart-saving-num">10日</div>
					<div class="lp-chart-saving-text">
						<strong>で巻き取りを開始</strong>
						退職者がいるうちに業務を引き取り、抜け漏れをその場で潰します。
					</div>
				</div>
			</div>

			<p style="font-size:11px;color:#999;text-align:right;margin-top:8px;">※ 業務内容・規模により変動します。目安の数値です。</p>
		</div>
	</section>

	<!-- ===== Section 2: どんな引き継ぎに対応できるか ===== -->
	<section class="lp-section lp-bg-light" id="coverage">
		<div class="lp-inner">
			<div class="lp-section-label">Coverage</div>
			<h2 class="lp-h2">後任がいなくても、属人業務でも<br>業務は止めない</h2>
			<p class="lp-lead">職種は問いません。オンラインで完結する業務なら、入ってきた引き継ぎをAIで共通化して巻き取ります。</p>

			<div class="lp-cards">
				<div class="lp-card">
					<span class="lp-card-icon"><i class="fa-solid fa-user-tie"></i></span>
					<h3>後任不在の引き継ぎ</h3>
					<p>後任が決まっていない・育てる時間がない。そのままうちが業務を引き取り、回し続けます。</p>
				</div>
				<div class="lp-card">
					<span class="lp-card-icon"><i class="fa-solid fa-box-archive"></i></span>
					<h3>属人化した業務</h3>
					<p>その人しか知らない手順・判断基準・例外対応を、AIヒアリングで吸い出して仕組みにします。</p>
				</div>
				<div class="lp-card">
					<span class="lp-card-icon"><i class="fa-solid fa-laptop"></i></span>
					<h3>オンラインで完結する業務</h3>
					<p>経理・営業事務・カスタマーサポート・EC運営など、PC上で完結する業務に幅広く対応します。</p>
				</div>
			</div>

			<!-- 競合比較 -->
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
						<tr><th>丸投げできる</th><td>○</td><td>✕ 指示待ち</td><td>◎</td><td class="col-offboard">○ AI＋人</td></tr>
						<tr><th>そのままAI化</th><td>✕</td><td>✕</td><td>△</td><td class="col-offboard">◎ 標準対応</td></tr>
					</tbody>
				</table>
			</div>
		</div>
	</section>

	<!-- ===== Section 3: AIが業務を巻き取って実行 ===== -->
	<section class="lp-section lp-bg-white" id="automation">
		<div class="lp-inner">
			<div class="lp-two-col">
				<div>
					<div class="lp-section-label">AI Execution</div>
					<h2 class="lp-h2">AIが退職者の業務を<br>引き取って自動で実行</h2>
					<p class="lp-lead">オフボードは<strong>AIが業務を実行し、専任スタッフが補助</strong>。人間と同じようにPC画面を認識し、ログイン・入力・確認・送信まで一連の業務を自律的に実行します。退職者がいなくても、業務は止まりません。</p>
					<ul class="lp-step-list">
						<li>退職者は「喋る・画面録画・ファイルを渡す」だけ。手順書はAIが作成</li>
						<li>Webブラウザ・基幹システム・SaaSを問わず操作を巻き取り</li>
						<li>定型業務はAIが無人実行、判断が要る所だけ人へエスカレーション</li>
						<li>専用アカウント方式で、退職後もそのまま業務を継続</li>
					</ul>
				</div>
				<div class="lp-two-col-img" style="background:none;padding:0;" aria-label="AIが入力フォームを操作するイラスト">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" style="width:100%;height:auto;display:block;">
						<defs>
							<linearGradient id="rpa-bg" x1="0%" y1="0%" x2="100%" y2="100%">
								<stop offset="0%" stop-color="#e8ecff"/>
								<stop offset="100%" stop-color="#c7d2fe"/>
							</linearGradient>
							<filter id="rpa-shadow" x="-10%" y="-10%" width="120%" height="130%">
								<feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#1a56db" flood-opacity="0.15"/>
							</filter>
						</defs>
						<circle cx="240" cy="185" r="170" fill="url(#rpa-bg)"/>
						<rect x="48" y="24" width="384" height="272" rx="10" fill="white" filter="url(#rpa-shadow)"/>
						<rect x="48" y="24" width="384" height="34" rx="10" fill="#1a56db"/>
						<rect x="48" y="46" width="384" height="12" fill="#1a56db"/>
						<circle cx="70" cy="41" r="5" fill="#ff5f57" opacity=".85"/>
						<circle cx="86" cy="41" r="5" fill="#ffbd2e" opacity=".85"/>
						<circle cx="102" cy="41" r="5" fill="#28c840" opacity=".85"/>
						<rect x="126" y="31" width="220" height="18" rx="9" fill="rgba(255,255,255,.15)"/>
						<text x="236" y="44" text-anchor="middle" fill="rgba(255,255,255,.75)" font-size="9" font-family="monospace">https://system.client.co.jp/nyuryoku</text>
						<rect x="48" y="58" width="384" height="238" fill="#fafbff"/>
						<rect x="48" y="58" width="384" height="28" fill="#f0f4ff"/>
						<text x="68" y="77" fill="#1a2f5e" font-size="11" font-weight="bold" font-family="sans-serif">受注データ入力フォーム</text>
						<text x="390" y="77" text-anchor="end" fill="#1a56db" font-size="10" font-family="sans-serif">3 / 4 完了</text>
						<text x="68" y="104" fill="#888" font-size="10" font-family="sans-serif">取引先名</text>
						<rect x="68" y="108" width="234" height="24" rx="4" fill="#f0fff4" stroke="#22c55e" stroke-width="1.5"/>
						<text x="78" y="124" fill="#1a2f5e" font-size="11" font-family="sans-serif">株式会社テスト商事</text>
						<circle cx="318" cy="120" r="9" fill="#22c55e"/>
						<path d="M313 120 L317 124 L324 115" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
						<text x="68" y="148" fill="#888" font-size="10" font-family="sans-serif">金額（税抜）</text>
						<rect x="68" y="152" width="234" height="24" rx="4" fill="#f0fff4" stroke="#22c55e" stroke-width="1.5"/>
						<text x="78" y="168" fill="#1a2f5e" font-size="11" font-family="sans-serif">¥ 125,000</text>
						<circle cx="318" cy="164" r="9" fill="#22c55e"/>
						<path d="M313 164 L317 168 L324 159" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
						<text x="68" y="192" fill="#1a56db" font-size="10" font-weight="bold" font-family="sans-serif">担当者</text>
						<rect x="68" y="196" width="234" height="24" rx="4" fill="white" stroke="#1a56db" stroke-width="2"/>
						<text x="78" y="212" fill="#1a2f5e" font-size="11" font-family="sans-serif">田中 太郎</text>
						<rect x="147" y="200" width="1.5" height="16" fill="#1a56db">
							<animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/>
						</rect>
						<text x="68" y="236" fill="#bbb" font-size="10" font-family="sans-serif">処理日付</text>
						<rect x="68" y="240" width="234" height="24" rx="4" fill="#fafafa" stroke="#e0e0e0" stroke-width="1"/>
						<text x="78" y="256" fill="#ccc" font-size="11" font-family="sans-serif">自動入力待ち...</text>
						<rect x="68" y="278" width="344" height="5" rx="2.5" fill="#e8ecff"/>
						<rect x="68" y="278" width="258" height="5" rx="2.5" fill="#1a56db">
							<animate attributeName="width" from="0" to="258" dur="1.5s" fill="freeze"/>
						</rect>
						<text x="68" y="294" fill="#888" font-size="9" font-family="sans-serif">巻き取り進捗: 75%</text>
						<g>
							<animateTransform attributeName="transform" type="translate"
								values="296,145; 296,145; 296,145; 220,196; 220,196; 220,196"
								keyTimes="0; 0.1; 0.4; 0.55; 0.8; 1"
								dur="4s" repeatCount="indefinite"/>
							<path d="M0 0 L0 20 L5 15 L8 23 L12 21 L9 13 L15 13 Z" fill="#ff6b35" stroke="white" stroke-width="1.2"/>
							<circle cx="20" cy="-5" r="13" fill="#1a56db" stroke="white" stroke-width="2"/>
							<text x="20" y="-1" text-anchor="middle" fill="white" font-size="9" font-weight="bold" font-family="sans-serif">AI</text>
							<circle cx="0" cy="0" r="0" fill="none" stroke="#ff6b35" stroke-width="1.5" opacity="0">
								<animate attributeName="r" values="0;20" dur="0.5s" begin="0.5s;4.5s" repeatCount="indefinite"/>
								<animate attributeName="opacity" values="0.8;0" dur="0.5s" begin="0.5s;4.5s" repeatCount="indefinite"/>
							</circle>
						</g>
						<rect x="208" y="296" width="64" height="10" rx="3" fill="#c7d2fe"/>
						<rect x="188" y="306" width="104" height="6" rx="3" fill="#a5b4fc"/>
					</svg>
				</div>
			</div>
		</div>
	</section>

	<!-- ===== Section 4: 人が監督・例外対応 ===== -->
	<section class="lp-section lp-bg-light" id="staff">
		<div class="lp-inner">
			<div class="lp-two-col">
				<div class="lp-two-col-img" style="background:none;padding:0;" aria-label="人がエラーを検知して修正するイラスト">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" style="width:100%;height:auto;display:block;">
						<defs>
							<linearGradient id="hum-bg" x1="0%" y1="0%" x2="100%" y2="100%">
								<stop offset="0%" stop-color="#fff4f0"/>
								<stop offset="100%" stop-color="#ffe4d6"/>
							</linearGradient>
							<filter id="hum-shadow" x="-10%" y="-10%" width="120%" height="130%">
								<feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#e85d04" flood-opacity="0.12"/>
							</filter>
						</defs>
						<circle cx="240" cy="185" r="170" fill="url(#hum-bg)"/>
						<rect x="48" y="24" width="384" height="272" rx="10" fill="white" filter="url(#hum-shadow)"/>
						<rect x="48" y="24" width="384" height="34" rx="10" fill="#dc2626"/>
						<rect x="48" y="46" width="384" height="12" fill="#dc2626"/>
						<circle cx="70" cy="41" r="5" fill="#ff5f57" opacity=".85"/>
						<circle cx="86" cy="41" r="5" fill="#ffbd2e" opacity=".85"/>
						<circle cx="102" cy="41" r="5" fill="#28c840" opacity=".85"/>
						<rect x="126" y="31" width="220" height="18" rx="9" fill="rgba(255,255,255,.15)"/>
						<text x="236" y="44" text-anchor="middle" fill="rgba(255,255,255,.75)" font-size="9" font-family="monospace">https://system.client.co.jp/nyuryoku</text>
						<rect x="48" y="58" width="384" height="238" fill="#fafbff"/>
						<rect x="48" y="58" width="384" height="28" fill="#fff0f0"/>
						<text x="68" y="77" fill="#dc2626" font-size="11" font-weight="bold" font-family="sans-serif">受注データ入力フォーム</text>
						<rect x="68" y="94" width="344" height="36" rx="6" fill="#fef2f2" stroke="#fca5a5" stroke-width="1.5"/>
						<text x="86" y="111" fill="#dc2626" font-size="11" font-weight="bold" font-family="sans-serif">！ 例外: 判断が必要なケースを検知</text>
						<text x="86" y="124" fill="#ef4444" font-size="10" font-family="sans-serif">AIが検知 → 専任スタッフが確認・対応します</text>
						<text x="68" y="150" fill="#888" font-size="10" font-family="sans-serif">取引先名</text>
						<rect x="68" y="154" width="234" height="24" rx="4" fill="#f0fff4" stroke="#22c55e" stroke-width="1.5"/>
						<text x="78" y="170" fill="#1a2f5e" font-size="11" font-family="sans-serif">株式会社テスト商事</text>
						<circle cx="318" cy="166" r="9" fill="#22c55e"/>
						<path d="M313 166 L317 170 L324 161" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
						<text x="68" y="194" fill="#dc2626" font-size="10" font-weight="bold" font-family="sans-serif">金額（税抜） ← 確認してください</text>
						<rect x="68" y="198" width="234" height="24" rx="4" fill="#fff0f0" stroke="#dc2626" stroke-width="2"/>
						<text x="78" y="214" fill="#dc2626" font-size="11" font-family="sans-serif">125000円</text>
						<circle cx="318" cy="210" r="9" fill="#dc2626"/>
						<text x="318" y="214" text-anchor="middle" fill="white" font-size="12" font-weight="bold" font-family="sans-serif">!</text>
						<text x="68" y="238" fill="#888" font-size="10" font-family="sans-serif">担当者</text>
						<rect x="68" y="242" width="234" height="24" rx="4" fill="#f0fff4" stroke="#22c55e" stroke-width="1.5"/>
						<text x="78" y="258" fill="#1a2f5e" font-size="11" font-family="sans-serif">田中 太郎</text>
						<circle cx="318" cy="254" r="9" fill="#22c55e"/>
						<path d="M313 254 L317 258 L324 249" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
						<rect x="68" y="274" width="100" height="26" rx="13" fill="#dc2626"/>
						<text x="118" y="291" text-anchor="middle" fill="white" font-size="11" font-weight="bold" font-family="sans-serif">対応する</text>
						<rect x="178" y="274" width="80" height="26" rx="13" fill="none" stroke="#ccc" stroke-width="1.5"/>
						<text x="218" y="291" text-anchor="middle" fill="#999" font-size="11" font-family="sans-serif">スキップ</text>
						<g>
							<animateTransform attributeName="transform" type="translate"
								values="280,230; 280,230; 118,268; 118,268; 118,268; 280,230"
								keyTimes="0; 0.2; 0.45; 0.6; 0.8; 1"
								dur="4s" repeatCount="indefinite"/>
							<path d="M6 22 C6 22 4 20 4 15 L4 6 C4 4.3 5.3 3 7 3 C8.7 3 10 4.3 10 6 L10 12 C10.4 11.4 11.1 11 12 11 C13.1 11 14 11.9 14 13 L14 14 C14.4 13.4 15.1 13 16 13 C17.1 13 18 13.9 18 15 L18 16 C18.4 15.4 19.1 15 20 15 C21.1 15 22 15.9 22 17 L22 22 C22 26.4 18.4 30 14 30 L12 30 C9.8 30 7.8 29.1 6.3 27.6 Z"
								fill="#f97316" stroke="white" stroke-width="1"/>
							<circle cx="9" cy="16" r="0" fill="none" stroke="#f97316" stroke-width="1.5" opacity="0">
								<animate attributeName="r" values="0;22" dur="0.5s" begin="1.9s;5.9s" repeatCount="indefinite"/>
								<animate attributeName="opacity" values="0.8;0" dur="0.5s" begin="1.9s;5.9s" repeatCount="indefinite"/>
							</circle>
						</g>
						<rect x="208" y="296" width="64" height="10" rx="3" fill="#fca5a5"/>
						<rect x="188" y="306" width="104" height="6" rx="3" fill="#f87171"/>
					</svg>
				</div>
				<div>
					<div class="lp-section-label">Human + AI</div>
					<h2 class="lp-h2">専任スタッフが監督し<br>例外と品質を担保</h2>
					<p class="lp-lead">AIは完璧ではありません。判断が要る業務・イレギュラーは、AIと協働が得意な専任スタッフ（人SV）が対応。<strong>退職者が在籍しているうちに実際の業務を試運転</strong>し、抜け漏れをその場で潰します。</p>
					<ul class="lp-step-list">
						<li>退職者の暗黙知（判断基準・例外・トラブル例）を人が深掘りヒアリング</li>
						<li>AIの処理結果を専任スタッフがリアルタイムで監視・承認</li>
						<li>退職前に実務を試運転し、ボールを落とさない体制を確立</li>
						<li>巻き取った業務はSOP化し、月次で精度と自動化率を改善</li>
					</ul>
				</div>
			</div>
		</div>
	</section>

	<!-- ===== Section 5: 引き継ぎの流れ ===== -->
	<section class="lp-section" id="workflow" style="background:linear-gradient(160deg,#f0f4ff 0%,#f8faff 60%,#ede9fe 100%);">
		<div class="lp-inner">
			<div class="lp-section-label">How It Works</div>
			<h2 class="lp-h2">引き継ぎから、その先のAI化まで</h2>
			<p class="lp-lead">まずは無料診断で「何が抜けているか」を可視化。そこから巻き取り、AI化まで一気通貫で対応します。</p>

			<div style="position:relative;margin-top:56px;max-width:680px;margin-left:auto;margin-right:auto;">

				<div style="position:absolute;left:35px;top:72px;bottom:72px;width:3px;background:linear-gradient(to bottom,#1a56db 0%,#7c3aed 100%);border-radius:2px;opacity:.25;"></div>

				<?php
				$intro_steps = [
					['01', 'fa-magnifying-glass', '無料で引き継ぎ診断',          '業種と辞める担当業務を選んで質問に答えるだけ。抜けやすいタスクを一覧化し、引き継ぎ漏れのリスクを「金額」で可視化します。',  '約60秒'],
					['02', 'fa-microphone',       '退職者ヒアリング（書かせない）', '退職者は「喋る・画面録画・ファイルを渡す」だけ。文書化はAIが肩代わりし、属人知を吸い出します。',                       '数日'],
					['03', 'fa-bolt',             '緊急巻き取り＋試運転',  '退職者が在籍しているうちにAI＋人で実務を引き取り、抜け漏れをその場で潰します。',                                     '最短10日'],
					['04', 'fa-rocket',           'AI化・運用代行',              '巻き取った業務を仕組み化して月額で継続運用。AI化が進むほど料金は下がります。',                                       '継続的'],
				];
				$colors = ['#1a56db','#4f46e5','#7c3aed','#6d28d9'];
				foreach ($intro_steps as $i => $step) {
					$is_last = ($i === count($intro_steps) - 1);
					$color   = $colors[$i];
					?>
					<div style="display:flex;gap:20px;align-items:center;margin-bottom:<?php echo $is_last ? '0' : '20px'; ?>;">
						<div style="flex-shrink:0;position:relative;z-index:1;width:70px;height:70px;border-radius:50%;background:#fff;border:3px solid <?php echo $color; ?>;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 4px 20px rgba(99,102,241,.18);">
							<span style="font-size:.6rem;font-weight:900;color:<?php echo $color; ?>;letter-spacing:.08em;line-height:1;"><?php echo $step[0]; ?></span>
							<span style="font-size:1.4rem;line-height:1.2;color:<?php echo $color; ?>;"><i class="fa-solid <?php echo $step[1]; ?>"></i></span>
						</div>
						<div style="flex:1;min-width:0;background:#fff;border-radius:18px;padding:22px 26px;box-shadow:0 2px 20px rgba(99,102,241,.09);border:1.5px solid rgba(99,102,241,.1);">
							<div style="display:flex;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:10px;">
								<span style="font-size:1rem;font-weight:800;color:#1a1a3c;flex:1;min-width:0;"><?php echo $step[2]; ?></span>
								<span style="font-size:.72rem;font-weight:700;color:#fff;background:<?php echo $color; ?>;border-radius:20px;padding:3px 12px;white-space:nowrap;flex-shrink:0;"><?php echo $step[4]; ?></span>
							</div>
							<p style="font-size:.88rem;color:#5a5a7a;margin:0;line-height:1.75;"><?php echo $step[3]; ?></p>
						</div>
					</div>
					<?php
				}
				?>
			</div>

			<div style="margin-top:52px;text-align:center;">
				<a href="<?php echo esc_url( $offboard_tool_url ); ?>" target="_blank" rel="noopener" class="lp-btn-primary" style="box-shadow:0 10px 36px rgba(255,107,53,.35);">まずは無料で引き継ぎ診断 →</a>
			</div>
		</div>
	</section>

	<!-- ===== Section 6: 料金 ===== -->
	<section class="lp-section lp-bg-white" id="price">
		<div class="lp-inner">
			<div class="lp-section-label">Price</div>
			<h2 class="lp-h2">料金</h2>
			<p class="lp-lead">まずは無料診断から。巻き取りは緊急対応として立ち上げ、AI化が進むほど月額は下がります。</p>

			<div class="lp-price-grid">
				<div class="lp-price-card">
					<div class="pc-name">引き継ぎ診断</div>
					<div class="pc-amt">無料</div>
					<div class="pc-desc">タスク棚卸し・漏れリスクの可視化・一覧表ダウンロード</div>
				</div>
				<div class="lp-price-card">
					<div class="pc-name">引き継ぎ設計のみ</div>
					<div class="pc-amt">20<span class="pc-unit">万円〜</span></div>
					<div class="pc-desc">巻き取りが難しい業務の棚卸し・SOP化まで（実務は持たない）</div>
				</div>
				<div class="lp-price-card is-feature">
					<div class="pc-name">緊急巻き取り</div>
					<div class="pc-amt">着手40<span class="pc-unit">万円</span></div>
					<div class="pc-desc">＋ 緊急運用 月40万円（2〜3ヶ月）。10日でボールを落とさない体制を確立</div>
				</div>
				<div class="lp-price-card">
					<div class="pc-name">AI化・運用代行</div>
					<div class="pc-amt">月30<span class="pc-unit">万円〜</span></div>
					<div class="pc-desc">巻き取った業務を継続運用。AI化が進むほど逓減</div>
				</div>
			</div>
			<p class="lp-price-note">現在テスト運用中のため、割引価格（通常の50〜70%）でご案内します。<br>※ 金額・診断結果はAIによる概算であり、成果を保証するものではありません。</p>
		</div>
	</section>

	<!-- ===== Section 7: 運営・信頼 ===== -->
	<section class="lp-section lp-bg-light" id="company">
		<div class="lp-inner">
			<div class="lp-section-label">Company</div>
			<h2 class="lp-h2">運営：ふえん株式会社</h2>
			<p class="lp-lead">AIとノーコードで“エンジニアに頼らない”開発を手がけてきたチームが、退職・引き継ぎの現場を支えます。</p>

			<div class="lp-profile">
				<div>
					<div class="lp-profile-avatar"><i class="fa-solid fa-user"></i></div>
				</div>
				<div>
					<h3>安藤 ｜ ふえん株式会社 代表取締役</h3>
					<div class="pf-role">富士通から独立 ／ 一般社団法人ノーコード推進協会 副代表理事</div>
					<p>AIとノーコードで「エンジニアに頼らない」アプリ・システム開発を支援。退職・休職する社員の業務をAIで引き継ぐ代行サービス「オフボード」を運営しています。</p>
					<p class="pf-meta">著書『<b>ノーコードシフト</b>』『<b>現場が動くDX</b>』／ Podcast『<b>聴くDX</b>』『<b>デジタルの仕組みラジオ</b>』</p>
				</div>
			</div>
		</div>
	</section>

	<!-- ===== 最終CTA ===== -->
	<section class="lp-cta-section" id="contact">
		<div class="lp-inner">
			<h2 class="lp-h2">担当者の退職、<br>引き継ぎは間に合います。</h2>
			<p class="lp-lead">まずは60秒の無料診断で「何が抜けているか」を確かめてください。退職日が近い方は、そのままご相談ください。</p>
			<div class="lp-cta-btns">
				<a href="<?php echo esc_url( $offboard_tool_url ); ?>" target="_blank" rel="noopener" class="lp-btn-primary">無料で引き継ぎ診断 →</a>
				<a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>" class="lp-btn-secondary">無料相談（30分）</a>
			</div>

			<div class="lp-principles">
				<div class="lp-principle">
					<h4>① AI実行＋専任スタッフ補助</h4>
					<p>AIが業務を実行し、専任スタッフが監督・例外対応・品質を担保します。</p>
				</div>
				<div class="lp-principle">
					<h4>② 責任分界</h4>
					<p>準委任契約。無料診断はAIによる概算で、成果を保証するものではありません。</p>
				</div>
				<div class="lp-principle">
					<h4>③ データ取扱</h4>
					<p>お預かりするデータは暗号化・AI学習には不使用。契約終了後30日で削除します。</p>
				</div>
			</div>
		</div>
	</section>

</div><!-- .lp-wrap -->

<script>
(function() {
	var bars = document.querySelectorAll('.lp-chart-bar');
	if (!bars.length) return;

	var animated = false;
	function animateBars() {
		if (animated) return;
		animated = true;
		bars.forEach(function(bar) {
			bar.classList.add('animated');
		});
	}

	var chart = document.getElementById('lp-cost-chart');
	if (!chart) return;

	if ('IntersectionObserver' in window) {
		var observer = new IntersectionObserver(function(entries) {
			if (entries[0].isIntersecting) {
				setTimeout(animateBars, 200);
				observer.disconnect();
			}
		}, { threshold: 0.3 });
		observer.observe(chart);
	} else {
		animateBars();
	}
})();
</script>

<?php
get_footer();
