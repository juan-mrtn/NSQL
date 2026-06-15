import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getSuperhero } from '../api/superheroes';
import { ChevronLeft, ChevronRight, ArrowLeft } from 'lucide-react';

export default function DetailView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [hero, setHero] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  useEffect(() => {
    const fetchHero = async () => {
      try {
        const data = await getSuperhero(id);
        setHero(data);
      } catch (err) {
        console.error("Failed to fetch hero", err);
      } finally {
        setLoading(false);
      }
    };
    fetchHero();
  }, [id]);

  if (loading) return <div className="text-center py-20 text-xl font-semibold text-gray-400 animate-pulse">Loading hero data...</div>;
  if (!hero) return <div className="text-center py-20 text-xl font-semibold text-gray-400">Hero not found</div>;

  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % hero.images.length);
  };

  const prevImage = () => {
    setCurrentImageIndex((prev) => (prev - 1 + hero.images.length) % hero.images.length);
  };

  const isMarvel = hero.house === 'Marvel';

  return (
    <div className="max-w-6xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
      <button onClick={() => navigate(-1)} className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors group">
        <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
        Back
      </button>

      <div className="bg-gray-800 rounded-3xl overflow-hidden shadow-2xl border border-gray-700 flex flex-col md:flex-row">
        {/* Carousel Section */}
        <div className="md:w-1/2 relative bg-gray-900 min-h-[400px]">
          <img 
            src={hero.images[currentImageIndex]} 
            alt={hero.name} 
            className="absolute inset-0 w-full h-full object-cover"
            onError={(e) => { e.target.src = 'https://via.placeholder.com/600x800?text=No+Image'; }}
          />
          {hero.images.length > 1 && (
            <>
              <button onClick={prevImage} className="absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/80 text-white p-2 rounded-full backdrop-blur-sm transition-colors">
                <ChevronLeft className="w-6 h-6" />
              </button>
              <button onClick={nextImage} className="absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/80 text-white p-2 rounded-full backdrop-blur-sm transition-colors">
                <ChevronRight className="w-6 h-6" />
              </button>
              <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
                {hero.images.map((_, idx) => (
                  <div key={idx} className={`w-2.5 h-2.5 rounded-full transition-all ${idx === currentImageIndex ? 'bg-white scale-125' : 'bg-white/50'}`} />
                ))}
              </div>
            </>
          )}
        </div>

        {/* Details Section */}
        <div className="md:w-1/2 p-8 md:p-12 flex flex-col relative">
          <div className="absolute top-8 right-8">
             {/* Simple visual indicator for logo instead of an actual image since finding reliable URLs can be tricky, but we can do a stylized text logo */}
             <div className={`font-black text-3xl italic tracking-tighter px-4 py-2 rounded-lg border-2 shadow-lg ${isMarvel ? 'bg-marvel text-white border-red-700' : 'bg-white text-dc border-blue-500'}`}>
                {hero.house.toUpperCase()}
             </div>
          </div>
          
          <div className="mt-12 md:mt-0">
            <h1 className="text-5xl font-black text-white uppercase tracking-tight mb-2">{hero.name}</h1>
            {hero.real_name && <h2 className="text-xl text-gray-400 font-medium mb-6">aka {hero.real_name}</h2>}
            
            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-300 border-b border-gray-700 pb-2 mb-3">Biography</h3>
              <p className="text-gray-300 leading-relaxed">{hero.biography}</p>
            </div>

            <div className="grid grid-cols-2 gap-6 mb-8">
              <div>
                <h3 className="text-lg font-semibold text-gray-300 border-b border-gray-700 pb-2 mb-3">Appearance Year</h3>
                <span className="text-2xl font-bold text-white bg-gray-900 px-4 py-2 rounded-lg inline-block border border-gray-700 shadow-inner">
                  {hero.appearance_year}
                </span>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-300 border-b border-gray-700 pb-2 mb-3">Equipment</h3>
                {hero.equipment && hero.equipment.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {hero.equipment.map((item, idx) => (
                      <span key={idx} className="bg-blue-900/50 text-blue-200 border border-blue-800 text-sm px-3 py-1 rounded-full font-medium shadow-sm">
                        {item}
                      </span>
                    ))}
                  </div>
                ) : (
                  <span className="text-gray-500 italic">None</span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
