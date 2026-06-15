import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import MarkerClusterGroup from 'react-leaflet-cluster';
import { fetchAllAirports, fetchAirportDetails } from '../api/services';
import AirportPopup from './AirportPopup';
import L from 'leaflet';

// Fix for default marker icon in leaflet with react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const createClusterCustomIcon = function (cluster) {
  return new L.divIcon({
    html: `<span>${cluster.getChildCount()}</span>`,
    className: 'marker-cluster-custom',
    iconSize: L.point(40, 40, true),
  });
};

const MapComponent = () => {
  const [airports, setAirports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAirport, setSelectedAirport] = useState(null);

  useEffect(() => {
    const loadAirports = async () => {
      try {
        const data = await fetchAllAirports();
        // Filter out airports without valid coordinates
        const validAirports = data.filter(a => a.lat != null && a.lng != null);
        setAirports(validAirports);
      } catch (error) {
        console.error("Failed to load airports", error);
      } finally {
        setLoading(false);
      }
    };
    loadAirports();
  }, []);

  const handleMarkerClick = async (iataCode) => {
    // Return early if no code
    if (!iataCode) return;
    
    setSelectedAirport({ loading: true, iataCode });
    try {
      const details = await fetchAirportDetails(iataCode);
      setSelectedAirport({ loading: false, data: details, iataCode });
    } catch (error) {
      console.error("Failed to fetch airport details", error);
      setSelectedAirport({ loading: false, error: true, iataCode });
    }
  };

  if (loading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#4da8da', fontSize: '1.2rem' }}>Loading global airports...</div>;
  }

  // Default center roughly on Europe/Africa
  const position = [20, 0];
  const zoom = 3;

  return (
    <MapContainer center={position} zoom={zoom} style={{ height: '100%', width: '100%' }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        url='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
      />
      <MarkerClusterGroup
        chunkedLoading
        iconCreateFunction={createClusterCustomIcon}
        maxClusterRadius={80}
      >
        {airports.map((airport) => (
          <Marker 
            key={airport.iata_faa || `${airport.lat}-${airport.lng}`} 
            position={[airport.lat, airport.lng]}
            eventHandlers={{
              click: () => handleMarkerClick(airport.iata_faa)
            }}
          >
            <Popup>
              <AirportPopup 
                airportData={selectedAirport} 
                basicData={airport} 
              />
            </Popup>
          </Marker>
        ))}
      </MarkerClusterGroup>
    </MapContainer>
  );
};

export default MapComponent;
