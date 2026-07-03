# -*- coding: utf-8 -*-
# Blog üreteci: _kaynak/blog/*.json -> /blog/ dizini + /blog/<slug>/ makale sayfaları
# Tasarım sistemi gen_pages.py'den exec ile alınır (header/footer/CSS/doc senkron kalır).
import os, html, json, re

SCR="/private/tmp/claude-501/-Volumes-ABDURRAHMAN-APP-Tavuk--ad-r-/c4778228-16bc-4e77-b9dd-f19e5b0e793d/scratchpad"
PROJ="/Volumes/ABDURRAHMAN/APP/Tavuk Çadırı"

_src=open(os.path.join(SCR,"gen_pages.py"),encoding="utf-8").read()
exec(_src.split("pages=[]")[0])  # e, SITE, WA, CSS, header, footer, doc, phead, cta_block

# Blog'a özel ek CSS (faq/rel gen_pages CSS'inde yok + kart/tablo stilleri)
CSS = CSS + """
.prose table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #ECE3D6;border-radius:14px;overflow:hidden;font-size:15px;margin:6px 0 18px}
.prose th{text-align:left;background:#FCFAF6;color:#6E6256;font-weight:700;font-size:12.5px;text-transform:uppercase;letter-spacing:.04em;padding:11px 14px}
.prose td{padding:11px 14px;border-top:1px solid #F1E9DC;color:#221A12;vertical-align:top}
.prose a{color:#C25E10;font-weight:600}
.prose ol{margin:0 0 14px;padding-left:22px;color:#4C443A;font-size:16px;line-height:1.7}
details>summary{list-style:none;cursor:pointer}details>summary::-webkit-details-marker{display:none}
.faq-chev{transition:transform .28s ease}details[open] .faq-chev{transform:rotate(180deg)}
.faq-list{display:flex;flex-direction:column;gap:12px;max-width:820px}
.faq{background:#fff;border:1px solid #EFE7DA;border-radius:16px;padding:2px 20px}
.faq summary{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px 0;font-family:'Poppins';font-weight:600;font-size:16.5px;color:#221A12}
.faq .ans{padding:0 0 16px;font-size:15.5px;line-height:1.65;color:#6E6256}
.rel{display:grid;grid-template-columns:1fr;gap:14px}
.rel a{display:flex;align-items:center;justify-content:space-between;gap:14px;background:#fff;border:1px solid #ECE3D6;border-radius:16px;padding:18px 20px;font-family:'Poppins';font-weight:600;font-size:16px;color:#221A12}
.rel a:hover{border-color:#E5751B}
.rel a svg{color:#E5751B;flex:none}
.bmeta{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.bmeta span{background:#fff;border:1px solid #ECE3D6;border-radius:999px;padding:6px 13px;font-size:13px;font-weight:600;color:#6E6256}
.bgrid{display:grid;grid-template-columns:1fr;gap:18px}
.bcard{background:#fff;border:1px solid #EFE7DA;border-radius:20px;padding:26px;display:flex;flex-direction:column;transition:.16s}
.bcard:hover{border-color:#E5751B;box-shadow:0 20px 40px -30px rgba(34,26,18,.4)}
.bcard .bk{font-weight:600;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#C25E10;margin-bottom:10px}
.bcard h2{font-family:'Poppins';font-weight:700;font-size:20px;line-height:1.25;color:#221A12;margin:0 0 10px}
.bcard p{font-size:14.5px;line-height:1.6;color:#6E6256;margin:0 0 16px;flex:1}
.bcard .bm{font-size:13px;color:#8B7E6E;display:flex;gap:10px;align-items:center}
.bcard .go{margin-top:14px;display:inline-flex;align-items:center;gap:7px;font-weight:600;font-size:14.5px;color:#C25E10}
@media(min-width:680px){.bgrid{grid-template-columns:1fr 1fr}.rel{grid-template-columns:repeat(3,1fr)}}
@media(min-width:1020px){.bgrid{grid-template-columns:repeat(3,1fr)}}
"""

ARROW='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#E5751B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'
CHEV='<svg class="faq-chev" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#C25E10" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex:none"><path d="M6 9l6 6 6-6"></path></svg>'

