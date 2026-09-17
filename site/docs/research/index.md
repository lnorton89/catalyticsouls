---
title: Research
---

# Method, sources, and open questions

## How this was built

**Input:** one file, `Tom-Hughes-Thesis.docx` (about 22,000 words), read in full, plus the pointer that the old catalyticsouls.com and the Shawnee Salt Petre Cave would carry the history.

**Process (September 16, 2026):**

1. Full read of the thesis and extraction of every checkable claim: names, dates, venues, numbers, predictions.
2. Three parallel research passes, each with its own brief and its own report (reproduced unedited under Research):
   - the crew, label, members and later Southern Illinois scene;
   - the venue, 1960s to 2026;
   - the industry, law, technology and scholarship, section by section against the thesis.
3. A direct pass on the highest-value primary sources: The Southern Illinoisan's 2005 Cave Fest preview, the Daily Egyptian's 2004–2008 coverage, Resident Advisor and Last.fm event pages, Camp Zoe's still-live website, the Discogs API, Florida corporate records, the Daily Yonder interview, and the Facebook post announcing Hughes' death.
4. The Internet Archive was offline for most of the session ("Internet Archive services are temporarily offline"). Its index came back near the end; page fetches remained intermittent. What was recovered is in the findings log and the repository's `research/raw/wayback/` folder.

**Tools:** web search (a 200-query budget, exhausted), direct page fetches, a browser for sites that block automated fetches (Facebook, Discogs, thesouthern.com, Camp Zoe), the Discogs API, and Wayback's CDX index.

## Sourcing rules used on every page

