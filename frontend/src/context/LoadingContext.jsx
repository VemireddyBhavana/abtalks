import React, { createContext, useContext, useState } from 'react';

const LoadingContext = createContext(null);

export const LoadingProvider = ({ children }) => {
  const [globalLoading, setGlobalLoading] = useState(false);
  const [pageLoading, setPageLoading] = useState(false);
  const [apiLoading, setApiLoading] = useState(false);

  return (
    <LoadingContext.Provider
      value={{
        globalLoading,
        setGlobalLoading,
        pageLoading,
        setPageLoading,
        apiLoading,
        setApiLoading,
      }}
    >
      {children}
    </LoadingContext.Provider>
  );
};

export const useLoading = () => {
  const context = useContext(LoadingContext);
  if (!context) {
    throw new Error('useLoading must be used within a LoadingProvider');
  }
  return context;
};
