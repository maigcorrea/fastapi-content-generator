'use client';

import { ReactNode } from 'react';
import { useAuthGuard } from '@/hooks/useAuthGuard';
import Navbar from '@/components/NavBar';
import { AuthProvider } from '@/context/AuthContext';

export default function PrivateLayout({ children }: { children: ReactNode }) {
  const { authorized, isLoading } = useAuthGuard(false); // false = no solo admins (Es como decir adminOnly = false)

  if (isLoading || !authorized) return null;

  return <><AuthProvider><Navbar />{children}</AuthProvider></>;
}
