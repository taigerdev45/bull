<template>
  <div class="app-layout">
    <VitePwaManifest />
    
    <!-- PWA Toast -->
    <client-only>
      <div v-if="$pwa?.needRefresh" class="pwa-toast-premium premium-card darker" role="alert">
        <div class="message">
          <span class="pulsar-white"></span>
          <span>Version optimisée disponible</span>
        </div>
        <button @click="$pwa.updateServiceWorker()" class="btn-pwa">Actualiser →</button>
      </div>
    </client-only>

    <!-- Sidebar Premium Monochrome -->
    <aside class="sidebar-p" :class="{ 'is-open': isSidebarOpen }">
      <div class="sidebar-header">
        <div class="logo-box">
          <img src="/logo.png" alt="Bull Logo" class="logo-img">
        </div>
        <div class="brand-info">
          <h2>Bull ASUR</h2>
          <span class="tagline">Enterprise Edition</span>
        </div>
      </div>

      <!-- Navigation Sections -->
      <nav class="sidebar-nav-p">
        <div class="nav-section-p" v-for="section in navSections" :key="section.title">
          <span class="nav-group-title">{{ section.title }}</span>
          <div class="nav-links-list">
            <NuxtLink 
              v-for="link in section.links" 
              :key="link.path" 
              :to="link.path" 
              class="nav-link-p"
              @click="isSidebarOpen = false"
            >
              <span class="icon-p" v-html="link.iconSvg"></span>
              <span class="label-p">{{ link.label }}</span>
            </NuxtLink>
          </div>
        </div>
      </nav>

      <!-- User Footer -->
      <div class="sidebar-footer-p">
        <div class="avatar-p">
          {{ userName?.charAt(0).toUpperCase() || 'U' }}
        </div>
        <div class="user-meta">
          <span class="name-p">{{ userName }}</span>
          <span class="role-p">{{ currentRole }}</span>
        </div>
        <button class="btn-logout-p" @click="logout" title="Déconnexion">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="20"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/></svg>
        </button>
      </div>
    </aside>

    <!-- Overlay Mobile -->
    <div v-if="isSidebarOpen" class="sidebar-overlay-p" @click="isSidebarOpen = false"></div>

    <div class="main-body-p">
      <header class="navbar-p">
        <div class="nav-left-p">
          <button class="menu-trigger-p" @click="isSidebarOpen = true">☰</button>
          <div class="breadcrumb-p">
            <span class="root">Bulletin</span>
            <span class="sep">/</span>
            <span class="current">{{ currentRoute }}</span>
          </div>
        </div>
        <div class="nav-right-p">
          <div class="search-premium">
            <span class="s-icon">🔍</span>
            <input type="text" placeholder="Recherche globale...">
          </div>
          <NotificationCenter />
        </div>
      </header>

      <main class="content-p">
        <slot />
      </main>
    </div>
    
    <NotificationSystem />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import NotificationSystem from '~/components/ui/NotificationSystem.vue'
import NotificationCenter from '~/components/ui/NotificationCenter.vue'

const route = useRoute()
const isSidebarOpen = ref(false)
const currentRole = useCookie('authRole', { default: () => 'etudiant' })
const userName = useCookie('authName')

const currentRoute = computed(() => {
  const path = route.path
  if (path === '/') return 'Authentification'
  const parts = path.split('/')
  const last = parts[parts.length - 1]
  return (last || '').charAt(0).toUpperCase() + (last || '').slice(1).replace(/-/g, ' ')
})

