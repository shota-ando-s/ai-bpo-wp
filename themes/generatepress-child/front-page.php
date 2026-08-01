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

// フォームの送信先。MA／CRM が決まったらここを差し替える。
$lp_form_action = '#';

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
