import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Home, HelpCircle } from 'lucide-react';

export const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-6">
      <div className="w-20 h-20 rounded-3xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-6">
        <HelpCircle className="w-10 h-10" />
      </div>
      <h1 className="text-4xl font-black text-slate-100 mb-2">404</h1>
      <h2 className="text-xl font-bold text-slate-300 mb-4">Page Not Found</h2>
      <p className="text-xs text-slate-400 max-w-sm mb-8">
        The requested URL was not found on this application server.
      </p>
      <button
        onClick={() => navigate('/')}
        className="flex items-center gap-2 px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition-all shadow-lg shadow-blue-500/20"
      >
        <Home className="w-4 h-4" />
        <span>Return to Home</span>
      </button>
    </div>
  );
};
