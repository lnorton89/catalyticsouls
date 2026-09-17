import sys,re,html
def rot47(s):
    return ''.join(chr(33+((ord(c)-33+47)%94)) if 33<=ord(c)<=126 else c for c in s)
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
m=re.search(r'<h1[^>]*class="headline"[^>]*>(.*?)</h1>',t,re.S); print('HEADLINE:',re.sub(r'<[^>]+>','',m.group(1)).strip() if m else None)
m=re.search(r'datetime="([^"]+)"',t); print('DATE:',m.group(1) if m else None)
m=re.search(r'"author":\s*\{[^}]*"name":\s*"([^"]+)"',t); print('AUTHOR:',m.group(1) if m else None)
t=re.sub(r'(?s)<script.*?</script>','',t)
paras=re.findall(r'<p[^>]*>(.*?)</p>',t,re.S)
out=[]
for p in paras:
    p=html.unescape(re.sub(r'<[^>]+>','',p)).strip()
    if len(p)<25: continue
    words=len(re.findall(r'\b(the|and|of|to|in|at|for|with|is|on)\b',p,re.I))
    if words<2:
        d=rot47(p)
        if len(re.findall(r'\b(the|and|of|to|in|at|for|with|is|on)\b',d,re.I))>=2: out.append(d)
    else:
        if not re.search(r'(browser|password|account|Javascript|subscri|newsletter|Secure transaction|purchase)',p,re.I): out.append(p)
print('\n'.join(out)[:6000])
