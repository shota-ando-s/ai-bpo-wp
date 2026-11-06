import re,sys,html
t=open(sys.argv[1],'rb').read()
enc=sys.argv[4] if len(sys.argv)>4 else 'utf-8'
t=t.decode(enc,errors='replace')
t=re.sub(r'(?is)<(script|style|head|nav|footer|header)[^>]*>.*?</\1>','',t)
t=re.sub(r'(?i)<br\s*/?>|</(p|div|li|tr|h\d|dt|dd)>','\n',t)
t=re.sub(r'(?i)</t[dh]>',' | ',t)
t=re.sub(r'<a [^>]*href="([^"]+)"[^>]*>',r' [\1] ',t)
t=html.unescape(re.sub('<[^>]+>','',t))
t=re.sub(r'[ \t　]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
k=sys.argv[3] if len(sys.argv)>3 else ''
i=t.find(k) if k else 0
i=max(i,0)
print(t[i:i+int(sys.argv[2])])
