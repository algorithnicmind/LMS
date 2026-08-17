import { ReducedMotionProvider } from '@/components/motion/ReducedMotionContext';
import type { ReactNode } from 'react';

export function MotionProvider({ children }: { children: ReactNode }) {
  return <ReducedMotionProvider>{children}</ReducedMotionProvider>;
}
