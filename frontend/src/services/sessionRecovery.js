import * as sessionApi from './session';

export const sessionRecovery = {
  getActiveSessionId: () => {
    return localStorage.getItem('abtalks_active_session_id') || null;
  },

  setActiveSessionId: (sessionId) => {
    if (sessionId) {
      localStorage.setItem('abtalks_active_session_id', sessionId);
    } else {
      localStorage.removeItem('abtalks_active_session_id');
    }
  },

  clearActiveSession: () => {
    localStorage.removeItem('abtalks_active_session_id');
  },

  recoverSessionState: async () => {
    const sessionId = sessionRecovery.getActiveSessionId();
    if (!sessionId) return null;

    try {
      console.log(`[sessionRecovery]: Recovering state for session '${sessionId}'...`);
      const state = await sessionApi.getSessionState(sessionId);
      return state;
    } catch (err) {
      console.warn(`[sessionRecovery Warning]: Session '${sessionId}' recovery failed. Invalidation applied:`, err);
      sessionRecovery.clearActiveSession();
      return null;
    }
  },
};
