import api from '../config/api';

/**
 * Pings backend health check endpoint.
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('[Health Check Error]: Backend server unavailable', error);
    return { status: 'offline', healthy: false };
  }
};
