export default defineNuxtRouteMiddleware((to, from) => {
  const token = useCookie('auth_token')

  // Pages publiques qui ne nécessitent pas d'auth
  const publicPages = ['/login']
  const isPublicPage = publicPages.includes(to.path)

  if (!token.value && !isPublicPage) {
    return navigateTo('/login')
  }

  if (token.value && isPublicPage) {
    // Si déjà loggé, redirection vers le dashboard par défaut (ou selon rôle)
    const role = useCookie('authRole')
    const dashboard = role.value ? `/${role.value}` : '/secretariat'
    return navigateTo(dashboard)
  }
})
