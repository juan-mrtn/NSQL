import { Link, useLocation } from 'react-router-dom';
import { Shield } from 'lucide-react';

export default function Navbar({ onOpenAddModal }) {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-gray-800 border-b border-gray-700 shadow-lg sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center gap-2 text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-marvel to-dc">
              <Shield className="w-8 h-8 text-white" />
              HeroesDB
            </Link>
            <div className="hidden md:block ml-10">
              <div className="flex items-baseline space-x-4">
                <Link to="/" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/') ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white'}`}>All</Link>
                <Link to="/marvel" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/marvel') ? 'bg-marvel text-white' : 'text-gray-300 hover:bg-marvel/20 hover:text-marvel'}`}>Marvel</Link>
                <Link to="/dc" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/dc') ? 'bg-dc text-white' : 'text-gray-300 hover:bg-dc/20 hover:text-dc'}`}>DC Comics</Link>
              </div>
            </div>
          </div>
          <div>
            <button 
              onClick={onOpenAddModal}
              className="bg-white text-gray-900 px-4 py-2 rounded-full font-bold text-sm hover:bg-gray-200 transition-colors shadow-md hover:shadow-lg active:scale-95"
            >
              + Add Hero
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
