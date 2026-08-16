import { motion } from 'framer-motion';
import { useReducedMotion } from './ReducedMotionContext';

interface SkeletonProps {
  className?: string;
  variant?: 'text' | 'circular' | 'rectangular';
  width?: string | number;
  height?: string | number;
  lines?: number;
}

const shimmerKeyframes = [
  { backgroundPosition: '-200% 0' },
  { backgroundPosition: '200% 0' },
];

export function Skeleton({
  className = '',
  variant = 'text',
  width = '100%',
  height,
  lines = 1,
}: SkeletonProps) {
  const shouldReduceMotion = useReducedMotion();

  const baseStyle: React.CSSProperties = {
    width,
    height,
    background: 'linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%)',
    backgroundSize: '200% 100%',
    borderRadius: variant === 'circular' ? '9999px' : variant === 'rectangular' ? '0.5rem' : '0.25rem',
  };

  if (variant === 'text' && lines > 1) {
    return (
      <div className={className} style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {Array.from({ length: lines }).map((_, i) => (
          <Skeleton
            key={i}
            variant="text"
            width={i === lines - 1 ? '60%' : '100%'}
            height={16}
          />
        ))}
      </div>
    );
  }

  if (shouldReduceMotion) {
    return <div className={className} style={baseStyle} aria-hidden="true" />;
  }

  return (
    <motion.div
      className={className}
      style={baseStyle}
      animate={{ backgroundPosition: ['-200% 0', '200% 0'] }}
      transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
      aria-hidden="true"
    />
  );
}