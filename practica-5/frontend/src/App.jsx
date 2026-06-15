import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Navbar from './components/Navbar';
import HeroesList from './pages/HeroesList';
import DetailView from './pages/DetailView';
import CRUDModal from './components/CRUDModal';

import { getSuperheroes, createSuperhero, updateSuperhero, deleteSuperhero } from './api/superheroes';

function App() {
  const [superheroes, setSuperheroes] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingHero, setEditingHero] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchHeroes = async () => {
    try {
      const data = await getSuperheroes();
      setSuperheroes(data);
    } catch (error) {
      toast.error("Failed to fetch superheroes");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHeroes();
  }, []);

  const handleOpenAddModal = () => {
    setEditingHero(null);
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (hero) => {
    setEditingHero(hero);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingHero(null);
  };

  const handleSubmitHero = async (heroData, id) => {
    try {
      if (id) {
        await updateSuperhero(id, heroData);
        toast.success("Superhero updated successfully!");
      } else {
        await createSuperhero(heroData);
        toast.success("Superhero created successfully!");
      }
      handleCloseModal();
      fetchHeroes();
    } catch (error) {
      toast.error(error.response?.data?.detail || "An error occurred");
    }
  };

  const handleDeleteHero = async (id) => {
    if (window.confirm("Are you sure you want to delete this superhero?")) {
      try {
        await deleteSuperhero(id);
        toast.success("Superhero deleted successfully!");
        fetchHeroes();
      } catch (error) {
        toast.error("Failed to delete superhero");
      }
    }
  };

  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-900 font-sans">
        <Navbar onOpenAddModal={handleOpenAddModal} />
        
        <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            </div>
          ) : (
            <Routes>
              <Route path="/" element={<HeroesList superheroes={superheroes} onEdit={handleOpenEditModal} onDelete={handleDeleteHero} />} />
              <Route path="/marvel" element={<HeroesList superheroes={superheroes} houseFilter="Marvel" onEdit={handleOpenEditModal} onDelete={handleDeleteHero} />} />
              <Route path="/dc" element={<HeroesList superheroes={superheroes} houseFilter="DC" onEdit={handleOpenEditModal} onDelete={handleDeleteHero} />} />
              <Route path="/hero/:id" element={<DetailView />} />
            </Routes>
          )}
        </main>

        <CRUDModal 
          isOpen={isModalOpen} 
          onClose={handleCloseModal} 
          onSubmit={handleSubmitHero} 
          hero={editingHero} 
        />
        
        <ToastContainer position="bottom-right" theme="dark" />
      </div>
    </Router>
  );
}

export default App;
