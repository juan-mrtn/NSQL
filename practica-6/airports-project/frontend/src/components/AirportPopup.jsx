import React from 'react';

const AirportPopup = ({ airportData, basicData }) => {
  // If the airport has no IATA code, we cannot fetch popularity updates,
  // but we can still display the basic data.
  const hasIata = !!basicData.iata_faa;

  // If it has IATA but data is still loading or doesn't match
  if (hasIata && (!airportData || airportData.loading || airportData.iataCode !== basicData.iata_faa)) {
    return (
      <div style={{ minWidth: '150px', textAlign: 'center', padding: '10px' }}>
        <h3 style={{ margin: '0 0 10px 0', color: '#4da8da' }}>{basicData.name}</h3>
        <p>Loading details...</p>
      </div>
    );
  }

  if (hasIata && airportData && airportData.error) {
    return (
      <div style={{ minWidth: '150px', padding: '10px' }}>
        <h3 style={{ margin: '0 0 10px 0', color: '#e74c3c' }}>{basicData.name}</h3>
        <p>Failed to load data for {basicData.iata_faa}</p>
      </div>
    );
  }

  // Use fetched details if available, otherwise fallback to basicData
  const data = (hasIata && airportData && airportData.data) ? airportData.data : basicData;

  return (
    <div style={{ minWidth: '200px', padding: '5px' }}>
      <h3 style={{ margin: '0 0 10px 0', color: '#4da8da', borderBottom: '1px solid #333', paddingBottom: '5px' }}>
        {data.name}
      </h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '5px 10px', fontSize: '14px' }}>
        <strong style={{ color: '#aaa' }}>IATA:</strong> <span>{data.iata_faa || 'N/A'}</span>
        <strong style={{ color: '#aaa' }}>ICAO:</strong> <span>{data.icao || 'N/A'}</span>
        <strong style={{ color: '#aaa' }}>City:</strong> <span>{data.city || 'N/A'}</span>
        <strong style={{ color: '#aaa' }}>Lat:</strong> <span>{data.lat ? data.lat.toFixed(4) : 'N/A'}</span>
        <strong style={{ color: '#aaa' }}>Lng:</strong> <span>{data.lng ? data.lng.toFixed(4) : 'N/A'}</span>
        <strong style={{ color: '#aaa' }}>Altitude:</strong> <span>{data.alt ? `${data.alt} ft` : 'N/A'}</span>
        <strong style={{ color: '#aaa' }}>Timezone:</strong> <span>{data.tz || 'N/A'}</span>
      </div>
      <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #333', fontSize: '12px', color: '#888', textAlign: 'center' }}>
        {hasIata ? (
          <p style={{ margin: 0 }}>Viewing this updates popularity!</p>
        ) : (
          <p style={{ margin: 0, color: '#e74c3c' }}>No IATA code to track popularity.</p>
        )}
      </div>
    </div>
  );
};

export default AirportPopup;
