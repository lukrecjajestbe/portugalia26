#!/usr/bin/env python3
"""Generuje web/src/data/data.json na podstawie plan/.

Jedno zrodlo prawdy to pliki markdown w plan/ - ten skrypt je parsuje
i sklada w jeden JSON konsumowany przez frontend (web/).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN_DIR = ROOT / "plan"
OUTPUT_JSON = ROOT / "web" / "src" / "data" / "data.json"

PLANY = [
    {"id": "maroko", "file": "maroko.md", "label": "Maroko"},
]

DAY_ROW_RE = re.compile(
    r"^\|\s*(?P<dzien>\d+)\s*\|\s*(?P<data>[^|]+)\|\s*(?P<miejsce>[^|]+)\|\s*(?P<plan>[^|]+)\|\s*$",
    re.MULTILINE,
)
TABLE_ROW_RE = re.compile(r"^\|(?P<cells>.+)\|\s*$")
TABLE_SEP_RE = re.compile(r"^\|[\s:|-]+\|\s*$")


def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_intro(text: str) -> str:
    lines = text.splitlines()
    intro: list[str] = []
    started = False
    for line in lines:
        if line.startswith("# "):
            started = True
            continue
        if not started:
            continue
        if line.startswith("|") or line.startswith("## "):
            break
        intro.append(line)
    return "\n".join(intro).strip()


def extract_days(text: str) -> list[dict]:
    days = []
    for match in DAY_ROW_RE.finditer(text):
        if match.group("dzien") == "" or not match.group("dzien").isdigit():
            continue
        days.append(
            {
                "dzien": int(match.group("dzien")),
                "data": match.group("data").strip(),
                "miejsce": match.group("miejsce").strip(),
                "plan": match.group("plan").strip(),
            }
        )
    return days


def _row_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def extract_koszty(uwagi_text: str) -> dict:
    lines = uwagi_text.splitlines()
    rows: list[list[str]] = []
    header: list[str] = []
    in_table = False
    for line in lines:
        if TABLE_SEP_RE.match(line):
            in_table = True
            continue
        if TABLE_ROW_RE.match(line):
            cells = _row_cells(line)
            if not in_table and not header:
                header = cells
                continue
            if in_table:
                rows.append(cells)
        elif in_table:
            break
    if not rows:
        return {}
    return {"header": header, "rows": rows}


def clean_uwagi(uwagi_text: str) -> list[str]:
    out: list[str] = []
    for raw in uwagi_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if TABLE_ROW_RE.match(line) or TABLE_SEP_RE.match(line):
            continue
        if line.startswith("**Szacunkowy koszt"):
            continue
        out.append(line)
    return out


def extract_lot(text: str) -> dict:
    match = re.search(r"## Lot\s*\n(?P<body>.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not match:
        return {}
    intro_lines: list[str] = []
    punkty: list[str] = []
    for raw in match.group("body").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("- "):
            punkty.append(line[2:].strip())
        elif not punkty:
            intro_lines.append(line)
    return {"intro": " ".join(intro_lines), "punkty": punkty}


def extract_transport(text: str) -> dict:
    match = re.search(
        r"## Transport\s*\n(?P<body>.*?)(?=\n## |\Z)", text, re.DOTALL
    )
    if not match:
        return {}
    intro_lines: list[str] = []
    punkty: list[str] = []
    for raw in match.group("body").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("- "):
            punkty.append(line[2:].strip())
        elif not punkty:
            intro_lines.append(line)
    return {"intro": " ".join(intro_lines), "punkty": punkty}


def extract_noclegi(text: str) -> dict:
    match = re.search(
        r"## Noclegi\s*\n(?P<body>.*?)(?=\n## |\Z)", text, re.DOTALL
    )
    if not match:
        return {}
    body = match.group("body")

    intro_lines: list[str] = []
    rows: list[list[str]] = []
    in_table = False
    for line in body.splitlines():
        if TABLE_SEP_RE.match(line):
            in_table = True
            continue
        if TABLE_ROW_RE.match(line):
            cells = _row_cells(line)
            if not in_table:
                continue
            rows.append(cells)
        elif not in_table and line.strip():
            intro_lines.append(line.strip())

    grupy: list[dict] = []
    index: dict[str, dict] = {}
    for cells in rows:
        if len(cells) < 8:
            continue
        miejsce, nocleg, transport, hotel, ocena, cena, cecha, link = cells[:8]
        if miejsce not in index:
            grupa = {
                "miejsce": miejsce,
                "nocleg": nocleg,
                "transport": transport,
                "hotele": [],
            }
            index[miejsce] = grupa
            grupy.append(grupa)
        index[miejsce]["hotele"].append(
            {
                "nazwa": hotel,
                "ocena": ocena,
                "cena": cena,
                "cecha": cecha,
                "link": link,
            }
        )

    return {"intro": " ".join(intro_lines), "grupy": grupy}


def build_plan(md_path: Path, plan_id: str, label: str) -> dict:
    text = md_path.read_text(encoding="utf-8")

    days = extract_days(text)
    for day in days:
        day["image"] = f"images/{plan_id}-{day['dzien']:02d}.jpg"

    uwagi_match = re.search(r"## Uwagi.*?\n(?P<body>.+)\Z", text, re.DOTALL)
    uwagi_text = uwagi_match.group("body").strip() if uwagi_match else ""

    return {
        "id": plan_id,
        "label": label,
        "title": extract_title(text),
        "intro": extract_intro(text),
        "lot": extract_lot(text),
        "transport": extract_transport(text),
        "dni": days,
        "noclegi": extract_noclegi(text),
        "koszty": extract_koszty(uwagi_text),
        "uwagi": clean_uwagi(uwagi_text),
    }


def main() -> None:
    plany = [build_plan(PLAN_DIR / p["file"], p["id"], p["label"]) for p in PLANY]
    data = {"plany": plany}

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Zapisano {len(plany)} planow do {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
