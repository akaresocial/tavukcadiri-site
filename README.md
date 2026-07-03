# tavukcadiri.com

Anahtar teslim tavuk çadırı tanıtım sitesi (statik HTML). Üretim & kurulum: DEHA Çadır.

## Otomatik yayın (auto-deploy)

İki katman var; ikisi de aynı `deploy.sh`'ı kullanır (Alastyr, GitHub IP'lerinden
FTP'yi engellediği için her iki düzen de sunucu-çeker mantığında çalışır):

1. **Webhook (anlık, birincil):** `main`'e push → GitHub, `https://tavukcadiri.com/deploy-hook.php`
   adresini çağırır (HMAC-SHA256 imzalı) → hook `~/site/deploy.sh`'ı hemen çalıştırır.
   Push'tan ~1 dk sonra canlıda.
2. **Cron (yedek):** Hosting cron'u periyodik `deploy.sh` çalıştırır (panelde 15 dk
   görünüyor; 5 dk'ya çekilebilir). Webhook bir sebeple çalışmazsa değişiklik en geç
   bir sonraki cron döngüsünde yayınlanır.

Mekanizma:
- Sunucuda repo klonu: `~/site`
- `deploy.sh`: `git fetch` → yeni commit varsa `ff-merge` + repo kökünü `public_html`'e kopyalar (hariç-tut listesi: _kaynak, README, deploy.sh, orijinal logo — yeni klasörler otomatik dahil)
- Yayın kaydı: sunucuda `~/deploy.log`; webhook kaydı: `~/deploy-hook.log`; son commit: `~/.last_deploy_commit`

### Webhook kurulumu (bir kez)

1. Secret repoda tutulmaz: hook'a gelen İLK istekte sunucu rastgele bir secret üretir,
   `~/.deploy_hook_secret`'a yazar ve değeri yalnızca o yanıtta bir kez gösterir.
   Rotasyon: sunucudaki dosya silinir → sonraki ilk istek yeni değeri üretip bir kez
   gösterir → GitHub'daki Secret aynı değerle güncellenir.
2. GitHub → repo → Settings → Webhooks → Add webhook:
   Payload URL `https://tavukcadiri.com/deploy-hook.php` · Content type `application/json`
   · Secret: ilk yanıtta gösterilen değer · Events: *Just the push event*.
3. Kayıttan sonra GitHub "ping" atar → Webhooks → Recent Deliveries'te **200 (pong)** görünmeli.
   Sorun olursa sunucudaki `~/deploy-hook.log`'a bak (`shell_exec` kapalıysa hook 501 döner;
   o durumda hosting panelinden PHP fonksiyon kısıtı açılmalı, cron yedek olarak çalışır).

Yani güncelleme akışı: değişiklik yap → commit → push → ~1 dk içinde canlıda
(webhook kurulana kadar: en geç bir cron döngüsü).

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
