import urllib.request,time
UA={'User-Agent':'Mozilla/5.0'}
ids="x3f2lBqeyP8 TY73p7pzC1s 2wBHnxCO5yg voksGVXLbUs PgaXppmckQk VIKXP5kJVcE IBp6eK9pkLA b7HsAmHsN9w 3nqo9TAq97k uWacDOuM_-o hHOYb31bxI4 QDV5XU5jQVE KZtC3Mg7bmk YGFNlOF2_mc 4fNaqkjkZzM uocmyMpSgDo aYaGHjfwsa8 RJhOCu_zWIo Uic6pF2E6wU HUNrPj6AB5c qMMba-j109Q rbMFn3Lt0bg -Kr3pGK8geQ FbBNs2FJVf0 DDhVJGMu4rc mD4HKlLsJ3M IUW-sWJvc-c BQgwz5Ouato j-dv9qssiD8 qjtmYMCbz3A EGthnulgcdE tYTmZq0HCPo AUh-kQ6KDvM zfch6DlM1d4 6t0TpFzZh_o L04hOuCmX64 daqn74e398s".split()
out=[]
for v in ids:
    try:
        s=urllib.request.urlopen(urllib.request.Request(f'https://www.youtube.com/watch?v={v}',headers=UA),timeout=60).read().decode('utf8','ignore')
        def g(k):
            i=s.find(k)
            if i<0: return ''
            j=s.find('"',i+len(k)); return s[i+len(k):j]
        desc=g('"shortDescription":"').encode('utf8').decode('unicode_escape',errors='ignore').replace('\n',' / ')
        rec=f"{v} | {g('\"title\":\"')} | {g('\"ownerChannelName\":\"')} | {g('\"publishDate\":\"')[:10]} | {g('\"viewCount\":\"')} views\n  desc: {desc[:500]}"
        out.append(rec); print(rec); time.sleep(0.8)
    except Exception as e: print(v,'ERR',e)
open('youtube/ugs-videos.txt','a',encoding='utf8').write('\n'+'\n'.join(out))
