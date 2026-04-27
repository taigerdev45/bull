<template>
  <div class="landing-page" @mousemove="handleMouseMove">
    <!-- Overlay Effet Spatial : Bulles Blanches -->
    <canvas ref="bubbleCanvas" class="bubble-layer"></canvas>
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
          <img src="/logo.png" alt="Bull ASUR Logo Officiel" class="landing-logo">
        </div>
        <h1>Portail Bull ASUR</h1>
        <p class="subtitle">Système Intégré de Gestion Académique - LP ASUR (INPTIC)</p>
      </header>

      <!-- Étape 1 : Sélection du Rôle (SANS ICONES) -->
      <transition name="fade-slide" mode="out-in">
        <div v-if="!showLoginForm" key="selection" class="roles-container">
          <div @click="selectRole('etudiant')" class="premium-card etudiant-border">
            <div class="card-content">
              <h2>Espace Étudiant</h2>
              <p>Consultation des notes et bulletins</p>
            </div>
          </div>

          <div @click="selectRole('enseignant')" class="premium-card enseignant-border">
            <div class="card-content">
              <h2>Espace Enseignant</h2>
              <p>Saisie et transmission des notes</p>
            </div>
          </div>

          <div @click="selectRole('secretariat')" class="premium-card secretariat-border">
            <div class="card-content">
              <h2>Secrétariat</h2>
              <p>Pilotage académique et administration</p>
            </div>
          </div>

          <div @click="selectRole('admin')" class="premium-card admin-border">
            <div class="card-content">
              <h2>Administrateur</h2>
              <p>Maintenance et sécurité système</p>
            </div>
          </div>
        </div>

        <!-- Étape 2 : Formulaire de Connexion Overlay -->
        <div v-else key="login" class="login-overlay">
          <div class="login-card glass-morphism">
            <button class="back-btn" @click="showLoginForm = false">
              ← Revenir à la sélection
            </button>
            <div class="login-header">
              <span class="role-badge">{{ roleTitle }}</span>
              <h2>Authentification Sécurisée</h2>
            </div>
            
            <form class="login-form" @submit.prevent="handleLogin">
              <div class="form-group">
                <label>Nom d'utilisateur / Email</label>
                <input type="email" v-model="username" placeholder="votre.nom@inptic.ga" required autocomplete="email" />
              </div>
              
              <div class="form-group">
                <label>Mot de passe</label>
                <input type="password" v-model="password" placeholder="••••••••" required autocomplete="current-password" />
              </div>
              
              <button type="submit" class="login-btn" :disabled="loading">
                <span v-if="!loading">Se Connecter</span>
                <span v-else class="loader"></span>
              </button>
            </form>
          </div>
        </div>
      </transition>

      <!-- SEO Content Sections -->
      <section class="seo-content">
        <div class="seo-grid">
          <article class="seo-item">
            <h3>À propos de Bull ASUR</h3>
            <p>Bull ASUR est la solution logicielle de pointe conçue spécifiquement pour la Licence Professionnelle en Administration et Sécurité des Réseaux (ASUR) de l'INPTIC. Cette plateforme centralise la gestion des notes, le suivi des présences et l'édition des bulletins officiels.</p>
          </article>
          <article class="seo-item">
            <h3>Modernisation Numérique</h3>
            <p>Dans le cadre de la transformation digitale de l'enseignement au Gabon, Bull ASUR offre une interface web moderne, intuitive et ultra-performante pour garantir la fiabilité des données académiques et la transparence des résultats.</p>
          </article>
          <article class="seo-item">
            <h3>Sécurité & Intégrité</h3>
            <p>Grâce à son architecture sécurisée, le système protège l'intégrité des notes et assure une traçabilité complète de chaque modification effectuée par le corps enseignant et le secrétariat pédagogique.</p>
          </article>
        </div>
      </section>

      <footer class="landing-footer">
        <p>&copy; 2026 INPTIC - Bull ASUR v2.5. Plateforme optimisée par TaigerDev.</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

definePageMeta({ layout: 'empty' })

const router = useRouter(); const { fetchApi } = useApi()

// Bubble Animation Logic
const bubbleCanvas = ref(null)
let ctx = null; let particles = []
const bubbleCount = 60
const mouse = { x: 0, y: 0 }

