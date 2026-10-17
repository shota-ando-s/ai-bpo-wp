#!/usr/bin/env python3
"""地域ページの重複率（固定文・他ページとほぼ同じ段落・固有の割合）を出す。

使い方:
    python3 scripts/area_uniq.py                    # 愛媛の全ページ
    python3 scripts/area_uniq.py ehime iyo toon     # 指定ページの重複段落も表示
    python3 scripts/area_uniq.py kagawa             # 香川の全ページ
    python3 scripts/area_uniq.py tokushima          # 徳島の全ページ

目安は固有60%以上。下回るページは、国・県の制度の説明や FAQ の定型の回答を、その市町の事情に合わせて書き直す。
"""
import glob,os,re,sys
from difflib import SequenceMatcher
ROOT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'articles')+'/'
FIXED=["掲載している会社に直接ご相談","掲載している会社は、公式サイトなどの公開情報","どの業務からAIを入れるべきか","無料でAI活用診断を申し込む","ヒキツギAIの料金は","料金は、AIチャットが月5万円","ふえんは横浜市港北区を拠点に","ヒキツギAIとは、担当者しか知らない"]
def paras(p):
    body=open(p).read().split('---',2)[2]
    return [(x, any(f in x for f in FIXED)) for x in (y.strip() for y in re.split(r"\n\s*\n",body)) if len(x)>=40 and not x.startswith(('#','!','['))]
args=sys.argv[1:]
PREF=args.pop(0) if args and args[0] in ('ehime','kagawa','tokushima') else 'ehime'
files=sorted(glob.glob(ROOT+f'2026-10-17-area-{PREF}*.md'))
P={f:paras(f) for f in files}
def best(f,x):
    b=(0,'')
    for g in files:
        if g==f: continue
        for y,_ in P[g]:
            if SequenceMatcher(None,x,y,autojunk=False).quick_ratio()>0.8:
                r=SequenceMatcher(None,x,y,autojunk=False).ratio()
                if r>b[0]: b=(r,g)
    return b
targets=[ROOT+f'2026-10-17-area-{PREF}-{s}.md' for s in args] or files
for f in targets:
    total=sum(len(x) for x,_ in P[f]); dup=fixed=0; rows=[]
    for x,fx in P[f]:
        if fx: fixed+=len(x); continue
        r,g=best(f,x)
        if r>0.8: dup+=len(x); rows.append(f"  {r:.2f} {g[len(ROOT)+16:-3]:12s} {len(x):4d}字 {x[:70]!r}")
    print(f"{f[len(ROOT)+16:-3]:14s} 固定文 {fixed/total:5.1%} 重複 {dup/total:5.1%} 固有 {(total-fixed-dup)/total:5.1%}")
    if args: print("\n".join(rows))
