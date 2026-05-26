<?php
/**
 * LP用フロントページテンプレート
 *
 * @package GeneratePress
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'wp_head', function() {
	?>
	<style>
	/* ===== LP 共通 ===== */
	.lp-wrap { font-family: 'Noto Sans JP', 'Hiragino Sans', 'Yu Gothic', sans-serif; color: #1a1a2e; }
	.lp-section { padding: 80px 20px; }
	.lp-inner { max-width: 960px; margin: 0 auto; }
	.lp-section-label { font-size: 13px; font-weight: 700; letter-spacing: .15em; text-transform: uppercase; color: #1a56db; margin-bottom: 12px; }
	.lp-h2 { font-size: clamp(1.5rem, 4vw, 2.2rem); font-weight: 800; line-height: 1.35; margin: 0 0 20px; }
	.lp-lead { font-size: 1.05rem; color: #4a4a6a; line-height: 1.8; margin-bottom: 0; }
	.lp-bg-white  { background: #fff; }
	.lp-bg-light  { background: #f5f7ff; }
	.lp-bg-dark   { background: #0d1b4b; color: #fff; }

	/* ===== Hero ===== */
	.lp-hero {
		background: linear-gradient(135deg, #0d1b4b 0%, #1a56db 100%);
		color: #fff;
		padding: 100px 20px 90px;
		text-align: center;
		position: relative;
		overflow: hidden;
	}
	.lp-hero::before {
		content: '';
		position: absolute; inset: 0;
		background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
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
		font-size: clamp(2rem, 6vw, 3.2rem);
		font-weight: 900;
		line-height: 1.2;
		margin: 0 0 16px;
		text-shadow: 0 2px 20px rgba(0,0,0,.2);
	}
	.lp-hero h1 em {
		font-style: normal;
		color: #ffd166;
	}
	.lp-hero-sub {
		font-size: clamp(1rem, 2.5vw, 1.2rem);
		opacity: .85;
		margin: 0 auto 40px;
		max-width: 600px;
		line-height: 1.7;
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

	/* ===== コスト比較グラフ ===== */
	.lp-chart { margin: 48px 0 32px; }
	.lp-chart-row { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
	.lp-chart-label { flex: 0 0 120px; font-size: 14px; font-weight: 700; text-align: right; color: #1a1a2e; }
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
		font-size: clamp(2.2rem, 6vw, 3.5rem);
		font-weight: 900;
		color: #e85d04;
		line-height: 1;
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
	.lp-card-icon { font-size: 2.4rem; margin-bottom: 16px; display: block; }
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

	/* ===== フロー図 ===== */
	.lp-flow {
		display: flex;
		flex-wrap: wrap;
		gap: 0;
		margin-top: 48px;
		justify-content: center;
	}
	.lp-flow-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		position: relative;
	}
	.lp-flow-item:not(:last-child)::after {
		content: '→';
		position: absolute;
		right: -16px;
		top: 28px;
		font-size: 1.4rem;
		color: #1a56db;
	}
	.lp-flow-box {
		background: #fff;
		border: 2px solid #c7d2fe;
		border-radius: 12px;
		width: 130px;
		padding: 16px 10px;
		font-size: .85rem;
		font-weight: 700;
		line-height: 1.4;
		position: relative;
	}
	.lp-flow-box .flow-icon { font-size: 1.8rem; display: block; margin-bottom: 8px; }
	.lp-flow-arrow { width: 40px; display: flex; align-items: center; justify-content: center; font-size: 1.6rem; color: #1a56db; margin-top: 26px; }
	.lp-flow-wrap {
		display: flex;
		align-items: flex-start;
		gap: 0;
		flex-wrap: wrap;
		justify-content: center;
		row-gap: 20px;
	}
	.lp-flow-step { display: flex; align-items: center; }

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
		padding: 80px 20px;
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

	/* ===== モバイル調整 ===== */
	@media (max-width: 480px) {
		.lp-section { padding: 60px 16px; }
		.lp-chart-label { flex: 0 0 80px; font-size: 12px; }
		.lp-cta-section { padding: 70px 16px; }
		.lp-pain { padding: 60px 16px; }
	}
	</style>
	<?php
} );

get_header();
?>

<div class="lp-wrap">

	<!-- ===== Hero ===== -->
	<section class="lp-hero">
		<div class="lp-inner">
			<div class="lp-hero-eyebrow">AI × BPO — 次世代の業務委託</div>
			<h1>AIで業務コストを<em>半額</em>に<br>現場の業務をそのままAIが自動化</h1>
			<p class="lp-hero-sub">ExcelもFAXも紙帳票も、複雑な業務フローもすべて対応。<br>AIが得意なスタッフが品質を守り、コストを大幅に削減します。</p>
			<a href="#contact" class="lp-hero-cta">無料相談はこちら →</a>
			<p class="lp-hero-note">※ 初回相談無料・導入実績多数</p>
		</div>
	</section>

	<!-- ===== こんな課題ありませんか ===== -->
	<section class="lp-pain">
		<div class="lp-inner">
			<div class="lp-pain-label">Your Challenges</div>
			<h2 class="lp-h2">こんな課題、<br>ありませんか？</h2>

			<div class="lp-pain-items">
				<div class="lp-pain-item">
					<div class="lp-pain-item-icon">🧓</div>
					<div class="lp-pain-item-body">
						<h3>ベテラン社員の<br>退職が決まった</h3>
						<p>長年の業務知識やノウハウが属人化していて、退職後の引き継ぎが不安…</p>
					</div>
				</div>
				<div class="lp-pain-item">
					<div class="lp-pain-item-icon">🔍</div>
					<div class="lp-pain-item-body">
						<h3>採用・育成できず<br>業務が回らない</h3>
						<p>求人を出しても集まらず、育てる余裕もない。現場のしわ寄せが続いている…</p>
					</div>
				</div>
				<div class="lp-pain-item">
					<div class="lp-pain-item-icon">📋</div>
					<div class="lp-pain-item-body">
						<h3>事務作業が増えすぎて<br>お客様と話せない</h3>
						<p>入力・集計・確認作業に追われて、本来やるべき顧客対応の時間が取れない…</p>
					</div>
				</div>
			</div>

			<p class="lp-pain-cta">その課題、<span>AIと専任スタッフの組み合わせ</span>で解決できます。</p>
		</div>
	</section>

	<!-- ===== Section 1: コスト比較グラフ ===== -->
	<section class="lp-section lp-bg-white" id="cost">
		<div class="lp-inner">
			<div class="lp-section-label">Cost Reduction</div>
			<h2 class="lp-h2">AIによる自動化で<br>既存BPOの<span style="color:#1a56db;">半額</span>を実現</h2>
			<p class="lp-lead">従来型BPOと比較して、人件費・管理費を大幅に圧縮。同じ業務量をAIが担うことで、コストを約50%削減します。</p>

			<div class="lp-chart" id="lp-cost-chart">
				<div class="lp-chart-row">
					<div class="lp-chart-label">従来型 BPO</div>
					<div class="lp-chart-bar-wrap">
						<div class="lp-chart-bar bar-before" style="--bar-w:100%">¥500,000 /月</div>
					</div>
				</div>
				<div class="lp-chart-row">
					<div class="lp-chart-label">AI-BPO</div>
					<div class="lp-chart-bar-wrap">
						<div class="lp-chart-bar bar-after" style="--bar-w:50%">¥250,000 /月</div>
					</div>
				</div>
				<div class="lp-chart-saving">
					<div class="lp-chart-saving-num">50<small style="font-size:.5em">%</small></div>
					<div class="lp-chart-saving-text">
						<strong>コスト削減を実現</strong>
						月25万円・年間300万円のコストを削減。品質は維持したまま、スリムな運用体制へ。
					</div>
				</div>
			</div>

			<p style="font-size:11px;color:#999;text-align:right;margin-top:8px;">※ 業務内容・規模により変動します。目安の数値です。</p>
		</div>
	</section>

	<!-- ===== Section 2: 対応範囲 ===== -->
	<section class="lp-section lp-bg-light" id="coverage">
		<div class="lp-inner">
			<div class="lp-section-label">Compatibility</div>
			<h2 class="lp-h2">ExcelもWebもFAXも紙も<br>あらゆる業務に対応</h2>
			<p class="lp-lead">現場で使っているツールや帳票を変える必要はありません。今の業務フローのまま、AIが自動化を担います。</p>

			<div class="lp-cards">
				<div class="lp-card">
					<span class="lp-card-icon">📊</span>
					<h3>Excel・スプレッドシート</h3>
					<p>集計・転記・チェック・メール送信まで、Excelを使った繰り返し作業をすべて自動化します。</p>
				</div>
				<div class="lp-card">
					<span class="lp-card-icon">🌐</span>
					<h3>Webシステム・基幹システム</h3>
					<p>社内システムやSaaS、ERPへのデータ入力・照合・出力をAIが人間と同じ操作で実行します。</p>
				</div>
				<div class="lp-card">
					<span class="lp-card-icon">📠</span>
					<h3>FAX・紙帳票</h3>
					<p>FAXで受信した帳票や紙書類をOCRとAIで読み取り、そのままシステムへ自動入力します。</p>
				</div>
			</div>
		</div>
	</section>

	<!-- ===== Section 3: AI自動化 ===== -->
	<section class="lp-section lp-bg-white" id="automation">
		<div class="lp-inner">
			<div class="lp-two-col">
				<div>
					<div class="lp-section-label">AI Automation</div>
					<h2 class="lp-h2">画面を見て、入力する<br>その操作もAIが行います</h2>
					<p class="lp-lead">AIは人間と同じようにPCの画面を認識し、クリック・入力・確認まで自律的に実行。RPAより柔軟に、例外にも対応します。</p>
					<ul class="lp-step-list">
						<li>画面キャプチャから状況を理解し、適切な操作を判断</li>
						<li>Webブラウザ・デスクトップアプリを問わず操作可能</li>
						<li>ログイン・ナビゲーション・データ入力・送信まで一貫実行</li>
						<li>RPAと異なり、画面変更があっても柔軟に対応</li>
					</ul>
				</div>
				<div class="lp-two-col-img" aria-hidden="true">🤖</div>
			</div>
		</div>
	</section>

	<!-- ===== Section 4: スタッフサポート ===== -->
	<section class="lp-section lp-bg-light" id="staff">
		<div class="lp-inner">
			<div class="lp-two-col">
				<div class="lp-two-col-img" aria-hidden="true">🧑‍💼</div>
				<div>
					<div class="lp-section-label">Human + AI</div>
					<h2 class="lp-h2">AIが得意なスタッフが<br>不備を即修正・品質を担保</h2>
					<p class="lp-lead">AIは完璧ではありません。イレギュラーな案件・AIが判断できないケースは、AIと協働が得意な専任スタッフが迅速に対処します。</p>
					<ul class="lp-step-list">
						<li>AIの処理結果をスタッフがリアルタイムで監視</li>
						<li>エラー検知→人手対応→再学習のサイクルで精度向上</li>
						<li>お客様の業務知識を蓄積し、AIの自動化率を継続改善</li>
						<li>月次レポートで稼働状況・精度・削減効果を可視化</li>
					</ul>
				</div>
			</div>
		</div>
	</section>

	<!-- ===== Section 5: 業務フロー管理 ===== -->
	<section class="lp-section lp-bg-white" id="workflow">
		<div class="lp-inner">
			<div class="lp-section-label">Workflow Management</div>
			<h2 class="lp-h2">複雑な業務フローも<br>AIで一元管理</h2>
			<p class="lp-lead">受付→処理→確認→通知→アーカイブまで、複数ステップにまたがる業務フロー全体をAIが自動でオーケストレーション。担当者への通知や例外処理も含めて管理します。</p>

			<div class="lp-flow-wrap" style="margin-top:48px;gap:0;display:flex;align-items:center;justify-content:center;flex-wrap:wrap;row-gap:16px;">
				<?php
				$flow_steps = [
					['📥', '受付<br>（FAX/Web/<br>メール）'],
					['🔍', 'AI読取<br>&amp;分類'],
					['⚙️', 'AI自動<br>処理・入力'],
					['✅', 'スタッフ<br>品質確認'],
					['📤', '完了通知<br>&amp;アーカイブ'],
				];
				$last = count($flow_steps) - 1;
				foreach ($flow_steps as $i => $step) {
					?>
					<div class="lp-flow-step">
						<div class="lp-flow-box">
							<span class="flow-icon"><?php echo $step[0]; ?></span>
							<?php echo $step[1]; ?>
						</div>
						<?php if ($i < $last): ?>
						<div class="lp-flow-arrow">→</div>
						<?php endif; ?>
					</div>
					<?php
				}
				?>
			</div>

			<div style="margin-top:48px;background:#f0f4ff;border-radius:16px;padding:32px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:24px;text-align:center;">
				<div>
					<div style="font-size:2rem;font-weight:900;color:#1a56db;">99<small style="font-size:.5em">%</small></div>
					<div style="font-size:.85rem;color:#5a5a7a;margin-top:4px;">処理完了率<br>（月次平均）</div>
				</div>
				<div>
					<div style="font-size:2rem;font-weight:900;color:#1a56db;">24h</div>
					<div style="font-size:.85rem;color:#5a5a7a;margin-top:4px;">自動処理対応<br>深夜・休日も稼働</div>
				</div>
				<div>
					<div style="font-size:2rem;font-weight:900;color:#1a56db;">50<small style="font-size:.5em">%↓</small></div>
					<div style="font-size:.85rem;color:#5a5a7a;margin-top:4px;">平均コスト削減率<br>（導入実績より）</div>
				</div>
				<div>
					<div style="font-size:2rem;font-weight:900;color:#1a56db;">2<small style="font-size:.5em">週間</small></div>
					<div style="font-size:.85rem;color:#5a5a7a;margin-top:4px;">最短導入期間<br>（標準業務の場合）</div>
				</div>
			</div>
		</div>
	</section>

	<!-- ===== 最終CTA ===== -->
	<section class="lp-cta-section" id="contact">
		<div class="lp-inner">
			<h2 class="lp-h2">まずは無料相談から<br>はじめましょう</h2>
			<p class="lp-lead">現在の業務内容をお聞かせいただければ、AI化できる範囲・削減コストの概算を無料でご提案します。</p>
			<div class="lp-cta-btns">
				<a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>" class="lp-btn-primary">無料相談を申し込む →</a>
				<a href="<?php echo esc_url( home_url( '/case/' ) ); ?>" class="lp-btn-secondary">導入事例を見る</a>
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
