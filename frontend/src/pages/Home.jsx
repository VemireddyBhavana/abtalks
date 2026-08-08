import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { PlayCircle, Sparkles, ShieldCheck, Cpu, Code2, ArrowRight } from 'lucide-react';
import { useInterview } from '../context/InterviewContext';

export const Home = () => {
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

  const features = [
    {
      icon: Cpu,
      title: 'LLM Question Generation',
      desc: 'Generates dynamic technical questions based on curriculum days and candidate profile using Gemini/OpenAI/Claude.',
    },
    {
      icon: ShieldCheck,
      title: 'Real-time Rubric Evaluation',
      desc: 'Evaluates technical accuracy, terminology, reasoning, and completeness across 7 weighted categories.',
    },
    {
      icon: Code2,
      title: 'Adaptive Follow-up Engine',
      desc: 'Probes deeper on strong answers, seeks clarification on average answers, or simplifies on weak answers.',
    },
  ];

  return (
    <div className="flex flex-col gap-12 py-6">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="glass-panel rounded-3xl p-8 sm:p-12 border border-slate-700/50 shadow-2xl relative overflow-hidden text-center flex flex-col items-center justify-center min-h-[420px]"
      >
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />

        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold mb-6">
          <Sparkles className="w-3.5 h-3.5" />
          <span>ABTalks AI Interview Agent Hackathon Edition</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black text-slate-100 tracking-tight leading-tight max-w-3xl mb-6">
          Master Full Stack AI Engineering with <span className="gradient-text">Adaptive AI Interviews</span>
        </h1>

        <p className="text-base sm:text-lg text-slate-300 max-w-2xl leading-relaxed mb-8">
          Autonomous technical interviewer that evaluates your React 19, FastAPI, Pydantic, and Agentic AI knowledge in real time.
        </p>

        <div className="flex flex-col sm:flex-row items-center gap-4">
          <button
            onClick={handleStart}
            disabled={loading}
            className="flex items-center gap-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold text-base shadow-xl shadow-blue-500/25 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
          >
            <PlayCircle className="w-5 h-5" />
            <span>{loading ? 'Initializing Session...' : 'Start AI Interview Now'}</span>
          </button>

          <button
            onClick={() => navigate('/lobby')}
            className="flex items-center gap-2 px-6 py-4 rounded-2xl bg-slate-800/80 hover:bg-slate-700/80 text-slate-200 font-semibold text-base border border-slate-700/60 transition-all"
          >
            <span>Enter Interview Lobby</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </motion.div>

      {/* Feature Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {features.map((f, idx) => {
          const Icon = f.icon;
          return (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              className="glass-panel glass-card-hover rounded-2xl p-6 border border-slate-700/40 flex flex-col gap-3"
            >
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                <Icon className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-100">{f.title}</h3>
              <p className="text-xs text-slate-400 leading-relaxed">{f.desc}</p>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};
