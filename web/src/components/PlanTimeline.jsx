import MarkdownText from './MarkdownText'

const PLACE_IMAGES = {
  faro: '01-faro',
  lagos: '02-lagos',
  sagres: '03-sagres-cabo-sao-vicente',
  'zambujeira do mar': '06-zambujeira-do-mar',
  'vila nova de milfontes': '07-vila-nova-de-milfontes',
  ericeira: '08-ericeira',
  'peniche/baleal': '09-peniche-baleal',
  óbidos: '10-obidos',
  sintra: '11-sintra',
  lizbona: '13-lizbona',
  'lizbona / sintra': '13-lizbona',
  porto: '19-porto',
}

function imageForPlace(miejsce) {
  const firstStop = miejsce.split('→')[0].trim().toLowerCase()
  const folderId = PLACE_IMAGES[firstStop]
  return folderId ? `${import.meta.env.BASE_URL}images/${folderId}.jpg` : null
}

export default function PlanTimeline({ plan }) {
  return (
    <div>
      <p className="plan-intro">{plan.intro}</p>
      <div className="timeline">
        {plan.dni.map((dzien) => {
          const image = imageForPlace(dzien.miejsce)
          return (
            <div className="timeline-day" key={dzien.dzien}>
              {image ? (
                <img className="timeline-day-thumb" src={image} alt={dzien.miejsce} loading="lazy" />
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
      {plan.uwagi && <MarkdownText text={plan.uwagi} className="plan-uwagi" />}
    </div>
  )
}
