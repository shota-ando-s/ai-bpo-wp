<?php

/**
 * LPのクロージングフォームに使う Contact Form 7 のフォームID。
 * 管理画面「お問い合わせ」→「LP：業務チェックリスト請求」。
 * 送信先メール・自動返信・Slack通知の設定はCF7側（DB）が持つ。
 */
define( 'HIKITSUGI_LP_CF7_ID', 1092 );

// ページビューカウンター（記事閲覧時にカウントアップ）
add_action( 'wp_head', function () {
	if ( ! is_single() ) return;
	global $post;
	$count = (int) get_post_meta( $post->ID, 'post_views_count', true );
	update_post_meta( $post->ID, 'post_views_count', $count + 1 );
} );

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style(
		'generatepress-child',
		get_stylesheet_uri(),
		[ 'generate-style' ],
		wp_get_theme()->get( 'Version' )
	);

	// Font Awesome 6（記事側アイコン用。LPでは使わない）
	if ( ! is_front_page() ) {
		wp_enqueue_style(
			'font-awesome',
			'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
			[],
			'6.5.1'
		);
	}
} );

/**
 * フロントページ（LP）は LP専用CSS（＋Google Fonts）のみを読む。
 * GeneratePress／子テーマのCSSは競合するので外す。
 *
 * assets/lp.css は手書き（ビルド不要）。レイアウトはマークアップ側の
 * インラインスタイルが持っているので、このCSSは @keyframes・:hover・
 * スクロール連動の状態・グローバル指定だけを担当する。
 */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_front_page() ) {
		return;
	}

	foreach ( [ 'generate-style', 'generate-style-grid', 'generate-mobile-style', 'generatepress-child', 'font-awesome' ] as $handle ) {
		wp_dequeue_style( $handle );
		wp_deregister_style( $handle );
	}

	wp_enqueue_style(
		'hikitsugi-lp-fonts',
		'https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap',
		[],
		null
	);

	$lp_css_path = get_stylesheet_directory() . '/assets/lp.css';
	wp_enqueue_style(
		'hikitsugi-lp',
		get_stylesheet_directory_uri() . '/assets/lp.css',
		[ 'hikitsugi-lp-fonts' ],
		file_exists( $lp_css_path ) ? (string) filemtime( $lp_css_path ) : wp_get_theme()->get( 'Version' )
	);
}, 100 );

// Google Fonts はレンダリングブロックになるので preconnect を先に張る
add_filter( 'wp_resource_hints', function ( $urls, $relation ) {
	if ( 'preconnect' !== $relation || ! is_front_page() ) {
		return $urls;
	}
	$urls[] = [ 'href' => 'https://fonts.googleapis.com' ];
	$urls[] = [ 'href' => 'https://fonts.gstatic.com', 'crossorigin' => 'anonymous' ];
	return $urls;
}, 10, 2 );

// カードサムネイル用に 1280×670 のカスタムサイズを登録
add_action( 'after_setup_theme', function () {
	add_image_size( 'card-thumb', 1280, 670, true );
} );

// 著者名（by aibpo）を非表示
add_filter( 'generate_post_author', '__return_false' );

// コメント機能を全無効化
add_filter( 'comments_open', '__return_false', 20, 2 );
add_filter( 'pings_open', '__return_false', 20, 2 );
add_filter( 'comments_array', '__return_empty_array', 10, 2 );

/**
 * ヘッダーロゴを子テーマ同梱の画像に固定する。
 * カスタマイザー（custom_logo）の設定より優先されるので、
 * ロゴ差し替えはこのファイルと images/ の入れ替えで完結する。
 */
add_filter( 'generate_logo', function () {
	return get_stylesheet_directory_uri() . '/images/hikitsugi_logo.png';
} );

// メディアライブラリ経由ではないので寸法が付かない。CLS防止に明示する（実寸 1000×250）。
add_filter( 'generate_logo_attributes', function ( $attr ) {
	$attr['width']  = 1000;
	$attr['height'] = 250;
	return $attr;
} );

