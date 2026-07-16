-- Tabela na trwale notatki wyjazdu. Uruchom w Supabase: SQL Editor -> New query -> Run.

create table if not exists public.notatki (
  plan_id text primary key,
  tresc text not null default '',
  updated_at timestamptz not null default now()
);

alter table public.notatki enable row level security;

-- Strona jest publiczna i uzywa klucza anon, wiec dajemy anon pelny dostep
-- do tej jednej tabeli. Notatki nie sa tajne (kazdy z linkiem do strony je widzi).

create policy "anon czyta notatki"
  on public.notatki for select
  to anon
  using (true);

create policy "anon zapisuje notatki"
  on public.notatki for insert
  to anon
  with check (true);

create policy "anon aktualizuje notatki"
  on public.notatki for update
  to anon
  using (true)
  with check (true);
