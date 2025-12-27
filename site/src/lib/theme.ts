export type Theme = 'light' | 'dark' | 'system';

const KEY = 'sua_theme';

function isBrowser(): boolean {
  return typeof window !== 'undefined' && typeof document !== 'undefined';
}

export function getTheme(): Theme {
  if (!isBrowser()) return 'system';
  const saved = localStorage.getItem(KEY) as Theme | null;
  return saved ?? 'system';
}

export function applyTheme(theme: Theme) {
  if (!isBrowser()) return;

  const root = document.documentElement;
  root.dataset.theme = theme;

  if (theme === 'system') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.resolvedTheme = prefersDark ? 'dark' : 'light';
  } else {
    root.dataset.resolvedTheme = theme;
  }
}

export function setTheme(theme: Theme) {
  if (!isBrowser()) return;
  localStorage.setItem(KEY, theme);
  applyTheme(theme);
}
