import re, html, sys
from html.parser import HTMLParser
class Strip(HTMLParser):
    def __init__(s): super().__init__(); s.out=[]; s.skip=0; s.imgs=[]; s.links=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in("script","style"): s.skip+=1
        if t=="img": s.imgs.append((a.get("src",""),a.get("alt","")))
        if t=="a" and a.get("href"): s.links.append(a["href"])
        if t in("br","p","div","tr","li","h1","h2","h3","h4","td","table","center"): s.out.append("\n")
    def handle_endtag(s,t):
        if t in("script","style"): s.skip=max(0,s.skip-1)
        if t in("p","div","tr","li","h1","h2","h3","h4","table","center"): s.out.append("\n")
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
def totext(h):
    s=Strip()
    try: s.feed(h)
    except Exception: pass
    t=html.unescape("".join(s.out)); t=re.sub(r"[ \t\r\xa0]+"," ",t); t=re.sub(r"\n\s*\n+","\n",t).strip()
    return t, s.imgs, s.links
if __name__=="__main__":
    for p in sys.argv[1:]:
        h=open(p,encoding="utf-8",errors="replace").read()
        t,imgs,links=totext(h)
        open(re.sub(r"\.html?$","",p)+".txt","w",encoding="utf-8").write(t+"\n\n--- IMAGES ---\n"+"\n".join(f"{a} | alt={b}" for a,b in imgs)+"\n--- LINKS ---\n"+"\n".join(links))