class Particle {
  constructor() {
    this.reset()
  }
  reset() {
    this.x = mouse.x + (Math.random() - 0.5) * 100
    this.y = mouse.y + (Math.random() - 0.5) * 100
    this.size = Math.random() * 3 + 1
    this.speedX = (Math.random() - 0.5) * 1.5
    this.speedY = (Math.random() - 0.5) * 1.5
    this.opacity = Math.random() * 0.5 + 0.2
    this.life = 0
    this.maxLife = Math.random() * 100 + 50
  }
  update() {
    this.x += this.speedX
    this.y += this.speedY
    this.life++
    if (this.life > this.maxLife) this.reset()
  }
  draw() {
    ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity * (1 - this.life/this.maxLife)})`
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
    ctx.fill()
  }
}

const handleMouseMove = (e) => {
  mouse.x = e.clientX; mouse.y = e.clientY
}

const animate = () => {
  if (!ctx) return
  ctx.clearRect(0, 0, bubbleCanvas.value.width, bubbleCanvas.value.height)
  particles.forEach(p => {
    p.update()
    p.draw()
  })
  requestAnimationFrame(animate)
}

onMounted(() => {
  if (bubbleCanvas.value) {
    bubbleCanvas.value.width = window.innerWidth
    bubbleCanvas.value.height = window.innerHeight
    ctx = bubbleCanvas.value.getContext('2d')
    for (let i = 0; i < bubbleCount; i++) particles.push(new Particle())
    animate()
  }
  window.addEventListener('resize', () => {
    if (bubbleCanvas.value) {
      bubbleCanvas.value.width = window.innerWidth
      bubbleCanvas.value.height = window.innerHeight
    }
  })
})

// Auth States
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
  } catch (e) { alert(e.data?.error || "Identifiants invalides") } finally { loading.value = false }
}
</script>

<style scoped>
.landing-page { position: relative; min-height: 100vh; width: 100%; display: flex; flex-direction: column; background-image: url('~/assets/images/acceuil_bull.jpeg'); background-size: cover; background-position: center; overflow: hidden; }
.bubble-layer { position: absolute; inset: 0; z-index: 2; pointer-events: none; }
.overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.65); backdrop-filter: blur(2px); z-index: 1; }

.top-banner { position: relative; z-index: 10; display: flex; justify-content: space-between; padding: 2rem 4rem; color: white; font-size: 0.75rem; font-weight: 800; }
.separator { width: 40px; height: 3px; background: #fff; margin-top: 8px; }

.content-wrapper { position: relative; z-index: 5; flex: 1; display: flex; flex-direction: column; align-items: center; padding: 4rem 2rem; overflow-y: auto; scrollbar-width: none; }
.content-wrapper::-webkit-scrollbar { display: none; }

.landing-header { text-align: center; margin-bottom: 5rem; }
.landing-logo { height: 160px; margin-bottom: 2rem; position: relative; z-index: 10; }
.landing-header h1 { font-size: clamp(2.5rem, 8vw, 5rem); font-weight: 950; letter-spacing: -3px; color: #fff; line-height: 1; margin-bottom: 1rem; }
.subtitle { font-size: 1.2rem; color: rgba(255,255,255,0.7); font-weight: 600; }

.roles-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 2rem; width: 100%; max-width: 1300px; margin-bottom: 8rem; }
.premium-card { background: rgba(255,255,255,0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 2.5rem; text-align: center; color: white; cursor: pointer; transition: all 0.4s; min-height: 180px; display: flex; align-items: center; justify-content: center; }
.premium-card:hover { background: #fff; color: #000; transform: translateY(-10px); }
.premium-card h2 { font-size: 1.4rem; font-weight: 900; margin-bottom: 0.5rem; }
.premium-card p { font-size: 0.85rem; opacity: 0.6; font-weight: 700; }

.login-card { background: #fff; color: #000; padding: 4rem; border-radius: 40px; width: 100%; max-width: 500px; box-shadow: 0 50px 100px rgba(0,0,0,0.5); }
.back-btn { background: transparent; border: none; font-weight: 800; color: #94a3b8; cursor: pointer; margin-bottom: 2rem; text-decoration: underline; }
.role-badge { padding: 0.4rem 1rem; background: #f1f5f9; border-radius: 50px; font-size: 0.75rem; font-weight: 950; text-transform: uppercase; margin-bottom: 1rem; display: inline-block; }

.form-group { margin-bottom: 2rem; }
.form-group label { display: block; font-size: 0.85rem; font-weight: 900; color: #64748b; margin-bottom: 0.75rem; text-align: left; text-transform: uppercase; }
.form-group input { width: 100%; padding: 1.25rem; background: #f8fafc; border: 2px solid #f1f5f9; border-radius: 16px; font-weight: 800; }
.form-group input:focus { border-color: #000; outline: none; }

.login-btn { width: 100%; padding: 1.25rem; background: #000; color: #fff; font-weight: 900; border-radius: 16px; border: none; cursor: pointer; transition: 0.3s; }

.seo-content { width: 100%; max-width: 1200px; margin-top: 6rem; padding-top: 6rem; border-top: 1px solid rgba(255,255,255,0.1); }
.seo-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 4rem; text-align: left; }
.seo-item h3 { font-size: 1.2rem; font-weight: 900; color: #fff; margin-bottom: 1.5rem; }
.seo-item p { font-size: 0.95rem; line-height: 1.7; color: rgba(255,255,255,0.6); font-weight: 500; }

.landing-footer { margin-top: 10rem; color: rgba(255,255,255,0.3); font-size: 0.8rem; font-weight: 700; text-align: center; }

@media (max-width: 640px) {
  .roles-container { grid-template-columns: 1fr; gap: 1rem; }
  .premium-card { min-height: 100px; padding: 1.5rem; }
  .landing-header h1 { font-size: 2.5rem; }
  .top-banner { padding: 1.5rem; }
  .login-card { padding: 2.5rem; }
}

.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.5s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateY(30px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-30px); }
</style>
