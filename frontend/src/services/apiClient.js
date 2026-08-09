import axios from 'axios';
import { API_BASE_URL } from '../config/env';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor
apiClient.interceptors.request.use(
  (config) => {
    if (import.meta.env.DEV) {
      console.log(`[apiClient Request] ${config.method?.toUpperCase()} -> ${config.url}`);
    }
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor with retry mechanism for transient failures
apiClient.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log(`[apiClient Response] ${response.status} <- ${response.config.url}`);
    }
    return response;
  },
  async (error) => {
    const config = error.config;
    if (!config || config._retryCount >= 2) {
      const formattedMessage = error.response?.data?.detail || error.message || 'API request failed';
      console.error('[apiClient Error]:', formattedMessage);
      return Promise.reject(error);
    }

    if (!error.response || (error.response.status >= 500 && error.response.status <= 599)) {
      config._retryCount = (config._retryCount || 0) + 1;
      console.warn(`[apiClient Retry]: Attempting retry ${config._retryCount} for ${config.url}...`);
      await new Promise((resolve) => setTimeout(resolve, 500 * config._retryCount));
      return apiClient(config);
    }

    return Promise.reject(error);
  }
);

/**
 * Sanitizes input text to prevent XSS injection.
 */
export const sanitizeInput = (input) => {
  if (typeof input !== 'string') return input;
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
};

export default apiClient;
