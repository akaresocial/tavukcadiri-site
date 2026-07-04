# -*- coding: utf-8 -*-
import os, html, json
PROJ="/Volumes/ABDURRAHMAN/APP/Tavuk Çadırı"
SCR="/private/tmp/claude-501/-Volumes-ABDURRAHMAN-APP-Tavuk--ad-r-/c4778228-16bc-4e77-b9dd-f19e5b0e793d/scratchpad"
SITE="https://tavukcadiri.com"
WA="905526663606"
WA_DISP="0552 666 36 06"
def e(t): return html.escape(str(t),quote=True)

WA_SVG='<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="{f}" aria-hidden="true"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm5.8 14.06c-.24.68-1.42 1.31-1.96 1.36-.5.05-.95.23-3.2-.67-2.7-1.07-4.42-3.84-4.55-4.02-.13-.18-1.1-1.46-1.1-2.79 0-1.33.7-1.98.94-2.25.24-.27.53-.34.7-.34.18 0 .35 0 .5.01.16.01.38-.06.59.45.24.59.81 2.04.88 2.19.07.15.12.32.02.5-.09.18-.14.29-.27.45-.14.16-.29.34-.41.46-.14.14-.28.29-.12.56.16.27.71 1.17 1.53 1.9 1.05.94 1.94 1.23 2.21 1.37.27.14.43.12.59-.07.16-.18.68-.79.86-1.06.18-.27.36-.22.6-.13.24.09 1.55.73 1.82.86.27.13.45.2.51.31.07.11.07.63-.17 1.31z"></path></svg>'

