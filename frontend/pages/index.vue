<template>
  <div class="landing-page" @mousemove="handleMouseMove">
    <div class="spatial-aura" :style="auraStyle"></div>
    <div class="overlay"></div>
    
    <!-- Barre Supérieure Ministérielle -->
    <div class="top-banner">
      <div class="ministry-info">
        <p>MINISTERE DE LA COMMUNICATION</p>
        <p>ET DE L'ECONOMIE NUMERIQUE</p>
        <div class="separator"></div>
      </div>
      <div class="republic-info">
        <p>REPUBLIQUE GABONAISE</p>
        <p>UNION - TRAVAIL - JUSTICE</p>
        <div class="separator"></div>
      </div>
    </div>

    <div class="content-wrapper">
      <header class="landing-header">
        <div class="main-logo-container">
          <img src="/logo.png" alt="Bull ASUR Logo" class="landing-logo">
        </div>
        <h1>Bienvenue sur Bull ASUR</h1>
        <p class="subtitle">Le portail de gestion des bulletins de notes - LP ASUR (INPTIC)</p>
      </header>

      <!-- Étape 1 : Sélection du Rôle -->
      <transition name="fade-slide" mode="out-in">
        <div v-if="!showLoginForm" key="selection" class="roles-container">
          <div @click="selectRole('etudiant')" class="premium-card etudiant-border">
            <div class="card-content">
              <span class="icon-p">🎓</span>
              <h2>Étudiant</h2>
              <p>Notes & Bulletins</p>
            </div>
          </div>

          <div @click="selectRole('enseignant')" class="premium-card enseignant-border">
            <div class="card-content">
              <span class="icon-p">📖</span>
              <h2>Enseignant</h2>
              <p>Saisie des Notes</p>
            </div>
          </div>

          <div @click="selectRole('secretariat')" class="premium-card secretariat-border">
            <div class="card-content">
              <span class="icon-p">🏢</span>
              <h2>Secrétariat</h2>
              <p>Gestion Académique</p>
            </div>
          </div>

          <div @click="selectRole('admin')" class="premium-card admin-border">
            <div class="card-content">
              <span class="icon-p">⚙️</span>
              <h2>Admin</h2>
              <p>Configuration</p>
            </div>
          </div>
        </div>

        <!-- Étape 2 : Formulaire de Connexion Overlay -->
        <div v-else key="login" class="login-overlay">
          <div class="login-card glass-morphism">
            <button class="back-btn" @click="showLoginForm = false">
              ← Retour aux rôles
            </button>
            <div class="login-header">
              <span class="role-badge" :class="selectedRole + '-badge'">{{ roleTitle }}</span>
              <h2>Identification</h2>
            </div>
            
            <form class="login-form" @submit.prevent="handleLogin">
              <div class="form-group">
                <label>Identifiant (Email)</label>
                <input type="email" v-model="username" placeholder="exemple@univ.ga" required autocomplete="email" />
              </div>
              
              <div class="form-group">
                <label>Mot de passe</label>
                <input type="password" v-model="password" placeholder="••••••••" required autocomplete="current-password" />
              </div>
              
              <button type="submit" class="login-btn" :disabled="loading">
                <span v-if="!loading">Accéder à l'espace</span>
                <span v-else class="loader"></span>
              </button>
            </form>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

definePageMeta({ layout: 'empty' })

const router = useRouter(); const { fetchApi } = useApi()

// Mouse Tracking pour effet spatial
const mouseX = ref(0); const mouseY = ref(0)
const handleMouseMove = (e) => {
  mouseX.value = e.clientX; mouseY.value = e.clientY
}
const auraStyle = computed(() => ({
  background: `radial-gradient(600px circle at ${mouseX.value}px ${mouseY.value}px, rgba(255,255,255,0.1), transparent 40%)`
}))

// États
const selectedRole = ref(null)
const showLoginForm = ref(false)
const username = ref(''); const password = ref(''); const loading = ref(false)

const roleTitle = computed(() => {
  const titles = { admin: 'Admin', secretariat: 'Secrétariat', enseignant: 'Enseignant', etudiant: 'Étudiant' }
  return titles[selectedRole.value] || 'Étudiant'
})

const selectRole = (role) => { selectedRole.value = role; showLoginForm.value = true }

