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
md=['---','title: Video & flyer archive','---','','# Video and flyer archive','',"Everything audiovisual that survives online from the Catalytic Souls years, gathered September 2026. Videos stay on YouTube under their uploaders' accounts; links go out. Flyers were recovered from the Wayback Machine's copies of catalyticsouls.com and are reproduced as historical documents; rights remain with their designers.",'','::: tip How to read this page',"Titles, uploader, upload date and view counts are as YouTube showed them on September 16, 2026. Descriptions in italics are the uploaders' own words. The raw list is in the repository at `research/raw/youtube/ugs-videos.txt`.",':::','',open('research/raw/youtube/flyers_section.md',encoding='utf8').read(),'','## Live recordings','',"The Live Music Archive (archive.org/details/etree) holds eleven taper recordings made at the cave, which between them cover the Goodale era from its first season to its last big weekend:",'',
"| Date | Artist | Event as tagged by the taper | Archive identifier |","|---|---|---|---|",
"| Apr 28, 2001 | David Nelson Band | Shawnee Cave, Murphysboro | `dnb2001-04-28.flac16` |",
"| Aug 31, 2002 | JEB | Shawnee Endless Summer Fest, Saltpetre Cave | `jeb2002-08-31.sbd` |",
"| Apr 21, 2006 | Cornmeal | Cave Fest 06, Shawnee Salt Petre Cave Amphitheatre | `crnml2006-04-21.flac16` |",
"| Apr 22, 2006 | Cornmeal | Cave Fest 06 | `crnml2006-04-22.flac16` |",
"| Sept 23, 2006 | The New Ledge Band | Cavestock III | `tnlb2006-09-23.sbd.flac16` |",
"| Sept 2, 2007 | Euforquestra | Stripminesfest, Shawnee Cave Amphitheatre | `e2007-09-02` |",
"| Sept 2, 2007 | Family Groove Company | Stripminesfest | `fgc2007-09-02` |",
"| Oct 6, 2007 | Jaik Willis | Cavestock 4 | `jw2007-10-06.mix.flac` |",
"| Oct 6, 2007 | The Super American Happy Fun Good Time Jamband | Cavestock 4 | `sahfgtjb2007-10-06..flac` |",
"| Aug 30, 2008 | Ultraviolet Hippopotamus | Strip Mines Festival | `uvh2008-08-30.flac` |",'',
"Each is at `https://archive.org/details/<identifier>`. No recordings of the electronic stages or of Underground Sound itself were found on the Live Music Archive, which is a jam-band tapers' collection; the DJ sets survive only as the YouTube clips below and as Brian Dervish's three Last.fm uploads (U Lounge 2006, Gamma Fest 2007, Cavestock 4).",'','## Videos','']
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
'<style>.flyer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;align-items:start}.flyer-grid p{margin:0}.flyer-grid img{width:100%;height:auto;border-radius:6px}.gallery{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}</style>']
open('site/docs/media.md','w',encoding='utf8').write('\n'.join(md))
print(len(out),'videos')
