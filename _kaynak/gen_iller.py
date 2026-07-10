# -*- coding: utf-8 -*-
# İl sayfası üreteci: _kaynak/iller/*.json + _kaynak/il_data.json ->
#   /<il>-tavuk-cadiri/index.html (81 sayfa) + /kurulum-bolgeleri/ hub + sitemap güncellemesi
# Tasarım sistemi _kaynak/gen_pages.py'den exec ile alınır (header/footer/CSS/doc senkron kalır).
import os, html, json, re
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)

_src = open(os.path.join(HERE, "gen_pages.py"), encoding="utf-8").read()
exec(_src.split("pages=[]")[0])  # e, SITE, WA, WA_DISP, WA_SVG, CSS, header, footer, doc, phead, cta_block

DATE = "2026-07-07"
DATE_DISP = "7 Temmuz 2026"

# il sayfalarına özel ek CSS (blog'dakiyle uyumlu: faq/rel/bmeta + fiyat kartları)
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
.pmodels{display:grid;grid-template-columns:1fr;gap:14px;margin-top:18px}
.pmodel{background:#fff;border:1px solid #EFE7DA;border-radius:16px;padding:18px 20px;display:flex;flex-direction:column;gap:4px}
.pmodel:hover{border-color:#E5751B}
.pmodel .pm-k{font-family:'Poppins';font-weight:700;font-size:17px;color:#221A12}
.pmodel .pm-m{font-size:13.5px;color:#8B7E6E}
.pmodel .pm-f{font-family:'Poppins';font-weight:700;font-size:16px;color:#C25E10;margin-top:6px}
.pmodel .pm-f small{font-weight:600;font-size:12px;color:#8B7E6E;display:block}
.hubgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.hubgrid a{background:#fff;border:1px solid #ECE3D6;border-radius:12px;padding:11px 14px;font-weight:600;font-size:14.5px;color:#3C342B}
.hubgrid a:hover{border-color:#E5751B;color:#C25E10}
.hubreg h2{font-family:'Poppins';font-weight:700;font-size:clamp(19px,2.4vw,24px);margin:30px 0 14px}
.kunye{background:#fff;border:1px solid #EFE7DA;border-radius:18px;padding:clamp(20px,3vw,30px)}
.kunye h2{font-family:'Poppins';font-weight:700;font-size:clamp(20px,2.6vw,26px);margin:0 0 4px}
.kn-sub{color:#6E6256;font-size:14.5px;margin:0 0 16px;max-width:640px}
.kn-grid{display:grid;grid-template-columns:1fr;gap:0;margin:0}
.kn-row{display:grid;grid-template-columns:140px 1fr;gap:14px;padding:12px 0;border-top:1px solid #F1E9DC}
.kn-grid .kn-row:first-child{border-top:0}
.kn-row dt{font-weight:700;font-size:13.5px;color:#8F5314}
.kn-row dd{margin:0;font-size:15px;color:#4C443A;line-height:1.55}
@media(min-width:680px){.pmodels{grid-template-columns:repeat(4,1fr)}.rel{grid-template-columns:repeat(3,1fr)}.hubgrid{grid-template-columns:repeat(3,1fr)}.kn-grid{grid-template-columns:1fr 1fr;column-gap:36px}.kn-grid .kn-row:nth-child(2){border-top:0}}
@media(min-width:980px){.hubgrid{grid-template-columns:repeat(4,1fr)}}
"""

CSS = CSS + """
.pjc{display:grid;grid-template-columns:1fr;gap:0;background:#fff;border:1px solid #EFE7DA;border-radius:20px;overflow:hidden;margin-top:18px}
.pjc img{width:100%;height:240px;object-fit:cover;display:block}
.pjc .pjc-b{padding:20px 22px 22px}
.pjc .pjc-t{font-family:'Poppins';font-weight:700;font-size:18px;color:#221A12;margin:0 0 6px}
.pjc .pjc-m{font-size:14px;color:#6E6256;margin:0 0 12px;line-height:1.6}
.pjc .pjc-l{display:inline-flex;align-items:center;gap:7px;font-weight:600;font-size:14.5px;color:#C25E10}
@media(min-width:760px){.pjc{grid-template-columns:1.1fr 1fr}.pjc img{height:100%;min-height:230px}.pjc .pjc-b{align-self:center}}
"""

ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#E5751B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'

# Tamamlanan projeler: il sayfasında o ile ait gerçek kurulum kartı çıkar (gen_projeler.py ile senkron)
PROJELER = []
_pj = os.path.join(HERE, "projeler.json")
if os.path.exists(_pj):
    PROJELER = json.load(open(_pj, encoding="utf-8"))
    PROJELER.sort(key=lambda r: r["date"], reverse=True)

def projeler_block(rec):
    pjs = [p for p in PROJELER if p["ilslug"] == rec["ilslug"]]
    if not pjs:
        return ""
    il_loc = pjs[0].get("il_loc", rec["il"])
    cards = ""
    for p in pjs[:2]:
        cards += ('<div class="pjc"><img src="../assets/photos/projeler/%s-1.webp" alt="%s" loading="lazy" width="1000" height="750">'
                  '<div class="pjc-b"><p class="pjc-t">%s — %s Tavuk Çadırı</p>'
                  '<p class="pjc-m">%s · %d m² · %s · nakliye ve kurulum dahil teslim edildi (%s).</p>'
                  '<a class="pjc-l" href="../projeler/#%s">Proje fotoğraflarını gör %s</a></div></div>') % (
                  p["slug"], e(p["alt"]), e(p["ilce"]), e(p["model_ad"]),
                  p["olcu"].replace("x", "×"), p["m2"], e(p["yalitim"]), e(p["date_disp"]), p["slug"], ARROW)
    return ('<section class="sec" style="background:#FBF8F3"><div class="wrap">'
            '<h2 style="font-family:Poppins;font-weight:700;font-size:clamp(22px,3vw,30px);margin:0 0 4px">%s tamamlanan projeler</h2>'
            '<p style="color:#6E6256;margin:0;max-width:720px">Sahadan gerçek kurulum fotoğrafları — tüm kurulumlar için <a href="../projeler/" style="color:#C25E10;font-weight:600">projeler sayfasına</a> bakın.</p>'
            '%s</div></section>') % (e(il_loc), cards)
CHEV = '<svg class="faq-chev" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#C25E10" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex:none"><path d="M6 9l6 6 6-6"></path></svg>'

# Gerçek DEHA fiyatları (3 kat / 4 kat, nakliye+kurulum dahil) — fiyatlar/ sayfasıyla senkron
MODELS = [
    ("500-tavukluk-tavuk-cadiri",  "500 Tavukluk",    "7x10 · 70 m²"),
    ("750-tavukluk-tavuk-cadiri",  "750 Tavukluk",    "7x15 · 105 m²"),
    ("1000-tavukluk-tavuk-cadiri", "1.000 Tavukluk",  "7x20 · 140 m²"),
    ("2000-tavukluk-tavuk-cadiri", "2.000+ Tavukluk", "10x30 · 300 m²"),
]
BLOG_TITLES = {
    "kumes-maliyeti-betonarme-mi-cadir-mi": "Kümes maliyeti: betonarme mi, çadır mı?",
    "500-tavukla-yumurta-isine-baslamak": "500 tavukla yumurta işine başlamak",
    "kumes-icin-ruhsat-gerekir-mi": "Kümes için ruhsat gerekir mi?",
    "tavukculukta-devlet-destegi-ve-hibeler": "Tavukçulukta devlet desteği ve hibeler",
    "kisin-kumes-nasil-sicak-tutulur": "Kışın kümes nasıl sıcak tutulur?",
    "gezen-tavuk-sistemi-kurmak": "Gezen tavuk sistemi kurmak",
    "kumes-zemini-ne-olmali": "Kümes zemini ne olmalı?",
    "tavuk-basina-kac-m2-gerekir": "Tavuk başına kaç m² gerekir?",
    "yumurta-verimini-dusuren-hatalar": "Yumurta verimini düşüren hatalar",
    "cadir-kumes-ne-kadar-dayanikli": "Çadır kümes ne kadar dayanıklı?",
}

ALLOWED = re.compile(r'</?(p|ul|ol|li|strong|em|a|h3|table|thead|tbody|tr|th|td)(\s[^>]*)?>', re.I)
def sanitize(h):
    h = re.sub(r'<script.*?</script>', '', h, flags=re.S | re.I)
    return re.sub(r'<[^>]+>', lambda m: m.group(0) if ALLOWED.match(m.group(0)) else '', h)

def tl(n):  # 95000 -> "95.000"
    return f"{n:,}".replace(",", ".")

def load():
    data = json.load(open(os.path.join(HERE, "il_data.json"), encoding="utf-8"))
    by_slug = {}
    d = os.path.join(HERE, "iller")
    recs = []
    for f in sorted(os.listdir(d)):
        if f.endswith(".json") and not f.startswith("._"):
            rec = json.load(open(os.path.join(d, f), encoding="utf-8"))
            rec["data"] = data[rec["il"]]
            recs.append(rec)
            by_slug[rec["slug"]] = rec
    recs.sort(key=lambda r: r["data"]["plaka"])
    return recs, by_slug

def faq_html(faq):
    return '<div class="faq-list">%s</div>' % "".join(
        '<details class="faq"><summary>%s%s</summary><div class="ans">%s</div></details>' % (e(x["q"]), CHEV, e(x["a"]))
        for x in faq)

def chips(rec):
    d = rec["data"]
    km = d["km_istanbul"]
    items = ["İstanbul'dan ~%s km" % tl(km), "10 günde kurulu teslim", "Nakliye + kurulum dahil",
             "Önerilen yalıtım: %s" % d["yalitim"]]
    return '<div class="bmeta">%s</div>' % "".join("<span>%s</span>" % e(x) for x in items)

def models_block(rec):
    d = rec["data"]; il = rec["il"]
    four = d["yalitim"] == "4 kat"
    both = d["yalitim"] == "3 veya 4 kat"
    cards = ""
    for slug, name, size in MODELS:
        if both:
            s = "3 kat / 4 kat seçeneği · nakliye+kurulum dahil"
        elif four:
            s = "4 kat yalıtımlı · nakliye+kurulum dahil"
        else:
            s = "3 kat yalıtımlı · nakliye+kurulum dahil"
        cards += ('<a class="pmodel" href="../%s/"><span class="pm-k">%s</span><span class="pm-m">%s</span>'
                  '<span class="pm-f">Güncel fiyatı gör →<small>%s</small></span></a>') % (slug, e(name), e(size), e(s))
    return ('<section class="sec" style="background:#FBF8F3"><div class="wrap">'
            '<h2 style="font-family:Poppins;font-weight:700;font-size:clamp(22px,3vw,30px);margin:0 0 4px">%s için modeller</h2>'
            '<p style="color:#6E6256;margin:0;max-width:720px">Fiyatlara nakliye ve kurulum dahildir; %s teslimatı da ücretsizdir. 8 farklı ölçünün tamamı için <a href="../fiyatlar/" style="color:#C25E10;font-weight:600">fiyat tablosuna</a> bakabilirsiniz.</p>'
            '<div class="pmodels">%s</div></div></section>') % (e(il), e(il), cards)

def wa_link(rec):
    return "https://wa.me/%s?text=%s" % (WA, quote(rec["wa_text"]))

def cta_il(rec):
    il = rec["il"]
    return ('<section class="sec"><div class="wrap"><div style="background:linear-gradient(135deg,#2E5A2C,#244A22);border-radius:24px;padding:clamp(28px,4vw,48px);color:#fff;text-align:center">'
            '<h2 style="font-weight:700;font-size:clamp(22px,3vw,32px);margin:0 0 10px">%s projenizi birlikte planlayalım</h2>'
            '<p style="color:#CBD8C7;margin:0 auto 20px;max-width:560px">Kapasitenizi ve kurulumu düşündüğünüz ilçeyi yazın; ölçüyü, yalıtımı ve teklifi aynı gün netleştirelim.</p>'
            '<a href="%s" target="_blank" rel="noopener" class="wa-btn" style="background:#fff;color:#1B3D1A;font-size:16px;padding:14px 24px;border-radius:13px">%s WhatsApp\'tan yazın</a>'
            '</div></div></section>') % (e(il), wa_link(rec), WA_SVG.format(w=19, f="#1FA855"))

KUNYE_ROWS = [
    ("İskelet", "40x40 mm / 2 mm çelik makas profil"),
    ("Branda", "650 g/m² TSE damgalı, UV dayanımlı, alev yürütmez"),
    ("İç astar", "180 g/m² antibakteriyel, yıkanabilir"),
    ("Yalıtım", "Alüminyum bizafol — 3 veya 4 kat"),
    ("Dayanıklılık", "Standart çadırlara göre 3 kat (kar, rüzgâr, yağış)"),
    ("Garanti", "2 yıl üretim garantisi"),
    ("Teslim", "Sipariş sonrası ~10 gün, kurulu"),
    ("Kapasite", "m² başına ~7 tavuk (70 m² ≈ 500 tavuk)"),
]
def kunye_block(il):
    dl = "".join('<div class="kn-row"><dt>%s</dt><dd>%s</dd></div>' % (e(k), e(v)) for k, v in KUNYE_ROWS)
    return ('<section class="sec" style="padding-top:clamp(20px,3vw,32px)"><div class="wrap"><div class="kunye">'
            '<h2>Teknik künye</h2>'
            '<p class="kn-sub">%s dahil 81 ilde aynı üretim standardı; nakliye ve kurulum her ölçüde fiyata dahildir. Ölçü ve yalıtım katı kapasitenize göre belirlenir.</p>'
            '<dl class="kn-grid">%s</dl></div></div></section>') % (e(il), dl)

def il_page(rec, by_slug):
    il = rec["il"]; slug = rec["slug"]; d = rec["data"]
    crumb = '<a href="../index.html">Ana Sayfa</a> › <a href="../kurulum-bolgeleri/">Kurulum Bölgeleri</a> › <b>%s</b>' % e(il)
    hero = ('<div class="wrap"><div class="crumb">%s</div></div>'
            '<section class="phead"><div class="wrap"><div class="ey">%s · Ücretsiz Nakliye ve Kurulum</div>'
            '<h1>%s</h1><p>%s</p>%s</div></section>') % (crumb, e(d["bolge"]), e(rec["h1"]), e(rec["hero_p"]), chips(rec))
    hero += ('<section style="padding:clamp(18px,3vw,30px) 0 0"><div class="wrap">'
             '<img src="../assets/photos/iller/%s.webp" alt="%s" width="1200" height="675" fetchpriority="high" '
             'style="width:100%%;aspect-ratio:16/9;max-height:440px;border-radius:20px;'
             'box-shadow:0 22px 42px -26px rgba(34,26,18,.5);object-fit:cover;display:block"></div></section>') % (rec["ilslug"], e(rec["img_alt"]))
    body_secs = '<section class="sec"><div class="wrap"><div class="prose">' + sanitize(rec["intro_html"])
    for s in rec["sections"]:
        body_secs += '<h2>%s</h2>' % e(s["h2"]) + sanitize(s["html"])
    body_secs += '</div></div></section>'
    faq = ('<section class="sec"><div class="wrap"><h2 style="font-family:Poppins;font-weight:700;font-size:clamp(22px,3vw,30px);margin:0 0 20px">%s için sık sorulanlar</h2>%s</div></section>'
           % (e(il), faq_html(rec["faq"])))
    rel_items = ""
    for rs in rec.get("related_blog", [])[:3]:
        if rs in BLOG_TITLES:
            rel_items += '<a href="../blog/%s/">%s %s</a>' % (rs, e(BLOG_TITLES[rs]), ARROW)
    related = ('<section class="sec" style="background:#FBF8F3;padding-top:clamp(24px,3vw,40px)"><div class="wrap"><h2 style="font-family:Poppins;font-weight:700;font-size:clamp(20px,2.6vw,26px);margin:0 0 18px">İşinize yarayacak rehberler</h2><div class="rel">%s</div></div></section>' % rel_items) if rel_items else ''
    body = hero + body_secs + projeler_block(rec) + models_block(rec) + kunye_block(il) + faq + related + cta_il(rec)
    out = doc(rec["meta_title"], rec["meta_desc"], slug, body, pre="../")
    out = out.replace(SITE + "/assets/photos/og/og-home.jpg", "%s/assets/photos/iller/%s.jpg" % (SITE, rec["ilslug"]))  # og/twitter image → il görseli
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": "%s Tavuk Çadırı Kurulumu" % il,
         "serviceType": "Anahtar teslim tavuk çadırı (çadır kümes) üretim, nakliye ve kurulum",
         "provider": {"@type": "Organization", "name": "Tavuk Çadırı", "url": SITE + "/", "telephone": "+90 552 666 36 06"},
         "areaServed": {"@type": "State", "name": il},
         "url": "%s/%s/" % (SITE, slug),
         "description": rec["meta_desc"],
         "offers": {"@type": "AggregateOffer", "priceCurrency": "TRY", "lowPrice": "99000", "highPrice": "820000",
                    "url": SITE + "/fiyatlar/"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": x["q"], "acceptedAnswer": {"@type": "Answer", "text": x["a"]}} for x in rec["faq"]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Kurulum Bölgeleri", "item": SITE + "/kurulum-bolgeleri/"},
            {"@type": "ListItem", "position": 3, "name": il, "item": "%s/%s/" % (SITE, slug)}]}]}
    out = out.replace('</head>', '<script type="application/ld+json">%s</script></head>' % json.dumps(graph, ensure_ascii=False, separators=(",", ":")), 1)
    return out

REGIONS = ["Marmara", "Ege", "Akdeniz", "İç Anadolu", "Karadeniz", "Doğu Anadolu", "Güneydoğu Anadolu"]

def hub_page(recs):
    crumb = '<a href="../index.html">Ana Sayfa</a> › <b>Kurulum Bölgeleri</b>'
    hero = ('<div class="wrap"><div class="crumb">%s</div></div>'
            '<section class="phead"><div class="wrap"><div class="ey">81 İl · Nakliye ve Kurulum Dahil</div>'
            '<h1>Türkiye\'nin her iline kurulum</h1>'
            '<p>Üretimimiz İstanbul\'da; nakliye ve montaj ekibimiz 81 ilin tamamına gidiyor, ikisi de fiyata dahil. '
            'Aşağıdan ilinizi seçin: o ilin iklimine göre yalıtım önerisini, nakliye süresini ve güncel fiyatları bir arada bulursunuz.</p></div></section>') % crumb
    groups = ""
    for reg in REGIONS:
        rs = [r for r in recs if r["data"]["bolge"] == reg]
        if not rs:
            continue
        links = "".join('<a href="../%s/">%s</a>' % (r["slug"], e(r["il"])) for r in rs)
        groups += '<div class="hubreg"><h2>%s</h2><div class="hubgrid">%s</div></div>' % (e(reg), links)
    body = (hero + '<section class="sec"><div class="wrap">' + groups + '</div></section>'
            + '<section class="sec" style="background:#FBF8F3"><div class="wrap"><div class="prose">'
            + '<h2>Şubemiz yok; işi tek merkezden doğru yapıyoruz</h2>'
            + '<p>Çadırınız İstanbul\'daki üretim tesisimizde ölçünüze göre dikiliyor, kamyonla adresinize geliyor ve kurulumu bizim ekibimiz yapıyor. '
            + 'Bu sayede her ilde aynı malzeme, aynı işçilik ve aynı 2 yıl garanti geçerli. Sipariş sonrası standart teslim süremiz kurulum dahil yaklaşık 10 gündür; '
            + 'yoğunluğa ve mesafeye göre gün netleşir, tarihi baştan birlikte planlarız.</p>'
            + '<p>Fiyat her ilde aynıdır: <a href="../fiyatlar/">fiyat tablosundaki</a> rakamlara nakliye ve kurulum dahildir, il için ek ücret çıkmaz. '
            + 'Zemin hazırlığı, su ve elektrik aboneliği ise her yerde olduğu gibi alıcıya aittir.</p>'
            + '</div></div></section>' + cta_block())
    out = doc("Kurulum Bölgeleri — 81 İle Nakliye ve Kurulum Dahil | Tavuk Çadırı",
              "Tavuk çadırında 81 ilin tamamına ücretsiz nakliye ve kurulum. İlinizi seçin; iklime göre yalıtım önerisi, teslim süresi ve güncel fiyatları görün.",
              "kurulum-bolgeleri", body, pre="../")
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Kurulum Bölgeleri", "url": SITE + "/kurulum-bolgeleri/", "inLanguage": "tr-TR",
         "description": "Tavuk çadırı kurulumu yapılan 81 ilin listesi."},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Kurulum Bölgeleri", "item": SITE + "/kurulum-bolgeleri/"}]}]}
    out = out.replace('</head>', '<script type="application/ld+json">%s</script></head>' % json.dumps(graph, ensure_ascii=False, separators=(",", ":")), 1)
    return out

def patch_sitemap(recs):
    p = os.path.join(PROJ, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'\s*<url><loc>[^<]*?/kurulum-bolgeleri/[^<]*</loc>.*?</url>', '', s)
    s = re.sub(r'\s*<url><loc>[^<]*?-tavuk-cadiri/</loc>.*?</url>',
               lambda m: m.group(0) if "tavukluk" in m.group(0) else "", s)
    entries = '<url><loc>%s/kurulum-bolgeleri/</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq></url>' % (SITE, DATE)
    for rec in recs:
        entries += '<url><loc>%s/%s/</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq></url>' % (SITE, rec["slug"], DATE)
    s = s.replace('</urlset>', entries + '\n</urlset>')
    open(p, "w", encoding="utf-8").write(s)
    print("sitemap: +%d il url + hub" % len(recs))

if __name__ == "__main__":
    recs, by_slug = load()
    os.makedirs(os.path.join(PROJ, "kurulum-bolgeleri"), exist_ok=True)
    open(os.path.join(PROJ, "kurulum-bolgeleri", "index.html"), "w", encoding="utf-8").write(hub_page(recs))
    for rec in recs:
        d = os.path.join(PROJ, rec["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(il_page(rec, by_slug))
    patch_sitemap(recs)
    print("iller: hub + %d il sayfası üretildi" % len(recs))
