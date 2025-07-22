'use client'

import { useState } from 'react'
import axios from 'axios'
import { registerUser } from '@/app/services/userService'

interface RegisterFormData {
  username: string
  email: string
  password: string
}

export default function RegisterForm() {
  const [formData, setFormData] = useState<RegisterFormData>({
    username: '',
    email: '',
    password: '',
  })

  // Estado para manejar mensajes de éxito o error
  const [message, setMessage] = useState<string | null>(null)

  // Manejo de cambios en los campos del formulario
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  // Manejo de envío del formulario
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const res = await registerUser(formData)

      if (!res.error) {
        setMessage('¡Usuario registrado con éxito!')
        setFormData({ username: '', email: '', password: '' }) // Limpieza del formulario
      }
    } catch (error: any) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        setMessage(`Error: ${error.response.data.detail}`)
      } else {
        setMessage('Error al registrar usuario')
      }
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Registro</h2>

      <input
        type="text"
        name="username"
        placeholder="Nombre de usuario"
        value={formData.username}
        onChange={handleChange}
        className="w-full border p-2 rounded"
        required
      />

      <input
        type="email"
        name="email"
        placeholder="Correo electrónico"
        value={formData.email}
        onChange={handleChange}
        className="w-full border p-2 rounded"
        required
      />

      <input
        type="password"
        name="password"
        placeholder="Contraseña"
        value={formData.password}
        onChange={handleChange}
        className="w-full border p-2 rounded"
        required
      />

      <button
        type="submit"
        className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
      >
        Registrarse
      </button>

      {message && <p className="text-center mt-4">{message}</p>}
    </form>
  )
}
