import os, re, glob, collections, sys
# Lines that are nav-menu items recur across many pages of the same domain; treat a line as "nav" if it appears in >= 40% of the domain's captures
out=open("bodies_by_page.txt","w",encoding="utf-8")
for d in sorted(os.listdir("pages")):
    files=sorted(glob.glob(f"pages/{d}/*.txt"))
    if not files: continue
    texts={}
    for f in files:
        raw=open(f,encoding="utf-8").read()
        body=raw.split("\n\n",1)[1] if "\n\n" in raw else raw
        body=body.split("--- IMAGES ---")[0]
        imgs=raw.split("--- IMAGES ---")[1].split("--- LINKS ---")[0].strip() if "--- IMAGES ---" in raw else ""
        lines=[l.strip() for l in body.split("\n") if l.strip()]
        texts[f]=(lines,imgs)
    n=len(texts)
    pagesof=collections.defaultdict(set)
    for f,(lines,_) in texts.items():
        pg=os.path.basename(f)[15:-4]
        for l in set(lines): pagesof[l].add(pg)
    nav={l for l,pgs in pagesof.items() if len(pgs)>=3 and n>=5 and len(l)<90}
    nav|={"Free Web space and hosting from fws1.com","Search the Web","Click Pic for Larger View","Click on Pic for Larger View"}
    # group by page path
    groups=collections.defaultdict(list)
    for f,(lines,imgs) in texts.items():
        ts=os.path.basename(f)[:14]; page=os.path.basename(f)[15:-4]
        keep=[l for l in lines if l not in nav]
        # keep also the title lines (first two lines) even if nav
        head=lines[:2]
        groups[page].append((ts,head,keep,imgs))
    out.write(f"\n\n######################## DOMAIN {d}  ({n} captures)\n")
    out.write("NAV LINES (suppressed below):\n  "+"\n  ".join(sorted(nav))+"\n")
    for page,vers in sorted(groups.items()):
        out.write(f"\n=================== PAGE {page}\n")
        prev=None
        for ts,head,keep,imgs in sorted(vers):
            sig="\n".join(keep)
            if sig==prev:
                out.write(f"--- {ts}: (identical body to previous capture)\n"); continue
            prev=sig
            out.write(f"--- {ts}  title: {head[0] if head else ''}\n")
            out.write(sig+"\n")
            if imgs: out.write("[IMAGES] "+" ; ".join(x.split(" | ")[0] for x in imgs.split("\n"))+"\n")
out.close()
print("wrote bodies_by_page.txt", os.path.getsize("bodies_by_page.txt"))
