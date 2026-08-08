import React from 'react';
import { ThumbsUp, AlertCircle, Sparkles, MessageSquare } from 'lucide-react';

export const FeedbackCard = ({ strengths = [], weaknesses = [], summary }) => {
  return (
    <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-700/50 shadow-2xl flex flex-col gap-6">
      <div className="flex items-center gap-3 border-b border-slate-800/80 pb-4">
        <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
          <MessageSquare className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-slate-100">Executive Summary & Assessment</h3>
          <p className="text-xs text-slate-400">AI Interview Agent Narrative Analysis</p>
        </div>
      </div>

      {summary && (
        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4 leading-relaxed text-sm text-slate-300">
          <p className="font-medium">{summary.overall_performance}</p>
          <p className="text-xs text-slate-400 mt-2">{summary.communication_assessment}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="bg-emerald-950/20 border border-emerald-500/20 rounded-xl p-4">
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-wider mb-3">
            <ThumbsUp className="w-4 h-4" />
            <span>Key Technical Strengths</span>
          </div>
          <ul className="flex flex-col gap-2">
            {strengths.map((s, idx) => (
              <li key={idx} className="flex items-start gap-2 text-xs text-slate-300">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0 mt-1.5" />
                <span>{s}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Weaknesses */}
        <div className="bg-rose-950/20 border border-rose-500/20 rounded-xl p-4">
          <div className="flex items-center gap-2 text-xs font-bold text-rose-400 uppercase tracking-wider mb-3">
            <AlertCircle className="w-4 h-4" />
            <span>Areas for Improvement</span>
          </div>
          <ul className="flex flex-col gap-2">
            {weaknesses.map((w, idx) => (
              <li key={idx} className="flex items-start gap-2 text-xs text-slate-300">
                <span className="w-1.5 h-1.5 rounded-full bg-rose-400 shrink-0 mt-1.5" />
                <span>{w}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
