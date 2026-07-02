import MarkdownText from './MarkdownText'

const CATEGORY_LABELS = {
  surfing: 'Surfing',
  kultura: 'Kultura',
  oba: 'Surfing + kultura',
}

export default function AttractionCard({ atrakcja }) {
  return (
    <div className="card">
      <img
        src={`/${atrakcja.image}`}
        alt={atrakcja.title}
        loading="lazy"
        onError={(e) => {
          e.target.style.display = 'none'
        }}
      />
      <div className="card-body">
        <h3>
          {atrakcja.title}
          <span className={`badge badge-${atrakcja.kategoria}`}>
            {CATEGORY_LABELS[atrakcja.kategoria]}
          </span>
        </h3>
        <MarkdownText text={atrakcja.opis} className="card-text" />

        {atrakcja.atrakcje && (
          <>
            <div className="card-section-title">Atrakcje</div>
            <MarkdownText text={atrakcja.atrakcje} className="card-text" />
          </>
        )}

        {atrakcja.ma_surfing && (
          <>
            <div className="card-section-title">Surfing</div>
            <MarkdownText text={atrakcja.surfing} className="card-text" />
          </>
        )}

        {atrakcja.praktyczne_info && (
          <>
            <div className="card-section-title">Praktyczne info</div>
            <MarkdownText text={atrakcja.praktyczne_info} className="card-text" />
          </>
        )}

        <div className="card-links">
          {atrakcja.locations.map((loc, i) => (
            <a key={i} href={loc.google_maps_url} target="_blank" rel="noreferrer">
              {loc.label ? `Mapa (${loc.label})` : 'Otwórz w Google Maps'}
              {i < atrakcja.locations.length - 1 ? ' · ' : ''}
            </a>
          ))}
        </div>
      </div>
    </div>
  )
}
