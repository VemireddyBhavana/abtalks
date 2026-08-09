import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { ErrorBoundary } from '../components/common/ErrorBoundary';
import { ApiErrorBoundary } from '../components/common/ApiErrorBoundary';
import { ThemeProvider } from './ThemeContext';
import { LoadingProvider } from './LoadingContext';
import { InterviewProvider } from './InterviewContext';

export const AppProvider = ({ children }) => {
  return (
    <ErrorBoundary>
      <ApiErrorBoundary>
        <ThemeProvider>
          <LoadingProvider>
            <InterviewProvider>
              <BrowserRouter>
                {children}
              </BrowserRouter>
            </InterviewProvider>
          </LoadingProvider>
        </ThemeProvider>
      </ApiErrorBoundary>
    </ErrorBoundary>
  );
};
