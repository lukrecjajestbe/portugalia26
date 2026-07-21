import MarkdownText from './MarkdownText'

export default function PlanTransport({ transport }) {
  if (!transport?.intro && !transport?.punkty?.length) return null

  return (
    <section className="transport">
      <h2>🧭 Jak się przemieszczamy</h2>
      {transport.intro && (
        <MarkdownText text={transport.intro} className="transport-intro" />
      )}
      {transport.punkty?.length > 0 && (
        <ul className="transport-punkty">
          {transport.punkty.map((punkt, i) => (
            <li key={i}>
              <MarkdownText text={punkt} as="span" />
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
