#!/usr/bin/env python3
"""data/subsidies/*.yml から診断ツール用のJSONを作る

使い方:
    python3 scripts/build_shindan_data.py

出力: plugins/hikitsugi-shindan/data/subsidies.json
"""

import datetime
import glob
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "subsidies")
OUT = os.path.join(ROOT, "plugins", "hikitsugi-shindan", "data", "subsidies.json")

REQUIRED = ["id", "name", "org", "area", "targets", "period", "url", "checked", "confidence"]
TARGET_KEYS = {"efficiency", "consulting", "training"}


def to_jsonable(v):
    """YAMLが日付に変換した値を文字列に戻す"""
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    if isinstance(v, dict):
        return {k: to_jsonable(x) for k, x in v.items()}
    if isinstance(v, list):
        return [to_jsonable(x) for x in v]
    return v


def main():
    areas = yaml.safe_load(open(os.path.join(SRC, "areas.yml"), encoding="utf-8"))
    area_codes = {"national"}
    for pref in areas:
        area_codes.add(pref["code"])
        area_codes.update(c["code"] for c in pref["cities"])

    subsidies, errors = [], []
    for path in sorted(glob.glob(os.path.join(SRC, "*.yml"))):
        if os.path.basename(path) == "areas.yml":
            continue
        for d in yaml.safe_load(open(path, encoding="utf-8")) or []:
            sid = d.get("id", "?")
            missing = [k for k in REQUIRED if k not in d]
            if missing:
                errors.append(f"{sid}: 必須項目がない {missing}")
            if set(d.get("targets", {})) != TARGET_KEYS:
                errors.append(f"{sid}: targets のキーが不正")
            if d.get("area") not in area_codes:
                errors.append(f"{sid}: area {d.get('area')} が areas.yml にない")
            subsidies.append(to_jsonable(d))

    ids = [s["id"] for s in subsidies]
    if len(ids) != len(set(ids)):
        errors.append("id が重複している")
    for s in subsidies:
        for key in ("addon_to", "exclusive_with"):
            for ref in (s.get("stacking") or {}).get(key, []):
                if ref not in ids:
                    errors.append(f"{s['id']}: stacking.{key} の {ref} が存在しない")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)

    data = {
        "generated": datetime.date.today().isoformat(),
        "areas": areas,
        "subsidies": subsidies,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(subsidies)}制度を書き出しました: {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
