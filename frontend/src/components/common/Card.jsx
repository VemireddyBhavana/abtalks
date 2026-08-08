import React from 'react';

export const Card = ({ children, className = '', hover = true }) => {
  return (
    <div
      className={`glass-card p-6 rounded-2xl border border-slate-800 ${
        hover ? 'glass-card-hover' : ''
      } ${className}`}
    >
      {children}
    </div>
  );
};

export default Card;