// ロゴの下にキャッチフレーズを表示
add_action( 'generate_after_logo', function() {
	$description = get_bloginfo( 'description' );
	if ( $description ) {
		echo '<p class="site-tagline">' . esc_html( $description ) . '</p>';
	}
} );

/* トップページ: 新着記事・ランキングをグリッド外（フッター直前）に出力
 *
 * ※ このフックは発火しない（デッドコード）。front-page.php を LP 専用の
 *    独立ドキュメントに作り替えた際に get_footer() を呼ばなくなったため。
 *
 *    「LPに記事一覧を戻したくなったら移植する」と書いていた件は対応済み。
 *    現在の新着記事は lp-markup.php の「11 新着記事」セクションが出しており、
 *    データは front-page.php の WP_Query が作る。
 *    ここに残っているのはランキング表示だけが未移植だからで、
 *    （投稿ページのサイドバーのランキングもピックアップに置き換えたため、
 *    閲覧数ランキングを表示している箇所は現在どこにもない）
 */
add_action( 'generate_before_footer', function() {
	if ( ! is_front_page() ) return;
	?>
	<div class="top-sections-wrapper">

		<section class="top-section top-latest">
			<h2 class="top-section-title">新着記事</h2>
			<div class="top-card-grid">
				<?php
				$latest = new WP_Query( [
					'posts_per_page' => 9,
					'post_status'    => 'publish',
				] );
				while ( $latest->have_posts() ) : $latest->the_post(); ?>
					<a class="top-card" href="<?php the_permalink(); ?>">
						<div class="top-card-thumb">
							<?php if ( has_post_thumbnail() ) :
								the_post_thumbnail( 'full' );
							else : ?>
								<div class="top-card-thumb-placeholder"></div>
							<?php endif; ?>
						</div>
						<div class="top-card-body">
							<?php $cats = get_the_category();
							if ( $cats ) : ?>
								<span class="top-card-cat"><?php echo esc_html( $cats[0]->name ); ?></span>
							<?php endif; ?>
							<h3 class="top-card-title"><?php the_title(); ?></h3>
							<time class="top-card-date" datetime="<?php echo esc_attr( get_the_date( 'Y-m-d' ) ); ?>"><?php echo esc_html( get_the_date( 'Y.m.d' ) ); ?></time>
						</div>
					</a>
				<?php endwhile; wp_reset_postdata(); ?>
			</div>
			<div class="top-section-more">
				<a href="<?php echo esc_url( home_url( '/archives/' ) ); ?>" class="top-more-btn">記事一覧を見る</a>
			</div>
		</section>

		<section class="top-section top-ranking">
			<h2 class="top-section-title">ランキング</h2>
			<ol class="top-ranking-list">
				<?php
				$has_views = get_posts( [
					'posts_per_page' => 1,
					'meta_key'       => 'post_views_count',
					'fields'         => 'ids',
				] );
				$ranking_args = ! empty( $has_views ) ? [
					'posts_per_page' => 10,
					'post_status'    => 'publish',
					'meta_key'       => 'post_views_count',
					'orderby'        => 'meta_value_num',
					'order'          => 'DESC',
				] : [
					'posts_per_page' => 10,
					'post_status'    => 'publish',
					'orderby'        => 'date',
					'order'          => 'DESC',
				];
				$ranking = new WP_Query( $ranking_args );
				$rank = 1;
				while ( $ranking->have_posts() ) : $ranking->the_post();
					$views = (int) get_post_meta( get_the_ID(), 'post_views_count', true );
					?>
					<li class="top-ranking-item">
						<a href="<?php the_permalink(); ?>">
							<span class="top-rank-num rank-<?php echo (int) $rank; ?>"><?php echo (int) $rank; ?></span>
							<div class="top-rank-thumb">
								<?php if ( has_post_thumbnail() ) :
									the_post_thumbnail( 'medium' );
								else : ?>
									<div class="top-card-thumb-placeholder"></div>
								<?php endif; ?>
							</div>
							<div class="top-rank-body">
								<?php $cats = get_the_category();
								if ( $cats ) : ?>
									<span class="top-card-cat"><?php echo esc_html( $cats[0]->name ); ?></span>
								<?php endif; ?>
								<h3 class="top-rank-title"><?php the_title(); ?></h3>
								<?php if ( $views > 0 ) : ?>
									<span class="top-rank-views"><?php echo esc_html( number_format( $views ) ); ?> views</span>
								<?php endif; ?>
							</div>
						</a>
					</li>
				<?php $rank++; endwhile; wp_reset_postdata(); ?>
			</ol>
		</section>

	</div>
	<?php
} );