ALLOWED=re.compile(r'</?(p|ul|ol|li|strong|em|a|h3|table|thead|tbody|tr|th|td)(\s[^>]*)?>', re.I)
def sanitize(h):
    # izinli etiket dışındakileri sök (script/style dahil)
    h=re.sub(r'<script.*?</script>','',h,flags=re.S|re.I)
    return re.sub(r'<[^>]+>', lambda m: m.group(0) if ALLOWED.match(m.group(0)) else '', h)

def words(art):
    t=art["intro_html"]+" ".join(s["html"]+" "+s["h2"] for s in art["sections"])
    return len(re.sub(r'<[^>]+>',' ',t).split())

def load_articles():
    d=os.path.join(PROJ,"_kaynak","blog")
    arts=[]
    for f in sorted(os.listdir(d)):
        if f.endswith(".json") and not f.startswith("._"):
            arts.append(json.load(open(os.path.join(d,f),encoding="utf-8")))
    arts.sort(key=lambda a:a.get("order",99))
    return arts

def faq_html(faq):
    items="".join('<details class="faq"><summary>%s%s</summary><div class="ans">%s</div></details>'%(e(x["q"]),CHEV,e(x["a"])) for x in faq)
    return '<div class="faq-list">%s</div>'%items

def article_page(rec, by_slug):
    a=rec["article"]; slug=rec["slug"]
    w=words(a); mins=max(3,round(w/200))
    date_disp=rec.get("date_disp","3 Temmuz 2026"); date_iso=rec.get("date","2026-07-03")
    crumb='<a href="../../index.html">Ana Sayfa</a> › <a href="../">Blog</a> › <b>%s</b>'%e(a["title"][:46]+("…" if len(a["title"])>46 else ""))
    hero=('<div class="wrap"><div class="crumb">%s</div></div>'
      '<section class="phead"><div class="wrap"><div class="ey">Blog</div><h1>%s</h1><p>%s</p>'
      '<div class="bmeta"><span>%s</span><span>%s dk okuma</span><span>Tavuk Çadırı Ekibi</span></div></div></section>')%(crumb,e(a["title"]),e(a["meta_desc"]),date_disp,mins)
    body_secs='<section class="sec"><div class="wrap"><div class="prose">'+sanitize(a["intro_html"])
    for s in a["sections"]:
        body_secs+='<h2>%s</h2>'%e(s["h2"])+sanitize(s["html"])
    body_secs+='</div></div></section>'
    faq='<section class="sec" style="background:#FBF8F3"><div class="wrap"><h2 style="font-family:Poppins;font-weight:700;font-size:clamp(22px,3vw,30px);margin:0 0 20px">Sık sorulanlar</h2>%s</div></section>'%faq_html(a["faq"])
    rel_items=""
    for rs in rec.get("related",[])[:3]:
        r=by_slug.get(rs)
        if r: rel_items+='<a href="../%s/">%s %s</a>'%(rs,e(r["article"]["title"]),ARROW)
    related='<section class="sec"><div class="wrap"><h2 style="font-family:Poppins;font-weight:700;font-size:clamp(20px,2.6vw,26px);margin:0 0 18px">İlgili yazılar</h2><div class="rel">%s</div></div></section>'%rel_items if rel_items else ''
    body=hero+body_secs+faq+related+cta_block()
    out=doc(a["meta_title"]+" | Tavuk Çadırı Blog", a["meta_desc"], "blog/"+slug, body, pre="../../")
    out=out.replace('og:type" content="website"','og:type" content="article"',1)
    graph={"@context":"https://schema.org","@graph":[
      {"@type":"BlogPosting","headline":a["title"],"description":a["meta_desc"],"inLanguage":"tr-TR",
       "datePublished":date_iso,"dateModified":date_iso,
       "image":SITE+"/assets/photos/model-1000.jpg",
       "author":{"@type":"Organization","name":"Tavuk Çadırı","url":SITE+"/"},
       "publisher":{"@type":"Organization","name":"Tavuk Çadırı","logo":{"@type":"ImageObject","url":SITE+"/assets/logo.png"}},
       "mainEntityOfPage":"%s/blog/%s/"%(SITE,slug)},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":x["q"],"acceptedAnswer":{"@type":"Answer","text":x["a"]}} for x in a["faq"]]},
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Ana Sayfa","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":SITE+"/blog/"},
        {"@type":"ListItem","position":3,"name":a["title"],"item":"%s/blog/%s/"%(SITE,slug)}]}]}
    out=out.replace('</head>','<script type="application/ld+json">%s</script></head>'%json.dumps(graph,ensure_ascii=False,separators=(",",":")),1)
    return out

