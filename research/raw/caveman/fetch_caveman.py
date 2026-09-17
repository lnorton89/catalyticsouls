import urllib.request, json, re, html, time, os
UA={'User-Agent':'Mozilla/5.0 (research)'}
OUT='research/raw/caveman'
def get(u,binary=False):
    r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=90)
    d=r.read()
    return d if binary else d.decode('utf8','ignore')
def strip(h):
    h=re.sub(r'(?is)<(script|style).*?</\1>','',h)
    h=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</tr>|</li>|</h\d>|</td>','\n',h)
    h=re.sub(r'<[^>]+>',' ',h); h=html.unescape(h)
    h=re.sub(r'[ \t\r\f\v]+',' ',h); h=re.sub(r'\n\s*\n+','\n',h)
    return h.strip()
log=open(f'{OUT}/log.txt','a',encoding='utf8')
def L(s): log.write(s+'\n'); log.flush(); print(s,flush=True)
# 1. wait for the archive
rows=None
for i in range(240):   # up to ~4 hours at 60s
    try:
        t=get("https://web.archive.org/cdx/search/cdx?url=intergruv.net/caveman*&output=json&filter=statuscode:200&collapse=digest&limit=2000")
        if 'Temporarily Offline' in t: raise Exception('offline')
        rows=json.loads(t) if t.strip() else []
        break
    except Exception as e:
        L(f"wait{i} {str(e)[:60]}"); time.sleep(60)
if rows is None: L("GAVE UP waiting"); raise SystemExit
rows=rows[1:] if rows else []
L(f"CDX rows: {len(rows)}")
# also intergruv.net root pages for context
try:
    t=get("https://web.archive.org/cdx/search/cdx?url=intergruv.net/*&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=urlkey&limit=500")
    extra=json.loads(t)[1:] if t.strip() else []
    L(f"intergruv.net html pages: {len(extra)}")
    open(f'{OUT}/cdx_intergruv_all.json','w').write(json.dumps(extra))
except Exception as e: L(f"extra cdx err {e}")
json.dump(rows,open(f'{OUT}/cdx_caveman.json','w'),indent=1)
os.makedirs(f'{OUT}/pages',exist_ok=True)
for row in rows:
    urlkey,ts,orig,mime,status,digest,length=row[:7]
    name=re.sub(r'[^A-Za-z0-9._-]+','_',orig.split('://',1)[-1])[-90:]
    isimg=mime.startswith('image/')
    fn=f"{OUT}/pages/{ts}_{name}" + ('' if os.path.splitext(name)[1] else ('.'+mime.split('/')[-1] if isimg else '.html'))
    if os.path.exists(fn): continue
    for a in range(8):
        try:
            d=get(f"https://web.archive.org/web/{ts}id_/{orig}",binary=True)
            if b'Temporarily Offline' in d[:3000]: raise Exception('offline')
            open(fn,'wb').write(d)
            if not isimg:
                open(fn+'.txt','w',encoding='utf8').write(strip(d.decode('utf8','ignore')))
            L(f"OK {ts} {orig} {len(d)}"); break
        except Exception as e:
            L(f"retry{a} {orig} {str(e)[:60]}"); time.sleep(30)
    time.sleep(1.5)
L("DONE")
