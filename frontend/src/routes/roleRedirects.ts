import type { Role } from '@/types/user';

const dashboardMap: Record<Role, string> = {
  STUDENT: '/dashboard',
  INSTRUCTOR: '/instructor',
  ADMIN: '/admin',
};

export function getDashboardPath(role: Role): string {
  return dashboardMap[role] || '/dashboard';
}

export function isPublicRoute(pathname: string): boolean {
  const publicRoutes = ['/', '/login', '/register', '/courses'];
  return publicRoutes.some((r) => pathname === r || pathname.startsWith('/courses/'));
}
