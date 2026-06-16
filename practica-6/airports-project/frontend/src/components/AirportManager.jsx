import React, { useState } from 'react';
import { createAirport, updateAirport, deleteAirport } from '../api/services';

const AirportManager = ({ onActionSuccess }) => {
  const [formData, setFormData] = useState({
    iata_faa: '',
    icao: '',
    name: '',
    city: '',
    lat: '',
    lng: '',
    alt: '',
    tz: ''
  });
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);

  const showMessage = (msg, type = 'success') => {
    setMessage({ text: msg, type });
    setTimeout(() => setMessage(null), 3000);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const getPayload = () => {
    const payload = { ...formData };
    if (payload.lat !== '') payload.lat = parseFloat(payload.lat);
    if (payload.lng !== '') payload.lng = parseFloat(payload.lng);
    if (payload.alt !== '') payload.alt = parseFloat(payload.alt);
    else delete payload.alt;
    return payload;
  };

  const handleCreate = async () => {
    setLoading(true);
    try {
      const payload = getPayload();
      await createAirport(payload);
      showMessage('Airport created successfully!');
      if (onActionSuccess) onActionSuccess(payload.lat, payload.lng);
    } catch (error) {
      showMessage('Error creating airport', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async () => {
    setLoading(true);
    try {
      const payload = getPayload();
      await updateAirport(formData.iata_faa, payload);
      showMessage('Airport updated successfully!');
      if (onActionSuccess) onActionSuccess(payload.lat, payload.lng);
    } catch (error) {
      showMessage('Error updating airport', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    setLoading(true);
    try {
      await deleteAirport(formData.iata_faa);
      showMessage('Airport deleted successfully!');
      if (onActionSuccess) onActionSuccess(null, null); // Just refresh, don't focus
    } catch (error) {
      showMessage('Error deleting airport', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sidebar-widget">
      <h3>Airport Manager</h3>
      <div className="form-group row">
        <input name="iata_faa" placeholder="IATA/FAA" value={formData.iata_faa} onChange={handleInputChange} />
        <input name="icao" placeholder="ICAO" value={formData.icao} onChange={handleInputChange} />
      </div>
      <div className="form-group">
        <input name="name" placeholder="Airport Name" value={formData.name} onChange={handleInputChange} />
      </div>
      <div className="form-group">
        <input name="city" placeholder="City" value={formData.city} onChange={handleInputChange} />
      </div>
      <div className="form-group row">
        <input name="lat" placeholder="Latitude" type="number" value={formData.lat} onChange={handleInputChange} />
        <input name="lng" placeholder="Longitude" type="number" value={formData.lng} onChange={handleInputChange} />
      </div>
      <div className="form-group row">
        <input name="alt" placeholder="Alt (ft)" type="number" value={formData.alt} onChange={handleInputChange} />
        <input name="tz" placeholder="Timezone" value={formData.tz} onChange={handleInputChange} />
      </div>
      
      <div className="action-buttons">
        <button onClick={handleCreate} disabled={loading} className="btn-create">Add</button>
        <button onClick={handleUpdate} disabled={loading} className="btn-update">Update</button>
        <button onClick={handleDelete} disabled={loading} className="btn-delete">Delete</button>
      </div>

      {message && (
        <div className={`toast-message ${message.type}`}>
          {message.text}
        </div>
      )}
    </div>
  );
};

export default AirportManager;

