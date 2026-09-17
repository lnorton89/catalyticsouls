import re
src=open('research/agent-reports/03-edm-industry-2007-2026.md',encoding='utf8').read()
parts=re.split(r'\n## ([A-F])\. ',src)
# parts: [preamble, 'A', bodyA, 'B', bodyB, ...]
pages={
 'A':('vinyl-and-retail','Vinyl, downloads & retail','The thesis (Oct 2007) documented a dance-vinyl collapse: 12" sales down from 2,000–3,000 per release to 300–600, labels and stores closing, Satellite Records gone, producers taking day jobs. Here is what happened next.'),
 'B':('beatport-and-distribution','Beatport & digital distribution','The thesis treated Beatport ($1.99 a track, "not taking on any new labels") as the destination and Symphonic Distribution as the way in, with deadmau5 as proof a store could break an unknown. Here is what happened to all four.'),
 'C':('boom-and-bust','The EDM boom and bust','The thesis described a post-2000 decline: clubs going hip-hop, raves shrinking to the low hundreds, Midwest warehouse scenes shut down, Shawnee Cave as the last legal all-nighter. Three years later the biggest boom in American dance-music history began.'),
 'D':('law-and-media','Law & media','The thesis spends a long section on the RAVE Act, the Utah ACLU suit, the UK Criminal Justice Act, and "Techno Rave" headlines. Here is the legal and media record since, including what happened to the venue Underground Sound moved to.'),
 'E':('technology','DJ & production technology','The thesis was written as its author learned Reason and Ableton Live, watched CDJs emulate turntables, and argued that laptops had merged the DJ and the producer. Here is where the booth and the studio went.'),
 'F':('scholarship','Scholarship since 2007','The thesis closed by hoping it had "contributed to what appears a steady but slow growing pool of research." That pool became a field.'),
}
titles={}
m=re.findall(r'\n## ([A-F])\. ([^\n]+)',src)
for k,t in m: titles[k]=t.strip()
for i in range(1,len(parts),2):
    k=parts[i]; body=parts[i+1]
    body=re.sub(r'\n---\s*\n## Gaps and caveats.*','',body,flags=re.S)
    body=re.sub(r'\n---\s*$','',body.strip())
    slug,title,lede=pages[k]
    md=f"---\ntitle: {title}\n---\n\n# {title}\n\n*{lede}*\n\n::: tip Source\nThis page is the section \"{titles[k]}\" of the industry research report compiled September 16, 2026 (about 80 searches and fetches). Items marked **[Inference]** or **[Unverified]** are synthesis or unconfirmed; everything else links to its source. The [scorecard](/then-and-now/scorecard) condenses it against the thesis's claims.\n:::\n\n{body.strip()}\n"
    open(f'site/docs/then-and-now/{slug}.md','w',encoding='utf8').write(md)
    print(slug, len(md))
# research copies
def wrap(title, path, out, intro):
    s=open(path,encoding='utf8').read()
    s=re.sub(r'^# .*\n','',s,count=1)
    open(out,'w',encoding='utf8').write(f"---\ntitle: {title}\n---\n\n# {title}\n\n{intro}\n\n{s}")
wrap('Primary findings log','research/01-primary-findings-log.md','site/docs/research/findings-log.md','*Everything gathered directly in the main research session, with URLs. Mirrors `research/01-primary-findings-log.md` in the repository.*')
wrap('Agent report: the venue','research/agent-reports/02-shawnee-cave-venue-timeline.md','site/docs/research/agent-report-venue.md','*Unedited output of the venue-research pass. Mirrors `research/agent-reports/02-shawnee-cave-venue-timeline.md`.*')
wrap('Agent report: the industry','research/agent-reports/03-edm-industry-2007-2026.md','site/docs/research/agent-report-industry.md','*Unedited output of the industry-research pass. Mirrors `research/agent-reports/03-edm-industry-2007-2026.md`.*')
print('ok')
