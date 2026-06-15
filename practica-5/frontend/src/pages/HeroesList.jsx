import { useState, useMemo } from 'react';
import SuperheroCard from '../components/SuperheroCard';
import { Search } from 'lucide-react';

export default function HeroesList({ superheroes, houseFilter, onEdit, onDelete }) {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredHeroes = useMemo(() => {
    let filtered = superheroes;
    if (houseFilter) {
      filtered = filtered.filter(h => h.house === houseFilter);
    }
    if (searchTerm) {
      const lowerSearch = searchTerm.toLowerCase();
      filtered = filtered.filter(h => h.name.toLowerCase().includes(lowerSearch));
    }
    return filtered;
  }, [superheroes, houseFilter, searchTerm]);

  return (
    <div>
      <div className="mb-8 relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          placeholder="Search heroes by name..."
          className="block w-full pl-10 pr-3 py-3 border border-gray-700 rounded-xl leading-5 bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-sm"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {filteredHeroes.length === 0 ? (
        <div className="text-center py-20 bg-gray-800 rounded-xl border border-gray-700 shadow-sm">
          <p className="text-gray-400 text-lg">No heroes found matching your search.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredHeroes.map(hero => (
            <SuperheroCard 
              key={hero._id} 
              hero={hero} 
              onEdit={onEdit}
              onDelete={onDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}
