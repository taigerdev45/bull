<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>Bull ASUR</h1>
        <p>Connexion | {{ roleTitle }}</p>
      </div>
      
      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Identifiant (Email)</label>
          <input 
            type="email" 
            id="username" 
            v-model="username" 
            placeholder="Entrez votre email" 
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
            placeholder="Entrez votre mot de passe" 
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
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

definePageMeta({
  layout: 'empty'
})

const route = useRoute()
const router = useRouter()
const { fetchApi } = useApi()

// Initialisation des cookies au niveau racine pour éviter les erreurs de contexte Nuxt
const authToken = useCookie('auth_token')
const authRole = useCookie('authRole')
const authEmail = useCookie('authEmail')
const authFullName = useCookie('authFullName')
const authId = useCookie('authId')

const userRole = computed(() => route.query.role || 'etudiant')

const roleTitle = computed(() => {
  switch (userRole.value) {
    case 'admin': return 'Administration'
    case 'secretariat': return 'Secrétariat Pédagogique'
    case 'enseignant': return 'Espace Enseignant'
    case 'etudiant': return 'Espace Étudiant'
    default: return 'Espace Étudiant'
  }
})

useHead({
  title: computed(() => `Connexion ${roleTitle.value} | LP ASUR`)
})

const username = ref('')
const password = ref('')
const loading = ref(false)

const handleLogin = async () => {
  if (loading.value) return
  loading.value = true
  
  try {
    // Appel à l'API réelle
    console.log("Tentative de connexion pour:", username.value)
    
    const authResult = await fetchApi('/auth/login/', {
      method: 'POST',
      body: {
        email: username.value,
        password: password.value
      }
    })
    
    if (authResult && authResult.access_token) {
      // Succès: Sauvegarde des infos dans les cookies
      authToken.value = authResult.access_token
      authRole.value = authResult.user.role
      authEmail.value = authResult.user.email
      authFullName.value = authResult.user.name
      authId.value = authResult.user.id

      console.log("Connexion réussie, rôle:", authResult.user.role)

      // Redirection selon le rôle retourné par le backend
      const role = authResult.user.role
      if (role === 'admin') router.push('/admin')
      else if (role === 'secretariat') router.push('/secretariat')
      else if (role === 'enseignant') router.push('/enseignant')
      else router.push('/etudiant')
    } else {
      throw new Error("Réponse invalide du serveur d'authentification.")
    }
  } catch (e) {
    console.error("Erreur login détail:", e)
    const errorMsg = e.data?.error || e.message || "Identifiant ou mot de passe incorrect."
    alert(errorMsg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  width: 100%;
  max-width: 420px;
  padding: 2rem;
}

.login-card {
  background-color: var(--surface);
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  padding: 2.5rem 2rem;
}

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.login-header h1 {
  color: var(--primary);
  font-size: 2.25rem;
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  background-color: #fcfcfc;
}

.form-group input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
  background-color: var(--surface);
}

.login-btn {
  width: 100%;
  padding: 0.875rem;
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-btn:hover {
  background-color: var(--primary-hover);
}

.login-btn:active {
  transform: scale(0.98);
}

.login-btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.loader {
  border: 2px solid rgba(255,255,255,0.3);
  border-left-color: #fff;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
