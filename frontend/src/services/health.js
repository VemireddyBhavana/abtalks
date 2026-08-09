import apiClient from './apiClient';

/**
 * Enhanced health check service with latency tracking in milliseconds.
 */
export const checkHealth = async () => {
  const startTime = performance.now();
  try {
    const response = await apiClient.get('/health');
    const latencyMs = Math.round(performance.now() - startTime);
    return {
      healthy: true,
      status: response.data.status || 'ok',
      latencyMs,
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    const latencyMs = Math.round(performance.now() - startTime);
    console.error(`[Health Check Error]: Backend offline (${latencyMs}ms)`, error);
    return {
      healthy: false,
      status: 'offline',
      latencyMs,
      timestamp: new Date().toISOString(),
    };
  }
};
