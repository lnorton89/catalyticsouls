import re, glob, html, csv, os, json
from collections import OrderedDict
import fetcher
def txt(s): return html.unescape(re.sub(r'<[^>]+>',' ',s)).replace('\xa0',' ').strip()
def norm(s): return re.sub(r'\s+',' ',s)
threads=OrderedDict()   # key (root,tid) -> dict
index_stats=[]
forum_names={}
for f in sorted(glob.glob('forums_html/*.html')):
    h=open(f,encoding='utf8').read()
    ts=re.search(r'_(\d{14})\.html$',f).group(1)
    root='2005root' if ('forums_' not in os.path.basename(f) and 'forums/' not in f) else 'forums'
    m=re.search(r'<title>(.*?)</title>',h,re.S)
    title=norm(txt(m.group(1))) if m else ''
    fid=re.search(r'f=(\d+)',f); fid=fid.group(1) if fid else ''
    if 'View Forum' in title or 'viewforum' in f:
        fname=title.split('View Forum -')[-1].strip() if 'View Forum' in title else ''
        # phpBB2 subSilver topic rows
        rows=re.findall(r'<a href="viewtopic\.php\?t=(\d+)[^"]*" class="topictitle">(.*?)</a>(.*?)</tr>',h,re.S)
        # fall back: some rows contain the topic-type prefix
        for tid,ttl,rest in rows:
            reps=re.findall(r'<span class="postdetails">(.*?)</span>',rest,re.S)
            auth=re.search(r'<span class="name">(.*?)</span>',rest,re.S)
            replies=txt(reps[0]) if len(reps)>0 else ''
            views=txt(reps[1]) if len(reps)>1 else ''
            last=norm(txt(reps[2])) if len(reps)>2 else ''
            lastdate=''; lastby=''
            if len(reps)>2:
                lm=re.match(r'(.*?)<br\s*/?>(.*)',reps[2],re.S)
                if lm: lastdate=norm(txt(lm.group(1))); lastby=norm(txt(lm.group(2)))
                else: lastdate=last
            # prefix like "Announcement:" / "Sticky:" sits right before the link
            pre=''
            pm=re.search(r'<b>(Announcement|Sticky):</b>\s*<a href="viewtopic\.php\?t='+tid,h)
            if pm: pre=pm.group(1)
            pages=re.search(r'<a href="viewtopic\.php\?t='+tid+r'[^"]*" class="topictitle">.*?</a>(.*?)</td>',h,re.S)
            key=(root,tid)
            d=dict(root=root,forum_id=fid,forum=fname,topic_id=tid,title=norm(txt(ttl)),type=pre,author=norm(txt(auth.group(1))) if auth else '',
                   replies=replies,views=views,last_post=lastdate,last_by=lastby,capture=ts,src=os.path.basename(f))
            if key not in threads or ts>threads[key]['capture']:
                threads[key]=d
        if fname and fid: forum_names[(root,fid)]=fname
    else:
        # forum index / forum.php: capture forum list and stats
        stats={}
        for k,pat in [('total_posts',r'posted a total of <b>(\d+)</b>'),('users',r'We have <b>(\d+)</b> registered users'),
                      ('newest',r'newest registered user is <b>.*?>(.*?)</a>'),('max_online',r'Most users ever online was <b>(\d+)</b> on (.*?)<')]:
            mm=re.search(pat,h,re.S)
            if mm: stats[k]=' '.join(x for x in mm.groups()) if mm.lastindex>1 else mm.group(1)
        forums=re.findall(r'<a href="viewforum\.php\?f=(\d+)" class="forumlink">(.*?)</a>.*?</tr>',h,re.S)
        flist=[]
        for fid2,nm in forums:
            blk=re.search(r'<a href="viewforum\.php\?f='+fid2+r'" class="forumlink">.*?</a>(.*?)</tr>',h,re.S).group(1)
            nums=re.findall(r'<span class="gensmall">(\d+)</span>',blk)
            desc=re.search(r'<br\s*/?>\s*<span class="genmed">(.*?)</span>',blk,re.S)
            flist.append(dict(id=fid2,name=norm(txt(nm)),desc=norm(txt(desc.group(1))) if desc else '',topics=nums[0] if nums else '',posts=nums[1] if len(nums)>1 else ''))
            forum_names.setdefault((root,fid2),norm(txt(nm)))
        cats=[norm(txt(c)) for c in re.findall(r'class="cattitle">(.*?)</a>',h,re.S)]
        index_stats.append(dict(file=os.path.basename(f),capture=ts,root=root,title=title,stats=stats,categories=cats,forums=flist))
# fill forum names where missing
for k,d in threads.items():
    if not d['forum']: d['forum']=forum_names.get((d['root'],d['forum_id']),'')
rows=sorted(threads.values(), key=lambda d:(d['root'],int(d['forum_id'] or 0),int(d['topic_id'])))
with open('thread-index.csv','w',newline='',encoding='utf8') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(r) for r in rows]
with open('forum-index-stats.json','w',encoding='utf8') as fh: json.dump(index_stats,fh,indent=1)
print('threads',len(rows),'index pages',len(index_stats))
from collections import Counter
print(Counter((r['root'],r['forum']) for r in rows).most_common())
print(rows[0]); print(rows[-1])
