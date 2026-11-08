#!/usr/bin/env python3
"""ヒキツギAI（hikitsugi.jp）→ かんたんAI（kantan-ai.jp）の置き換えをリポジトリに適用する。

WordPress のデータベースは scripts/cutover_kantan.sh が同じ規則で置き換える。
何度実行しても同じ結果になる（置き換え済みのものは変わらない）。

変えないもの:
- checklist.hikitsugi.jp（別サーバーの別サービス）
- ページの URL のパス（/hikitsugi-ai-bpo-step/ など）、プラグインやコードの内部名（hikitsugi-smtp・HIKITSUGI_SMTP_* など）
- 移行の経緯を書いた記録（EXCLUDE）

使い方:
    python3 scripts/rebrand_kantan.py --dry-run   # 変わるファイルと件数を表示
    python3 scripts/rebrand_kantan.py             # 置き換える
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RULES = [
    (re.compile(r"ヒキツギAI"), "かんたんAI"),
    (re.compile(r"https?:(//|\\/\\/)(?:www\.)?hikitsugi\.jp"), r"https:\1kantan-ai.jp"),
    (re.compile(r"(?<![\w.-])(send|offboard)\.hikitsugi\.jp"), r"\1.kantan-ai.jp"),
    # checklist.hikitsugi.jp は前に「.」があるので当たらない
    (re.compile(r"(?<![\w.-])(?:www\.)?hikitsugi\.jp"), "kantan-ai.jp"),
]

EXCLUDE = {
    "scripts/rebrand_kantan.py",
    "scripts/cutover_kantan.sh",
    # 経緯の記録。切り替えのあとに手で書き直す
    "memory/project_domain_migration.md",
    "memory/project_brand_name.md",
    "memory/MEMORY.md",
    ".claude/settings.json",
}


def main():
    dry = "--dry-run" in sys.argv
    files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    changed = total = 0
    for rel in files:
        if not rel or rel in EXCLUDE:
            continue
        p = ROOT / rel
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        new, n = text, 0
        for pat, rep in RULES:
            new, k = pat.subn(rep, new)
            n += k
        if n:
            changed += 1
            total += n
            if dry:
                print(f"{n:5d}  {rel}")
            else:
                p.write_text(new, encoding="utf-8")
    print(f"{'変わる' if dry else '置き換えた'}ファイル: {changed}件、箇所: {total}件")


if __name__ == "__main__":
    main()
