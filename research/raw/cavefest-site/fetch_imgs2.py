import os, sys, time, urllib.request, random
urls = ["http://www.cavefest.fws1.com/images/2004flier1.jpg","http://www.cavefest.fws1.com/images/previousflier1_162x250.jpg",
"http://www.cavefest.fws1.com/images/ugs4front_500x391.jpg","http://www.cavefest.fws1.com/images/cavestock4bck_500x340.jpg",
"http://www.cavefest.fws1.com/images/summer_379x500.jpg","http://www.cavefest.fws1.com/images/summer_solstice_back_001_383x500.jpg",
"http://www.cavefest.fws1.com/images/stripmines_378x500.jpg","http://www.cavefest.fws1.com/images/420_show_177x250.jpg",
"http://www.cavefest.fws1.com/images/map_100x65.jpg","http://www.cavefest.fws1.com/images/corn_500x375.jpg",
"http://www.cavefest.fws1.com/images/nrps_250x189.jpg","http://www.cavefest.fws1.com/images/cavefestsky_500x332.jpg",
"http://www.cavefest.fws1.com/images/img00057-20100411-1628_180x132.jpg","http://www.cavefest.fws1.com/images/hackensaw_180x88.jpg",
"http://www.cavefest.fws1.com/images/vendor_180x135.jpg","http://www.cavefest.fws1.com/images/glossyl_eaa8540c6a0f42f1b982f759b0b3cc5b_250x166.jpg",
"http://i84.photobucket.com/albums/k17/celestialaquria/CAVESTOCK5.jpg","http://photobucket.com/albums/k17/celestialaquria/stirpeminesfest08.gif",
"http://i84.photobucket.com/albums/k17/celestialaquria/cavefest07001.jpg","http://i84.photobucket.com/albums/k17/celestialaquria/zacksfest.jpg",
"http://img213.imageshack.us/img213/3478/mybanner475332a08b4ddzx3.jpg","http://farm4.static.flickr.com/3062/2978579931_caf778defd.jpg","http://farm4.static.flickr.com/3063/2978579937_6bed732b09.jpg",
"http://64.136.20.22/312966_q.JPG","http://64.136.20.22/1186795_q.jpg"]
def fetch(url, tries=6):
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 research-scraper"})
            with urllib.request.urlopen(req,timeout=120) as r: return r.read(), r.geturl(), r.headers.get("Content-Type")
        except Exception as e:
            code=getattr(e,"code",None)
            if code==404: return None,None,None
            time.sleep(3*(i+1)+random.random()*2)
    return None,None,None
for u in urls:
    fn="x_"+u.rsplit("/",1)[-1]
    if os.path.exists(fn): continue
    data,final,ct=fetch("https://web.archive.org/web/2010id_/"+u)
    if data and ct and ct.startswith("image"):
        open(fn,"wb").write(data); print("OK",u,len(data),final[:60])
    else: print("MISS",u,ct)
    sys.stdout.flush(); time.sleep(1.5)
