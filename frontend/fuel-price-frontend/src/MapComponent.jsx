import { useState } from 'react'
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet'
import L from 'leaflet'
import iconUrl from 'leaflet/dist/images/marker-icon.png'
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png'
import shadowUrl from 'leaflet/dist/images/marker-shadow.png'
import 'leaflet/dist/leaflet.css'

delete L.Icon.Default.prototype._getIconUrl

L.Icon.Default.mergeOptions({
  iconRetinaUrl,
  iconUrl,
  shadowUrl,
})

function ClickHandler({ onClick }){
    useMapEvents({
        click(e){
            onClick(e.latlng)
        }
    })
    return null
}

export default function MapComponent() {
    const [pin, setPin] = useState(null)
  
    return (
    <MapContainer center={[55.1694, 23.8813]} zoom={8} style={{ height: '100%', width: '100%' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
      <ClickHandler onClick={(latlng) => setPin(latlng)}/>
        {pin && <Marker position={pin} />}
    </MapContainer>
  )
}