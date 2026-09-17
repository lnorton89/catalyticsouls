import sys,re,html
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'(?s)<script.*?</script>','',t); t=re.sub(r'(?s)<style.*?</style>','',t); t=re.sub(r'(?s)<!--.*?-->','',t)
if len(sys.argv)>2 and sys.argv[2]=='links':
    for m in re.findall(r'href="([^"]+)"',t): print(m)
    sys.exit()
t=re.sub(r'<br\s*/?>|</p>|</div>|</tr>|</li>|</h\d>','\n',t); t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t)
for l in t.splitlines():
    l=re.sub(r'\s+',' ',l).strip()
    if l: print(l)