- **Thesis says** is the author's account, quoted or paraphrased, treated as a primary source with a primary source's limits.
- **Documented** means a dated external source. Contemporaneous listings (RA, Last.fm, forum announcements, a promoter's own site) count as documentation of dates and billing but not of attendance or quality.
- **Inferred / unverified** is flagged in the text. Where two sources conflict (Bluegrass Today's "2004" purchase date versus Wade's "2012 or 2013"), the conflict is stated and the better-supported reading given.
- Numbers from the thesis (attendance, budgets, sales) are reported as his. Independent figures, where they exist, run lower.

## Reliability notes on specific sources

| Source | Note |
|---|---|
| The thesis | Founder's memoir with citations. Anonymizes rivals. Reliable on dates within a season, less so on attendance. |
| The Southern Illinoisan (2005) | Fetched in full via browser; the site rate-limits (HTTP 429) and its 2007–2008 coverage could not be retrieved. |
| Daily Egyptian archive | Reliable and dated; its own search returns nothing for "Underground Sound," so coverage of UGS itself may not exist there. |
| Resident Advisor / Last.fm / The Untz | Event listings only; good for dates, venues, billing. |
| campzoe.com | Still live in 2026 (with SEO spam appended); the UGS 5–6 pages are the promoter's own copy. |
| Discogs | Complete for the label; catalog gaps noted. |
| Florida Division of Corporations (via bisprofiles / flcompany) | Filing dates reliable. |
| Facebook posts (Lo IQ?, TomFoolery page, Shawnee Cave) | Read via browser; dates as displayed. |
| ukfestivalguides.com "Tom Foolery" | Machine-merged page that conflates two artists (wrong real name, UK festival dates); only its CatalyticSouls paragraph matches Hughes. Used with caution. |
| The DJ List rankings | Fan-vote site; "Top 5 breaks" and "#1 Acid Breaks" are self-reported bio claims. |
| Industry statistics | Taken from RIAA, IMS, Pollstar, Billboard, Music Business Worldwide, NTIA, DOJ and court records; each is linked in the industry report. |

## Second pass (September 16–17, 2026)

A second, deeper pass added: the full text of The Southern's July 9, 2007 article and the lead of the July 10 follow-up; 57 YouTube clips across UGS 2 through 7 and Cavetronic; eleven Live Music Archive taper recordings from the cave (2001–2008); the Cavetronic festival of July 2009 (Electronic Assault, Clarksville TN), which shows the cave's electronic era outlasting Catalytic Souls by a year; Andy B's later duo BNasty (Carbondale, 2012–2015); Reperkushin's and Benji Ramsey's later trails; Hughes' 2013 Green Velvet co-credit as Zcarab, his 2016–17 SoundCloud output and the Bandcamp "dub ship Catalytic"; the 1,250-member Facebook fan group created the day after UGS 6; and three background scrapes of the Wayback Machine. Before the archive went offline again those scrapes recovered: an index of 451 forum threads and the text of about 150 (UGS 1's full bill, the UGS 2 announcement and aftermath, the clean-up crisis, the crew's club life); 324 captures of Goodale's cavefest.fws1.com (the "Save The Cave" banner from March 2008, the October 2007 Freakenstein night, the Halloween 2008 co-billing, the 2011 dubstep stage); the Camp Zoe pages and posters for UGS 5 and 6; and 215 images, including the UGS 3 flyer, the 2008 Cave Fest and Halloween flyers and the UGS 6 gallery thumbnails, all now on the [Media](/media) page. The crew's MySpace profiles have no archive captures; the live myspace.com page for catalyticsouls survives with 2,502 connections and album titles but dead photo files. Raw output is under `research/raw/wayback-forum/`, `research/raw/cavefest-site/`, `research/raw/flyers/` and `research/raw/myspace/`. Reddit, TranceAddict, Dogs On Acid, Hip Forums and Facebook group content were unreadable from this environment; the Southern's 2005–2008 features render only headline and byline behind its paywall except for the two July 2007 news stories.

## What could not be found

- The full text of the 2007 coverage of Underground Sound 3. The Southern Illinoisan's July 9 and 10, 2007 stories (at least four arrests; a security firm burning confiscated drugs and knives) were located by headline and lead paragraph only; the paywalled full text and any WSIL/KFVS broadcast segments were not.
- Any explanation, from either side, of why Catalytic Souls and Goodale parted before Cave Fest 2009.
- A newspaper obituary for Tom Hughes.
- Any information on Bob Goodale after 2020.
- Why the Shawnee Cave Amphitheater cancelled its August 2024 festival and whether it will reopen.
- The thesis in OpenSIUC or any library catalog reachable online. Your .docx may be one of very few copies.
- The *USAmnesia* CD or any of the pre-2007 mix CDs.
- Real names for Andy B and Unkl Ryan; what "growAglow" was; anything about later Southern Illinois electronic crews (the one search that ran before the budget ended returned nothing).

## Open questions {#open-questions}

1. **What the archive does not hold.** The catalyticsouls.com forum was fully recovered for 2005–2006 (2,089 captures, 1,325 posts; see `research/raw/wayback-forum/report.md`), but no 2007–2008 threads were ever captured, so the June 2007 "Stabbing at the cave???" thread and any UGS 3, UGS 4 or Camp Zoe discussion are gone. The crew's MySpace profiles have no captures at all. The Caveman Experience site at `intergruv.net/caveman/` (2003–04) was recovered on a later retry and is summarized on [The Cave](/cave/#2-caveman-bob-2000-2011); raw pages are under `research/raw/caveman/`. Goodale's `cavefest.fws1.com` was recovered in full (324 captures).
2. **The 2007 press.** Probably in The Southern's print archive for July 2007 and on WSIL/KFVS.
3. **The split.** Wade, Parrish, Goodale (if living), Andy B, and whoever ran the 2011 Digital-Glitch stage would know.
4. **An obituary.** Full Sail, Auburn's alumni office, or family in Alabama.
5. **The venue now.** Someone in Murphysboro could answer in five minutes what the web can't.
6. **Media.** Notley Hawkins' 266-image Flickr set of UGS 7 exists; the 2006 laser footage and the 2007 YouTube clip exist; the phocas.net UGS 3 gallery exists.

## Files in the repository

- `research/00-WRITEUP-Catalytic-Souls-2007-2026.md` — the long-form writeup this wiki was built from.
- `research/01-primary-findings-log.md` — mirrored at [Primary findings log](/research/findings-log).
- `research/agent-reports/01-catalytic-souls-crew.md` — mirrored at [Agent report: the crew](/research/agent-report-crew).
- `research/agent-reports/02-shawnee-cave-venue-timeline.md` — mirrored at [Agent report: the venue](/research/agent-report-venue).
- `research/agent-reports/03-edm-industry-2007-2026.md` — mirrored at [Agent report: the industry](/research/agent-report-industry).
- `research/raw/Tom-Hughes-Thesis-extracted-text.txt`, `research/raw/discogs-tomfoolery-releases.json`, `research/raw/wayback/` — raw materials.
- `site/` — this wiki (VitePress). `npm install && npm run dev` to run locally; `netlify.toml` is configured for deployment with base `site`, build `npm run build`, publish `docs/.vitepress/dist`.
