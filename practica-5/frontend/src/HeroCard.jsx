import { Link } from 'react-router-dom';

export default function HeroCard({ heroe }) {

  const bioTruncada = heroe.biografia.length > 100 
    ? heroe.biografia.substring(0, 100) + '...' 
    : heroe.biografia;

  return (
    <div className="card">
      <img 
        src={heroe.imagenes[0] || 'https://via.placeholder.com/150'} 
        alt={heroe.nombre} 
      />
      <div className="card-body">
        <h3>{heroe.nombre}</h3>
        {heroe.nombre_real && <h4>({heroe.nombre_real})</h4>}
        <span className={`badge ${heroe.casa.toLowerCase()}`}>{heroe.casa}</span>
        <p>{bioTruncada}</p>
        <Link to={`/heroes/${heroe.id}`} className="btn-detalle">Ver Detalle</Link>
      </div>
    </div>
  );
}