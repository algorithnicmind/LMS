import { createContext, useContext, useEffect, useState, ReactNode } from 'react';

interface ReducedMotionContextValue {
  shouldReduceMotion: boolean;
}

const ReducedMotionContext = createContext<ReducedMotionContextValue>({
  shouldReduceMotion: false,
});

export function ReducedMotionProvider({ children }: { children: ReactNode }) {
  const [shouldReduceMotion, setShouldReduceMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setShouldReduceMotion(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => {
      setShouldReduceMotion(event.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return (
    <ReducedMotionContext.Provider value={{ shouldReduceMotion }}>
      {children}
    </ReducedMotionContext.Provider>
  );
}

export function useReducedMotion(): boolean {
  const { shouldReduceMotion } = useContext(ReducedMotionContext);
  return shouldReduceMotion;
}