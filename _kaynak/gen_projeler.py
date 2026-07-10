# -*- coding: utf-8 -*-
# Projeler üreteci: _kaynak/projeler.json + _kaynak/projeler/<slug>/*.png|jpg ->
#   assets/photos/projeler/ (webp, EXIF'siz) + /projeler/ sayfası + ana sayfa "Son projeler" şeridi + sitemap
# Tasarım sistemi gen_pages.py'den exec ile alınır (header/footer/CSS/doc senkron kalır).
# Yeni proje akışı: ham fotoğraf klasörünü /projeler/ altına bırak -> bu betik _kaynak/projeler/'e taşır,
#   projeler.json'a kayıt eklenince bir sonraki çalıştırmada yayına girer.
import os, html, json, re, shutil
from urllib.parse import quote
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)

_src = open(os.path.join(HERE, "gen_pages.py"), encoding="utf-8").read()
exec(_src.split("pages=[]")[0])  # e, SITE, WA, WA_DISP, WA_SVG, CSS, header, footer, doc, phead, cta_block

RAW = os.path.join(HERE, "projeler")          # ham fotoğraf kaynağı (deploy edilmez)
GELEN = os.path.join(PROJ, "projeler")        # yayın klasörü; içine bırakılan ham klasörler _kaynak'a taşınır
OUT = os.path.join(PROJ, "assets", "photos", "projeler")
CARD_W, Q = 1000, 82

CSS = CSS + """
.bmeta{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.bmeta span{background:#fff;border:1px solid #ECE3D6;border-radius:999px;padding:6px 13px;font-size:13px;font-weight:600;color:#6E6256}
.proj{background:#fff;border:1px solid #EFE7DA;border-radius:22px;overflow:hidden;margin:0 0 26px;scroll-margin-top:96px}
.pj-strip{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;padding:10px;background:#F6F1E8;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.pj-strip::-webkit-scrollbar{display:none}
.pj-strip img{width:100%;aspect-ratio:4/3;object-fit:cover;flex:none;scroll-snap-align:center;border-radius:14px;display:block;pointer-events:none;user-select:none}
.pj-dots{display:flex;justify-content:center;gap:7px;padding:12px 0 2px;background:#fff}
.pj-dots span{width:7px;height:7px;border-radius:50%;background:#E3D7C5;transition:background .2s,transform .2s}
.pj-dots span.on{background:#E5751B;transform:scale(1.2)}
@media(min-width:900px){.pj-strip img{width:auto;aspect-ratio:auto;height:340px}.pj-dots{display:none}.pj-strip{scrollbar-width:thin}.pj-strip::-webkit-scrollbar{display:initial;height:8px}}
.pj-body{padding:22px clamp(18px,3vw,28px) 24px}
.pj-body h2{font-family:'Poppins';font-weight:700;font-size:clamp(20px,2.6vw,26px);letter-spacing:-.015em;color:#221A12;margin:0}
.pj-body .bmeta{margin:12px 0 2px}
.pj-body p{font-size:15.5px;line-height:1.65;color:#4C443A;margin:12px 0 18px;max-width:760px}
.pj-links{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.pj-links .ln{display:inline-flex;align-items:center;gap:7px;border:1px solid #E3D7C5;border-radius:999px;padding:10px 16px;font-weight:600;font-size:14.5px;color:#3C342B}
.pj-links .ln:hover{border-color:#E5751B;color:#C25E10}
@media(max-width:899px){
.pj-body{padding-bottom:26px}
.pj-body h2{font-size:21px}
.pj-body .bmeta,.pj-links .ln{display:none}
.pj-body p{margin:12px 0 20px}
.pj-links{justify-content:center}
.pj-links .wa-btn{font-size:15.5px;padding:13px 24px}
}
"""

# mobil: kaydırma konumunu gösteren noktalar (JS yoksa noktalar hiç çizilmez, galeri yine çalışır)
DOTS_JS = (
 "(function(){document.querySelectorAll('.pj-strip').forEach(function(st){"
 "var ims=st.querySelectorAll('img');if(ims.length<2)return;"
 "var d=document.createElement('div');d.className='pj-dots';"
 "ims.forEach(function(_,i){var s=document.createElement('span');if(i===0)s.className='on';d.appendChild(s);});"
 "st.after(d);"
 "st.addEventListener('scroll',function(){"
 "var w=ims[0].offsetWidth+10,i=Math.max(0,Math.min(ims.length-1,Math.round(st.scrollLeft/w)));"
 "d.querySelectorAll('span').forEach(function(s,j){s.className=j===i?'on':'';});},{passive:true});});})();")

