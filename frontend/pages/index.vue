<template>
  <div class="landing-page">
    <div class="overlay"></div>
    <div class="content-wrapper">
      <header class="landing-header">
        <h1>Bienvenue sur Bull ASUR</h1>
        <p>Le portail de gestion des bulletins de notes <strong>DAR 3</strong></p>
      </header>

      <!-- Étape 1 : Sélection du Rôle -->
      <transition name="fade-slide" mode="out-in">
        <div v-if="!showLoginForm" key="selection" class="roles-grid">
          <div @click="selectRole('etudiant')" class="role-card etudiant-theme clickable">
            <div class="role-icon">🎓</div>
            <h2>Espace Étudiant</h2>
            <p>Consultez vos notes officielles.</p>
          </div>

          <div @click="selectRole('enseignant')" class="role-card enseignant-theme clickable">
            <div class="role-icon">👨‍🏫</div>
            <h2>Espace Enseignant</h2>
            <p>Gérez vos évaluations simplement.</p>
          </div>

          <div @click="selectRole('secretariat')" class="role-card secretariat-theme clickable">
            <div class="role-icon">💼</div>
            <h2>Secrétariat Pédagogique</h2>
            <p>Gestion administrative globale.</p>
          </div>

          <div @click="selectRole('admin')" class="role-card admin-theme clickable">
            <div class="role-icon">⚙️</div>
            <h2>Administrateur</h2>
            <p>Management système.</p>
          </div>
        </div>

        <!-- Étape 2 : Formulaire de Connexion -->
        <div v-else key="login" class="login-container">
          <div class="login-card glass-morphism">
            <button class="back-btn" @click="showLoginForm = false">
              ← Retour aux rôles
            </button>
            <div class="login-header">
              <span class="role-badge" :class="selectedRole + '-badge'">{{ roleTitle }}</span>
              <h2>Connexion</h2>
              <p>Entrez vos identifiants pour continuer</p>
            </div>
            
            <form class="login-form" @submit.prevent="handleLogin">
              <div class="form-group">
                <label for="username">Identifiant (Email)</label>
                <input 
                  type="email" 
                  id="username" 
                  v-model="username" 
                  placeholder="exemple@univ.ga" 
                  required 
                  autocomplete="username"
                />
              </div>
              
              <div class="form-group">
                <label for="password">Mot de passe</label>
                <input 
                  type="password" 
                  id="password" 
                  v-model="password" 
                  placeholder="••••••••" 
                  required 
                  autocomplete="current-password"
                />
              </div>
              
              <button type="submit" class="login-btn" :disabled="loading">
                <span v-if="!loading">Se Connecter</span>
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

definePageMeta({
  layout: 'empty'
})

const router = useRouter()
const { fetchApi } = useApi()

// États
const showLoginForm = ref(false)
const selectedRole = ref('etudiant')
const username = ref('')
const password = ref('')
const loading = ref(false)

// Cookies
const authToken = useCookie('auth_token')
const authRole = useCookie('authRole')
const authEmail = useCookie('authEmail')
const authFullName = useCookie('authFullName')
const authId = useCookie('authId')

const roleTitle = computed(() => {
  switch (selectedRole.value) {
    case 'admin': return 'Administrateur'
    case 'secretariat': return 'Secrétariat'
    case 'enseignant': return 'Enseignant'
    case 'etudiant': return 'Étudiant'
    default: return 'Étudiant'
  }
})

useHead({
  title: computed(() => `Accueil | Connexion ${roleTitle.value}`)
})

const selectRole = (role) => {
  selectedRole.value = role
  showLoginForm.value = true
}

const handleLogin = async () => {
  if (loading.value) return
  loading.value = true
  
  try {
    const authResult = await fetchApi('/auth/login/', {
      method: 'POST',
      body: {
        email: username.value,
        password: password.value
      }
    })
    
    if (authResult && authResult.access_token) {
      // Sauvegarde des infos
      authToken.value = authResult.access_token
      authRole.value = authResult.user.role
      authEmail.value = authResult.user.email
      authFullName.value = authResult.user.name
      authId.value = authResult.user.id

      // Redirection dynamique basée sur la sélection ET le retour API
      const role = authResult.user.role || selectedRole.value
      if (role === 'admin') router.push('/admin')
      else if (role === 'secretariat') router.push('/secretariat')
      else if (role === 'enseignant') router.push('/enseignant')
      else router.push('/etudiant')
    } else {
      throw new Error("Réponse invalide du serveur.")
    }
  } catch (e) {
    console.error("Login error:", e)
    const errorMsg = e.data?.error || e.message || "Identifiant ou mot de passe incorrect."
    alert(errorMsg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.landing-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: url('~/assets/images/acceuil_bull.jpeg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(15, 23, 42, 0.6) 0%, rgba(15, 23, 42, 0.9) 100%);
  z-index: 1;
}

.content-wrapper {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1200px;
  padding: 2rem;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.landing-header {
  text-align: center;
  margin-bottom: 3.5rem;
}

.landing-header h1 {
  font-size: 3.5rem;
  font-weight: 800;
  letter-spacing: -2px;
  margin-bottom: 0.5rem;
  background: linear-gradient(to right, #fff, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.landing-header p {
  font-size: 1.25rem;
  color: #cbd5e1;
}

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  width: 100%;
}

.role-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1.25rem;
  padding: 2.5rem 1.5rem;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  cursor: pointer;
}

.role-card:hover {
  transform: translateY(-10px);
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.role-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* Redesign Login Card */
.login-container {
  width: 100%;
  max-width: 450px;
}

.glass-morphism {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 1.5rem;
  padding: 3rem 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
}

.back-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 0.875rem;
  cursor: pointer;
  margin-bottom: 2rem;
  padding: 0;
  transition: color 0.2s;
}

.back-btn:hover {
  color: white;
}

.login-header {
  margin-bottom: 2rem;
}

.role-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 1rem;
}

.etudiant-badge { background: #3b82f633; color: #60a5fa; }
.enseignant-badge { background: #10b98133; color: #34d399; }
.secretariat-badge { background: #8b5cf633; color: #a78bfa; }
.admin-badge { background: #f59e0b33; color: #fbbf24; }

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  color: #94a3b8;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  color: white;
  outline: none;
  transition: all 0.2s;
}

.form-group input:focus {
  border-color: #3b82f6;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.login-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  margin-top: 1rem;
  transition: all 0.3s;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
}

.loader {
  border: 2px solid rgba(255,255,255,0.3);
  border-left-color: #fff;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  display: inline-block;
}

/* Transitions */
.fade-slide-enter-active, .fade-slide-leave-active {
  transition: all 0.4s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .landing-header h1 { font-size: 2.5rem; }
  .roles-grid { grid-template-columns: 1fr; }
}
</style>
