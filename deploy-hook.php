<?php
// tavukcadiri.com — GitHub push webhook tetikleyicisi
// Amaç: main'e push olur olmaz (cron'u beklemeden) sunucudaki ~/site/deploy.sh'ı çalıştırmak.
//
// KURULUM (tek adım):
//  Secret repoda TUTULMAZ. İlk istekte sunucu rastgele bir secret üretip
//  ~/.deploy_hook_secret dosyasına yazar ve değeri YALNIZCA O YANITTA bir kez gösterir.
//  O değerle GitHub → repo → Settings → Webhooks → Add webhook:
//       Payload URL : https://tavukcadiri.com/deploy-hook.php
//       Content type: application/json
//       Secret      : ilk yanıtta gösterilen değer
//       Events      : Just the push event
//  Kayıt sonrası GitHub "ping" gönderir; Recent Deliveries'te 200 (pong) görmelisiniz.
//  Rotasyon: sunucudaki ~/.deploy_hook_secret silinir → sonraki ilk istek yeni değer
//  üretip bir kez gösterir → GitHub'daki Secret da aynı değerle güncellenir.
//
// Güvenlik: her istek GitHub'ın HMAC-SHA256 imzasıyla doğrulanır (X-Hub-Signature-256).
// İmzasız/yanlış imzalı istekler 403 alır; komut hiçbir kullanıcı girdisi içermez.
// Kayıtlar: ~/deploy-hook.log (tetikleyici) ve ~/deploy.log (deploy.sh çıktısı).

$home = dirname($_SERVER['DOCUMENT_ROOT']);   // public_html'in bir üstü (home dizini)
$secretFile = $home.'/.deploy_hook_secret';
$log = $home.'/deploy-hook.log';

function say($code, $msg){ http_response_code($code); header('Content-Type: text/plain; charset=utf-8'); echo $msg."\n"; exit; }
function logline($msg){ global $log; @file_put_contents($log, date('Y-m-d H:i:s').' '.$msg."\n", FILE_APPEND); }

if (!is_file($secretFile)) {
  // İlk kurulum: rastgele secret üret, dosyaya yaz, değeri sadece bu yanıtta bir kez göster.
  // (Bu değer yalnızca "deploy'u şimdi tetikle" isteğini doğrular; site içeriğine/hesaba erişim sağlamaz.)
  $new = function_exists('random_bytes') ? bin2hex(random_bytes(24)) : bin2hex(openssl_random_pseudo_bytes(24));
  if (@file_put_contents($secretFile, $new, LOCK_EX) === false) {
    logline('HATA: .deploy_hook_secret yazilamadi ('.$secretFile.')');
    say(503, 'Kurulum eksik: home dizinine .deploy_hook_secret yazilamadi — dosya yoneticisinden elle olusturun.');
  }
  @chmod($secretFile, 0600);
  logline('KURULUM: secret uretildi ve bir kez gosterildi');
  say(200, "KURULUM: secret olusturuldu. Asagidaki degeri GitHub webhook ayarindaki Secret alanina yapistirin.\nBu deger bir daha GOSTERILMEYECEK:\n".$new);
}
$secret = trim((string)file_get_contents($secretFile));
if ($secret === '') { logline('HATA: secret dosyasi bos'); say(503, 'Kurulum eksik: .deploy_hook_secret bos.'); }

$payload = file_get_contents('php://input');
$sig = $_SERVER['HTTP_X_HUB_SIGNATURE_256'] ?? '';
$expected = 'sha256='.hash_hmac('sha256', $payload, $secret);
if ($sig === '' || !hash_equals($expected, $sig)) { logline('RED: imza gecersiz ('.($_SERVER['REMOTE_ADDR'] ?? '?').')'); say(403, 'imza gecersiz'); }

$event = $_SERVER['HTTP_X_GITHUB_EVENT'] ?? '';
if ($event === 'ping') { logline('ping OK'); say(200, 'pong'); }
if ($event !== 'push') { logline('yoksayildi: event='.$event); say(200, 'yoksayildi: '.$event); }

$data = json_decode($payload, true);
$ref = (string)($data['ref'] ?? '');
if ($ref !== 'refs/heads/main') { logline('yoksayildi: '.$ref); say(200, 'yoksayildi: sadece main yayinlanir'); }

$deploy = $home.'/site/deploy.sh';
if (!is_file($deploy)) { logline('HATA: deploy.sh yok: '.$deploy); say(500, 'deploy.sh bulunamadi'); }

if (!function_exists('shell_exec') || in_array('shell_exec', array_map('trim', explode(',', (string)ini_get('disable_functions'))), true)) {
  logline('HATA: shell_exec kapali'); say(501, 'shell_exec kapali — hosting panelinden PHP fonksiyon kisitlamasi acilmali (cron yedek olarak calismaya devam eder).');
}

// Arka planda, kilitle sıraya sokarak çalıştır; çıktı deploy.log'a. Webhook hemen 200 döner.
$cmd = 'HOME='.escapeshellarg($home)
     .' nohup flock '.escapeshellarg($home.'/.deploy.lock')
     .' /bin/bash '.escapeshellarg($deploy)
     .' >> '.escapeshellarg($home.'/deploy.log').' 2>&1 &';
shell_exec($cmd);
logline('OK: deploy tetiklendi (commit '.substr((string)($data['after'] ?? ''), 0, 7).')');
say(200, 'deploy tetiklendi');
