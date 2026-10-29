/**
 * 補助金診断＋実質負担シミュレーター
 *
 * データは PHP 側が window.HIKITSUGI_SHINDAN_DATA に入れる（data/subsidies.json）。
 * 計算ロジック（Logic）は DOM に依存しないので、Node からも読み込んでテストできる。
 */
(function (root) {
	'use strict';

	var PURPOSES = {
		efficiency: 'AI業務効率化（ツールの導入）',
		training: 'AI研修',
		consulting: 'AIコンサル・伴走支援',
	};
	var STATUS_LABELS = {
		now: '今申請できる',
		next: '来年度の見込み',
		check: '受付状況を要確認',
	};

	// ---------- 計算ロジック ----------

	var Logic = {
		/** 'YYYY-MM' や 'YYYY-MM-DD' を Date にする（月だけなら1日） */
		parseDate: function (s) {
			if (!s) return null;
			var p = String(s).split('-').map(Number);
			return new Date(p[0], (p[1] || 1) - 1, p[2] || 1);
		},

		/** 従業員数と業種から小規模事業者かどうか（商業・サービスは5人以下、それ以外は20人以下） */
		isSmall: function (employees, industry) {
			return employees <= (industry === 'commerce' ? 5 : 20);
		},

		/** 制度の表示区分：now / next / check。対象外なら null */
		status: function (s, purpose, today) {
			// ふえんがまだ対応していない制度は、目的に関係なく来年度扱い
			var from = Logic.parseDate(s.fuenn_available_from);
			if (from && today < from) return 'next';
			var p = s.period || {};
			var end = Logic.parseDate(p.end);
			var start = Logic.parseDate(p.start);
			// 締切日の当日は受付中として扱う
			if (end) end = new Date(end.getFullYear(), end.getMonth(), end.getDate() + 1);
			var finished = p.status === 'closed' || (end && end <= today);
			if (finished) return s.next_expected ? 'next' : null;
			if (p.status === 'unknown') return 'check';
			if (start && start > today) return 'next';
			return 'now';
		},

		/** 地域と目的で候補を絞る */
		candidates: function (data, input) {
			var areas = ['national', input.pref, input.city].filter(Boolean);
			return data.subsidies.filter(function (s) {
				return areas.indexOf(s.area) !== -1 && s.targets[input.purpose] && s.targets[input.purpose] !== '×';
			});
		},

		/** 入力から総費用と、制度ごとの対象経費を出す */
		totalCost: function (input) {
			if (input.purpose === 'efficiency') return input.initial + input.monthly * input.months;
			return input.total;
		},

		eligibleCost: function (s, input) {
			if (input.purpose !== 'efficiency') return input.total;
			var months = s.max_months ? Math.min(input.months, s.max_months) : input.months;
			return input.initial + input.monthly * months;
		},

		/** 単独で使ったときの補助額。計算できない制度は amount: null */
		calc: function (s, input) {
			if (s.addon) return { amount: null, reason: '国などの補助金への上乗せです（組み合わせの欄で計算します）' };
			if (s.rate_num == null) return { amount: null, reason: '定額の助成で、費用の補助ではありません' };
			if (s.small_only && !Logic.isSmall(input.employees, input.industry)) {
				return { amount: null, reason: '小規模事業者だけが対象です' };
			}
			var eligible = Logic.eligibleCost(s, input);
			if (s.min_cost_yen && eligible < s.min_cost_yen) {
				return { amount: null, reason: '対象経費が下限（' + Logic.yen(s.min_cost_yen) + '）に届きません' };
			}
			var rate = Logic.isSmall(input.employees, input.industry) && s.rate_small_num ? s.rate_small_num : s.rate_num;
			var amount = Math.floor(eligible * rate);
			if (s.max_yen) amount = Math.min(amount, s.max_yen);
			return { amount: amount, eligible: eligible, rate: rate };
		},

		/** 上乗せ制度の補助額 */
		calcAddon: function (addon, base, baseAmount, input) {
			var eligible = Logic.eligibleCost(base, input);
			var amount;
			if (addon.addon.kind === 'remaining_tiered') {
				// 自己負担のうち full_upto までは全額、超えた分に ratio を掛ける（仙台生産性ブースト補助金）
				var self = eligible - baseAmount;
				var full = Math.min(self, addon.addon.full_upto);
				amount = Math.floor((full + (self - full) * addon.addon.ratio) / 1000) * 1000;
			} else if (addon.addon.kind === 'over_threshold') {
				// 対象経費のうち threshold を超えた部分に ratio を掛ける（岐阜市 DX推進補助金のスマート経営実践事業）
				amount = Math.floor((eligible - addon.addon.threshold) * addon.addon.ratio);
			} else {
				amount = addon.addon.kind === 'remaining'
					? Math.floor((eligible - baseAmount) * addon.addon.ratio)
					: Math.floor(eligible * addon.addon.ratio);
			}
			if (addon.max_yen) amount = Math.min(amount, addon.max_yen);
			return Math.max(amount, 0);
		},

		/**
		 * 区分ごとに、◎○の制度から1つを選び、使える上乗せ制度と組み合わせる。
		 * 補助額の合計（上乗せを含む）が最も大きい組み合わせを返す。△の制度は条件が厳しいので使わない。
		 */
		plan: function (items, group, input) {
			var pool = items.filter(function (it) { return it.status === group && it.rating !== '△' && it.calc.amount; });
			var total = Logic.totalCost(input);
			var best = null;
			pool.forEach(function (base) {
				var addons = items.filter(function (it) {
					var st = it.s.stacking || {};
					return it.s.addon && it.rating !== '△' && (st.addon_to || []).indexOf(base.s.id) !== -1 && (it.status === 'now' || it.status === group);
				}).map(function (it) {
					return { item: it, amount: Logic.calcAddon(it.s, base.s, base.calc.amount, input) };
				}).filter(function (a) { return a.amount > 0; });
				var subsidy = Math.min(base.calc.amount + addons.reduce(function (n, a) { return n + a.amount; }, 0), total);
				if (!best || subsidy > best.subsidy) {
					best = { base: base, addons: addons, subsidy: subsidy, total: total, self: total - subsidy };
				}
			});
			return best;
		},

		/** 併用できない組み合わせの警告 */
		conflicts: function (items) {
			var ids = items.map(function (it) { return it.s.id; });
			var out = [];
			items.forEach(function (it) {
				((it.s.stacking || {}).exclusive_with || []).forEach(function (ref) {
					if (ids.indexOf(ref) !== -1) {
						var other = items[ids.indexOf(ref)];
						out.push(it.s.name + '（' + it.s.org + '）は、' + other.s.name + 'と併用できません。');
					}
				});
			});
			return out;
		},

		run: function (data, input, today) {
			var items = Logic.candidates(data, input).map(function (s) {
				return { s: s, rating: s.targets[input.purpose], status: Logic.status(s, input.purpose, today), calc: Logic.calc(s, input) };
			}).filter(function (it) { return it.status; });
			var rank = { '◎': 0, '○': 1, '△': 2 };
			items.sort(function (a, b) {
				return (rank[a.rating] - rank[b.rating]) || ((b.calc.amount || 0) - (a.calc.amount || 0));
			});
			return {
				items: items,
				now: Logic.plan(items, 'now', input),
				next: Logic.plan(items, 'next', input),
				conflicts: Logic.conflicts(items),
			};
		},

		yen: function (n) {
			if (n >= 10000) {
				var man = Math.round(n / 1000) / 10;
				return man.toLocaleString('ja-JP') + '万円';
			}
			return n.toLocaleString('ja-JP') + '円';
		},
	};

	// ---------- 画面 ----------

	function esc(s) {
		return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
			return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
		});
	}

	function fmtDate(s) {
		var d = Logic.parseDate(s);
		if (!d) return '';
		return d.getFullYear() + '年' + (d.getMonth() + 1) + '月' + (String(s).length > 7 ? d.getDate() + '日' : '');
	}

	function periodText(it) {
		var p = it.s.period || {};
		if (it.status === 'next') {
			if (it.s.fuenn_available_from && Logic.parseDate(it.s.fuenn_available_from) > new Date()) {
				return 'ふえんの対応は' + fmtDate(it.s.fuenn_available_from) + 'から（予定）';
			}
			return it.s.next_expected ? '次回の公募は' + fmtDate(it.s.next_expected) + 'ごろの見込み' : '次回は未定';
		}
		if (it.status === 'check') return '受付状況は窓口に確認してください';
		if (p.status === 'rolling') return p.end ? '随時受付（' + fmtDate(p.end) + 'まで）' : '随時受付';
		return p.end ? fmtDate(p.end) + 'まで' : '受付中';
	}

	function card(it) {
		var s = it.s;
		var amount;
		if (it.rating === '△') {
			amount = '<div class="hs-card-amount hs-muted">使えるかどうかは条件次第のため、補助額は試算していません</div>';
		} else if (it.calc.amount) {
			amount = '<div class="hs-card-amount">補助額の目安 <strong>' + Logic.yen(it.calc.amount) + '</strong></div>';
		} else {
			amount = it.calc.reason ? '<div class="hs-card-amount hs-muted">' + esc(it.calc.reason) + '</div>' : '';
		}
		return '<article class="hs-card">' +
			'<div class="hs-card-head"><span class="hs-rating hs-rating-' + (it.rating === '◎' ? 'a' : it.rating === '○' ? 'b' : 'c') + '">' + esc(it.rating) + '</span>' +
			'<div><h4>' + esc(s.name) + '</h4><div class="hs-org">' + esc(s.org) + '</div></div></div>' +
			'<dl class="hs-dl">' +
			(s.max_yen ? '<dt>上限</dt><dd>' + Logic.yen(s.max_yen) + '</dd>' : '') +
			'<dt>補助率</dt><dd>' + esc(s.rate || '―') + '</dd>' +
			'<dt>期間</dt><dd>' + esc(periodText(it)) + '</dd>' +
			(s.expenses ? '<dt>対象経費</dt><dd>' + esc(s.expenses) + '</dd>' : '') +
			(s.conditions ? '<dt>条件</dt><dd>' + esc(s.conditions) + '</dd>' : '') +
			'</dl>' + amount +
			(s.fuenn_note ? '<p class="hs-fuenn">' + esc(s.fuenn_note) + '</p>' : '') +
			(s.note ? '<p class="hs-note">' + esc(s.note) + '</p>' : '') +
			'<div class="hs-card-foot"><a href="' + esc(s.url) + '" target="_blank" rel="noopener">公式ページ</a>' +
			'<span>確認日 ' + esc(s.checked) + (s.confidence === 'secondary' ? '（二次情報）' : '') + '</span></div>' +
			'</article>';
	}

	function planBox(title, plan, note) {
		if (!plan) return '';
		var rows = '<tr><td>' + esc(plan.base.s.name) + '<span class="hs-org">' + esc(plan.base.s.org) + '</span></td><td>' + Logic.yen(plan.base.calc.amount) + '</td></tr>';
		plan.addons.forEach(function (a) {
			rows += '<tr><td>＋ ' + esc(a.item.s.name) + '<span class="hs-org">' + esc(a.item.s.org) + '</span></td><td>' + Logic.yen(a.amount) + '</td></tr>';
		});
		return '<section class="hs-plan">' +
			'<h3>' + esc(title) + '</h3>' +
			'<div class="hs-plan-figures">' +
			'<div><span>費用の合計</span><strong>' + Logic.yen(plan.total) + '</strong></div>' +
			'<div><span>補助額の目安</span><strong class="hs-green">−' + Logic.yen(plan.subsidy) + '</strong></div>' +
			'<div><span>実質の自己負担</span><strong class="hs-big">' + Logic.yen(plan.self) + '</strong></div>' +
			'</div>' +
			'<table class="hs-plan-table">' + rows + '</table>' +
			(note ? '<p class="hs-note">' + esc(note) + '</p>' : '') +
			'</section>';
	}

	function render(el, data, input) {
		var res = Logic.run(data, input, new Date());
		var pref = data.areas.filter(function (a) { return a.code === input.pref; })[0];
		var city = pref && pref.cities.filter(function (c) { return c.code === input.city; })[0];
		var place = (pref ? pref.name : '') + (city ? city.name : '');
		var html = '<h2 class="hs-result-title">' + esc(place) + '・' + esc(PURPOSES[input.purpose]) + 'の診断結果</h2>';

		function count(g, weak) {
			return res.items.filter(function (it) { return it.status === g && (it.rating === '△') === weak; }).length;
		}
		html += '<p class="hs-summary">今申請できる制度は<strong>' + count('now', false) + '件</strong>、来年度の公募が見込まれる制度は<strong>' +
			count('next', false) + '件</strong>あります（ほかに、条件次第で使える制度が' + (count('now', true) + count('next', true)) + '件）。</p>';

		if (city && city.none) {
			html += '<p class="hs-callout">' + esc(city.name) + 'には、AI・IT導入向けの独自の補助金が見つかりませんでした（' + esc(data.generated) + '時点）。' +
				esc(pref.name) + 'と国の制度を使います。' + (city.note ? esc(city.note) : '') + '</p>';
		}

		html += planBox('今年度に使える組み合わせ', res.now, '予算に達すると期限前でも締め切られます。申請前に窓口で受付状況を確認してください。');
		html += planBox('来年度に使える見込みの組み合わせ', res.next, '来年度の制度は未公表です。今年度の内容をもとにした見込みです。');
		if (!res.now && !res.next) {
			html += '<p class="hs-callout">入力された条件で、そのまま使える制度は見つかりませんでした。条件付きで使える制度は下の一覧のとおりです。無料のAI活用診断でご相談ください。</p>';
		}
		res.conflicts.forEach(function (c) { html += '<p class="hs-callout hs-warn">' + esc(c) + '</p>'; });

		['now', 'next', 'check'].forEach(function (g) {
			var list = res.items.filter(function (it) { return it.status === g; });
			if (!list.length) return;
			html += '<h3 class="hs-group">' + STATUS_LABELS[g] + '（' + list.length + '件）</h3><div class="hs-cards">' + list.map(card).join('') + '</div>';
		});

		html += '<p class="hs-legend">◎ そのまま使える／○ 条件付きで使える／△ 一部だけ・難しい。補助額は入力された金額と補助率・上限から計算した目安で、採択や対象になることを保証するものではありません。' +
			'小規模事業者の判定は、商業・サービス業は従業員5人以下、それ以外は20人以下としています。</p>';

		var q = 'from=shindan&area=' + encodeURIComponent(place) + '&purpose=' + encodeURIComponent(PURPOSES[input.purpose]);
		html += '<div class="hs-cta"><p>どの制度が使えるか、申請までの段取りまで含めて、無料のAI活用診断でご案内します。</p>' +
			'<a class="hs-button" href="/contact/?' + q + '">無料でAI活用診断を申し込む</a></div>';

		el.innerHTML = html;
		el.hidden = false;
		el.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}

	function num(form, name) {
		var v = Number(String(form.elements[name].value).replace(/[,，]/g, ''));
		return isFinite(v) && v > 0 ? v : 0;
	}

	function init(rootEl, data) {
		var form = rootEl.querySelector('form');
		var prefSel = form.elements.pref;
		var citySel = form.elements.city;
		var result = rootEl.querySelector('.hs-result');

		prefSel.innerHTML = data.areas.map(function (a) {
			return '<option value="' + esc(a.code) + '">' + esc(a.name) + '</option>';
		}).join('');

		function fillCities() {
			var pref = data.areas.filter(function (a) { return a.code === prefSel.value; })[0];
			citySel.innerHTML = '<option value="">上記以外の市区町村</option>' + pref.cities.map(function (c) {
				return '<option value="' + esc(c.code) + '">' + esc(c.name) + '</option>';
			}).join('');
		}

		function toggleCost() {
			var eff = form.elements.purpose.value === 'efficiency';
			rootEl.querySelector('.hs-cost-eff').hidden = !eff;
			rootEl.querySelector('.hs-cost-total').hidden = eff;
			rootEl.querySelector('.hs-cost-total-label').textContent = form.elements.purpose.value === 'training' ? '研修費用の合計（円）' : 'コンサル費用の合計（円）';
		}

		prefSel.addEventListener('change', fillCities);
		Array.prototype.forEach.call(form.elements.purpose, function (r) { r.addEventListener('change', toggleCost); });
		fillCities();
		toggleCost();

		form.addEventListener('submit', function (e) {
			e.preventDefault();
			render(result, data, {
				pref: prefSel.value,
				city: citySel.value,
				purpose: form.elements.purpose.value,
				industry: form.elements.industry.value,
				employees: num(form, 'employees') || 1,
				initial: num(form, 'initial'),
				monthly: num(form, 'monthly'),
				months: num(form, 'months') || 12,
				total: num(form, 'total'),
			});
		});
	}

	root.HikitsugiShindan = { Logic: Logic, init: init };
	if (typeof module !== 'undefined' && module.exports) module.exports = { Logic: Logic };

	if (typeof document !== 'undefined') {
		document.addEventListener('DOMContentLoaded', function () {
			var data = root.HIKITSUGI_SHINDAN_DATA;
			if (!data) return;
			Array.prototype.forEach.call(document.querySelectorAll('.hikitsugi-shindan'), function (el) { init(el, data); });
		});
	}
})(typeof window !== 'undefined' ? window : globalThis);
