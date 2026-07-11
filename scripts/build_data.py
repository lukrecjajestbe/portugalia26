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
    {"id": "sycylia", "file": "sycylia.md", "label": "Sycylia"},
    {"id": "maroko", "file": "maroko.md", "label": "Maroko"},
    {"id": "madagaskar", "file": "madagaskar.md", "label": "Madagaskar"},
]

DAY_ROW_RE = re.compile(
    r"^\|\s*(?P<dzien>\d+)\s*\|\s*(?P<data>[^|]+)\|\s*(?P<miejsce>[^|]+)\|\s*(?P<plan>[^|]+)\|\s*$",
    re.MULTILINE,
)


def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def build_plan(md_path: Path, plan_id: str, label: str) -> dict:
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

    return {
        "id": plan_id,
        "label": label,
        "title": title,
        "intro": intro,
        "dni": days,
        "uwagi": uwagi,
    }


def main() -> None:
    plany = [
        build_plan(PLAN_DIR / p["file"], p["id"], p["label"]) for p in PLANY
    ]
    data = {"plany": plany}

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Zapisano {len(plany)} planow do {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
