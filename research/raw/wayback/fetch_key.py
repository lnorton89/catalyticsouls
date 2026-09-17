import urllib.request, re, html, time, os, json
UA={'User-Agent':'Mozilla/5.0 (research)'}
def get(url):
    r=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(r,timeout=90) as f: return f.read().decode('utf8','ignore')
def strip(h):
    h=re.sub(r'(?is)<(script|style).*?</\1>','',h)
    h=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</tr>|</li>|</h\d>|</td>','\n',h)
    h=re.sub(r'<[^>]+>',' ',h); h=html.unescape(h)
    h=re.sub(r'[ \t\r\f\v]+',' ',h); h=re.sub(r'\n\s*\n+','\n',h)
    return h.strip()
targets=[
 ("2005-home","20050204034141","http://www.catalyticsouls.com:80/"),
 ("2005-portal0","20050204063004","http://www.catalyticsouls.com:80/portal.php?article=0"),
 ("2005-portal1","20050204064012","http://www.catalyticsouls.com:80/portal.php?article=1"),
 ("2005-portal2","20050204065017","http://www.catalyticsouls.com:80/portal.php?article=2"),
 ("2005-portal3","20050204065718","http://www.catalyticsouls.com:80/portal.php?article=3"),
 ("2005-portal4","20050204070141","http://www.catalyticsouls.com:80/portal.php?article=4"),
 ("2005-ugs","20050522225201","http://catalyticsouls.com:80/undergroundsound/"),
 ("2006-home","20060415124210","http://www.catalyticsouls.com:80/index.php?"),
 ("2006-about","20060522222934","http://www.catalyticsouls.com/index.php?c=1&a=about"),
 ("2006-allevents","20060522222937","http://www.catalyticsouls.com/index.php?c=1&a=view_all_events"),
 ("2006-pastevents","20060522233030","http://www.catalyticsouls.com/index.php?c=1&a=view_past_events"),
 ("2006-event23","20060522222803","http://www.catalyticsouls.com/index.php?c=1&a=show_event&e=23"),
 ("2006-event25","20060522222917","http://www.catalyticsouls.com/index.php?c=1&a=show_event&e=25"),
 ("2006-event26","20061106204454","http://www.catalyticsouls.com/index.php?c=1&a=show_event&e=26"),
 ("2006-forumindex","20060629131723","http://www.catalyticsouls.com:80/forums/index.php"),
 ("2007-artists","20070704121223","http://www.catalyticsouls.com:80/index.php?c=1&a=artists"),
 ("2007-event30","20070704121403","http://www.catalyticsouls.com:80/index.php?c=1&a=show_event&e=30"),
 ("2007-events","20070614013735","http://catalyticsouls.com:80/events.php?"),
 ("2008-home","20080611000825","http://www.catalyticsouls.com:80/index.html"),
 ("2008-about","20080611000759","http://www.catalyticsouls.com:80/about.html"),
 ("2008-artists","20080610075737","http://www.catalyticsouls.com:80/artists.html"),
 ("2008-events","20080611000810","http://www.catalyticsouls.com:80/events.html"),
 ("2008-news","20080611000830","http://www.catalyticsouls.com:80/news.html"),
 ("2008-musicshop","20080610072236","http://www.catalyticsouls.com:80/musicshop.html"),
 ("2008-downloads","20080611000804","http://www.catalyticsouls.com:80/downloads.html"),
 ("2011-ugs","20110202200501","http://www.catalyticsouls.com/ugs/"),
 ("2011-ugs-index","20110325103830","http://www.catalyticsouls.com:80/ugs/index.php?"),
 ("2012-ugs-event61","20120501135941","http://www.catalyticsouls.com:80/ugs/index.php?option=com_eventlist&view=details&id=61&Itemid=9"),
 ("2009-home","2009","http://www.catalyticsouls.com/"),
 ("2010-home","2010","http://www.catalyticsouls.com/"),
 ("2012-home","2012","http://www.catalyticsouls.com/"),
]
os.makedirs('research/raw/wayback/pages',exist_ok=True)
log=open('research/raw/wayback/fetch_log.txt','a',encoding='utf8')
pending=list(targets)
for attempt in range(12):
    still=[]
    for name,ts,url in pending:
        try:
            raw=get(f"https://web.archive.org/web/{ts}id_/{url}")
            open(f'research/raw/wayback/pages/{name}.html','w',encoding='utf8').write(raw)
            open(f'research/raw/wayback/pages/{name}.txt','w',encoding='utf8').write(strip(raw))
            log.write(f"OK {name} {ts} {url}\n"); log.flush()
            time.sleep(2)
        except Exception as e:
            log.write(f"FAIL{attempt} {name} {e}\n"); log.flush(); still.append((name,ts,url)); time.sleep(3)
    pending=still
    if not pending: break
    time.sleep(60)
log.write(f"DONE pending={len(pending)}\n"); log.close()
print("done; pending:",len(pending))
