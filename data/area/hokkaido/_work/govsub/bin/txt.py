import re,sys,html
t=open(sys.argv[1],encoding=sys.argv[3] if len(sys.argv)>3 else 'utf-8',errors='replace').read()
t=re.sub(r'(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>','',t)
m=re.search(r'(?is)<main.*?</main>',t)
if m: t=m.group(0)
t=re.sub(r'(?i)<br\s*/?>|</(p|div|li|tr|h\d|dt|dd)>','\n',t)
t=re.sub(r'(?i)</t[dh]>',' | ',t)
t=re.sub(r'<a [^>]*href="([^"]+)"[^>]*>',r' [\1] ',t)
t=html.unescape(re.sub('<[^>]+>','',t))
t=re.sub(r'[ \t　]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
n=int(sys.argv[2]) if len(sys.argv)>2 else 5000
print(t[:n])
