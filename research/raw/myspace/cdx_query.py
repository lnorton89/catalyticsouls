import json, time, sys, urllib.request, urllib.parse, os
names = ["catalyticsouls","djtomfoolery","djandyb","unklryan","unklryanmusic","briandervish","briandervishmusicpage","djderve","reperkushin","daveskeezy","brainstormdj","midwestdrumbassalliance","benjiramsey"]
hosts = ["myspace.com","www.myspace.com","profile.myspace.com","blog.myspace.com","blogs.myspace.com","music.myspace.com"]
def fetch(url, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (research scraper; polite)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8","replace")
        except Exception as e:
            code = getattr(e, "code", None)
            print(f"  err {code or e} try {i+1}", file=sys.stderr)
            time.sleep(3 * (i+1))
    return None
results = {}
for n in names:
    results[n] = []
    for h in hosts:
        u = f"http://web.archive.org/cdx/search/cdx?url={h}/{n}*&output=json&filter=statuscode:200&collapse=digest&limit=500&from=2005&to=2013"
        txt = fetch(u)
        time.sleep(1.5)
        if txt is None:
            print(f"{n} {h}: FAILED"); continue
        txt = txt.strip()
        if not txt:
            print(f"{n} {h}: 0"); continue
        try:
            rows = json.loads(txt)
        except Exception:
            print(f"{n} {h}: parse fail {txt[:100]}"); continue
        if rows: rows = rows[1:]
        print(f"{n} {h}: {len(rows)}")
        for r in rows:
            results[n].append({"host":h,"ts":r[1],"url":r[2],"mime":r[3],"status":r[4],"digest":r[5],"len":r[6]})
    with open(f"cdx/{n}.json","w",encoding="utf-8") as f:
        json.dump(results[n], f, indent=1)
json.dump(results, open("cdx/all_crew.json","w"), indent=1)
