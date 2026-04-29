export default defineNuxtRouteMiddleware((to, from) => {
  const role = useCookie('authRole')
  
  if (role.value !== 'admin' && role.value !== 'super_admin') {
    return navigateTo(`/${role.value || 'etudiant'}`)
  }
})
