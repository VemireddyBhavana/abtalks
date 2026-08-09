import React, { createContext, useContext, useState, useEffect } from 'react';
import * as interviewApi from '../services/interview';
import * as resultsApi from '../services/results';
import * as sessionApi from '../services/session';
import * as healthApi from '../services/health';
import { sessionRecovery } from '../services/sessionRecovery';
import { eventLogger } from '../services/eventLogger';
import { useNetworkStatus } from '../hooks/useNetworkStatus';
import { notificationService } from '../services/notificationService';

const InterviewContext = createContext(null);

export const InterviewProvider = ({ children }) => {
  const [candidate, setCandidate] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [sessionId, setSessionId] = useState(() => sessionRecovery.getActiveSessionId());
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(8);
  const [answerText, setAnswerText] = useState('');
  const [isCompleted, setIsCompleted] = useState(false);
  const [feedbackReport, setFeedbackReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isBackendHealthy, setIsBackendHealthy] = useState(true);
  const [latencyMs, setLatencyMs] = useState(null);
  const [toastMessage, setToastMessage] = useState(null);

  const { isOnline, wasOffline } = useNetworkStatus();

  // Subscribe to notificationService events
  useEffect(() => {
    const unsubscribe = notificationService.subscribe((notification) => {
      setToastMessage(notification);
      setTimeout(() => setToastMessage(null), 4000);
    });
    return unsubscribe;
  }, []);

  // Show reconnect toast when coming back online
  useEffect(() => {
    if (wasOffline) {
      notificationService.notify('Network reconnected! Synchronizing state...', 'success');
      if (sessionId) {
        sessionRecovery.recoverSessionState().then((stateData) => {
          if (stateData) {
            setCurrentQuestionIndex(stateData.current_question_index);
            setIsCompleted(stateData.done);
          }
        });
      }
    }
  }, [wasOffline, sessionId]);

  // Check health and load candidate data on mount
  useEffect(() => {
    initApp();
  }, []);

  const initApp = async () => {
    setLoading(true);
    try {
      const health = await healthApi.checkHealth();
      setIsBackendHealthy(health.healthy !== false);
      setLatencyMs(health.latencyMs ?? null);

      const profile = await resultsApi.getCandidateProfile();
      const analyticsData = await resultsApi.getCandidateAnalytics();
      setCandidate(profile);
      setAnalytics(analyticsData);

      // Session restore on page refresh via sessionRecovery service
      const storedSessionId = sessionRecovery.getActiveSessionId();
      if (storedSessionId) {
        console.log(`[Session Restore]: Attempting state recovery for '${storedSessionId}'...`);
        const stateData = await sessionRecovery.recoverSessionState();
        if (stateData) {
          setSessionId(stateData.session_id);
          setCurrentQuestionIndex(stateData.current_question_index);
          setIsCompleted(stateData.done);
          if (stateData.plan?.questions?.[stateData.current_question_index]) {
            setCurrentQuestion(stateData.plan.questions[stateData.current_question_index]);
            eventLogger.questionViewed(
              stateData.plan.questions[stateData.current_question_index].id,
              stateData.current_question_index,
              stateData.plan.questions[stateData.current_question_index].topic_title
            );
          }
          if (stateData.done) {
            const summaryData = await sessionApi.getSessionSummary(storedSessionId);
            setFeedbackReport(summaryData.feedback_report);
          }
          console.log('[Session Restored]: State synchronized cleanly.');
        } else {
          setSessionId(null);
        }
      }
    } catch (err) {
      console.error('Failed to initialize app context:', err);
      eventLogger.apiError('initApp', err.message);
    } finally {
      setLoading(false);
    }
  };

  const showToast = (message, type = 'info') => {
    notificationService.notify(message, type);
  };

  const startSession = async (customCandidateId = 'cand_alex_dev_99') => {
    setLoading(true);
    setError(null);
    try {
      console.log('[Interview Started]: Initiating session request to FastAPI...');
      const data = await interviewApi.startInterview(customCandidateId);
      
      setSessionId(data.session_id);
      sessionRecovery.setActiveSessionId(data.session_id);
      
      setCurrentQuestion(data.question);
      eventLogger.interviewStarted(data.session_id, customCandidateId);
      if (data.question) {
        eventLogger.questionViewed(data.question.question_id, 0, data.question.topic_title);
      }
      
      setCurrentQuestionIndex(data.current_question_index);
      setTotalQuestions(data.total_questions);
      setAnswerText('');
      setIsCompleted(false);
      setFeedbackReport(null);
      
      showToast('Interview session initialized!', 'success');
      return data;
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to start interview session';
      setError(msg);
      eventLogger.apiError('/interview/start', msg);
      console.error('[Error]: Start interview failed:', msg);
      showToast(msg, 'error');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const submitTurnAnswer = async () => {
    if (!sessionId || !answerText.trim()) return;
    setLoading(true);
    setError(null);
    try {
      console.log(`[Answer Submitted]: Submitting candidate answer for turn ${currentQuestionIndex + 1}...`);
      eventLogger.answerSubmitted(sessionId, currentQuestionIndex, answerText.length);
      const data = await interviewApi.submitAnswer(sessionId, answerText);
      console.log('[Evaluation Received]: Turn evaluation processed by backend.');

      setIsCompleted(data.done);
      setCurrentQuestionIndex(data.current_question_index);

      if (data.done) {
        setFeedbackReport(data.feedback_report);
        setCurrentQuestion(null);
        eventLogger.interviewCompleted(sessionId, data.feedback_report?.overall_score);
        console.log('[Interview Completed]: Final feedback report generated.');
        showToast('Interview completed! Report generated.', 'success');
      } else {
        setCurrentQuestion(data.next_question);
        if (data.next_question) {
          eventLogger.questionViewed(
            data.next_question.question_id,
            data.current_question_index,
            data.next_question.topic_title
          );
        }
        setAnswerText('');
        showToast('Answer recorded. Next question loaded.', 'info');
      }
      return data;
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to submit answer';
      setError(msg);
      eventLogger.apiError('/interview/submit', msg);
      console.error('[Error]: Submit answer failed:', msg);
      showToast(msg, 'error');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const loadSummary = async (targetSessionId) => {
    setLoading(true);
    try {
      const data = await sessionApi.getSessionSummary(targetSessionId);
      setFeedbackReport(data.feedback_report);
      return data;
    } catch (err) {
      console.error('Failed to load session summary:', err);
      eventLogger.apiError(`/session/${targetSessionId}/summary`, err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <InterviewContext.Provider
      value={{
        candidate,
        analytics,
        sessionId,
        currentQuestion,
        currentQuestionIndex,
        totalQuestions,
        answerText,
        setAnswerText,
        isCompleted,
        feedbackReport,
        loading,
        error,
        isBackendHealthy,
        latencyMs,
        isOnline,
        toastMessage,
        showToast,
        startSession,
        submitTurnAnswer,
        loadSummary,
        fetchCandidateData: initApp,
      }}
    >
      {children}
    </InterviewContext.Provider>
  );
};

export const useInterview = () => {
  const context = useContext(InterviewContext);
  if (!context) {
    throw new Error('useInterview must be used within an InterviewProvider');
  }
  return context;
};
