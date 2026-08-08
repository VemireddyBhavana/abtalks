import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useInterview } from '../context/InterviewContext';
import { PlayCircle, ShieldCheck, CheckCircle2, AlertCircle } from 'lucide-react';

export const InterviewLobby = () => {
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

  const rules = [
    'The evaluation consists of 8 planned technical questions covering Full Stack AI Engineering.',
    'Questions span React 19, FastAPI, Pydantic, System Prompts, MCP Tools, and Agent Loops.',
    'The AI engine evaluates your answers using weighted rubrics and asks adaptive follow-ups.',
    'Once completed, a structured Feedback Report & Final Scorecard will be generated automatically.',
  ];

  return (
    <div className="max-w-3xl mx-auto py-8">
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel rounded-3xl p-8 border border-slate-700/50 shadow-2xl flex flex-col gap-6"
      >
        <div className="flex items-center gap-4 border-b border-slate-800 pb-6">
          <div className="w-12 h-12 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-100">AI Technical Interview Lobby</h1>
            <p className="text-xs text-slate-400">Pre-flight system checks & rules guidelines</p>
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex flex-col gap-3">
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider mb-2">
            Interview Rules & Guidelines
          </h3>
          {rules.map((rule, idx) => (
            <div key={idx} className="flex items-start gap-3 text-xs text-slate-300">
              <CheckCircle2 className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
              <span className="leading-relaxed">{rule}</span>
            </div>
          ))}
        </div>

        <div className="flex items-center justify-between pt-4">
          <button
            onClick={() => navigate('/')}
            className="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-semibold transition-all"
          >
            Back to Home
          </button>

          <button
            onClick={handleStart}
            disabled={loading}
            className="flex items-center gap-2.5 px-7 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-sm shadow-xl shadow-blue-500/20 transition-all"
          >
            <PlayCircle className="w-5 h-5" />
            <span>{loading ? 'Starting...' : 'Begin Technical Session'}</span>
          </button>
        </div>
      </motion.div>
    </div>
  );
};
