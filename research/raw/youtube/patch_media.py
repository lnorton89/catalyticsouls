p='research/raw/youtube/build_media.py'
s=open(p,encoding='utf8').read()
start=s.index('"## Flyers and posters"')
end=s.index("'## Live recordings'")
s=s[:start]+"open('research/raw/youtube/flyers_section.md',encoding='utf8').read(),'',"+s[end:]
open(p,'w',encoding='utf8').write(s)
print('patched')