CSS="""
*{box-sizing:border-box}html,body{margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:'Hanken Grotesk',system-ui,-apple-system,sans-serif;color:#221A12;background:#fff;line-height:1.6;-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%}a{color:inherit;text-decoration:none}
::selection{background:#F6DFC2;color:#221A12}
a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid #C25E10;outline-offset:3px;border-radius:6px}
.skip{position:absolute;left:-9999px;top:0;background:#243A1E;color:#fff;padding:11px 18px;border-radius:0 0 12px 0;z-index:200;font-weight:600}.skip:focus{left:0}
.wrap{max-width:1100px;margin:0 auto;padding:0 clamp(16px,5vw,40px)}
h1,h2,h3{font-family:'Poppins',sans-serif;letter-spacing:-.02em}
header{position:sticky;top:0;z-index:60;background:rgba(255,255,255,.92);backdrop-filter:saturate(180%) blur(10px);-webkit-backdrop-filter:saturate(180%) blur(10px);border-bottom:1px solid rgba(231,221,205,.6)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:11px clamp(16px,5vw,40px);max-width:1200px;margin:0 auto}
.nav-links{display:none;align-items:center;gap:28px}
.nav-links a{font-weight:500;font-size:15.5px;color:#3C342B;padding:8px 2px;display:inline-flex;align-items:center}
.nav-links a:hover{color:#C25E10}
.wa-btn{display:inline-flex;align-items:center;gap:8px;background:#1FA855;color:#fff;font-weight:600;font-size:15px;padding:11px 17px;border-radius:999px}
.burger{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border:1px solid #E7DDCD;background:#fff;border-radius:12px;cursor:pointer;color:#221A12}
#mobile-menu{display:none;opacity:0;transform:translateY(-8px);transition:.22s;position:absolute;top:100%;left:0;right:0;background:#fff;border-bottom:1px solid #E7DDCD;box-shadow:0 26px 40px -28px rgba(34,26,18,.5);flex-direction:column;padding:8px clamp(16px,5vw,40px) 20px}
#mobile-menu a{padding:13px 6px;font-weight:600;font-size:17px;border-bottom:1px solid #F1E9DC}
.crumb{font-size:13.5px;color:#6E6256;padding:18px 0 0}.crumb a{color:#6E6256}.crumb a:hover{color:#C25E10}.crumb b{color:#3C342B;font-weight:600}
.phead{padding:16px 0 clamp(26px,4vw,44px);background:radial-gradient(120% 90% at 92% 0,#FDF4E7 0%,#FFFDF9 55%,#fff 100%)}
.ey{font-weight:600;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#C25E10;margin-bottom:12px}
.phead h1{font-weight:800;font-size:clamp(30px,5vw,48px);line-height:1.06;color:#243A1E;margin:0 0 14px}
.phead p{font-size:clamp(15.5px,1.7vw,18px);line-height:1.6;color:#6E6256;margin:0;max-width:720px}
.sec{padding:clamp(30px,4vw,52px) 0}
.prose{max-width:760px}
.prose h2{font-weight:700;font-size:clamp(20px,3vw,28px);color:#221A12;margin:34px 0 12px}
.prose h3{font-weight:700;font-size:18px;color:#221A12;margin:22px 0 8px}
.prose p{font-size:16.5px;line-height:1.72;color:#4C443A;margin:0 0 12px}
.prose ul{margin:0 0 14px;padding-left:22px;color:#4C443A;font-size:16px;line-height:1.7}
.prose li{margin-bottom:6px}
.note{background:#FCF3E7;border:1px solid #F1E1C9;border-radius:14px;padding:16px 18px;font-size:14.5px;color:#6E6256;margin:0 0 8px}
.vals{display:grid;grid-template-columns:1fr;gap:16px;margin-top:8px}
.val{background:#fff;border:1px solid #EFE7DA;border-radius:18px;padding:24px}
.val .ic{width:48px;height:48px;border-radius:13px;background:#FBEFDF;display:inline-flex;align-items:center;justify-content:center;color:#C25E10;margin-bottom:14px}
.val h3{font-family:'Poppins';font-weight:700;font-size:19px;color:#221A12;margin:0 0 7px}
.val p{font-size:15px;line-height:1.58;color:#6E6256;margin:0}
.form{background:#fff;border:1px solid #ECE3D6;border-radius:20px;padding:clamp(20px,3vw,32px);box-shadow:0 24px 50px -34px rgba(34,26,18,.4)}
.form .row{display:grid;grid-template-columns:1fr;gap:14px;margin-bottom:14px}
.form label{display:block;font-weight:600;font-size:14px;color:#3C342B;margin-bottom:6px}
.form input,.form select,.form textarea{width:100%;font:inherit;font-size:15.5px;color:#221A12;background:#FCFAF6;border:1px solid #E3D7C5;border-radius:12px;padding:12px 14px}
.form textarea{min-height:110px;resize:vertical}
.form .chk{display:flex;gap:10px;align-items:flex-start;font-size:14px;color:#6E6256;margin-bottom:16px}
.form .chk input{width:auto;margin-top:3px}
.form button{width:100%;display:inline-flex;align-items:center;justify-content:center;gap:10px;background:#1FA855;color:#fff;font-weight:700;font-size:16.5px;padding:15px;border:0;border-radius:14px;cursor:pointer}
.cinfo{display:grid;grid-template-columns:1fr;gap:14px;margin-bottom:22px}
.cinfo a{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid #ECE3D6;border-radius:14px;padding:15px 18px;font-weight:600;color:#221A12}
.cinfo .ic{width:40px;height:40px;border-radius:11px;background:#EAF1E6;display:inline-flex;align-items:center;justify-content:center;color:#2E5A2C;flex:none}
.grid2{display:grid;grid-template-columns:1fr;gap:clamp(24px,4vw,44px);align-items:start}
footer{background:#FAF6EF;border-top:1px solid #EEE6D8;padding:clamp(40px,6vw,64px) 0 24px;margin-top:40px}
.foot-grid{display:grid;grid-template-columns:1fr;gap:clamp(24px,3vw,40px)}
footer .about{font-size:14.5px;line-height:1.6;color:#7C6F60;margin:10px 0 16px;max-width:300px}
footer h5{font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#221A12;margin:0 0 13px;font-family:'Poppins'}
footer ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
footer ul a{font-size:14.5px;color:#6E6256}footer ul a:hover{color:#C25E10}
.foot-bottom{margin-top:clamp(26px,4vw,40px);padding:20px 0;border-top:1px solid #EEE6D8;display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;font-size:13px;color:#6E6256}
@media(min-width:680px){.vals{grid-template-columns:repeat(3,1fr)}.cinfo{grid-template-columns:1fr 1fr}}
@media(min-width:900px){.grid2{grid-template-columns:1fr 1fr}}
@media(min-width:980px){.nav-links{display:flex}.burger{display:none}.foot-grid{grid-template-columns:1.5fr 1fr 1fr 1fr}}
@media(prefers-reduced-motion:reduce){*{transition-duration:.001ms!important;animation-duration:.001ms!important}}
"""

