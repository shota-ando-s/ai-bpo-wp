<?php
/**
 * LPの静的プレビューHTMLを生成する（デプロイ前のブラウザ確認用）。
 *
 *   php tools/build-lp-preview.php
 *   open dist/lp-preview.html
 *
 * front-page.php と同じ lp/lp-markup.php を読むので、本番と表示が一致する。
 * 画像は dist/images/lp/ へコピーする。dist/ は .gitignore 済み。
 */

$root  = dirname( __DIR__ );
$theme = $root . '/themes/generatepress-child';
$dist  = $root . '/dist';

if ( ! is_dir( $dist ) && ! mkdir( $dist, 0755, true ) && ! is_dir( $dist ) ) {
	fwrite( STDERR, "dist/ を作成できませんでした\n" );
	exit( 1 );
}

$css_path = $theme . '/assets/lp.css';
if ( ! is_file( $css_path ) ) {
	fwrite( STDERR, "assets/lp.css がありません\n" );
	exit( 1 );
}

// マークアップ側が期待する変数（プレビューでは相対リンクにしておく）
$lp_home        = '#';
$lp_img         = 'images/lp';
$lp_privacy     = '#';
$lp_tokusho     = '#';
$lp_company     = 'https://fuenn.co.jp/';
$lp_archives    = '#';
$lp_form_action = '#';

ob_start();
require $theme . '/lp/lp-markup.php';
$body = ob_get_clean();

$css = file_get_contents( $css_path );

// 画像を dist 配下へコピー（相対パス images/lp/… で引けるようにする）
$img_dst = $dist . '/images/lp';
if ( ! is_dir( $img_dst ) && ! mkdir( $img_dst, 0755, true ) && ! is_dir( $img_dst ) ) {
	fwrite( STDERR, "dist/images/lp/ を作成できませんでした\n" );
	exit( 1 );
}
foreach ( glob( $theme . '/images/lp/*' ) as $file ) {
	copy( $file, $img_dst . '/' . basename( $file ) );
}

$html = "<!DOCTYPE html>\n"
	. "<html lang=\"ja\">\n<head>\n"
	. "<meta charset=\"UTF-8\">\n"
	. "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
	. "<meta name=\"robots\" content=\"noindex\">\n"
	. "<title>ヒキツギAI｜LPプレビュー</title>\n"
	. "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
	. "<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n"
	. "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&amp;display=swap\">\n"
	. "<style>\n{$css}\n</style>\n"
	. "</head>\n<body class=\"lp-body\">\n"
	. $body
	. "\n</body>\n</html>\n";

file_put_contents( $dist . '/lp-preview.html', $html );

printf( "生成: %s (%.1f KB)\n", $dist . '/lp-preview.html', strlen( $html ) / 1024 );
