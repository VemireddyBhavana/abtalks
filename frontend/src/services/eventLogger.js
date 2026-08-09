export const eventLogger = {
  logEvent: (eventName, details = {}) => {
    if (import.meta.env.DEV) {
      console.log(`[Event Analytics]: ${eventName}`, details);
    }
  },

  interviewStarted: (sessionId, candidateId) => {
    eventLogger.logEvent('Interview started', { sessionId, candidateId, timestamp: new Date().toISOString() });
  },

  questionViewed: (questionId, turnIndex, topicTitle) => {
    eventLogger.logEvent('Question viewed', { questionId, turnIndex, topicTitle });
  },

  answerSubmitted: (sessionId, turnIndex, answerLength) => {
    eventLogger.logEvent('Answer submitted', { sessionId, turnIndex, answerLength });
  },

  interviewCompleted: (sessionId, overallScore) => {
    eventLogger.logEvent('Interview completed', { sessionId, overallScore });
  },

  apiError: (endpoint, message) => {
    eventLogger.logEvent('API error', { endpoint, message });
  },
};
