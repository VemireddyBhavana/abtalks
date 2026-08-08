import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, LayoutDashboard, PlayCircle, History, Sparkles, BookOpen } from 'lucide-react';

export const Sidebar = () => {
  const navItems = [
    { to: '/', label: 'Home', icon: Home },
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/lobby', label: 'Interview Lobby', icon: PlayCircle },
    { to: '/history', label: 'Interview History', icon: History },
  ];

  return (
    <aside className="hidden lg:flex flex-col w-64 glass-panel border-r border-slate-800/80 p-5 min-h-screen">
      <div className="flex items-center gap-3 mb-8 px-2">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-blue-500/30">
          <Sparkles className="w-5 h-5" />
        </div>
        <div>
          <h1 className="font-bold text-slate-100 text-base leading-tight gradient-text">ABTalks AI</h1>
          <p className="text-xs text-slate-400">Interview Agent</p>
        </div>
      </div>

      <nav className="flex flex-col gap-1.5 flex-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30 font-semibold shadow-inner'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="glass-panel p-4 rounded-xl border border-slate-700/30 mt-auto">
        <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 mb-1">
          <BookOpen className="w-3.5 h-3.5" />
          <span>Full Stack AI Engineering</span>
        </div>
        <p className="text-xs text-slate-400 leading-relaxed">
          Curriculum Days 1–5 • Real-time adaptive LLM questions & evaluation.
        </p>
      </div>
    </aside>
  );
};
