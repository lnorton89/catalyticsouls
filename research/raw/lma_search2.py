import json,urllib.request,urllib.parse
q='mediatype:etree AND (Saltpetre OR "Salt Petre" OR Saltpeter OR "Shawnee Cave" OR Murphysboro OR "Cave Fest" OR Cavestock OR "Underground Sound" OR "Hogrock")'
u="https://archive.org/advancedsearch.php?q="+urllib.parse.quote(q)+"&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=date&fl%5B%5D=creator&fl%5B%5D=venue&fl%5B%5D=coverage&rows=200&sort%5B%5D=date+asc&output=json"
d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60))
for r in d['response']['docs']: print((r.get('date') or '')[:10],'|',r.get('creator'),'|',r.get('venue'),'|',r.get('coverage'),'|',r.get('title'),'|',r['identifier'])
print('total',d['response']['numFound'])
