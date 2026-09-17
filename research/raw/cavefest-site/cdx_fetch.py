import sys, json, time, urllib.request, urllib.parse, os
domains = ["cavefest.fws1.com","shawneecave.com","cavefest.com","shawneesaltpetrecave.com","saltpetrecave.com","shawneecaveamphitheater.com",
           "intergruv.com","intergruvnetwork.com","middleschoolproductions.com","geniusoffun.com","cavemanexperience.com","campzoe.com"]
def fetch(url, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 research-scraper"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read().decode("utf-8","replace")
        except Exception as e:
            code = getattr(e,"code",None)
            print(f"  retry {i} {url[:80]} -> {e}", file=sys.stderr)
            time.sleep(4*(i+1))
    return None
for d in domains:
    out = f"cdx/{d}.json"
    if os.path.exists(out) and os.path.getsize(out)>2:
        print(d,"exists"); continue
    q = urllib.parse.urlencode({"url":d,"matchType":"prefix","filter":"statuscode:200","collapse":"digest","fl":"timestamp,original,mimetype,statuscode,digest,length"})
    txt = fetch("https://web.archive.org/web/timemap/json?"+q)
    if txt is None:
        print(d,"FAILED"); continue
    open(out,"w",encoding="utf-8").write(txt)
    try:
        rows = json.loads(txt) if txt.strip() else []
    except Exception:
        rows=[]
    print(d, len(rows)-1 if rows else 0, "rows")
    time.sleep(2)
