# -*- coding: utf-8 -*-
# Tek komutla yeni proje ekler: projeler.json'a kayıt yazar, isteğe bağlı sayfaları üretir.
# Kullanım (en sade):
#   python3 _kaynak/proje_ekle.py --klasor "Konya Meram 7x20" --il Konya --ilce Meram --olcu 7x20 --uret
# Alanların çoğu ölçüden ve ilden otomatik türetilir; gerekirse --model, --yalitim, --tarih, --not ile ezersiniz.
#
# Akış: ham fotoğraf klasörünü /projeler/ (veya _kaynak/projeler/) altına bırakın; --klasor ile o klasörün
# adını verin. --uret eklenirse gen_projeler.py (fotoğrafları webp'ye çevirir + sayfaları üretir) ve
# gen_iller.py (o ilin sayfasına kart ekler) otomatik çalışır. Sonra: git add/commit/push.
import os, json, re, argparse, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
JSON = os.path.join(HERE, "projeler.json")

AYLAR = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
         "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

# ölçü (m²) -> ürün modeli. Ara ölçüler m²'ye göre en yakın modele yuvarlanır.
def model_sec(m2):
    if m2 <= 85:   return ("500 Tavukluk",    "500-tavukluk-tavuk-cadiri")
    if m2 <= 120:  return ("750 Tavukluk",    "750-tavukluk-tavuk-cadiri")
    if m2 <= 200:  return ("1.000 Tavukluk",  "1000-tavukluk-tavuk-cadiri")
    return ("2.000+ Tavukluk", "2000-tavukluk-tavuk-cadiri")

_TR = str.maketrans("İIŞĞÜÖÇışğüöç", "iisguocisguoc")
def slugify(s):
    s = s.translate(_TR).lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")

# Türkçe bulunma hâli (-de/-da/-te/-ta) — özel ada kesme ile: "İzmir'de", "Muş'ta", "Konya'da"
_ONSUZ_SERT = set("fstkçşhp")
def locative(ad):
    harfler = ad.translate(str.maketrans("", "", " ")).lower()
    son_unlu = ""
    for ch in reversed(harfler):
        if ch in "aeıioöuü":
            son_unlu = ch; break
    e = son_unlu in "eiöü"  # ince ünlü -> e, kalın -> a
    son_harf = harfler[-1] if harfler else ""
    sert = son_harf in _ONSUZ_SERT
    ek = ("t" if sert else "d") + ("e" if e else "a")
    return "%s'%s" % (ad, ek)

def main():
    ap = argparse.ArgumentParser(description="Yeni tamamlanan proje ekle")
    ap.add_argument("--klasor", required=True, help="Ham fotoğraf klasörünün adı (/projeler/ veya _kaynak/projeler/ içinde)")
    ap.add_argument("--il", required=True)
    ap.add_argument("--ilce", required=True)
    ap.add_argument("--olcu", required=True, help="örn 7x20")
    ap.add_argument("--yalitim", default="3 kat yalıtım")
    ap.add_argument("--m2", type=int, default=0, help="boş bırakılırsa ölçüden hesaplanır")
    ap.add_argument("--model", default="", help="boş bırakılırsa m²'den seçilir (örn '750 Tavukluk')")
    ap.add_argument("--tarih", default="", help="YYYY-AA-GG; boş=bugün")
    ap.add_argument("--not", dest="notu", default="", help="özel açıklama; boş=otomatik şablon")
    ap.add_argument("--uret", action="store_true", help="ekledikten sonra gen_projeler.py + gen_iller.py çalıştır")
    a = ap.parse_args()

    a2, b2 = (re.findall(r"\d+", a.olcu) + ["0", "0"])[:2]
    m2 = a.m2 or (int(a2) * int(b2))
    model_ad, model_slug = (a.model, slugify(a.model).replace("-tavukluk", "") + "-tavukluk-tavuk-cadiri") if a.model else model_sec(m2)
    ilslug = slugify(a.il)
    tarih = a.tarih or datetime.date.today().isoformat()
    yil, ay, _ = tarih.split("-")
    date_disp = "%s %s" % (AYLAR[int(ay)], yil)
    slug = "%s-%s-%s" % (ilslug, slugify(a.ilce), model_slug.split("-")[0])
    olcu_disp = a.olcu.replace("x", "×")

    _kat = re.search(r"\d+", a.yalitim)
    yal_ifade = ("%s kat alüminyum bizafol yalıtım" % _kat.group()) if _kat else a.yalitim
    notu = a.notu or (
        "%s %d m² alana %s (%s) çadır kümes kurduk. Çelik makas iskelet, %s ve 650 g/m² TSE "
        "damgalı brandayla; nakliye ve montaj dahil anahtar teslim edildi."
        % (locative(a.ilce), m2, model_ad.replace(" Tavukluk", " tavukluk"), a.olcu, yal_ifade))

    rec = {
        "slug": slug, "kaynak": a.klasor,
        "il": a.il, "il_loc": locative(a.il), "ilce": a.ilce,
        "ilslug": ilslug, "il_page": "%s-tavuk-cadiri" % ilslug,
        "olcu": a.olcu, "m2": m2, "model_ad": model_ad, "model_slug": model_slug,
        "yalitim": a.yalitim, "date": tarih, "date_disp": date_disp,
        "aciklama": notu,
        "alt": "%s %s'da kurulan %s %d m² %s tavuk çadırı" % (a.il, a.ilce, olcu_disp, m2, model_ad.replace(" Tavukluk", " tavukluk")),
        "wa_text": "Merhaba, %s %s'daki %s kurulumunuzu gordum. Benzer bir tavuk cadiri icin teklif istiyorum. Bolge: ... / Kapasite: ..." % (a.il, a.ilce, a.olcu),
    }

    recs = json.load(open(JSON, encoding="utf-8")) if os.path.exists(JSON) else []
    varolan = next((i for i, r in enumerate(recs) if r["slug"] == slug), None)
    if varolan is not None:
        recs[varolan] = rec; durum = "GÜNCELLENDİ"
    else:
        recs.append(rec); durum = "EKLENDİ"
    recs.sort(key=lambda r: r["date"], reverse=True)
    json.dump(recs, open(JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("%s: %s" % (durum, slug))
    print("  başlık : %s %s — %s Tavuk Çadırı Kurulumu Tamamlandı" % (a.il, a.ilce, model_ad))
    print("  açıklama: %s" % notu)
    print("  kaynak klasör: %s" % a.klasor)

    if a.uret:
        for betik in ("gen_projeler.py", "gen_iller.py"):
            print("→ %s" % betik)
            subprocess.run(["python3", os.path.join(HERE, betik)], cwd=HERE, check=True)
        print("\nHazır. Şimdi: git add -A && git commit && git push  (5 dk'da canlıda)")
    else:
        print("\nSonra: python3 _kaynak/gen_projeler.py && python3 _kaynak/gen_iller.py")

if __name__ == "__main__":
    main()
