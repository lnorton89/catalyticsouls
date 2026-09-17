import json, os, re, sys, time, urllib.request, random
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,".")
from strip import totext
def fetch(url, tries=14):
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 research-scraper"})
            with urllib.request.urlopen(req,timeout=120) as r:
                return r.read()
        except Exception as e:
            code=getattr(e,"code",None)
            if code==404: return None
            time.sleep(min(60, 3*(i+1))+random.random()*2)
    return None
def job(args):
    d,ts,orig=args
    path=orig.split("://",1)[1].split("/",1)[1] if "/" in orig.split("://",1)[1] else ""
    safe=re.sub(r"[^A-Za-z0-9._-]+","_",path)[:80] or "root"
    base=f"pages/{d}/{ts}_{safe}"
    if os.path.exists(base+".txt"): return "SKIP"
    data=fetch(f"https://web.archive.org/web/{ts}id_/{orig}")
    if data is None: return f"MISS {ts} {orig}"
    try: h=data.decode("utf-8")
    except UnicodeDecodeError: h=data.decode("latin-1")
    open(base+".html","w",encoding="utf-8").write(h)
    t,imgs,links=totext(h)
    with open(base+".txt","w",encoding="utf-8") as f:
        f.write(f"SOURCE: {orig}\nCAPTURE: {ts}\nFETCHED: https://web.archive.org/web/{ts}id_/{orig}\n\n{t}\n\n--- IMAGES ---\n")
        for s,a in imgs: f.write(f"{s} | alt={a}\n")
        f.write("--- LINKS ---\n"); f.write("\n".join(links))
    time.sleep(1)
    return f"OK {ts} {orig} {len(t)}"
jobs=[]
for d in sys.argv[1:]:
    os.makedirs(f"pages/{d}",exist_ok=True)
    for ts,orig,mt,st,dg,ln in json.load(open(f"cdx/{d}.json"))[1:]:
        if mt!="text/html": continue
        if "cgi-bin/ad" in orig or "cgi-bin/login" in orig or "/manual/" in orig: continue
        jobs.append((d,ts,orig))
print(len(jobs),"jobs"); sys.stdout.flush()
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(job,jobs):
        if r!="SKIP": print(r); sys.stdout.flush()
print("ALLDONE")
