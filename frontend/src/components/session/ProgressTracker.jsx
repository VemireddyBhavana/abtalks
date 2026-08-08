import React from 'react';
import { motion } from 'framer-motion';

export const ProgressTracker = ({ currentQuestionIndex = 0, totalQuestions = 8 }) => {
  const percentage = Math.round(((currentQuestionIndex + 1) / totalQuestions) * 100);

  return (
    <div className="w-full">
      <div className="flex items-center justify-between text-xs font-medium text-slate-400 mb-2">
        <span>
          Question <strong className="text-slate-100">{currentQuestionIndex + 1}</strong> of{' '}
          <strong className="text-slate-100">{totalQuestions}</strong>
        </span>
        <span className="text-blue-400 font-semibold">{percentage}% Complete</span>
      </div>

      <div className="w-full h-2.5 bg-slate-800/80 rounded-full overflow-hidden border border-slate-700/30 p-0.5">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="h-full bg-gradient-to-r from-blue-600 via-indigo-500 to-cyan-400 rounded-full shadow-lg shadow-blue-500/30"
        />
      </div>
    </div>
  );
};
