import React from 'react';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '../src/context/ThemeContext';
import { LoadingProvider } from '../src/context/LoadingContext';
import { InterviewProvider } from '../src/context/InterviewContext';

/**
 * Custom render helper that automatically wraps component under test with all application context providers.
 */
export const renderWithProviders = (ui, options = {}) => {
  const Wrapper = ({ children }) => (
    <ThemeProvider>
      <LoadingProvider>
        <InterviewProvider>
          <BrowserRouter>{children}</BrowserRouter>
        </InterviewProvider>
      </LoadingProvider>
    </ThemeProvider>
  );

  return render(ui, { wrapper: Wrapper, ...options });
};

export * from '@testing-library/react';
