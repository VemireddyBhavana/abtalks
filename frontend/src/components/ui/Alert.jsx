import React from 'react';
import { Info, CheckCircle2, AlertTriangle, AlertCircle } from 'lucide-react';

export const Alert = ({ title, children, variant = 'info', className = '' }) => {
  const icons = {
    info: Info,
    success: CheckCircle2,
    warning: AlertTriangle,
    error: AlertCircle,
  };

  const variants = {
    info: 'bg-sky-950/40 border-sky-500/30 text-sky-200',
    success: 'bg-emerald-950/40 border-emerald-500/30 text-emerald-200',
    warning: 'bg-amber-950/40 border-amber-500/30 text-amber-200',
    error: 'bg-rose-950/40 border-rose-500/30 text-rose-200',
  };

  const Icon = icons[variant];

  return (
    <div className={`flex items-start gap-3 p-4 rounded-xl border backdrop-blur-md ${variants[variant]} ${className}`}>
      <Icon className="w-5 h-5 shrink-0 mt-0.5" />
      <div className="flex-1 text-xs leading-relaxed">
        {title && <h4 className="font-bold text-sm mb-1">{title}</h4>}
        {children}
      </div>
    </div>
  );
};
