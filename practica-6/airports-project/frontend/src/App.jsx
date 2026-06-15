import React from 'react';
import MapComponent from './components/MapComponent';
import './index.css';

function App() {
  return (
    <>
      <header className="header">
        <h1>Global Airports Explorer</h1>
      </header>
      <main className="map-container">
        <MapComponent />
      </main>
    </>
  );
}

export default App;
