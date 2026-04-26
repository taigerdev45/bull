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
        <div class="logo-outer">
          <img src="/logo.png" alt="Bull Logo">
        </div>
        <div class="brand-name">
          <h2>Bull ASUR</h2>
          <span class="tagline">Enterprise Edition</span>
        </div>
      </div>

      <nav class="sidebar-nav-p">
        <div class="nav-section-p">
          <span class="section-title">Principal</span>
          <NuxtLink :to="`/${currentRole}`" class="nav-link-p">
            <span class="icon-p">⊞</span>
            Dashboard
          </NuxtLink>
        </div>

        <div class="nav-section-p">
          <span class="section-title">Administration</span>
          <NuxtLink v-for="link in allowedLinks" :key="link.path" :to="link.path" class="nav-link-p">
            <span class="icon-p" v-html="link.iconSvg"></span>
            {{ link.label }}
          </NuxtLink>
        </div>
      </nav>

      <div class="sidebar-footer-p">
        <div class="profile-mini">
          <div class="avatar-p">{{ currentRole.charAt(0).toUpperCase() }}</div>
          <div class="meta-p">
            <span class="name-p">{{ userName || 'Admin' }}</span>
            <span class="role-p">{{ currentRole }}</span>
          </div>
        </div>
        <button @click="logout" class="btn-logout-p" title="Sortie">✕</button>
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
          <div class="notif-p">
            <span class="n-icon">🔔</span>
            <span class="dot"></span>
          </div>
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

const route = useRoute()
const isSidebarOpen = ref(false)
const currentRole = useCookie('authRole', { default: () => 'etudiant' })
const userName = useCookie('authName')

const currentRoute = computed(() => {
  const path = route.path
  if (path === '/') return 'Authentification'
  const parts = path.split('/')
  const last = parts[parts.length - 1]
  return last.charAt(0).toUpperCase() + last.slice(1).replace(/-/g, ' ')
})

const allLinks = [
  { 
    path: '/admin/referentiels', 
    label: 'Architecture', 
    roles: ['admin', 'super_admin'], 
    iconSvg: '⚙️'
  },
  { 
    path: '/secretariat/etudiants', 
    label: 'Registre Étudiants', 
    roles: ['admin', 'secretariat', 'super_admin'], 
    iconSvg: '👥'
  },
  { 
    path: '/secretariat/enseignants', 
    label: 'Intervenants', 
    roles: ['admin', 'secretariat', 'super_admin'], 
    iconSvg: '👨‍🏫'
  },
  { 
    path: '/secretariat/absences', 
    label: 'Journal Absences', 
    roles: ['admin', 'secretariat', 'super_admin'], 
    iconSvg: '⌛'
  },
  { 
    path: '/secretariat/bulletins', 
    label: 'Bulletins & Jury', 
    roles: ['admin', 'secretariat', 'super_admin', 'etudiant', 'enseignant'], 
    iconSvg: '📄'
  },
  { 
    path: '/secretariat/modification-notes', 
    label: 'Mise à jour Notes', 
    roles: ['admin', 'secretariat', 'super_admin', 'enseignant'], 
    iconSvg: '✏️'
  }
]

const allowedLinks = computed(() => allLinks.filter(l => l.roles.includes(currentRole.value)))

const logout = () => {
  const t = useCookie('auth_token'); const r = useCookie('authRole'); const i = useCookie('authId')
  t.value = null; r.value = null; i.value = null
  navigateTo('/')
}
</script>

