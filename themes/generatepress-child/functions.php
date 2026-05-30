<?php

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
} );

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

// ロゴの下にキャッチフレーズを表示
add_action( 'generate_after_logo', function() {
	$description = get_bloginfo( 'description' );
	if ( $description ) {
		echo '<p class="site-tagline">' . esc_html( $description ) . '</p>';
	}
} );

// トップページ: 新着記事・ランキングをグリッド外（フッター直前）に出力
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

// 投稿ページ: 右サイドバーを強制表示
add_filter( 'generate_sidebar_layout', function( $layout ) {
	if ( is_single() ) return 'right-sidebar';
	return $layout;
} );

// 投稿ページ: サイドバーにCTA・カテゴリ・ランキングを出力
add_action( 'generate_before_right_sidebar_content', function() {
	if ( ! is_single() ) return;
	?>

	<div class="sidebar-widget sidebar-cta">
		<div class="sidebar-cta-inner">
			<span class="sidebar-cta-label">無料相談受付中</span>
			<p class="sidebar-cta-title">AIで毎日の業務を<br>スリム化</p>
			<p class="sidebar-cta-text">まずはお気軽にご相談ください。専門スタッフが課題を整理します。</p>
			<a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>" class="sidebar-cta-btn">無料で相談する →</a>
		</div>
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

	<div class="sidebar-widget sidebar-ranking">
		<h3 class="sidebar-widget-title">ランキング</h3>
		<ol class="sidebar-rank-list">
			<?php
			$has_views = get_posts( [
				'posts_per_page' => 1,
				'meta_key'       => 'post_views_count',
				'fields'         => 'ids',
			] );
			$rank_args = ! empty( $has_views ) ? [
				'posts_per_page' => 5,
				'post_status'    => 'publish',
				'meta_key'       => 'post_views_count',
				'orderby'        => 'meta_value_num',
				'order'          => 'DESC',
			] : [
				'posts_per_page' => 5,
				'post_status'    => 'publish',
				'orderby'        => 'date',
				'order'          => 'DESC',
			];
			$ranking = new WP_Query( $rank_args );
			$rank = 1;
			while ( $ranking->have_posts() ) : $ranking->the_post(); ?>
				<li class="sidebar-rank-item">
					<a href="<?php the_permalink(); ?>">
						<span class="sidebar-rank-num rank-<?php echo (int) $rank; ?>"><?php echo (int) $rank; ?></span>
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
			<?php $rank++; endwhile; wp_reset_postdata(); ?>
		</ol>
		<a href="<?php echo esc_url( home_url( '/archives/' ) ); ?>" class="sidebar-ranking-more">もっとみる</a>
	</div>

	<?php
} );

// フッター著作権表示
add_action( 'generate_credits', 'generate_add_footer_info' );
function generate_add_footer_info() {
	?>
	<div class="footer-copyright">
		<span>&copy; <?php echo esc_html( date( 'Y' ) ); ?> <?php bloginfo( 'name' ); ?></span>
		<a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>">プライバシーポリシー</a>
		<a href="<?php echo esc_url( home_url( '/#contact' ) ); ?>">お問い合わせ</a>
	</div>
	<?php
}
