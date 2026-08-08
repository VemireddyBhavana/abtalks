import React from 'react';

export const AuthLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-[#0b0f19] flex items-center justify-center p-6 text-slate-100">
      <div className="w-full max-w-md glass-panel p-8 rounded-2xl border border-slate-700/50 shadow-2xl">
        {children}
      </div>
    </div>
  );
};
