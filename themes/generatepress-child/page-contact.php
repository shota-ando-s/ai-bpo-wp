<?php
/**
 * Template Name: お問い合わせページ
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
	body.page-template-page-contact #content.site-content,
	body.page-template-page-contact .site-content.grid-container,
	body.page-template-page-contact .inside-page-wrapper {
		max-width: 100% !important;
		width: 100% !important;
		padding-left: 0 !important;
		padding-right: 0 !important;
		margin-left: 0 !important;
		margin-right: 0 !important;
	}

	/* ===== 共通 ===== */
	.cp-wrap { font-family: 'Noto Sans JP', 'Hiragino Sans', 'Yu Gothic', sans-serif; color: #1a1a2e; width: 100%; overflow-x: hidden; }
	.cp-inner { max-width: 860px; margin: 0 auto; padding: 0 40px; box-sizing: border-box; }

	/* ===== Hero ===== */
	.cp-hero {
		background: linear-gradient(135deg, #0d1b4b 0%, #1a56db 100%);
		color: #fff;
		padding: 72px 40px 64px;
		text-align: center;
	}
	.cp-hero-eyebrow {
		display: inline-block;
		background: rgba(255,255,255,.15);
		border: 1px solid rgba(255,255,255,.3);
		border-radius: 50px;
		padding: 5px 16px;
		font-size: 12px;
		font-weight: 600;
		letter-spacing: .1em;
		margin-bottom: 18px;
	}
	.cp-hero h1 {
		font-size: clamp(1.6rem, 4vw, 2.4rem);
		font-weight: 900;
		line-height: 1.3;
		margin: 0 0 14px;
	}
	.cp-hero-sub {
		font-size: 1rem;
		opacity: .85;
		margin: 0 auto;
		max-width: 500px;
		line-height: 1.7;
	}

	/* ===== 安心ポイント ===== */
	.cp-trust {
		background: #fff;
		padding: 40px 40px 0;
	}
	.cp-trust-list {
		display: flex;
		gap: 16px;
		justify-content: center;
		flex-wrap: wrap;
		list-style: none;
		padding: 0;
		margin: 0;
	}
	.cp-trust-list li {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: .9rem;
		font-weight: 700;
		color: #1a56db;
		background: #f0f4ff;
		border-radius: 50px;
		padding: 10px 20px;
	}
	.cp-trust-list li span { font-size: 1.1rem; }

	/* ===== フォームエリア ===== */
	.cp-form-section {
		background: #fff;
		padding: 56px 40px 80px;
	}
	.cp-form-intro {
		text-align: center;
		margin-bottom: 40px;
	}
	.cp-form-intro h2 {
		font-size: clamp(1.3rem, 3vw, 1.8rem);
		font-weight: 800;
		margin: 0 0 10px;
		color: #1a1a2e;
	}
	.cp-form-intro p {
		font-size: .95rem;
		color: #5a5a7a;
		line-height: 1.7;
		margin: 0;
	}

	/* ===== CF7 スタイリング ===== */
	.cp-form-box {
		background: #f8faff;
		border: 1px solid #e0e7ff;
		border-radius: 20px;
		padding: 48px 48px;
	}
	@media (max-width: 640px) {
		.cp-form-box { padding: 32px 24px; }
	}

	.cf7-field-wrap {
		margin-bottom: 24px;
	}
	.cf7-label {
		display: block;
		font-size: .88rem;
		font-weight: 700;
		color: #2a2a4a;
		margin-bottom: 8px;
	}
	.cf7-required {
		display: inline-block;
		background: #1a56db;
		color: #fff;
		font-size: 10px;
		font-weight: 700;
		padding: 2px 7px;
		border-radius: 4px;
		margin-left: 6px;
		vertical-align: middle;
	}
	.cp-form-box .wpcf7-form input[type="text"],
	.cp-form-box .wpcf7-form input[type="email"],
	.cp-form-box .wpcf7-form input[type="tel"],
	.cp-form-box .wpcf7-form select,
	.cp-form-box .wpcf7-form textarea {
		width: 100%;
		padding: 12px 16px;
		border: 2px solid #e0e7ff;
		border-radius: 10px;
		font-size: .95rem;
		font-family: inherit;
		color: #1a1a2e;
		background: #fff;
		box-sizing: border-box;
		transition: border-color .2s, box-shadow .2s;
		appearance: none;
	}
	.cp-form-box .wpcf7-form input[type="text"]:focus,
	.cp-form-box .wpcf7-form input[type="email"]:focus,
	.cp-form-box .wpcf7-form input[type="tel"]:focus,
	.cp-form-box .wpcf7-form select:focus,
	.cp-form-box .wpcf7-form textarea:focus {
		outline: none;
		border-color: #1a56db;
		box-shadow: 0 0 0 4px rgba(26,86,219,.1);
	}
	.cp-form-box .wpcf7-form select {
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%231a56db' stroke-width='2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: right 16px center;
		padding-right: 40px;
	}
	.cp-form-box .wpcf7-form textarea {
		resize: vertical;
		min-height: 140px;
	}

	/* 同意チェックボックス */
	.cf7-acceptance-wrap {
		margin-bottom: 32px;
		font-size: .9rem;
		color: #4a4a6a;
	}
	.cf7-acceptance-wrap .wpcf7-acceptance {
		display: flex;
		align-items: center;
		gap: 10px;
	}
	.cf7-acceptance-wrap input[type="checkbox"] {
		width: 18px;
		height: 18px;
		accent-color: #1a56db;
		flex-shrink: 0;
		cursor: pointer;
	}
	.cf7-acceptance-wrap a {
		color: #1a56db;
		text-decoration: underline;
	}

	/* 送信ボタン */
	.cp-form-box .wpcf7-form .wpcf7-submit {
		display: block;
		width: 100%;
		background: #ff6b35;
		color: #fff;
		font-size: 1.05rem;
		font-weight: 700;
		padding: 16px 32px;
		border: none;
		border-radius: 50px;
		cursor: pointer;
		box-shadow: 0 8px 30px rgba(255,107,53,.4);
		transition: transform .2s, box-shadow .2s;
		font-family: inherit;
	}
	.cp-form-box .wpcf7-form .wpcf7-submit:hover {
		transform: translateY(-2px);
		box-shadow: 0 12px 40px rgba(255,107,53,.55);
	}

	/* バリデーション */
	.wpcf7-not-valid-tip {
		color: #dc2626;
		font-size: .82rem;
		margin-top: 4px;
		display: block;
	}
	.wpcf7-response-output {
		border-radius: 10px;
		padding: 14px 18px !important;
		font-size: .9rem;
		margin-top: 24px !important;
	}
	.wpcf7-mail-sent-ok {
		background: #f0fdf4 !important;
		border-color: #86efac !important;
		color: #15803d !important;
	}
	.wpcf7-mail-sent-ng,
	.wpcf7-validation-errors {
		background: #fef2f2 !important;
		border-color: #fca5a5 !important;
		color: #dc2626 !important;
	}

	/* ===== よくある質問 ===== */
	.cp-faq-section {
		background: #f5f7ff;
		padding: 72px 40px;
	}
	.cp-faq-section h2 {
		font-size: clamp(1.3rem, 3vw, 1.8rem);
		font-weight: 800;
		text-align: center;
		margin: 0 0 40px;
		color: #1a1a2e;
	}
	.cp-faq-list {
		list-style: none;
		padding: 0;
		margin: 0;
	}
	.cp-faq-item {
		background: #fff;
		border-radius: 12px;
		margin-bottom: 12px;
		overflow: hidden;
	}
	.cp-faq-q {
		display: flex;
		align-items: flex-start;
		gap: 14px;
		padding: 20px 24px;
		font-weight: 700;
		font-size: .95rem;
		color: #1a1a2e;
	}
	.cp-faq-q::before {
		content: 'Q';
		flex-shrink: 0;
		width: 28px;
		height: 28px;
		background: #1a56db;
		color: #fff;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 14px;
		font-weight: 900;
	}
	.cp-faq-a {
		display: flex;
		align-items: flex-start;
		gap: 14px;
		padding: 0 24px 20px;
		font-size: .9rem;
		color: #4a4a6a;
		line-height: 1.7;
		border-top: 1px solid #f0f4ff;
	}
	.cp-faq-a::before {
		content: 'A';
		flex-shrink: 0;
		width: 28px;
		height: 28px;
		background: #ff6b35;
		color: #fff;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 14px;
		font-weight: 900;
		margin-top: -1px;
	}

	/* ===== モバイル調整 ===== */
	@media (max-width: 768px) {
		.cp-hero { padding: 56px 24px 48px; }
		.cp-trust, .cp-form-section, .cp-faq-section { padding-left: 24px; padding-right: 24px; }
		.cp-inner { padding: 0 24px; }
	}
	@media (max-width: 480px) {
		.cp-hero { padding: 48px 16px 40px; }
		.cp-trust, .cp-form-section, .cp-faq-section { padding-left: 16px; padding-right: 16px; }
		.cp-inner { padding: 0 16px; }
	}
	</style>
	<?php
} );

