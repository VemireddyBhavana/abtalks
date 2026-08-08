import { useThemeContext } from '../context/ThemeContext';

export const useTheme = () => {
  const { theme, setTheme } = useThemeContext();
  return {
    theme,
    setTheme,
    isDark: theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches),
  };
};
