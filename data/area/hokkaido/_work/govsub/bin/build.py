import sys, re, json, openpyxl
S=sys.argv[1]; brief=sys.argv[2]
munis=[]; kyoku=None
for line in open(brief,encoding='utf-8'):
    m=re.match(r'### (.+?)（',line)
    if m and '振興局' in line: kyoku=m.group(1); continue
    m=re.match(r'\| (\S+?) \| (\d{6}) \| (\S+) \| `([^`]+)` \|',line)
    if m and kyoku: munis.append(dict(kyoku=kyoku,name=m.group(1),code=m.group(2),yomi=m.group(3),slug=m.group(4)))
print(len(munis),file=sys.stderr)
def rows(f,start=5):
    ws=openpyxl.load_workbook(f'{S}/dl/soumu/{f}.xlsx',read_only=True).worksheets[0]
    hdr=list(ws.iter_rows(min_row=2,max_row=4,values_only=True))
    data=[r for r in ws.iter_rows(min_row=start,values_only=True)]
    return hdr,data
# status files: by pref col 3, name col 4
def status(f):
    hdr,data=rows(f); out={}
    names=[ (hdr[2][j] or '') for j in range(len(hdr[2]))]
    for r in data:
        if r[3]!='北海道': continue
        nm=r[4] if r[4] not in (None,'-') else '北海道'
        st='導入済' if r[5]=='○' else ('実証中' if r[6]=='○' else '?')
        sel=[names[j] for j in range(7,len(r)) if r[j]=='○']
        oth=[str(r[j]) for j in range(7,len(r)) if r[j] not in (None,'','○')]
        out[nm]=dict(st=st,sel=sel,oth=oth)
    return out
def detail(f):
    hdr,data=rows(f); out={}
    h3=[hdr[2][j] for j in range(len(hdr[2]))]; h1=[hdr[0][j] for j in range(len(hdr[0]))]
    for r in data:
        if r[5]!='北海道': continue
        nm=r[6] if r[6] not in (None,'-') else '北海道'
        d={'code':r[1],'cells':{}}
        for j in range(7,len(r)):
            if r[j] not in (None,''): d['cells'][j]=r[j]
        out.setdefault(nm,[]).append(d)
    return out,h1,h3
g=status('001070424'); a=status('001070421')
gd,gh1,gh3=detail('001070425'); ad,ah1,ah3=detail('001070422')
json.dump(dict(munis=munis,g=g,a=a,gd=gd,ad=ad,gh1=gh1,gh3=gh3,ah1=ah1,ah3=ah3),open(f'{S}/hk.json','w'),ensure_ascii=False,default=str)
names={m['name'] for m in munis}
print('g not in munis',[k for k in g if k not in names]); print('a not in',[k for k in a if k not in names])
print('gd not',[k for k in gd if k not in names]); print('ad not',[k for k in ad if k not in names])
print('counts g',len(g),'a',len(a),'gd',len(gd),'ad',len(ad))
from collections import Counter
print(Counter(m['kyoku'] for m in munis))
