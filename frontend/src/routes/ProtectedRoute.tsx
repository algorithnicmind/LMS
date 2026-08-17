import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { getDashboardPath } from '@/routes/roleRedirects';
import { Skeleton } from '@/components/motion/Skeleton';
import type { Role } from '@/types/user';
import type { ReactNode } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
  role?: Role;
}

export function ProtectedRoute({ children, role }: ProtectedRouteProps) {
  const user = useAuthStore((s) => s.user);
  const isLoading = useAuthStore((s) => s.isLoading);

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="w-64 space-y-4">
          <Skeleton className="h-8 w-full" />
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-4 w-1/2" />
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (role && user.role !== role) {
    return <Navigate to={getDashboardPath(user.role)} replace />;
  }

  return <>{children}</>;
}
