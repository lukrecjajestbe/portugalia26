export default function PlanNoclegi({ noclegi }) {
  if (!noclegi?.grupy?.length) return null

  return (
    <section className="noclegi">
      <h2>Noclegi na trasie</h2>
      {noclegi.intro && <p className="noclegi-intro">{noclegi.intro}</p>}

      <div className="noclegi-grupy">
        {noclegi.grupy.map((grupa) => (
          <div className="noclegi-grupa" key={grupa.miejsce}>
            <div className="noclegi-grupa-head">
              <span className="noclegi-transport">{grupa.transport}</span>
              <h3>{grupa.miejsce}</h3>
              <span className="noclegi-nocleg">{grupa.nocleg}</span>
            </div>
            <div className="noclegi-hotele">
              {grupa.hotele.map((hotel) => (
                <article className="hotel-card" key={hotel.nazwa}>
                  <div className="hotel-card-top">
                    <h4>{hotel.nazwa}</h4>
                    <span className="hotel-ocena">{hotel.ocena}</span>
                  </div>
                  <p className="hotel-cecha">{hotel.cecha}</p>
                  <div className="hotel-card-bottom">
                    <span className="hotel-cena">{hotel.cena}</span>
                    <a
                      className="hotel-link"
                      href={hotel.link}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Booking ↗
                    </a>
                  </div>
                </article>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