def ingest():
    # /projeler/ içine bırakılan ham klasörleri kaynağa taşı (yayına ham dosya sızmasın)
    if not os.path.isdir(GELEN): return
    for item in os.listdir(GELEN):
        p = os.path.join(GELEN, item)
        if os.path.isdir(p):
            dest = os.path.join(RAW, item)
            if os.path.exists(dest): dest += "-yeni"
            shutil.move(p, dest)
            print("TAŞINDI: /projeler/%s -> _kaynak/projeler/ — projeler.json'a kayıt ekleyin" % item)
        elif item.startswith("._"):
            os.remove(p)

def load():
    recs = json.load(open(os.path.join(HERE, "projeler.json"), encoding="utf-8"))
    recs.sort(key=lambda r: r["date"], reverse=True)
    return recs

def photos(rec):
    # ham klasördeki görselleri webp'ye çevir (Pillow yeniden kaydettiği için EXIF/GPS taşınmaz)
    src = os.path.join(RAW, rec.get("kaynak", rec["slug"]))
    if not os.path.isdir(src):
        # ham kaynak bu makinede yok (gitignore'lu) -> daha önce üretilmiş webp'lerle devam et
        n = len([f for f in os.listdir(OUT) if re.match(re.escape(rec["slug"]) + r"-\d+\.webp$", f)])
        if n: print("bilgi: ham klasör yok, mevcut %d webp kullanılıyor: %s" % (n, rec["slug"]))
        else: print("UYARI: ne ham klasör ne işlenmiş görsel var, proje atlandı: %s" % rec["slug"])
        return list(range(1, n + 1))
    files = sorted(f for f in os.listdir(src)
                   if not f.startswith("._") and f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")))
    # eski çıktıları temizle (fotoğraf sayısı azaldıysa bayat webp kalmasın)
    for f in os.listdir(OUT):
        if re.match(re.escape(rec["slug"]) + r"-(\d+(-buyuk)?\.webp|og\.jpg)$", f):
            os.remove(os.path.join(OUT, f))
    out = []
    for i, f in enumerate(files, 1):
        im = Image.open(os.path.join(src, f)).convert("RGB")
        r = im if im.width <= CARD_W else im.resize((CARD_W, round(im.height * CARD_W / im.width)), Image.LANCZOS)
        r.save(os.path.join(OUT, "%s-%d.webp" % (rec["slug"], i)), "WEBP", quality=Q, method=6)
        if i == 1:  # og:image — 1200x630 merkez kırpma, jpg
            ow, oh = 1200, 630
            s = max(ow / im.width, oh / im.height)
            r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            x, y = (r.width - ow) // 2, (r.height - oh) // 2
            r.crop((x, y, x + ow, y + oh)).save(os.path.join(OUT, "%s-og.jpg" % rec["slug"]), "JPEG", quality=85)
        out.append(i)
    return out

def chips(rec):
    items = ["%s · %d m²" % (rec["olcu"].replace("x", "×"), rec["m2"]), rec["model_ad"], rec["yalitim"],
             "Nakliye + kurulum dahil", rec["date_disp"]]
    return '<div class="bmeta">%s</div>' % "".join("<span>%s</span>" % e(x) for x in items)

def strip_html(rec, n, pre="", eager=False):
    imgs = ""
    for i in range(1, n + 1):
        alt = "%s — fotoğraf %d/%d" % (rec["alt"], i, n)
        imgs += ('<img src="%sassets/photos/projeler/%s-%d.webp" alt="%s" %s>') % (
                 pre, rec["slug"], i, e(alt),
                 'fetchpriority="high"' if (eager and i == 1) else 'loading="lazy"')
    return '<div class="pj-strip">%s</div>' % imgs

ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#E5751B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'

def yer(rec):  # "İl İlçe" — ilçe yoksa sadece "İl" (çift boşluk olmasın)
    return "%s %s" % (rec["il"], rec["ilce"]) if rec.get("ilce") else rec["il"]

def proj_card(rec, n, first=False):
    wa = "https://wa.me/%s?text=%s" % (WA, quote(rec["wa_text"]))
    links = ('<div class="pj-links">'
             '<a href="%s" target="_blank" rel="noopener" class="wa-btn" style="font-size:14.5px;padding:11px 18px">%s<span>Benzer kurulum için teklif al</span></a>'
             '<a class="ln" href="../%s/">%s modeli %s</a>'
             '<a class="ln" href="../%s/">%s kurulum sayfası %s</a>'
             '</div>') % (wa, WA_SVG.format(w=17, f="#fff"), rec["model_slug"], e(rec["model_ad"]), ARROW,
                          rec["il_page"], e(rec["il"]), ARROW)
    return ('<article class="proj" id="%s">%s'
            '<div class="pj-body"><h2>%s — %s Tavuk Çadırı Kurulumu Tamamlandı</h2>%s<p>%s</p>%s</div></article>') % (
            rec["slug"], strip_html(rec, n, pre="../", eager=first),
            e(yer(rec)), e(rec["model_ad"]), chips(rec), e(rec["aciklama"]), links)

def hub_page(recs, counts):
    crumb = '<a href="../index.html">Ana Sayfa</a> › <b>Projeler</b>'
    hero = phead("Sahadan", "Tamamlanan projeler",
                 "Kurduğumuz her çadırı sahada çekilmiş fotoğraflarıyla burada yayınlıyoruz — söz değil, teslim edilmiş iş. Liste her yeni kurulumla büyüyor.", crumb)
    cards = "".join(proj_card(r, counts[r["slug"]], first=(i == 0)) for i, r in enumerate(recs) if counts.get(r["slug"]))
    davet = ('<section class="sec" style="background:#FBF8F3"><div class="wrap"><div class="prose">'
             '<h2 style="margin-top:0">Sizin sahanız da burada yer alsın</h2>'
             '<p>Kurulum tamamlandığında fotoğrafları (izninizle) bu sayfada yayınlıyor, ilinizin sayfasına da ekliyoruz. '
             'Bölgenize benzer bir kurulum için <a href="../iletisim/" style="color:#C25E10;font-weight:600">bize ulaşın</a> '
             'veya <a href="../fiyatlar/" style="color:#C25E10;font-weight:600">güncel fiyat tablosuna</a> bakın.</p>'
             '</div></div></section>')
    body = hero + '<section class="sec"><div class="wrap">' + cards + '</div></section>' + davet + cta_block()
    out = doc("Tamamlanan Projeler — Sahadan Kurulum Fotoğrafları",
              "Türkiye genelinde kurduğumuz tavuk çadırlarından saha fotoğrafları: il il tamamlanan projeler, ölçü ve kurulum detayları. Benzer kurulum için teklif alın.",
              "projeler", body, pre="../", extra_js=DOTS_JS)
    if recs and counts.get(recs[0]["slug"]):
        out = out.replace(SITE + "/assets/photos/og/og-home.jpg", "%s/assets/photos/projeler/%s-og.jpg" % (SITE, recs[0]["slug"]))
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Tamamlanan Projeler", "url": SITE + "/projeler/", "inLanguage": "tr-TR",
         "description": "Tavuk Çadırı tarafından tamamlanan kurulumların saha fotoğrafları."},
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "name": "%s — %s Tavuk Çadırı Kurulumu" % (yer(r), r["model_ad"]),
             "url": "%s/projeler/#%s" % (SITE, r["slug"]),
             "image": "%s/assets/photos/projeler/%s-1.webp" % (SITE, r["slug"])} for i, r in enumerate(recs)]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Projeler", "item": SITE + "/projeler/"}]}]}
    out = out.replace('</head>', '<script type="application/ld+json">%s</script></head>' % json.dumps(graph, ensure_ascii=False, separators=(",", ":")), 1)
    return out

