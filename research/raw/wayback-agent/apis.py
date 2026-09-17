import json,urllib.request,re,sys
def get(u):
    r=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0) Chrome/120'})
    return urllib.request.urlopen(r,timeout=40).read().decode('utf-8','ignore')
for term in ['tomfoolery','tom+foolery','zcarab','catalyticsouls','catalytic+souls']:
    print('=== iTunes',term)
    try:
        d=json.loads(get('https://itunes.apple.com/search?term=%s&entity=song&limit=200'%term))
        seen=set()
        for r in d['results']:
            blob=(r.get('artistName','')+' '+r.get('collectionName','')+' '+(r.get('copyright') or '')).lower()
            if not any(k in blob for k in ['foolery','zcarab','catalytic','bay area rec']): continue
            k=(r.get('collectionName'),r.get('releaseDate','')[:10])
            if k in seen: continue
            seen.add(k); print(r.get('releaseDate','')[:10],'|',r.get('artistName'),'|',r.get('collectionName'),'|',r.get('primaryGenreName'),'|',(r.get('copyright') or '')[:70],'| artistId',r.get('artistId'))
    except Exception as e: print('ERR',e)
for q in ['tomfoolery','catalytic souls','zcarab']:
    print('=== Mixcloud users',q)
    try:
        d=json.loads(get('https://api.mixcloud.com/search/?q=%s&type=user'%q.replace(' ','%20')))
        for r in d.get('data',[])[:8]: print(r.get('username'),'|',r.get('name'),'|',r.get('city'),r.get('country'),'|',r.get('url'))
    except Exception as e: print('ERR',e)
print('=== Mixcloud djtomfoolery cloudcasts')
try:
    d=json.loads(get('https://api.mixcloud.com/djtomfoolery/cloudcasts/'))
    for r in d.get('data',[]): print(r.get('created_time','')[:10],'|',r.get('name'),'|',r.get('play_count'),'plays |',[t['name'] for t in r.get('tags',[])])
    u=json.loads(get('https://api.mixcloud.com/djtomfoolery/')); print({k:u.get(k) for k in ['name','city','country','biog','follower_count','created_time','updated_time']})
except Exception as e: print('ERR',e)
print('=== SoundCloud hydration')
t=open('sc.html',encoding='utf-8',errors='ignore').read()
for k in ['followers_count','track_count','playlist_count','city','country_code','description','last_modified','created_at','full_name','permalink_url']:
    m=re.search(r'"%s":("(?:[^"\]|\.)*"|\d+|null)'%k,t); print(k,':',(m.group(1)[:500] if m else None))
