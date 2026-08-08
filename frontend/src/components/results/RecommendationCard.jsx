import React from 'react';
import { BookOpen, ArrowRight, CheckCircle2 } from 'lucide-react';
import { Badge } from '../ui/Badge';

export const RecommendationCard = ({ recommendations = [] }) => {
  if (!recommendations.length) return null;

  return (
    <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-slate-700/50 shadow-2xl flex flex-col gap-6">
      <div className="flex items-center gap-3 border-b border-slate-800/80 pb-4">
        <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
          <BookOpen className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-slate-100">Curriculum Study Recommendations</h3>
          <p className="text-xs text-slate-400">Actionable learning objectives mapped to curriculum days</p>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        {recommendations.map((rec, idx) => (
          <div
            key={idx}
            className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-4"
          >
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <Badge variant="blue" size="sm">
                  Day {rec.curriculum_day}
                </Badge>
                <Badge
                  variant={rec.priority === 'Critical' || rec.priority === 'High' ? 'rose' : 'amber'}
                  size="sm"
                >
                  {rec.priority} Priority
                </Badge>
                <span className="text-xs font-bold text-slate-200">{rec.topic_title}</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">{rec.recommended_action}</p>

              {rec.learning_objectives?.length > 0 && (
                <div className="mt-2.5 flex flex-wrap gap-1.5">
                  {rec.learning_objectives.map((obj, i) => (
                    <span
                      key={i}
                      className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded border border-slate-700/40 flex items-center gap-1"
                    >
                      <CheckCircle2 className="w-3 h-3 text-blue-400" />
                      <span>{obj}</span>
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
