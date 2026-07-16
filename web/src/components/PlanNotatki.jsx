import { useEffect, useRef, useState } from 'react'
import { supabase, supabaseSkonfigurowane } from '../lib/supabase'

const DEBOUNCE_MS = 800

export default function PlanNotatki({ planId }) {
  const [tresc, setTresc] = useState('')
  const [status, setStatus] = useState('ladowanie')
  const timerRef = useRef(null)
  const zaladowaneRef = useRef(false)

  useEffect(() => {
    if (!supabaseSkonfigurowane) {
      setStatus('brak-konfiguracji')
      return
    }
    let anulowane = false
    zaladowaneRef.current = false
    setStatus('ladowanie')

    async function wczytaj() {
      const { data, error } = await supabase
        .from('notatki')
        .select('tresc')
        .eq('plan_id', planId)
        .maybeSingle()

      if (anulowane) return
      if (error) {
        setStatus('blad')
        return
      }
      setTresc(data?.tresc ?? '')
      zaladowaneRef.current = true
      setStatus('gotowe')
    }

    wczytaj()
    return () => {
      anulowane = true
    }
  }, [planId])

  async function zapisz(nowaTresc) {
    setStatus('zapisywanie')
    const { error } = await supabase
      .from('notatki')
      .upsert({ plan_id: planId, tresc: nowaTresc }, { onConflict: 'plan_id' })
    setStatus(error ? 'blad' : 'zapisano')
  }

  function onZmiana(event) {
    const nowaTresc = event.target.value
    setTresc(nowaTresc)
    if (!supabaseSkonfigurowane || !zaladowaneRef.current) return
    if (timerRef.current) clearTimeout(timerRef.current)
    timerRef.current = setTimeout(() => zapisz(nowaTresc), DEBOUNCE_MS)
  }

  const komunikat = {
    ladowanie: 'Wczytywanie...',
    zapisywanie: 'Zapisywanie...',
    zapisano: 'Zapisano ✓',
    gotowe: '',
    blad: 'Blad zapisu - sprobuj ponownie',
    'brak-konfiguracji': 'Notatki niedostepne (brak konfiguracji Supabase)',
  }[status]

  return (
    <section className="notatki">
      <div className="notatki-head">
        <h2>Notatki</h2>
        {komunikat && <span className="notatki-status">{komunikat}</span>}
      </div>
      <p className="notatki-intro">
        Wspolny brudnopis na caly wyjazd - co spakowac, co zarezerwowac, pomysly.
        Zapisuje sie automatycznie i jest widoczny z kazdego urzadzenia.
      </p>
      <textarea
        className="notatki-pole"
        value={tresc}
        onChange={onZmiana}
        placeholder="Wpisz notatki..."
        rows={10}
        disabled={status === 'ladowanie' || status === 'brak-konfiguracji'}
      />
    </section>
  )
}
