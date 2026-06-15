import { Link } from 'react-router-dom';
import { Pencil, Trash2 } from 'lucide-react';

export default function SuperheroCard({ hero, onEdit, onDelete }) {
  const isMarvel = hero.house === 'Marvel';
  
  return (
    <div className="group bg-gray-800 rounded-xl overflow-hidden shadow-lg border border-gray-700 hover:border-gray-500 hover:-translate-y-1 hover:shadow-2xl transition-all duration-300 flex flex-col h-full relative">
      <div className="absolute top-2 right-2 flex gap-2 z-10 opacity-0 group-hover:opacity-100 transition-opacity">
        <button onClick={() => onEdit(hero)} className="bg-blue-600 p-2 rounded-full hover:bg-blue-500 shadow-md">
          <Pencil className="w-4 h-4 text-white" />
        </button>
        <button onClick={() => onDelete(hero._id)} className="bg-red-600 p-2 rounded-full hover:bg-red-500 shadow-md">
          <Trash2 className="w-4 h-4 text-white" />
        </button>
      </div>

      <Link to={`/hero/${hero._id}`} className="flex flex-col h-full cursor-pointer">
        <div className="relative h-64 overflow-hidden">
          <img 
            src={hero.images[0]} 
            alt={hero.name} 
            className="w-full h-full object-cover object-top group-hover:scale-105 transition-transform duration-500"
            onError={(e) => { e.target.src = 'https://via.placeholder.com/400x600?text=No+Image'; }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent opacity-80" />
          <div className="absolute bottom-3 left-4">
            <span className={`text-xs font-bold px-2 py-1 rounded uppercase tracking-wider ${isMarvel ? 'bg-marvel text-white' : 'bg-dc text-white'}`}>
              {hero.house}
            </span>
          </div>
        </div>
        <div className="p-5 flex-grow flex flex-col">
          <h3 className="text-2xl font-black text-white uppercase tracking-tight">{hero.name}</h3>
          {hero.real_name && <p className="text-gray-400 text-sm font-medium mb-3">{hero.real_name}</p>}
          <p className="text-gray-300 text-sm line-clamp-3 mt-auto">
            {hero.biography}
          </p>
        </div>
      </Link>
    </div>
  );
}
