#!/usr/bin/env python3
"""Generuje atrakcje.csv na podstawie plikow atrakcje/*/README.md.

Kazdy plik README.md moze zawierac jedna lub wiecej linii w formacie:
    **Mapa[ (Nazwa)]:** [Otworz w Google Maps](URL)

Z kazdej takiej linii wyciagana jest lat/lng z parametru query= w URL.
Kategoria (surfing / kultura / oba) wykrywana jest na podstawie obecnosci
naglowka "## Surfing" w pliku.
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATRAKCJE_DIR = ROOT / "atrakcje"
OUTPUT_CSV = ROOT / "atrakcje.csv"

MAPA_LINE_RE = re.compile(
    r"\*\*Mapa(?: \((?P<label>[^)]+)\))?:\*\*\s*\[[^\]]+\]\((?P<url>https://\S+?)\)"
)
QUERY_LATLNG_RE = re.compile(r"query=(?P<lat>-?\d+\.\d+),(?P<lng>-?\d+\.\d+)")


def extract_locations(readme_text: str) -> list[dict]:
    locations = []
    for match in MAPA_LINE_RE.finditer(readme_text):
        url = match.group("url")
        label = match.group("label")
        latlng_match = QUERY_LATLNG_RE.search(url)
        if not latlng_match:
            continue
        locations.append(
            {
                "label": label,
                "url": url,
                "lat": latlng_match.group("lat"),
                "lng": latlng_match.group("lng"),
            }
        )
    return locations


def extract_title(readme_text: str) -> str:
    for line in readme_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


SURFING_SECTION_RE = re.compile(r"## Surfing\s*\n(?P<body>.*?)(?=\n## |\Z)", re.DOTALL)


def has_surfing_section(readme_text: str) -> bool:
    match = SURFING_SECTION_RE.search(readme_text)
    if not match:
        return False
    body = match.group("body").strip()
    return not body.startswith("Brak")


def main() -> None:
    rows = []
    folders = sorted(p for p in ATRAKCJE_DIR.iterdir() if p.is_dir())

    for folder in folders:
        readme_path = folder / "README.md"
        if not readme_path.exists():
            continue

        text = readme_path.read_text(encoding="utf-8")
        title = extract_title(text)
        surfing = "tak" if has_surfing_section(text) else "nie"
        locations = extract_locations(text)

        if not locations:
            continue

        for loc in locations:
            name = f"{title} ({loc['label']})" if loc["label"] else title
            rows.append(
                {
                    "nazwa": name,
                    "folder": folder.name,
                    "lat": loc["lat"],
                    "lng": loc["lng"],
                    "surfing": surfing,
                    "google_maps_url": loc["url"],
                }
            )

    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["nazwa", "folder", "lat", "lng", "surfing", "google_maps_url"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Zapisano {len(rows)} wierszy do {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
