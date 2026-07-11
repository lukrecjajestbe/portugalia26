# CLAUDE.md

Instrukcje dla Claude Code dotyczące pracy w tym repo (planowanie dwutygodniowych wakacji, 3 kierunki do wyboru: Sycylia, Maroko, Madagaskar; termin 24.07 - 7.08).

## Struktura projektu

- `plan/<kierunek>.md` - jeden plik na każdy kierunek (`sycylia.md`, `maroko.md`, `madagaskar.md`), plan dzień po dniu. Każdy plik zawiera:
  - nagłówek `# Nazwa: 24.07 - 7.08 (14 dni)`
  - akapit wprowadzenia (intro) tuż pod tytułem
  - tabelę dni w formacie `| Dzień | Data | Miejsce (nocleg) | Plan |` (parsowaną wprost przez `scripts/build_data.py` - kolejność i liczba kolumn są sztywne)
  - sekcję zaczynającą się od `## Uwagi` z orientacyjną wyceną kosztów dla 2 osób (tabela) i praktycznymi uwagami
- `plan/README.md` - skrót porównawczy trzech kierunków, aktualizować gdy zmieni się plan.
- `scripts/build_data.py` - skrypt generujący `web/src/data/data.json` (dane dla interaktywnej strony) z plików `plan/*.md`. Lista planów jest zadeklarowana w stałej `PLANY` na górze skryptu - żeby dodać/usunąć kierunek, edytuj tę listę.
- `web/` - interaktywna prezentacja: React + Vite, zakładki z trzema planami, oś czasu dzień po dniu. Konsumuje `web/src/data/data.json` - nie edytować danych ręcznie, tylko przez `build_data.py`.
- Skrypt Pythona uruchamiany jest przez `uv run scripts/build_data.py`, zależności zarządzane przez `uv` (`pyproject.toml`, `uv.lock`). Nie używać gołego `python3` ani `pip`.

## Regeneracja danych

Za każdym razem gdy zmienisz cokolwiek w `plan/*.md` (dodasz dzień, poprawisz wycenę, dodasz nowy kierunek), **uruchom ponownie skrypt** zamiast edytować `data.json` ręcznie:

```bash
uv run scripts/build_data.py
```

## Dodawanie nowego kierunku

1. Stwórz `plan/<kierunek>.md` zgodnie ze strukturą opisaną wyżej (nagłówek, intro, tabela dni, sekcja `## Uwagi` z wyceną).
2. Dodaj wpis `{"id": ..., "file": ..., "label": ...}` do stałej `PLANY` w `scripts/build_data.py`.
3. Dodaj kierunek do skrótu porównawczego w `plan/README.md`.
4. Uruchom `uv run scripts/build_data.py`.

## Interaktywna prezentacja (`web/`)

Frontend to React + Vite (bez TypeScript), zależności npm (nie uv - to warstwa JS, oddzielna od skryptu Pythona). Dane wczytywane statycznie z `web/src/data/data.json` (import JSON w `App.jsx`), generowane przez `scripts/build_data.py` - nigdy nie edytuj tego pliku ręcznie.

Struktura komponentów w `web/src/components/`:
- `PlanTimeline.jsx` - oś czasu dzień po dniu dla wybranego planu
- `MarkdownText.jsx` - lekki renderer markdown (bold, linki, listy `- `) używany wszędzie tam, gdzie tekst pochodzi z plików `.md` - nie wyświetlaj surowego tekstu z `data.json` bez przepuszczenia przez ten komponent, bo będą widoczne gwiazdki `**...**`

Zakładki (jedna na plan) są budowane dynamicznie z `data.plany` w `App.jsx` - nie trzeba ich dopisywać ręcznie po dodaniu nowego kierunku.

Uruchomienie lokalne: `cd web && npm install && npm run dev`. Build produkcyjny: `npm run build` (output do `web/dist/`, w `.gitignore`).

`vite.config.js` ma ustawione `base: '/portugalia26/'` (nazwa repo na GitHubie) - wymagane dla poprawnych ścieżek assetów na GitHub Pages. Jeśli repo zostanie kiedyś przemianowane, zaktualizuj to pole.

## Deploy (GitHub Actions → GitHub Pages)

Strona deployuje się **automatycznie** przy każdym pushu do `main` przez `.github/workflows/deploy.yml`: `uv run scripts/build_data.py` (świeże dane) → `npm ci && npm run build` w `web/` → publikacja `web/dist` na GitHub Pages przez oficjalne akcje (`actions/deploy-pages`). Nie ma osobnego skryptu deploy ani brancha `gh-pages` do zarządzania ręcznie - to wszystko obsługuje Actions.

Warunek wstępny (jednorazowo, w ustawieniach repo na GitHubie): Settings → Pages → Source → "GitHub Actions" (nie "Deploy from a branch").

## Wersjonowanie

Repo używa jednocześnie git i jj (kolokowane, `jj git init --colocate`). Zmiany commituj przez `git commit`, jj automatycznie widzi nowy commit jako HEAD.
