/**
 * Global design tokens and theme configuration
 */
export const themeConfig = {
  colors: {
    primary: {
      light: '#ccfbf1',
      main: '#14b8a6',
      dark: '#0f766e',
    },
    background: {
      default: '#0B0F17',
      surface: '#111827',
      card: '#1F2937',
    },
    accent: {
      emerald: '#34d399',
      teal: '#2dd4bf',
      cyan: '#22d3ee',
    },
  },
  navigation: [
    { name: 'Home', path: '/' },
    { name: 'Interview Session', path: '/interview' },
    { name: 'Evaluation Result', path: '/result' },
  ],
};

export default themeConfig;
