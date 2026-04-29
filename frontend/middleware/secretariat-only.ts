export default defineNuxtRouteMiddleware((to, from) => {
  const role = useCookie('authRole')
  const allowedRoles = ['admin', 'super_admin', 'secretariat']
  
  if (!allowedRoles.includes(role.value)) {
    return navigateTo(`/${role.value || 'etudiant'}`)
  }
})
