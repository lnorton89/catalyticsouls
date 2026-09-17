q(){ # $1 = label, $2 = url param
  out="cdx/$1.json"
  for try in 1 2 3 4 5; do
    code=$(curl -s -m 150 -o "$out" -w "%{http_code}" "http://web.archive.org/cdx/search/cdx?url=$2&output=json&filter=statuscode:200&collapse=digest&limit=500&from=2005&to=2013")
    if [ "$code" = "200" ]; then n=$(python -c "import json;d=open('$out').read().strip();print(max(0,len(json.loads(d))-1) if d else 0)" 2>/dev/null); echo "$1: $n"; return; fi
    echo "  $1 http $code retry $try"; sleep $((8*try))
  done
  echo "$1: FAILED"
}
for n in unklryan unklryanmusic briandervish briandervishmusicpage djderve reperkushin daveskeezy brainstormdj midwestdrumbassalliance benjiramsey; do q "${n}__myspace.com" "myspace.com/${n}*"; sleep 2; done
for n in unklryan unklryanmusic briandervish briandervishmusicpage djderve reperkushin daveskeezy midwestdrumbassalliance benjiramsey djandyb; do q "${n}__profile.myspace.com" "profile.myspace.com/${n}*"; sleep 2; done
q "friendid_10064828__profile" "profile.myspace.com/index.cfm?fuseaction=user.viewprofile&friendid=10064828*"
q "friendid_10064828__blog" "blog.myspace.com/index.cfm?fuseaction=blog.ListAll&friendid=10064828*"
q "friendid_10064828__blogs" "blogs.myspace.com/*friendid=10064828*"
q "friendid_10064828__comment" "comment.myspace.com/*friendid=10064828*"
q "friendid_10064828__any" "myspace.com/*friendid=10064828*"
for n in catalyticsouls djtomfoolery djandyb unklryan briandervish djderve reperkushin daveskeezy brainstormdj midwestdrumbassalliance benjiramsey; do q "${n}__blog.myspace.com" "blog.myspace.com/${n}*"; sleep 2; q "${n}__blogs.myspace.com" "blogs.myspace.com/${n}*"; sleep 2; done
echo ALLDONE
