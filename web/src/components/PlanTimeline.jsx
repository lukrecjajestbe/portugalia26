import MarkdownText from './MarkdownText'
import PlanLot from './PlanLot'
import PlanTransport from './PlanTransport'
import PlanNoclegi from './PlanNoclegi'
import PlanNotatki from './PlanNotatki'

function imageForDay(dzien) {
  return dzien.image ? `${import.meta.env.BASE_URL}${dzien.image}` : null
}

export default function PlanTimeline({ plan }) {
  return (
    <div>
      <MarkdownText text={plan.intro} className="plan-intro" />

      <PlanLot lot={plan.lot} />

      <PlanTransport transport={plan.transport} />

      <div className="timeline">
        {plan.dni.map((dzien) => {
          const image = imageForDay(dzien)
          return (
            <div className="timeline-day" key={dzien.dzien}>
              {image ? (
                <img
                  className="timeline-day-thumb"
                  src={image}
                  alt={dzien.miejsce}
                  loading="lazy"
                />
              ) : (
                <div className="timeline-day-thumb" />
              )}
              <div className="timeline-day-num">{dzien.dzien}</div>
              <div className="timeline-day-meta">{dzien.data}</div>
              <div className="timeline-day-body">
                <div className="timeline-day-place">{dzien.miejsce}</div>
                <MarkdownText text={dzien.plan} className="timeline-day-plan" />
              </div>
            </div>
          )
        })}
      </div>

      <PlanNoclegi noclegi={plan.noclegi} />

      {plan.koszty?.rows?.length > 0 && (
        <section className="koszty">
          <h2>Szacunkowy koszt dla 2 osób / 14 dni</h2>
          <table className="koszty-table">
            <thead>
              <tr>
                {plan.koszty.header.map((h, i) => (
                  <th key={i}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {plan.koszty.rows.map((row, i) => {
                const razem = row[0].includes('**')
                return (
                  <tr key={i} className={razem ? 'koszty-razem' : ''}>
                    {row.map((cell, j) => (
                      <td key={j}>
                        <MarkdownText text={cell} as="span" />
                      </td>
                    ))}
                  </tr>
                )
              })}
            </tbody>
          </table>
        </section>
      )}

      {plan.uwagi?.length > 0 && (
        <section className="plan-uwagi">
          {plan.uwagi.map((linia, i) => (
            <MarkdownText key={i} text={linia} />
          ))}
        </section>
      )}

      <PlanNotatki planId={plan.id} />
    </div>
  )
}
