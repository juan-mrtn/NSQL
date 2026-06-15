import { useState, useEffect } from 'react';
import { X } from 'lucide-react';

export default function CRUDModal({ isOpen, onClose, onSubmit, hero = null }) {
  const isEditing = !!hero;
  const [formData, setFormData] = useState({
    name: '',
    real_name: '',
    appearance_year: 2000,
    house: 'Marvel',
    biography: '',
    equipment: '',
    images: ''
  });

  useEffect(() => {
    if (hero) {
      setFormData({
        name: hero.name,
        real_name: hero.real_name || '',
        appearance_year: hero.appearance_year,
        house: hero.house,
        biography: hero.biography,
        equipment: (hero.equipment || []).join(', '),
        images: (hero.images || []).join(', ')
      });
    } else {
      setFormData({
        name: '',
        real_name: '',
        appearance_year: 2000,
        house: 'Marvel',
        biography: '',
        equipment: '',
        images: ''
      });
    }
  }, [hero, isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.submitter?.blur();
    e.preventDefault();
    const dataToSubmit = {
      ...formData,
      appearance_year: parseInt(formData.appearance_year, 10),
      equipment: formData.equipment.split(',').map(s => s.trim()).filter(Boolean),
      images: formData.images.split(',').map(s => s.trim()).filter(Boolean)
    };
    if (dataToSubmit.images.length === 0) {
      alert("At least one image URL is required");
      return;
    }
    onSubmit(dataToSubmit, hero?._id);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="bg-gray-800 rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl border border-gray-700 max-h-[90vh] flex flex-col">
        <div className="p-4 border-b border-gray-700 flex justify-between items-center bg-gray-900/50">
          <h2 className="text-2xl font-bold">{isEditing ? 'Edit Superhero' : 'Add New Superhero'}</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-700 rounded-full transition-colors"><X className="w-5 h-5"/></button>
        </div>
        
        <div className="p-6 overflow-y-auto">
          <form id="hero-form" onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Name *</label>
                <input required type="text" name="name" value={formData.name} onChange={handleChange} className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Real Name</label>
                <input type="text" name="real_name" value={formData.real_name} onChange={handleChange} className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Appearance Year *</label>
                <input required type="number" name="appearance_year" value={formData.appearance_year} onChange={handleChange} className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">House *</label>
                <select name="house" value={formData.house} onChange={handleChange} className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all">
                  <option value="Marvel">Marvel</option>
                  <option value="DC">DC</option>
                </select>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1">Biography *</label>
              <textarea required rows="3" name="biography" value={formData.biography} onChange={handleChange} className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all resize-none"></textarea>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1">Equipment (comma separated)</label>
              <input type="text" name="equipment" value={formData.equipment} onChange={handleChange} placeholder="e.g. Shield, Sword, Grappling Hook" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all" />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1">Image URLs (comma separated) *</label>
              <textarea required rows="2" name="images" value={formData.images} onChange={handleChange} placeholder="https://..., https://..." className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all resize-none"></textarea>
            </div>
          </form>
        </div>
        
        <div className="p-4 border-t border-gray-700 bg-gray-900/50 flex justify-end gap-3">
          <button type="button" onClick={onClose} className="px-5 py-2.5 rounded-lg text-sm font-medium text-gray-300 hover:bg-gray-700 transition-colors">Cancel</button>
          <button type="submit" form="hero-form" className="px-5 py-2.5 rounded-lg text-sm font-medium bg-blue-600 text-white hover:bg-blue-500 transition-colors shadow-lg hover:shadow-blue-500/25">
            {isEditing ? 'Update Superhero' : 'Create Superhero'}
          </button>
        </div>
      </div>
    </div>
  );
}
