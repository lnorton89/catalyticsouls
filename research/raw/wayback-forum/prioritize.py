import re, csv, json
idx={}
for r in csv.DictReader(open('thread-index.csv',encoding='utf8')): idx[(r['root'],r['topic_id'])]=r
tiers=[
 (1, r'underground ?sound|\bugs\b|freak ?fest|back 2 the freak|midwest freak|timeslots|time slots|set times'),
 (1.5, r'stab'),
 (2, r'cave ?fest|cave ?stock|cave ?jam|gamma|cave ?country|cornmeal|solstice|caveman|goodale'),
 (2.5, r'police|sheriff|arrest|cops|bust|media|news|illinoisan|rave|techno|raid|jail|court'),
 (3, r'chicago|true midwest|drama|promoter|experience'),
 (3.5, r'intro|mix|bio|crew|who (is|are)|welcome|hello|new here|hey|pics|photos|review|thank'),
 (3.6, r'zoe|leaving|moving|2008|2009|future|next year'),
]
spam=r'tramadol|viagra|xanax|alprazolam|mortgage|debt|p0rn|porn|loan|casino|poker|pharm|cialis|phentermine|ambien|valium|insurance|my site|titmuss|yespica|tones online|ringtone|lima adriana|mature|depakote|zoloft|levitra|soma\b|hydrocodone|vicodin|adipex|carisoprodol|diazepam|lorazepam|ultram|celebrex|paxil|prozac|lipitor|nexium|propecia|zyban|meridia|ionamin|texas hold|blackjack|slots|roulette|credit|refinanc|cheap|buy |free |online|\.com|http|sex|nude|naked|teen|lesbian|gay|anal|fuck|hentai|incest|rape|escort|dating|pills|drug|hcl|rx\b|pharmacy'
rows=[]
for line in open('cdx/forum-captures.txt',encoding='utf8'):
    p=line.split()
    if len(p)<3 or 'viewtopic' not in p[2]: continue
    ts,o=p[1],p[2]
    root='forums' if '/forums/' in o else '2005root'
    tm=re.search(r'[?&]t=(\d+)',o); tid=tm.group(1) if tm else ''
    sm=re.search(r'[?&]start=(\d+)',o); start=sm.group(1) if sm else '0'
    r=idx.get((root,tid),{})
    title=r.get('title',''); forum=r.get('forum',''); author=r.get('author','')
    score=7 if tid else (4.5 if root=='2005root' else 8)
    for t,pat in tiers:
        if re.search(pat,title+' '+forum,re.I): score=min(score,t)
    if author.lower()=='tomfoolery': score=min(score,3.2)
    if tid and re.search(spam,title,re.I) and not re.search(r'cave|ugs|underground|stock',title,re.I): score=9.5
    rows.append(dict(score=score,ts=ts,o=o,root=root,tid=tid,start=start,title=title,forum=forum,author=author))
# duplicates: same root/tid/start -> newest first, older ones +10
seen={}
for r in sorted(rows,key=lambda r:r['ts'],reverse=True):
    if r['tid']:
        k=(r['root'],r['tid'],r['start'])
        if k in seen: r['score']+=10
        else: seen[k]=r['ts']
rows.sort(key=lambda r:(r['score'],int(r['tid'] or 0),r['ts']))
with open('fetch-order.tsv','w',encoding='utf8') as fh:
    for r in rows: fh.write('\t'.join(str(r[k]) for k in ['score','ts','o','tid','title','forum','author'])+'\n')
from collections import Counter
print(len(rows), sorted(Counter(r['score'] for r in rows).items()))
print('unmatched titles:', sum(1 for r in rows if not r['title']), 'unique t/start keys', len(seen))
