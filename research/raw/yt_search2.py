import urllib.request,re,time,urllib.parse
UA={'User-Agent':'Mozilla/5.0'}
seen=set()
for q in ['Underground Sound 3 Cave Rave 07','Underground Sound Camp Zoe 2009','Underground Sound Camp Zoe 2010 Rabbit in the Moon','Shawnee cave rave Murphysboro','Cavefest Shawnee Saltpetre cave','Underground Sound Hogrock 2011 Freaky Tiki','TomFoolery breaks Catalytic Souls']:
    s=urllib.request.urlopen(urllib.request.Request('https://www.youtube.com/results?search_query='+urllib.parse.quote(q),headers=UA),timeout=60).read().decode('utf8','ignore')
    for vid,t in re.findall(r'"videoId":"([A-Za-z0-9_-]{11})".{0,400}?"title":\{"runs":\[\{"text":"([^"]+)"',s)[:12]:
        if vid in seen: continue
        seen.add(vid)
        tl=t.lower()
        if any(k in tl for k in ['underground sound','cave','ugs','catalytic','tomfoolery','tom foolery','camp zoe','saltpet']):
            print(q,'||',vid,'|',t)
    time.sleep(1)
