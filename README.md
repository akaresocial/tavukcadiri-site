# tavukcadiri.com

Anahtar teslim tavuk çadırı tanıtım sitesi (statik HTML). Üretim & kurulum: DEHA Çadır.

## Otomatik yayın (auto-deploy)

İki katman var; ikisi de aynı `deploy.sh`'ı kullanır (Alastyr, GitHub IP'lerinden
FTP'yi engellediği için her iki düzen de sunucu-çeker mantığında çalışır):

1. **Webhook (anlık, birincil):** `main`'e push → GitHub, `https://tavukcadiri.com/deploy-hook.php`
   adresini çağırır (HMAC-SHA256 imzalı) → hook deploy'u **saf PHP ile kendisi yapar**:
   push'taki commit'in zip'ini GitHub'dan indirir, açar, `public_html`'e kopyalar
   (repo public olduğu için token gerekmez; Alastyr'da `shell_exec` kapalı olduğundan
   deploy.sh çağrılmaz). Push'tan saniyeler sonra canlıda.
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
   Push teslimatlarının yanıtında `yayinlandi: commit … · N dosya · X sn` özeti görünür.
   Sorun olursa sunucudaki `~/deploy-hook.log`'a bak; hook hata verirse bile cron yedeği
   değişikliği en geç bir sonraki döngüde yayınlar.

Yani güncelleme akışı: değişiklik yap → commit → push → ~1 dk içinde canlıda
(webhook kurulana kadar: en geç bir cron döngüsü).

## Yapı — önce bunu oku

Kökteki ~90 klasörün ÇOĞU **otomatik üretilen yayın çıktısıdır** (bir "build/dist" klasörü gibi).
Her klasör = sitede bir sayfa = bir URL. **Bunları elle açıp düzenleme.** Tüm iş `_kaynak/`'ta olur:
üreteci değiştir → çalıştır → klasörler yeniden üretilir → commit + push.

| Kökteki klasör/dosya | Kim üretir? | Elle mi? |
|---|---|---|
| `index.html` | — | ✍️ elle yazılır |
| `500/750/1000/2000-tavukluk-tavuk-cadiri/`, `fiyatlar/` | `_kaynak/gen_products.py` | 🤖 otomatik |
| `hakkimizda/`, `iletisim/`, `kvkk/`, `gizlilik/`, `404.html` | `_kaynak/gen_pages.py` | 🤖 otomatik |
| `<il>-tavuk-cadiri/` (81 il), `kurulum-bolgeleri/` | `_kaynak/gen_iller.py` | 🤖 otomatik |
| `blog/` + alt yazılar | `_kaynak/gen_blog.py` | 🤖 otomatik |
| `projeler/` | `_kaynak/gen_projeler.py` | 🤖 otomatik |
| `assets/` | görseller (webp) + logo/favicon | — |
| `sitemap.xml` | üreteçler günceller | 🤖 otomatik |
| `.htaccess` | HTTPS & www yönlendirme, 404, önbellek | ✍️ elle |

Yeni proje eklemek için: `python3 _kaynak/proje_ekle.py --klasor "…" --il … --ilce … --olcu … --uret`
(detay: memory `tavukcadiri-projeler-sistemi`). Görsel güncellemede `?v=` sürümünü artır.

## Yayına dahil OLMAYANLAR

- `_kaynak/` — tüm üreteçler, JSON verileri ve `_kaynak/_orijinal-gorseller/` (orijinal kaynak
  fotoğraflar: Hero / Ürün / Birlikte; gitignore'da, siteye dahil değil)
- `README.md`, `deploy.sh`, `Tavuk Çadırı Logo.png` (FTP/deploy exclude)
