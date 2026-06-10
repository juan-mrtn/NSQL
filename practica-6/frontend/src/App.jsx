import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import HeroesScreen from './HeroesScreen';
import HeroDetail from './HeroDetail';
import HeroForm from './HeroForm';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      {/* Componente global que maneja las alertas flotantes */}
      <Toaster position="bottom-right" /> 
      
      <nav className="navbar">
        <h2>🦸‍♂️ Superhéroes SPA</h2>
        <div className="links">
          <Link to="/">Todos</Link>
          <Link to="/marvel">Marvel</Link>
          <Link to="/dc">DC</Link>
          <Link to="/nuevo" className="btn-nuevo">+ Cargar Héroe</Link>
        </div>
      </nav>
      
      <main className="container">
        <Routes>
          <Route path="/" element={<HeroesScreen casa="" />} />
          <Route path="/marvel" element={<HeroesScreen casa="Marvel" />} />
          <Route path="/dc" element={<HeroesScreen casa="DC" />} />
          <Route path="/heroe/:id" element={<HeroDetail />} />
          
          {/* Rutas para Cargar y Actualizar */}
          <Route path="/nuevo" element={<HeroForm />} />
          <Route path="/editar/:id" element={<HeroForm />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;