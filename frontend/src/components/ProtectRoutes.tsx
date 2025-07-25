'use client';
import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';

interface ProtectRoutesProps {
  children: React.ReactNode;
  adminOnly?: boolean; // Si es true, solo deja entrar admins
}

const ProtectRoutes: React.FC<ProtectRoutesProps> = ({ children, adminOnly = false }) => {
  const router = useRouter();
  const { token, isAdmin, isLoading } = useContext(AuthContext);
  const [isAuthorized, setIsAuthorized] = useState(false);

  useEffect(() => {
    if (isLoading) return; // esperamos a que el contexto cargue

    // Si no hay token -> login
    if (!token) {
      router.push('/login');
      return;
    }

    // Si la ruta requiere admin y el usuario no lo es -> permission denied
    if (adminOnly && !isAdmin) {
      router.push('/permission'); // página de acceso denegado
      return;
    }

    // Si todo bien -> autorizado
    setIsAuthorized(true);
  }, [router, token, isAdmin, adminOnly, isLoading]);

  // Mientras carga el contexto o decide si está autorizado -> no renderiza nada
  if (isLoading || !isAuthorized) return null;

  return <>{children}</>;
};

export default ProtectRoutes;
