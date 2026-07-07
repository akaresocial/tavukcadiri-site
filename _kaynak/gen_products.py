# -*- coding: utf-8 -*-
# Gerçek DEHA Çadır verisiyle: ölçü + yalıtım(3/4 kat) + fiyat. Marka nötr (Tavuk Çadırı).
import os, html, json
PROJ="/Volumes/ABDURRAHMAN/APP/Tavuk Çadırı"
SCR="/private/tmp/claude-501/-Volumes-ABDURRAHMAN-APP-Tavuk--ad-r-/c4778228-16bc-4e77-b9dd-f19e5b0e793d/scratchpad"
SITE="https://tavukcadiri.com"
WA="905526663606"
def e(t): return html.escape(str(t),quote=True)

WA_SVG='<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="{f}" aria-hidden="true"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm5.8 14.06c-.24.68-1.42 1.31-1.96 1.36-.5.05-.95.23-3.2-.67-2.7-1.07-4.42-3.84-4.55-4.02-.13-.18-1.1-1.46-1.1-2.79 0-1.33.7-1.98.94-2.25.24-.27.53-.34.7-.34.18 0 .35 0 .5.01.16.01.38-.06.59.45.24.59.81 2.04.88 2.19.07.15.12.32.02.5-.09.18-.14.29-.27.45-.14.16-.29.34-.41.46-.14.14-.28.29-.12.56.16.27.71 1.17 1.53 1.9 1.05.94 1.94 1.23 2.21 1.37.27.14.43.12.59-.07.16-.18.68-.79.86-1.06.18-.27.36-.22.6-.13.24.09 1.55.73 1.82.86.27.13.45.2.51.31.07.11.07.63-.17 1.31z"></path></svg>'
CHECK='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2E5A2C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex:none;margin-top:2px"><path d="M20 6 9 17l-5-5"></path></svg>'

# ---- REAL DATA ----
# (en, boy, m2, tavuk~7/m2, 3kat fiyat, 4kat fiyat)
SIZES=[
 ("7","10",70,500,95000,105000),
 ("7","14",98,680,110000,135000),
 ("7","20",140,980,185000,195000),
 ("7","30",210,1470,235000,270000),
 ("10","20",200,1400,225000,265000),
 ("10","30",300,2100,325000,395000),
 ("10","40",400,2800,425000,495000),
]
def tl(n): return format(n,",d").replace(",",".")+" TL"

# featured detail pages: slug -> size index
FEAT=[("500-tavukluk-tavuk-cadiri",0),("750-tavukluk-tavuk-cadiri",1),("1000-tavukluk-tavuk-cadiri",2),("2000-tavukluk-tavuk-cadiri",5)]
FEAT_SLUGS=[f[0] for f in FEAT]

