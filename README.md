# Wakacje 2026 - 3 plany do wyboru

Planowanie dwutygodniowej podróży dla pary, termin **24.07 - 7.08 (14 dni)**, wylot z Polski, średni standard. Trzy kierunki do porównania, każdy łączy sporty wodne z czymś do obejrzenia:

- **Sycylia** - snorkeling, kajak, rejsy + Etna, barok i teatry greckie.
- **Maroko** - surfing i wiatr Atlantyku + medyny, Atlas i noc na Saharze.
- **Madagaskar** - nurkowanie, snorkeling i sezon na humbaki + lemury i tsingy.

**Interaktywna strona (3 plany, oś czasu dzień po dniu):** https://lukrecjajestbe.github.io/portugalia26/ (deployuje się automatycznie po każdej zmianie na `main`)

## Struktura repo

- **`plan/`** - trzy plany dzień po dniu w markdownie: [`sycylia.md`](plan/sycylia.md), [`maroko.md`](plan/maroko.md), [`madagaskar.md`](plan/madagaskar.md). Każdy kończy się orientacyjną wyceną kosztów dla 2 osób. Zobacz [`plan/README.md`](plan/README.md) dla skrótu porównawczego.
- **`scripts/build_data.py`** - skrypt Pythona (uruchamiany przez `uv run`) generujący dane dla interaktywnej strony z plików w `plan/`.
- **`web/`** - interaktywna prezentacja (React + Vite): zakładki z trzema planami i oś czasu dzień po dniu. Zobacz sekcję niżej.

## Zależności (uv)

Projekt używa [uv](https://docs.astral.sh/uv/) do zarządzania zależnościami Pythona. Instalacja:

```bash
uv sync
```

Skrypt w `scripts/` uruchamia się przez `uv run scripts/build_data.py`, nie bezpośrednio `python3`.

## Interaktywna prezentacja (`web/`)

Jednostronicowa aplikacja React pokazująca trzy plany jako zakładki, każdy jako oś czasu dzień po dniu z wyceną.

Dane dla strony (`web/src/data/data.json`) są generowane z plików markdown w `plan/` - to nie jest osobne źródło prawdy, tylko odbicie tych plików.

```bash
# 1. Wygeneruj dane (za kazdym razem po zmianie plikow w plan/)
uv run scripts/build_data.py

# 2. Zainstaluj zaleznosci frontendu (jednorazowo)
cd web && npm install

# 3. Uruchom lokalnie
npm run dev
```

Otwórz `http://localhost:5173` (albo adres wypisany w terminalu).

## Deploy

Automatyczny - GitHub Actions (`.github/workflows/deploy.yml`) buduje i publikuje stronę na GitHub Pages po każdym pushu do `main`. Nie trzeba nic uruchamiać ręcznie. Szczegóły w sekcji "Deploy" w [`CLAUDE.md`](CLAUDE.md).
