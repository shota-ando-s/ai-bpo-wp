<?php
/**
 * ヒキツギAI ランディングページ 本体マークアップ
 *
 * front-page.php から include される。
 * tools/build-lp-preview.php からも同じファイルを読み込んで静的HTMLを生成するため、
 * WordPress 関数には依存せず、呼び出し側が渡す変数だけを使う。
 *
 * @var string $lp_home     サイトルートURL
 * @var string $lp_contact  クロージングフォームへのアンカー
 * @var string $lp_privacy  プライバシーポリシーURL
 * @var string $lp_tokusho  特定商取引法に基づく表記URL
 * @var string $lp_company  運営会社サイトURL
 * @var string $lp_archives 記事一覧URL
 */

if ( ! isset( $lp_home ) )     { $lp_home     = '/'; }
if ( ! isset( $lp_contact ) )  { $lp_contact  = '#contact'; }
if ( ! isset( $lp_privacy ) )  { $lp_privacy  = '/privacy-policy/'; }
if ( ! isset( $lp_tokusho ) )  { $lp_tokusho  = '/tokushoho/'; }
if ( ! isset( $lp_company ) )  { $lp_company  = 'https://fuenn.co.jp/'; }
if ( ! isset( $lp_archives ) ) { $lp_archives = '/archives/'; }

/* 課題提起カードのアイコン（インラインSVG／外部フォント不使用） */
$lp_icons = array(
	'message'  => '<path d="M4 5.5h16v10H9.5L5.5 19v-3.5H4z"/>',
	'key'      => '<circle cx="8" cy="12" r="3.5"/><path d="M11.5 12H20M17 12v3M20 12v3"/>',
	'search'   => '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l4.5 4.5"/>',
	'document' => '<path d="M6 3.5h8l4 4v13H6z"/><path d="M14 3.5v4h4"/><path d="M9 12.5h6M9 16h4"/>',
	'stack'    => '<path d="M12 3.5 3.5 8l8.5 4.5L20.5 8z"/><path d="M3.5 13l8.5 4.5L20.5 13"/>',
	'clock'    => '<circle cx="12" cy="12" r="8"/><path d="M12 7.5V12l3.5 2"/>',
);

$lp_problems = array(
	array( 'message',  '産休に入る本人に、休み中も連絡してしまっている' ),
	array( 'key',      '「前任者しか知らない」取引先の事情がある' ),
	array( 'search',   '過去のやり取りは残っているが、探せない' ),
	array( 'document', '毎月の請求書発行を、誰がやるか決まっていない' ),
	array( 'stack',    '引き継いだ人の仕事が、単純に倍になった' ),
	array( 'clock',    '引き継ぐ本人が、産休直前まで残業している' ),
);
?>

<!-- ============================================================
     ヘッダー
     ============================================================ -->
<header class="sticky top-0 z-40 border-b border-line bg-white/90 backdrop-blur">
	<div class="lp-shell flex h-14 items-center justify-between sm:h-16">
		<a href="<?php echo htmlspecialchars( $lp_home, ENT_QUOTES ); ?>" class="text-base font-bold tracking-tight text-ink sm:text-lg">
			ヒキツギAI
		</a>
		<nav class="flex items-center gap-4 text-xs sm:gap-7 sm:text-sm" aria-label="主要導線">
			<!-- 資料PDFを用意したら href を差し替える -->
			<a href="#offer" class="text-muted transition-colors hover:text-ink">資料ダウンロード</a>
			<a href="#contact" class="font-medium text-ink underline decoration-line underline-offset-4 transition-colors hover:decoration-ink">相談する</a>
		</nav>
	</div>
</header>

