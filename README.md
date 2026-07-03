# tavukcadiri.com

Anahtar teslim tavuk çadırı tanıtım sitesi (statik HTML). Üretim & kurulum: DEHA Çadır.

## Otomatik yayın (auto-deploy)

`main` dalına yapılan her push, GitHub Actions ile Alastyr hosting'e (FTP) otomatik senkronize edilir.
Workflow: `.github/workflows/deploy.yml`

Gerekli GitHub Secrets (repo → Settings → Secrets and variables → Actions):
- `FTP_SERVER` — ör. `ftp.tavukcadiri.com` veya sunucu adresi
- `FTP_USERNAME` — cPanel/FTP kullanıcı adı
- `FTP_PASSWORD` — FTP şifresi

İlk çalıştırmada tüm dosyalar yüklenir; sonraki push'larda yalnızca değişenler gider
(sunucuda `.ftp-deploy-sync-state.json` durum dosyası tutulur).

## Yapı

- `index.html` — ana sayfa (elle yazılır)
- `*-tavukluk-tavuk-cadiri/`, `fiyatlar/` — `_kaynak/gen_products.py` ÜRETİR
- `hakkimizda/`, `iletisim/`, `kvkk/`, `gizlilik/`, `404.html` — `_kaynak/gen_pages.py` ÜRETİR
- `assets/photos/*.webp` — ekran görselleri; `model-*.jpg` sadece og:image (WhatsApp önizleme) için
- `.htaccess` — HTTPS & www yönlendirme, 404, önbellek

Ürün/kurumsal sayfaları elle düzenleme; `_kaynak/` içindeki üreteci değiştirip çalıştır.
Görsel güncellemede `?v=` sürümünü artır.

## Yayına dahil OLMAYANLAR

`Hero Fotoğraflar/`, `Ürün Fotoğrafları/`, `Birlikte bölüm foto/` (orijinal kaynak fotoğraflar, gitignore'da),
`_kaynak/`, `README.md`, `Tavuk Çadırı Logo.png` (FTP exclude).
