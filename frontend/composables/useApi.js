export const useApi = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase || 'http://localhost:8000/api'
  
  // Récupération du token depuis le storage (cookie ou localStorage)
  const token = useCookie('auth_token')

  const fetchApi = async (url, options = {}) => {
    // Nettoyage de l'URL pour éviter les doubles slashes
    const cleanUrl = url.startsWith('/') ? url : `/${url}`
    const fullUrl = `${apiBase}${cleanUrl}`

    const defaultOptions = {
      headers: {
        'Accept': 'application/json',
        'Authorization': token.value ? `Bearer ${token.value}` : '',
        ...options.headers
      }
    }

    try {
      const response = await $fetch(fullUrl, {
        ...defaultOptions,
        ...options
      })
      return response
    } catch (error) {
      console.error(`API Error [${fullUrl}]:`, error)
      // Gestion globale des erreurs (ex: redirection si 401)
      if (error.response?.status === 401) {
        token.value = null
        navigateTo('/login')
      }
      throw error
    }
  }

  return {
    fetchApi,
    apiBase
  }
}