/**
 * ブログと同じ右サイドバーを出すページか。
 * 投稿に加え、補助金診断（/shindan/）と地域ページ（/area/ 以下の固定ページ）で出す。
 * お問い合わせなど、ほかの固定ページには出さない。
 *
 * @return bool
 */
function hikitsugi_has_blog_sidebar() {
	if ( is_single() ) {
		return true;
	}
	if ( ! is_page() || is_front_page() ) {
		return false;
	}
	if ( is_page( [ 'shindan', 'supervisor' ] ) ) {
		return true;
	}
	$area = get_page_by_path( 'area' );
	return $area && ( is_page( $area->ID ) || in_array( $area->ID, get_post_ancestors( get_queried_object_id() ), true ) );
}

/**
 * 本文の「よくある質問」見出しの下にある質問と回答を取り出す。
 * 「よくある質問」を含む見出しのひとつ下のレベルの見出しを質問、
 * 次の見出しまでの段落を回答とする。
 *
 * @param string $html 本文のHTML。
 * @return array<int, array{q: string, a: string}>
 */
function hikitsugi_extract_faq( $html ) {
	if ( ! class_exists( 'DOMDocument' ) || false === strpos( $html, 'よくある質問' ) ) {
		return [];
	}
	$doc = new DOMDocument();
	libxml_use_internal_errors( true );
	$doc->loadHTML( '<?xml encoding="UTF-8"><div>' . $html . '</div>' );
	libxml_clear_errors();

	$faq       = [];
	$faq_level = 0;
	$current   = null;
	foreach ( $doc->getElementsByTagName( 'div' )->item( 0 )->childNodes as $node ) {
		if ( XML_ELEMENT_NODE !== $node->nodeType ) {
			continue;
		}
		$text = trim( $node->textContent );
		if ( preg_match( '/^h([2-6])$/', $node->nodeName, $m ) ) {
			$level = (int) $m[1];
			if ( $current ) {
				$faq[]   = $current;
				$current = null;
			}
			if ( false !== strpos( $text, 'よくある質問' ) ) {
				$faq_level = $level;
			} elseif ( $faq_level && $level === $faq_level + 1 ) {
				$current = [ 'q' => $text, 'a' => '' ];
			} elseif ( $faq_level && $level <= $faq_level ) {
				$faq_level = 0;
			}
			continue;
		}
		if ( $current && in_array( $node->nodeName, [ 'p', 'ul', 'ol' ], true ) ) {
			$current['a'] = trim( $current['a'] . "\n" . $text );
		}
	}
	if ( $current ) {
		$faq[] = $current;
	}
	return array_values( array_filter( $faq, function ( $item ) {
		return '' !== $item['a'];
	} ) );
}

/**
 * パンくずの項目。
 * 投稿: サイト名 > カテゴリ（親カテゴリから） > 記事。カテゴリは Rank Math の主カテゴリ、なければ最初のカテゴリ。
 * 固定ページ: サイト名 > 親ページ > ページ。
 *
 * @param WP_Post $post 対象の投稿・固定ページ。
 * @return array<int, array{name: string, url: string}>
 */
