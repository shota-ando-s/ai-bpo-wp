<?php
/**
 * フロントページ = ヒキツギAI ランディングページ
 *
 * GeneratePress のヘッダー／フッター／コンテナは使わず、LP専用の
 * 独立したドキュメントとして出力する（get_header() / get_footer() を呼ばない）。
 * wp_head() / wp_footer() は残すので Rank Math の title / meta / OGP は従来どおり効く。
 *
 * 本体マークアップは lp/lp-markup.php。静的プレビュー生成
 * （tools/build-lp-preview.php）と同じファイルを共有している。
 *
 * @package GeneratePress Child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$lp_home     = home_url( '/' );
$lp_img      = get_stylesheet_directory_uri() . '/images/lp';
$lp_privacy  = home_url( '/privacy-policy/' );
$lp_tokusho  = home_url( '/tokushoho/' );
$lp_company  = 'https://fuenn.co.jp/';
$lp_archives = home_url( '/archives/' );

// クロージングフォームは Contact Form 7（ID は functions.php の定数）。
// CF7 が落ちている・IDが変わった等で空になったら、
// lp-markup.php 側が静的フォームにフォールバックする。
$lp_form_html = '';
if ( defined( 'HIKITSUGI_LP_CF7_ID' ) && shortcode_exists( 'contact-form-7' ) ) {
	$lp_form_html = do_shortcode(
		sprintf( '[contact-form-7 id="%d" html_class="lp-form"]', HIKITSUGI_LP_CF7_ID )
	);
}

// 静的フォールバック時の送信先（CF7が使えるときは参照されない）
$lp_form_action = '#';

/**
 * 記事カード用に WP_Post を lp-markup.php が期待する素の配列へ均す。
 * マークアップ側は WordPress 非依存（tools/ のプレビューと共有）なので、
 * WP関数を呼ぶのはこの front-page.php までに閉じる。
 */
$lp_map_post = function ( $post ) {
	$cats  = get_the_category( $post->ID );
	$thumb = has_post_thumbnail( $post->ID )
		? wp_get_attachment_image_src( get_post_thumbnail_id( $post->ID ), 'card-thumb' )
		: false;

	return array(
		'title'    => get_the_title( $post->ID ),
		'url'      => get_permalink( $post->ID ),
		'cat'      => $cats ? $cats[0]->name : '',
		'date'     => get_the_date( 'Y.m.d', $post->ID ),
		'datetime' => get_the_date( 'Y-m-d', $post->ID ),
		'thumb'    => $thumb ? $thumb[0] : '',
		'thumb_w'  => $thumb ? (int) $thumb[1] : 0,
		'thumb_h'  => $thumb ? (int) $thumb[2] : 0,
	);
};

// ピックアップ記事：プラグイン ai-bpo-pickup のチェックが入った投稿。
// 未指定なら0件になり、LP側でセクションごと出力されない。
$lp_pickup_posts = get_posts( array(
	'posts_per_page'      => 3,
	'post_status'         => 'publish',
	'ignore_sticky_posts' => true,
	'meta_query'          => array(
		array(
			'key'   => 'ai_bpo_pickup',
			'value' => '1',
		),
	),
) );

// 新着記事：ピックアップと重複させない
$lp_latest_posts = get_posts( array(
	'posts_per_page'      => 6,
	'post_status'         => 'publish',
	'ignore_sticky_posts' => true,
	'post__not_in'        => wp_list_pluck( $lp_pickup_posts, 'ID' ),
) );

$lp_pickup = array_map( $lp_map_post, $lp_pickup_posts );
$lp_latest = array_map( $lp_map_post, $lp_latest_posts );

?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class( 'lp-body' ); ?>>
<?php wp_body_open(); ?>

<?php require get_stylesheet_directory() . '/lp/lp-markup.php'; ?>

<?php wp_footer(); ?>
</body>
</html>
