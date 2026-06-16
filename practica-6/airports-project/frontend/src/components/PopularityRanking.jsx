import React, { useEffect, useState } from 'react';
import { fetchPopularAirports } from '../api/services';

const PopularityRanking = () => {
  const [popularAirports, setPopularAirports] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadPopularity = async () => {
    setLoading(true);
    try {
      const data = await fetchPopularAirports();
      if (Array.isArray(data)) {
        setPopularAirports(data);
      } else if (typeof data === 'object') {
        const arr = Object.entries(data).map(([code, count]) => ({ code, count })).sort((a,b) => b.count - a.count);
        setPopularAirports(arr);
      }
    } catch (error) {
      console.error('Failed to load popularity', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPopularity();
  }, []);

  return (
    <div className="sidebar-widget">
      <h3>Popular Airports</h3>
      <button onClick={loadPopularity} disabled={loading} className="btn-refresh">Refresh Rankings</button>
      {popularAirports.length > 0 ? (
        <ul className="results-list ranked-list">
          {popularAirports.map((item, index) => {
            // Flexible property names to handle different potential backend formats
            const code = item.iata_code || item.code || item[0] || (typeof item === 'string' ? item : JSON.stringify(item));
            const count = item.count || item.score || item[1] || item.visits || '';
            return (
              <li key={code}>
                <span className="rank">#{index + 1}</span> <strong>{code}</strong> {count && `(${count} clicks)`}
              </li>
            );
          })}
        </ul>
      ) : (
        <div className="no-results">No popular airports found yet.</div>
      )}
    </div>
  );
};

export default PopularityRanking;
