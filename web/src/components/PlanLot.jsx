import MarkdownText from './MarkdownText'

export default function PlanLot({ lot }) {
  if (!lot?.intro && !lot?.punkty?.length) return null

  return (
    <section className="lot">
      <h2>✈️ Lot</h2>
      {lot.intro && <MarkdownText text={lot.intro} className="lot-intro" />}
      {lot.punkty?.length > 0 && (
        <ul className="lot-punkty">
          {lot.punkty.map((punkt, i) => (
            <li key={i}>
              <MarkdownText text={punkt} as="span" />
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
