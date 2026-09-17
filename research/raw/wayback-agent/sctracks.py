import re,json
t=open('sc.html',encoding='utf-8',errors='ignore').read()
m=re.search(r'window\.__sc_hydration\s*=\s*(\[.*?\]);</script>',t,re.S)
if m:
    data=json.loads(m.group(1))
    for item in data:
        if item.get('hydratable')=='user':
            u=item['data']; print({k:u.get(k) for k in ['username','full_name','city','country_code','followers_count','track_count','created_at','last_modified','description']})
        if item.get('hydratable') in ('playlist','sound','tracks'):
            print(item.get('hydratable'), str(item['data'])[:300])
else: print('no hydration')
