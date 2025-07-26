"use client";

import { useContext } from "react";
import { AuthContext } from "@/context/AuthContext";
import { useRouter } from 'next/navigation';
import { routerServerGlobal } from "next/dist/server/lib/router-utils/router-server-context";
import { Router } from "next/router";

export default function Navbar() {
  const { token, isAdmin, logout } = useContext(AuthContext);
  const router = useRouter();

  return (
    <nav className="flex justify-between items-center bg-gray-800 text-white p-4">
      <h1 className="text-lg font-bold">Mi App</h1>

      {token ? (
        <div className="flex gap-4 items-center">
          <span>{isAdmin ? "👑 Admin" : "🙋 Usuario"}</span>
          <button
            onClick={logout}
            className="bg-red-600 px-3 py-1 rounded hover:bg-red-700"
          >
            Cerrar sesión
          </button>
        </div>
      ) : (
        <div className="flex gap-4 items-center">
            <span className="text-sm">No has iniciado sesión</span>
            <button
            onClick={() => {router.push('/login')}}
            className="bg-red-600 px-3 py-1 rounded hover:bg-red-700"
          >
            Login
          </button>

          <button
            onClick={() => {router.push('/register')}}
            className="bg-red-600 px-3 py-1 rounded hover:bg-red-700"
          >
            Registrarse
          </button>
        </div>
        
      )}
    </nav>
  );
}
