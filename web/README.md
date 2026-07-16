# Interaktywna prezentacja - Portugalia 2026

React + Vite. Dane wczytywane z `src/data/data.json`, generowanego skryptem `../scripts/build_data.py` - nie edytuj tego pliku ręcznie.

```bash
npm install
npm run dev
```

## Notatki (Supabase)

Sekcja "Notatki" na stronie to wspólny brudnopis, który zapisuje się trwale w Supabase (darmowy Postgres). Treść przeżywa odświeżenie i deploy, i jest widoczna z każdego urządzenia.

Konfiguracja (jednorazowa):

1. Załóż projekt na [supabase.com](https://supabase.com) (darmowy plan wystarcza).
2. W panelu Supabase: SQL Editor → New query → wklej i uruchom [`supabase.sql`](supabase.sql) (tworzy tabelę `notatki` i polityki dostępu dla klucza anon).
3. Supabase → Project Settings → API → skopiuj **Project URL** i **anon/public key**.
4. Lokalnie: skopiuj `.env.example` do `.env.local` i wpisz oba klucze (`.env.local` jest w `.gitignore`).
5. Deploy: w repo na GitHubie → Settings → Secrets and variables → Actions → dodaj sekrety `VITE_SUPABASE_URL` i `VITE_SUPABASE_ANON_KEY` (workflow wstrzykuje je przy buildzie).

Bez tych kluczy strona działa normalnie, tylko sekcja notatek pokazuje "Notatki niedostępne". Klucz anon jest publiczny (ląduje w zbudowanym JS) - to normalne przy Supabase, dostęp ograniczają polityki RLS z `supabase.sql`.

Zobacz sekcję "Interaktywna prezentacja" w [`../CLAUDE.md`](../CLAUDE.md) po pełny opis (generowanie danych, zdjęcia, struktura komponentów).
