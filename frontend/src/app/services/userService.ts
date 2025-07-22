import axios from 'axios'

const API_URL = 'http://localhost:8000/users'

export const registerUser = async (formData: {
  username: string
  email: string
  password: string
}) => {
  const response = await axios.post(API_URL, formData)
  return response.data
}