def header(pre):
    L=[("Modeller",pre+"index.html#modeller"),("Fiyatlar",pre+"fiyatlar/"),("Özellikler",pre+"index.html#ozellikler"),("Neden Biz",pre+"index.html#referanslar"),("S.S.S.",pre+"index.html#sss"),("Blog",pre+"blog/"),("İletişim",pre+"iletisim/")]
    nav="".join('<a href="%s">%s</a>'%(u,e(t)) for t,u in L)
    mob="".join('<a href="%s">%s</a>'%(u,e(t)) for t,u in L)
    return ('<header><div class="nav"><a href="%sindex.html" aria-label="Tavuk Çadırı ana sayfa"><img src="%sassets/logo.png" alt="Tavuk Çadırı" style="height:52px;width:auto"></a>'
      '<nav class="nav-links">%s</nav>'
      '<div class="nav-cta"><a href="https://wa.me/%s" target="_blank" rel="noopener" class="wa-btn">%s<span>Teklif al</span></a>'
      '<button id="nav-burger" class="burger" aria-label="Menü" aria-expanded="false" aria-controls="mobile-menu"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"></path></svg></button></div>'
      '<div id="mobile-menu">%s</div></div></header>')%(pre,pre,nav,WA,WA_SVG.format(w=18,f="#fff"),mob)

def footer(pre):
    prod=[("500-tavukluk-tavuk-cadiri","500 Tavuk / 70 m²"),("750-tavukluk-tavuk-cadiri","750 Tavuk / 98 m²"),("1000-tavukluk-tavuk-cadiri","1.000 Tavuk / 140 m²"),("2000-tavukluk-tavuk-cadiri","2.000+ / 300 m²"),("fiyatlar","Tüm ölçüler & fiyatlar")]
    m="".join('<li><a href="%s%s/">%s</a></li>'%(pre,s,e(t)) for s,t in prod)
    return ('<footer><div class="wrap"><div class="foot-grid">'
      '<div><img src="%sassets/logo.png" alt="Tavuk Çadırı" style="width:150px"><p class="about">3 ve 4 kat yalıtımlı, TSE damgalı brandalı anahtar teslim tavuk çadırı. Türkiye geneli 81 ile nakliye ve kurulum. Üretim: DEHA Çadır.</p>'
      '<a href="https://wa.me/%s" target="_blank" rel="noopener" class="wa-btn" style="font-size:14.5px;padding:11px 17px">%s<span>Bize ulaşın</span></a></div>'
      '<div><h5>Ürünler</h5><ul>%s</ul></div>'
      '<div><h5>Kurumsal</h5><ul><li><a href="%shakkimizda/">Hakkımızda</a></li><li><a href="%siletisim/">İletişim</a></li><li><a href="%sindex.html#sss">S.S.S.</a></li><li><a href="%sblog/">Blog</a></li></ul></div>'
      '<div><h5>Yasal</h5><ul><li><a href="%skvkk/">KVKK Aydınlatma Metni</a></li><li><a href="%sgizlilik/">Gizlilik &amp; Çerez Politikası</a></li></ul></div>'
      '</div><div class="foot-bottom"><span>© 2026 Tavuk Çadırı. Tüm hakları saklıdır.</span><span>Üretim &amp; kurulum: DEHA Çadır · 81 il</span></div></div></footer>')%(pre,WA,WA_SVG.format(w=17,f="#fff"),m,pre,pre,pre,pre,pre,pre)

