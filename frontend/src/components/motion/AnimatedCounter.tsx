import { useMotionValue, useSpring, motion } from 'framer-motion';
import { useEffect } from 'react';
import { useReducedMotion } from './ReducedMotionContext';

interface AnimatedCounterProps {
  value: number;
  duration?: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
  className?: string;
}

export function AnimatedCounter({
  value,
  duration = 1.5,
  decimals = 0,
  prefix = '',
  suffix = '',
  className,
}: AnimatedCounterProps) {
  const shouldReduceMotion = useReducedMotion();
  const count = useMotionValue(0);
  const displayValue = useSpring(count, { stiffness: 100, damping: 20 });

  useEffect(() => {
    if (shouldReduceMotion) {
      count.set(value);
    } else {
      count.set(value);
    }
  }, [value, shouldReduceMotion, count]);

  return (
    <motion.span className={className}>
      {prefix}
      <motion.span
        style={{ x: displayValue }}
      >
        {displayValue.get().toFixed(decimals)}
      </motion.span>
      {suffix}
    </motion.span>
  );
}