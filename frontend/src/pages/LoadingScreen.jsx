import React from 'react';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const LoadingScreen = () => {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <LoadingSpinner label="Evaluating Technical Responses & Generating Scorecard..." size="lg" />
    </div>
  );
};
