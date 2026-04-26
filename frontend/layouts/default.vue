<template>
  <div class="app-layout">
    <VitePwaManifest />
    
    <!-- Notification PWA Update -->
    <client-only>
      <div v-if="$pwa?.needRefresh" class="pwa-toast shadow-lg" role="alert">
        <div class="message">
          <span>✨ Nouvelle version disponible !</span>
        </div>
        <div class="actions">
          <button @click="$pwa.updateServiceWorker()" class="btn-refresh">Actualiser</button>
        </div>
      </div>
    </client-only>

    <!-- Overlay pour Mobile -->
    <div v-if="isSidebarOpen" class="sidebar-overlay" @click="closeSidebar"></div>

    <!-- Sidebar Premium -->
    <aside class="sidebar" :class="{ 'is-open': isSidebarOpen }">
      <div class="sidebar-brand">
        <div class="logo-box">
          <img src="/logo.png" alt="Bull ASUR Logo" class="sidebar-logo-img">
        </div>
        <div class="brand-text">
          <h1>Bull ASUR</h1>
          <p>Gestion Académique</p>
        </div>
        <!-- Bouton fermer sur mobile -->
        <button class="mobile-close" @click="closeSidebar">✕</button>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-section">
          <span class="nav-section-title">Menu Principal</span>
          <NuxtLink :to="`/${currentRole}`" class="nav-link" @click="closeSidebar">
            <span class="nav-icon-svg">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            </span>
            Dashboard
          </NuxtLink>
        </div>

        <div class="nav-section">
          <span class="nav-section-title">Gestion</span>
          <NuxtLink v-for="link in allowedLinks" :key="link.path" :to="link.path" class="nav-link" @click="closeSidebar">
            <span class="nav-icon-svg" v-html="link.iconSvg"></span>
            {{ link.label }}
          </NuxtLink>
        </div>
      </nav>

      <div class="sidebar-user">
        <div class="user-info">
          <div class="user-avatar monochrome-avatar">
            {{ currentRole.charAt(0).toUpperCase() }}
          </div>
          <div class="user-details">
            <span class="user-name">{{ userName || 'Utilisateur' }}</span>
            <span class="user-role">{{ currentRole.toUpperCase() }}</span>
          </div>
        </div>
        <button @click="logout" class="logout-btn monochrome-btn" title="Déconnexion">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
        </button>
      </div>
    </aside>
    
    <!-- Main Content Area -->
    <div class="main-wrapper">
      <header class="navbar">
        <div class="navbar-left">
          <!-- Bouton Menu Hamburger -->
          <button class="hamburger-btn" @click="toggleSidebar">
            <span>☰</span>
          </button>
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
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import NotificationSystem from '~/components/ui/NotificationSystem.vue'

const route = useRoute()
const isSidebarOpen = ref(false)
const currentRole = useCookie('authRole', { default: () => 'etudiant' })
const userName = useCookie('authName')

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const closeSidebar = () => {
  isSidebarOpen.value = false
}

// Fermer la sidebar lors du changement de route (mobile)
watch(() => route.path, () => {
  closeSidebar()
})

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

// Liens de navigation
const allLinks = [
  // Admin links
  { 
    path: '/admin/referentiels', 
    label: 'Référentiels', 
    roles: ['admin', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12.22 2h-.44a2 2 0 00-2 2v.18a2 2 0 01-1 1.73l-.43.25a2 2 0 01-2 0l-.15-.08a2 2 0 00-2.73.73l-.22.38a2 2 0 00.73 2.73l.15.1a2 2 0 011 1.72v.51a2 2 0 01-1 1.74l-.15.09a2 2 0 00-.73 2.73l.22.38a2 2 0 002.73.73l.15-.08a2 2 0 012 0l.43.25a2 2 0 011 1.73V20a2 2 0 002 2h.44a2 2 0 002-2v-.18a2 2 0 011-1.73l.43-.25a2 2 0 012 0l.15.08a2 2 0 002.73-.73l.22-.39a2 2 0 00-.73-2.73l-.15-.08a2 2 0 01-1-1.74v-.5a2 2 0 011-1.74l.15-.09a2 2 0 00.73-2.73l-.22-.38a2 2 0 00-2.73-.73l-.15.08a2 2 0 01-2 0l-.43-.25a2 2 0 01-1-1.73V4a2 2 0 00-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>'
  },
  { 
    path: '/admin/logs', 
    label: 'Audit Système', 
    roles: ['admin', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>'
  },
  
  // Secretariat links
  { 
    path: '/secretariat/etudiants', 
    label: 'Étudiants', 
    roles: ['admin', 'secretariat', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 00-3-3.87"></path><path d="M16 3.13a4 4 0 010 7.75"></path></svg>'
  },
  { 
    path: '/secretariat/enseignants', 
    label: 'Enseignants', 
    roles: ['admin', 'secretariat', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><polyline points="16 11 18 13 22 9"></polyline></svg>'
  },
  { 
    path: '/secretariat/absences', 
    label: 'Absences', 
    roles: ['admin', 'secretariat', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>'
  },
  { 
    path: '/secretariat/bulletins', 
    label: 'Bulletins', 
    roles: ['admin', 'secretariat', 'super_admin', 'etudiant', 'enseignant'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"></path></svg>'
  },
  { 
    path: '/secretariat/modification-notes', 
    label: 'Saisie Notes', 
    roles: ['admin', 'secretariat', 'super_admin', 'enseignant'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>'
  }
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

/* Sidebar Overlay */
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 100;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
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
  z-index: 110;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar-brand {
  padding: 2rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.mobile-close {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  margin-left: auto;
}

.logo-box {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 16px;
  padding: 10px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.sidebar-logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.brand-text {
  text-align: center;
}

.brand-text h1 {
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  letter-spacing: -0.5px;
  margin: 0;
}

.brand-text .tagline {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.5);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0;
}

.sidebar-nav {
  flex: 1;
  padding: 1.5rem 1rem;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 2rem;
}

.nav-section-title {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.3);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 1rem;
  padding-left: 1rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.85rem 1rem;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.2s;
  margin-bottom: 0.25rem;
}

.nav-icon-svg {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: currentColor;
}

.nav-link:hover, .nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-link.router-link-active {
  background: white;
  color: black;
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
  transition: margin 0.3s ease;
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

.navbar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.hamburger-btn {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-primary);
  cursor: pointer;
  padding: 0.5rem;
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

/* Mobile Responsive Styles */
@media (max-width: 1024px) {
  .sidebar { 
    transform: translateX(-100%); 
    width: 280px;
  }
  
  .sidebar.is-open {
    transform: translateX(0);
    box-shadow: 10px 0 30px rgba(0,0,0,0.3);
  }

  .main-wrapper { 
    margin-left: 0; 
  }

  .hamburger-btn {
    display: block;
  }

  .mobile-close {
    display: block;
  }

  .navbar {
    padding: 0 1rem;
  }

  .search-bar {
    display: none; /* Cache la recherche sur mobile pour plus d'espace */
  }

  .page-content {
    padding: 1rem;
  }
}
</style>
