'use client';
import { ReactNode } from 'react';
import { useAuthGuard } from '@/hooks/useAuthGuard';

interface ProtectRoutesProps {
  children: ReactNode;
  adminOnly?: boolean;
}

export default function ProtectRoutes({ children, adminOnly = false }: ProtectRoutesProps) {
  const { authorized, isLoading } = useAuthGuard(adminOnly);

  if (isLoading || !authorized) return null;

  return <>{children}</>;
}
