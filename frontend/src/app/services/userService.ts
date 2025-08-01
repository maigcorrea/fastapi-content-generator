import axios from 'axios'

const API_URL = 'http://localhost:8000/users'

export const registerUser = async (formData: {
  username: string
  email: string
  password: string
}) => {
  const response = await axios.post(`${API_URL}/register-pending`, formData) //Antes se mandaba a /users/ directamente (sin envío de email), ahora en este endpoint se incluye el encío de un correo de verificación
  return response.data
}

export const loginUser = async (credentials: { email: string; password: string }) => {
  const response = await axios.post(`${API_URL}/login`, credentials)
  return response.data
}


export const verifyUser = async (email: string, code: string) => {
  const response = await axios.post(`${API_URL}/verify`, { email, code })
  return response.data
}

export const resendVerificationCode = async (email: string) => {
  const response = await axios.post(`${API_URL}/resend-code`, { email })
  return response.data
}