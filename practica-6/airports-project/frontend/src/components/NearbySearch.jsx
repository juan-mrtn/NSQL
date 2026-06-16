import React, { useState } from 'react';
import { fetchNearbyAirports } from '../api/services';

const NearbySearch = () => {
  const [lat, setLat] = useState('');
  const [lng, setLng] = useState('');
  const [radius, setRadius] = useState('50');
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!lat || !lng || !radius) return;
    setLoading(true);
    setHasSearched(true);
    try {
      const data = await fetchNearbyAirports(lat, lng, radius);
      setResults(data);
    } catch (error) {
      console.error('Failed to fetch nearby airports', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sidebar-widget">
      <h3>Nearby Airports</h3>
      <div className="form-group row">
        <input type="number" placeholder="Lat" value={lat} onChange={(e) => setLat(e.target.value)} />
        <input type="number" placeholder="Lng" value={lng} onChange={(e) => setLng(e.target.value)} />
      </div>
      <div className="form-group">
        <input type="number" placeholder="Radius (km)" value={radius} onChange={(e) => setRadius(e.target.value)} />
      </div>
      <button onClick={handleSearch} disabled={loading} className="btn-search">Search</button>

      {results.length > 0 && (
        <ul className="results-list">
          {results.map((airport) => (
            <li key={airport.iata_faa || `${airport.lat}-${airport.lng}`}>
              <strong>{airport.name}</strong> ({airport.iata_faa})
              <br/>
              <small>{airport.city}</small>
            </li>
          ))}
        </ul>
      )}
      
      {hasSearched && !loading && results.length === 0 && (
        <div className="no-results">No airports found in this radius.</div>
      )}
    </div>
  );
};

export default NearbySearch;