COOKIE=''

JS=("""(function(){var b=document.getElementById('nav-burger'),m=document.getElementById('mobile-menu'),o=false;
function tg(){o=!o;if(!m)return;if(b)b.setAttribute('aria-expanded',o?'true':'false');if(o){m.style.display='flex';requestAnimationFrame(function(){m.style.opacity='1';m.style.transform='translateY(0)';var f=m.querySelector('a');if(f)f.focus();});}else{m.style.opacity='0';m.style.transform='translateY(-8px)';setTimeout(function(){if(!o)m.style.display='none';},230);}}
if(b)b.addEventListener('click',tg);if(m)m.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){if(o)tg();});});
document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&o){tg();if(b)b.focus();}});
var h=document.querySelector('header');window.addEventListener('scroll',function(){if(h)h.style.boxShadow=window.scrollY>14?'0 10px 30px -22px rgba(34,26,18,.5)':'none';},{passive:true});
})();
""")

# Google Analytics 4 (G-RES77XE6HP) + WhatsApp/telefon tiklama olaylari — tum sayfalarin head'ine girer
GA_TAG = ('<!-- Google tag (gtag.js) -->'
 '<script async src="https://www.googletagmanager.com/gtag/js?id=G-RES77XE6HP"></script>'
 '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-RES77XE6HP");'
 'document.addEventListener("click",function(ev){var a=ev.target&&ev.target.closest?ev.target.closest("a"):null;if(!a)return;var h=a.href||"";'
 'if(h.indexOf("wa.me")>-1){gtag("event","whatsapp_click",{link_url:h});}'
 'else if(h.indexOf("tel:")===0){gtag("event","phone_click",{link_url:h});}});</script>')

def doc(title,desc,slug,body_main,pre="../",noindex=False,extra_js=""):
    robots='<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow">'
    canon='' if noindex else '<link rel="canonical" href="%s/%s/">'%(SITE,slug)
    og='' if noindex else '<meta property="og:url" content="%s/%s/"><meta property="og:image" content="%s/assets/photos/og/og-home.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="%s/assets/photos/og/og-home.jpg">'%(SITE,slug,SITE,SITE)
    return ('<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
      '<title>%s</title><meta name="description" content="%s">%s%s'
      '<meta property="og:type" content="website"><meta property="og:site_name" content="Tavuk Çadırı"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:locale" content="tr_TR">%s'
      '<link rel="icon" type="image/png" sizes="32x32" href="%sassets/favicon-32.png"><link rel="icon" type="image/png" sizes="512x512" href="%sassets/favicon.png"><link rel="apple-touch-icon" href="%sassets/apple-touch-icon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
      '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Hanken+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"><style>%s</style>'
      +GA_TAG+'</head>'
      '<body><a href="#main" class="skip">İçeriğe geç</a>%s<main id="main">%s</main>%s%s<script>%s</script>%s</body></html>')%(
      e(title),e(desc),robots,canon,e(title),e(desc),og,pre,pre,pre,CSS,header(pre),body_main,footer(pre),COOKIE,JS,('<script>%s</script>'%extra_js if extra_js else ''))

def phead(ey,h1,p,crumb):
    return ('<div class="wrap"><div class="crumb">%s</div></div><section class="phead"><div class="wrap"><div class="ey">%s</div><h1>%s</h1><p>%s</p></div></section>')%(crumb,e(ey),e(h1),e(p))

def cta_block():
    return ('<section class="sec"><div class="wrap"><div style="background:linear-gradient(135deg,#2E5A2C,#244A22);border-radius:24px;padding:clamp(28px,4vw,48px);color:#fff;text-align:center">'
      '<h2 style="font-weight:700;font-size:clamp(22px,3vw,32px);margin:0 0 10px">Projenizi birlikte planlayalım</h2>'
      '<p style="color:#CBD8C7;margin:0 auto 20px;max-width:520px">Kapasitenizi ve bölgenizi yazın; ölçü ve teklifi birlikte çıkaralım.</p>'
      '<a href="https://wa.me/%s" target="_blank" rel="noopener" class="wa-btn" style="background:#fff;color:#1B3D1A;font-size:16px;padding:14px 24px;border-radius:13px">%s Kapasitenizi yazın</a>'
      '</div></div></section>')%(WA,WA_SVG.format(w=19,f="#1FA855"))