def home_card(rec):
    return ('<a data-reveal href="projeler/#%s" style="background:#fff;border:1px solid #EFE7DA;border-radius:20px;overflow:hidden;display:flex;flex-direction:column;transition:.16s" '
            'onmouseover="this.style.borderColor=\'#E5751B\'" onmouseout="this.style.borderColor=\'#EFE7DA\'">'
            '<img src="assets/photos/projeler/%s-1.webp" alt="%s" loading="lazy" width="1000" height="750" style="width:100%%;height:210px;object-fit:cover;display:block;border-bottom:1px solid #F1E9DC">'
            '<span style="padding:18px 20px 20px;display:flex;flex-direction:column;gap:6px">'
            '<span style="font-weight:600;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#C25E10">%s</span>'
            '<span style="font-family:\'Poppins\',sans-serif;font-weight:700;font-size:18px;color:#221A12">%s — %s Kurulumu Tamamlandı</span>'
            '<span style="font-size:14px;color:#6E6256">%s · %d m² · nakliye ve kurulum dahil teslim edildi</span>'
            '<span style="display:inline-flex;align-items:center;gap:7px;font-weight:600;font-size:14.5px;color:#C25E10;margin-top:6px">Projeyi incele %s</span>'
            '</span></a>') % (rec["slug"], rec["slug"], e(rec["alt"]), e(rec["date_disp"]),
                              e(yer(rec)), e(rec["model_ad"]),
                              rec["olcu"].replace("x", "×"), rec["m2"], ARROW)

