import json,collections
d=json.load(open('cdx_intergruv_all.json'))
paths=collections.Counter(r[2].split('intergruv.net')[-1].split('?')[0].rstrip('/').split('/')[1] if '/' in r[2].split('intergruv.net')[-1].strip('/') else r[2].split('intergruv.net')[-1] for r in d)
print(len(d),'pages');print(paths.most_common(25))
yrs=collections.Counter(r[1][:4] for r in d);print(sorted(yrs.items()))
