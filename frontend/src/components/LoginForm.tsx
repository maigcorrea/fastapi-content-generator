"use client";

import { useState } from "react";

type LoginFormData = {
  email: string;
  password: string;
};

export default function LoginForm() {
  const [formData, setFormData] = useState<LoginFormData>({
    email: "",
    password: "",
  });
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const res = await fetch("http://localhost:8000/users/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Login failed");
      }

      const data = await res.json();
      localStorage.setItem("token", data.access_token); // Guardar el token en localStorage
      localStorage.setItem("isAdmin", String(data.is_admin)); // Guardar si es admin
      alert("Login exitoso. Token guardado en localStorage.");
      // Aquí podrías redirigir al usuario o actualizar el contexto de auth
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-80 mx-auto">
      <h2 className="text-xl font-bold">Iniciar Sesión</h2>

      <input
        type="email"
        name="email"
        placeholder="Correo"
        value={formData.email}
        onChange={handleChange}
        required
        className="border p-2 rounded"
      />
      <input
        type="password"
        name="password"
        placeholder="Contraseña"
        value={formData.password}
        onChange={handleChange}
        required
        className="border p-2 rounded"
      />

      <button type="submit" className="bg-blue-600 text-white p-2 rounded">
        Iniciar sesión
      </button>

      {error && <p className="text-red-500 text-sm">{error}</p>}
    </form>
  );
}