get_header();
?>

<div class="cp-wrap">

	<!-- ===== Hero ===== -->
	<section class="cp-hero">
		<div class="cp-inner">
			<div class="cp-hero-eyebrow">無料相談受付中</div>
			<h1>お問い合わせ・<br>BPO無料相談</h1>
			<p class="cp-hero-sub">業務内容をお聞かせください。AI化できる範囲と<br>削減コストの概算を無料でご提案します。</p>
		</div>
	</section>

	<!-- ===== 安心ポイント ===== -->
	<div class="cp-trust">
		<div class="cp-inner">
			<ul class="cp-trust-list">
				<li><span>🕐</span> 2営業日以内に返信</li>
				<li><span>🔒</span> 秘密厳守・NDA対応可</li>
				<li><span>💬</span> 初回相談は完全無料</li>
				<li><span>📋</span> 見積もりだけでもOK</li>
			</ul>
		</div>
	</div>

	<!-- ===== フォームエリア ===== -->
	<section class="cp-form-section">
		<div class="cp-inner">
			<div class="cp-form-intro">
				<h2>お問い合わせフォーム</h2>
				<p>以下のフォームにご入力の上、送信してください。<br>折り返しご連絡いたします。</p>
			</div>

			<div class="cp-form-box">
				<?php echo do_shortcode('[contact-form-7 id="19"]'); ?>
			</div>
		</div>
	</section>

	<!-- ===== よくある質問 ===== -->
	<section class="cp-faq-section">
		<div class="cp-inner">
			<h2>よくある質問</h2>
			<ul class="cp-faq-list">
				<li class="cp-faq-item">
					<div class="cp-faq-q">相談・見積もりは本当に無料ですか？</div>
					<div class="cp-faq-a">はい、初回のご相談・概算見積もりは完全無料です。業務内容をお聞かせいただいた上で、AI化できる範囲と削減コストの目安をご提案します。</div>
				</li>
				<li class="cp-faq-item">
					<div class="cp-faq-q">どんな業務でも対応できますか？</div>
					<div class="cp-faq-a">Excel・Webシステム・FAX・紙帳票など幅広い業務に対応しています。まずはどんな業務でもご相談ください。対応可能かどうか、担当者が確認してご回答します。</div>
				</li>
				<li class="cp-faq-item">
					<div class="cp-faq-q">導入までどのくらいの期間がかかりますか？</div>
					<div class="cp-faq-a">標準的な業務であれば最短2週間での導入が可能です。業務の複雑さや連携するシステムによって異なりますので、相談時に詳しくお伝えします。</div>
				</li>
				<li class="cp-faq-item">
					<div class="cp-faq-q">情報の取り扱いはどうなっていますか？</div>
					<div class="cp-faq-a">お預かりした情報は厳重に管理し、第三者への提供は一切行いません。NDA（秘密保持契約）のご締結にも対応しております。</div>
				</li>
			</ul>
		</div>
	</section>

</div><!-- .cp-wrap -->

<?php
get_footer();
