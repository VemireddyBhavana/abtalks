import React from 'react';

export const CurriculumCoverageChart = ({ completedDays = 4, totalDays = 5 }) => {
  const percentage = Math.round((completedDays / totalDays) * 100);

  return (
    <div className="flex flex-col items-center gap-3 p-4 glass-panel rounded-xl">
      <div className="flex items-center justify-between w-full text-xs font-semibold text-slate-300">
        <span>Curriculum Day Coverage</span>
        <span className="text-emerald-400 font-bold">{percentage}%</span>
      </div>
      <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden p-0.5 border border-slate-700/40">
        <div
          className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 rounded-full transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