def index_page(arts):
    crumb='<a href="../index.html">Ana Sayfa</a> › <b>Blog</b>'
    hero=('<div class="wrap"><div class="crumb">%s</div></div>'
      '<section class="phead"><div class="wrap"><div class="ey">Blog</div><h1>Tavukçuluk ve kümes rehberi</h1>'
      '<p>Kümes kurmayı düşünenler ve sürüsünü büyütmek isteyenler için sahadan, abartısız rehberler: maliyet hesapları, ruhsat ve destekler, kışa hazırlık, verim ve daha fazlası.</p></div></section>')%crumb
    cards=""
    for rec in arts:
        a=rec["article"]; w=words(a); mins=max(3,round(w/200))
        cards+=('<a class="bcard" href="%s/"><span class="bk">Rehber</span><h2>%s</h2><p>%s</p>'
          '<span class="bm">%s · %s dk okuma</span><span class="go">Yazıyı oku %s</span></a>')%(rec["slug"],e(a["title"]),e(a["meta_desc"]),rec.get("date_disp","3 Temmuz 2026"),mins,ARROW)
    body=hero+'<section class="sec"><div class="wrap"><div class="bgrid">%s</div></div></section>'%cards+cta_block()
    out=doc("Blog — Tavukçuluk ve Kümes Rehberi","Tavukçuluğa başlayacaklar için maliyet, ruhsat, devlet desteği, kış bakımı ve verim rehberleri. Sahadan, abartısız ve güncel bilgiler.","blog",body,pre="../")
    graph={"@context":"https://schema.org","@graph":[
      {"@type":"Blog","name":"Tavuk Çadırı Blog","url":SITE+"/blog/","inLanguage":"tr-TR",
       "publisher":{"@type":"Organization","name":"Tavuk Çadırı","logo":{"@type":"ImageObject","url":SITE+"/assets/logo.png"}}},
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Ana Sayfa","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":SITE+"/blog/"}]}]}
    out=out.replace('</head>','<script type="application/ld+json">%s</script></head>'%json.dumps(graph,ensure_ascii=False,separators=(",",":")),1)
    return out

def patch_sitemap(arts):
    for base in (PROJ,SCR):
        p=os.path.join(base,"sitemap.xml")
        if not os.path.exists(p): continue
        s=open(p,encoding="utf-8").read()
        s=re.sub(r'\s*<url><loc>[^<]*?/blog/[^<]*</loc>.*?</url>','',s)  # eski blog kayıtlarını temizle (idempotent)
        entries='<url><loc>%s/blog/</loc><lastmod>2026-07-03</lastmod><changefreq>weekly</changefreq></url>'%SITE
        for rec in arts:
            entries+='<url><loc>%s/blog/%s/</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq></url>'%(SITE,rec["slug"],rec.get("date","2026-07-03"))
        s=s.replace('</urlset>',entries+'\n</urlset>')
        open(p,"w",encoding="utf-8").write(s)
    print("sitemap: +%d blog url"%(len(arts)+1))

arts=load_articles()
by_slug={r["slug"]:r for r in arts}
for base in (PROJ,SCR):
    os.makedirs(os.path.join(base,"blog"),exist_ok=True)
    open(os.path.join(base,"blog","index.html"),"w",encoding="utf-8").write(index_page(arts))
    for rec in arts:
        d=os.path.join(base,"blog",rec["slug"]); os.makedirs(d,exist_ok=True)
        open(os.path.join(d,"index.html"),"w",encoding="utf-8").write(article_page(rec,by_slug))
patch_sitemap(arts)
print("blog: dizin + %d makale üretildi"%len(arts))
