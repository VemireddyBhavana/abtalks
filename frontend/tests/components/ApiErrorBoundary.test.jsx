import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ApiErrorBoundary } from '../../src/components/common/ApiErrorBoundary';

const ProblemChild = () => {
  throw new Error('API Timeout Error');
};

describe('ApiErrorBoundary Component', () => {
  it('should render children when no error occurs', () => {
    render(
      <ApiErrorBoundary>
        <div>Normal Component</div>
      </ApiErrorBoundary>
    );
    expect(screen.getByText('Normal Component')).toBeInTheDocument();
  });

  it('should render fallback UI when an API error is caught', () => {
    // Suppress console.error during expected error boundary test
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    render(
      <ApiErrorBoundary>
        <ProblemChild />
      </ApiErrorBoundary>
    );
    
    expect(screen.getByText('API Communication Failure')).toBeInTheDocument();
    expect(screen.getByText('API Timeout Error')).toBeInTheDocument();

    consoleSpy.mockRestore();
  });
});
