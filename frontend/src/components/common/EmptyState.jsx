import React from 'react';
import { Inbox } from 'lucide-react';

export const EmptyState = ({
  title = 'No Data Found',
  description = 'There are no active records to display right now.',
  actionLabel,
  onAction,
}) => {
  return (
    <div className="glass-panel rounded-2xl p-12 text-center flex flex-col items-center justify-center max-w-lg mx-auto my-8">
      <div className="w-16 h-16 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-4">
        <Inbox className="w-8 h-8" />
      </div>
      <h3 className="text-xl font-bold text-slate-100 mb-2">{title}</h3>
      <p className="text-sm text-slate-400 mb-6">{description}</p>
      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-medium text-sm shadow-lg shadow-blue-500/20 transition-all"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
};
