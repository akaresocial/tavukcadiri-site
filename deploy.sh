#!/bin/bash
# tavukcadiri.com — sunucu tarafı otomatik yayın (cron her 5 dk çalıştırır)
# Akış: GitHub'dan fetch → yeni commit varsa ff-merge → dosyaları public_html'e kopyala
# main() sarmalayıcı: merge script'in kendisini güncellese bile bu çalıştırma bütün kalır.
set -u
main() {
  REPO="$HOME/site"
  PUB="$HOME/public_html"
  MARKER="$HOME/.last_deploy_commit"

  cd "$REPO" || exit 1
  git fetch -q origin main || exit 1
  REMOTE=$(git rev-parse origin/main)
  LAST=$(cat "$MARKER" 2>/dev/null || echo "yok")
  [ "$REMOTE" = "$LAST" ] && exit 0

  git merge -q --ff-only origin/main || exit 1

  # Yayın: repo kökündeki HER ŞEY, hariç tutulanlar dışında (yeni klasörler otomatik dahil)
  cp -f .htaccess "$PUB/" 2>/dev/null
  for item in *; do
    case "$item" in
      _kaynak|README.md|deploy.sh|"Tavuk Çadırı Logo.png") continue ;;
    esac
    cp -Rf "$item" "$PUB/" || exit 1
  done

  echo "$REMOTE" > "$MARKER"
  echo "$(date '+%Y-%m-%d %H:%M:%S') yayinlandi: $REMOTE" >> "$HOME/deploy.log"
}
main
