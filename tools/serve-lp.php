<?php
/**
 * LPのローカル開発サーバー（PHPビルトインサーバーのルーター）。
 *
 *   php -S localhost:8080 tools/serve-lp.php
 *   open http://localhost:8080
 *
 * front-page.php と同じ lp/lp-markup.php をリクエストのたびに描画するので、
 * マークアップを編集したらリロードするだけで反映される。
 * CSSだけは事前ビルドが必要（`cd themes/generatepress-child && npm run build:lp`）。
 */

$root  = dirname( __DIR__ );
$theme = $root . '/themes/generatepress-child';
$path  = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );

// テーマ配下の静的ファイル（CSS・画像）はそのまま返す
if ( '/' !== $path ) {
	$file = realpath( $theme . $path );
	if ( $file && str_starts_with( $file, realpath( $theme ) ) && is_file( $file ) ) {
		$types = array(
			'css' => 'text/css', 'js' => 'text/javascript', 'svg' => 'image/svg+xml',
			'png' => 'image/png', 'jpg' => 'image/jpeg', 'jpeg' => 'image/jpeg',
			'webp' => 'image/webp', 'ico' => 'image/x-icon',
		);
		$ext = strtolower( pathinfo( $file, PATHINFO_EXTENSION ) );
		header( 'Content-Type: ' . ( $types[ $ext ] ?? 'application/octet-stream' ) );
		header( 'Cache-Control: no-store' );
		readfile( $file );
		return true;
	}
	http_response_code( 404 );
	echo 'Not Found: ' . htmlspecialchars( $path, ENT_QUOTES );
	return true;
}

$css = $theme . '/assets/lp.css';
if ( ! is_file( $css ) ) {
	http_response_code( 500 );
	echo '<h1>assets/lp.css がありません</h1>'
		. '<p><code>cd themes/generatepress-child &amp;&amp; npm run build:lp</code> を実行してください。</p>';
	return true;
}

// 本番（front-page.php）と同じ変数を渡す
$lp_home     = '/';
$lp_contact  = '#contact';
$lp_privacy  = '#';
$lp_tokusho  = '#';
$lp_company  = 'https://fuenn.co.jp/';
$lp_archives = '#';

header( 'Content-Type: text/html; charset=UTF-8' );
?><!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>ヒキツギAI｜引き継ぎを、人ではなく方法で解決する</title>
<link rel="stylesheet" href="/assets/lp.css?v=<?php echo filemtime( $css ); ?>">
</head>
<body class="lp-body">
<?php require $theme . '/lp/lp-markup.php'; ?>
</body>
</html>
