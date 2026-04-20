export const useApi = () => {
  const authToken = useCookie('authToken')
  const baseUrl = 'https://api.lp-asur.ga'

  /**
   * Wrapper around $fetch to automatically include the Firebase ID Token
   * and handle common errors.
   */
  const apiFetch = async (url: string, options: any = {}) => {
    try {
      return await $fetch(url, {
        baseURL: baseUrl,
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
          'Authorization': authToken.value ? `Bearer ${authToken.value}` : undefined
        },
        onResponseError({ response }: { response: any }) {
          if (response.status === 403) {
            console.error("Accès refusé : Vérifiez vos droits d'accès.")
            // Logic for 403 could go here
          }
          if (response.status === 401) {
             console.error("Session expirée ou non authentifiée.")
             // Redirect to login or refresh token logic
          }
        }
      })
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  return {
    apiFetch
  }
}
