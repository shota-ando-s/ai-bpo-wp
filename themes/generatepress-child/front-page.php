<?php
if ( ! defined( 'ABSPATH' ) ) exit;

get_header(); ?>

<div <?php generate_do_attr( 'content' ); ?>>
	<main <?php generate_do_attr( 'main' ); ?>>
		<?php
		do_action( 'generate_before_main_content' );

		if ( generate_has_default_loop() ) {
			while ( have_posts() ) :
				the_post();
				generate_do_template_part( 'page' );
			endwhile;
		}

		do_action( 'generate_after_main_content' );
		?>
	</main>
</div>

<?php
do_action( 'generate_after_primary_content_area' );
generate_construct_sidebars();
?>

<div class="top-sections-wrapper">

	<!-- 新着記事 -->
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
							the_post_thumbnail( 'medium_large' );
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
			<a href="<?php echo esc_url( home_url( '/blog/' ) ); ?>" class="top-more-btn">記事一覧を見る</a>
		</div>
	</section>

	<!-- ランキング -->
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
								the_post_thumbnail( 'thumbnail' );
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

<?php get_footer();
