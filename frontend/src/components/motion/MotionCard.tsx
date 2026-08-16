import { motion, HTMLMotionProps } from 'framer-motion';
import { useReducedMotion } from './ReducedMotionContext';

interface MotionCardProps extends Omit<HTMLMotionProps<'div'>, 'whileHover' | 'whileTap'> {
  children: React.ReactNode;
  className?: string;
  elevated?: boolean;
}

export function MotionCard({
  children,
  className = '',
  elevated = false,
  ...props
}: MotionCardProps) {
  const shouldReduceMotion = useReducedMotion();

  const baseClasses = 'rounded-xl bg-surface border border-border p-6 transition-shadow duration-200';
  const elevatedClasses = elevated ? 'shadow-lg' : 'shadow-md hover:shadow-xl';

  if (shouldReduceMotion) {
    return (
      <div className={`${baseClasses} ${elevatedClasses} ${className}`} {...props}>
        {children}
      </div>
    );
  }

  return (
    <motion.div
      className={`${baseClasses} ${elevatedClasses} ${className}`}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      whileTap={{ scale: 0.98, transition: { duration: 0.1 } }}
      {...props}
    >
      {children}
    </motion.div>
  );
}