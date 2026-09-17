import json,urllib.request,re,time
UA={'User-Agent':'Mozilla/5.0'}
ids="nnqnKg7K0AE NMQOhb7AhHg 0eeV-3nuevA IPmu1hxilnI 2-vmgyxuaio BUwxzD_pASk r_7j_IPPFlE d5LuKtTaHfE tPRSF7FKhDI OhwNCc8faYM wMFP-mPD4i0 mov4fp6Vops vI7jPz7uiYw YBSYkn6KAGY ECtKBXli2Bw".split()
out=[]
for v in ids:
    try:
        s=urllib.request.urlopen(urllib.request.Request(f'https://www.youtube.com/watch?v={v}',headers=UA),timeout=60).read().decode('utf8','ignore')
        def g(k):
            i=s.find(k)
            if i<0: return ''
            j=s.find('"',i+len(k)); return s[i+len(k):j]
        title=g('"title":"'); desc=g('"shortDescription":"'); views=g('"viewCount":"'); date=g('"publishDate":"'); ch=g('"ownerChannelName":"')
        desc=desc.encode('utf8').decode('unicode_escape',errors='ignore')
        rec=f"{v} | {title} | {ch} | {date[:10]} | {views} views\n  desc: {desc[:700]}"
        out.append(rec); print(rec); time.sleep(1)
    except Exception as e: print(v,'ERR',e)
open('youtube/ugs-videos.txt','w',encoding='utf8').write('\n'.join(out))
