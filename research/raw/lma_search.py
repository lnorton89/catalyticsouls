import json,urllib.request
u="https://archive.org/advancedsearch.php?q=%28%22Salt+Petre+Cave%22+OR+%22Saltpetre+Cave%22+OR+%22Shawnee+Cave%22+OR+%22Saltpeter+Cave%22+OR+%22Camp+Zoe%22+OR+%22Underground+Sound%22%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=date&fl%5B%5D=creator&fl%5B%5D=mediatype&rows=200&output=json"
try:
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60))
    for r in d['response']['docs']: print((r.get('date') or '')[:10],'|',r.get('mediatype'),'|',r.get('creator'),'|',r.get('title'),'|',r['identifier'])
    print('total',d['response']['numFound'])
except Exception as e: print('err',e)
