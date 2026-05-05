import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

export default function HeroForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    nombre: '', nombre_real: '', anio_aparicion: '', casa: 'Marvel', 
    biografia: '', equipamiento: '', imagenes: ''
  });

  // Si hay ID, buscamos los datos para rellenar el formulario (Actualizar)[cite: 5]
  useEffect(() => {
    if (id) {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      fetch(`${apiUrl}/api/heroes/${id}`)
        .then(res => res.json())
        .then(data => {
          setFormData({
            ...data,
            // Convertimos arrays a texto separado por comas para el input
            equipamiento: data.equipamiento.join(', '),
            imagenes: data.imagenes.join(', ')
          });
        });
    }
  }, [id]);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const url = id ? `${apiUrl}/api/heroes/${id}` : `${apiUrl}/api/heroes`;
    const method = id ? 'PUT' : 'POST';

    // Armamos el JSON final, convirtiendo los textos con comas de nuevo a Arrays
    const payload = {
      ...formData,
      anio_aparicion: parseInt(formData.anio_aparicion) || new Date().getFullYear(),
      equipamiento: formData.equipamiento.split(',').map(i => i.trim()).filter(i => i),
      imagenes: formData.imagenes.split(',').map(i => i.trim()).filter(i => i)
    };

    try {
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        toast.success(`Superhéroe ${id ? 'actualizado' : 'creado'} con éxito!`); // Cartel de éxito[cite: 5]
        navigate('/'); // Volvemos al inicio
      } else {
        toast.error("Error al guardar en la base de datos."); // Cartel de fracaso[cite: 5]
      }
    } catch (err) {
      toast.error("Error de conexión con la API.");
    }
  };

  return (
    <div className="form-container">
      <h2>{id ? 'Editar Superhéroe' : 'Nuevo Superhéroe'}</h2>
      <form onSubmit={handleSubmit} className="hero-form">
        <input name="nombre" value={formData.nombre} onChange={handleChange} placeholder="Nombre (Ej: Batman)" required />
        <input name="nombre_real" value={formData.nombre_real} onChange={handleChange} placeholder="Nombre Real" />
        <input name="anio_aparicion" type="number" value={formData.anio_aparicion} onChange={handleChange} placeholder="Año de Aparición" required />
        
        <select name="casa" value={formData.casa} onChange={handleChange}>
          <option value="Marvel">Marvel</option>
          <option value="DC">DC</option>
        </select>

        <textarea name="biografia" value={formData.biografia} onChange={handleChange} placeholder="Biografía..." rows="4" required />
        
        <input name="equipamiento" value={formData.equipamiento} onChange={handleChange} placeholder="Equipamiento (Separado por comas)" />
        <input name="imagenes" value={formData.imagenes} onChange={handleChange} placeholder="URLs de imágenes (Separadas por comas)" required />

        <button type="submit" className="btn-guardar">Guardar Superhéroe</button>
      </form>
    </div>
  );
}