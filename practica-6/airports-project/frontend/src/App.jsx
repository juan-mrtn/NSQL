import React, { useState } from 'react';
import MapComponent from './components/MapComponent';
import AirportManager from './components/AirportManager';
import NearbySearch from './components/NearbySearch';
import PopularityRanking from './components/PopularityRanking';
import './index.css';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [focusLocation, setFocusLocation] = useState(null);

  const handleAirportAction = (lat, lng) => {
    // Increment trigger to reload airports on the map
    setRefreshTrigger(prev => prev + 1);
    // Focus map on the new/updated airport if coordinates exist
    if (lat && lng) {
      setFocusLocation([lat, lng]);
    }
  };

  return (
    <div className="app-layout">
      <header className="header">
        <h1>Global Airports Explorer</h1>
      </header>
      <div className="main-content">
        <aside className="sidebar">
          <AirportManager onActionSuccess={handleAirportAction} />
          <NearbySearch />
          <PopularityRanking />
        </aside>
        <main className="map-container">
          <MapComponent refreshTrigger={refreshTrigger} focusLocation={focusLocation} />
        </main>
      </div>
    </div>
  );
}

export default App;
