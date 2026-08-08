import React from 'react';

export const Footer = () => {
  return (
    <footer className="border-t border-slate-800/80 bg-dark-surface/50 py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-400">
        <div>
          <span className="font-semibold text-slate-300">AI Interview Agent</span> &copy; 2026 ABTalks Hackathon. All rights reserved.
        </div>
        <div className="flex items-center space-x-4">
          <span className="hover:text-slate-200 transition-colors">React 19</span>
          <span>•</span>
          <span className="hover:text-slate-200 transition-colors">Vite</span>
          <span>•</span>
          <span className="hover:text-slate-200 transition-colors">Tailwind CSS</span>
          <span>•</span>
          <span className="hover:text-slate-200 transition-colors">FastAPI</span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
