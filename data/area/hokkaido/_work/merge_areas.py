# areas.yml の北海道の行を data/area/hokkaido/_areas_snippet.yml で置き換える（ほかの県の行は変えない）。使い方: python3 data/area/hokkaido/_work/merge_areas.py data/subsidies/areas.yml data/area/hokkaido/_areas_snippet.yml
import sys
dst,snip=sys.argv[1],sys.argv[2]
s=open(dst).read()
i=s.index('- code: hokkaido\n')
j=s.find('\n- code: ',i+5)
# also strip comment lines directly before next block belong to next pref: find start of comment block before j
if j==-1: j=len(s)
else:
    k=j
    lines=s[:j].split('\n')
    # walk back over comment lines preceding next code
    while lines and lines[-1].startswith('#'): lines.pop()
    j=len('\n'.join(lines))
n=open(snip).read(); n=n[n.index('- code: hokkaido\n'):].rstrip('\n')
s=s[:i]+n+s[j:]
open(dst,'w').write(s)
