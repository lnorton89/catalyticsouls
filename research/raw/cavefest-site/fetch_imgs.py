import json, os, re, sys, time, urllib.request, random
want = ["cavestock08_373x500.gif","summer_cavefest_08_250x167.jpg","halloween3_386x500.jpg","flier_391x500.jpg","flier_blooze_gas_376x500.jpg","flier_blooze_gas_front_500x372.jpg","4x6front7_7_7web_340x500.jpg","cavestock34x6back_170x250.jpg","cavestock34x6front_102x150.jpg","cavemanbob_180x135.jpg","cavewomanlou_216x162.jpg","8pt5x11_bnw_1up_300dpi_cave_flyer_193x250.jpg","cornmeal_250x187.jpg","staff_250x187.jpg","cavefestsky_250x166.jpg","cave2.jpg","thecaveroad.jpg","people_333x500.jpg","theaudience_250x187.jpg","3guyssound_250x187.jpg",
        "DSC00279.JPG","DSC00281.JPG","DSC00285.JPG","index.2.jpg","wpe5.jpg","main.jpg","back.jpg","logo.png"]
rows=[]
for d in ["cavefest.fws1.com","shawneecave.com","cavefest.com","cavemanexperience.com"]:
    rows += json.load(open(f"../cdx/{d}.json"))[1:]
def fetch(url, tries=10):
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 research-scraper"})
            with urllib.request.urlopen(req,timeout=120) as r: return r.read()
        except Exception as e:
            if getattr(e,"code",None)==404: return None
            time.sleep(3*(i+1)+random.random()*2)
    return None
for ts,orig,mt,st,dg,ln in rows:
    fn=orig.rsplit("/",1)[-1]
    if fn in want and not mt.startswith("text"):
        out=fn if not os.path.exists(fn) else ts+"_"+fn
        if os.path.exists(out): continue
        data=fetch(f"https://web.archive.org/web/{ts}id_/{orig}")
        print("OK" if data else "MISS", ts, orig, len(data) if data else 0); sys.stdout.flush()
        if data: open(out,"wb").write(data)
        time.sleep(1.5)
