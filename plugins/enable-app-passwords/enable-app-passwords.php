<?php
/**
 * Plugin Name: Enable Application Passwords (HTTP)
 * Description: HTTPサイトでもアプリケーションパスワードを有効化する
 * Version: 1.0
 */
add_filter('wp_is_application_passwords_available', '__return_true');
