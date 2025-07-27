'use client';

import { ReactNode } from 'react';
import { useAuthGuard } from '@/hooks/useAuthGuard';
import Navbar from '@/components/NavBar';

export default function AdminLayout({ children }: { children: ReactNode }) {
  const { authorized, isLoading } = useAuthGuard(true); // true = solo admins (Es como decir adminOnly = true)

  if (isLoading || !authorized) return null;

  return <><Navbar />{children}</>;
}
