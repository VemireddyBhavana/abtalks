import React from 'react';
import { Badge } from '../ui/Badge';
import { BookOpen } from 'lucide-react';

export const TopicBadge = ({ title, dayNumber }) => {
  return (
    <Badge variant="blue" size="md" className="gap-1.5 shadow-sm">
      <BookOpen className="w-3.5 h-3.5" />
      <span>Day {dayNumber} • {title}</span>
    </Badge>
  );
};
