export const APP_NAME = 'AI Interview Agent';
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const NAV_LINKS = [
  { name: 'Home', path: '/' },
  { name: 'Interview Session', path: '/interview' },
  { name: 'Evaluation Result', path: '/result' },
];

export const STATUS_CODES = {
  RUNNING: 'running',
  IDLE: 'idle',
  COMPLETED: 'completed',
};
