import urllib.request, re, html, json, sys, time
UA={'User-Agent':'Mozilla/5.0 (research)'}
def get(url):
    r=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(r,timeout=60) as f: return f.read().decode('utf8','ignore')
def strip(h):
    h=re.sub(r'(?is)<(script|style).*?</\1>','',h)
    h=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</tr>|</li>|</h\d>','\n',h)
    h=re.sub(r'<[^>]+>',' ',h)
    h=html.unescape(h)
    h=re.sub(r'[ \t\r\f\v]+',' ',h)
    h=re.sub(r'\n\s*\n+','\n',h)
    return h.strip()
out=[]
for year in ['2005','2006','2007','2008','2009','2010','2011','2012','2013','2014']:
    try:
        cdx=get(f"https://web.archive.org/cdx/search/cdx?url=catalyticsouls.com/&output=json&from={year}&to={year}&filter=statuscode:200&limit=1")
        rows=json.loads(cdx)
        if len(rows)<2: out.append(f"\n===== {year}: no 200 capture of homepage\n"); continue
        ts=rows[1][1]
        raw=get(f"https://web.archive.org/web/{ts}id_/http://www.catalyticsouls.com/")
        txt=strip(raw)
        links=re.findall(r'href=["\']([^"\']+)["\']',raw)
        out.append(f"\n===== {year} homepage capture {ts} =====\n{txt[:6000]}\n--- links: {sorted(set(l for l in links if 'catalyticsouls' in l or l.startswith('/') or l.endswith('.php') or l.endswith('.html')))[:60]}\n")
        time.sleep(1)
    except Exception as e:
        out.append(f"\n===== {year}: ERROR {e}\n")
open('research/raw/wayback/homepage-by-year.txt','w',encoding='utf8').write(''.join(out))
print(''.join(out)[:20000])
