import re,sys
t=open(sys.argv[1],encoding='utf-8',errors='replace').read()
pat=sys.argv[2] if len(sys.argv)>2 else '.'
for m in re.finditer(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>',t,re.S):
  s=re.sub('<[^>]+>','',m.group(2)).strip().replace('\n',' ')
  if s and re.search(pat,m.group(1)+s): print(m.group(1),s[:100])
