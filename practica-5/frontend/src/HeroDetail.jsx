import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

export default function HeroDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [heroe, setHeroe] = useState(null);
  const [imgIndex, setImgIndex] = useState(0);

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    fetch(`${apiUrl}/api/heroes/${id}`)
      .then(res => res.json())
      .then(data => setHeroe(data))
      .catch(err => console.error("Error:", err));
  }, [id]);

  if (!heroe) return <p>Cargando detalle...</p>;

  const nextImg = () => setImgIndex((imgIndex + 1) % heroe.imagenes.length);
  const eliminarHeroe = async () => {
    if(!window.confirm(`¿Seguro que querés eliminar a ${heroe.nombre}?`)) return;
    
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    try {
      const res = await fetch(`${apiUrl}/api/heroes/${id}`, { method: 'DELETE' });
      if (res.ok) {
        toast.success("Superhéroe eliminado correctamente"); // Cartel de éxito[cite: 5]
        navigate('/'); // Volver al inicio
      } else {
        toast.error("Hubo un problema al eliminar"); // Cartel de fracaso[cite: 5]
      }
    } catch(err) {
      toast.error("Error de conexión");
    }
  };
  return (
    <div className="detalle-container">
      <button onClick={() => navigate(-1)} className="btn-volver">⬅ Volver</button>
      <div className="acciones-detalle">
        <button onClick={() => navigate(-1)} className="btn-volver">⬅ Volver</button>
        <Link to={`/editar/${heroe.id}`} className="btn-editar">✏️ Editar</Link>
        <button onClick={eliminarHeroe} className="btn-eliminar">🗑️ Eliminar</button>
      </div>
      <div className="detalle-content">
        <div className="carrusel">
          <img src={heroe.imagenes[imgIndex]} alt={heroe.nombre} className="img-principal" />
          {heroe.imagenes.length > 1 && (
            <button onClick={nextImg} className="btn-next">Siguiente Imagen 📸</button>
          )}
        </div>

        <div className="info-texto">
          <div className="header-detalle">
            <h1>{heroe.nombre}</h1>
            {/* Punto 8: Mostrar el logo de la casa */}
            <img 
              src={heroe.casa.toLowerCase() === 'marvel' 
                ? 'https://upload.wikimedia.org/wikipedia/commons/b/b9/Marvel_Logo.svg' 
                : 'https://upload.wikimedia.org/wikipedia/commons/3/3d/DC_Comics_logo.svg'} 
              alt="Logo Casa" 
              className="logo-casa"
            />
          </div>

          <p><strong>Nombre Real:</strong> {heroe.nombre_real || 'Desconocido'}</p>
          <p><strong>Aparición:</strong> {heroe.anio_aparicion}</p>
          <p><strong>Biografía:</strong> {heroe.biografia}</p>
          
          {heroe.equipamiento.length > 0 && (
            <div>
              <strong>Equipamiento:</strong>
              <ul>
                {heroe.equipamiento.map((item, i) => <li key={i}>{item}</li>)}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}