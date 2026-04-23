<template>
  <div class="app-layout">
    <!-- Sidebar Premium -->
    <aside class="sidebar">
      <div class="sidebar-brand">
        <div class="logo-box">
          <span class="logo-text">B</span>
        </div>
        <div class="brand-text">
          <h1>Bull ASUR</h1>
          <p>Gestion Académique</p>
        </div>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-section">
          <span class="nav-section-title">Menu Principal</span>
          <NuxtLink :to="`/${currentRole}`" class="nav-link">
            <span class="nav-icon">🏠</span>
            Dashboard
          </NuxtLink>
        </div>

        <div class="nav-section">
          <span class="nav-section-title">Gestion</span>
          <NuxtLink v-for="link in allowedLinks" :key="link.path" :to="link.path" class="nav-link">
            <span class="nav-icon">{{ link.icon }}</span>
            {{ link.label }}
          </NuxtLink>
        </div>
      </nav>

      <div class="sidebar-user">
        <div class="user-info">
          <div class="user-avatar" :style="{ backgroundColor: avatarColor }">
            {{ currentRole.charAt(0).toUpperCase() }}
          </div>
          <div class="user-details">
            <span class="user-name">{{ userName || 'Utilisateur' }}</span>
            <span class="user-role">{{ currentRole.toUpperCase() }}</span>
          </div>
        </div>
        <button @click="logout" class="logout-btn" title="Déconnexion">
          <span>🚪</span>
        </button>
      </div>
    </aside>
    
    <!-- Main Content Area -->
    <div class="main-wrapper">
      <header class="navbar">
        <div class="navbar-left">
          <h2 class="page-title">{{ currentRoute }}</h2>
        </div>
        <div class="navbar-right">
          <div class="search-bar">
            <span>🔍</span>
            <input type="text" placeholder="Rechercher..." />
          </div>
          <button class="notif-btn">
            <span>🔔</span>
            <span class="notif-badge"></span>
          </button>
        </div>
      </header>

      <main class="page-content">
        <slot />
      </main>
    </div>
    
    <NotificationSystem />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NotificationSystem from '~/components/ui/NotificationSystem.vue'

const route = useRoute()
const currentRole = useCookie('authRole', { default: () => 'etudiant' })
const userName = useCookie('authName') // On suppose qu'on a stocké le nom

const avatarColor = computed(() => {
  const colors = ['#2563eb', '#10b981', '#f59e0b', '#7c3aed', '#db2777']
  return colors[currentRole.value.length % colors.length]
})

const currentRoute = computed(() => {
  const path = route.path
  if (['/admin', '/secretariat', '/enseignant', '/etudiant'].includes(path)) return 'Tableau de Bord'
  const lastPart = path.split('/').pop()
  return lastPart.charAt(0).toUpperCase() + lastPart.slice(1)
})

const allLinks = [
  { path: '/etudiants', label: 'Étudiants', icon: '🎓', roles: ['admin', 'secretariat'] },
  { path: '/saisie', label: 'Saisie Notes', icon: '📝', roles: ['admin', 'secretariat', 'enseignant'] },
  { path: '/referentiels', label: 'Référentiels', icon: '📚', roles: ['admin'] },
  { path: '/deliberations', label: 'Délibérations', icon: '⚖️', roles: ['admin', 'secretariat'] },
  { path: '/bulletins', label: 'Bulletins', icon: '📄', roles: ['admin', 'secretariat', 'etudiant', 'enseignant'] },
  { path: '/personnel', label: 'Personnel', icon: '👥', roles: ['admin', 'super_admin'] },
  { path: '/profil', label: 'Profil', icon: '👤', roles: ['admin', 'secretariat', 'enseignant', 'etudiant'] }
]

const allowedLinks = computed(() => {
  return allLinks.filter(link => link.roles.includes(currentRole.value))
})

const logout = () => {
  const token = useCookie('auth_token')
  const role = useCookie('authRole')
  const id = useCookie('authId')
  token.value = null
  role.value = null
  id.value = null
  navigateTo('/')
}
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: var(--sidebar-width);
  background-color: var(--bg-sidebar);
  color: white;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0; left: 0; bottom: 0;
  z-index: 20;
}

.sidebar-brand {
  padding: 2rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-box {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 1.25rem;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.brand-text h1 {
  font-size: 1.15rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.5px;
}

.brand-text p {
  font-size: 0.75rem;
  opacity: 0.5;
  margin: 0;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 2rem;
}

.nav-section-title {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  color: rgba(255,255,255,0.3);
  font-weight: 700;
  padding-left: 1rem;
  margin-bottom: 0.75rem;
  letter-spacing: 1px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.8rem 1rem;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: all 0.2s;
  font-size: 0.95rem;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.nav-link:hover {
  background: rgba(255,255,255,0.05);
  color: white;
}

.router-link-active {
  background: rgba(37, 99, 235, 0.15) !important;
  color: #3b82f6 !important;
  font-weight: 600;
}

/* Sidebar User */
.sidebar-user {
  padding: 1.25rem;
  background: rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  border: 2px solid rgba(255,255,255,0.1);
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 0.7rem;
  opacity: 0.5;
}

.logout-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.logout-btn:hover {
  opacity: 1;
}

/* Main Wrapper */
.main-wrapper {
  margin-left: var(--sidebar-width);
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-main);
}

.navbar {
  height: var(--navbar-height);
  background: var(--bg-glass);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.page-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.search-bar {
  background: white;
  border: 1px solid var(--border-light);
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 240px;
}

.search-bar input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 0.85rem;
}

.notif-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.notif-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 8px;
  height: 8px;
  background: #ef4444;
  border: 2px solid white;
  border-radius: 50%;
}

.page-content {
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

@media (max-width: 1024px) {
  .sidebar { transform: translateX(-100%); }
  .main-wrapper { margin-left: 0; }
}
</style>
