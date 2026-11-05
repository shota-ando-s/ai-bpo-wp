#!/usr/bin/env python3
"""地域ページの重複率（固定文・他ページとほぼ同じ段落・固有の割合）を出す。

使い方:
    python3 scripts/area_uniq.py                    # 愛媛の全ページ
    python3 scripts/area_uniq.py ehime iyo toon     # 指定ページの重複段落も表示
    python3 scripts/area_uniq.py kagawa             # 香川の全ページ
    python3 scripts/area_uniq.py tokushima          # 徳島の全ページ
    python3 scripts/area_uniq.py kochi              # 高知の全ページ
    python3 scripts/area_uniq.py aomori             # 青森の全ページ
    python3 scripts/area_uniq.py iwate              # 岩手の全ページ（ファイル名の日付は 2026-10-18）
    python3 scripts/area_uniq.py akita              # 秋田の全ページ（ファイル名の日付は 2026-10-18）
    python3 scripts/area_uniq.py miyagi             # 宮城の全ページ（ファイル名の日付は 2026-10-23）
    python3 scripts/area_uniq.py yamagata           # 山形の全ページ
    python3 scripts/area_uniq.py fukushima          # 福島の全ページ
    python3 scripts/area_uniq.py toyama             # 富山の全ページ
    python3 scripts/area_uniq.py ishikawa           # 石川の全ページ
    python3 scripts/area_uniq.py fukui              # 福井の全ページ
    python3 scripts/area_uniq.py gifu               # 岐阜の全ページ
    python3 scripts/area_uniq.py niigata            # 新潟の全ページ
    python3 scripts/area_uniq.py nagano             # 長野の全ページ
    python3 scripts/area_uniq.py yamanashi          # 山梨の全ページ（山梨市の slug は yamanashi-city）
    python3 scripts/area_uniq.py shimane            # 島根の全ページ（美郷町の slug は misato-town-shimane）
    python3 scripts/area_uniq.py tottori            # 鳥取の全ページ（鳥取市の slug は tottori-city）
    python3 scripts/area_uniq.py hiroshima          # 広島の全ページ（広島市の slug は hiroshima-city）
    python3 scripts/area_uniq.py yamaguchi          # 山口の全ページ（山口市の slug は yamaguchi-city）
    python3 scripts/area_uniq.py okayama            # 岡山の全ページ（岡山市の slug は okayama-city）
    python3 scripts/area_uniq.py saga               # 佐賀の全ページ（佐賀市の slug は saga-city）
    python3 scripts/area_uniq.py fukuoka            # 福岡の全ページ（福岡市の slug は fukuoka-city、北九州市は kitakyushu）
    python3 scripts/area_uniq.py kagoshima          # 鹿児島の全ページ（鹿児島市の slug は kagoshima-city）
    python3 scripts/area_uniq.py gunma              # 群馬の全ページ
    python3 scripts/area_uniq.py ibaraki            # 茨城の全ページ（茨城町の slug は ibaraki-town）
    python3 scripts/area_uniq.py tochigi            # 栃木の全ページ（栃木市の slug は tochigi-city、那珂川町は nakagawa-town）
    python3 scripts/area_uniq.py oita               # 大分の全ページ（大分市の slug は oita-city）
    python3 scripts/area_uniq.py kumamoto           # 熊本の全ページ（熊本市の slug は kumamoto-city）
    python3 scripts/area_uniq.py miyazaki           # 宮崎の全ページ（宮崎市の slug は miyazaki-city）
    python3 scripts/area_uniq.py okinawa            # 沖縄の全ページ（沖縄市の slug は okinawa-city）

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
PREF=args.pop(0) if args and args[0] in ('ehime','kagawa','tokushima','kochi','aomori','iwate','akita','miyagi','yamagata','fukushima','niigata','toyama','ishikawa','fukui','gifu','nagano','yamanashi','shimane','tottori','hiroshima','yamaguchi','okayama','saga','kagoshima','oita','nagasaki','fukuoka','kumamoto','miyazaki','gunma','ibaraki','okinawa','tochigi') else 'ehime'
# 県ごとにファイル名の日付が違う（四国・青森は 2026-10-17、岩手は 2026-10-18）ので日付は問わない
files=sorted(glob.glob(ROOT+f'2026-??-??-area-{PREF}.md')+glob.glob(ROOT+f'2026-??-??-area-{PREF}-*.md'))
DATE={os.path.basename(f)[:10] for f in files}.pop() if files else '2026-10-17'
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
targets=[ROOT+f'{DATE}-area-{PREF}-{s}.md' for s in args] or files
for f in targets:
    total=sum(len(x) for x,_ in P[f]); dup=fixed=0; rows=[]
    for x,fx in P[f]:
        if fx: fixed+=len(x); continue
        r,g=best(f,x)
        if r>0.8: dup+=len(x); rows.append(f"  {r:.2f} {g[len(ROOT)+16:-3]:12s} {len(x):4d}字 {x[:70]!r}")
    print(f"{f[len(ROOT)+16:-3]:14s} 固定文 {fixed/total:5.1%} 重複 {dup/total:5.1%} 固有 {(total-fixed-dup)/total:5.1%}")
    if args: print("\n".join(rows))