function hikitsugi_breadcrumbs( $post ) {
	$crumbs = [ [ 'name' => get_bloginfo( 'name' ), 'url' => home_url( '/' ) ] ];
	if ( 'post' === $post->post_type ) {
		$cat_id = (int) get_post_meta( $post->ID, 'rank_math_primary_category', true );
		$cat    = $cat_id ? get_term( $cat_id, 'category' ) : null;
		if ( ! $cat || is_wp_error( $cat ) ) {
			$cats = get_the_category( $post->ID );
			$cat  = $cats ? $cats[0] : null;
		}
		if ( $cat ) {
			foreach ( array_reverse( get_ancestors( $cat->term_id, 'category' ) ) as $ancestor_id ) {
				$ancestor = get_term( $ancestor_id, 'category' );
				$crumbs[] = [ 'name' => $ancestor->name, 'url' => get_term_link( $ancestor ) ];
			}
			$crumbs[] = [ 'name' => $cat->name, 'url' => get_term_link( $cat ) ];
		}
	} else {
		foreach ( array_reverse( get_post_ancestors( $post ) ) as $ancestor_id ) {
			$crumbs[] = [ 'name' => get_the_title( $ancestor_id ), 'url' => get_permalink( $ancestor_id ) ];
		}
	}
	$crumbs[] = [ 'name' => get_the_title( $post ), 'url' => get_permalink( $post ) ];
	return $crumbs;
}

// 投稿: 記事の上（アイキャッチの上）にパンくずを表示
add_action( 'generate_before_content', function () {
	if ( ! is_single() ) {
		return;
	}
	$crumbs = hikitsugi_breadcrumbs( get_queried_object() );
	$last   = count( $crumbs ) - 1;
	echo '<nav class="breadcrumbs" aria-label="パンくずリスト"><ol>';
	foreach ( $crumbs as $i => $crumb ) {
		echo $i === $last
			? '<li aria-current="page">' . esc_html( $crumb['name'] ) . '</li>'
			: '<li><a href="' . esc_url( $crumb['url'] ) . '">' . esc_html( $crumb['name'] ) . '</a></li>';
	}
	echo '</ol></nav>';
}, 5 );

