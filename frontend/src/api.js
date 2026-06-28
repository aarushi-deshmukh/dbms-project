import axios from "axios"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/"
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear tokens on 401 Unauthorized
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
      localStorage.removeItem("user_type")
      
      // Redirect to signin if not already there
      if (!window.location.pathname.endsWith("/signin")) {
        window.location.href = "/signin"
      }
    }
    return Promise.reject(error)
  }
)

export default api