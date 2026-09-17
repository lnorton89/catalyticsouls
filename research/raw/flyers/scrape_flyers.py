import urllib.request, json, os, time, re, hashlib
UA={'User-Agent':'Mozilla/5.0 (research)'}
OUT='research/raw/flyers'
def get(u,binary=False):
    r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=90)
    return r.read() if binary else r.read().decode('utf8','ignore')
def cdx(pattern):
    for attempt in range(40):
        try:
            t=get(f"https://web.archive.org/cdx/search/cdx?url={pattern}&output=json&filter=statuscode:200&filter=mimetype:image/.*&collapse=digest&limit=2000")
            if 'Temporarily Offline' in t: raise Exception('offline')
            rows=json.loads(t) if t.strip() else []
            return rows[1:] if rows else []
        except Exception as e:
            time.sleep(60)
    return []
patterns=[
 'catalyticsouls.com/flyers*','catalyticsouls.com/images*','catalyticsouls.com/img*','catalyticsouls.com/*.jpg','catalyticsouls.com/*.gif','catalyticsouls.com/*.png',
 'catalyticsouls.com/ugs/*','catalyticsouls.com/forums/files*','catalyticsouls.com/forums/images*',
 'cavefest.fws1.com/*','shawneecave.com/*','campzoe.com/*underground*','campzoe.com/images/*ugs*','campzoe.com/images/*underground*',
 'myspace.com/catalyticsouls*','theuntz.com/*underground-sound*',
]
log=open(f'{OUT}/scrape_log.txt','a',encoding='utf8')
index=[]
for p in patterns:
    rows=cdx(p)
    log.write(f"{p}: {len(rows)} image captures\n"); log.flush()
    for row in rows:
        urlkey,ts,orig,mime,status,digest,length=row[:7]
        try: length=int(length)
        except: length=0
        if length<15000: continue   # skip icons/buttons/thumbnails
        name=re.sub(r'[^A-Za-z0-9._-]+','_',orig.split('://',1)[-1])[-90:]
        fn=f"{OUT}/{ts}_{name}"
        if not os.path.splitext(fn)[1]: fn+='.'+mime.split('/')[-1]
        if os.path.exists(fn): continue
        for attempt in range(6):
            try:
                data=get(f"https://web.archive.org/web/{ts}id_/{orig}",binary=True)
                if data[:6] in (b'<html>',b'<!DOCT') or len(data)<5000: raise Exception('placeholder')
                open(fn,'wb').write(data)
                index.append((ts,orig,mime,len(data),fn))
                log.write(f"OK {ts} {orig} {len(data)}\n"); log.flush()
                break
            except Exception as e:
                log.write(f"retry{attempt} {orig} {e}\n"); log.flush(); time.sleep(20)
        time.sleep(1.5)
json.dump(index,open(f'{OUT}/index.json','w'),indent=1)
log.write("DONE\n"); log.close()
print("done",len(index))
