#!/usr/bin/env python3
"""補助金データの点検。更新が必要な制度を一覧にする

使い方:
    python3 scripts/check_subsidies.py            # 日付の点検だけ
    python3 scripts/check_subsidies.py --urls     # 公式URLの死活も確認する
    python3 scripts/check_subsidies.py --days 45  # 確認日が45日より古いものを出す（既定30日）

出力は Markdown。月1回の更新作業（docs/area-update.md）の最初に実行する。
"""

import argparse
import datetime
import glob
import os
import urllib.error
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "subsidies")


def as_date(v):
    if v is None:
        return None
    if isinstance(v, datetime.date):
        return v
    parts = [int(x) for x in str(v).split("-")]
    return datetime.date(parts[0], parts[1], parts[2] if len(parts) > 2 else 1)


def url_status(url):
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "Mozilla/5.0 (subsidy-check)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # タイムアウトやDNSエラー
        return type(e).__name__


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", action="store_true", help="公式URLにアクセスして確認する")
    ap.add_argument("--days", type=int, default=30, help="確認日がこの日数より古ければ再確認対象にする")
    args = ap.parse_args()

    today = datetime.date.today()
    issues = {"締切を過ぎたのに受付中のまま": [], "来年度の公募の見込み時期になった": [],
              "確認日が古い": [], "公式URLにアクセスできない": []}

    for path in sorted(glob.glob(os.path.join(SRC, "*.yml"))):
        if os.path.basename(path) == "areas.yml":
            continue
        for s in yaml.safe_load(open(path, encoding="utf-8")) or []:
            label = f"`{s['id']}` {s['name']}（{s['org']}）"
            period = s.get("period") or {}
            end = as_date(period.get("end"))
            if period.get("status") in ("open", "rolling") and end and end < today:
                issues["締切を過ぎたのに受付中のまま"].append(f"{label} 締切 {end}")
            nxt = as_date(s.get("next_expected"))
            if period.get("status") == "closed" and nxt and nxt <= today:
                issues["来年度の公募の見込み時期になった"].append(f"{label} 見込み {s['next_expected']}")
            checked = as_date(s.get("checked"))
            if checked and (today - checked).days > args.days:
                issues["確認日が古い"].append(f"{label} 確認日 {checked}")
            if args.urls:
                st = url_status(s["url"])
                if st != 200:
                    issues["公式URLにアクセスできない"].append(f"{label} → {st} {s['url']}")

    print(f"# 補助金データの点検（{today}）\n")
    total = 0
    for title, rows in issues.items():
        if title == "公式URLにアクセスできない" and not args.urls:
            continue
        print(f"## {title}（{len(rows)}件）\n")
        print("\n".join(f"- {r}" for r in rows) if rows else "- なし")
        print()
        total += len(rows)
    print(f"要対応：{total}件")


if __name__ == "__main__":
    main()
