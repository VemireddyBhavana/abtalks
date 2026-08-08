import React from 'react';
import { useInterview } from '../../context/InterviewContext';
import { User, Activity, AlertCircle } from 'lucide-react';

export const Navbar = () => {
  const { candidate, isBackendHealthy } = useInterview();

  return (
    <header className="hidden lg:flex items-center justify-between px-8 py-4 glass-panel border-b border-slate-800/80 sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <span
          className={`w-2.5 h-2.5 rounded-full animate-pulse ${
            isBackendHealthy ? 'bg-emerald-400' : 'bg-rose-400'
          }`}
        />
        <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
          {isBackendHealthy ? (
            'FastAPI Engine: Online'
          ) : (
            <span className="text-rose-400 flex items-center gap-1">
              <AlertCircle className="w-3.5 h-3.5" />
              FastAPI Engine: Offline
            </span>
          )}
        </span>
      </div>

      <div className="flex items-center gap-4">
        {candidate && (
          <div className="flex items-center gap-3 bg-slate-800/40 border border-slate-700/40 px-3.5 py-1.5 rounded-xl">
            <div className="w-7 h-7 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-xs">
              <User className="w-4 h-4" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-200">{candidate.full_name}</p>
              <p className="text-[10px] text-slate-400">{candidate.target_role}</p>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};
