import api from '../config/api';

/**
 * Initiates a new interview session.
 */
export const startInterview = async (candidateId = 'cand_alex_dev_99', sessionId = null) => {
  const response = await api.post('/api/v1/interview/start', {
    candidate_id: candidateId,
    session_id: sessionId,
  });
  return response.data;
};

/**
 * Submits candidate answer for current active question.
 */
export const submitAnswer = async (sessionId, answerText) => {
  const response = await api.post('/api/v1/interview/answer', {
    session_id: sessionId,
    answer_text: answerText,
  });
  return response.data;
};

/**
 * Fetches current active question for session.
 */
export const getCurrentQuestion = async (sessionId) => {
  const response = await api.get(`/api/v1/interview/${sessionId}/current-question`);
  return response.data;
};
