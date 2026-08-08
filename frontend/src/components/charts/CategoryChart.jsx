import React from 'react';
import { motion } from 'framer-motion';

export const CategoryChart = ({ categories = [] }) => {
  return (
    <div className="flex flex-col gap-3 w-full">
      {categories.map((cat, idx) => (
        <div key={idx} className="flex flex-col gap-1 text-xs">
          <div className="flex justify-between font-semibold">
            <span className="text-slate-300">{cat.category_name || cat.name}</span>
            <span className="text-blue-400 font-bold">{cat.score} / 100</span>
          </div>
          <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${Math.min(100, cat.score)}%` }}
              transition={{ duration: 0.6, delay: idx * 0.05 }}
              className="h-full bg-gradient-to-r from-blue-500 to-indigo-400 rounded-full"
            />
          </div>
        </div>
      ))}
    </div>
  );
};
