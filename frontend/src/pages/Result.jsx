import React from 'react';
import { Award, BarChart2, CheckCircle2, Download, FileText } from 'lucide-react';

export const Result = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 glass-card p-6 rounded-2xl border border-slate-800">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-emerald-400">
            Evaluation Report
          </span>
          <h1 className="text-2xl font-bold text-white">Interview Results & Scorecard</h1>
          <p className="text-sm text-slate-400">
            Placeholder feedback summary and candidate scorecard view.
          </p>
        </div>

        <button
          disabled
          className="px-4 py-2 rounded-xl bg-slate-800 text-slate-500 font-medium text-sm flex items-center gap-2 cursor-not-allowed border border-slate-700"
        >
          <Download className="w-4 h-4" />
          Export Scorecard PDF
        </button>
      </div>

      {/* Grid of Mock Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="glass-card p-5 rounded-2xl space-y-2 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Overall Rating</span>
            <Award className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">-- / 100</div>
          <p className="text-xs text-slate-400">Pending Evaluation Engine</p>
        </div>

        <div className="glass-card p-5 rounded-2xl space-y-2 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Technical Skill</span>
            <BarChart2 className="w-5 h-5 text-teal-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">-- %</div>
          <p className="text-xs text-slate-400">Placeholder metric</p>
        </div>

        <div className="glass-card p-5 rounded-2xl space-y-2 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Communication</span>
            <CheckCircle2 className="w-5 h-5 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">-- %</div>
          <p className="text-xs text-slate-400">Placeholder metric</p>
        </div>

        <div className="glass-card p-5 rounded-2xl space-y-2 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase">Problem Solving</span>
            <FileText className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">-- %</div>
          <p className="text-xs text-slate-400">Placeholder metric</p>
        </div>

      </div>

      {/* Main Feedback Box Placeholder */}
      <div className="glass-card p-6 rounded-2xl space-y-3 border border-slate-800">
        <h3 className="text-base font-bold text-white">Detailed AI Feedback Summary</h3>
        <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-sm text-slate-400">
          Candidate scoring feedback and rubric breakdowns will appear here after interview sessions are completed.
        </div>
      </div>
    </div>
  );
};

export default Result;
