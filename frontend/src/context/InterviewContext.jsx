import React, { createContext, useContext, useState, useEffect } from 'react';
import * as interviewApi from '../services/interview';
import * as resultsApi from '../services/results';
import * as sessionApi from '../services/session';

const InterviewContext = createContext(null);

export const InterviewProvider = ({ children }) => {
  const [candidate, setCandidate] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(8);
  const [answerText, setAnswerText] = useState('');
  const [isCompleted, setIsCompleted] = useState(false);
  const [feedbackReport, setFeedbackReport] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [toastMessage, setToastMessage] = useState(null);

  // Load candidate profile & analytics on initial mount
  useEffect(() => {
    fetchCandidateData();
  }, []);

  const fetchCandidateData = async () => {
    try {
      const profile = await resultsApi.getCandidateProfile();
      const analyticsData = await resultsApi.getCandidateAnalytics();
      setCandidate(profile);
      setAnalytics(analyticsData);
    } catch (err) {
      console.error('Failed to load candidate data:', err);
    }
  };

  const showToast = (message, type = 'info') => {
    setToastMessage({ message, type, id: Date.now() });
    setTimeout(() => {
      setToastMessage(null);
    }, 4000);
  };

  const startSession = async (customCandidateId = 'cand_alex_dev_99') => {
    setLoading(true);
    setError(null);
    try {
      const data = await interviewApi.startInterview(customCandidateId);
      setSessionId(data.session_id);
      setCurrentQuestion(data.question);
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
      const data = await interviewApi.submitAnswer(sessionId, answerText);
      setIsCompleted(data.done);
      setCurrentQuestionIndex(data.current_question_index);

      if (data.done) {
        setFeedbackReport(data.feedback_report);
        setCurrentQuestion(null);
        showToast('Interview completed! Report generated.', 'success');
      } else {
        setCurrentQuestion(data.next_question);
        setAnswerText('');
        showToast('Answer recorded. Next question loaded.', 'info');
      }
      return data;
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to submit answer';
      setError(msg);
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
        history,
        loading,
        error,
        toastMessage,
        showToast,
        startSession,
        submitTurnAnswer,
        loadSummary,
        fetchCandidateData,
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
