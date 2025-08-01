import axios from 'axios'

// Creamos la instancia de axios
const API = axios.create({
  baseURL: 'http://localhost:8000', // Ajusta la URL de tu backend
})

// Interceptor de respuestas (para capturar errores 401)
API.interceptors.response.use(
  (response) => response, // Si todo va bien, sigue normal
  (error) => {
    if (error.response?.status === 401) {
      // Token inválido o caducado
      localStorage.removeItem('token') // Limpia el token
      window.location.href = '/login'  // Redirige al login
    }
    return Promise.reject(error)
  }
)

export default API
