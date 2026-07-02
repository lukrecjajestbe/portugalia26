#!/usr/bin/env bash
# Buduje dane, zdjecia i strone, potem publikuje web/dist na branchu gh-pages.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Generuje dane z atrakcje/ i plan/"
uv run scripts/build_data.py

echo "==> Pobieram brakujace zdjecia (Wikimedia Commons)"
uv run scripts/fetch_images.py

echo "==> Instaluje zaleznosci frontendu"
cd web
npm install

echo "==> Build produkcyjny"
npm run build

echo "==> Publikuje web/dist na branchu gh-pages"
npm run deploy

echo "==> Gotowe. Strona bedzie dostepna pod https://lukrecjajestbe.github.io/portugalia26/ (moze zajac kilka minut przy pierwszym deployu)"