pages=[]

# ---- HAKKIMIZDA ----
ic=lambda p:'<span class="ic"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="%s"/></svg></span>'%p
about_body=(phead("Hakkımızda","Anahtar teslim tavuk çadırında güvenilir çözüm ortağınız",
  "Galvaniz çelik iskelet ve izolasyonlu branda ile Türkiye geneli anahtar teslim kümes çadırı üretiyor, nakliye ve kurulumu tek elden tamamlıyoruz.",
  '<a href="../index.html">Ana Sayfa</a> › <b>Hakkımızda</b>')
 +'<section class="sec"><div class="wrap"><div class="prose">'
 +'<p>Tavuk Çadırı olarak amacımız, tavuk ve kümes hayvanı yetiştiriciliğine başlamak ya da işini büyütmek isteyen üreticilere; betonarmenin yüksek maliyeti ve uzun izin süreçleri olmadan, hızlı kurulan, izolasyonlu ve dayanıklı bir barınak çözümü sunmaktır. 500 tavuktan 2.800 tavuğa kadar her kapasitede, ölçüye özel üretim yapıyoruz.</p>'
 +'<h2>Nasıl çalışıyoruz?</h2>'
 +'<p>Çalışma modelimiz baştan sona <strong>anahtar teslim</strong>dir. Kapasitenizi ve bölgenizi konuştuktan sonra ölçü, izolasyon ve ekipmanı birlikte planlar; üretimi tamamlar, ürünü sahaya nakleder ve ekibimizle yerinde kurarız. Siz yalnızca sürünüzü yerleştirirsiniz. Nakliye ve montaj fiyata dahildir; Türkiye’nin her iline hizmet veriyoruz.</p>'
 +'<h2>Neden çadır kümes?</h2>'
 +'<ul><li>Betonarmeye göre belirgin düşük maliyet, temel/inşaat gerektirmez.</li><li>Galvaniz çelik makaslı iskelet + 650 g/m² TSE damgalı, UV ve alev yürütmez branda ile uzun ömür.</li><li>3 veya 4 kat alüminyum bizafol izolasyon: yazın serin, kışın sıcak; yoğuşmayı önleyen dengeli iç ortam.</li><li>Demonte edilip taşınabilir; çoğu bölgede yapı ruhsatı gerektirmez.</li></ul>'
 +'<h2>Şeffaflık sözümüz</h2>'
 +'<p>Neyin fiyata dahil olduğunu (nakliye, montaj, ekipman) ve neyin hariç olduğunu (zemin, su, elektrik altyapısı) baştan net konuşuyoruz. Ruhsat ve devlet desteği konularında da abartısız, dürüst yönlendirme yapıyoruz. Sorularınızı WhatsApp’tan yazın, aynı gün dönüş yapalım.</p>'
 +'<div class="note">Yeni bir markayız ve ilk referanslarımızı oluşturuyoruz; sizinle uzun soluklu çalışmaktan memnuniyet duyarız.</div>'
 +'</div></div></section>'+cta_block())
pages.append(("hakkimizda","Hakkımızda | Tavuk Çadırı — Anahtar Teslim Kümes Çadırı Üreticisi",
  "Tavuk Çadırı: galvaniz çelik ve izolasyonlu branda ile Türkiye geneli anahtar teslim kümes çadırı üretimi, nakliye ve kurulum. Şeffaf, dürüst çalışma modeli.",about_body,False))