<main id="lp-main">

	<!-- ============================================================
	     1. トップ（ファーストビュー）
	     ============================================================ -->
	<section class="bg-paper pb-14 pt-12 sm:pb-20 sm:pt-20 md:pb-28 md:pt-28">
		<div class="lp-shell">

			<!-- inline-block で折り返し位置を制御（狭い画面でも「引き継ぎ書が／役に立った試しがない。」で割れる） -->
			<h1 class="text-[1.75rem] font-bold leading-[1.5] tracking-tight sm:text-[2.75rem] sm:leading-[1.4] md:text-[3.5rem] md:leading-[1.35]">
				<span class="inline-block">引き継ぎ書が</span><span class="inline-block">役に立った試しがない。</span>
			</h1>

			<!-- 断定と解説を切り離す余白（このブロック最重要の指示） -->
			<div class="h-[4.5rem] sm:h-28 md:h-36" aria-hidden="true"></div>

			<div class="max-w-[34ch] sm:max-w-none">
				<p class="text-[1.0625rem] font-bold leading-[1.85] sm:text-xl md:text-[1.375rem]">
					原因は、人ではなく方法にあります。
				</p>
				<p class="mt-2 text-[1.0625rem] leading-[1.85] text-ink-soft sm:mt-3 sm:text-xl md:text-[1.375rem]">
					ヒキツギAIは人よりも速く、正確に<br>知識と作業を引き継ぎます。
				</p>
			</div>

			<div class="mt-9 flex flex-col items-stretch gap-3 sm:mt-12 sm:flex-row sm:items-center sm:gap-5">
				<a href="#contact" class="lp-btn-primary">無料で業務チェックリストを受け取る</a>
				<!-- 資料PDFを用意したら href を差し替える -->
				<a href="#offer" class="lp-btn-ghost">3分でわかる資料</a>
			</div>

			<div class="mt-10 sm:mt-16">
				<!-- IMAGE: Slack上でヒキツギAIが質問に回答し、作業完了を報告している画面 -->
				<div class="lp-imgph aspect-[16/10] sm:aspect-[16/9]">
					<span>IMAGE：Slack上でヒキツギAIが質問に回答し、<br class="sm:hidden">作業完了を報告している画面</span>
				</div>
			</div>

		</div>
	</section>

	<!-- ============================================================
	     2. 課題提起
	     ============================================================ -->
	<section id="problems" class="lp-section bg-white">
		<div class="lp-shell">
			<h2 class="lp-h2">引き継ぎ、こうなっていませんか？</h2>

			<ul class="mt-8 grid gap-3 sm:mt-12 sm:grid-cols-2 sm:gap-4 lg:gap-5">
				<?php foreach ( $lp_problems as $lp_i => $lp_p ) : ?>
					<li class="flex items-start gap-4 rounded-lg border border-line bg-paper p-5 sm:p-6">
						<svg class="mt-0.5 h-6 w-6 shrink-0 text-muted" viewBox="0 0 24 24" fill="none"
						     stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
						     aria-hidden="true"><?php echo $lp_icons[ $lp_p[0] ]; ?></svg>
						<p class="text-[0.9375rem] font-medium leading-[1.8] sm:text-base"><?php echo htmlspecialchars( $lp_p[1], ENT_QUOTES ); ?></p>
					</li>
				<?php endforeach; ?>
			</ul>
		</div>
	</section>

	<!-- ============================================================
	     3. オファー（LPで最も重要／唯一のダーク面＋囲み）
	     ============================================================ -->
	<section id="offer" class="lp-section bg-ink text-white">
		<div class="lp-shell">
			<h2 class="lp-h2">まず、引き継ぎの棚卸しから<wbr>始めませんか。</h2>

			<div class="mt-8 rounded-xl border border-line-dark bg-ink-deep p-6 sm:mt-12 sm:p-10 md:p-12">
				<p class="lp-eyebrow text-muted-dark">無料でご提供するもの</p>

				<ol class="mt-6 space-y-7 sm:mt-8 sm:space-y-9">
					<li class="grid grid-cols-[1.75rem_1fr] gap-x-3 sm:grid-cols-[2.5rem_1fr] sm:gap-x-4">
						<span class="text-lg font-bold leading-[1.6] text-accent sm:text-2xl" aria-hidden="true">①</span>
						<div>
							<h3 class="lp-h3">業務チェックリスト</h3>
							<p class="mt-2 text-sm leading-[1.9] text-muted-dark sm:text-[0.9375rem]">
								引き継ぎが必要な業務を洗い出すためのリストです。<br class="hidden sm:inline">ヒキツギAIを使わない場合でも、そのままお使いいただけます。
							</p>
						</div>
					</li>
					<li class="grid grid-cols-[1.75rem_1fr] gap-x-3 sm:grid-cols-[2.5rem_1fr] sm:gap-x-4">
						<span class="text-lg font-bold leading-[1.6] text-accent sm:text-2xl" aria-hidden="true">②</span>
						<div>
							<h3 class="lp-h3">対応可能業務の整理</h3>
							<p class="mt-2 text-sm leading-[1.9] text-muted-dark sm:text-[0.9375rem]">
								洗い出した業務のうち、どれをAIに引き継げるかを仕分けします。
							</p>
						</div>
					</li>
					<li class="grid grid-cols-[1.75rem_1fr] gap-x-3 sm:grid-cols-[2.5rem_1fr] sm:gap-x-4">
						<span class="text-lg font-bold leading-[1.6] text-accent sm:text-2xl" aria-hidden="true">③</span>
						<div>
							<h3 class="lp-h3">引き継ぎ方法のご提案</h3>
							<p class="mt-2 text-sm leading-[1.9] text-muted-dark sm:text-[0.9375rem]">
								AIに任せる業務、人が引き継ぐ業務、それぞれの進め方をお伝えします。
							</p>
						</div>
					</li>
				</ol>

				<p class="mt-8 border-t border-line-dark pt-6 text-sm leading-[1.9] text-muted-dark sm:mt-10 sm:pt-7 sm:text-[0.9375rem]">
					ご相談・お見積もりは無料です。最低利用期間の縛りもありません。
				</p>

				<div class="mt-7 sm:mt-9">
					<a href="#contact" class="lp-btn-primary">無料で業務チェックリストを受け取る</a>
				</div>
			</div>
		</div>
	</section>

	<!-- ============================================================
	     4. 解決策・カテゴリ定義（知識／作業の2軸図解）
	     ============================================================ -->
	<section class="lp-section bg-paper">
		<div class="lp-shell">
			<h2 class="lp-h2">引き継ぎ書をつくるのではなく、<br class="hidden sm:inline">引き継ぎ担当者をつくる。</h2>

			<div class="mt-9 sm:mt-14">
				<!-- 列見出し（PCのみ） -->
				<div class="hidden md:grid md:grid-cols-[5.5rem_1fr_1fr] md:gap-x-5 md:pb-3">
					<span></span>
					<span class="lp-eyebrow">これまで</span>
					<span class="lp-eyebrow text-accent-deep">ヒキツギAI</span>
				</div>

				<div class="space-y-10 md:space-y-3">
					<?php
					$lp_axes = array(
						array(
							'label'  => '知識',
							'before' => array( '書いて残す', '書いた時点で古い' ),
							'after'  => array( '読み込んで、答える', 'ログが増えるほど正確に' ),
						),
						array(
							'label'  => '作業',
							'before' => array( '人が引き受ける', '引き継いだ人の負担増' ),
							'after'  => array( 'AIが引き受ける', '負担は増えない' ),
						),
					);
					foreach ( $lp_axes as $lp_ax ) :
						?>
						<div class="md:grid md:grid-cols-[5.5rem_1fr_1fr] md:items-stretch md:gap-x-5">

							<!-- 軸ラベル（PCでは行の高さいっぱいに伸ばして2軸構造を強調） -->
							<div class="mb-3 flex md:mb-0 md:h-full">
								<span class="inline-flex items-center justify-center rounded bg-ink px-3 py-1.5 text-sm font-bold tracking-[0.1em] text-white md:w-full md:py-0 md:text-base">
									<?php echo htmlspecialchars( $lp_ax['label'], ENT_QUOTES ); ?>
								</span>
							</div>

							<!-- これまで -->
							<div class="rounded-lg border border-line bg-white/70 p-5 sm:p-6">
								<span class="lp-eyebrow md:hidden">これまで</span>
								<p class="text-base font-bold leading-[1.7] text-muted md:mt-0 mt-2 md:text-lg"><?php echo htmlspecialchars( $lp_ax['before'][0], ENT_QUOTES ); ?></p>
								<p class="mt-1.5 text-sm leading-[1.8] text-muted"><?php echo htmlspecialchars( $lp_ax['before'][1], ENT_QUOTES ); ?></p>
							</div>

							<!-- 矢印（SPのみ） -->
							<div class="flex justify-center py-1.5 md:hidden" aria-hidden="true">
								<svg class="h-5 w-5 text-line" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M6 13l6 6 6-6"/></svg>
							</div>

							<!-- ヒキツギAI -->
							<div class="rounded-lg border-2 border-ink bg-white p-5 sm:p-6">
								<span class="lp-eyebrow text-accent-deep md:hidden">ヒキツギAI</span>
								<p class="mt-2 text-base font-bold leading-[1.7] text-ink md:mt-0 md:text-lg"><?php echo htmlspecialchars( $lp_ax['after'][0], ENT_QUOTES ); ?></p>
								<p class="mt-1.5 text-sm leading-[1.8] text-ink-soft"><?php echo htmlspecialchars( $lp_ax['after'][1], ENT_QUOTES ); ?></p>
							</div>

						</div>
					<?php endforeach; ?>
				</div>
			</div>
		</div>
	</section>

	<!-- ============================================================
	     5. 選ばれる理由
	     ============================================================ -->
	<section class="lp-section bg-white">
		<div class="lp-shell">
			<h2 class="lp-h2">一度つくれば、あとはAIが繰り返します。</h2>

			<p class="lp-lead mt-6 max-w-[42em] text-ink-soft sm:mt-8">
				ヒキツギAIは、御社の業務をそのまま引き継ぐようにつくります。<br class="hidden sm:inline">テンプレートに業務を合わせるのではなく、いま回っているやり方をAIに移します。
			</p>

			<div class="mt-9 sm:mt-14">
				<div class="hidden md:grid md:grid-cols-2 md:gap-x-5 md:pb-3">
					<span class="lp-eyebrow">人に頼む場合</span>
					<span class="lp-eyebrow text-accent-deep">ヒキツギAIの場合</span>
				</div>

				<div class="space-y-4 md:space-y-3">
					<?php
					$lp_reasons = array(
						array( '依頼するたびに時間が発生', '最初に設計し、あとは自動で繰り返す' ),
						array( '量が増えれば費用も増える', '量が増えても、費用は増えない' ),
						array( '担当者が変われば振り出し', '仕組みは残り続ける' ),
					);
					foreach ( $lp_reasons as $lp_r ) :
						?>
						<div class="grid gap-2 md:grid-cols-2 md:gap-x-5">
							<div class="rounded-lg border border-line bg-paper px-5 py-4 sm:px-6 sm:py-5">
								<span class="lp-eyebrow md:hidden">人に頼む場合</span>
								<p class="mt-1.5 text-[0.9375rem] leading-[1.8] text-muted md:mt-0 md:text-base"><?php echo htmlspecialchars( $lp_r[0], ENT_QUOTES ); ?></p>
							</div>
							<div class="rounded-lg border-2 border-ink bg-white px-5 py-4 sm:px-6 sm:py-5">
								<span class="lp-eyebrow text-accent-deep md:hidden">ヒキツギAIの場合</span>
								<p class="mt-1.5 text-[0.9375rem] font-bold leading-[1.8] text-ink md:mt-0 md:text-base"><?php echo htmlspecialchars( $lp_r[1], ENT_QUOTES ); ?></p>
							</div>
						</div>
					<?php endforeach; ?>
				</div>
			</div>

			<div class="mt-12 rounded-lg bg-paper p-6 sm:mt-16 sm:p-10">
				<p class="lp-eyebrow">ご相談いただく業務の例</p>
				<ul class="mt-5 grid gap-x-8 gap-y-3 sm:mt-6 sm:grid-cols-2">
					<?php
					$lp_tasks = array(
						'請求書の発行と送付',
						'入金消込・売上集計',
						'定例レポートの作成',
						'問い合わせメールの一次返信',
						'CRM・スプレッドシートへのデータ入力',
						'定型的な社内申請の処理',
					);
					foreach ( $lp_tasks as $lp_t ) :
						?>
						<li class="flex items-start gap-2.5 text-[0.9375rem] leading-[1.8] sm:text-base">
							<span class="mt-px shrink-0 text-muted" aria-hidden="true">▸</span>
							<span><?php echo htmlspecialchars( $lp_t, ENT_QUOTES ); ?></span>
						</li>
					<?php endforeach; ?>
				</ul>
				<p class="mt-7 text-sm leading-[1.9] text-ink-soft sm:text-[0.9375rem]">
					上記に限りません。「これは人にしかできない」と思っている業務ほど、<br class="hidden sm:inline">一度ご相談ください。
				</p>
			</div>
		</div>
	</section>

	<!-- ============================================================
	     6. セキュリティ
	     ※ ISMAP／ISMS の表記は一字一句変更しないこと
	     ============================================================ -->
	<section class="lp-section bg-paper">
		<div class="lp-shell">
			<h2 class="lp-h2">社内のやり取りを読ませることに、<br class="hidden sm:inline">不安はありませんか。</h2>

			<div class="mt-9 grid gap-4 sm:mt-14 sm:gap-5 md:grid-cols-2">

				<div class="rounded-lg border border-line bg-white p-6 sm:p-8">
					<p class="lp-eyebrow">基盤</p>
					<p class="mt-4 text-[0.9375rem] leading-[2] sm:text-base">
						日本政府が求めるセキュリティ基準（ISMAP）に登録された<br class="hidden lg:inline">クラウド基盤上で稼働しています。<br class="hidden lg:inline">政府機関が採用する水準の環境で、御社のデータをお預かりします。
					</p>
				</div>

				<div class="rounded-lg border border-line bg-white p-6 sm:p-8">
					<p class="lp-eyebrow">データ管理</p>
					<p class="mt-4 text-[0.9375rem] leading-[2] sm:text-base">
						ISMSに準拠した体制で運用しています。（認証は取得手続き中）
					</p>
					<ul class="mt-5 space-y-2.5">
						<?php
						$lp_sec = array(
							'入力されたデータをAIの学習に使用しません',
							'データはすべて国内で保管します',
							'誰がどの情報にアクセスできるか、チャンネル・フォルダ単位で制御します',
						);
						foreach ( $lp_sec as $lp_s ) :
							?>
							<li class="flex items-start gap-2.5 text-[0.9375rem] leading-[1.85]">
								<span class="mt-px shrink-0 text-muted" aria-hidden="true">▸</span>
								<span><?php echo htmlspecialchars( $lp_s, ENT_QUOTES ); ?></span>
							</li>
						<?php endforeach; ?>
					</ul>
				</div>

			</div>
		</div>
	</section>

	<!-- ============================================================
	     7. 先行導入募集
	     ============================================================ -->
	<section class="lp-section bg-white">
		<div class="lp-shell">
			<div class="rounded-xl border-2 border-ink p-6 sm:p-10 md:p-14">
				<h2 class="lp-h2">先行導入3社を募集しています。</h2>

				<p class="mt-6 text-[1.0625rem] font-bold leading-[1.9] sm:mt-8 sm:text-xl">
					初期設計費を半額でご提供します。
				</p>
				<p class="mt-4 text-[0.9375rem] leading-[2] text-ink-soft sm:text-base">
					その代わり、導入後の効果を事例として<br class="hidden sm:inline">公開させていただきます。
				</p>

				<dl class="mt-8 grid gap-3 border-t border-line pt-6 sm:mt-10 sm:grid-cols-2 sm:gap-6 sm:pt-8">
					<div class="flex items-baseline gap-4">
						<dt class="lp-eyebrow w-10 shrink-0">対象</dt>
						<dd class="text-[0.9375rem] leading-[1.8] sm:text-base">3社</dd>
					</div>
					<div class="flex items-baseline gap-4">
						<dt class="lp-eyebrow w-10 shrink-0">条件</dt>
						<dd class="text-[0.9375rem] leading-[1.8] sm:text-base">導入プロセスと効果測定へのご協力</dd>
					</div>
				</dl>
			</div>
		</div>
	</section>

	<!-- ============================================================
	     8-1. 料金の考え方（金額は書かない）
	     ============================================================ -->
	<section class="lp-section bg-paper">
		<div class="lp-shell">
			<h2 class="lp-h2">料金の考え方</h2>

			<ul class="mt-8 space-y-4 sm:mt-12 sm:space-y-5">
				<li class="flex items-start gap-3 text-[0.9375rem] leading-[1.9] sm:text-base">
					<span class="mt-px shrink-0 text-muted" aria-hidden="true">▸</span>
					<span>初期設計費 ＋ 月額の2本立てです</span>
				</li>
				<li class="flex items-start gap-3 text-[0.9375rem] leading-[1.9] sm:text-base">
					<span class="mt-px shrink-0 text-muted" aria-hidden="true">▸</span>
					<span>月額は、引き継ぐ業務の範囲で決まります<br>
						<span class="text-sm text-muted sm:text-[0.9375rem]">人時ではなく業務単位。作業量が増えても料金は比例しません</span>
					</span>
				</li>
				<li class="flex items-start gap-3 text-[0.9375rem] leading-[1.9] sm:text-base">
					<span class="mt-px shrink-0 text-muted" aria-hidden="true">▸</span>
					<span>最低利用期間の縛りはありません</span>
				</li>
				<li class="flex items-start gap-3 text-[0.9375rem] leading-[1.9] sm:text-base">
					<span class="mt-px shrink-0 text-muted" aria-hidden="true">▸</span>
					<span>初期のご相談・お見積もりは無料です</span>
				</li>
				<li class="flex items-start gap-3 text-[0.9375rem] leading-[1.9] sm:text-base">
					<span class="mt-px shrink-0 text-muted" aria-hidden="true">▸</span>
					<span>IT導入補助金の対象です</span>
				</li>
				<li class="flex items-start gap-3 text-[0.9375rem] leading-[1.9] sm:text-base">
					<span class="mt-px shrink-0 text-muted" aria-hidden="true">▸</span>
					<span>先行導入3社は、初期設計費が半額になります</span>
				</li>
			</ul>

			<p class="mt-9 border-t border-line pt-7 text-[0.9375rem] leading-[2] text-ink-soft sm:mt-12 sm:pt-9 sm:text-base">
				業務チェックリストで棚卸しを行ったうえで、<br class="hidden sm:inline">御社の業務量に合わせた概算をその場でお出しします。
			</p>
		</div>
	</section>

	<!-- ============================================================
	     8-2. 代表の言葉
	     ============================================================ -->
	<section class="lp-section bg-white">
		<div class="lp-shell">
			<h2 class="lp-h2">なぜ、この会社がこれをつくるのか</h2>

			<div class="mt-8 grid gap-7 sm:mt-12 md:grid-cols-[15rem_1fr] md:gap-10">

				<!-- IMAGE: 代表の顔写真 -->
				<div class="lp-imgph aspect-[4/5] max-w-[15rem]">
					<span>IMAGE：代表の顔写真</span>
				</div>

				<!-- TEXT: 本文は後日差し込み。300〜500字程度 -->
				<div class="rounded-lg border border-dashed border-line p-6 sm:p-8">
					<p class="lp-eyebrow">代表の言葉（300〜500字）はここに入ります</p>
					<div class="mt-5 space-y-3" aria-hidden="true">
						<div class="h-3.5 w-full rounded bg-paper"></div>
						<div class="h-3.5 w-full rounded bg-paper"></div>
						<div class="h-3.5 w-[92%] rounded bg-paper"></div>
						<div class="h-3.5 w-full rounded bg-paper"></div>
						<div class="h-3.5 w-[78%] rounded bg-paper"></div>
						<div class="h-6"></div>
						<div class="h-3.5 w-full rounded bg-paper"></div>
						<div class="h-3.5 w-[95%] rounded bg-paper"></div>
						<div class="h-3.5 w-full rounded bg-paper"></div>
						<div class="h-3.5 w-[64%] rounded bg-paper"></div>
					</div>
					<p class="mt-7 text-sm text-muted">株式会社不縁　代表</p>
				</div>

			</div>
		</div>
	</section>

	<!-- ============================================================
	     8-3. クロージングCTA・フォーム
	     ============================================================ -->
	<section id="contact" class="lp-section bg-ink text-white">
		<div class="lp-shell">

			<p class="text-[1.5rem] font-bold leading-[1.5] tracking-tight sm:text-[2rem] md:text-[2.5rem] md:leading-[1.4]">
				<span class="inline-block">引き継ぎ書が</span><span class="inline-block">役に立った試しがない。</span>
			</p>
			<div class="h-12 sm:h-20" aria-hidden="true"></div>
			<p class="text-base font-bold leading-[1.85] sm:text-lg md:text-xl">原因は、人ではなく方法にあります。</p>
			<p class="mt-2 text-base leading-[1.85] text-muted-dark sm:text-lg md:text-xl">
				ヒキツギAIは人よりも速く、正確に<br>知識と作業を引き継ぎます。
			</p>

			<!-- 送信先は後日接続する -->
			<form class="mt-10 rounded-xl bg-white p-6 text-ink sm:mt-14 sm:p-10 md:p-12"
			      action="#" method="post" novalidate>

				<div class="grid gap-5 sm:grid-cols-2 sm:gap-6">

					<div class="sm:col-span-2">
						<label for="lp-company-name" class="block text-sm font-bold">
							会社名 <span class="lp-required">必須</span>
						</label>
						<input id="lp-company-name" name="company" type="text" required autocomplete="organization"
						       class="lp-field">
					</div>

					<div>
						<label for="lp-name" class="block text-sm font-bold">
							氏名 <span class="lp-required">必須</span>
						</label>
						<input id="lp-name" name="name" type="text" required autocomplete="name"
						       class="lp-field">
					</div>

					<div>
						<label for="lp-email" class="block text-sm font-bold">
							ビジネスメール <span class="lp-required">必須</span>
						</label>
						<input id="lp-email" name="email" type="email" required autocomplete="email" inputmode="email"
						       class="lp-field">
					</div>

					<div>
						<label for="lp-headcount" class="block text-sm font-bold">
							従業員数 <span class="lp-required">必須</span>
						</label>
						<select id="lp-headcount" name="headcount" required
						        class="lp-field lp-select">
							<option value="">選択してください</option>
							<option value="1-10">〜10名</option>
							<option value="11-50">11〜50名</option>
							<option value="51-100">51〜100名</option>
							<option value="101-">101名以上</option>
						</select>
					</div>

					<div>
						<label for="lp-timing" class="block text-sm font-bold">
							引き継ぎ予定時期 <span class="lp-required">必須</span>
						</label>
						<select id="lp-timing" name="timing" required
						        class="lp-field lp-select">
							<option value="">選択してください</option>
							<option value="1m">1ヶ月以内</option>
							<option value="3m">3ヶ月以内</option>
							<option value="6m">半年以内</option>
							<option value="unknown">未定</option>
						</select>
					</div>

					<div class="sm:col-span-2">
						<label class="flex items-start gap-3 rounded-md bg-paper p-4">
							<input name="early_adopter" type="checkbox" value="1"
							       class="mt-0.5 h-5 w-5 shrink-0 rounded border-line accent-ink">
							<span class="text-[0.9375rem] leading-[1.7]">先行導入3社への応募を希望する</span>
						</label>
					</div>

				</div>

				<div class="mt-8">
					<button type="submit" class="lp-btn-primary sm:w-full">業務チェックリストを受け取る</button>
					<p class="mt-4 text-center text-xs leading-[1.8] text-muted sm:text-[0.8125rem]">
						※ しつこい営業は行いません。まずは可否のご相談だけでも歓迎です。
					</p>
				</div>

			</form>
		</div>
	</section>

