import sys,re,html
def rot47(s): return ''.join(chr(33+((ord(c)-33+47)%94)) if 33<=ord(c)<=126 else c for c in s)
def score(s): return len(re.findall(r'\b(the|and|of|to|in|at|for|with|is|on|was|said|were|from)\b',s,re.I))
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
m=re.search(r'<h1[^>]*class="headline"[^>]*>(.*?)</h1>',t,re.S); print('HEADLINE:',re.sub(r'<[^>]+>','',m.group(1)).strip() if m else None)
m=re.search(r'datetime="([^"]+)"',t); print('DATE:',m.group(1)[:10] if m else None)
m=re.search(r'class="[^"]*byline[^"]*"[^>]*>(.*?)</',t,re.S); print('BYLINE:',re.sub(r'<[^>]+>','',m.group(1)).strip()[:120] if m else None)
t=re.sub(r'(?s)<script.*?</script>','',t)
seen=set()
for p in re.findall(r'<p[^>]*>(.*?)</p>',t,re.S):
    p=html.unescape(re.sub(r'<[^>]+>','',p)).strip().replace('\n',' ')
    if len(p)<30 or p in seen: continue
    seen.add(p)
    d=rot47(p)
    best=d if score(d)>score(p) else p
    if score(best)>=2 and not re.search(r'(browser|password|account|Javascript|subscri|newsletter|Secure transaction|purchase|email address|Cancel anytime)',best,re.I): print('-',best)
