<?php
/**
 * Plugin Name: ヒキツギAI CF7調整
 * Description: cf7-to-zapier がSlackへ送るデータを整える。checkbox等の配列値を文字列に均し、custom_body のJSONテンプレートに差し込めるようにする。
 * Version:     1.0.0
 * Author:      株式会社ふえん
 *
 * @package Hikitsugi
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Webhookへ渡すデータの配列値を文字列に均す。
 *
 * CFTZ は custom_body の [フィールド名] を json_encode した値で置換する
 * （modules/zapier/class-module-zapier.php）。checkbox は配列のままなので
 * ["サービス紹介資料が欲しい"] に展開され、JSON文字列の中に入れると
 * クォートで構造が壊れて json_decode が null になり、フォーム送信自体が
 * mail_failed に落ちる。ここで先に文字列化しておけば素直に差し込める。
 *
 * @param array $data フォームから集めた値。
 * @return array 配列値を文字列に均したもの。
 */
add_filter( 'ctz_get_data_from_contact_form', function ( $data ) {
	foreach ( $data as $key => $value ) {
		if ( is_array( $value ) ) {
			$data[ $key ] = implode( '、', array_filter( $value, 'is_scalar' ) );
		}
	}
	return $data;
} );
