import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: `${API_URL}/superheroes`,
});

export const getSuperheroes = async () => {
  const response = await api.get('/');
  return response.data;
};

export const getSuperhero = async (id) => {
  const response = await api.get(`/${id}`);
  return response.data;
};

export const createSuperhero = async (data) => {
  const response = await api.post('/', data);
  return response.data;
};

export const updateSuperhero = async (id, data) => {
  const response = await api.put(`/${id}`, data);
  return response.data;
};

export const deleteSuperhero = async (id) => {
  const response = await api.delete(`/${id}`);
  return response.data;
};
