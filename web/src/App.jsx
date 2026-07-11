import { useState } from 'react'
import data from './data/data.json'
import PlanTimeline from './components/PlanTimeline'

function App() {
  const [tab, setTab] = useState(data.plany[0]?.id)

  const aktywnyPlan = data.plany.find((p) => p.id === tab) ?? data.plany[0]

  return (
    <>
      <header className="app-header">
        <h1>Wakacje 2026 - 3 plany do wyboru</h1>
        <p>24.07 - 7.08 (14 dni), 2 osoby: Sycylia · Maroko · Madagaskar</p>
      </header>

      <nav className="tabs">
        {data.plany.map((p) => (
          <button
            key={p.id}
            className={`tab-button ${tab === p.id ? 'active' : ''}`}
            onClick={() => setTab(p.id)}
          >
            {p.label}
          </button>
        ))}
      </nav>

      <main>{aktywnyPlan && <PlanTimeline plan={aktywnyPlan} />}</main>
    </>
  )
}

export default App