# ---- ILETISIM ----
tel_svg='<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
ig_svg='<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'
contact_body=(phead("İletişim","Teklif ve bilgi için bize ulaşın",
  "Kapasitenizi, bölgenizi ve ihtiyacınızı yazın; ölçü ve teklifinizi aynı gün hazırlayalım. En hızlı yanıt WhatsApp üzerindendir.",
  '<a href="../index.html">Ana Sayfa</a> › <b>İletişim</b>')
 +'<section class="sec"><div class="wrap"><div class="grid2">'
 +'<div><h2 style="font-family:Poppins;font-weight:700;font-size:24px;margin:0 0 6px">Doğrudan ulaşın</h2><p style="color:#6E6256;margin:0 0 18px">Aşağıdaki formu doldurup tek dokunuşla WhatsApp’tan gönderebilir ya da doğrudan yazabilirsiniz.</p>'
 +'<div class="cinfo"><a href="https://wa.me/%s" target="_blank" rel="noopener"><span class="ic">%s</span>WhatsApp: %s</a>'%(WA,WA_SVG.format(w=20,f="#2E5A2C"),WA_DISP)
 +'<a href="tel:0%s"><span class="ic">%s</span>Telefon: %s</a>'%(WA[2:],tel_svg,WA_DISP)
 +'</div>'
 +'<p style="font-size:14px;color:#6E6256">Merkez: İstanbul / Sancaktepe · E-posta: <a href="mailto:info@tavukcadiri.com" style="color:#C25E10">info@tavukcadiri.com</a> · Türkiye geneli 81 ilde üretim ve kurulum (Deha Yapı ve Mimarlık Ltd. Şti.).</p></div>'
 # form
 +'<div><form class="form" id="lead" onsubmit="return sendWA(event)">'
 +'<div class="row"><div><label for="f-ad">Ad Soyad</label><input id="f-ad" name="ad" required></div></div>'
 +'<div class="row" style="grid-template-columns:1fr 1fr"><div><label for="f-tel">Telefon</label><input id="f-tel" name="tel" inputmode="tel" required></div><div><label for="f-il">İl / İlçe</label><input id="f-il" name="il"></div></div>'
 +'<div class="row"><div><label for="f-kap">Kapasite</label><select id="f-kap" name="kap"><option value="">Seçin…</option><option>500 tavuk</option><option>750 tavuk</option><option>1000 tavuk</option><option>2000 tavuk</option><option>2000+ / özel</option><option>Kararsızım</option></select></div></div>'
 +'<div class="row"><div><label for="f-msg">Mesajınız (opsiyonel)</label><textarea id="f-msg" name="msg" placeholder="Zemin durumu, hedef tarih, sorularınız…"></textarea></div></div>'
 +'<label class="chk"><input type="checkbox" id="f-kvkk" required><span><a href="../kvkk/">KVKK Aydınlatma Metni</a>’ni okudum; verilerimin teklif ve iletişim amacıyla işlenmesini kabul ediyorum.</span></label>'
 +'<button type="submit">%s Formu gönderin</button>'%WA_SVG.format(w=20,f="#fff")
 +'<p style="font-size:12.5px;color:#6E6256;margin:12px 0 0;text-align:center">Form, bilgilerinizle hazırlanmış bir mesajı WhatsApp’ta açar; oradan gönderirsiniz.</p>'
 +'</form></div>'
 +'</div></div></section>')
contact_js=("function sendWA(ev){ev.preventDefault();var g=function(i){var el=document.getElementById(i);return el?el.value.trim():'';};"
 "var nl=String.fromCharCode(10);"
 "var t='Merhaba, tavuk cadiri icin teklif almak istiyorum.'+nl+'Ad: '+g('f-ad')+nl+'Telefon: '+g('f-tel')+nl+'Il/Ilce: '+g('f-il')+nl+'Kapasite: '+g('f-kap')+nl+'Mesaj: '+g('f-msg');"
 "window.open('https://wa.me/__WA__?text='+encodeURIComponent(t),'_blank');return false;}").replace('__WA__',WA)
pages.append(("iletisim","İletişim | Tavuk Çadırı — Teklif ve Bilgi",
  "Tavuk çadırı teklifi için bize ulaşın. Formu doldurup WhatsApp’tan gönderin ya da doğrudan yazın. Merkez İstanbul, Türkiye geneli hizmet.",contact_body,False,contact_js))

