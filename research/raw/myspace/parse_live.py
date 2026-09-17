import re, html, json, glob, os
out = []
for f in sorted(glob.glob("live/*.html")):
    s = open(f, encoding="utf-8", errors="replace").read()
    if "404" in os.path.basename(f) or len(s) < 90000 and "Page not found" in s: pass
    rec = {"file": f}
    m = re.search(r"<title>(.*?)</title>", s, re.S); rec["title"] = html.unescape(m.group(1).strip()) if m else None
    for tag in ["description","og:title","og:description","og:image","og:url","keywords"]:
        m = re.search(r'<meta\s+(?:name|property)="%s"\s+content="(.*?)"' % re.escape(tag), s, re.S)
        if m: rec[tag] = html.unescape(m.group(1))[:500]
    # profile data
    m = re.search(r'"profileId"\s*:\s*"?(\d+)', s); rec["profileId"] = m.group(1) if m else None
    for key in ["fullName","displayName","location","userName","profileUrl","isVerified","createdDate","joinedDate","memberSince","profileType","bio","biography","aboutMe","gender","age","birthdate","city","state","country","website"]:
        m = re.search(r'"%s"\s*:\s*("[^"]*"|\d+|null|true|false)' % key, s)
        if m: rec[key] = json.loads(m.group(1)) if m.group(1)!="null" else None
    # connection counts
    for key in ["totalConnectionsOut","totalConnectionsIn","outConnections","inConnections","connectionsOut","connectionsIn","friendCount","totalFriends"]:
        m = re.search(r'"%s"\s*:\s*(\d+)' % key, s)
        if m: rec[key] = int(m.group(1))
    # counts visible as text
    rec["count_text"] = re.findall(r'(\d[\d,\.]*[KM]?)\s*</span>\s*<span[^>]*>\s*(connections|out|in|photos|mixes|songs|albums|videos|articles|people)', s, re.I)[:20]
    # top friends / connections links (profile links)
    links = re.findall(r'href="(/[a-zA-Z0-9_.\-]+)"[^>]*>', s)
    skip = {"/discover","/search","/signin","/signup","/settings","/help","/messages","/notifications","/about","/privacy","/terms","/blog","/mixes","/photos","/music","/people","/videos","/press","/topics","/home","/friends"}
    uniq = []
    for l in links:
        if l.lower() in skip or l.count("/")>1: continue
        if l not in uniq: uniq.append(l)
    rec["profile_links"] = uniq[:80]
    # data-profile-name / connection cards
    rec["cards"] = re.findall(r'data-(?:username|profile-name|user-name|display-name)="([^"]+)"', s)[:80]
    # jsonld
    rec["jsonld"] = [html.unescape(x)[:1500] for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)]
    # photo / mix titles
    rec["img_alts"] = list(dict.fromkeys(html.unescape(a) for a in re.findall(r'<img[^>]+alt="([^"]{3,120})"', s)))[:80]
    rec["mix_titles"] = list(dict.fromkeys(re.findall(r'"(?:mixTitle|title)"\s*:\s*"([^"]{3,120})"', s)))[:80]
    out.append(rec)
json.dump(out, open("live/parsed_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
for r in out:
    print("=== ", r["file"], "|", r.get("title"))
    for k in ["og:title","description","profileId","fullName","displayName","location","memberSince","createdDate","bio","totalConnectionsOut","totalConnectionsIn","count_text"]:
        if r.get(k) not in (None, [], ""): print("  ", k, ":", str(r[k])[:300])
    print("   links:", r["profile_links"][:60])
    print("   cards:", r["cards"][:40])
    print("   alts:", r["img_alts"][:40])
    print("   mixes:", r["mix_titles"][:30])
