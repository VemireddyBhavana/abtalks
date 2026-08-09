import React from 'react';
import { Navigate } from 'react-router-dom';
import { useInterview } from '../../context/InterviewContext';
import { LoadingSpinner } from './LoadingSpinner';

/**
 * Route guard requiring an active interview session ID to view /interview.
 */
export const RequireSession = ({ children }) => {
  const { sessionId, loading } = useInterview();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <LoadingSpinner label="Validating active session..." size="lg" />
      </div>
    );
  }

  if (!sessionId) {
    console.warn('[Route Guard]: Redirecting to /lobby - No active session ID found or session expired.');
    return <Navigate to="/lobby" replace />;
  }

  return children;
};

/**
 * Route guard requiring a completed feedback report to view /result.
 */
export const RequireCompletedInterview = ({ children }) => {
  const { feedbackReport, loading } = useInterview();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <LoadingSpinner label="Validating report status..." size="lg" />
      </div>
    );
  }

  if (!feedbackReport) {
    console.warn('[Route Guard]: Redirecting to /lobby - No completed feedback report found.');
    return <Navigate to="/lobby" replace />;
  }

  return children;
};
