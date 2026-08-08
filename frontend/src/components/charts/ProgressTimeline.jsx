import React from 'react';
import { CheckCircle, Circle } from 'lucide-react';

export const ProgressTimeline = ({ turns = [] }) => {
  return (
    <div className="flex items-center justify-between w-full py-4 px-2">
      {turns.map((turn, idx) => (
        <div key={idx} className="flex flex-col items-center gap-1.5 relative">
          <div className="w-8 h-8 rounded-full bg-blue-600/20 border border-blue-500/40 text-blue-400 flex items-center justify-center font-bold text-xs">
            {idx + 1}
          </div>
          <span className="text-[10px] text-slate-400 font-mono">T{idx + 1}</span>
        </div>
      ))}
    </div>
  );
};
