<?php
/**
 * Plugin Name: ヒキツギAI SMTP送信
 * Description: wp_mail() をSMTP経由に切り替える。さくらのサーバはPHPの mail() から外部宛のリレーを拒否する（553 not local address）ため、これが無いと問い合わせフォームの通知・自動返信が一切届かない。
 * Version:     1.0.0
 * Author:      株式会社ふえん
 *
 * 認証情報はこのファイルには置かない。リポジトリが公開されているので、
 * サーバの wp-config.php（Git管理外）に定数として書く：
 *
 *   define( 'HIKITSUGI_SMTP_HOST',      'smtp.resend.com' );
 *   define( 'HIKITSUGI_SMTP_PORT',      587 );
 *   define( 'HIKITSUGI_SMTP_USER',      'resend' );
 *   define( 'HIKITSUGI_SMTP_PASS',      're_xxxxxxxxxxxx' );   // ResendのAPIキー
 *   define( 'HIKITSUGI_SMTP_FROM',      'noreply@hikitsugi.jp' );
 *   define( 'HIKITSUGI_SMTP_FROM_NAME', 'ヒキツギAI' );
 *
 * @package Hikitsugi
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * 設定が揃っているか。ひとつでも欠けたら何もしない（＝従来の mail() のまま）。
 */
function hikitsugi_smtp_is_configured() {
	foreach ( array( 'HIKITSUGI_SMTP_HOST', 'HIKITSUGI_SMTP_PORT', 'HIKITSUGI_SMTP_USER', 'HIKITSUGI_SMTP_PASS' ) as $c ) {
		if ( ! defined( $c ) || '' === constant( $c ) ) {
			return false;
		}
	}
	return true;
}

/**
 * PHPMailer をSMTPモードに切り替える。
 *
 * @param PHPMailer\PHPMailer\PHPMailer $phpmailer メール送信オブジェクト。
 */
add_action( 'phpmailer_init', function ( $phpmailer ) {
	if ( ! hikitsugi_smtp_is_configured() ) {
		return;
	}

	$phpmailer->isSMTP();
	$phpmailer->Host       = HIKITSUGI_SMTP_HOST;
	$phpmailer->Port       = (int) HIKITSUGI_SMTP_PORT;
	$phpmailer->SMTPAuth   = true;
	$phpmailer->Username   = HIKITSUGI_SMTP_USER;
	$phpmailer->Password   = HIKITSUGI_SMTP_PASS;
	$phpmailer->SMTPSecure = ( 465 === (int) HIKITSUGI_SMTP_PORT ) ? 'ssl' : 'tls';
	$phpmailer->Timeout    = 20;
	$phpmailer->CharSet    = 'UTF-8';

	/* 送信元は認証済みドメインのアドレスに固定する。ResendもSendGridも
	   未認証ドメインの From を拒否するため、CF7側の設定に依存させない。
	   差出人名と Reply-To（CF7が問い合わせ者のアドレスを入れる）は触らない。 */
	if ( defined( 'HIKITSUGI_SMTP_FROM' ) && '' !== HIKITSUGI_SMTP_FROM ) {
		$name = defined( 'HIKITSUGI_SMTP_FROM_NAME' ) ? HIKITSUGI_SMTP_FROM_NAME : $phpmailer->FromName;
		$phpmailer->setFrom( HIKITSUGI_SMTP_FROM, $name, false );
		$phpmailer->Sender = HIKITSUGI_SMTP_FROM;
	}
}, 20 );

/**
 * 失敗はログに残す。原因がSMTPなのかCF7なのか後から切り分けられるように。
 *
 * @param WP_Error $error 失敗内容。
 */
add_action( 'wp_mail_failed', function ( $error ) {
	error_log( '[hikitsugi-smtp] 送信失敗: ' . $error->get_error_message() );
} );

/**
 * 設定が入っていないうちは管理画面で警告する。黙って mail() に落ちると
 * 「送っているつもりで一通も届いていない」状態に気づけないため。
 */
add_action( 'admin_notices', function () {
	if ( hikitsugi_smtp_is_configured() || ! current_user_can( 'manage_options' ) ) {
		return;
	}
	echo '<div class="notice notice-error"><p><strong>ヒキツギAI SMTP送信</strong>：'
		. 'SMTPの設定定数が wp-config.php にありません。このままではフォームの通知メールが届きません。'
		. '</p></div>';
} );
