import { motion, HTMLMotionProps } from 'framer-motion';
import { useInView } from 'framer-motion';
import { useRef } from 'react';
import { useReducedMotion } from './ReducedMotionContext';

interface RevealOnScrollProps extends Omit<HTMLMotionProps<'div'>, 'initial' | 'whileInView' | 'viewport'> {
  children: React.ReactNode;
  variant?: 'fade' | 'slide-up' | 'slide-left' | 'slide-right';
  delay?: number;
  duration?: number;
  once?: boolean;
}

const variants = {
  fade: {
    initial: { opacity: 0 },
    visible: { opacity: 1 },
  },
  'slide-up': {
    initial: { opacity: 0, y: 40 },
    visible: { opacity: 1, y: 0 },
  },
  'slide-left': {
    initial: { opacity: 0, x: -40 },
    visible: { opacity: 1, x: 0 },
  },
  'slide-right': {
    initial: { opacity: 0, x: 40 },
    visible: { opacity: 1, x: 0 },
  },
};

export function RevealOnScroll({
  children,
  variant = 'slide-up',
  delay = 0,
  duration = 0.6,
  once = true,
  className,
  ...props
}: RevealOnScrollProps) {
  const shouldReduceMotion = useReducedMotion();
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once, margin: '-100px' });

  if (shouldReduceMotion) {
    return <div ref={ref} className={className} {...props}>{children}</div>;
  }

  return (
    <motion.div
      ref={ref}
      initial={variants[variant].initial}
      animate={isInView ? variants[variant].visible : variants[variant].initial}
      transition={{ duration, delay, ease: 'easeOut' }}
      className={className}
      {...props}
    >
      {children}
    </motion.div>
  );
}