import api from '../config/api';

/**
 * Fetches full session state model.
 */
export const getSessionState = async (sessionId) => {
  const response = await api.get(`/api/v1/interview/${sessionId}/state`);
  return response.data;
};

/**
 * Fetches high-level session summary metadata & report if completed.
 */
export const getSessionSummary = async (sessionId) => {
  const response = await api.get(`/api/v1/interview/${sessionId}/summary`);
  return response.data;
};
