import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useInterview } from '../context/InterviewContext';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { Badge } from '../components/ui/Badge';
import { User, Award, BookOpen, Activity, PlayCircle, TrendingUp } from 'lucide-react';

export const CandidateDashboard = () => {
  const navigate = useNavigate();
  const { candidate, analytics, startSession, loading } = useInterview();

  if (!candidate || !analytics) {
    return <LoadingSpinner label="Loading Candidate Profile & Analytics..." />;
  }

  const handleStart = async () => {
    try {
      await startSession();
      navigate('/interview');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col gap-8 py-4">
      {/* Header Banner */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-700/50 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-6"
      >
        <div className="flex items-center gap-5">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white font-bold text-2xl shadow-lg shadow-blue-500/30 shrink-0">
            <User className="w-8 h-8" />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Badge variant="blue" size="sm">{candidate.experience_level}</Badge>
              <span className="text-xs text-slate-400 font-mono">ID: {candidate.candidate_id}</span>
            </div>
            <h1 className="text-2xl font-bold text-slate-100">{candidate.full_name}</h1>
            <p className="text-xs text-slate-400">{candidate.target_role} • Email: {candidate.email}</p>
          </div>
        </div>

        <button
          onClick={handleStart}
          disabled={loading}
          className="flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-sm shadow-xl shadow-blue-500/20 transition-all shrink-0"
        >
          <PlayCircle className="w-5 h-5" />
          <span>Launch AI Interview</span>
        </button>
      </motion.div>

      {/* Analytics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="glass-panel rounded-2xl p-6 border border-slate-700/40 flex flex-col gap-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Curriculum Completion</span>
            <BookOpen className="w-4 h-4 text-blue-400" />
          </div>
          <span className="text-3xl font-black text-slate-100">
            {analytics.completion_rate_percentage}%
          </span>
          <p className="text-xs text-slate-400">
            {analytics.completed_days_count} of {analytics.total_days} Curriculum Days Completed
          </p>
        </div>

        <div className="glass-panel rounded-2xl p-6 border border-slate-700/40 flex flex-col gap-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Mastered Topics</span>
            <Award className="w-4 h-4 text-emerald-400" />
          </div>
          <span className="text-3xl font-black text-emerald-400">
            {candidate.completed_topics.length}
          </span>
          <p className="text-xs text-slate-400">High-proficiency core full-stack topics</p>
        </div>

        <div className="glass-panel rounded-2xl p-6 border border-slate-700/40 flex flex-col gap-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Remaining Days</span>
            <TrendingUp className="w-4 h-4 text-amber-400" />
          </div>
          <span className="text-3xl font-black text-amber-400">
            {analytics.remaining_days_count}
          </span>
          <p className="text-xs text-slate-400">Curriculum days scheduled for review</p>
        </div>
      </div>
    </div>
  );
};
