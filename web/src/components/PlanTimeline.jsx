import MarkdownText from './MarkdownText'

export default function PlanTimeline({ plan }) {
  return (
    <div>
      <p className="plan-intro">{plan.intro}</p>
      <div className="timeline">
        {plan.dni.map((dzien) => (
          <div className="timeline-day" key={dzien.dzien}>
            <div className="timeline-day-num">{dzien.dzien}</div>
            <div className="timeline-day-meta">{dzien.data}</div>
            <div>
              <div className="timeline-day-place">{dzien.miejsce}</div>
              <MarkdownText text={dzien.plan} className="timeline-day-plan" />
            </div>
          </div>
        ))}
      </div>
      {plan.uwagi && <MarkdownText text={plan.uwagi} className="plan-uwagi" />}
    </div>
  )
}
