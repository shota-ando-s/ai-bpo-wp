<?php
add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style(
        'generatepress-child',
        get_stylesheet_uri(),
        ['generatepress-style'],
        wp_get_theme()->get('Version')
    );
});
