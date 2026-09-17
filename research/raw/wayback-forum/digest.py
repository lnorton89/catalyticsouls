import re, sys, glob, os, json
import parse_thread as pt
SPAM=re.compile(r'ringtone|tramadol|viagra|xanax|alprazolam|mortgage|halloween (wallpaper|costume)|spyder|velvet blazer|nike blazer|home office furniture|shakiranude|theaaliyah|akira fubuki|online poker|casino|Airline Tickets Barcelona|phentermine|cialis|levitra|hydrocodone|\.info/movies|debt consolidation|p0rn|ambien|valium|carisoprodol|lipitor|zoloft|adipex|lesbian|hentai|yespica|titmuss|Health Insurance$',re.I)
SIG=re.compile(r'^(_{5,}|nu mix:|USAmnesia Dates:|Thursdays at The Skyy Box|0\d/\d\d/(20)?06 - |CAVEFEST .06 420 edition|UnderGround Sound Back 2 the Freak!|http://catalyticsouls\.com/forums/viewtopic\.php\?t=234|www\.catalyticsouls\.com|http://www\.myspace\.com/djtomfoolery|http://catalyticsouls\.com/music/tomfooleryresolution|"I give up, who are you\?"|"I\'m the Antichrist|:: 609:U Lounge|K_I_T :: ragga jungle|Upcoming gigs?:|18 June 2006 : Party|1 July 2006 : Midwest|Cavefest 3 :: Saturday|"Fulfilling the wishes|Religion Is the Root|-Jon Hamilton|"Didnt you know\? The world|DJ DERVE$|MD n Herrer speed garage|http://www\.demostreams\.com/\?ID=DJMD|yesterday will never end\.|GET TO JAMMIN!|ilevel inc\.|Catalt?y?ticsouls Prod\.|hhead Records|Joined: |Posts: \d+|Location: |Site Admin\]?$|New Catalyst\]?$|Evolving\]?$|nuclear\]?$|Guest\]$|\[Guest|\[New Catalyst|\[Evolving|\[nuclear|\[Site Admin)',re.I)
def is_spam(p):
    b=p['body']; u=p['user']; words=b.split()
    if SPAM.search(b) and not re.search(r'cave|ugs|underground|stock|tom',b,re.I): return True
    if len(words)>40 and len(set(w.lower() for w in words))/len(words)<0.35: return True
    if re.match(r'^(Ence|Moted|Pojo|Mopo|Hatard|Sterjob|Hadick|Terhab|Motard)',u): return True
    if re.match(r'^[A-Za-z]{8,12}$',u) and re.search(r'[a-z][A-Z]',u) and re.search(r'[A-Z].*[A-Z].*[A-Z]',u): return True
    if b.count('href=')>=2 or (b.count('http')>=6 and len(words)<200): return True
    if re.search(r'^(wow|cool|nice|good|thanks?|good news|respond)\W*$',b.strip().split('\n')[0],re.I) and re.search(r'http|\.(info|org|com)|Insurance|Tickets Barcelona',b): return True
    return False
cdx={}
for line in open('cdx/forum-captures.txt',encoding='utf8'):
    p=line.split()
    if len(p)>=3: cdx[p[1]]=p[2]
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
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    os.makedirs('digest',exist_ok=True)
    done=set(l.strip() for l in open('read_done.txt',encoding='utf8')) if os.path.exists('read_done.txt') else set()
    maxchars=int(sys.argv[1]) if len(sys.argv)>1 else 3000
    newly=[]
    seenf='seen_content.txt'
    seen=set(l.strip() for l in open(seenf,encoding='utf8')) if os.path.exists(seenf) else set()
    for f in sorted(glob.glob('threads_html/*.html')):
        b=os.path.basename(f)[:-5]
        if not os.path.exists('digest/'+b+'.md'):
            open('digest/'+b+'.md','w',encoding='utf8').write(digest_file(f))
        if b not in done:
            out=open('digest/'+b+'.md',encoding='utf8').read()
            m=re.search(r'\| t=(\d*) \|',out); m2=re.search(r'^-- #(\d+) ',out,re.M)
            key=f"{m.group(1) if m else ''}:{m2.group(1) if m2 else ''}:{out.count(chr(10))}"
            if key in seen or (m2 is None):
                newly.append(b); continue
            seen.add(key); open(seenf,'a',encoding='utf8').write(key+'
')
            print(out[:maxchars]+(' [TRUNC]\n' if len(out)>maxchars else ''))
            newly.append(b)
    with open('read_done.txt','a',encoding='utf8') as fh:
        for b in newly: fh.write(b+'\n')
    print('### printed',len(newly),'new digests')
