import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { ErrorBoundary } from '../components/common/ErrorBoundary';
import { ThemeProvider } from './ThemeContext';
import { InterviewProvider } from './InterviewContext';

export const AppProvider = ({ children }) => {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <InterviewProvider>
          <BrowserRouter>
            {children}
          </BrowserRouter>
        </InterviewProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
};