const allLinks = [
  { 
    path: '/secretariat/edition-bulletins', 
    label: 'Architecture Académique', 
    roles: ['admin', 'super_admin', 'secretariat'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>'
  },
  { 
    path: '/secretariat/etudiants', 
    label: 'Registre Étudiants', 
    roles: ['admin', 'secretariat', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 00-3-3.87"></path><path d="M16 3.13a4 4 0 010 7.75"></path></svg>'
  },
  { 
    path: '/secretariat/enseignants', 
    label: 'Intervenants', 
    roles: ['admin', 'secretariat', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><polyline points="16 11 18 13 22 9"></polyline></svg>'
  },
  { 
    path: '/secretariat/absences', 
    label: 'Journal Absences', 
    roles: ['admin', 'secretariat', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>'
  },
  { 
    path: '/secretariat/bulletins', 
    label: 'Bulletins & Jury', 
    roles: ['admin', 'secretariat', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"></path><path d="M14 2v6h6m-8 5h5m-5 4h5m-9-9h1"></path></svg>'
  },
  { 
    path: '/secretariat/modification-notes', 
    label: 'Mise à jour Notes', 
    roles: ['admin', 'secretariat', 'super_admin', 'enseignant'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>'
  },
  { 
    path: '/deliberations', 
    label: 'PV & Délibérations', 
    roles: ['admin', 'secretariat', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>'
  },
  { 
    path: '/personnel', 
    label: 'Gestion Personnel', 
    roles: ['admin', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 00-3-3.87m-4-12a4 4 0 010 7.75"></path></svg>'
  },
  { 
    path: '/admin/audit', 
    label: 'Journal d\'Audit', 
    roles: ['admin', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
  },
  { 
    path: '/parametres', 
    label: 'Paramètres', 
    roles: ['admin', 'super_admin'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"></path></svg>'
  },
  { 
    path: '/profil', 
    label: 'Mon Profil', 
    roles: ['admin', 'secretariat', 'super_admin', 'enseignant', 'etudiant'], 
    iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>'
  }
]

const navSections = computed(() => {
  const links = allLinks.filter(l => l.roles.includes(currentRole.value))
  
  return [
    {
      title: 'Pédagogie',
      links: links.filter(l => ['Architecture Académique', 'Registre Étudiants', 'Intervenants', 'Journal Absences', 'Bulletins & Jury', 'PV & Délibérations'].includes(l.label))
    },
    {
      title: 'Saisie & Notes',
      links: links.filter(l => ['Mise à jour Notes'].includes(l.label))
    },
    {
      title: 'Administration',
      links: links.filter(l => ['Gestion Personnel', 'Journal d\'Audit', 'Paramètres'].includes(l.label))
    },
    {
      title: 'Compte',
      links: links.filter(l => ['Mon Profil'].includes(l.label))
    }
  ].filter(s => s.links.length > 0)
})

// Bloquer le scroll du body quand la sidebar mobile est ouverte
watch(isSidebarOpen, (val) => {
  if (process.client) {
    document.body.style.overflow = val ? 'hidden' : ''
  }
})

const logout = () => {
  const t = useCookie('auth_token'); const r = useCookie('authRole'); const i = useCookie('authId')
  t.value = null; r.value = null; i.value = null
  navigateTo('/')
}
</script>

<style scoped>
.app-layout { 
  display: flex; 
  min-height: 100vh; 
  background: #f1f5f9; 
}

/* Sidebar Monochrome & Professionnelle */
.sidebar-p { 
  width: 280px; 
  background: #0f172a; 
  color: #f8fafc; 
  display: flex; 
  flex-direction: column; 
  position: fixed; 
  top: 0; 
  left: 0; 
  height: 100vh; 
  z-index: 1000; 
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-right: 1px solid rgba(255, 255, 255, 0.05);
}

.sidebar-header { 
  padding: 2.5rem 1.5rem; 
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-box {
  width: 42px;
  height: 42px;
  background: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 4px;
}

.brand-info h2 {
  font-size: 1.15rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -0.02em;
  color: white;
}

.brand-info .tagline {
  display: block;
  font-size: 0.6rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.sidebar-nav-p { 
  flex: 1; 
  padding: 1rem; 
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.nav-group-title {
  font-size: 0.7rem;
  font-weight: 700;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding-left: 1rem;
  margin-bottom: 0.75rem;
}

.nav-links-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.nav-link-p { 
  display: flex; 
  align-items: center; 
  gap: 1rem; 
  padding: 0.8rem 1.25rem; 
  color: #94a3b8; 
  text-decoration: none; 
  font-size: 0.9rem; 
  font-weight: 600; 
  border-radius: 10px; 
  transition: all 0.2s; 
}

.nav-link-p:hover { 
  background: rgba(255, 255, 255, 0.05); 
  color: white; 
}

.nav-link-p.router-link-active { 
  background: rgba(255, 255, 255, 0.1); 
  color: white; 
}

.icon-p { 
  font-size: 1.2rem; 
  opacity: 0.7; 
}

.sidebar-footer-p { 
  padding: 1.5rem; 
  background: rgba(0, 0, 0, 0.2); 
  display: flex; 
  align-items: center; 
  gap: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.avatar-p { 
  width: 38px; 
  height: 38px; 
  background: rgba(255, 255, 255, 0.1); 
  color: white; 
  border-radius: 8px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  font-weight: 700; 
  font-size: 0.9rem;
}

.user-meta {
  flex: 1;
  min-width: 0;
}

.name-p { 
  font-size: 0.85rem; 
  font-weight: 700; 
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis; 
}

.role-p { 
  font-size: 0.7rem; 
  color: #64748b; 
  text-transform: capitalize; 
}

.btn-logout-p { 
  background: transparent; 
  border: none;
  color: #ef4444; 
  padding: 0.5rem; 
  border-radius: 8px; 
  cursor: pointer; 
  transition: all 0.2s; 
  opacity: 0.7;
}

.btn-logout-p:hover { 
  background: rgba(239, 68, 68, 0.1); 
  opacity: 1;
}

/* Main Content Area */
.main-body-p { 
  margin-left: 280px; 
  flex: 1; 
  display: flex; 
  flex-direction: column; 
}

.navbar-p { 
  height: 70px; 
  background: white; 
  border-bottom: 1px solid #e2e8f0; 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  padding: 0 2rem; 
  position: sticky; 
  top: 0; 
  z-index: 100;
}

.menu-trigger-p { 
  display: none; 
  background: #f1f5f9; 
  border: none; 
  width: 36px; 
  height: 36px; 
  border-radius: 8px; 
  cursor: pointer; 
}

@media (max-width: 1024px) {
  .sidebar-p { transform: translateX(-100%); }
  .sidebar-p.is-open { transform: translateX(0); }
  .main-body-p { margin-left: 0; }
  .menu-trigger-p { display: block; }
}
</style>
