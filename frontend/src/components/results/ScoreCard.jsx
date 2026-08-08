import React from 'react';
import { motion } from 'framer-motion';
import { Award, TrendingUp, CheckCircle } from 'lucide-react';

export const ScoreCard = ({ overallScore }) => {
  if (!overallScore) return null;

  const { overall_score, grade, rating_label, breakdown } = overallScore;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-700/50 shadow-2xl relative overflow-hidden"
    >
      <div className="flex flex-col md:flex-row items-center justify-between gap-6 pb-6 border-b border-slate-800/80">
        <div className="flex items-center gap-5">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex flex-col items-center justify-center text-white shadow-xl shadow-blue-500/30 shrink-0">
            <span className="text-3xl font-black">{overall_score}</span>
            <span className="text-[10px] font-semibold text-blue-200 uppercase tracking-widest">Score</span>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 rounded-md bg-blue-500/20 text-blue-400 font-bold text-xs border border-blue-500/30">
                Grade {grade}
              </span>
              <span className="text-xs font-semibold text-slate-400">{rating_label} Performance</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-slate-100 gradient-text">
              Final Evaluation Scorecard
            </h2>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 bg-emerald-950/40 border border-emerald-500/30 px-3.5 py-2 rounded-xl">
          <Award className="w-4 h-4" />
          <span>Evaluation Verified</span>
        </div>
      </div>

      <div className="mt-6">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">
          Category Score Breakdown
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {breakdown.map((cat, idx) => (
            <div
              key={idx}
              className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-3.5 flex flex-col gap-1.5"
            >
              <div className="flex items-center justify-between text-xs font-medium">
                <span className="text-slate-300 font-semibold">{cat.category_name}</span>
                <span className="text-blue-400 font-bold">{cat.score} / 100</span>
              </div>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-indigo-400 rounded-full"
                  style={{ width: `${Math.min(100, cat.score)}%` }}
                />
              </div>
              <p className="text-[10px] text-slate-500 mt-0.5">
                Weight: {Math.round(cat.weight * 100)}% • Contribution: {cat.weighted_score} pts
              </p>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};
