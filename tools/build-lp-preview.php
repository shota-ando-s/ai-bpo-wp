<?php
/**
 * LPの静的プレビューHTMLを生成する（デプロイ前のブラウザ確認用）。
 *
 *   php tools/build-lp-preview.php
 *   open dist/lp-preview.html
 *
 * front-page.php と同じ lp/lp-markup.php を読むので、本番と表示が一致する。
 * dist/ は .gitignore 済み。
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
	fwrite( STDERR, "assets/lp.css がありません。先に `npm run build:lp` を実行してください\n" );
	exit( 1 );
}

// マークアップ側が期待する変数（プレビューでは相対リンクにしておく）
$lp_home     = '#';
$lp_contact  = '#contact';
$lp_privacy  = '#';
$lp_tokusho  = '#';
$lp_company  = 'https://fuenn.co.jp/';
$lp_archives = '#';

ob_start();
require $theme . '/lp/lp-markup.php';
$body = ob_get_clean();

$css = file_get_contents( $css_path );

$html = "<!DOCTYPE html>\n"
	. "<html lang=\"ja\">\n<head>\n"
	. "<meta charset=\"UTF-8\">\n"
	. "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
	. "<meta name=\"robots\" content=\"noindex\">\n"
	. "<title>ヒキツギAI｜LPプレビュー</title>\n"
	. "<style>\n{$css}\n</style>\n"
	. "</head>\n<body class=\"lp-body\">\n"
	. $body
	. "\n</body>\n</html>\n";

file_put_contents( $dist . '/lp-preview.html', $html );

printf( "生成: %s (%.1f KB)\n", $dist . '/lp-preview.html', strlen( $html ) / 1024 );
