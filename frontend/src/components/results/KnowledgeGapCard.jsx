import React from 'react';
import { ShieldAlert } from 'lucide-react';
import { Badge } from '../ui/Badge';

export const KnowledgeGapCard = ({ knowledgeGaps = [] }) => {
  if (!knowledgeGaps.length) return null;

  return (
    <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-700/50 shadow-2xl flex flex-col gap-6">
      <div className="flex items-center gap-3 border-b border-slate-800/80 pb-4">
        <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
          <ShieldAlert className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-slate-100">Identified Knowledge Gaps</h3>
          <p className="text-xs text-slate-400">Specific concept gaps flagged during evaluation turns</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {knowledgeGaps.map((gap, idx) => (
          <div
            key={idx}
            className="bg-amber-950/20 border border-amber-500/20 rounded-xl p-4 flex flex-col gap-2"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-200">{gap.topic_title}</span>
              <Badge variant={gap.severity === 'High' ? 'rose' : 'amber'} size="sm">
                Day {gap.day_number}
              </Badge>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">{gap.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
