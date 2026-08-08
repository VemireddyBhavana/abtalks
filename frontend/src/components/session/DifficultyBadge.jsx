import React from 'react';
import { Badge } from '../ui/Badge';
import { ShieldCheck, Zap, Flame } from 'lucide-react';

export const DifficultyBadge = ({ difficulty = 'Intermediate' }) => {
  const configs = {
    Fundamental: { variant: 'emerald', icon: ShieldCheck, label: 'Fundamental' },
    Intermediate: { variant: 'amber', icon: Zap, label: 'Intermediate' },
    Advanced: { variant: 'rose', icon: Flame, label: 'Advanced' },
  };

  const cfg = configs[difficulty] || configs.Intermediate;
  const Icon = cfg.icon;

  return (
    <Badge variant={cfg.variant} size="md" className="gap-1.5 shadow-sm">
      <Icon className="w-3.5 h-3.5" />
      <span>{cfg.label}</span>
    </Badge>
  );
};
