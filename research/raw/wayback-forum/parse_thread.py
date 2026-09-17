import re, html, os, glob, sys, json
def txt(s):
    s=re.sub(r'(?is)<(script|style).*?</\1>','',s)
    s=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</tr>|</li>|</h\d>','\n',s)
    s=re.sub(r'<img[^>]*alt="([^"]*)"[^>]*>',r' \1 ',s)
    s=re.sub(r'<[^>]+>',' ',s); s=html.unescape(s).replace('\xa0',' ')
    s=re.sub(r'[ \t\r\f\v]+',' ',s); s=re.sub(r'\n\s*\n+','\n',s)
    return s.strip()
def parse(h):
    out={}
    m=re.search(r'<title>(.*?)</title>',h,re.S); out['page_title']=txt(m.group(1)) if m else ''
    m=re.search(r'<a class="maintitle" href="viewtopic\.php\?t=(\d+)[^"]*">(.*?)</a>',h,re.S)
    out['topic_id']=m.group(1) if m else ''; out['title']=txt(m.group(2)) if m else out['page_title'].split('::')[-1].strip()
    crumbs=re.findall(r'<a href="viewforum\.php\?f=(\d+)" class="nav">(.*?)</a>',h,re.S)
    out['forum_id']=crumbs[-1][0] if crumbs else ''; out['forum']=txt(crumbs[-1][1]) if crumbs else ''
    pg=re.search(r'Goto page(.*?)</span>',h,re.S); out['pages']=txt(pg.group(1)) if pg else ''
    posts=[]
    pat=re.compile(r'<span class="name"><a name="(\d+)"></a><b>(.*?)</b></span>(.*?)(?=<span class="name"><a name="\d+"></a>|$)',re.S)
    for pm in pat.finditer(h):
        pid,user,rest=pm.group(1),txt(pm.group(2)),pm.group(3)
        det=re.search(r'<span class="postdetails">(.*?)</span>',rest,re.S)
        details=txt(det.group(1)) if det else ''
        dm=re.search(r'Posted: (.*?)(?:&nbsp;|<)',rest,re.S)
        sm=re.search(r'Post subject: (.*?)</span>',rest,re.S)
        body=''
        bi=rest.find('<span class="postbody">')
        if bi>=0:
            seg=rest[bi:]
            cut=seg.find('<a href="#top"')
            if cut>0: seg=seg[:cut]
            seg=seg.replace('<td class="quote">',' [quote] ')
            seg=re.sub(r'<span class="genmed"><b>(.*?)</b></span>',lambda mm:'\n>> '+mm.group(1)+' ',seg)
            body=txt(seg)
            body=re.sub(r'\s*Back to top\s*$','',body).strip()
        posts.append(dict(post_id=pid,user=user,details=details,date=txt(dm.group(1)) if dm else '',subject=txt(sm.group(1)) if sm else '',body=body))
    out['posts']=posts
    return out
def render(d, ts, orig):
    L=[f"# {d['title']}", f"forum: {d['forum']} (f={d['forum_id']})  topic_id: {d['topic_id']}  pages: {d['pages']}",
       f"capture: {ts}  wayback: https://web.archive.org/web/{ts}/{orig}", f"posts on this page: {len(d['posts'])}", ""]
    for p in d['posts']:
        L.append(f"--- post #{p['post_id']} | {p['user']} | {p['date']} | subj: {p['subject']}")
        if p['details']: L.append(f"    [{p['details']}]")
        L.append(p['body']); L.append("")
    return '\n'.join(L)
if __name__=='__main__':
    cdx={}
    for line in open('cdx/forum-captures.txt',encoding='utf8'):
        p=line.split()
        if len(p)>=3: cdx[p[1]]=p[2]
    os.makedirs('threads',exist_ok=True)
    n=0; meta=[]
    for f in sorted(glob.glob('threads_html/*.html')):
        name=os.path.basename(f)[:-5]; ts=name.rsplit('_',1)[1]
        h=open(f,encoding='utf8').read()
        d=parse(h)
        orig=cdx.get(ts,'')
        open(f'threads/{name}.txt','w',encoding='utf8').write(render(d,ts,orig))
        meta.append(dict(file=name,ts=ts,orig=orig,topic_id=d['topic_id'],forum=d['forum'],forum_id=d['forum_id'],title=d['title'],nposts=len(d['posts']),
                         users=sorted(set(p['user'] for p in d['posts'])),first_date=d['posts'][0]['date'] if d['posts'] else '',first_user=d['posts'][0]['user'] if d['posts'] else ''))
        n+=1
    json.dump(meta,open('threads-meta.json','w',encoding='utf8'),indent=1)
    print('rendered',n)
