import json,urllib.request,re,html
UA={'User-Agent':'Mozilla/5.0 (research; catalyticsouls wiki)'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read().decode('utf8','ignore')
# reddit search
for q in ['Shawnee cave Underground Sound','Underground Sound 4 Murphysboro','cave rave Illinois Murphysboro']:
    try:
        d=json.loads(get('https://www.reddit.com/search.json?q='+urllib.parse.quote(q)+'&limit=10&sort=relevance'))
        for c in d['data']['children']:
            p=c['data']; print('REDDIT|',p['subreddit'],'|',p['title'],'|',p['created_utc'],'|https://www.reddit.com'+p['permalink'])
    except Exception as e: print('reddit err',q,e)
# youtube search
try:
    s=get('https://www.youtube.com/results?search_query=Underground+Sound+Shawnee+Cave')
    ids=re.findall(r'"videoId":"([A-Za-z0-9_-]{11})".{0,400}?"title":\{"runs":\[\{"text":"([^"]+)"',s)
    seen=set()
    for vid,t in ids:
        if vid in seen: continue
        seen.add(vid); print('YT|',vid,'|',t)
except Exception as e: print('yt err',e)
# zcarab discogs
d=json.loads(get('https://api.discogs.com/artists/3537925/releases?per_page=50'))
for r in d.get('releases',[]): print('ZCARAB|',r.get('year'),'|',r.get('artist'),'|',r.get('title'),'|',r.get('label'),'|',r.get('role'))