const handleLogin = async () => {
  if (loading.value) return; loading.value = true
  try {
    const res = await fetchApi('/auth/login/', { method: 'POST', body: { email: username.value, password: password.value } })
    if (res?.access_token) {
      useCookie('auth_token').value = res.access_token
      useCookie('authRole').value = res.user.role
      useCookie('authFullName').value = res.user.name
      useCookie('authId').value = res.user.id
      router.push(`/${res.user.role}`)
    }
  } catch (e) { 
    console.error(e)
    alert(e.data?.error || "Échec de connexion") 
  } finally { loading.value = false }
}
</script>

<style scoped>
.landing-page { position: relative; min-height: 100vh; width: 100%; display: flex; flex-direction: column; background-image: url('~/assets/images/acceuil_bull.jpeg'); background-size: cover; background-position: center; overflow: hidden; }
.spatial-aura { position: absolute; inset: 0; z-index: 2; pointer-events: none; transition: background 0.1s ease-out; }
.overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(2px); z-index: 1; }

.top-banner { position: relative; z-index: 10; display: flex; justify-content: space-between; padding: 2rem 4rem; color: white; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; }
.separator { width: 40px; height: 2px; background: #fff; margin-top: 5px; }

.content-wrapper { position: relative; z-index: 5; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; }
.landing-header { text-align: center; margin-bottom: 5rem; }
.landing-logo { height: 160px; filter: drop-shadow(0 20px 40px rgba(0,0,0,0.4)); margin-bottom: 2rem; position: relative; z-index: 10; }
.landing-header h1 { font-size: clamp(2.5rem, 8vw, 5.5rem); font-weight: 950; letter-spacing: -3px; color: #fff; margin-bottom: 1rem; }
.subtitle { font-size: 1.2rem; color: rgba(255,255,255,0.7); font-weight: 600; letter-spacing: 0.5px; }

.roles-container { display: grid; grid-template-columns: repeat(4, 280px); gap: 2rem; justify-content: center; width: 100%; max-width: 1400px; }
.premium-card { background: rgba(255,255,255,0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 3rem 2rem; text-align: center; color: white; cursor: pointer; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); min-height: 250px; display: flex; align-items: center; justify-content: center; }
.premium-card:hover { background: #fff; color: #000; transform: translateY(-15px) scale(1.05); box-shadow: 0 40px 80px rgba(0,0,0,0.5); }
.icon-p { font-size: 3rem; display: block; margin-bottom: 1.5rem; }
.premium-card h2 { font-size: 1.5rem; font-weight: 900; margin-bottom: 0.5rem; }
.premium-card p { font-size: 0.85rem; opacity: 0.6; font-weight: 700; }

.login-card { background: #fff; color: #000; padding: 4rem; border-radius: 40px; width: 100%; max-width: 500px; box-shadow: 0 50px 100px rgba(0,0,0,0.5); position: relative; z-index: 10; }
.back-btn { background: transparent; border: none; font-weight: 800; color: #64748b; cursor: pointer; margin-bottom: 2rem; padding: 0; }
.role-badge { padding: 0.5rem 1rem; background: #f1f5f9; border-radius: 50px; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; margin-bottom: 1.5rem; display: inline-block; }

.form-group { margin-bottom: 2rem; }
.form-group label { display: block; font-size: 0.8rem; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.75rem; text-align: left; }
.form-group input { width: 100%; padding: 1.25rem; background: #f8fafc; border: 2.5px solid #f1f5f9; border-radius: 16px; font-weight: 800; outline: none; }
.form-group input:focus { border-color: #000; }

.login-btn { width: 100%; padding: 1.25rem; background: #000; color: #fff; font-weight: 900; border-radius: 16px; border: none; cursor: pointer; transition: 0.3s; }
.login-btn:hover { transform: scale(1.02); }

@media (max-width: 1200px) { .roles-container { grid-template-columns: repeat(2, 1fr); max-width: 700px; } }
@media (max-width: 640px) {
  .roles-container { grid-template-columns: 1fr; gap: 1rem; width: 100%; }
  .premium-card { min-height: 120px; padding: 1.5rem; border-radius: 20px; }
  .icon-p { font-size: 2rem; margin-bottom: 0.5rem; }
  .premium-card h2 { font-size: 1.2rem; }
  .landing-header { margin-bottom: 3rem; }
  .landing-logo { height: 100px; }
  .top-banner { padding: 1.5rem; }
  .login-card { padding: 2.5rem; border-radius: 30px; }
}

.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.5s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateY(30px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-30px); }
</style>
