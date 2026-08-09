import apiClient from './apiClient';
import { API_ENDPOINTS } from '../constants/api';

/**
 * Fetches full session state model.
 */
export const getSessionState = async (sessionId, signal = null) => {
  const response = await apiClient.get(API_ENDPOINTS.SESSION_STATE(sessionId), { signal });
  return response.data;
};

/**
 * Fetches high-level session summary metadata & report if completed.
 */
export const getSessionSummary = async (sessionId, signal = null) => {
  const response = await apiClient.get(API_ENDPOINTS.SESSION_SUMMARY(sessionId), { signal });
  return response.data;
};
