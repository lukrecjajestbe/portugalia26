#!/usr/bin/env python3
"""Pobiera reprezentatywne zdjecie dla kazdego dnia planu z Wikimedia Commons.

Zapisuje do web/public/images/<plan_id>-<NN>.jpg. Pomija pobieranie jesli
plik juz istnieje - usun go recznie zeby wymusic ponowne pobranie.
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import httpx
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "web" / "public" / "images"

HEADERS = {"User-Agent": "WakacjeTripPlanner/1.0 (jakub@lite.tech)"}
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
MAX_WIDTH = 1600
JPEG_QUALITY = 78

SEARCH_QUERIES: dict[str, str] = {
    "sycylia-01": "Catania Piazza del Duomo Sicily",
    "sycylia-02": "Mount Etna volcano Sicily",
    "sycylia-03": "Isola Bella Taormina Sicily",
    "sycylia-04": "Ortygia Syracuse Sicily cathedral",
    "sycylia-05": "Neapolis archaeological park Syracuse",
    "sycylia-06": "Noto Sicily baroque",
    "sycylia-07": "Ragusa Ibla Sicily",
    "sycylia-08": "Valley of the Temples Agrigento",
    "sycylia-09": "Scala dei Turchi Sicily",
    "sycylia-10": "Favignana Cala Rossa Aegadian",
    "sycylia-11": "Erice Sicily medieval town",
    "sycylia-12": "Zingaro nature reserve Sicily",
    "sycylia-13": "Cefalu Sicily cathedral beach",
    "sycylia-14": "Palermo Quattro Canti Sicily",
    "maroko-01": "Jemaa el-Fnaa Marrakech night",
    "maroko-02": "Bahia Palace Marrakech",
    "maroko-03": "Essaouira medina ramparts Morocco",
    "maroko-04": "Essaouira kitesurfing beach Morocco",
    "maroko-05": "Taghazout Morocco",
    "maroko-06": "surfer ocean wave",
    "maroko-07": "Paradise Valley Agadir Morocco",
    "maroko-08": "Marrakech riad rooftop Atlas",
    "maroko-09": "Setti Fatma Ourika Morocco",
    "maroko-10": "Ait Benhaddou Morocco kasbah",
    "maroko-11": "Dades Gorge Morocco valley",
    "maroko-12": "Erg Chebbi dunes camel Morocco",
    "maroko-13": "Sahara desert sunrise dunes Morocco",
    "maroko-14": "Marrakech souk market Morocco",
    "madagaskar-01": "Antananarivo Madagascar city",
    "madagaskar-02": "Nosy Be beach Madagascar",
    "madagaskar-03": "sea turtle coral reef snorkeling",
    "madagaskar-04": "Humpback whale breaching ocean",
    "madagaskar-05": "Nosy Komba lemur Madagascar",
    "madagaskar-06": "Mont Passot Nosy Be lakes",
    "madagaskar-07": "Ankarana National Park Madagascar tsingy",
    "madagaskar-08": "Tsingy Ankarana limestone Madagascar",
    "madagaskar-09": "vanilla pods drying",
    "madagaskar-10": "Nosy Be Madagascar",
    "madagaskar-11": "Rova Antananarivo palace Madagascar",
    "madagaskar-12": "Andasibe Mantadia rainforest Madagascar",
    "madagaskar-13": "Indri lemur Andasibe Madagascar",
    "madagaskar-14": "Baobab avenue Madagascar sunset",
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
            "gsrlimit": 8,
        },
        headers=HEADERS,
        timeout=15,
    )
    response.raise_for_status()
    pages = response.json().get("query", {}).get("pages", {})
    ordered = sorted(pages.values(), key=lambda p: p.get("index", 999))
    for page in ordered:
        original = page.get("original")
        if original and re.search(
            r"\.(jpe?g|png)$", original["source"], re.IGNORECASE
        ):
            return original["source"]
    return None


def download_and_resize(url: str, dest: Path) -> None:
    with httpx.stream(
        "GET", url, headers=HEADERS, timeout=30, follow_redirects=True
    ) as response:
        response.raise_for_status()
        raw = b"".join(response.iter_bytes())

    image = Image.open(io.BytesIO(raw)).convert("RGB")
    if image.width > MAX_WIDTH:
        new_height = round(image.height * MAX_WIDTH / image.width)
        image = image.resize((MAX_WIDTH, new_height), Image.LANCZOS)
    image.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    for image_id, query in SEARCH_QUERIES.items():
        dest = IMAGES_DIR / f"{image_id}.jpg"
        if dest.exists():
            print(f"pomijam (juz istnieje): {image_id}")
            continue

        try:
            image_url = find_image_url(query)
            if not image_url:
                print(f"BRAK wyniku dla: {image_id} ({query})")
                continue
            download_and_resize(image_url, dest)
            print(f"OK {image_id} <- {image_url}")
        except httpx.HTTPError as exc:
            print(f"BLAD {image_id}: {exc}")


if __name__ == "__main__":
    main()