// 投稿・診断・地域ページ: FAQPage と BreadcrumbList の構造化データを出力
add_action( 'wp_head', function () {
	if ( ! hikitsugi_has_blog_sidebar() ) {
		return;
	}
	$post    = get_queried_object();
	$schemas = [];

	$faq = hikitsugi_extract_faq( apply_filters( 'the_content', $post->post_content ) );
	if ( $faq ) {
		$schemas[] = [
			'@context'   => 'https://schema.org',
			'@type'      => 'FAQPage',
			'mainEntity' => array_map( function ( $item ) {
				return [
					'@type'          => 'Question',
					'name'           => $item['q'],
					'acceptedAnswer' => [ '@type' => 'Answer', 'text' => $item['a'] ],
				];
			}, $faq ),
		];
	}

	$crumbs    = hikitsugi_breadcrumbs( $post );
	$schemas[] = [
		'@context'        => 'https://schema.org',
		'@type'           => 'BreadcrumbList',
		'itemListElement' => array_map( function ( $crumb, $i ) {
			return [ '@type' => 'ListItem', 'position' => $i + 1, 'name' => $crumb['name'], 'item' => $crumb['url'] ];
		}, $crumbs, array_keys( $crumbs ) ),
	];

	foreach ( $schemas as $schema ) {
		echo '<script type="application/ld+json">' . wp_json_encode( $schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
	}
} );

/**
 * 診断・地域ページの監修者。プロフィールの詳細は固定ページ /supervisor/ に書く。
 *
 * @return array
 */
function hikitsugi_supervisor() {
	return [
		'@type'    => 'Person',
		'name'     => '安藤 昭太',
		'jobTitle' => '株式会社ふえん 代表取締役',
		'url'      => home_url( '/supervisor/' ),
		'worksFor' => [ '@type' => 'Organization', 'name' => '株式会社ふえん', 'url' => 'https://fuenn.co.jp/' ],
		'sameAs'   => [
			'https://fuenn.co.jp/',
			'https://fuenn.co.jp/book/genba-dx.html',
			'https://news.mynavi.jp/techplus/article/20240916-3017816',
		],
	];
}

/**
 * 監修者の情報を出すページか（診断・地域ページ。監修者ページ自身は除く）。
 *
 * @return bool
 */
function hikitsugi_is_supervised_page() {
	return is_page() && hikitsugi_has_blog_sidebar() && ! is_page( 'supervisor' );
}

// 診断・地域ページ: 本文の最後に監修者を表示
add_filter( 'the_content', function ( $content ) {
	if ( ! hikitsugi_is_supervised_page() || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	$sv  = hikitsugi_supervisor();
	$box = '<aside class="supervisor-box">'
		. '<p class="supervisor-label">監修</p>'
		. '<p class="supervisor-name"><a href="' . esc_url( $sv['url'] ) . '">' . esc_html( $sv['name'] ) . '</a></p>'
		. '<p class="supervisor-title">株式会社ふえん 代表取締役／一般社団法人ノーコード推進協会 副代表理事</p>'
		. '<p class="supervisor-text">富士通でシステム開発に従事したのち独立。ノーコードによる市民開発とDX内製化を専門とし、中小企業のDX推進と研修を手がける。著書に『現場が動くDX ノーコードから始める市民開発実践ガイド』（共著）など。</p>'
		. '<p class="supervisor-more"><a href="' . esc_url( $sv['url'] ) . '">プロフィールを見る →</a></p>'
		. '</aside>';
	return $content . $box;
} );

// 診断・地域ページ: Rank Math の WebPage と Article に監修者（reviewedBy）を加える
add_filter( 'rank_math/json_ld', function ( $data ) {
	if ( ! is_page() || ! ( hikitsugi_is_supervised_page() || is_page( 'supervisor' ) ) ) {
		return $data;
	}
	foreach ( $data as $key => $entity ) {
		$types = (array) ( $entity['@type'] ?? [] );
		if ( is_page( 'supervisor' ) ) {
			if ( in_array( 'WebPage', $types, true ) ) {
				$data[ $key ]['@type']      = 'ProfilePage';
				$data[ $key ]['mainEntity'] = hikitsugi_supervisor();
			}
			continue;
		}
		if ( array_intersect( $types, [ 'WebPage', 'Article', 'BlogPosting' ] ) ) {
			$data[ $key ]['reviewedBy'] = hikitsugi_supervisor();
		}
	}
	return $data;
}, 99 );

// 診断・地域・監修者ページ: アイキャッチはSNS・検索の共有画像（og:image）にだけ使い、ページ上部には出さない
add_action( 'wp', function () {
	if ( is_page() && hikitsugi_has_blog_sidebar() ) {
		remove_action( 'generate_after_header', 'generate_featured_page_header', 10 );
	}
} );

// 投稿・診断・地域ページ: 右サイドバーを強制表示
add_filter( 'generate_sidebar_layout', function( $layout ) {
	if ( hikitsugi_has_blog_sidebar() ) return 'right-sidebar';
	return $layout;
} );

// 投稿・診断・地域ページ: サイドバーにCTA・ピックアップ・カテゴリを出力
add_action( 'generate_before_right_sidebar_content', function() {
	if ( ! hikitsugi_has_blog_sidebar() ) return;
	?>

	<div class="sidebar-widget sidebar-cta">
		<div class="sidebar-cta-inner">
			<span class="sidebar-cta-label">無料相談受付中</span>
			<p class="sidebar-cta-title">AIで毎日の業務を<br>スリム化</p>
			<p class="sidebar-cta-text">まずはお気軽にご相談ください。専門スタッフが課題を整理します。</p>
			<a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>" class="sidebar-cta-btn">無料で相談する →</a>
		</div>
	</div>

	<?php
	// ピックアップ記事：プラグイン ai-bpo-pickup のチェックが入った投稿。表示形式はランキングと共通
	$pickup = new WP_Query( [
		'posts_per_page'      => 5,
		'post_status'         => 'publish',
		'ignore_sticky_posts' => true,
		'meta_query'          => [ [ 'key' => 'ai_bpo_pickup', 'value' => '1' ] ],
	] );
	if ( $pickup->have_posts() ) : ?>
	<div class="sidebar-widget sidebar-ranking sidebar-pickup">
		<h3 class="sidebar-widget-title">ピックアップ</h3>
		<ul class="sidebar-rank-list">
			<?php while ( $pickup->have_posts() ) : $pickup->the_post(); ?>
				<li class="sidebar-rank-item">
					<a href="<?php the_permalink(); ?>">
						<div class="sidebar-rank-thumb">
							<?php if ( has_post_thumbnail() ) :
								the_post_thumbnail( 'medium' );
							else : ?>
								<div class="sidebar-rank-placeholder"></div>
							<?php endif; ?>
						</div>
						<p class="sidebar-rank-title"><?php the_title(); ?></p>
					</a>
				</li>
			<?php endwhile; wp_reset_postdata(); ?>
		</ul>
		<a href="<?php echo esc_url( home_url( '/archives/' ) ); ?>" class="sidebar-ranking-more">もっとみる</a>
	</div>
	<?php endif; ?>

	<div class="sidebar-widget sidebar-tools">
		<a class="sidebar-tool" href="<?php echo esc_url( home_url( '/shindan/' ) ); ?>">
			<span class="sidebar-tool-label">無料ツール</span>
			<span class="sidebar-tool-title">AI導入の補助金診断</span>
			<span class="sidebar-tool-text">所在地と費用から、使える補助金と実質の自己負担を試算します</span>
		</a>
		<a class="sidebar-tool" href="<?php echo esc_url( home_url( '/area/' ) ); ?>">
			<span class="sidebar-tool-label">地域別ガイド</span>
			<span class="sidebar-tool-title">首都圏の地域別AI導入ガイド</span>
			<span class="sidebar-tool-text">都県・市ごとの補助金、人手不足、事業承継のデータ</span>
		</a>
	</div>

	<div class="sidebar-widget sidebar-categories">
		<h3 class="sidebar-widget-title">カテゴリ</h3>
		<ul class="sidebar-cat-list">
			<?php
			$cats = get_categories( [ 'hide_empty' => false ] );
			foreach ( $cats as $cat ) : ?>
				<li class="sidebar-cat-item">
					<a href="<?php echo esc_url( get_category_link( $cat->term_id ) ); ?>">
						<span class="sidebar-cat-name"><?php echo esc_html( $cat->name ); ?></span>
						<span class="sidebar-cat-count"><?php echo (int) $cat->count; ?></span>
					</a>
				</li>
			<?php endforeach; ?>
		</ul>
	</div>

	<?php
} );

// フッター著作権表示
add_action( 'generate_credits', 'generate_add_footer_info' );
function generate_add_footer_info() {
	?>
	<div class="footer-copyright">
		<span>&copy; <?php echo esc_html( date( 'Y' ) ); ?> <?php bloginfo( 'name' ); ?></span>
		<a href="<?php echo esc_url( home_url( '/shindan/' ) ); ?>">補助金診断</a>
		<a href="<?php echo esc_url( home_url( '/area/' ) ); ?>">地域別AI導入ガイド</a>
		<a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>">プライバシーポリシー</a>
		<a href="<?php echo esc_url( home_url( '/#form' ) ); ?>">お問い合わせ</a>
	</div>
	<?php
}
