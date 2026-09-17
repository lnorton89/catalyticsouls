import re, html, sys, os, json
def strip(path):
    s=open(path,encoding="utf-8",errors="replace").read()
    fids=sorted(set(re.findall(r'friendi?d=(\d+)',s,re.I)))
    links=re.findall(r'href="(https?://[^"]*myspace\.com[^"]*)"',s,re.I)
    prof=[re.sub(r'^https?://web\.archive\.org/web/\d+(?:id_)?/','',l) for l in dict.fromkeys(links)]
    prof=[l for l in prof if re.search(r'myspace\.com/[A-Za-z0-9_.\-]+/?$',l) or 'viewprofile' in l.lower()]
    txt=re.sub(r'<script.*?</script>',' ',s,flags=re.S|re.I); txt=re.sub(r'<style.*?</style>',' ',txt,flags=re.S|re.I)
    txt=re.sub(r'<!--.*?-->',' ',txt,flags=re.S)
    txt=re.sub(r'<br\s*/?>|</p>|</div>|</td>|</tr>|</li>|</h\d>|</span>','\n',txt,flags=re.I); txt=re.sub(r'<[^>]+>',' ',txt); txt=html.unescape(txt)
    lines=[re.sub(r'\s+',' ',l).strip() for l in txt.split("\n")]; lines=[l for l in lines if l]
    base=os.path.splitext(os.path.basename(path))[0]
    out="text/"+base+".txt"
    with open(out,"w",encoding="utf-8") as f:
        f.write("FRIENDIDS: "+", ".join(fids)+"\n")
        f.write("PROFILE_LINKS:\n"+"\n".join("  "+l for l in prof)+"\n\n=== TEXT ===\n")
        f.write("\n".join(lines))
    return out, fids, prof, lines
if __name__=="__main__":
    for p in sys.argv[1:]:
        out,fids,prof,lines=strip(p)
        print("#####",p,"->",out,len(lines),"lines; friendids",fids)
        print("PROFILE_LINKS:",prof)
        print("\n".join(lines))