</main>

<!-- ============================================================
     8-4. フッター
     ============================================================ -->
<footer class="bg-ink-deep py-12 text-muted-dark sm:py-16">
	<div class="lp-shell">
		<div class="flex flex-col gap-8 md:flex-row md:items-start md:justify-between">

			<div>
				<p class="text-base font-bold text-white">ヒキツギAI</p>
				<p class="mt-3 text-sm leading-[1.9]">
					運営：株式会社不縁<br>
					<!-- 住所・電話番号を確定したらここに追記 -->
				</p>
			</div>

			<nav class="flex flex-col gap-3 text-sm sm:flex-row sm:gap-7" aria-label="フッター">
				<a href="<?php echo htmlspecialchars( $lp_company, ENT_QUOTES ); ?>" class="transition-colors hover:text-white">会社情報</a>
				<a href="<?php echo htmlspecialchars( $lp_tokusho, ENT_QUOTES ); ?>" class="transition-colors hover:text-white">特定商取引法に基づく表記</a>
				<a href="<?php echo htmlspecialchars( $lp_privacy, ENT_QUOTES ); ?>" class="transition-colors hover:text-white">プライバシーポリシー</a>
				<a href="<?php echo htmlspecialchars( $lp_archives, ENT_QUOTES ); ?>" class="transition-colors hover:text-white">記事一覧</a>
			</nav>

		</div>

		<p class="mt-10 border-t border-line-dark pt-6 text-xs text-muted-dark/70">
			&copy; <?php echo htmlspecialchars( gmdate( 'Y' ), ENT_QUOTES ); ?> 株式会社不縁
		</p>
	</div>
