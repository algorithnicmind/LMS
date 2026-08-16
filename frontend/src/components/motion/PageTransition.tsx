import { AnimatePresence, motion } from 'framer-motion';
import { Outlet } from 'react-router-dom';
import { useReducedMotion } from './ReducedMotionContext';

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  enter: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

const transition = { duration: 0.3, ease: 'easeInOut' };

export function PageTransition() {
  const shouldReduceMotion = useReducedMotion();

  if (shouldReduceMotion) {
    return <Outlet />;
  }

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={window.location.pathname}
        initial="initial"
        animate="enter"
        exit="exit"
        variants={pageVariants}
        transition={transition}
      >
        <Outlet />
      </motion.div>
    </AnimatePresence>
  );
}