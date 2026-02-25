#!/bin/bash
# ============================================================
# Let's Encrypt — İlk Sertifika Alma Scripti
#
# Kullanım:
#   1. .env dosyasında DOMAIN ve CERTBOT_EMAIL değerlerini doldur
#   2. nginx/default.conf içindeki "yourdomain.com" ifadelerini
#      kendi alan adınla değiştir
#   3. bash init-letsencrypt.sh
# ============================================================

set -e

# .env'den değişkenleri oku
if [ -f .env ]; then
  export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

DOMAIN="${DOMAIN:?'HATA: .env içinde DOMAIN tanımlı değil'}"
CERTBOT_EMAIL="${CERTBOT_EMAIL:?'HATA: .env içinde CERTBOT_EMAIL tanımlı değil'}"

CERT_PATH="./certbot/conf/live/$DOMAIN"

echo "==> Alan adı : $DOMAIN"
echo "==> E-posta  : $CERTBOT_EMAIL"
echo ""

# ----------------------------------------------------------
# 1. Dizinleri oluştur
# ----------------------------------------------------------
echo "[1/5] Dizinler oluşturuluyor..."
mkdir -p "$CERT_PATH" ./certbot/www

# ----------------------------------------------------------
# 2. Geçici (dummy) sertifika oluştur → nginx ilk kez başlayabilsin
# ----------------------------------------------------------
echo "[2/5] Geçici sertifika oluşturuluyor..."
openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
  -keyout "$CERT_PATH/privkey.pem" \
  -out    "$CERT_PATH/fullchain.pem" \
  -subj   "/CN=localhost" 2>/dev/null

# ----------------------------------------------------------
# 3. nginx'i geçici sertifikayla başlat
# ----------------------------------------------------------
echo "[3/5] nginx başlatılıyor (geçici sertifika ile)..."
docker compose up -d nginx
echo "    nginx ayağa kalkması için 3 saniye bekleniyor..."
sleep 3

# ----------------------------------------------------------
# 4. Geçici sertifikayı sil, gerçek sertifikayı al
# ----------------------------------------------------------
echo "[4/5] Let's Encrypt sertifikası alınıyor: $DOMAIN ..."
rm -rf "./certbot/conf/live/$DOMAIN" \
       "./certbot/conf/archive/$DOMAIN" \
       "./certbot/conf/renewal/$DOMAIN.conf"

docker compose run --rm --entrypoint certbot certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email "$CERTBOT_EMAIL" \
  --agree-tos \
  --no-eff-email \
  -d "$DOMAIN" \
  -d "www.$DOMAIN"

# ----------------------------------------------------------
# 5. nginx'i gerçek sertifikayla yeniden yükle
# ----------------------------------------------------------
echo "[5/5] nginx yeniden yükleniyor..."
docker compose exec nginx nginx -s reload

echo ""
echo "✓ Tamamlandı! https://$DOMAIN adresini ziyaret edebilirsiniz."
