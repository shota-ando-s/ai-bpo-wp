# 補助金・助成金データ

診断ツール（`/shindan/`）、締切カレンダー（`/calendar/`）、地域ページの補助金表の元データ。1ファイル＝1地域（国は `national.yml`）。

## 項目

| キー | 必須 | 内容 |
|---|---|---|
| id | ○ | 一意のID（英小文字とハイフン） |
| name | ○ | 制度名 |
| org | ○ | 実施主体 |
| area | ○ | 対象地域。`national`、都県コード（`tokyo` など）、区市コード（`tokyo/shinagawa` など） |
| max_yen | | 補助上限（円）。定額や記載なしは null |
| rate | | 補助率の表記（例 `1/2（小規模2/3）`） |
| targets | ○ | 使えるサービスの判定。`efficiency`（AI業務効率化）、`consulting`（AIコンサル）、`training`（AI研修）に ◎ ○ △ × を入れる |
| expenses | | 対象経費の要約 |
| conditions | | 対象者や申請の条件 |
| period | ○ | `open`（受付中）、`closed`（今年度は終了）、`rolling`（随時）、`unknown`。`start` と `end`（YYYY-MM-DD）を併記できる |
| next_expected | | 来年度の公募開始の見込み（例 `2027-04`）。今年度の公募時期からの推測なので、表示するときは「見込み」と書く |
| stacking | | 併用・上乗せの関係。`addon_to: [id]`（上乗せ先）、`exclusive_with: [id]`（併用不可） |
| url | ○ | 公式URL |
| checked | ○ | 確認日（YYYY-MM-DD） |
| confidence | ○ | `official`（公式で確認）、`secondary`（二次情報） |
| note | | 補足、注意点 |
| rate_num | | 試算に使う補助率（小数）。定額の制度は書かない |
| rate_small_num | | 小規模事業者の補助率（小数） |
| max_months | | 月額利用料を補助する最大の月数 |
| min_cost_yen | | 対象経費の下限（円） |
| small_only | | true なら小規模事業者だけが対象 |
| addon | | 上乗せ制度の計算方法。`{kind: remaining, ratio: 0.5}` は（経費−上乗せ先の補助額）×0.5、`{kind: cost_ratio, ratio: 0.2}` は経費×0.2、`{kind: remaining_tiered, full_upto: 250000, ratio: 0.5}` は（経費−上乗せ先の補助額）のうち full_upto までは全額・超えた分×0.5（千円未満切り捨て）。どれも max_yen が上限 |
| fuenn_available_from | | ふえんのサービスで使えるようになる時期（YYYY-MM）。それまでは診断で「来年度」に表示する |
| fuenn_note | | 診断結果に出す、ふえんからの案内文 |

## 地域名

`areas.yml` に、地域コードと表示名を持たせる。独自の制度がない区市も載せ、診断で「独自の制度はない」と表示する。

## 診断ツールへの反映

```bash
python3 scripts/build_shindan_data.py
```

`plugins/hikitsugi-shindan/data/subsidies.json` が更新される。JSONもコミットしてからデプロイする（サーバーではYAMLを読まない）。

## 運用

- 月1回、受付状況と締切を確認して `checked` を更新する。
- 予算残額は公開されていないので、`open` でも締め切られている場合がある。表示側で必ず注記する。
