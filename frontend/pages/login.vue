<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>Bull ASUR</h1>
        <p>Connexion | {{ roleTitle }}</p>
      </div>
      
      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Identifiant</label>
          <input type="text" id="username" v-model="username" placeholder="Entrez votre identifiant" required />
        </div>
        
        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input type="password" id="password" v-model="password" placeholder="Entrez votre mot de passe" required />
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
  loading.value = true
  
  try {
    const { useMockDb } = await import('~/composables/useMockDb.js')
    const db = useMockDb()
    
    // Essayer d'authentifier l'utilisateur
    const authResult = db.authenticate(username.value, password.value, userRole.value)
    
    if (authResult) {
      // Succès: Sauvegarde des infos dans les cookies
      const authRole = useCookie('authRole', { default: () => 'etudiant' })
      const authUsername = useCookie('authUsername')
      const authEmail = useCookie('authEmail')
      const authFullName = useCookie('authFullName')
      const authId = useCookie('authId')

      authRole.value = authResult.role
      authUsername.value = authResult.prenom
      authEmail.value = authResult.email
      authFullName.value = authResult.name
      authId.value = authResult.id

      // Redirection dynamisée selon le rôle
      if (authResult.role === 'admin') router.push('/admin')
      else if (authResult.role === 'secretariat') router.push('/secretariat')
      else if (authResult.role === 'enseignant') router.push('/enseignant')
      else router.push('/etudiant')
    } else {
      alert("Identifiant ou mot de passe incorrect pour ce rôle.")
    }
  } catch (e) {
    console.error(e)
    alert("Erreur lors de la connexion.")
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
