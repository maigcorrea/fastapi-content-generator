'use client';
import { createContext, useState, useEffect, useMemo, Dispatch, SetStateAction, ReactNode } from 'react';

// Definimos el tipo del contexto de autenticación, se define la forma de un objeto: que propiedades tiene y de qué tipo son
interface AuthContextType {
  isAdmin: boolean | null;
  setIsAdmin: Dispatch<SetStateAction<boolean | null>>;
  token: string;
  setToken: Dispatch<SetStateAction<string>>;
  logout: () => void;
  isLoading: boolean;
}

// Creamos el contexto con sus valores definidos y tipados según el tipo AuthContextType
// El valor por defecto es un objeto con las propiedades inicializadas, pero no se usa directamente
export const AuthContext = createContext<AuthContextType>({
  isAdmin: null,
  setIsAdmin: () => {},
  token: '',
  setToken: () => {},
  logout: () => {},
  isLoading: true,
});

// Provider para envolver la app
export const AuthProvider = ({ children } : { children: ReactNode }) => { //tipar el prop children para decirle a TypeScript que puede ser cualquier cosa que React permita renderizar (texto, elementos, arrays, fragmentos, etc.)
  // const [isAdmin, setIsAdmin] = useState<boolean|null>(null);
  // const [token, setToken] = useState('');
  // const [isLoading, setIsLoading] = useState(true);

  //VERSIÓN OPTIMIZADA: Inicializamos directamente desde localStorage
  const [isAdmin, setIsAdmin] = useState<boolean | null>(() => {
    if (typeof window !== "undefined") {
      const storedAdmin = localStorage.getItem("is_admin");
      return storedAdmin ? storedAdmin === "true" : null;
    }
    return null;
  });


  const [token, setToken] = useState<string>(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("token") || "";
    }
    return "";
  });

  // Al cargar los valores desde localStorage ya no necesitamos un useEffect para setearlos
  const [isLoading, setIsLoading] = useState(false);


  const logout = () => {
    localStorage.clear();
    setIsAdmin(null);
    setToken('');
  };

  // Al cargar los valores desde localStorage ya no necesitamos un useEffect para setearlos
  // useEffect(() => { // VERSIÓN OPTIMIZADA, POR ESO ESTO NO HACE FALTA
  //   const storedToken = localStorage.getItem('token');
  //   const storedAdmin = localStorage.getItem('is_admin');

  //   if (storedToken) setToken(storedToken);
  //   if (storedAdmin) setIsAdmin(storedAdmin === 'true'); // <-- conversión de string a bool, si storedAdmin es "true", isAdmin se guardará como true; si es "false", se guardará como false.

  //   setIsLoading(false); // Ya se han cargado los datos
  // }, []);

  const contextValue = useMemo(() => ({
    isAdmin,
    setIsAdmin,
    token,
    setToken,
    logout,
    isLoading,
  }), [isAdmin, token, isLoading]);

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};
