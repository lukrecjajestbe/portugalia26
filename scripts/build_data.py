#!/usr/bin/env python3
"""Generuje web/src/data/data.json na podstawie atrakcje/ i plan/.

Jedno zrodlo prawdy to pliki markdown - ten skrypt je parsuje i sklada
w jeden JSON konsumowany przez frontend (web/).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATRAKCJE_DIR = ROOT / "atrakcje"
PLAN_DIR = ROOT / "plan"
OUTPUT_JSON = ROOT / "web" / "src" / "data" / "data.json"

KATEGORIA_RE = re.compile(r"\*\*Kategoria:\*\*\s*(?P<kategoria>\S+)")
MAPA_LINE_RE = re.compile(
    r"\*\*Mapa(?: \((?P<label>[^)]+)\))?:\*\*\s*\[[^\]]+\]\((?P<url>https://\S+?)\)"
)
QUERY_LATLNG_RE = re.compile(r"query=(?P<lat>-?\d+\.\d+),(?P<lng>-?\d+\.\d+)")
SECTION_RE = re.compile(r"^## (?P<heading>.+)$", re.MULTILINE)
VALID_KATEGORIE = {"surfing", "kultura", "oba"}


def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_kategoria(text: str, folder_name: str) -> str:
    match = KATEGORIA_RE.search(text)
    if not match:
        msg = f"Brak linii **Kategoria:** w {folder_name}/README.md"
        raise ValueError(msg)
    kategoria = match.group("kategoria")
    if kategoria not in VALID_KATEGORIE:
        msg = (
            f"Nieznana kategoria '{kategoria}' w {folder_name}/README.md "
            f"(dozwolone: {VALID_KATEGORIE})"
        )
        raise ValueError(msg)
    return kategoria


def extract_locations(text: str) -> list[dict]:
    locations = []
    for match in MAPA_LINE_RE.finditer(text):
        url = match.group("url")
        latlng_match = QUERY_LATLNG_RE.search(url)
        if not latlng_match:
            continue
        locations.append(
            {
                "label": match.group("label"),
                "lat": float(latlng_match.group("lat")),
                "lng": float(latlng_match.group("lng")),
                "google_maps_url": url,
            }
        )
    return locations


def extract_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(SECTION_RE.finditer(text))
    for i, match in enumerate(matches):
        heading = match.group("heading").strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[heading] = text[start:end].strip()
    return sections


def build_attractions() -> list[dict]:
    attractions = []
    folders = sorted(p for p in ATRAKCJE_DIR.iterdir() if p.is_dir())

    for folder in folders:
        readme_path = folder / "README.md"
        if not readme_path.exists():
            continue

        text = readme_path.read_text(encoding="utf-8")
        sections = extract_sections(text)
        surfing_section = sections.get("Surfing", "")

        attractions.append(
            {
                "id": folder.name,
                "order": int(folder.name.split("-", 1)[0]),
                "title": extract_title(text),
                "kategoria": extract_kategoria(text, folder.name),
                "locations": extract_locations(text),
                "opis": sections.get("Opis", ""),
                "atrakcje": sections.get("Atrakcje", ""),
                "surfing": surfing_section,
                "ma_surfing": bool(surfing_section) and not surfing_section.startswith("Brak"),
                "praktyczne_info": sections.get("Praktyczne info", ""),
                "image": f"images/{folder.name}.jpg",
            }
        )

    attractions.sort(key=lambda a: a["order"])
    return attractions


DAY_ROW_RE = re.compile(
    r"^\|\s*(?P<dzien>\d+)\s*\|\s*(?P<data>[^|]+)\|\s*(?P<miejsce>[^|]+)\|\s*(?P<plan>[^|]+)\|\s*$",
    re.MULTILINE,
)


def build_plan(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    title = extract_title(text)
    intro_match = re.search(r"^# .+\n\n(?P<intro>.+?)\n\n\|", text, re.DOTALL)
    intro = intro_match.group("intro").strip() if intro_match else ""

    days = []
    for match in DAY_ROW_RE.finditer(text):
        days.append(
            {
                "dzien": int(match.group("dzien")),
                "data": match.group("data").strip(),
                "miejsce": match.group("miejsce").strip(),
                "plan": match.group("plan").strip(),
            }
        )

    uwagi_match = re.search(r"## Uwagi.*?\n(?P<body>.+)\Z", text, re.DOTALL)
    uwagi = uwagi_match.group("body").strip() if uwagi_match else ""

    return {"title": title, "intro": intro, "dni": days, "uwagi": uwagi}


def build_beginner_guide() -> dict:
    path = ATRAKCJE_DIR / "DLA-POCZATKUJACYCH.md"
    text = path.read_text(encoding="utf-8")
    sections = extract_sections(text)
    return {
        "rekomendowane": sections.get("Rekomendowane dla początkujących (w kolejności trasy)", ""),
        "unikac": sections.get(
            "Zdecydowanie NIE dla początkujących (ominąć wodę, można tylko popatrzeć)", ""
        ),
        "rezerwacja": sections.get("Rekomendacja rezerwacji lekcji", ""),
    }


def main() -> None:
    data = {
        "atrakcje": build_attractions(),
        "plany": {
            "wariant_a": build_plan(PLAN_DIR / "wariant-a-18-31-lipca.md"),
            "wariant_b": build_plan(PLAN_DIR / "wariant-b-21-31-lipca.md"),
        },
        "dla_poczatkujacych": build_beginner_guide(),
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Zapisano {len(data['atrakcje'])} atrakcji do {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