def home_section(recs):
    cards = "".join(home_card(r) for r in recs[:3])
    return ('\n  <!-- ===== PROJELER (gen_projeler.py üretir; elle düzenlemeyin) ===== -->\n'
            '  <section id="projeler" style="padding:clamp(58px,8vw,104px) 0;background:#fff">\n'
            '    <div style="max-width:1200px;margin:0 auto;padding:0 clamp(16px,5vw,40px)">\n'
            '      <div data-reveal style="display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:clamp(28px,4vw,44px)">\n'
            '        <div style="max-width:640px">\n'
            '          <div style="font-weight:600;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#C25E10;margin-bottom:14px">Sahadan</div>\n'
            '          <h2 style="font-family:\'Poppins\',sans-serif;font-weight:700;font-size:clamp(28px,4.4vw,46px);line-height:1.04;letter-spacing:-.025em;color:#221A12;margin:0 0 12px">Son tamamlanan projeler</h2>\n'
            '          <p style="font-size:clamp(15px,1.7vw,17.5px);line-height:1.6;color:#6E6256;margin:0">Kurduğumuz çadırları sahadan fotoğraflarla paylaşıyoruz; her proje gerçek bir teslimattır.</p>\n'
            '        </div>\n'
            '        <a href="projeler/" class="lnk-u" style="font-weight:600;font-size:15.5px;color:#C25E10;white-space:nowrap">Tüm projeler →</a>\n'
            '      </div>\n'
            '      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,300px),1fr));gap:18px;max-width:%s">%s</div>\n'
            '    </div>\n'
            '  </section>\n  ') % ("420px" if len(recs) == 1 else "none", cards)

def patch_home(recs):
    p = os.path.join(PROJ, "index.html")
    s = open(p, encoding="utf-8").read()
    blok = home_section(recs)
    if "<!-- PROJELER:BASLA -->" in s:
        s = re.sub(r'<!-- PROJELER:BASLA -->.*?<!-- PROJELER:BITIR -->',
                   lambda m: '<!-- PROJELER:BASLA -->%s<!-- PROJELER:BITIR -->' % blok, s, flags=re.S)
    else:
        isaret = '  <!-- ===== REFERANSLAR ===== -->'
        s = s.replace(isaret, '<!-- PROJELER:BASLA -->%s<!-- PROJELER:BITIR -->\n\n%s' % (blok, isaret), 1)
    open(p, "w", encoding="utf-8").write(s)
    print("ana sayfa: 'Son tamamlanan projeler' şeridi güncellendi (%d kart)" % min(3, len(recs)))

def patch_sitemap(recs):
    p = os.path.join(PROJ, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'\s*<url><loc>[^<]*?/projeler/[^<]*</loc>.*?</url>', '', s)
    last = max(r["date"] for r in recs) if recs else "2026-07-10"
    entry = '<url><loc>%s/projeler/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq></url>' % (SITE, last)
    s = s.replace('</urlset>', entry + '\n</urlset>')
    open(p, "w", encoding="utf-8").write(s)
    print("sitemap: /projeler/ (lastmod %s)" % last)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(GELEN, exist_ok=True)
    ingest()
    recs = load()
    counts = {r["slug"]: len(photos(r)) for r in recs}
    open(os.path.join(GELEN, "index.html"), "w", encoding="utf-8").write(hub_page(recs, counts))
    patch_home(recs)
    patch_sitemap(recs)
    print("projeler: %d proje, %d fotoğraf yayında" % (len(recs), sum(counts.values())))
