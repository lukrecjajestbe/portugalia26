# CLAUDE.md

Instrukcje dla Claude Code dotyczące pracy w tym repo (planowanie podróży po Portugalii).

## Struktura projektu

- `atrakcje/<NN-nazwa>/README.md` - jeden folder na każde miejsce na trasie, ponumerowane w kolejności geograficznej (południe → północ). Każdy plik zawiera:
  - nagłówek `# Nazwa`
  - jedną lub więcej linii w formacie: `**Mapa[ (Etykieta)]:** [Otwórz w Google Maps](URL)`, gdzie URL to link postaci `https://www.google.com/maps/search/?api=1&query=LAT,LNG&query_place_id=PLACE_ID`
  - sekcje `## Opis`, `## Atrakcje`, `## Surfing`, `## Praktyczne info`
  - jeśli w danym miejscu nie ma surfingu, sekcja `## Surfing` zaczyna się od słowa `Brak`
- `plan/` - plany dzień po dniu (markdown) dla poszczególnych wariantów czasowych.
- `atrakcje.csv` - wygenerowany automatycznie z `atrakcje/*/README.md`, nie edytować ręcznie.
- `scripts/generate_csv.py` - skrypt generujący `atrakcje.csv`.

## Generowanie / regeneracja `atrakcje.csv`

Za każdym razem gdy dodasz nowy folder do `atrakcje/`, zmienisz link do mapy albo zmienisz sekcję `## Surfing` w istniejącym pliku, **uruchom ponownie skrypt generujący CSV** zamiast edytować `atrakcje.csv` ręcznie:

```bash
python3 scripts/generate_csv.py
```

Skrypt:
1. Przechodzi po wszystkich folderach `atrakcje/*/`.
2. Z każdego `README.md` wyciąga tytuł (pierwszy nagłówek `# `), wszystkie linie `**Mapa...:** [...](URL)` (parsując `lat,lng` z parametru `query=` w URL) oraz sprawdza, czy sekcja `## Surfing` istnieje i nie zaczyna się od słowa "Brak" (kolumna `surfing`: `tak`/`nie`).
3. Jeśli plik ma kilka linii `Mapa (Etykieta):`, tworzy osobny wiersz CSV dla każdej lokalizacji, z nazwą w formacie `Tytuł (Etykieta)`.
4. Zapisuje wynik do `atrakcje.csv` w katalogu głównym repo, z kolumnami: `nazwa,folder,lat,lng,surfing,google_maps_url`.

Jeśli trzeba dodać nowe pole do CSV (np. kategorię, region), edytuj `scripts/generate_csv.py`, nie dopisuj kolumn ręcznie w CSV - przy następnym uruchomieniu zostałyby nadpisane.

## Dodawanie nowego miejsca na trasie

1. Stwórz folder `atrakcje/NN-nazwa/` (NN = kolejny numer w kolejności geograficznej, zero-padded jeśli trzeba zachować sortowanie).
2. Napisz `README.md` zgodnie ze strukturą opisaną wyżej. Współrzędne i `place_id` do linku Google Maps zdobądź przez MCP Google Maps (`mcp__google-maps__maps_geocode` lub `mcp__google-maps__maps_search_places`), nie zgaduj ich.
3. Dodaj wpis do listy w `atrakcje/README.md`.
4. Uruchom `python3 scripts/generate_csv.py`.

## Wersjonowanie

Repo używa jednocześnie git i jj (kolokowane, `jj git init --colocate`). Zmiany commituj przez `git commit`, jj automatycznie widzi nowy commit jako HEAD.
