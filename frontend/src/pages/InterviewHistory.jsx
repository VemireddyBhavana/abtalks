import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useInterview } from '../context/InterviewContext';
import { History, PlayCircle, Award, Calendar } from 'lucide-react';
import { Badge } from '../components/ui/Badge';

export const InterviewHistory = () => {
  const navigate = useNavigate();
  const { startSession, loading } = useInterview();

  const handleStart = async () => {
    try {
      await startSession();
      navigate('/interview');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col gap-6 py-4 max-w-4xl mx-auto">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
            <History className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-100">Interview Session History</h1>
            <p className="text-xs text-slate-400">Persistent Breeth Memory session archives</p>
          </div>
        </div>

        <button
          onClick={handleStart}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition-all"
        >
          <PlayCircle className="w-4 h-4" />
          <span>New Session</span>
        </button>
      </div>

      <div className="glass-panel rounded-2xl p-6 border border-slate-700/40 text-center py-12">
        <Award className="w-12 h-12 text-blue-400 mx-auto mb-3 opacity-80" />
        <h3 className="text-base font-bold text-slate-200 mb-1">Persistent Breeth Memory Active</h3>
        <p className="text-xs text-slate-400 max-w-md mx-auto mb-6">
          All session turns, rubrics, and feedback scorecards are automatically persisted in Breeth Persistent Memory.
        </p>
        <button
          onClick={handleStart}
          className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-xs transition-all shadow-lg shadow-blue-500/20"
        >
          Launch Active Interview Session
        </button>
      </div>
    </div>
  );
};
