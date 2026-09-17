import re, sys, glob, os, json
import parse_thread as pt
SPAM=re.compile(r'ringtone|tramadol|viagra|xanax|alprazolam|mortgage|halloween (wallpaper|costume)|spyder|velvet blazer|nike blazer|home office furniture|shakiranude|theaaliyah|akira fubuki|online poker|casino|Airline Tickets Barcelona|phentermine|cialis|levitra|hydrocodone|\.info/movies|debt consolidation|p0rn|ambien|valium|carisoprodol|lipitor|zoloft|adipex|lesbian|hentai',re.I)
SIG=re.compile(r'^(_{5,}|nu mix:|USAmnesia Dates:|Thursdays at The Skyy Box|0\d/\d\d/(20)?06 - |CAVEFEST .06 420 edition|UnderGround Sound Back 2 the Freak!|http://catalyticsouls\.com/forums/viewtopic\.php\?t=234|www\.catalyticsouls\.com|http://www\.myspace\.com/djtomfoolery|http://catalyticsouls\.com/music/tomfooleryresolution|"I give up, who are you\?"|"I\'m the Antichrist|:: 609:U Lounge|K_I_T :: ragga jungle|Upcoming gigs?:|18 June 2006 : Party|1 July 2006 : Midwest|Cavefest 3 :: Saturday|"Fulfilling the wishes|Religion Is the Root|-Jon Hamilton|"Didnt you know\? The world|DJ DERVE$|MD n Herrer speed garage|http://www\.demostreams\.com/\?ID=DJMD|yesterday will never end\.|Joined: |Posts: \d+|Location: |Site Admin\]?$|New Catalyst\]?$|Evolving\]?$|nuclear\]?$|Guest\]$|\[Guest|\[New Catalyst|\[Evolving|\[nuclear|\[Site Admin)',re.I)
def is_spam(p):
    b=p['body']
    if SPAM.search(b) and not re.search(r'cave|ugs|underground|stock|tom',b,re.I): return True
    words=b.split()
    if len(words)>40 and len(set(w.lower() for w in words))/len(words)<0.35: return True
    if re.match(r'^(Ence|Moted|Pojo|Mopo|Hatard|Sterjob|Hadick)',p['user']): return True
    return False
def digest_file(f, maxlen=900):
    name=os.path.basename(f)[:-5]; ts=name.rsplit('_',1)[1]
    d=pt.parse(open(f,encoding='utf8').read())
    L=[f"##### {name} | t={d['topic_id']} | {d['forum']} | {d['title']} | pages: {d['pages']}"]
    L.append(f"wayback: http://web.archive.org/web/{ts}/{cdx.get(ts,'')}")
    n=0
    for p in d['posts']:
        if is_spam(p): continue
        n+=1
        body='\n'.join(l for l in p['body'].split('\n') if l.strip() and not SIG.match(l.strip()))
        if len(body)>maxlen: body=body[:maxlen]+' [...]'
        L.append(f"-- #{p['post_id']} {p['user']} | {p['date']}" + (f" | {p['subject']}" if p['subject'] and p['subject']!=d['title'] else ''))
        L.append(body)
    L.insert(2,f"(non-spam posts: {n} of {len(d['posts'])})")
    return '\n'.join(L)+'\n'
cdx={}
for line in open('cdx/forum-captures.txt',encoding='utf8'):
    p=line.split()
    if len(p)>=3: cdx[p[1]]=p[2]
if __name__=='__main__':
    pats=sys.argv[1:] or ['*']
    os.makedirs('digest',exist_ok=True)
    for pat in pats:
        for f in sorted(glob.glob(f'threads_html/{pat}.html')):
            out=digest_file(f)
            open('digest/'+os.path.basename(f)[:-5]+'.md','w',encoding='utf8').write(out)
            print(out)
