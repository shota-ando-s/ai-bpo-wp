<?php
/**
 * Plugin Name: ヒキツギAI 補助金診断
 * Description: 所在地・目的・費用から、使える補助金と実質の自己負担を試算する診断ツール。固定ページにショートコード [hikitsugi_shindan] を置いて使う。データは data/subsidies.json（scripts/build_shindan_data.py で data/subsidies/*.yml から生成）。
 * Version:     1.0.0
 * Author:      株式会社ふえん
 *
 * @package Hikitsugi
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * スクリプトとスタイルを登録する。読み込むのはショートコードが使われたときだけ。
 */
add_action( 'wp_enqueue_scripts', function () {
	$dir = plugin_dir_path( __FILE__ );
	$url = plugin_dir_url( __FILE__ );
	wp_register_style( 'hikitsugi-shindan', $url . 'assets/shindan.css', array(), (string) filemtime( $dir . 'assets/shindan.css' ) );
	wp_register_script( 'hikitsugi-shindan', $url . 'assets/shindan.js', array(), (string) filemtime( $dir . 'assets/shindan.js' ), true );
} );

/**
 * [hikitsugi_shindan] 診断フォームと結果の表示領域を出力する。
 *
 * @return string HTML。
 */
add_shortcode( 'hikitsugi_shindan', function () {
	$json = file_get_contents( plugin_dir_path( __FILE__ ) . 'data/subsidies.json' );
	if ( false === $json ) {
		return '';
	}
	wp_enqueue_style( 'hikitsugi-shindan' );
	wp_enqueue_script( 'hikitsugi-shindan' );
	wp_add_inline_script( 'hikitsugi-shindan', 'window.HIKITSUGI_SHINDAN_DATA = ' . $json . ';', 'before' );

	ob_start();
	?>
	<div class="hikitsugi-shindan">
		<form class="hs-form" novalidate>
			<fieldset>
				<legend>1. 所在地</legend>
				<div class="hs-row">
					<label>都道府県<select name="pref"></select></label>
					<label>市区町村<select name="city"></select></label>
				</div>
			</fieldset>
			<fieldset>
				<legend>2. やりたいこと</legend>
				<div class="hs-radios">
					<label><input type="radio" name="purpose" value="efficiency" checked> AI業務効率化（ツールの導入）</label>
					<label><input type="radio" name="purpose" value="training"> AI研修</label>
					<label><input type="radio" name="purpose" value="consulting"> AIコンサル・伴走支援</label>
				</div>
			</fieldset>
			<fieldset>
				<legend>3. 会社の規模</legend>
				<div class="hs-row">
					<label>業種
						<select name="industry">
							<option value="other">製造・建設・運輸・その他</option>
							<option value="commerce">商業（卸売・小売）・サービス業</option>
						</select>
					</label>
					<label>従業員数（人）<input type="number" name="employees" min="1" value="30" inputmode="numeric"></label>
				</div>
			</fieldset>
			<fieldset>
				<legend>4. 想定している費用</legend>
				<div class="hs-row hs-cost-eff">
					<label>初期費用（円）<input type="number" name="initial" min="0" step="10000" value="500000" inputmode="numeric"></label>
					<label>月額（円）<input type="number" name="monthly" min="0" step="10000" value="50000" inputmode="numeric"></label>
					<label>利用する月数<input type="number" name="months" min="1" max="60" value="12" inputmode="numeric"></label>
				</div>
				<div class="hs-row hs-cost-total" hidden>
					<label><span class="hs-cost-total-label">研修費用の合計（円）</span><input type="number" name="total" min="0" step="10000" value="500000" inputmode="numeric"></label>
				</div>
				<p class="hs-hint">ヒキツギAIの料金は、AIチャットが月5万円〜、AI自動化が月20万円〜です（初期導入費は別途お見積もり）。</p>
			</fieldset>
			<button type="submit" class="hs-button">使える補助金を調べる</button>
		</form>
		<div class="hs-result" hidden aria-live="polite"></div>
		<noscript><p>この診断ツールを使うには、JavaScriptを有効にしてください。</p></noscript>
	</div>
	<?php
	return ob_get_clean();
} );
