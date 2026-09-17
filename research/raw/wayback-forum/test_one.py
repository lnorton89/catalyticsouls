import fetcher,time
t=time.time()
b,e=fetcher.get('https://web.archive.org/web/20061106221606id_/http://www.catalyticsouls.com/forums/viewforum.php?f=9&start=0',tries=3,log=print)
print('err',e,'len',len(b) if b else None, round(time.time()-t,1),'s')
if b: print(fetcher.strip(b)[:1500])
