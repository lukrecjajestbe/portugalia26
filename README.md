# Portugalia 2026 - road trip surfingowy

Planowanie podróży po Portugalii: Faro (przylot, wynajem auta) → Algarve → Alentejo → Ericeira/Peniche → Lizbona (+ okolice) → Nazaré → Aveiro → Porto (zwrot auta, wylot). Nacisk na surfing.

**Mapa Google (My Maps) ze wszystkimi punktami:** https://www.google.com/maps/d/u/1/edit?mid=1xCJXVbxLQ7gCA_lBUf9ftX1pNqmFcPs&usp=sharing

## Struktura repo

- **`atrakcje/`** - 20 folderów, po jednym na każde miejsce na trasie. Każdy zawiera `README.md` z opisem, kategorią (`surfing`/`kultura`/`oba`), sekcją o surfingu i linkiem do Google Maps. Zobacz [`atrakcje/README.md`](atrakcje/README.md) dla pełnej listy w kolejności geograficznej.
- **`atrakcje/DLA-POCZATKUJACYCH.md`** - wybór spotów surfingowych odpowiednich dla początkujących (i tych do ominięcia), przygotowany pod nasz poziom.
- **`plan/`** - plany podróży dzień po dniu dla dwóch wariantów czasowych: [18.07-31.07 (14 dni)](plan/wariant-a-18-31-lipca.md) i [21.07-31.07 (11 dni)](plan/wariant-b-21-31-lipca.md).
- **`atrakcje.csv`** - wygenerowany lokalnie (nie jest w repo, patrz niżej), zawiera wszystkie atrakcje w jednym pliku CSV (nazwa, folder, lat, lng, kategoria, link do mapy) - gotowe do importu np. do Google My Maps.
- **`scripts/`** - skrypty Pythona (uruchamiane przez `uv run`) generujące `atrakcje.csv` i dane dla interaktywnej strony.
- **`web/`** - interaktywna prezentacja (React + Vite): mapa, karty atrakcji ze zdjęciami, filtry kategorii, oś czasu obu wariantów planu. Zobacz sekcję "Interaktywna prezentacja" niżej.

## Zależności (uv)

Projekt używa [uv](https://docs.astral.sh/uv/) do zarządzania zależnościami Pythona. Środowisko i zależności są już zdefiniowane w `pyproject.toml` - żeby je zainstalować:

```bash
uv sync
```

Wszystkie skrypty w `scripts/` uruchamia się przez `uv run scripts/<nazwa>.py`, nie bezpośrednio `python3`.

## Generowanie `atrakcje.csv`

Plik `atrakcje.csv` nie jest trzymany w repo (jest w `.gitignore`) - wygeneruj go lokalnie:

```bash
uv run scripts/generate_csv.py
```

Zobacz sekcję "Generowanie / regeneracja `atrakcje.csv`" w [`CLAUDE.md`](CLAUDE.md) po szczegóły i zasady dodawania nowych miejsc.

## Interaktywna prezentacja (`web/`)

Jednostronicowa aplikacja React pokazująca mapę, karty atrakcji ze zdjęciami (pobranymi automatycznie z Wikimedia Commons), filtry po kategorii oraz oś czasu dla obu wariantów planu.

Dane dla strony (`web/src/data/data.json`) są generowane z plików markdown w `atrakcje/` i `plan/` - to nie jest osobne źródło prawdy, tylko odbicie tych plików.

```bash
# 1. Wygeneruj dane (za każdym razem po zmianie plikow w atrakcje/ lub plan/)
uv run scripts/build_data.py

# 2. (jednorazowo, albo po zmianie zdjec) pobierz zdjecia z Wikimedia Commons
uv run scripts/fetch_images.py

# 3. Zainstaluj zaleznosci frontendu (jednorazowo)
cd web && npm install

# 4. Uruchom lokalnie
npm run dev
```

Otwórz `http://localhost:5173` (albo adres wypisany w terminalu).

## Import do Google My Maps

1. Wejdź na [mymaps.google.com](https://mymaps.google.com) i utwórz nową mapę.
2. Kliknij "Importuj" w panelu warstwy i wskaż plik `atrakcje.csv`.
3. Jako kolumny współrzędnych wybierz `lat` i `lng`, jako tytuł markera `nazwa`.
4. Użyj kolumny `kategoria` (`surfing`/`kultura`/`oba`) do pokolorowania punktów - Google My Maps pozwala stylizować markery wg wartości kolumny, dzięki czemu łatwo odróżnisz miejsca surfingowe od czysto turystycznych.

## Wynajem auta i inne uwagi praktyczne

Zobacz sekcję "Wspólne założenia" w [`plan/README.md`](plan/README.md) - m.in. o myto Via Verde, opłacie za zwrot auta w Porto (one-way) i biletach do Sintry/Livraria Lello, które trzeba kupić z wyprzedzeniem.
