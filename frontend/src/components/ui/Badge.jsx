import React from 'react';

export const Badge = ({ children, variant = 'emerald', className = '' }) => {
  const variants = {
    emerald: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
    amber: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
    cyan: 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400',
    slate: 'bg-slate-800 border-slate-700 text-slate-300',
  };

  const selected = variants[variant] || variants.emerald;

  return (
    <span
      className={`inline-flex items-center space-x-1.5 px-3 py-1 rounded-full border text-xs font-semibold ${selected} ${className}`}
    >
      {children}
    </span>
  );
};

export default Badge;
