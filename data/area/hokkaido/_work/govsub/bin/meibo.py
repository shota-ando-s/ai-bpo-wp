import re,sys,html,glob
rows={}
for f in sorted(glob.glob(sys.argv[1]+'/r_*.html'),key=lambda x:int(x.split('_')[-1][:-5])):
  t=open(f,encoding='utf-8',errors='replace').read()
  s=html.unescape(re.sub(r'<a [^>]*href="([^"]+)"[^>]*>',r' [\1] ',t))
  s=re.sub(r'<[^>]+>',' ',s); s=re.sub(r'[ \t　]+',' ',s)
  for m in re.finditer(r'(\d+)\.\s*(?:\[([^\]]*)\])?\s*(\S+)\s*〒\s*([\d\-]+)\s*住所\s*(.*?)\s*TEL\s*([\d\-]+)',s,re.S):
    rows[int(m.group(1))]=(m.group(3),m.group(4),re.sub(r'\s+',' ',m.group(5)).strip(),m.group(6),m.group(2) or "")
for k in sorted(rows): print('\t'.join([str(k)]+list(rows[k])))
