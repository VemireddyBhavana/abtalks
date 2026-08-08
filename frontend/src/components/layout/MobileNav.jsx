import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { Menu, X, Home, LayoutDashboard, PlayCircle, History, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const MobileNav = () => {
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { to: '/', label: 'Home', icon: Home },
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/lobby', label: 'Lobby', icon: PlayCircle },
    { to: '/history', label: 'History', icon: History },
  ];

  return (
    <div className="lg:hidden glass-panel border-b border-slate-800/80 px-4 py-3 sticky top-0 z-40 flex items-center justify-between">
      <div className="flex items-center gap-2.5">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white">
          <Sparkles className="w-4 h-4" />
        </div>
        <span className="font-bold text-slate-100 text-sm gradient-text">ABTalks AI</span>
      </div>

      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-2 rounded-xl bg-slate-800/70 text-slate-300 hover:text-white transition-colors"
      >
        {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="absolute top-full left-0 w-full glass-panel border-b border-slate-800 p-4 flex flex-col gap-2 shadow-2xl"
          >
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  onClick={() => setIsOpen(false)}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                      isActive ? 'bg-blue-600/20 text-blue-400 font-semibold' : 'text-slate-400 hover:bg-slate-800/50'
                    }`
                  }
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
