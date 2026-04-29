export default defineNuxtRouteMiddleware((to, from) => {
  const token = useCookie('auth_token')
  const role = useCookie('authRole')

  // Pages publiques
  const publicPages = ['/']
  const isPublicPage = publicPages.includes(to.path) || to.path.startsWith('/verify/')

  // 1. Si pas de token et pas publique -> login
  if (!token.value && !isPublicPage) {
    return navigateTo('/')
  }

  // 2. Si token et publique -> dashboard
  if (token.value && isPublicPage) {
    const dashboard = role.value ? `/${role.value}` : '/etudiant'
    return navigateTo(dashboard)
  }

  // 3. Vérification des routes Admin/Secrétariat via le chemin
  if (token.value) {
    const userRole = (role.value || '').toLowerCase()
    
    // Protection spécifique des routes /admin/*
    if (to.path.startsWith('/admin') && userRole !== 'admin' && userRole !== 'super_admin') {
      return navigateTo(`/${userRole || 'etudiant'}`)
    }
    
    // Protection des routes /referentiels (Secretariat + Admin)
    const restrictedToSecretariat = ['/referentiels', '/personnel', '/enseignant']
    const isRestricted = restrictedToSecretariat.some(path => to.path.startsWith(path))
    if (isRestricted && !['admin', 'super_admin', 'secretariat'].includes(userRole)) {
      return navigateTo(`/${userRole || 'etudiant'}`)
    }
  }
})
