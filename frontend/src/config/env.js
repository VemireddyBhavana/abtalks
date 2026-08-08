/**
 * Environment configuration wrapper
 */
export const env = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  appTitle: import.meta.env.VITE_APP_TITLE || 'AI Interview Agent',
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD,
};

export default env;
