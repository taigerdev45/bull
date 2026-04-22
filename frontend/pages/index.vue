<template>
  <div class="landing-page">
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
        <h1>Bienvenue sur Bull ASUR</h1>
        <p class="subtitle">Le portail de gestion des bulletins de notes - LP ASUR (INPTIC)</p>
      </header>

      <!-- Étape 1 : Sélection du Rôle -->
      <transition name="fade-slide" mode="out-in">
        <div v-if="!showLoginForm" key="selection" class="roles-container">
          <div @click="selectRole('etudiant')" class="premium-card etudiant-border">
            <div class="card-content">
              <h2>Espace Étudiant</h2>
              <p>Consultez vos notes, absences et téléchargez vos bulletins officiels.</p>
            </div>
          </div>

          <div @click="selectRole('enseignant')" class="premium-card enseignant-border">
            <div class="card-content">
              <h2>Espace Enseignant</h2>
              <p>Saisissez les notes de vos évaluations (CC, Examens, Rattrapages).</p>
            </div>
          </div>

          <div @click="selectRole('secretariat')" class="premium-card secretariat-border">
            <div class="card-content">
              <h2>Secrétariat Pédagogique</h2>
              <p>Gérez les élèves, les inscriptions, la saisie administrative et générez les bulletins.</p>
            </div>
          </div>

          <div @click="selectRole('admin')" class="premium-card admin-border">
            <div class="card-content">
              <h2>Administration</h2>
              <p>Configuration complète, gestion des référentiels (UEs, Matières), audits système.</p>
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
              <h2>Connexion</h2>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

definePageMeta({
  layout: 'empty'
})

const router = useRouter()
const route = useRoute()
const { fetchApi } = useApi()

// États
const selectedRole = ref(null)
const showLoginForm = ref(false)
const username = ref('')
const password = ref('')
const loading = ref(false)

// Détection automatique du rôle via l'URL (compatibilité anciens liens)
onMounted(() => {
  const roleQuery = route.query.role
  if (roleQuery && ['etudiant', 'enseignant', 'secretariat', 'admin'].includes(roleQuery)) {
    selectRole(roleQuery)
  }
})

// Cookies
const authToken = useCookie('auth_token')
const authRole = useCookie('authRole')
const authEmail = useCookie('authEmail')
const authFullName = useCookie('authFullName')
const authId = useCookie('authId')

const roleTitle = computed(() => {
  switch (selectedRole.value) {
    case 'admin': return 'Administration'
    case 'secretariat': return 'Secrétariat'
    case 'enseignant': return 'Enseignant'
    case 'etudiant': return 'Étudiant'
    default: return 'Étudiant'
  }
})

useHead({
  title: computed(() => `Accueil | ${roleTitle.value}`)
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
      authToken.value = authResult.access_token
      authRole.value = authResult.user.role
      authEmail.value = authResult.user.email
      authFullName.value = authResult.user.name
      authId.value = authResult.user.id

      const role = authResult.user.role || selectedRole.value
      if (role === 'admin') router.push('/admin')
      else if (role === 'secretariat') router.push('/secretariat')
      else if (role === 'enseignant') router.push('/enseignant')
      else router.push('/etudiant')
    } else {
      throw new Error("Serveur inaccessible ou réponse invalide.")
    }
  } catch (e) {
    console.error("Login error:", e)
    const errorMsg = e.data?.error || e.message || "Identifiants incorrects."
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
  flex-direction: column;
  background-image: url('~/assets/images/acceuil_bull.jpeg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  overflow-x: hidden;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: brightness(0.8);
  z-index: 1;
}

/* Barre Supérieure */
.top-banner {
  position: relative;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  padding: 1.5rem 3rem;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.ministry-info, .republic-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.separator {
  width: 60%;
  height: 2px;
  background: white;
  margin-top: 5px;
  opacity: 0.8;
}

/* Content Wrapper */
.content-wrapper {
  position: relative;
  z-index: 2;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: white;
}

.landing-header {
  text-align: center;
  margin-bottom: 4rem;
}

.landing-header h1 {
  font-size: 4.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  text-shadow: 0 4px 10px rgba(0,0,0,0.5);
  letter-spacing: -2px;
}

.subtitle {
  font-size: 1.4rem;
  font-weight: 400;
  opacity: 0.95;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

/* Roles Grid (Match avec l'image) */
.roles-container {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  width: 100%;
  max-width: 1300px;
}

.premium-card {
  flex: 1;
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 3rem 1.5rem;
  min-height: 380px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
  cursor: pointer;
  box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

.premium-card:hover {
  transform: translateY(-12px);
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.3);
}

/* Borders colorés en bas */
.etudiant-border { border-bottom: 6px solid #3b82f6; }
.enseignant-border { border-bottom: 6px solid #10b981; }
.secretariat-border { border-bottom: 6px solid #8b5cf6; }
.admin-border { border-bottom: 6px solid #f59e0b; }

.premium-card h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
}

.premium-card p {
  font-size: 1rem;
  line-height: 1.6;
  opacity: 0.85;
}

/* Login Overlay */
.login-overlay {
  width: 100%;
  max-width: 480px;
}

.glass-morphism {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 2rem;
  padding: 4rem 3rem;
  box-shadow: 0 30px 60px rgba(0,0,0,0.6);
}

.back-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 0.9rem;
  cursor: pointer;
  margin-bottom: 2.5rem;
  padding: 0;
  transition: color 0.2s;
}

.back-btn:hover { color: white; }

.role-badge {
  display: inline-block;
  padding: 0.4rem 1rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 800;
  text-transform: uppercase;
  margin-bottom: 1.5rem;
}

.etudiant-badge { background: #3b82f633; color: #60a5fa; }
.enseignant-badge { background: #10b98133; color: #34d399; }
.secretariat-badge { background: #8b5cf633; color: #a78bfa; }
.admin-badge { background: #f59e0b33; color: #fbbf24; }

.form-group { margin-bottom: 1.5rem; }
.form-group label { display: block; font-size: 0.9rem; margin-bottom: 0.75rem; color: #cbd5e1; }
.form-group input {
  width: 100%;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.8rem;
  color: white;
  transition: all 0.3s;
}

.form-group input:focus { border-color: #3b82f6; outline: none; background: #0f172a; }

.login-btn {
  width: 100%;
  padding: 1.25rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  font-weight: 800;
  border-radius: 0.8rem;
  cursor: pointer;
  border: none;
  transition: transform 0.3s;
}

.login-btn:hover:not(:disabled) { transform: scale(1.02); }

/* Transitions */
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.5s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateY(30px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-30px); }

@media (max-width: 1024px) {
  .roles-container { flex-wrap: wrap; }
  .premium-card { min-width: 45%; }
}

@media (max-width: 640px) {
  .top-banner { padding: 1rem; flex-direction: column; gap: 1rem; }
  .landing-header h1 { font-size: 2.5rem; }
  .premium-card { min-width: 100%; min-height: auto; padding: 2rem; }
}
</style>
