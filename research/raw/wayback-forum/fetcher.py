import urllib.request, urllib.error, re, html, time, os, sys, json, threading, random
UA={'User-Agent':'Mozilla/5.0 (compatible; research-archive-reader; contact lnorton89@gmail.com)'}
LOCK=threading.Lock()
def get(url, tries=40, log=None):
    delay=3
    for i in range(tries):
        try:
            r=urllib.request.Request(url,headers=UA)
            with urllib.request.urlopen(r,timeout=90) as f:
                body=f.read().decode('utf8','ignore')
            if ('Temporarily Offline' in body or 'Internet Archive services are temporarily offline' in body) and 'phpBB' not in body:
                err='TEMP-OFFLINE'
                if log: log(f"  retry{i} {err} {url}")
                time.sleep(60); continue
            return body, None
        except urllib.error.HTTPError as e:
            if e.code in (404,403):
                return None, f"HTTP {e.code}"
            err=f"HTTP {e.code}"
        except Exception as e:
            err=repr(e)[:120]
        if log: log(f"  retry{i} {err} {url}")
        if 'refused' in err or '10061' in err:
            time.sleep(3+random.random()*3)
        else:
            time.sleep(delay+random.random()*2)
            delay=min(delay*1.7, 90)
    return None, err
def strip(h):
    h=re.sub(r'(?is)<(script|style).*?</\1>','',h)
    h=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</tr>|</li>|</h\d>|</td>','\n',h)
    h=re.sub(r'<[^>]+>',' ',h); h=html.unescape(h)
    h=re.sub(r'[ \t\r\f\v]+',' ',h); h=re.sub(r'\n\s*\n+','\n',h)
    return h.strip()
def safe_name(ts, orig):
    m=re.search(r'[?&]t=(\d+)', orig)
    if m: return f"t{m.group(1)}_{ts}"
    m=re.search(r'[?&]p=(\d+)', orig)
    if m: return f"p{m.group(1)}_{ts}"
    s=re.sub(r'^https?://(www\.)?catalyticsouls\.com(:80)?/','',orig)
    s=re.sub(r'[^A-Za-z0-9._=-]+','_',s)[:80]
    return f"{s}_{ts}"
def fetch_list(rows, outdir, workers=3, logpath=None):
    """rows: list of (ts, original). saves outdir/<name>.html"""
    os.makedirs(outdir, exist_ok=True)
    logf=open(logpath or os.path.join(outdir,'_fetch_log.txt'),'a',encoding='utf8')
    def log(s):
        with LOCK: logf.write(s+'\n'); logf.flush(); print(s, flush=True)
    todo=[(ts,o) for ts,o in rows if not os.path.exists(os.path.join(outdir,safe_name(ts,o)+'.html'))]
    log(f"START {len(rows)} rows, {len(todo)} to fetch")
    idx=[0]
    def worker():
        while True:
            with LOCK:
                if idx[0]>=len(todo): return
                ts,o=todo[idx[0]]; idx[0]+=1
            name=safe_name(ts,o)
            url=f"http://web.archive.org/web/{ts}id_/{o}"
            body,err=get(url, log=log)
            if body is None:
                log(f"FAIL {name} {err}")
                open(os.path.join(outdir,name+'.FAILED'),'w').write(err or '')
            else:
                open(os.path.join(outdir,name+'.html'),'w',encoding='utf8').write(body)
                log(f"OK {name} {len(body)}")
            time.sleep(1.0+random.random())
    ths=[threading.Thread(target=worker) for _ in range(workers)]
    [t.start() for t in ths]; [t.join() for t in ths]
    log("DONE")
if __name__=='__main__':
    which=sys.argv[1]
    rows=[]
    for line in open('cdx/forum-captures.txt',encoding='utf8'):
        p=line.split()
        if len(p)<3: continue
        ts,o=p[1],p[2]
        if which=='forums' and ('viewforum' in o or 'forums/index.php' in o or o.endswith('/forums/') or 'forum.php' in o):
            rows.append((ts,o))
        elif which=='topics' and 'viewtopic' in o and not os.path.exists('fetch-order.tsv'):
            rows.append((ts,o))
    if which=='topics' and os.path.exists('fetch-order.tsv'):
        rows=[(l.split('	')[1],l.split('	')[2]) for l in open('fetch-order.tsv',encoding='utf8') if l.strip()]
    outdir='forums_html' if which=='forums' else 'threads_html'
    workers=int(sys.argv[2]) if len(sys.argv)>2 else 3
    fetch_list(rows, outdir, workers=workers)
