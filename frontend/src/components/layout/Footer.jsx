import React from 'react';
import { Heart, Github } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="mt-auto border-t border-slate-800/60 py-6 px-8 text-slate-500 text-xs flex flex-col sm:flex-row items-center justify-between gap-4">
      <div className="flex items-center gap-1.5">
        <span>Built with</span>
        <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500" />
        <span>for ABTalks AI Interview Agent Hackathon</span>
      </div>

      <div className="flex items-center gap-6">
        <a
          href="https://github.com/VemireddyBhavana/abtalks"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 hover:text-slate-300 transition-colors"
        >
          <Github className="w-3.5 h-3.5" />
          <span>GitHub Repository</span>
        </a>
        <span>Vite + React 19 + FastAPI</span>
      </div>
    </footer>
  );
};
