# CLAUDE.md

Instrukcje dla Claude Code dotyczące pracy w tym repo (planowanie podróży po Portugalii).

## Struktura projektu

- `atrakcje/<NN-nazwa>/README.md` - jeden folder na każde miejsce na trasie, ponumerowane w kolejności geograficznej (południe → północ). Każdy plik zawiera:
  - nagłówek `# Nazwa`
  - linię `**Kategoria:** surfing|kultura|oba` zaraz po tytule - `surfing` gdy głównym powodem odwiedzin jest surfing, `kultura` gdy surfingu tam nie ma lub jest nieistotny, `oba` gdy jedno i drugie ma podobną wagę. To pole jest **obowiązkowe i czytane wprost** przez `scripts/generate_csv.py` (nie jest zgadywane z treści).
  - jedną lub więcej linii w formacie: `**Mapa[ (Etykieta)]:** [Otwórz w Google Maps](URL)`, gdzie URL to link postaci `https://www.google.com/maps/search/?api=1&query=LAT,LNG&query_place_id=PLACE_ID`
  - sekcje `## Opis`, `## Atrakcje`, `## Surfing`, `## Praktyczne info`
  - jeśli w danym miejscu nie ma surfingu, sekcja `## Surfing` zaczyna się od słowa `Brak`
- `atrakcje/DLA-POCZATKUJACYCH.md` - lista spotów surfingowych odpowiednich dla początkujących (i tych do ominięcia), aktualizować ręcznie gdy dojdzie nowy spot.
- `plan/` - plany dzień po dniu (markdown) dla poszczególnych wariantów czasowych.
- `atrakcje.csv` - wygenerowany automatycznie z `atrakcje/*/README.md`, nie edytować ręcznie. Plik jest w `.gitignore` (nie trzymamy go w repo) - wygeneruj go lokalnie po sklonowaniu.
- `scripts/generate_csv.py` - skrypt generujący `atrakcje.csv`.
- `scripts/build_data.py` - skrypt generujący `web/src/data/data.json` (dane dla interaktywnej strony) z `atrakcje/*/README.md`, `plan/*.md` i `atrakcje/DLA-POCZATKUJACYCH.md`.
- `scripts/fetch_images.py` - pobiera i kompresuje (max 1600px, JPEG q=78) reprezentatywne zdjęcie dla każdej atrakcji z Wikimedia Commons do `web/public/images/<folder-id>.jpg`. Pomija pobieranie jeśli plik już istnieje - usuń go ręcznie żeby wymusić ponowne pobranie. Zapytania do Wikimedia wymagają nagłówka `User-Agent` (inaczej 403).
- `web/` - interaktywna prezentacja: React + Vite, mapa Leaflet/OpenStreetMap (bez klucza API), karty atrakcji, filtry kategorii, oś czasu planów. Konsumuje `web/src/data/data.json` - nie edytować danych ręcznie, tylko przez `build_data.py`.
- Wszystkie skrypty Pythona uruchamiane są przez `uv run scripts/<nazwa>.py`, zależności zarządzane przez `uv` (`pyproject.toml`, `uv.lock`). Nie używać gołego `python3` ani `pip`.

## Generowanie / regeneracja `atrakcje.csv`

Za każdym razem gdy dodasz nowy folder do `atrakcje/`, zmienisz link do mapy albo zmienisz `**Kategoria:**` w istniejącym pliku, **uruchom ponownie skrypt generujący CSV** zamiast edytować `atrakcje.csv` ręcznie:

```bash
uv run scripts/generate_csv.py
```

Skrypt:
1. Przechodzi po wszystkich folderach `atrakcje/*/`.
2. Z każdego `README.md` wyciąga tytuł (pierwszy nagłówek `# `), linię `**Kategoria:**` (rzuca błąd, jeśli jej brak albo wartość spoza `surfing`/`kultura`/`oba`) oraz wszystkie linie `**Mapa...:** [...](URL)` (parsując `lat,lng` z parametru `query=` w URL).
3. Jeśli plik ma kilka linii `Mapa (Etykieta):`, tworzy osobny wiersz CSV dla każdej lokalizacji, z nazwą w formacie `Tytuł (Etykieta)`.
4. Zapisuje wynik do `atrakcje.csv` w katalogu głównym repo, z kolumnami: `nazwa,folder,lat,lng,kategoria,google_maps_url`.

Jeśli trzeba dodać nowe pole do CSV (np. region, poziom trudności), edytuj `scripts/generate_csv.py`, nie dopisuj kolumn ręcznie w CSV - przy następnym uruchomieniu zostałyby nadpisane.

## Dodawanie nowego miejsca na trasie

1. Stwórz folder `atrakcje/NN-nazwa/` (NN = kolejny numer w kolejności geograficznej, zero-padded jeśli trzeba zachować sortowanie).
2. Napisz `README.md` zgodnie ze strukturą opisaną wyżej, **pamiętając o linii `**Kategoria:**`**. Współrzędne i `place_id` do linku Google Maps zdobądź przez MCP Google Maps (`mcp__google-maps__maps_geocode` lub `mcp__google-maps__maps_search_places`), nie zgaduj ich.
3. Dodaj wpis do listy w `atrakcje/README.md`.
4. Jeśli miejsce nadaje się dla początkujących surferów, dodaj je też do `atrakcje/DLA-POCZATKUJACYCH.md`.
5. Uruchom `uv run scripts/generate_csv.py` oraz `uv run scripts/build_data.py`.
6. Dodaj zapytanie wyszukiwania dla nowego folderu do `SEARCH_QUERIES` w `scripts/fetch_images.py`, uruchom `uv run scripts/fetch_images.py`.

## Interaktywna prezentacja (`web/`)

Frontend to React + Vite (bez TypeScript), zależności npm (nie uv - to warstwa JS, oddzielna od skryptów Pythona). Dane wczytywane statycznie z `web/src/data/data.json` (import JSON w `App.jsx`), generowane przez `scripts/build_data.py` - nigdy nie edytuj tego pliku ręcznie.

Struktura komponentów w `web/src/components/`:
- `MapView.jsx` - mapa Leaflet z pinezkami kolorowanymi wg kategorii
- `AttractionCard.jsx` - karta atrakcji ze zdjęciem, opisem, sekcjami
- `PlanTimeline.jsx` - oś czasu dzień-po-dniu dla wariantu planu
- `BeginnerGuide.jsx` - przewodnik dla początkujących
- `MarkdownText.jsx` - lekki renderer markdown (bold, linki, listy `- `) używany wszędzie tam, gdzie tekst pochodzi z plików `.md` - nie wyświetlaj surowego tekstu z `data.json` bez przepuszczenia przez ten komponent, bo będą widoczne gwiazdki `**...**`

Uruchomienie lokalne: `cd web && npm install && npm run dev`. Build produkcyjny: `npm run build` (output do `web/dist/`, w `.gitignore`).

## Wersjonowanie

Repo używa jednocześnie git i jj (kolokowane, `jj git init --colocate`). Zmiany commituj przez `git commit`, jj automatycznie widzi nowy commit jako HEAD.