</footer>

<!-- ============================================================
     追従CTAバー（スクロール30%以降・フォーム表示中は隠す）
     ============================================================ -->
<div id="lp-sticky" class="lp-sticky" aria-hidden="true">
	<div class="mx-auto w-full max-w-3xl">
		<a href="#contact" class="lp-btn-primary w-full sm:w-full">無料で業務チェックリストを受け取る</a>
	</div>
</div>

<script>
(function () {
	var bar = document.getElementById('lp-sticky');
	var form = document.getElementById('contact');
	if (!bar) return;

	var formVisible = false;
	var ticking = false;

	function update() {
		var el = document.documentElement;
		var max = el.scrollHeight - el.clientHeight;
		var ratio = max > 0 ? (window.pageYOffset || el.scrollTop) / max : 0;
		var show = ratio >= 0.3 && !formVisible;
		bar.classList.toggle('is-visible', show);
		bar.setAttribute('aria-hidden', show ? 'false' : 'true');
	}

	if ('IntersectionObserver' in window && form) {
		new IntersectionObserver(function (entries) {
			formVisible = entries[0].isIntersecting;
			update();
		}, { threshold: 0 }).observe(form);
	}

	window.addEventListener('scroll', function () {
		if (ticking) return;
		ticking = true;
		window.requestAnimationFrame(function () {
			ticking = false;
			update();
		});
	}, { passive: true });
	window.addEventListener('resize', update, { passive: true });

	update();
})();
</script>