# ---- KVKK ----
kvkk_body=(phead("KVKK Aydınlatma Metni","Kişisel Verilerin Korunması Aydınlatma Metni",
  "6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında veri sorumlusu sıfatıyla hazırlanmıştır.",
  '<a href="../index.html">Ana Sayfa</a> › <b>KVKK Aydınlatma Metni</b>')
 +'<section class="sec"><div class="wrap"><div class="prose">'
 +'<h2>1. Veri Sorumlusu</h2><p>İşbu aydınlatma metni, Deha Yapı ve Mimarlık Ltd. Şti. (“DEHA Çadır”, tavukcadiri.com) tarafından, 6698 sayılı Kişisel Verilerin Korunması Kanunu (“KVKK”) 10. maddesi uyarınca hazırlanmıştır. Adres: Sancaktepe, İstanbul. E-posta: info@tavukcadiri.com.</p>'
 +'<h2>2. İşlenen Kişisel Veriler</h2><p>Sitemizdeki iletişim/teklif formu ve WhatsApp üzerinden bizimle iletişime geçtiğinizde; ad-soyad, telefon numarası, bulunduğunuz il/ilçe ve talebinize ilişkin ilettiğiniz bilgiler işlenir. Ayrıca site kullanımına dair zorunlu çerezler aracılığıyla teknik veriler işlenebilir.</p>'
 +'<h2>3. İşleme Amaçları</h2><ul><li>Teklif ve fiyatlandırma taleplerinizin karşılanması,</li><li>Ürün ve hizmetlerimiz hakkında sizinle iletişim kurulması,</li><li>Sözleşme öncesi görüşme ve satış-kurulum süreçlerinin yürütülmesi,</li><li>Yasal yükümlülüklerin yerine getirilmesi.</li></ul>'
 +'<h2>4. Hukuki Sebep</h2><p>Verileriniz KVKK 5. madde kapsamında; talebinize istinaden sözleşmenin kurulması/ifası ve meşru menfaat hukuki sebeplerine dayanılarak, açık rızanızın gerektiği hallerde ise rızanıza dayanılarak işlenir.</p>'
 +'<h2>5. Aktarım</h2><p>Kişisel verileriniz, hizmetin gerektirdiği ölçüde nakliye/kurulum ekipleri ve yasal olarak yetkili kamu kurumları ile paylaşılabilir; bunun dışında üçüncü kişilere satılmaz veya pazarlama amacıyla aktarılmaz. WhatsApp üzerinden iletişimde ilgili platformun kendi politikaları geçerlidir.</p>'
 +'<h2>6. Saklama Süresi</h2><p>Verileriniz, işleme amacının gerektirdiği ve ilgili mevzuatta öngörülen süreler boyunca saklanır; sürenin sonunda silinir, yok edilir veya anonim hale getirilir.</p>'
 +'<h2>7. Haklarınız (KVKK md. 11)</h2><p>Kişisel verilerinizin işlenip işlenmediğini öğrenme, bilgi talep etme, düzeltilmesini/silinmesini isteme, işlemenin sınırlandırılmasını talep etme ve kanunda sayılan diğer haklara sahipsiniz. Taleplerinizi info@tavukcadiri.com adresine iletebilirsiniz.</p>'
 +'</div></div></section>')
pages.append(("kvkk","KVKK Aydınlatma Metni | Tavuk Çadırı",
  "Tavuk Çadırı KVKK aydınlatma metni: işlenen kişisel veriler, amaçlar, hukuki sebep, aktarım, saklama ve KVKK madde 11 kapsamındaki haklarınız.",kvkk_body,False))

