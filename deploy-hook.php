<?php
// tavukcadiri.com — GitHub push webhook tetikleyicisi (saf PHP deploy, shell gerekmez)
//
// Akış: main'e push → GitHub bu adresi çağırır (HMAC-SHA256 imzalı) → hook, push'taki
// commit'in zip arşivini GitHub'dan indirir, açar ve dosyaları public_html'e kopyalar.
// Alastyr'da shell_exec kapalı olduğu için deploy.sh çağrılmaz; cron + deploy.sh
// yedek katman olarak aynen çalışmaya devam eder (aynı hariç-tutma listesi).
//
// KURULUM (tek adım):
//  Secret repoda TUTULMAZ. İlk istekte sunucu rastgele bir secret üretip
//  ~/.deploy_hook_secret dosyasına yazar ve değeri YALNIZCA O YANITTA bir kez gösterir.
//  O değerle GitHub → repo → Settings → Webhooks → Add webhook:
//       Payload URL : https://tavukcadiri.com/deploy-hook.php
//       Content type: application/json
//       Secret      : ilk yanıtta gösterilen değer
//       Events      : Just the push event
//  Rotasyon: sunucudaki ~/.deploy_hook_secret silinir → sonraki ilk istek yeni değer
//  üretip bir kez gösterir → GitHub'daki Secret da aynı değerle güncellenir.
//
// Kayıtlar: ~/deploy-hook.log · son yayınlanan commit: ~/.last_deploy_commit

$repoGit  = 'akaresocial/tavukcadiri-site';
$home     = dirname($_SERVER['DOCUMENT_ROOT']);   // public_html'in bir üstü (home dizini)
$pub      = $_SERVER['DOCUMENT_ROOT'];
$secretFile = $home.'/.deploy_hook_secret';
$log      = $home.'/deploy-hook.log';
// deploy.sh ile aynı hariç-tutma listesi (+ repo yönetim dosyaları)
$exclude  = array('_kaynak','README.md','deploy.sh','Tavuk Çadırı Logo.png','.gitignore','.github','.git');

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
$sha = preg_match('/^[0-9a-f]{40}$/', (string)($data['after'] ?? '')) ? $data['after'] : 'refs/heads/main';

// --- Saf PHP deploy ---
ignore_user_abort(true);
@set_time_limit(300);

// Aynı anda tek deploy: kilidi al (öndeki bitene dek bekler)
$lockFh = fopen($home.'/.deploy.lock', 'c');
if ($lockFh) { flock($lockFh, LOCK_EX); }

$t0 = microtime(true);
$tmpZip = $home.'/.deploy_tmp_'.getmypid().'.zip';
$tmpDir = $home.'/.deploy_tmp_'.getmypid();

// 1) Zip arşivini indir (curl uzantısı; yoksa allow_url_fopen denenir)
$url = 'https://codeload.github.com/'.$repoGit.'/zip/'.$sha;
$ok = false;
if (function_exists('curl_init')) {
  $fh = fopen($tmpZip, 'wb');
  $ch = curl_init($url);
  curl_setopt_array($ch, array(CURLOPT_FILE=>$fh, CURLOPT_FOLLOWLOCATION=>true, CURLOPT_TIMEOUT=>180, CURLOPT_USERAGENT=>'tavukcadiri-deploy-hook'));
  $ok = curl_exec($ch) && curl_getinfo($ch, CURLINFO_HTTP_CODE) === 200;
  curl_close($ch); fclose($fh);
} elseif (ini_get('allow_url_fopen')) {
  $ok = @copy($url, $tmpZip);
}
if (!$ok || !is_file($tmpZip) || filesize($tmpZip) < 1000) {
  @unlink($tmpZip); logline('HATA: zip indirilemedi ('.$url.')');
  say(500, 'zip indirilemedi — cron yedek dongusu yayinlayacak');
}

// 2) Aç
if (!class_exists('ZipArchive')) { @unlink($tmpZip); logline('HATA: ZipArchive yok'); say(501, 'ZipArchive uzantisi kapali — cron yedek dongusu yayinlayacak'); }
$zip = new ZipArchive();
if ($zip->open($tmpZip) !== true || !$zip->extractTo($tmpDir)) { @unlink($tmpZip); logline('HATA: zip acilamadi'); say(500, 'zip acilamadi'); }
$zip->close(); @unlink($tmpZip);
$roots = glob($tmpDir.'/*', GLOB_ONLYDIR);
if (!$roots) { logline('HATA: zip icerigi bos'); say(500, 'zip icerigi bos'); }
$src = $roots[0];

// 3) public_html'e kopyala (hariç-tutma listesi dışında her şey; silinenlere dokunulmaz — deploy.sh ile aynı)
function copy_tree($from, $to){
  $n = 0;
  $items = scandir($from);
  foreach ($items as $it) {
    if ($it === '.' || $it === '..') continue;
    $f = $from.'/'.$it; $t = $to.'/'.$it;
    if (is_dir($f)) { if (!is_dir($t)) @mkdir($t, 0755, true); $n += copy_tree($f, $t); }
    else { if (@copy($f, $t)) $n++; }
  }
  return $n;
}
$copied = 0;
foreach (scandir($src) as $it) {
  if ($it === '.' || $it === '..' || in_array($it, $exclude, true)) continue;
  $f = $src.'/'.$it; $t = $pub.'/'.$it;
  if (is_dir($f)) { if (!is_dir($t)) @mkdir($t, 0755, true); $copied += copy_tree($f, $t); }
  else { if (@copy($f, $t)) $copied++; }
}

// 4) Temizlik + kayıt
function rm_tree($d){
  foreach (scandir($d) as $it) { if ($it==='.'||$it==='..') continue; $p=$d.'/'.$it; is_dir($p) ? rm_tree($p) : @unlink($p); }
  @rmdir($d);
}
rm_tree($tmpDir);
if (preg_match('/^[0-9a-f]{40}$/', $sha)) { @file_put_contents($home.'/.last_deploy_commit', $sha."\n"); }
if ($lockFh) { flock($lockFh, LOCK_UN); fclose($lockFh); }

$sure = round(microtime(true) - $t0, 1);
logline('OK: yayinlandi commit='.substr($sha,0,7).' dosya='.$copied.' sure='.$sure.'sn');
say(200, 'yayinlandi: commit '.substr($sha,0,7).' · '.$copied.' dosya · '.$sure.' sn');
