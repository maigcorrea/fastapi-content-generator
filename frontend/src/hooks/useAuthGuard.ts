'use client';

import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AuthContext } from '@/context/AuthContext';

export function useAuthGuard(adminOnly = false) {
  const { token, isAdmin, isLoading } = useContext(AuthContext);
  const router = useRouter();
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    // Si todavía se está cargando el contexto, no hacemos nada
    if (isLoading) return;

    // Si no hay token -> login
    if (!token) {
      router.push('/login');
      return;
    }

    // Si la ruta requiere admin y el usuario no lo es -> acceso denegado
    if (adminOnly && !isAdmin) {
      router.push('/permission');
      return;
    }

    // Si todo OK -> autorizado
    setAuthorized(true);
  }, [token, isAdmin, isLoading, adminOnly, router]);

  return { authorized, isLoading };
}
