import json, os, re, sys, time, html, urllib.request
from html.parser import HTMLParser
class Strip(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0; s.imgs=[]; s.links=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in("script","style"): s.skip+=1
        if t=="img": s.imgs.append((a.get("src",""),a.get("alt","")))
        if t=="a" and a.get("href"): s.links.append(a["href"])
        if t in("br","p","div","tr","li","h1","h2","h3","h4","td","table","center","font"): s.out.append("\n")
    def handle_endtag(s,t):
        if t in("script","style"): s.skip=max(0,s.skip-1)
        if t in("p","div","tr","li","h1","h2","h3","h4","table","center"): s.out.append("\n")
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
def totext(h):
    p=Strip(); 
    try: p.feed(h)
    except Exception: pass
    t="".join(p.out); t=html.unescape(t)
    t=re.sub(r"[ \t\r\xa0]+"," ",t); t=re.sub(r"\n\s*\n+","\n",t)
    return t.strip(), p.imgs, p.links
def fetch(url, tries=7):
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 research-scraper"})
            with urllib.request.urlopen(req,timeout=120) as r:
                return r.read(), r.geturl()
        except Exception as e:
            code=getattr(e,"code",None)
            if code==404: return None,None
            print(f"  retry {i} {url[:90]} -> {e}",file=sys.stderr); sys.stderr.flush()
            time.sleep(5*(i+1))
    return None,None
domains=sys.argv[1:]
for d in domains:
    rows=json.load(open(f"cdx/{d}.json"))[1:]
    os.makedirs(f"pages/{d}",exist_ok=True)
    for ts,orig,mt,st,dg,ln in rows:
        if mt!="text/html": continue
        if "cgi-bin/ad" in orig or "cgi-bin/login" in orig or "/manual/" in orig: continue
        path=orig.split("://",1)[1].split("/",1)[1] if "/" in orig.split("://",1)[1] else ""
        safe=re.sub(r"[^A-Za-z0-9._-]+","_",path)[:80] or "root"
        base=f"pages/{d}/{ts}_{safe}"
        if os.path.exists(base+".txt"): continue
        data,final=fetch(f"https://web.archive.org/web/{ts}id_/{orig}")
        if data is None:
            print("MISS",ts,orig); continue
        try: h=data.decode("utf-8")
        except UnicodeDecodeError: h=data.decode("latin-1")
        open(base+".html","w",encoding="utf-8").write(h)
        t,imgs,links=totext(h)
        with open(base+".txt","w",encoding="utf-8") as f:
            f.write(f"SOURCE: {orig}\nCAPTURE: {ts}\nFETCHED: https://web.archive.org/web/{ts}id_/{orig}\n\n{t}\n\n--- IMAGES ---\n")
            for s,a in imgs: f.write(f"{s} | alt={a}\n")
            f.write("--- LINKS ---\n"); f.write("\n".join(links))
        print("OK",ts,orig,len(t)); sys.stdout.flush()
        time.sleep(1.5)
