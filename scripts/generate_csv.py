#!/usr/bin/env python3
"""Generuje atrakcje.csv na podstawie plikow atrakcje/*/README.md.

Kazdy plik README.md musi zawierac linie:
    **Kategoria:** surfing|kultura|oba

oraz jedna lub wiecej linii w formacie:
    **Mapa[ (Nazwa)]:** [Otworz w Google Maps](URL)

Z kazdej takiej linii wyciagana jest lat/lng z parametru query= w URL.
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATRAKCJE_DIR = ROOT / "atrakcje"
OUTPUT_CSV = ROOT / "atrakcje.csv"

KATEGORIA_RE = re.compile(r"\*\*Kategoria:\*\*\s*(?P<kategoria>\S+)")
MAPA_LINE_RE = re.compile(
    r"\*\*Mapa(?: \((?P<label>[^)]+)\))?:\*\*\s*\[[^\]]+\]\((?P<url>https://\S+?)\)"
)
QUERY_LATLNG_RE = re.compile(r"query=(?P<lat>-?\d+\.\d+),(?P<lng>-?\d+\.\d+)")
VALID_KATEGORIE = {"surfing", "kultura", "oba"}


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


def extract_kategoria(readme_text: str, folder_name: str) -> str:
    match = KATEGORIA_RE.search(readme_text)
    if not match:
        msg = f"Brak linii **Kategoria:** w {folder_name}/README.md"
        raise ValueError(msg)
    kategoria = match.group("kategoria")
    if kategoria not in VALID_KATEGORIE:
        msg = f"Nieznana kategoria '{kategoria}' w {folder_name}/README.md (dozwolone: {VALID_KATEGORIE})"
        raise ValueError(msg)
    return kategoria


def main() -> None:
    rows = []
    folders = sorted(p for p in ATRAKCJE_DIR.iterdir() if p.is_dir())

    for folder in folders:
        readme_path = folder / "README.md"
        if not readme_path.exists():
            continue

        text = readme_path.read_text(encoding="utf-8")
        title = extract_title(text)
        kategoria = extract_kategoria(text, folder.name)
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
                    "kategoria": kategoria,
                    "google_maps_url": loc["url"],
                }
            )

    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["nazwa", "folder", "lat", "lng", "kategoria", "google_maps_url"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Zapisano {len(rows)} wierszy do {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
