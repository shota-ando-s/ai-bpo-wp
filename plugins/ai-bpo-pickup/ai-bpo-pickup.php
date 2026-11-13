<?php
/**
 * Plugin Name: AI-BPO Pickup Posts
 * Description: ピックアップ記事を管理画面・REST APIから指定できるプラグイン
 * Version: 1.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'init', function() {
	register_post_meta( 'post', 'ai_bpo_pickup', [
		'show_in_rest'  => true,
		'single'        => true,
		'type'          => 'boolean',
		'default'       => false,
		'auth_callback' => function() {
			return current_user_can( 'edit_posts' );
		},
	] );
} );

add_action( 'add_meta_boxes', function() {
	add_meta_box(
		'ai_bpo_pickup_box',
		'ピックアップ設定',
		'ai_bpo_pickup_render_meta_box',
		'post',
		'side',
		'high'
	);
} );

function ai_bpo_pickup_render_meta_box( $post ) {
	wp_nonce_field( 'ai_bpo_pickup_save', 'ai_bpo_pickup_nonce' );
	$checked = (bool) get_post_meta( $post->ID, 'ai_bpo_pickup', true );
	?>
	<label style="display:flex;align-items:center;gap:8px;cursor:pointer;">
		<input type="checkbox" name="ai_bpo_pickup" value="1" <?php checked( $checked ); ?>>
		<span>ピックアップ記事にする</span>
	</label>
	<p style="margin:8px 0 0;font-size:12px;color:#666;">チェックするとトップページのピックアップ欄に表示されます。</p>
	<?php
}

add_action( 'save_post', function( $post_id ) {
	if ( ! isset( $_POST['ai_bpo_pickup_nonce'] ) ) {
		return;
	}
	if ( ! wp_verify_nonce( $_POST['ai_bpo_pickup_nonce'], 'ai_bpo_pickup_save' ) ) {
		return;
	}
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}

	$pickup = isset( $_POST['ai_bpo_pickup'] ) ? true : false;
	update_post_meta( $post_id, 'ai_bpo_pickup', $pickup );
} );
