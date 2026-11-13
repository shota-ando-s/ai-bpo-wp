#!/usr/bin/env python3
"""前回投稿したあとに変わった記事を、まとめて WordPress に投稿する。

使い方:
    python3 scripts/post_changed.py --dry-run   # 何を投稿・デプロイするかを表示するだけ
    python3 scripts/post_changed.py             # デプロイ（必要なとき）→ 記事の投稿
    python3 scripts/post_changed.py --init REV  # REV（例 HEAD）までは投稿済みとして記録する（初回だけ）

- 前回すべて投稿し終えたコミットを .post_state.json（Git 管理外）に持ち、そこから HEAD までに
  articles/ で追加・変更された .md を投稿する。コミットしていない変更があると止まる
- 固定ページは親から先に投稿する（parent の階層が浅い順）。親が失敗すると子も失敗するので、
  ある階層で1件でも失敗したら、より深い階層は投稿しない
- WordPress が空の応答を返して止まることがあるので、失敗したら1回だけ間を空けて投稿し直す
- 途中で止まったら、投稿できた記事を記録しておき、次に実行したときは残りだけ投稿する
- themes/ plugins/ data/subsidies/ が変わっていれば、補助金の JSON を作り直してから ./deploy.sh を実行する
"""

import argparse
import json
import os
import subprocess
import sys
import time

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, ".post_state.json")
DEPLOY_PATHS = ("themes/", "plugins/", "data/subsidies/")
RETRY_WAIT = 10


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def rev(name):
    return git("rev-parse", "--verify", f"{name}^{{commit}}").strip()


def load_state():
    if not os.path.exists(STATE):
        return None
    with open(STATE, encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")


def changed_files(base, head):
    """base..head で変わったファイルを (追加・変更, 削除) で返す。名前の変更は新しい名前を追加として扱う"""
    changed, deleted = [], []
    for line in git("diff", "--name-status", "-M", base, head).splitlines():
        status, *paths = line.split("\t")
        if status.startswith("D"):
            deleted.append(paths[0])
        else:
            changed.append(paths[-1])
    return changed, deleted


def depth(path):
    """投稿の順番。投稿と最上位の固定ページは 0、area/akita の子は 2"""
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        text = f.read()
    meta = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
    if meta.get("type") != "page":
        return 0
    return len([s for s in str(meta.get("parent") or "").strip("/").split("/") if s])


def post(path):
    """post.py を実行し、(成功したか, 新規投稿か, 出力) を返す"""
    for attempt in (1, 2):
        r = subprocess.run([sys.executable, "post.py", path], cwd=ROOT, capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        if r.returncode == 0:
            return True, "投稿完了" in out, out
        if attempt == 1:
            print(f"  失敗。{RETRY_WAIT}秒後にもう一度投稿します")
            time.sleep(RETRY_WAIT)
    return False, False, out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="投稿・デプロイせずに対象を表示する")
    ap.add_argument("--init", metavar="REV", help="REV までを投稿済みとして記録して終わる")
    ap.add_argument("--no-deploy", action="store_true", help="デプロイしない")
    args = ap.parse_args()

    if args.init:
        save_state({"base": rev(args.init), "target": None, "done": []})
        print(f"{rev(args.init)[:7]} までを投稿済みとして記録しました")
        return

    state = load_state()
    if state is None:
        print("Error: 前回の投稿の記録（.post_state.json）がありません。"
              "最後にすべて投稿し終えたコミットを --init で記録してください（例: --init HEAD）", file=sys.stderr)
        sys.exit(1)

    dirty = git("status", "--porcelain", "--", "articles", *DEPLOY_PATHS).strip()
    if dirty:
        print("Error: コミットしていない変更があります。先にコミットしてください:\n" + dirty, file=sys.stderr)
        sys.exit(1)

    head = rev("HEAD")
    # 途中で止まった回の続きなら、その回に投稿できた記事を飛ばす。その後にまた変わった記事は投稿し直す
    done = set(state.get("done") or []) if state.get("target") else set()
    if done and state["target"] != head:
        done -= set(changed_files(state["target"], head)[0])
    changed, deleted = changed_files(state["base"], head)
    articles = sorted(p for p in changed if p.startswith("articles/") and p.endswith(".md"))
    todo = [p for p in articles if p not in done]
    needs_deploy = any(p.startswith(DEPLOY_PATHS) for p in changed)

    print(f"前回の投稿: {state['base'][:7]} → いま: {head[:7]}")
    print(f"投稿する記事: {len(todo)}件" + (f"（前回の途中までで投稿済み {len(done)}件は飛ばす）" if done else ""))
    for p in todo:
        print(f"  {p}")
    for p in deleted:
        if p.startswith("articles/"):
            print(f"  削除された記事（WordPress からは消さない）: {p}")
    print("デプロイ: " + ("する（themes/ plugins/ data/subsidies/ が変わった）" if needs_deploy and not args.no_deploy else "しない"))
    if args.dry_run:
        return

    if needs_deploy and not args.no_deploy:
        print("\n==> 補助金の JSON を作り直します")
        subprocess.run([sys.executable, "scripts/build_shindan_data.py"], cwd=ROOT, check=True)
        if git("status", "--porcelain", "--", "plugins/hikitsugi-shindan/data").strip():
            print("Error: 補助金の JSON がコミットと違います。作り直した JSON をコミットしてから実行し直してください",
                  file=sys.stderr)
            sys.exit(1)
        print("==> デプロイします")
        subprocess.run(["./deploy.sh"], cwd=ROOT, check=True)

    state["target"] = head
    state["done"] = sorted(done)
    save_state(state)

    created, failed = [], []
    for level in sorted({depth(p) for p in todo}):
        if failed:
            break
        for p in [p for p in todo if depth(p) == level]:
            print(f"\n==> {p}")
            ok, is_new, out = post(p)
            print("  " + out.replace("\n", "\n  "))
            if ok:
                done.add(p)
                state["done"] = sorted(done)
                save_state(state)
                if is_new:
                    created.append(p)
            else:
                failed.append(p)

    skipped = [p for p in todo if p not in done and p not in failed]
    print("\n==> 結果")
    print(f"投稿・更新できた記事: {len([p for p in todo if p in done])}件")
    if created:
        print("新しく作ったページ（画像に地図が入っていないか目で確かめる）:")
        for p in created:
            print(f"  {p}")
    if failed or skipped:
        for p in failed:
            print(f"  失敗: {p}")
        for p in skipped:
            print(f"  未投稿（親の階層で失敗があったため）: {p}")
        print("もう一度このスクリプトを実行すると、残りだけ投稿します")
        sys.exit(1)

    save_state({"base": head, "target": None, "done": []})
    print(f"すべて投稿しました。{head[:7]} までを投稿済みとして記録しました")


if __name__ == "__main__":
    main()
