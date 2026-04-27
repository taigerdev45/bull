export default defineNuxtRouteMiddleware((to, from) => {
  const token = useCookie('auth_token')

  // Pages publiques qui ne nécessitent pas d'auth
  const publicPages = ['/']
  const isPublicPage = publicPages.includes(to.path) || to.path.startsWith('/verify/')

  if (!token.value && !isPublicPage) {
    return navigateTo('/')
  }

  if (token.value && isPublicPage) {
    // Si déjà loggé, redirection vers le dashboard selon rôle
    const role = useCookie('authRole')
    const dashboard = role.value ? `/${role.value}` : '/etudiant'
    return navigateTo(dashboard)
  }
})