SPECS=[
 ("İskelet","40x40 mm / 2 mm et kalınlığı galvaniz profil, makaslı (kemerli) sistem"),
 ("Dayanım","Standart çadırlara göre 3 kat daha dayanıklı — kar, tipik rüzgâr ve yağmura karşı; yıkılma/çökme yapmaz"),
 ("Dış örtü","650 g/m² TSE damgalı branda (su geçirmez, dayanıklı)"),
 ("İç astar","180 g antibakteriyel, yıkanabilir astar (hijyenik iç ortam)"),
 ("Yalıtım","Alüminyum bizafol yalıtım — 3 kat veya 4 kat seçenek (sıcak/soğuktan koruma)"),
 ("Montaj","Hafif sistem, her zemine montaj"),
 ("Nakliye + Kurulum","Türkiye geneli 81 il — fiyata dahil"),
 ("Teslim","Sipariş sonrası 10 gün içinde kurulu teslim"),
 ("Garanti","2 yıl üretim garantisi"),
 ("Üretim","Özel ölçü ve imalattan halka satış"),
]
EQUIP=[
 ("Yemlik","Otomatik veya manuel yemleme hattı"),
 ("Nipel suluk","Hijyenik nipel suluk sistemi"),
 ("Folluk","Yumurtlama için folluk bölmeleri"),
 ("Havalandırma","Fan ve havalandırma çözümleri"),
]
FEATURES=[
 ("wind","Rüzgâra dayanıklı","Standart çadırlara göre 3 kat daha dayanıklı; kar, tipik rüzgâr ve yağmurda yıkılma/çökme yapmaz."),
 ("frame","Sağlam iskelet","40x40 / 2 mm profil makas sistemiyle güçlü, taşıyıcı galvaniz iskelet."),
 ("shield","Hijyenik iç ortam","180 g antibakteriyel, yıkanabilir astar; kolay temizlenen sağlıklı iç yüzey."),
 ("thermo","Isı yalıtımı","Alüminyum bizafol yalıtım (3/4 kat) ile yazın serin, kışın sıcak dengeli ortam."),
 ("layers","650 g TSE branda","Su geçirmez, TSE damgalı dış örtü; uzun ömürlü ve dayanıklı."),
 ("badge","2 yıl garanti","Üretim kaynaklı hatalara karşı 2 yıl üretim garantisi; uzun ömürlü kullanım."),
]
FEAT_ICON={
 "wind":'<path d="M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2M17.6 7.4A2 2 0 1 1 19 11H2"/>',
 "frame":'<path d="M3 21l9-15 9 15z"/>',
 "shield":'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
 "thermo":'<path d="M14 14.76V5a2 2 0 0 0-4 0v9.76a4 4 0 1 0 4 0z"/>',
 "layers":'<path d="M12 2 2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>',
 "badge":'<path d="M12 15l-3.5 2 1-4L6 10l4-.5L12 6l2 3.5 4 .5-3.5 3 1 4z"/>',
}

CSS=open(os.path.join(SCR,"_prodcss.txt"),encoding="utf-8").read() if os.path.exists(os.path.join(SCR,"_prodcss.txt")) else ""
# fallback: inline CSS (base + product)
if not CSS:
 CSS = """__CSS__"""

def header(links_extra=""):
    L=[("Modeller","../index.html#modeller"),("Fiyatlar","../fiyatlar/"),("Özellikler","../index.html#ozellikler"),("Neden Biz","../index.html#referanslar"),("S.S.S.","../index.html#sss"),("Blog","../blog/"),("İletişim","../iletisim/")]
    nav="".join('<a href="%s">%s</a>'%(u,e(t)) for t,u in L)
    mob="".join('<a href="%s">%s</a>'%(u,e(t)) for t,u in L)
    return ('<header><div class="nav"><a href="../index.html" aria-label="Tavuk Çadırı ana sayfa"><img src="../assets/logo.png" alt="Tavuk Çadırı" style="height:52px;width:auto"></a>'
      '<nav class="nav-links">%s</nav>'
      '<div class="nav-cta"><a href="https://wa.me/%s" target="_blank" rel="noopener" class="wa-btn">%s<span>Teklif al</span></a>'
      '<button id="nav-burger" class="burger" aria-label="Menü" aria-expanded="false" aria-controls="mobile-menu"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"></path></svg></button></div>'
      '<div id="mobile-menu">%s</div></div></header>')%(nav,WA,WA_SVG.format(w=18,f="#fff"),mob)

def footer():
    prod="".join('<li><a href="../%s/">%s</a></li>'%(s,e(t)) for s,t in [("500-tavukluk-tavuk-cadiri","500 Tavuk / 70 m²"),("750-tavukluk-tavuk-cadiri","750 Tavuk / 98 m²"),("1000-tavukluk-tavuk-cadiri","1.000 Tavuk / 140 m²"),("2000-tavukluk-tavuk-cadiri","2.000+ / 300 m²"),("fiyatlar","Tüm ölçüler & fiyatlar")])
    return ('<footer><div class="wrap"><div class="foot-grid">'
      '<div><img src="../assets/logo.png" alt="Tavuk Çadırı" style="width:150px"><p class="about">3 ve 4 kat yalıtımlı, TSE damgalı brandalı anahtar teslim tavuk çadırı. Türkiye geneli 81 ile nakliye ve kurulum. Üretim: DEHA Çadır.</p>'
      '<a href="https://wa.me/%s" target="_blank" rel="noopener" class="wa-btn" style="font-size:14.5px;padding:11px 17px">%s<span>Bize ulaşın</span></a></div>'
      '<div><h5>Ürünler</h5><ul>%s</ul></div>'
      '<div><h5>Kurumsal</h5><ul><li><a href="../hakkimizda/">Hakkımızda</a></li><li><a href="../iletisim/">İletişim</a></li><li><a href="../kurulum-bolgeleri/">Kurulum Bölgeleri</a></li><li><a href="../index.html#sss">S.S.S.</a></li><li><a href="../blog/">Blog</a></li></ul></div>'
      '<div><h5>Yasal</h5><ul><li><a href="../kvkk/">KVKK Aydınlatma Metni</a></li><li><a href="../gizlilik/">Gizlilik &amp; Çerez Politikası</a></li></ul></div>'
      '</div><div class="foot-bottom"><span>© 2026 Tavuk Çadırı. Tüm hakları saklıdır.</span><span>Üretim &amp; kurulum: DEHA Çadır · 81 il</span></div></div></footer>')%(WA,WA_SVG.format(w=17,f="#fff"),prod)

