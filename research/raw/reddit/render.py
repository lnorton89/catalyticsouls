import json, glob, datetime, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
out = []
for sub in sorted(glob.glob('sub_*.json')):
    lid = sub[4:-5]
    s = json.load(open(sub, encoding='utf-8'))['data']
    for p in s:
        d = datetime.datetime.utcfromtimestamp(float(p['created_utc'])).strftime('%Y-%m-%d')
        out.append(f"# r/{p.get('subreddit')} — {p.get('title')}\n({d}) u/{p.get('author')} https://www.reddit.com{p.get('permalink','')}\n\n{p.get('selftext','')}\n")
    c = json.load(open(f'comments_{lid}.json', encoding='utf-8'))['data']
    for x in sorted(c, key=lambda k: float(k['created_utc'])):
        d = datetime.datetime.utcfromtimestamp(float(x['created_utc'])).strftime('%Y-%m-%d')
        out.append(f"--- u/{x.get('author')} ({d}, score {x.get('score')}):\n{x.get('body','')}\n")
    out.append('\n=====================\n')
open('reddit-threads.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
