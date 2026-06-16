import axios from 'axios';

// The nginx reverse proxy routes /api/ to the backend port 8000
const API_BASE_URL = '/api';

export const fetchAllAirports = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/airports?limit=10000`);
    return response.data;
  } catch (error) {
    console.error('Error fetching airports:', error);
    throw error;
  }
};

export const fetchAirportDetails = async (iataCode) => {
  try {
    // Calling this specific endpoint triggers the popularity counter on the backend
    const response = await axios.get(`${API_BASE_URL}/airports/${iataCode}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching details for airport ${iataCode}:`, error);
    throw error;
  }
};

export const createAirport = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/airports`, data);
    return response.data;
  } catch (error) {
    console.error('Error creating airport:', error);
    throw error;
  }
};

export const updateAirport = async (iataCode, data) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/airports/${iataCode}`, data);
    return response.data;
  } catch (error) {
    console.error(`Error updating airport ${iataCode}:`, error);
    throw error;
  }
};

export const deleteAirport = async (iataCode) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/airports/${iataCode}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting airport ${iataCode}:`, error);
    throw error;
  }
};

export const fetchNearbyAirports = async (lat, lng, radius) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/airports/nearby`, {
      params: { lat, lng, radius }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching nearby airports:', error);
    throw error;
  }
};

export const fetchPopularAirports = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/airports/popular`);
    return response.data;
  } catch (error) {
    console.error('Error fetching popular airports:', error);
    throw error;
  }
};
