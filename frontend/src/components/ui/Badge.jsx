import React from 'react';

export const Badge = ({ children, variant = 'default', size = 'md', className = '' }) => {
  const variants = {
    default: 'bg-slate-800 text-slate-300 border-slate-700/50',
    blue: 'bg-blue-950/60 text-blue-400 border-blue-500/30',
    purple: 'bg-purple-950/60 text-purple-400 border-purple-500/30',
    emerald: 'bg-emerald-950/60 text-emerald-400 border-emerald-500/30',
    amber: 'bg-amber-950/60 text-amber-400 border-amber-500/30',
    rose: 'bg-rose-950/60 text-rose-400 border-rose-500/30',
  };

  const sizes = {
    sm: 'px-2 py-0.5 text-[10px]',
    md: 'px-2.5 py-1 text-xs',
    lg: 'px-3 py-1.5 text-sm',
  };

  return (
    <span
      className={`inline-flex items-center font-semibold rounded-lg border backdrop-blur-sm ${variants[variant]} ${sizes[size]} ${className}`}
    >
      {children}
    </span>
  );
};
