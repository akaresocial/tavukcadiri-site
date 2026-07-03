#!/bin/bash
# tavukcadiri.com — sunucu tarafı otomatik yayın (cron her 5 dk çalıştırır)
# Akış: GitHub'dan fetch → yeni commit varsa ff-merge → dosyaları public_html'e kopyala
set -u
REPO="$HOME/site"
PUB="$HOME/public_html"
MARKER="$HOME/.last_deploy_commit"

cd "$REPO" || exit 1
git fetch -q origin main || exit 1
REMOTE=$(git rev-parse origin/main)
LAST=$(cat "$MARKER" 2>/dev/null || echo "yok")

# Yeni commit yoksa ve daha önce en az bir kez yayınlandıysa çık
[ "$REMOTE" = "$LAST" ] && exit 0

git merge -q --ff-only origin/main || exit 1

cp -f index.html 404.html robots.txt sitemap.xml .htaccess "$PUB/" || exit 1
cp -Rf assets "$PUB/"
cp -Rf 500-tavukluk-tavuk-cadiri 750-tavukluk-tavuk-cadiri 1000-tavukluk-tavuk-cadiri 2000-tavukluk-tavuk-cadiri "$PUB/"
cp -Rf fiyatlar hakkimizda iletisim kvkk gizlilik "$PUB/"

echo "$REMOTE" > "$MARKER"
echo "$(date '+%Y-%m-%d %H:%M:%S') yayinlandi: $REMOTE" >> "$HOME/deploy.log"
