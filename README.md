# Portugalia 2026 - road trip surfingowy

Planowanie podróży po Portugalii: Faro (przylot, wynajem auta) → Algarve → Alentejo → Ericeira/Peniche → Lizbona (+ okolice) → Nazaré → Aveiro → Porto (zwrot auta, wylot). Nacisk na surfing.

## Struktura repo

- **`atrakcje/`** - 20 folderów, po jednym na każde miejsce na trasie. Każdy zawiera `README.md` z opisem, sekcją o surfingu i linkiem do Google Maps. Zobacz [`atrakcje/README.md`](atrakcje/README.md) dla pełnej listy w kolejności geograficznej.
- **`plan/`** - plany podróży dzień po dniu dla dwóch wariantów czasowych: [18.07-31.07 (14 dni)](plan/wariant-a-18-31-lipca.md) i [21.07-31.07 (11 dni)](plan/wariant-b-21-31-lipca.md).
- **`atrakcje.csv`** - wszystkie atrakcje z pliku `atrakcje/` w jednym pliku CSV (nazwa, folder, lat, lng, czy jest tam surfing, link do mapy) - gotowe do importu np. do Google My Maps. Zobacz sekcję "Generowanie CSV" w [`CLAUDE.md`](CLAUDE.md) jak go odtworzyć po zmianach w `atrakcje/`.
- **`scripts/generate_csv.py`** - skrypt generujący `atrakcje.csv` na podstawie plików w `atrakcje/*/README.md`.

## Import do Google My Maps

1. Wejdź na [mymaps.google.com](https://mymaps.google.com) i utwórz nową mapę.
2. Kliknij "Importuj" w panelu warstwy i wskaż plik `atrakcje.csv`.
3. Jako kolumny współrzędnych wybierz `lat` i `lng`, jako tytuł markera `nazwa`.
4. Opcjonalnie: użyj kolumny `surfing` do pokolorowania punktów (Google My Maps pozwala stylizować markery wg wartości kolumny).

## Wynajem auta i inne uwagi praktyczne

Zobacz sekcję "Wspólne założenia" w [`plan/README.md`](plan/README.md) - m.in. o myto Via Verde, opłacie za zwrot auta w Porto (one-way) i biletach do Sintry/Livraria Lello, które trzeba kupić z wyprzedzeniem.
