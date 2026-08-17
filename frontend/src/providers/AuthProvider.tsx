import { useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';
import type { ReactNode } from 'react';

export function AuthProvider({ children }: { children: ReactNode }) {
  const fetchUser = useAuthStore((s) => s.fetchUser);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  return <>{children}</>;
}