COOKIE=''
JS=("""(function(){var b=document.getElementById('nav-burger'),m=document.getElementById('mobile-menu'),o=false;
function tg(){o=!o;if(!m)return;if(b)b.setAttribute('aria-expanded',o?'true':'false');if(o){m.style.display='flex';requestAnimationFrame(function(){m.style.opacity='1';m.style.transform='translateY(0)';var f=m.querySelector('a');if(f)f.focus();});}else{m.style.opacity='0';m.style.transform='translateY(-8px)';setTimeout(function(){if(!o)m.style.display='none';},230);}}
if(b)b.addEventListener('click',tg);if(m)m.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){if(o)tg();});});
document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&o){tg();if(b)b.focus();}});
var h=document.querySelector('header');window.addEventListener('scroll',function(){if(h)h.style.boxShadow=window.scrollY>14?'0 10px 30px -22px rgba(34,26,18,.5)':'none';},{passive:true});
})();
""")

def doc(title,desc,canon_slug,body,jsonld="",img_num="1000"):
    return ('<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
      '<title>%s</title><meta name="description" content="%s"><meta name="robots" content="index,follow"><link rel="canonical" href="%s/%s/">'
      '<meta property="og:type" content="product"><meta property="og:site_name" content="Tavuk Çadırı"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s/%s/"><meta property="og:image" content="%s/assets/photos/og/og-%s.jpg?v=2"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="tr_TR"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="%s/assets/photos/og/og-%s.jpg?v=2">'
      '<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png"><link rel="icon" type="image/png" sizes="512x512" href="../assets/favicon.png"><link rel="apple-touch-icon" href="../assets/apple-touch-icon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
      '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Hanken+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"><style>%s</style>%s'
      '<!-- Google tag (gtag.js) --><script async src="https://www.googletagmanager.com/gtag/js?id=G-RES77XE6HP"></script>'
      '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-RES77XE6HP");'
      'document.addEventListener("click",function(ev){var a=ev.target&&ev.target.closest?ev.target.closest("a"):null;if(!a)return;var h=a.href||"";'
      'if(h.indexOf("wa.me")>-1){gtag("event","whatsapp_click",{link_url:h});}else if(h.indexOf("tel:")===0){gtag("event","phone_click",{link_url:h});}});</script></head>'
      '<body><a href="#main" class="skip">İçeriğe geç</a>%s<main id="main">%s</main>%s%s<script>%s</script></body></html>')%(
      e(title),e(desc),SITE,canon_slug,e(title),e(desc),SITE,canon_slug,SITE,img_num,SITE,img_num,CSS,
      ('<script type="application/ld+json">%s</script>'%jsonld if jsonld else ''),
      header(),body,footer(),COOKIE,JS)

def price_box(m2,p3,p4):
    return ('<div class="pricebox"><div class="pb"><div class="pb-t">3 Kat Yalıtımlı</div><div class="pb-p">%s</div><div class="pb-s">%d m² · anahtar teslim</div></div>'
      '<div class="pb pb-hot"><span class="pb-badge">Daha güçlü yalıtım</span><div class="pb-t">4 Kat Yalıtımlı</div><div class="pb-p">%s</div><div class="pb-s">%d m² · sert iklim için</div></div></div>'
      '<p class="pb-note">Fiyatlara nakliye ve kurulum dahildir. Ölçüye özel ve diğer boyutlar için <a href="../fiyatlar/">tüm fiyat tablosuna</a> bakın veya WhatsApp’tan yazın.</p>')%(tl(p3),m2,tl(p4),m2)

