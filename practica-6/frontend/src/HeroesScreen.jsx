import { useState, useEffect } from 'react';
import HeroCard from './HeroCard';

export default function HeroesScreen({ casa }) {
  const [heroes, setHeroes] = useState([]);
  const [busqueda, setBusqueda] = useState('');

  useEffect(() => {
    // Le pegamos a nuestra API. Vite usa import.meta.env para las variables de entorno
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    // Si hay una casa definida (Marvel o DC), la pasamos como parámetro
    const url = casa ? `${apiUrl}/api/heroes?casa=${casa}` : `${apiUrl}/api/heroes`;

    fetch(url)
      .then(res => res.json())
      .then(data => setHeroes(data))
      .catch(err => console.error("Error al cargar héroes:", err));
  }, [casa]);

  // Filtro del lado del cliente por nombre de superhéroe
  const heroesFiltrados = heroes.filter(heroe => 
    heroe.nombre.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div>
      <div className="buscador">
        <input 
          type="text" 
          placeholder={`Buscar en ${casa || 'Todos'}...`}
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
      </div>

      <div className="grid-cards">
        {heroesFiltrados.length > 0 ? (
          heroesFiltrados.map(heroe => (
            <HeroCard key={heroe.id} heroe={heroe} />
          ))
        ) : (
          <p>No se encontraron superhéroes.</p>
        )}
      </div>
    </div>
  );
}