import axios from 'axios';

// The nginx reverse proxy routes /api/ to the backend port 8000
const API_BASE_URL = '/api';

export const fetchAllAirports = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/airports`);
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
