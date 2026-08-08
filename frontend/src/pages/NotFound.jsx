import React from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertCircle, Home as HomeIcon } from 'lucide-react';

export const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center space-y-6">
      <div className="w-20 h-20 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-400">
        <AlertCircle className="w-10 h-10" />
      </div>

      <div className="space-y-2">
        <h1 className="text-4xl font-extrabold text-white">404 - Page Not Found</h1>
        <p className="text-slate-400 text-sm max-w-md mx-auto">
          The requested page route does not exist or has been moved.
        </p>
      </div>

      <button
        onClick={() => navigate('/')}
        className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 text-slate-950 font-bold flex items-center gap-2 shadow-lg shadow-emerald-500/20 transition-all"
      >
        <HomeIcon className="w-4 h-4" />
        Return to Home
      </button>
    </div>
  );
};

export default NotFound;
