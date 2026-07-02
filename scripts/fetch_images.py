#!/usr/bin/env python3
"""Pobiera reprezentatywne zdjecie dla kazdej atrakcji z Wikimedia Commons.

Zapisuje do web/public/images/<folder-id>.jpg. Pomija pobieranie jesli
plik juz istnieje - usun go recznie zeby wymusic ponowne pobranie.
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import httpx
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ATRAKCJE_DIR = ROOT / "atrakcje"
IMAGES_DIR = ROOT / "web" / "public" / "images"

HEADERS = {"User-Agent": "PortugaliaTripPlanner/1.0 (jakub@lite.tech)"}
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
MAX_WIDTH = 1600
JPEG_QUALITY = 78

SEARCH_QUERIES: dict[str, str] = {
    "01-faro": "Faro Portugal old town",
    "02-lagos": "Ponta da Piedade Lagos Portugal",
    "03-sagres-cabo-sao-vicente": "Cabo de Sao Vicente lighthouse",
    "04-praia-do-amado": "Praia do Amado beach Portugal",
    "05-arrifana": "Praia da Arrifana Portugal",
    "06-zambujeira-do-mar": "Zambujeira do Mar Portugal",
    "07-vila-nova-de-milfontes": "Vila Nova de Milfontes Portugal",
    "08-ericeira": "Ericeira Portugal town",
    "09-peniche-baleal": "Baleal Peniche Portugal",
    "10-obidos": "Obidos Portugal walls",
    "11-sintra": "Palacio da Pena Sintra",
    "12-cabo-da-roca": "Cabo da Roca cliff Portugal",
    "13-lizbona": "Lisbon Alfama tram",
    "14-costa-da-caparica": "Costa da Caparica beach Portugal",
    "15-arrabida": "Praia da Portinho da Arrabida Portugal",
    "16-nazare": "Nazare Portugal beach cliff",
    "17-sao-pedro-de-moel": "Sao Pedro de Moel Portugal",
    "18-aveiro-costa-nova": "Costa Nova striped houses Portugal",
    "19-porto": "Porto Ribeira Douro river",
    "20-matosinhos": "Praia de Matosinhos Portugal",
}


def find_image_url(query: str) -> str | None:
    response = httpx.get(
        COMMONS_API,
        params={
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "piprop": "original",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": 6,
            "gsrlimit": 5,
        },
        headers=HEADERS,
        timeout=15,
    )
    response.raise_for_status()
    pages = response.json().get("query", {}).get("pages", {})
    for page in pages.values():
        original = page.get("original")
        if original and re.search(r"\.(jpe?g|png)$", original["source"], re.IGNORECASE):
            return original["source"]
    return None


def download_and_resize(url: str, dest: Path) -> None:
    with httpx.stream("GET", url, headers=HEADERS, timeout=30, follow_redirects=True) as response:
        response.raise_for_status()
        raw = b"".join(response.iter_bytes())

    image = Image.open(io.BytesIO(raw)).convert("RGB")
    if image.width > MAX_WIDTH:
        new_height = round(image.height * MAX_WIDTH / image.width)
        image = image.resize((MAX_WIDTH, new_height), Image.LANCZOS)
    image.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    for folder_id, query in SEARCH_QUERIES.items():
        dest = IMAGES_DIR / f"{folder_id}.jpg"
        if dest.exists():
            print(f"pomijam (juz istnieje): {folder_id}")
            continue

        try:
            image_url = find_image_url(query)
            if not image_url:
                print(f"BRAK wyniku dla: {folder_id} ({query})")
                continue
            download_and_resize(image_url, dest)
            print(f"OK {folder_id} <- {image_url}")
        except httpx.HTTPError as exc:
            print(f"BLAD {folder_id}: {exc}")


if __name__ == "__main__":
    main()
