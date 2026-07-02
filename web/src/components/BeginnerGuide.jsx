import MarkdownText from './MarkdownText'

export default function BeginnerGuide({ guide }) {
  return (
    <div>
      <h2>Dla początkujących surferów</h2>
      <div className="beginner-section">
        <h3>Rekomendowane spoty</h3>
        <MarkdownText text={guide.rekomendowane} as="div" />
      </div>
      <div className="beginner-section">
        <h3>Zdecydowanie unikać</h3>
        <MarkdownText text={guide.unikac} as="div" />
      </div>
      <div className="beginner-section">
        <h3>Rezerwacja lekcji</h3>
        <MarkdownText text={guide.rezerwacja} as="div" />
      </div>
    </div>
  )
}
