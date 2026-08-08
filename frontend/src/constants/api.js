export const API_ENDPOINTS = {
  START_INTERVIEW: '/api/v1/interview/start',
  SUBMIT_ANSWER: '/api/v1/interview/answer',
  CURRENT_QUESTION: (sessionId) => `/api/v1/interview/${sessionId}/current-question`,
  SESSION_STATE: (sessionId) => `/api/v1/interview/${sessionId}/state`,
  SESSION_SUMMARY: (sessionId) => `/api/v1/interview/${sessionId}/summary`,
  CANDIDATE_PROFILE: '/api/v1/candidate',
  CANDIDATE_ANALYTICS: '/api/v1/candidate/analytics',
  CURRICULUM: '/api/v1/curriculum',
};
