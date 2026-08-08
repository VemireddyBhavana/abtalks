import React from 'react';

export const Button = ({
  children,
  onClick,
  variant = 'primary',
  disabled = false,
  className = '',
  type = 'button',
  ...props
}) => {
  const baseStyle =
    'px-5 py-2.5 rounded-xl font-semibold text-sm transition-all flex items-center justify-center gap-2 focus:outline-none';

  const variants = {
    primary:
      'bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 text-slate-950 shadow-lg shadow-emerald-500/20 active:scale-[0.98]',
    secondary:
      'glass-card hover:bg-slate-800 text-slate-200 border border-slate-700 active:scale-[0.98]',
    disabled:
      'bg-slate-800 text-slate-500 border border-slate-700/50 cursor-not-allowed opacity-70',
  };

  const selectedVariant = disabled ? variants.disabled : variants[variant] || variants.primary;

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyle} ${selectedVariant} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
