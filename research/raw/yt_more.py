import urllib.request,re,urllib.parse,time
UA={'User-Agent':'Mozilla/5.0'}
def meta(v):
    s=urllib.request.urlopen(urllib.request.Request(f'https://www.youtube.com/watch?v={v}',headers=UA),timeout=60).read().decode('utf8','ignore')
    def g(k):
        i=s.find(k)
        if i<0: return ''
        j=s.find('"',i+len(k)); return s[i+len(k):j]
    d=g('"shortDescription":"').encode('utf8').decode('unicode_escape',errors='ignore').replace('\n',' / ')
    return f"{v} | {g('\"title\":\"')} | {g('\"ownerChannelName\":\"')} | {g('\"publishDate\":\"')[:10]} | {g('\"viewCount\":\"')} views\n  desc: {d[:500]}"
known=set(l.split(' | ')[0] for l in open('youtube/ugs-videos.txt',encoding='utf8',errors='ignore') if ' | ' in l)
out=[]
for v in ['CCvP5UyUdsE']:
    if v not in known:
        try: r=meta(v); print(r.encode('ascii','replace').decode()); out.append(r)
        except Exception as e: print(v,'ERR',e)
for q in ['Underground Sound 5 camp zoe 2009','Underground Sound 4 shawnee cave 2008','Underground Sound 2 cave 2006 Infected Mushroom','UGS7 freaky tiki hogrock']:
    s=urllib.request.urlopen(urllib.request.Request('https://www.youtube.com/results?search_query='+urllib.parse.quote(q),headers=UA),timeout=60).read().decode('utf8','ignore')
    for vid,t in re.findall(r'"videoId":"([A-Za-z0-9_-]{11})".{0,400}?"title":\{"runs":\[\{"text":"([^"]+)"',s)[:15]:
        tl=t.lower()
        if vid in known or not any(k in tl for k in ['underground sound','ugs','cave','zoe','tiki']): continue
        known.add(vid)
        try: r=meta(vid); print(r.encode('ascii','replace').decode()); out.append(r)
        except Exception as e: print(vid,'ERR',e)
        time.sleep(0.7)
open('youtube/ugs-videos.txt','a',encoding='utf8').write('\n'+'\n'.join(out)+'\n')
