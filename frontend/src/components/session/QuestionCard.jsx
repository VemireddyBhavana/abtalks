import React from 'react';
import { motion } from 'framer-motion';
import { TopicBadge } from './TopicBadge';
import { DifficultyBadge } from './DifficultyBadge';
import { HelpCircle } from 'lucide-react';

export const QuestionCard = ({ question }) => {
  if (!question) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-700/50 shadow-2xl relative overflow-hidden"
    >
      <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
        <TopicBadge title={question.topic_title} dayNumber={question.day_number} />
        <DifficultyBadge difficulty={question.difficulty} />
      </div>

      <div className="flex gap-4 items-start">
        <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 shrink-0 mt-1">
          <HelpCircle className="w-5 h-5" />
        </div>

        <div className="flex-1">
          <h2 className="text-xl sm:text-2xl font-bold text-slate-100 leading-snug tracking-tight">
            {question.question_text}
          </h2>
          <p className="text-xs text-slate-400 mt-3">
            Provide a clear, detailed technical explanation covering core concepts, tools, and architecture trade-offs.
          </p>
        </div>
      </div>
    </motion.div>
  );
};
