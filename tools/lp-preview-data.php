<?php
/**
 * ローカル確認用のダミーデータ。
 *
 * tools/build-lp-preview.php と tools/serve-lp.php の両方から読む。
 * 本番では front-page.php が WP_Query と CF7 から同じ形のデータを作るので、
 * ここはあくまで「WordPressなしで見た目を確認する」ためのもの。
 *
 * 呼び出し側に $lp_pickup / $lp_latest を生やす。
 */

$lp_dummy_post = function ( $title, $cat, $date ) {
	return array(
		'title'    => $title,
		'url'      => '#',
		'cat'      => $cat,
		'date'     => str_replace( '-', '.', $date ),
		'datetime' => $date,
		'thumb'    => '',
		'thumb_w'  => 0,
		'thumb_h'  => 0,
	);
};

$lp_pickup = array(
	$lp_dummy_post( '退職者のITアカウント棚卸しでよくある抜け漏れ', '引き継ぎ', '2026-06-21' ),
	$lp_dummy_post( '引き継ぎマニュアルが機能しない3つの理由', '引き継ぎ', '2026-06-21' ),
	$lp_dummy_post( 'オフボーディングのチェックリスト', '退職手続き', '2026-06-21' ),
);

$lp_latest = array(
	$lp_dummy_post( '退職手続きで会社がやることの全体像', '退職手続き', '2026-06-21' ),
	$lp_dummy_post( '退職者のセキュリティリスクにどう備えるか', 'セキュリティ', '2026-06-21' ),
	$lp_dummy_post( 'エグジットインタビューの設計と運用', '組織', '2026-06-21' ),
	$lp_dummy_post( 'アルムナイ採用を前提にした退職対応', '採用', '2026-06-21' ),
	$lp_dummy_post( 'オフボーディングを代行するという選択肢', '引き継ぎ', '2026-06-21' ),
	$lp_dummy_post( '引き継ぎの進め方をゼロから組み立てる', '引き継ぎ', '2026-06-21' ),
);
