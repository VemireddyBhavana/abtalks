import apiClient from './apiClient';
import { API_ENDPOINTS } from '../constants/api';

/**
 * Initiates a new interview session.
 */
export const startInterview = async (candidateId = 'cand_alex_dev_99', sessionId = null, signal = null) => {
  const response = await apiClient.post(
    API_ENDPOINTS.START_INTERVIEW,
    { candidate_id: candidateId, session_id: sessionId },
    { signal }
  );
  return response.data;
};

/**
 * Submits candidate answer for current active question.
 */
export const submitAnswer = async (sessionId, answerText, signal = null) => {
  const response = await apiClient.post(
    API_ENDPOINTS.SUBMIT_ANSWER,
    { session_id: sessionId, answer_text: answerText },
    { signal }
  );
  return response.data;
};

/**
 * Fetches current active question for session.
 */
export const getCurrentQuestion = async (sessionId, signal = null) => {
  const response = await apiClient.get(API_ENDPOINTS.CURRENT_QUESTION(sessionId), { signal });
  return response.data;
};