<style scoped>
.app-layout { display: flex; min-height: 100vh; background: #f8fafc; }

/* Sidebar Premium */
.sidebar-p { 
  width: 280px; background: #000; color: #fff; display: flex; flex-direction: column; 
  position: fixed; top: 0; left: 0; bottom: 0; z-index: 1000; 
  box-shadow: 10px 0 30px rgba(0,0,0,0.1); transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.sidebar-header { padding: 3rem 2rem; text-align: center; }
.logo-outer { 
  width: 60px; height: 60px; background: #fff; margin: 0 auto 1.5rem; 
  border-radius: 18px; padding: 12px; transform: rotate(-3deg);
  box-shadow: 10px 10px 20px rgba(0,0,0,0.3);
}
.logo-outer img { width: 100%; height: 100%; object-fit: contain; }
.brand-name h2 { font-size: 1.4rem; font-weight: 900; letter-spacing: -1px; margin-bottom: 0.25rem; }
.brand-name .tagline { font-size: 0.65rem; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 2px; }

.sidebar-nav-p { flex: 1; padding: 1rem; }
.nav-section-p { margin-bottom: 2.5rem; }
.section-title { font-size: 0.65rem; font-weight: 900; color: #475569; text-transform: uppercase; letter-spacing: 2px; margin-left: 1.5rem; margin-bottom: 1rem; display: block; }

.nav-link-p { 
  display: flex; align-items: center; gap: 1rem; padding: 1rem 1.5rem; 
  color: #94a3b8; text-decoration: none; font-size: 0.95rem; font-weight: 800; 
  border-radius: 14px; transition: all 0.2s; margin-bottom: 0.5rem;
}
.nav-link-p .icon-p { font-size: 1.2rem; opacity: 0.5; }
.nav-link-p:hover { background: rgba(255,255,255,0.05); color: #fff; }
.nav-link-p.router-link-active { background: #fff; color: #000; box-shadow: 0 10px 20px rgba(255,255,255,0.1); }
.nav-link-p.router-link-active .icon-p { opacity: 1; }

.sidebar-footer-p { padding: 2rem; background: rgba(255,255,255,0.03); display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.profile-mini { display: flex; align-items: center; gap: 1rem; }
.avatar-p { width: 40px; height: 40px; background: #fff; color: #000; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: 950; }
.meta-p { display: flex; flex-direction: column; line-height: 1.2; }
.name-p { font-size: 0.85rem; font-weight: 800; }
.role-p { font-size: 0.65rem; font-weight: 800; color: #64748b; text-transform: uppercase; }
.btn-logout-p { background: transparent; border: 2px solid rgba(255,255,255,0.1); color: #fff; padding: 0.5rem; border-radius: 10px; cursor: pointer; transition: all 0.2s; }
.btn-logout-p:hover { background: #fee2e2; color: #ef4444; border-color: #ef4444; }

/* Main Body */
.main-body-p { margin-left: 280px; flex: 1; display: flex; flex-direction: column; min-height: 100vh; }
.navbar-p { 
  height: 80px; background: rgba(255,255,255,0.8); backdrop-filter: blur(12px); 
  border-bottom: 1px solid rgba(0,0,0,0.05); display: flex; align-items: center; 
  justify-content: space-between; padding: 0 3rem; position: sticky; top: 0; z-index: 100;
}

.nav-left-p { display: flex; align-items: center; gap: 2rem; }
.menu-trigger-p { display: none; background: #000; color: #fff; border: none; width: 40px; height: 40px; border-radius: 10px; cursor: pointer; }

.breadcrumb-p { display: flex; align-items: center; gap: 0.75rem; font-size: 0.9rem; font-weight: 900; }
.breadcrumb-p .root { color: #94a3b8; }
.breadcrumb-p .sep { color: #cbd5e1; }
.breadcrumb-p .current { color: #000; }

.nav-right-p { display: flex; align-items: center; gap: 2rem; }
.search-premium { 
  display: flex; align-items: center; gap: 0.75rem; background: #fff; 
  border: 2px solid #f1f5f9; padding: 0.7rem 1.5rem; border-radius:14px; width: 300px; 
  transition: all 0.3s;
}
.search-premium:focus-within { border-color: #000; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
.search-premium input { border: none; outline: none; width: 100%; font-weight: 700; font-size: 0.85rem; }

.notif-p { position: relative; cursor: pointer; }
.n-icon { font-size: 1.4rem; color: #64748b; }
.notif-p .dot { position: absolute; top: -2px; right: -2px; width: 10px; height: 10px; background: #000; border: 2px solid #fff; border-radius: 50%; }

.content-p { padding: 0; }

/* PWA Toast Premium */
.pwa-toast-premium { 
  position: fixed; bottom: 2rem; right: 2rem; padding: 1.5rem 2.5rem; 
  background: #000; color: #fff; border-radius: 20px; z-index: 2000; 
  display: flex; align-items: center; gap: 2rem; 
}
.message { display: flex; align-items: center; gap: 1rem; font-weight: 800; font-size: 0.9rem; }
.btn-pwa { background: #fff; border: none; color: #000; padding: 0.6rem 1.2rem; border-radius: 50px; font-weight: 900; font-size: 0.8rem; cursor: pointer; transition: scale 0.2s; }
.btn-pwa:hover { scale: 1.05; }
.pulsar-white { width: 10px; height: 10px; background: #fff; border-radius: 50%; animation: pulse-w 1.5s infinite; }
@keyframes pulse-w { 0% { box-shadow: 0 0 0 0 rgba(255,255,255,0.4); } 70% { box-shadow: 0 0 0 12px rgba(255,255,255,0); } 100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); } }

@media (max-width: 1024px) {
  .sidebar-p { transform: translateX(-100%); }
  .sidebar-p.is-open { transform: translateX(0); }
  .main-body-p { margin-left: 0; }
  .menu-trigger-p { display: block; }
  .search-premium { display: none; }
  .navbar-p { padding: 0 1.5rem; }
  .sidebar-overlay-p { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(8px); z-index: 999; }
}
</style>
