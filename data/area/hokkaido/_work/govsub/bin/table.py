import sys,json,re
S=sys.argv[1]; D=json.load(open(f'{S}/hk.json'))
def clean(s): return re.sub(r"^[・\s]+","",re.sub(r'\s*※.*','',str(s)).replace('　',' ').strip())
def tools(nm):
    out=[]
    for d in D['gd'].get(nm,[]):
        c={int(k):v for k,v in d['cells'].items()}
        t=clean(c.get(9,''))
        if c.get(10): t=(t+'「'+clean(c[10])+'」') if t and t!='その他' else 'その他「'+clean(c[10])+'」'
        extra=[]
        if c.get(8)=='○': extra.append('実証中')
        if c.get(18)=='○': extra.append('RAG')
        if c.get(38)=='○': extra.append('個別契約')
        elif c.get(37)=='○': extra.append('約款型')
        elif c.get(39)=='○': extra.append('試用中')
        out.append(t+('（'+'・'.join(extra)+'）' if extra else ''))
    return out
def tasks(nm):
    return [clean(d['cells'].get('11','')) for d in D['ad'].get(nm,[])]
def row(m):
    nm=m['name'] if m!='道' else '北海道'
    g=D['g'].get(nm); a=D['a'].get(nm)
    gs=g['st'] if g else '**表にない**'
    t=tools(nm); 
    gt='、'.join(t) if t else ('-（詳細の行なし）' if g else '-')
    if len(t)>1: gt+=f'（{len(t)}行）'
    as_=a['st'] if a else '**表にない**'
    tk=tasks(nm); at='、'.join(tk) if tk else ('-（詳細の行なし）' if a else '-')
    if tk: at+=f'（{len(tk)}件）'
    return gs,gt,as_,at
mode=sys.argv[2]
if mode=='all':
    g,gt,a,at=row('道'); print(f'| （道） | 北海道 | hokkaido | 010006 | {g} | {gt} | {a} | {at} |')
    for m in D['munis']:
        g,gt,a,at=row(m)
        print(f"| {m['kyoku'].replace('総合振興局','').replace('振興局','')} | {m['name']} | {m['slug']} | {m['code']} | {g} | {gt} | {a} | {at} |")
elif mode=='stats':
    from collections import defaultdict
    k=defaultdict(lambda:[0,0,0,0,0])
    for m in D['munis']:
        r=k[m['kyoku']]; r[0]+=1
        g=D['g'].get(m['name']); a=D['a'].get(m['name'])
        if g and g['st']=='導入済': r[1]+=1
        if g and g['st']=='実証中': r[2]+=1
        if a: r[3]+=1
        if not g and not a: r[4]+=1
    tot=[0]*5
    for kk,r in k.items():
        print(f'| {kk} | {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |'); tot=[x+y for x,y in zip(tot,r)]
    print('| 計 |',' | '.join(map(str,tot)),'|')
    # mismatches status vs detail
    for nm in D['g']:
        if nm not in D['gd']: print('gen status only',nm)
    for nm in D['a']:
        if nm not in D['ad']: print('ai status only',nm)
    for nm in D['gd']:
        if nm not in D['g']: print('gen detail only',nm)
