import { env } from './env';

/**
 * API configuration and endpoints registry
 */
export const apiConfig = {
  baseURL: env.apiBaseUrl,
  timeout: 10000,
  endpoints: {
    rootHealth: '/',
    v1Health: '/api/v1/health',
    // Future endpoint placeholders
    interview: '/api/v1/interview',
    feedback: '/api/v1/feedback',
    session: '/api/v1/session',
  },
};

export default apiConfig;
