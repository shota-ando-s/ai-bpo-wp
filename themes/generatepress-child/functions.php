<?php

// ページビューカウンター（記事閲覧時にカウントアップ）
add_action( 'wp_head', function () {
	if ( ! is_single() ) return;
	global $post;
	$count = (int) get_post_meta( $post->ID, 'post_views_count', true );
	update_post_meta( $post->ID, 'post_views_count', $count + 1 );
} );

add_action('wp_enqueue_scripts', function () {
	wp_enqueue_style(
		'generatepress-child',
		get_stylesheet_uri(),
		['generate-style'],
		wp_get_theme()->get('Version')
	);
});

// フッター著作権表示（親テーマの pluggable 関数を子テーマで上書き）
add_action('generate_credits', 'generate_add_footer_info');
function generate_add_footer_info() {
	?>
	<div class="footer-copyright">
		<span>&copy; <?php echo esc_html( date( 'Y' ) ); ?> <?php bloginfo( 'name' ); ?></span>
		<a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>">プライバシーポリシー</a>
		<a href="<?php echo esc_url( home_url( '/#contact' ) ); ?>">お問い合わせ</a>
	</div>
	<?php
}

// フッター著作権表示のオーバーライド（親テーマの pluggable 関数より先にロードされる）
add_action('generate_credits', 'generate_add_footer_info');
function generate_add_footer_info() {
	?>
	<div class="footer-copyright">
		<span>&copy; <?php echo esc_html( date( 'Y' ) ); ?> <?php bloginfo( 'name' ); ?></span>
		<a href="<?php echo esc_url( home_url( '/privacy-policy/' ) ); ?>">プライバシーポリシー</a>
		<a href="<?php echo esc_url( home_url( '/#contact' ) ); ?>">お問い合わせ</a>
	</div>
	<?php
}
