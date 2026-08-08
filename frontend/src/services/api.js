import axios from 'axios';
import { apiConfig } from '../config/api';

const apiClient = axios.create({
  baseURL: apiConfig.baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: apiConfig.timeout,
});

// Request Interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Request Error:', error.response || error.message);
    return Promise.reject(error);
  }
);

export const checkBackendHealth = async () => {
  const response = await apiClient.get(apiConfig.endpoints.rootHealth);
  return response.data;
};

export const checkBackendV1Health = async () => {
  const response = await apiClient.get(apiConfig.endpoints.v1Health);
  return response.data;
};

export default apiClient;
