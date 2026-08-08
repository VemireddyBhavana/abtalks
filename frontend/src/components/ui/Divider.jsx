import React from 'react';

export const Divider = ({ className = '' }) => {
  return <hr className={`border-t border-slate-800/80 my-4 ${className}`} />;
};
