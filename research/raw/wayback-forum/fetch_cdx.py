import urllib.request, urllib.parse, json, time, sys, os
queries = {
 "forums": "catalyticsouls.com/forums/*",
 "viewtopic_root": "catalyticsouls.com/viewtopic*",
 "viewforum_root": "catalyticsouls.com/viewforum*",
 "forum_php_root": "catalyticsouls.com/forum.php*",
 "phpbb": "catalyticsouls.com/phpBB*",
 "forum_dir": "catalyticsouls.com/forum/*",
 "www_forums": "www.catalyticsouls.com/forums/*",
}
def get(url, tries=8):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 research-scraper"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:
            print("  retry", i, e, file=sys.stderr)
            time.sleep(5*(i+1))
    return None
for name, u in queries.items():
    out = f"cdx/{name}.json"
    if os.path.exists(out): continue
    url = ("http://web.archive.org/cdx/search/cdx?url=" + urllib.parse.quote(u, safe='') +
           "&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=digest&limit=20000")
    print(name, url)
    data = get(url)
    if data is None:
        print("FAILED", name); continue
    open(out, "wb").write(data)
    try:
        rows = json.loads(data)
        print("  rows:", len(rows)-1)
    except Exception as e:
        print("  not json:", data[:200])
    time.sleep(2)
