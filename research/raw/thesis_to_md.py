import re
src=open('research/raw/Tom-Hughes-Thesis-extracted-text.txt',encoding='utf8').read().split('\n')
headings={"Foreword","Statement of Purpose","The History of the Dance Genre","Disco Roots","The New Era: Rave and Club Genres","Governmental Censorship & Media Sensationalism to Dance Ritual","Digital Media Technology and DJ Culture","The Economics of the DJ/Producer Team","The Independent Dance Music Industry vs. the Mainstream","The Birth of a Project:  The Cave and TomFoolery","CaveStock 1:  My First Lesson from Promotions 101","CaveFest and Underground Sound:  My Second Lesson from Promotions 102","Back to Cave Fest","Leading Up to the Main Event","The Main Event:  Underground Sound 2 and Lesson Learned","Value Added:  Promotional Compact Discs","Measuring Success Through Branding","Revisiting TomFoolery:  Technology Brings Together the DJ and Producer","Conclusion","REFERENCES:","VITA"}
out=["---","title: Full text of the thesis","outline: [2,3]","---","",
"# Digital Media Technology, Synergy and Making It in Electronic Dance Music","",
"**Thomas W. Hughes** · Southern Illinois University Carbondale · Fall 2007 · Major professor: Phylis Johnson","",
"::: info About this text","This is the complete text of the graduate project paper, extracted from the author's Word document (`Tom-Hughes-Thesis.docx`). Paragraphing follows the original; typographical errors in the original are preserved. Section headings are the author's. Copyright remains with the author's estate; it is reproduced here for study of the work it describes.",":::",""]
buf=[]
def flush():
    global buf
    if buf:
        t=' '.join(x.strip() for x in buf).strip()
        t=re.sub(r'\s+',' ',t)
        if t: out.append(t); out.append("")
        buf=[]
for line in src:
    s=line.strip()
    key=re.sub(r'\s+',' ',s)
    if s in headings or key in {re.sub(r'\s+',' ',h) for h in headings}:
        flush()
        h = s.replace("REFERENCES:","References").replace("VITA","Vita")
        h = re.sub(r'\s+',' ',h)
        out.append("## "+h); out.append("")
        continue
    if not s:
        flush(); continue
    buf.append(s)
flush()
md='\n'.join(out)
# references: put each reference on its own bullet
md=md.replace("## References\n\n","## References\n\n")
open('site/docs/thesis/full-text.md','w',encoding='utf8').write(md)
print(len(md),'chars written')
