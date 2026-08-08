/**
 * @typedef {Object} InterviewSessionState
 * @property {string} sessionId - Session unique identifier
 * @property {'idle'|'active'|'paused'|'completed'} status - Current lifecycle status
 * @property {number} currentQuestionIndex - Active question index tracker
 */

export const SessionPlaceholder = {
  sessionId: '',
  status: 'idle',
  currentQuestionIndex: 0,
};

export default SessionPlaceholder;
