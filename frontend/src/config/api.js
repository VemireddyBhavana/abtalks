import axios from 'axios';
import { API_BASE_URL } from './env';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor
api.interceptors.request.use(
  (config) => {
    // Development mode request logging
    if (import.meta.env.DEV) {
      console.log(`[API Request] ${config.method?.toUpperCase()} -> ${config.url}`);
    }
    // Auth header placeholder
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor with retry logic for transient failures
api.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log(`[API Response] ${response.status} <- ${response.config.url}`);
    }
    return response;
  },
  async (error) => {
    const config = error.config;
    if (!config || config._retryCount >= 2) {
      const formattedMessage = error.response?.data?.detail || error.message || 'API request failed';
      console.error('[API Error]:', formattedMessage);
      return Promise.reject(error);
    }

    // Retry transient network timeouts or 5xx server errors
    if (!error.response || (error.response.status >= 500 && error.response.status <= 599)) {
      config._retryCount = (config._retryCount || 0) + 1;
      console.warn(`[API Retry]: Attempting retry ${config._retryCount} for ${config.url}...`);
      await new Promise((resolve) => setTimeout(resolve, 500 * config._retryCount));
      return api(config);
    }

    return Promise.reject(error);
  }
);

export default api;
