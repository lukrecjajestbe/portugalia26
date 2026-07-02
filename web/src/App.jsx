import { useState } from 'react'
import data from './data/data.json'
import MapView from './components/MapView'
import AttractionCard from './components/AttractionCard'
import PlanTimeline from './components/PlanTimeline'
import BeginnerGuide from './components/BeginnerGuide'

const TABS = [
  { id: 'atrakcje', label: 'Atrakcje i mapa' },
  { id: 'wariant_a', label: 'Plan: 18-31.07' },
  { id: 'wariant_b', label: 'Plan: 21-31.07' },
  { id: 'poczatkujacy', label: 'Dla początkujących' },
]

const CATEGORY_FILTERS = [
  { id: 'wszystkie', label: 'Wszystkie' },
  { id: 'surfing', label: 'Surfing' },
  { id: 'kultura', label: 'Kultura' },
  { id: 'oba', label: 'Surfing + kultura' },
]

function App() {
  const [tab, setTab] = useState('atrakcje')
  const [kategoria, setKategoria] = useState('wszystkie')

  const atrakcje =
    kategoria === 'wszystkie'
      ? data.atrakcje
      : data.atrakcje.filter((a) => a.kategoria === kategoria)

  return (
    <>
      <header className="app-header">
        <h1>Portugalia 2026 - road trip surfingowy</h1>
        <p>Faro → Algarve → Alentejo → Ericeira/Peniche → Lizbona → Nazaré → Aveiro → Porto</p>
      </header>

      <nav className="tabs">
        {TABS.map((t) => (
          <button
            key={t.id}
            className={`tab-button ${tab === t.id ? 'active' : ''}`}
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </nav>

      <main>
        {tab === 'atrakcje' && (
          <>
            <MapView atrakcje={atrakcje} />

            <div className="filters">
              {CATEGORY_FILTERS.map((f) => (
                <button
                  key={f.id}
                  className={`filter-button ${kategoria === f.id ? 'active' : ''}`}
                  onClick={() => setKategoria(f.id)}
                >
                  {f.label}
                </button>
              ))}
            </div>

            <div className="card-grid">
              {atrakcje.map((a) => (
                <AttractionCard atrakcja={a} key={a.id} />
              ))}
            </div>
          </>
        )}

        {tab === 'wariant_a' && <PlanTimeline plan={data.plany.wariant_a} />}
        {tab === 'wariant_b' && <PlanTimeline plan={data.plany.wariant_b} />}
        {tab === 'poczatkujacy' && <BeginnerGuide guide={data.dla_poczatkujacych} />}
      </main>
    </>
  )
}

export default App