# ---- GIZLILIK ----
giz_body=(phead("Gizlilik & Çerez Politikası","Gizlilik ve Çerez Politikası",
  "Kişisel verilerinizin ve gizliliğinizin korunmasına ilişkin ilkelerimiz ve çerez kullanımımız.",
  '<a href="../index.html">Ana Sayfa</a> › <b>Gizlilik &amp; Çerez Politikası</b>')
 +'<section class="sec"><div class="wrap"><div class="prose">'
 +'<h2>Hangi verileri topluyoruz?</h2><p>Yalnızca iletişim/teklif formu ve WhatsApp üzerinden bize ilettiğiniz bilgileri (ad, telefon, il/ilçe, mesaj) ve sitenin çalışması için gerekli teknik verileri topluyoruz. Sitede üyelik veya çevrimiçi ödeme bulunmamaktadır.</p>'
 +'<h2>Çerezler</h2><p>Sitemiz, temel işlevler ve deneyim iyileştirmesi için sınırlı çerez kullanır. Kullanılabilecek çerez türleri:</p>'
 +'<ul><li><strong>Zorunlu çerezler:</strong> Sitenin temel işlevlerinin çalışması için gerekli olabilir.</li><li><strong>Üçüncü taraf:</strong> Yazı tipleri Google Fonts üzerinden yüklenir; bu sırada tarayıcınızın IP bilgisi ilgili sağlayıcıya iletilebilir. WhatsApp bağlantısına tıkladığınızda WhatsApp’ın kendi politikaları geçerli olur.</li></ul>'
 +'<p>Tarayıcı ayarlarınızdan çerezleri dilediğiniz zaman silebilir veya engelleyebilirsiniz; ancak bazı işlevler etkilenebilir.</p>'
 +'<h2>Verilerin güvenliği</h2><p>Verileriniz yalnızca teklif ve iletişim amacıyla kullanılır; üçüncü kişilere satılmaz. Ayrıntılı bilgi için <a href="../kvkk/">KVKK Aydınlatma Metni</a>’ni inceleyebilirsiniz.</p>'
 +'<h2>İletişim</h2><p>Gizlilikle ilgili sorularınız için <a href="../iletisim/">İletişim</a> sayfamızdan bize ulaşabilirsiniz.</p>'
 +'</div></div></section>')
pages.append(("gizlilik","Gizlilik & Çerez Politikası | Tavuk Çadırı",
  "Tavuk Çadırı gizlilik ve çerez politikası: hangi veriler toplanır, çerez kullanımı, üçüncü taraflar ve veri güvenliği.",giz_body,False))

# write subfolder pages
new_slugs=[]
for slug,title,desc,body,noindex,*rest in [(p[0],p[1],p[2],p[3],p[4],*(p[5:])) for p in pages]:
    ejs=rest[0] if rest else ""
    d=doc(title,desc,slug,body,pre="../",noindex=noindex,extra_js=ejs)
    for base in (PROJ,SCR):
        os.makedirs(os.path.join(base,slug),exist_ok=True)
        open(os.path.join(base,slug,"index.html"),"w",encoding="utf-8").write(d)
    if not noindex: new_slugs.append(slug)

# ---- 404 (root) ----
body404=('<section class="phead"><div class="wrap" style="text-align:center;padding-top:40px">'
 '<div class="ey" style="justify-content:center">Hata 404</div>'
 '<h1>Aradığınız sayfa bulunamadı</h1>'
 '<p style="margin:0 auto 22px">Sayfa taşınmış veya kaldırılmış olabilir. Aşağıdan devam edebilirsiniz.</p>'
 '<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a href="/" class="wa-btn" style="background:#2E5A2C">Ana sayfaya dön</a>'
 '<a href="/iletisim/" class="wa-btn" style="background:#fff;color:#221A12;border:1px solid #E3D7C5">İletişim</a></div></div></section>')
d404=doc("Sayfa Bulunamadı (404) | Tavuk Çadırı","Aradığınız sayfa bulunamadı.","",body404.replace('href="../','href="/').replace('%sassets','/assets').replace(header("../"),header("/")) if False else body404,pre="/",noindex=True)
for base in (PROJ,SCR): open(os.path.join(base,"404.html"),"w",encoding="utf-8").write(d404)

print("new pages:", [p[0] for p in pages], "+ 404.html")
print("indexable new slugs:", new_slugs)
