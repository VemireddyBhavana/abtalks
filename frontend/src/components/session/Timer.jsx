import React, { useState, useEffect } from 'react';
import { Clock } from 'lucide-react';

export const Timer = ({ initialSeconds = 300, onExpire }) => {
  const [seconds, setSeconds] = useState(initialSeconds);

  useEffect(() => {
    if (seconds <= 0) {
      if (onExpire) onExpire();
      return;
    }

    const timerId = setInterval(() => {
      setSeconds((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timerId);
  }, [seconds, onExpire]);

  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  const formatted = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

  const isLow = seconds < 60;

  return (
    <div
      className={`flex items-center gap-2 px-3 py-1.5 rounded-xl border backdrop-blur-md text-xs font-mono font-bold transition-all ${
        isLow
          ? 'bg-rose-950/60 text-rose-400 border-rose-500/40 animate-pulse'
          : 'bg-slate-800/60 text-slate-300 border-slate-700/40'
      }`}
    >
      <Clock className="w-3.5 h-3.5" />
      <span>{formatted}</span>
    </div>
  );
};
