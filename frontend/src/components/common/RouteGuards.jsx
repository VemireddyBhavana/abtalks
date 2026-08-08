import React from 'react';
import { Navigate } from 'react-router-dom';
import { useInterview } from '../../context/InterviewContext';

/**
 * Route guard requiring an active interview session ID to view /interview.
 */
export const RequireSession = ({ children }) => {
  const { sessionId } = useInterview();

  if (!sessionId) {
    console.warn('[Route Guard]: Redirecting to /lobby - No active session ID found.');
    return <Navigate to="/lobby" replace />;
  }

  return children;
};

/**
 * Route guard requiring a completed feedback report to view /result.
 */
export const RequireCompletedInterview = ({ children }) => {
  const { feedbackReport } = useInterview();

  if (!feedbackReport) {
    console.warn('[Route Guard]: Redirecting to /lobby - No completed feedback report found.');
    return <Navigate to="/lobby" replace />;
  }

  return children;
};
