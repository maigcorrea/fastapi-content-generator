'use client';
import { ReactNode } from 'react';
import { useAuthGuard } from '@/hooks/useAuthGuard';

interface ProtectRoutesProps {
  children: ReactNode;
  adminOnly?: boolean;
}

export default function ProtectRoutes({ children, adminOnly = false }: ProtectRoutesProps) {
  // Utilizamos el hook useAuthGuard para verificar la autorización
  // Si adminOnly es true, se verifica si el usuario es administrador
  // Si no, se verifica solo si el usuario está autenticado
  // El hook devuelve un objeto con authorized e isLoading
  // authorized indica si el usuario tiene acceso a la ruta
  // isLoading indica si aún se está verificando la autorización
  // Si isLoading es true, no renderizamos nada aún
  // Si authorized es false, tampoco renderizamos nada
  const { authorized, isLoading } = useAuthGuard(adminOnly);

  if (isLoading || !authorized) return null;

  return <>{children}</>;
}
