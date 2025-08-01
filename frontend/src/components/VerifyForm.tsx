'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { verifyUser, resendVerificationCode } from '@/app/services/userService'
import { useSearchParams } from 'next/navigation'
import axios from 'axios'

export default function VerifyForm() {

  const [code, setCode] = useState('')
  const [message, setMessage] = useState<string | null>(null)
  const [timeLeft, setTimeLeft] = useState(300) // 5 min = 300s
  const [cooldown, setCooldown] = useState(0) // tiempo para reenviar
  const [loading, setLoading] = useState(false); // loading al pulsar botón "Verificar" (Mientras se comprueba el código bloquear botón)
  const router = useRouter()

  // Obtenemos el email del localStorage al montar el componente
  const [email, setEmail] = useState('')
  useEffect(() => {
    const storedEmail = localStorage.getItem('pendingEmail')
    if (storedEmail) {
      setEmail(storedEmail)
    } else {
      // Si no hay email en localStorage, redirigimos al registro
      router.push('/register')
    }
  }, [router])


  // Cuenta atrás del tiempo de caducidad del código
  useEffect(() => {
    if (timeLeft <= 0) return
    const timer = setInterval(() => setTimeLeft((t) => t - 1), 1000)
    return () => clearInterval(timer)
  }, [timeLeft])


  // Cuenta atrás para el cooldown del botón de reenvío
  useEffect(() => {
    if (cooldown <= 0) return
    const timer = setInterval(() => setCooldown((t) => t - 1), 1000)
    return () => clearInterval(timer)
  }, [cooldown])


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      await verifyUser(email, code)
      setMessage('✅ Cuenta verificada con éxito')
      localStorage.removeItem("pendingEmail") //Eliminamos el email ya que el usuario ha completado el proceso
      setTimeout(() => router.push('/login'), 2000)
    } catch (error: any) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        setMessage(`❌ Error: ${error.response.data.detail}`)
      } else {
        setMessage('❌ Error al verificar')
      }
    }finally{
      setLoading(false);
    }
  }

  const handleResend = async () => {
    try {
      await resendVerificationCode(email)
      setMessage('📧 Nuevo código enviado')
      setTimeLeft(300) // reinicia el contador
      setCooldown(20)  // 20 segundos de cooldown para el botón (desactivación durante 20seg)
    } catch (error) {
      setMessage('❌ Error al reenviar el código')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        placeholder="Código de verificación"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        className="w-full border p-2 rounded"
        required
      />

      <div className="flex justify-between items-center">
        <button
          type="submit"
          disabled={loading}
          className="bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700"
        >
          {loading && (
            // Spin de carga
            <svg 
              className="animate-spin h-4 w-4 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
              />
            </svg>
          )}
          Verificar
        </button>

        <button
          type="button"
          onClick={handleResend}
          disabled={cooldown > 0}
          className={`py-2 px-4 rounded ${
            cooldown > 0
              ? 'bg-gray-400 text-white cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          {cooldown > 0 ? `Reenviar (${cooldown})` : 'Reenviar código'}
        </button>
      </div>

      <p className="text-center text-sm text-gray-600">
        Tiempo restante: {Math.floor(timeLeft / 60)}:
        {String(timeLeft % 60).padStart(2, '0')}
      </p>

      {message && <p className="text-center mt-4">{message}</p>}
    </form>
  )
}
