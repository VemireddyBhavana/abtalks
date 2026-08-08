import React from 'react';
import { NavLink } from 'react-router-dom';
import { Bot, Sparkles, Terminal } from 'lucide-react';
import { themeConfig } from '../../config/theme';
import { env } from '../../config/env';

export const Navbar = () => {
  return (
    <header className="sticky top-0 z-50 glass-card border-b border-gray-800 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Brand */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-emerald-400 flex items-center justify-center shadow-lg shadow-brand-500/20">
              <Bot className="w-6 h-6 text-dark-bg" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-lg tracking-tight text-white flex items-center gap-1.5">
                {env.appTitle}
                <Sparkles className="w-4 h-4 text-emerald-400 animate-pulse-slow" />
              </span>
              <span className="text-xs text-slate-400">ABTalks Hackathon Edition</span>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="flex items-center space-x-1 sm:space-x-2">
            {themeConfig.navigation.map((link) => (
              <NavLink
                key={link.path}
                to={link.path}
                className={({ isActive }) =>
                  `px-3 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                    isActive
                      ? 'bg-brand-500/10 text-emerald-400 border border-emerald-500/20'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                  }`
                }
              >
                {link.name}
              </NavLink>
            ))}
          </nav>

          {/* Status Indicator */}
          <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-900/80 border border-slate-800 text-xs">
            <Terminal className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-slate-400">Status:</span>
            <span className="flex items-center text-emerald-400 font-semibold gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              Foundation Ready
            </span>
          </div>

        </div>
      </div>
    </header>
  );
};

export default Navbar;
