# tavukcadiri.com

Anahtar teslim tavuk çadırı tanıtım sitesi (statik HTML). Üretim & kurulum: DEHA Çadır.

## Otomatik yayın (auto-deploy)

`main` dalına push → Alastyr sunucusundaki cron (her 5 dk) değişikliği çekip yayınlar.

Mekanizma (Alastyr, GitHub IP'lerinden FTP'yi engellediği için sunucu-çeker düzen):
- Sunucuda repo klonu: `~/site`
- Cron (hosting hesabı, */5): repo yoksa klonlar, sonra `deploy.sh` çalıştırır
- `deploy.sh`: `git fetch` → yeni commit varsa `ff-merge` + dosyaları `public_html`'e kopyalar
- Yayın kaydı: sunucuda `~/deploy.log`, son commit: `~/.last_deploy_commit`

Yani güncelleme akışı: değişiklik yap → commit → push → en geç 5 dk içinde canlıda.

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
