import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

const CATEGORY_COLORS = {
  surfing: '#0a8f6b',
  kultura: '#b5533a',
  oba: '#7a5cc7',
}

export default function MapView({ atrakcje }) {
  const center = [39.4, -8.8]

  return (
    <div className="map-wrapper">
      <MapContainer center={center} zoom={7} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {atrakcje.flatMap((atrakcja) =>
          atrakcja.locations.map((loc, i) => (
            <CircleMarker
              key={`${atrakcja.id}-${i}`}
              center={[loc.lat, loc.lng]}
              radius={8}
              pathOptions={{
                color: CATEGORY_COLORS[atrakcja.kategoria],
                fillColor: CATEGORY_COLORS[atrakcja.kategoria],
                fillOpacity: 0.85,
                weight: 2,
              }}
            >
              <Popup>
                <div className="popup-title">
                  {atrakcja.title}
                  {loc.label ? ` (${loc.label})` : ''}
                </div>
                <p style={{ margin: '4px 0' }}>{atrakcja.opis}</p>
                <a href={loc.google_maps_url} target="_blank" rel="noreferrer">
                  Otwórz w Google Maps
                </a>
              </Popup>
            </CircleMarker>
          )),
        )}
      </MapContainer>
    </div>
  )
}
