import sys,json,re
S=sys.argv[1]; D=json.load(open(f'{S}/hk.json'))
def cl(s): return re.sub(r'\s*※.*','',str(s)).replace('　',' ').strip()
gh3=D['gh3']; ah3=D['ah3']
for nm in sys.argv[2:]:
    print('#####',nm)
    g=D['g'].get(nm); a=D['a'].get(nm)
    if g: print('GEN status',g['st'],'| sel:',g['sel'],'| oth:',g['oth'])
    for d in D['gd'].get(nm,[]):
        c={int(k):v for k,v in d['cells'].items()}
        print(' gd',d['code'],{j:(cl(gh3[j]) if c[j]=='○' else str(c[j])[:600]) for j in sorted(c)})
    if a: print('AI status',a['st'],'| sel:',a['sel'],'| oth:',a['oth'])
    for d in D['ad'].get(nm,[]):
        c={int(k):v for k,v in d['cells'].items()}
        print(' ad',d['code'],{j:(cl(ah3[j])[:25] if c[j]=='○' else str(c[j])[:600]) for j in sorted(c)})