def specs_table():
    return '<table class="specs"><tbody>%s</tbody></table>'%("".join('<tr><td class="k">%s</td><td class="v">%s</td></tr>'%(e(k),e(v)) for k,v in SPECS))

def equip_list():
    return "".join('<div class="it">%s<div><strong>%s</strong> — %s</div></div>'%(CHECK,e(n),e(d)) for n,d in EQUIP)

def features_grid():
    def fc(f):
        ic='<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#C25E10" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">%s</svg>'%FEAT_ICON[f[0]]
        return '<div class="fcard"><span class="fic">%s</span><h3>%s</h3><p>%s</p></div>'%(ic,e(f[1]),e(f[2]))
    return '<div class="fgrid">%s</div>'%("".join(fc(f) for f in FEATURES))

def faq_block(items):
    return '<div class="faq-list">%s</div>'%("".join('<details class="faq"><summary>%s<svg class="faq-chev" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#C25E10" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex:none"><path d="M6 9l6 6 6-6"></path></svg></summary><div class="ans">%s</div></details>'%(e(q),e(a)) for q,a in items))

def cta_band(txt="Ölçünüz ve bütçenize en uygun tavuk çadırını birlikte planlayalım"):
    return ('<section class="sec"><div class="wrap"><div class="cta-band"><div class="glow"></div><h2>%s</h2>'
      '<p>3 kat mı 4 kat mı, hangi ölçü? Kapasitenizi ve bölgenizi yazın; nakliye ve kurulum dahil net teklifinizi verelim.</p>'
      '<div class="cta-actions"><a href="https://wa.me/%s" target="_blank" rel="noopener" class="wa">%s Ölçüye özel teklif alın</a>'
      '<a href="tel:0%s" class="tel"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>Telefon</a></div></div></div></section>')%(e(txt),WA,WA_SVG.format(w=20,f="#1FA855"),WA[2:])

