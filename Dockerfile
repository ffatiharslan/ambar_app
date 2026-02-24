# ============================================================
# Stage 1 — Tailwind CSS derle
# ============================================================
FROM node:20-alpine AS css-builder

WORKDIR /build

# Bağımlılıkları önce kopyala (layer cache için)
COPY ambar/package.json ./
RUN npm install

# Tailwind config ve kaynak CSS
COPY ambar/tailwind.config.js ./
COPY ambar/ambarapp/static/css/input.css ambarapp/static/css/input.css

# Tailwind template taraması için HTML şablonları
COPY ambar/templates/ templates/

# Minify edilmiş CSS üret
RUN npx tailwindcss \
    -i ambarapp/static/css/input.css \
    -o ambarapp/static/css/output.css \
    --minify

# ============================================================
# Stage 2 — Django uygulaması
# ============================================================
FROM python:3.13-slim

# Bytecode ve buffering'i kapat
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Üretim için ortam değişkenleri (docker run -e ile geçersiz kılınabilir)
ENV DJANGO_SECRET_KEY="degistir-bunu-gercek-bir-secret-key-ile" \
    DJANGO_DEBUG="0" \
    DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"

WORKDIR /app

# Python bağımlılıklarını yükle
COPY ambar/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY ambar/ .

# Tailwind stage'inden derlenen CSS'i al
COPY --from=css-builder /build/ambarapp/static/css/output.css \
     ambarapp/static/css/output.css

# Statik dosyaları topla
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# migrate + gunicorn ile başlat
CMD ["sh", "-c", \
     "python manage.py migrate --noinput && \
      gunicorn ambar.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 60"]
