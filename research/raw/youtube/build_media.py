import re
lines=open('research/raw/youtube/ugs-videos.txt',encoding='utf8',errors='ignore').read().split('\n')
vids=[];i=0
while i<len(lines):
    m=re.match(r'^([A-Za-z0-9_-]{11}) \| (.*?) \| (.*?) \| (\d{4}-\d{2}-\d{2}) \| (\d*) views',lines[i])
    if m:
        desc=lines[i+1][8:].strip() if i+1<len(lines) and lines[i+1].startswith('  desc:') else ''
        vids.append(dict(id=m.group(1),title=m.group(2).replace('\u0026','&'),ch=m.group(3).replace('\ufffd',"'"),date=m.group(4),views=m.group(5),desc=desc))
    i+=1
seen=set();out=[]
for v in vids:
    if v['id'] in seen: continue
    seen.add(v['id']);out.append(v)
def bucket(v):
    t=v['title'].lower()
    if 'cavetronic' in t: return '2009: Cavetronic (the year after Catalytic Souls)'
    if 'sound 2' in t or 'sounds 2' in t: return '2006: Underground Sound 2'
    if 'sound 3' in t or '2007' in t: return '2007: Underground Sound 3'
    if 'sound 4' in t: return '2008: Underground Sound 4'
    if 'sound 5' in t: return '2009: Underground Sound 5, Camp Zoe'
    if 'sound 6' in t: return '2010: Underground Sound 6, Camp Zoe'
    if 'sound 7' in t: return '2011: Underground Sound 7, Hogrock'
    if 'cavefest' in t: return '2011: Cave Fest (Goodale era)'
    return 'Other'
groups={}
for v in out: groups.setdefault(bucket(v),[]).append(v)
order=['2006: Underground Sound 2','2007: Underground Sound 3','2008: Underground Sound 4','2009: Underground Sound 5, Camp Zoe','2010: Underground Sound 6, Camp Zoe','2011: Underground Sound 7, Hogrock','2009: Cavetronic (the year after Catalytic Souls)','2011: Cave Fest (Goodale era)','Other']
md=['---','title: Video & flyer archive','---','','# Video and flyer archive','',"Everything audiovisual that survives online from the Catalytic Souls years, gathered September 2026. Videos stay on YouTube under their uploaders' accounts; links go out. Flyers were recovered from the Wayback Machine's copies of catalyticsouls.com and are reproduced as historical documents; rights remain with their designers.",'','::: tip How to read this page',"Titles, uploader, upload date and view counts are as YouTube showed them on September 16, 2026. Descriptions in italics are the uploaders' own words. The raw list is in the repository at `research/raw/youtube/ugs-videos.txt`.",':::','','## Flyers','','<div class="flyer-grid">','','![Cave Jam Solstice pre-flyer, June 23–25, 2006 (Vince Herman of Leftover Salmon)](/flyers/cavejamweb.jpg)','','![Gamma Fest pre-flyer, August 17–18, 2007, Eureka Springs, Arkansas (Shpongle, Hallucinogen; Catalytic Souls with Twisted)](/flyers/shpongle-pre.jpg)','','![Underground Sound 6 "Freakadelic" flyer, August 13–15, 2010, Camp Zoe (Rabbit in the Moon 3D)](/flyers/ugs6.jpg)','','</div>','',"*Left to right: Cave Jam Solstice, June 2006 · Gamma Fest, August 2007 · Underground Sound 6, August 2010.* The archived `/flyers/` directory on catalyticsouls.com also listed Cave Fest 2005 (back), Cave Rock Festival 2005 (front and back), Underground Sound 1 (front and back), TechnoMeister, CaveStock 2, Face of Bass (St. Louis and Jackson), PsychoTronic, Mardi Gras 2006, Cave Fest 2006 and UGS 2 (\"undergroundin\" / \"undergroundout\"); the archive holds only placeholder pages for those files. A scraper for further images across the archived crew, cave, Camp Zoe and MySpace pages is in `research/raw/flyers/`; anything it recovers will be added here.",'','## Live recordings','',"- **Cornmeal, Cave Fest 2006** — two full audience recordings on the Live Music Archive: April 21, 2006 (https://archive.org/details/crnml2006-04-21.flac16) and April 22, 2006 (https://archive.org/details/crnml2006-04-22.flac16), \"Live at Shawnee Salt Petre Cave Amphitheatre.\"",'','## Videos','']
for g in order:
    if g not in groups: continue
    md.append(f'### {g}');md.append('')
    for v in sorted(groups[g],key=lambda x:x['date']):
        d=v['desc'] if v['desc'] and v['desc'] not in (':)',';)','(promo clip)') else ''
        md.append(f"- [**{v['title']}**](https://www.youtube.com/watch?v={v['id']}) — {v['ch']}, uploaded {v['date']}, {v['views']} views." + (f" *\"{d}\"*" if d else ''))
    md.append('')
md+=['## Photo sets and groups (not reproduced here)','',
'- **UGS 3, July 2007** — phocas.net photo report "Underground Sound 3: the freaks come out" (100+ DJ lineup listed): https://www.phocas.net/2007/07/underground-sound-3-thre-freaks-come-out.html',
'- **UGS 7, July 2011** — Notley Hawkins, Flickr, "Underground Sound 7" (about 266 images): https://www.flickr.com/search/?text=%22Underground%20Sound%207%22%20Hogrock',
'- **UGS 6 gallery** — roughly 70 images were embedded on catalyticsouls.com\'s 2010–11 front page (Wayback capture 20110201223509).',
'- **Facebook group "UnderGround Sound Festival UGS7--- Fan Page"** — public group created August 16, 2010 (the day after UGS 6 ended), 1,256 members as of September 2026, an "Andy" as admin, no posts in the past month: https://www.facebook.com/groups/148266991867017',
'- **Reddit** — r/aves "Underground Sound 4 [8/16/2008] Multigenre Rave in Murphysboro, IL" (photo post) and r/aves "Cave Rave" (memories thread). Reddit could not be read from this research environment.','',
'<style>.flyer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;align-items:start}.flyer-grid p{margin:0}.flyer-grid img{width:100%;height:auto;border-radius:6px}</style>']
open('site/docs/media.md','w',encoding='utf8').write('\n'.join(md))
print(len(out),'videos')