# ---- DETAIL PAGE ----
def detail_page(slug,idx):
    en,boy,m2,tavuk,p3,p4=SIZES[idx]
    tavuk_f=format(tavuk,',d').replace(",",".")
    num=slug.split("-")[0]
    num_disp="2.000+" if num=="2000" else format(int(num),",d").replace(",",".")
    cap="%s tavuk"%(("2.000+" if num=="2000" else format(int(num),',d').replace(",","."))) if num.isdigit() else "%d tavuk"%tavuk
    title="%s Kapasiteli Tavuk Çadırı (%dx%d = %d m²) Fiyatları | tavukcadiri.com"%(num if num!="2000" else "2000+",int(en),int(boy),m2)
    desc="%s tavukluk (%dx%d, %d m²) yalıtımlı tavuk çadırı. 3 kat %s / 4 kat %s. 40x40 galvaniz makas, 650g TSE branda, 2 yıl garanti; nakliye+kurulum dahil."%(num,int(en),int(boy),m2,tl(p3),tl(p4))
    h1="%s Kapasiteli Tavuk Çadırı"%num_disp
    badges=[("Ölçü","%dx%d m"%(int(en),int(boy))),("Alan","%d m²"%m2),("Kapasite","~%s tavuk"%format(tavuk,',d').replace(",",".")),
            ("3 Kat","%s"%tl(p3)),("4 Kat","%s"%tl(p4)),("Garanti","2 yıl"),("Teslim","10 gün / kurulu"),("Nakliye","81 il — dahil")]
    bd='<div class="badges">%s</div>'%("".join('<div class="badge"><div class="l">%s</div><div class="v">%s</div></div>'%(e(l),e(v)) for l,v in badges))
    crumb='<a href="../index.html">Ana Sayfa</a> › <a href="../index.html#modeller">Tavuk Çadırı Modelleri</a> › <b>%s Tavukluk / %d m²</b>'%(num_disp,m2)
    hero=('<div class="wrap"><div class="crumb">%s</div></div><section class="hero"><div class="wrap"><div class="hero-grid">'
      '<div><div class="ey">Anahtar Teslim Kümes Çadırı · %dx%d m · %d m²</div><h1>%s</h1>'
      '<p class="lead">Yaklaşık %s tavuk için %d m² yalıtımlı, anahtar teslim kümes çadırı. Galvaniz makas iskelet, TSE damgalı branda ve 3-4 kat bizafol yalıtımla üretilir; nakliye ve kurulum dahil, 10 günde kurulu teslim.</p>'
      '%s<div class="actions"><a href="https://wa.me/%s" target="_blank" rel="noopener" class="btn-wa">%s Bu ürünü sorun</a><a href="#fiyat" class="btn-ghost">Fiyat &amp; detay</a></div></div>'
      '<div><img class="hero-img" src="../assets/photos/model-%s.webp?v=2" alt="%s"><div class="pgal"><img src="../assets/photos/tech-1.webp?v=2" loading="lazy" alt="%s kapasiteli tavuk çadırı — iç mekan"><img src="../assets/photos/tech-2.webp?v=2" loading="lazy" alt="%s kapasiteli tavuk çadırı — yakın çekim"><img src="../assets/photos/tech-3.webp?v=2" loading="lazy" alt="%s kapasiteli tavuk çadırı — iç görünüm"></div></div></div></div></section>')%(crumb,int(en),int(boy),m2,e(h1),num_disp,m2,bd,WA,WA_SVG.format(w=20,f="#fff"),num,e(h1),num,num,num)
    # kapasite açıklaması (per-size unique intro)
    who={"500":"Yeni başlayan ve yarı-ticari üreticiler için en uygun başlangıç ölçüsü.","750":"Küçük kümesini büyütmek isteyen üreticiler için dengeli orta ölçü.","1000":"Ticari yumurta/et üretimine geçenlerin en çok tercih ettiği ölçü.","2000":"Büyük ölçekli, ciddi ticari üretim için geniş kapasiteli model."}.get(num,"")
    body=(hero
      +'<section class="sec" id="fiyat"><div class="wrap"><div class="sec-head"><div class="ey">Fiyat</div><h2>%s Tavukluk (%d m²) Fiyatları</h2></div>%s</div></section>'%(num_disp,m2,price_box(m2,p3,p4))
      +'<section class="sec alt"><div class="wrap"><div class="prose">'
      +'<div class="block"><h2>Bu ölçü kime uygun?</h2><p>%s %d m²’lik kapalı alan, barınak içi standart yoğunlukla (m²’ye ~7 tavuk) yaklaşık %s tavuğu doğru şekilde barındırır. Serbest/gezen sistemde bu çadır, tavukların gecelediği ve yumurtladığı korunaklı barınak olarak kullanılır.</p></div>'%(who,m2,format(tavuk,',d').replace(",","."))
      +'<div class="block"><h2>3 kat mı, 4 kat yalıtım mı?</h2><p>Her iki seçenekte de alüminyum bizafol yalıtım kullanılır; fark katman sayısındadır. <strong>3 kat</strong> çoğu bölge için yeterli, dengeli bir çözümdür (%s). <strong>4 kat</strong>, sert kış/aşırı sıcak bölgelerde ekstra ısı yalıtımı sağlar (%s). Bölgenizin iklimine göre birlikte seçelim.</p></div>'%(tl(p3),tl(p4))
      +'<div class="block"><h2>Neden dayanıklı?</h2><p>Taşıyıcı iskelet 40x40 mm / 2 mm et kalınlığında galvaniz profil makas (kemerli) sistemdir; standart çadırlara göre 3 kat daha dayanıklıdır. Kar yükü, tipik rüzgâr ve yağmura karşı yıkılma/çökme yapmaz. Dış örtü 650 g/m² TSE damgalı branda, iç yüzey 180 g antibakteriyel yıkanabilir astardır — hem sağlam hem hijyenik.</p></div>'
      +'<div class="block"><h2>Nakliye, kurulum ve teslim</h2><p>Türkiye’nin 81 iline hizmet veriyoruz; nakliye ve kurulum fiyata dahildir. Hafif sistem her zemine monte edilebilir. Sipariş sonrası <strong>10 gün içinde kurulu şekilde</strong> teslim ediyoruz. Ürün <strong>2 yıl üretim garantilidir</strong>; üretim kaynaklı hatalar kapsamdadır (doğal afet ve kullanıcı hataları hariç).</p></div>'
      +'<div class="block"><h2>İsteğe bağlı ekipman</h2><p>Barınağı, talebinize göre iç ekipmanla birlikte teslim edebiliriz; ihtiyacınıza göre birlikte belirleyelim.</p><div class="equip">%s</div></div>'%equip_list()
      +'</div></div></section>'
      +'<section class="sec"><div class="wrap"><div class="sec-head"><div class="ey">Teknik Künye</div><h2>Teknik Özellikler</h2></div>%s</div></section>'%specs_table()
      +'<section class="sec alt"><div class="wrap"><div class="sec-head"><div class="ey">Öne çıkanlar</div><h2>Öne Çıkan Özellikler</h2></div>%s</div></section>'%features_grid()
      +'<section class="sec"><div class="wrap"><div class="sec-head"><div class="ey">Sıkça sorulanlar</div><h2>Merak Edilenler</h2></div>%s</div></section>'%faq_block([
         ("%s tavukluk çadır kaç m²?"%num_disp,"%d m² (%dx%d m). Barınak içi standart yoğunlukla ~%s tavuk kapasitelidir."%(m2,int(en),int(boy),format(tavuk,',d').replace(",","."))),
         ("Fiyata neler dahil?","3 kat yalıtımlı %s, 4 kat yalıtımlı %s. Her iki fiyata da nakliye ve kurulum dahildir; zemin, su ve elektrik altyapısı hariçtir."%(tl(p3),tl(p4))),
         ("3 kat ve 4 kat farkı nedir?","4 kat yalıtım, ekstra bir katmanla soğuk/sıcak yalıtımını güçlendirir; sert iklim bölgeleri için önerilir. 3 kat çoğu bölge için yeterlidir."),
         ("Çadır ne kadar dayanıklı, garanti var mı?","40x40/2 mm galvaniz makas iskelet ve 650 g TSE brandayla standart çadırlardan 3 kat dayanıklıdır; kar/rüzgâr/yağmurda çökme yapmaz. 2 yıl üretim garantilidir."),
         ("Ne kadar sürede teslim edilir?","Sipariş sonrası 10 gün içinde, kurulu şekilde teslim edilir. Türkiye geneli 81 ile kurulum yapıyoruz."),
         ("Zemin beton mu olmalı?","Hafif sistem her zemine monte edilir; beton şart değildir. Temizlik kolaylığı için beton veya kilit taşı öneririz."),
       ])
      +'<section class="sec alt"><div class="wrap"><div class="sec-head"><div class="ey">Diğer ölçüler</div><h2>İlgili Ölçüler &amp; Fiyatlar</h2></div><div class="rel">%s</div></div></section>'%(
         "".join('<a href="../%s/">%s <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#C25E10" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"></path></svg></a>'%(fs, e(dict([("500-tavukluk-tavuk-cadiri","500 Tavuk / 70 m²"),("750-tavukluk-tavuk-cadiri","750 Tavuk / 98 m²"),("1000-tavukluk-tavuk-cadiri","1.000 Tavuk / 140 m²"),("2000-tavukluk-tavuk-cadiri","2.000+ / 300 m²")])[fs])) for fs in FEAT_SLUGS if fs!=slug)
         + '<a href="../fiyatlar/">Tüm ölçüler &amp; fiyat tablosu <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#C25E10" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"></path></svg></a>')
      +cta_band())
    # JSON-LD with Offer price (3 kat as low price)
    faqld=[{"@type":"Question","name":"%s tavukluk çadır kaç m²?"%num_disp,"acceptedAnswer":{"@type":"Answer","text":"%d m² (%dx%d m), ~%s tavuk kapasiteli."%(m2,int(en),int(boy),tavuk_f)}},
           {"@type":"Question","name":"%s kapasiteli tavuk çadırı fiyatı ne kadar?"%num_disp,"acceptedAnswer":{"@type":"Answer","text":"3 kat yalıtımlı %s, 4 kat yalıtımlı %s; nakliye ve kurulum dahil."%(tl(p3),tl(p4))}}]
    graph={"@context":"https://schema.org","@graph":[
     {"@type":"Product","name":h1,"description":desc,"image":"%s/assets/photos/model-%s.jpg"%(SITE,num),"category":"Tavuk Çadırı / Kümes Çadırı","brand":{"@type":"Brand","name":"Tavuk Çadırı"},
      "offers":{"@type":"AggregateOffer","priceCurrency":"TRY","lowPrice":p3,"highPrice":p4,"offerCount":2,"availability":"https://schema.org/InStock","url":"%s/%s/"%(SITE,slug)},
      "additionalProperty":[{"@type":"PropertyValue","name":"Ölçü","value":"%dx%d m"%(int(en),int(boy))},{"@type":"PropertyValue","name":"Alan","value":"%d m²"%m2},{"@type":"PropertyValue","name":"Kapasite","value":"~%s tavuk"%tavuk_f},{"@type":"PropertyValue","name":"İskelet","value":"40x40/2mm galvaniz makas"},{"@type":"PropertyValue","name":"Branda","value":"650 g TSE"},{"@type":"PropertyValue","name":"Garanti","value":"2 yıl"}]},
     {"@type":"FAQPage","mainEntity":faqld},
     {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Ana Sayfa","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Tavuk Çadırı Modelleri","item":SITE+"/#modeller"},{"@type":"ListItem","position":3,"name":"%s Tavukluk / %d m²"%(num_disp,m2),"item":"%s/%s/"%(SITE,slug)}]}
    ]}
    return doc(title,desc,slug,body,json.dumps(graph,ensure_ascii=False,separators=(",",":")),img_num=num)

# ---- FIYATLAR PAGE ----
def price_table(kat):
    i2s={0:"500-tavukluk-tavuk-cadiri",1:"750-tavukluk-tavuk-cadiri",2:"1000-tavukluk-tavuk-cadiri",5:"2000-tavukluk-tavuk-cadiri"}
    rows=""
    for i,(en,boy,m2,tavuk,p3,p4) in enumerate(SIZES):
        olc="%dx%d m"%(int(en),int(boy))
        cell=('<a href="../%s/">%s</a>'%(i2s[i],olc)) if i in i2s else olc
        rows+='<tr><td>%s</td><td>%d m²</td><td>~%s</td><td class="pr">%s</td></tr>'%(cell,m2,format(tavuk,',d').replace(",","."),tl(p3 if kat==3 else p4))
    return '<table class="ptable"><thead><tr><th>Ölçü</th><th>Alan</th><th>Kapasite</th><th>Fiyat</th></tr></thead><tbody>%s</tbody></table>'%rows

def fiyatlar_page():
    title="Tavuk Çadırı Fiyatları 2026 — 3 & 4 Kat Yalıtımlı Ölçü Tablosu | tavukcadiri.com"
    desc="Tavuk çadırı fiyatları: 7x10’dan 10x40’a tüm ölçüler, 3 kat ve 4 kat yalıtımlı. 70 m² 95.000 TL’den başlayan; nakliye + kurulum dahil, 81 il, 10 gün teslim, 2 yıl garanti."
    crumb='<a href="../index.html">Ana Sayfa</a> › <b>Fiyatlar</b>'
    body=('<div class="wrap"><div class="crumb">%s</div></div><section class="phead"><div class="wrap"><div class="ey">Şeffaf Fiyat</div><h1>Tavuk Çadırı Fiyatları (2026)</h1><p>Ölçü ve yalıtım seviyesine göre güncel fiyatlarımız. Tüm fiyatlara <strong>nakliye ve kurulum dahildir</strong>; Türkiye geneli 81 ile hizmet, 10 gün içinde kurulu teslim, 2 yıl üretim garantisi.</p></div></section>'%crumb
      +'<section class="sec" style="padding:clamp(24px,3vw,34px) 0 0"><div class="wrap"><p style="font-size:15px;color:#6E6256;margin:0">Öne çıkan ölçüler için detay sayfaları: <a class="lnk-u" style="color:#C25E10;font-weight:600" href="../500-tavukluk-tavuk-cadiri/">500</a> · <a class="lnk-u" style="color:#C25E10;font-weight:600" href="../750-tavukluk-tavuk-cadiri/">750</a> · <a class="lnk-u" style="color:#C25E10;font-weight:600" href="../1000-tavukluk-tavuk-cadiri/">1.000</a> · <a class="lnk-u" style="color:#C25E10;font-weight:600" href="../2000-tavukluk-tavuk-cadiri/">2.000+</a> tavukluk</p></div></section>'
      +'<section class="sec"><div class="wrap"><div class="sec-head"><div class="ey">3 Kat Yalıtımlı</div><h2>3 Kat Yalıtımlı Çadır Fiyatları</h2><p style="color:#6E6256;margin:8px 0 0">Çoğu bölge için dengeli ve ekonomik çözüm.</p></div>%s</div></section>'%price_table(3)
      +'<section class="sec alt"><div class="wrap"><div class="sec-head"><div class="ey">4 Kat Yalıtımlı</div><h2>4 Kat Yalıtımlı Çadır Fiyatları</h2><p style="color:#6E6256;margin:8px 0 0">Sert kış / aşırı sıcak bölgeler için ekstra yalıtım katmanı.</p></div>%s</div></section>'%price_table(4)
      +'<section class="sec"><div class="wrap"><div class="prose">'
      +'<div class="block"><h2>Fiyata neler dahil?</h2><p><strong>Dahil:</strong> 40x40/2 mm galvaniz makaslı iskelet, 650 g TSE damgalı branda, 180 g antibakteriyel astar, alüminyum bizafol yalıtım (3 veya 4 kat), Türkiye geneli nakliye ve yerinde kurulum. <strong>Hariç:</strong> zemin (beton/kilit taşı vb.), su ve elektrik altyapısı.</p></div>'
      +'<div class="block"><h2>Ölçüye özel üretim</h2><p>Tablodaki ölçülerin dışında ihtiyacınıza özel ölçülerde de imalat yapıyoruz (imalattan halka satış). Farklı en/boy veya ek ekipman için WhatsApp’tan yazın; ölçünüze göre net fiyat çıkaralım.</p></div>'
      +'<div class="block"><h2>Kapasite nasıl hesaplanır?</h2><p>Barınak içi standart yoğunluk m²’ye yaklaşık 7 tavuktur; tablodaki kapasiteler buna göredir. Serbest/gezen sistemde hayvan başına daha fazla alan önerildiğinden kapasite düşer — sisteminize göre birlikte planlayalım.</p></div>'
      +'</div></div></section>'
      +cta_band("Ölçünüze ve bölgenize göre net fiyat alın"))
    faqld=[{"@type":"Question","name":"Tavuk çadırı fiyatları ne kadar?","acceptedAnswer":{"@type":"Answer","text":"70 m² (7x10) 3 kat yalıtımlı 95.000 TL’den başlar; 4 kat 105.000 TL. Ölçü büyüdükçe fiyat artar (10x40 400 m²’ye kadar). Tüm fiyatlara nakliye ve kurulum dahildir."}},
           {"@type":"Question","name":"Fiyata nakliye ve kurulum dahil mi?","acceptedAnswer":{"@type":"Answer","text":"Evet, tüm fiyatlara Türkiye geneli nakliye ve yerinde kurulum dahildir. Zemin, su ve elektrik altyapısı hariçtir."}}]
    graph={"@context":"https://schema.org","@graph":[
     {"@type":"FAQPage","mainEntity":faqld},
     {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Ana Sayfa","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Fiyatlar","item":SITE+"/fiyatlar/"}]}]}
    return doc(title,desc,"fiyatlar",body,json.dumps(graph,ensure_ascii=False,separators=(",",":")))

# ---- WRITE ----
for slug,idx in FEAT:
    d=detail_page(slug,idx)
    for base in (PROJ,SCR):
        os.makedirs(os.path.join(base,slug),exist_ok=True)
        open(os.path.join(base,slug,"index.html"),"w",encoding="utf-8").write(d)
fp=fiyatlar_page()
for base in (PROJ,SCR):
    os.makedirs(os.path.join(base,"fiyatlar"),exist_ok=True)
    open(os.path.join(base,"fiyatlar","index.html"),"w",encoding="utf-8").write(fp)
print("detail:",FEAT_SLUGS,"+ fiyatlar")
