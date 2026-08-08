/**
 * Environment configuration wrapper
 */
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const env = {
  apiBaseUrl: API_BASE_URL,
  appTitle: import.meta.env.VITE_APP_TITLE || 'AI Interview Agent',
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD,
};

export default env;
