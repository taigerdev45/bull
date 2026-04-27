<template>
  <div class="landing-page" @mousemove="handleMouseMove">
    <!-- Overlay Effet Spatial : Bulle Sphérique de Particules -->
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
          <!-- Logo Restoré Couleurs d'Origine -->
          <img src="/logo.png" alt="Bull ASUR Logo Officiel" class="landing-logo">
        </div>
        <h1>Portail Bull ASUR</h1>
        <p class="subtitle">Gestion Académique & Sécurité des Réseaux - LP ASUR</p>
      </header>

      <!-- Étape 1 : Sélection du Rôle -->
      <transition name="fade-slide" mode="out-in">
        <div v-if="!showLoginForm" key="selection" class="roles-container">
          <div @click="selectRole('etudiant')" class="premium-card etudiant-border">
            <div class="card-content">
              <h2>Étudiant</h2>
              <p>Notes & Parcours</p>
            </div>
          </div>

          <div @click="selectRole('enseignant')" class="premium-card enseignant-border">
            <div class="card-content">
              <h2>Enseignant</h2>
              <p>Saisie Pédagogique</p>
            </div>
          </div>

          <div @click="selectRole('secretariat')" class="premium-card secretariat-border">
            <div class="card-content">
              <h2>Secrétariat</h2>
              <p>Gestion Administrative</p>
            </div>
          </div>

          <div @click="selectRole('admin')" class="premium-card admin-border">
            <div class="card-content">
              <h2>Admin</h2>
              <p>Contrôle Système</p>
            </div>
          </div>
        </div>

        <!-- Étape 2 : Formulaire de Connexion -->
        <div v-else key="login" class="login-overlay">
          <div class="login-card glass-morphism">
            <button class="back-btn" @click="showLoginForm = false">
              ← Retour
            </button>
            <div class="login-header">
              <span class="role-badge">{{ roleTitle }}</span>
              <h2>Authentification</h2>
            </div>
            
            <form class="login-form" @submit.prevent="handleLogin">
              <div class="form-group">
                <label>Email</label>
                <input type="email" v-model="username" placeholder="identifiant@inptic.ga" required autocomplete="email" />
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

      <!-- SEO Content -->
      <section class="seo-content">
        <div class="seo-grid">
          <article class="seo-item">
            <h3>Excellence Académique ASUR</h3>
            <p>La solution logicielle Bull ASUR optimise le suivi des performances pour la Licence Professionnelle en Administration et Sécurité des Réseaux de l'INPTIC.</p>
          </article>
          <article class="seo-item">
            <h3>Digitalisation de l'INPTIC</h3>
            <p>Plateforme centralisée permettant une gestion fluide des notes, PV et délibérations annuelles en toute sécurité et transparence.</p>
          </article>
          <article class="seo-item">
            <h3>Technologie Cloud Gabon</h3>
            <p>Une interface SaaS moderne, conçue pour les standards de l'éducation supérieure numérique au Gabon.</p>
          </article>
        </div>
      </section>

      <footer class="landing-footer">
        <p>&copy; 2026 INPTIC - Plateforme Bull ASUR</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

definePageMeta({ layout: 'empty' })

const router = useRouter(); const { fetchApi } = useApi()

// Bubble Animation Logic (Spherical Sphere Formation)
const bubbleCanvas = ref(null)
let ctx = null; let particles = []
const bubbleCount = 60
const mouse = { x: 0, y: 0 }

class Particle {
  constructor(index) {
    this.index = index
    this.reset()
  }
  reset() {
    this.radius = 80 + Math.random() * 20 // Rayon de la sphère
    this.angle = (this.index / bubbleCount) * Math.PI * 2 + Math.random() * 0.5
    this.size = Math.random() * 2.5 + 1
    this.opacity = Math.random() * 0.6 + 0.2
    this.speed = 0.02 + Math.random() * 0.02
    this.offset = Math.random() * 10
  }
  update() {
    this.angle += this.speed
    this.x = mouse.x + Math.cos(this.angle) * (this.radius + Math.sin(this.angle * 2) * 5)
    this.y = mouse.y + Math.sin(this.angle) * (this.radius + Math.cos(this.angle * 2) * 5)
  }
  draw() {
    ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
    ctx.fill()
    // Subtle glow for the particles
    ctx.shadowBlur = 4; ctx.shadowColor = "white"
  }
}

const handleMouseMove = (e) => {
  mouse.x = e.clientX; mouse.y = e.clientY
}

const animate = () => {
  if (!ctx) return
  ctx.clearRect(0, 0, bubbleCanvas.value.width, bubbleCanvas.value.height)
  ctx.shadowBlur = 0 // Reset shadow for background
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
    for (let i = 0; i < bubbleCount; i++) particles.push(new Particle(i))
    animate()
  }
  window.addEventListener('resize', () => {
    if (bubbleCanvas.value) {
      bubbleCanvas.value.width = window.innerWidth
      bubbleCanvas.value.height = window.innerHeight
    }
  })
})

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
  } catch (e) { alert("Erreur d'identification") } finally { loading.value = false }
}
</script>

<style scoped>
.landing-page { position: relative; min-height: 100vh; width: 100%; display: flex; flex-direction: column; background-image: url('~/assets/images/acceuil_bull.jpeg'); background-size: cover; background-position: center; overflow: hidden; }
.bubble-layer { position: absolute; inset: 0; z-index: 2; pointer-events: none; }
.overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(2px); z-index: 1; }

.top-banner { position: relative; z-index: 10; display: flex; justify-content: space-between; padding: 2rem 4rem; color: white; font-size: 0.7rem; font-weight: 800; }
.separator { width: 40px; height: 3px; background: #fff; margin-top: 8px; }

.content-wrapper { position: relative; z-index: 5; flex: 1; display: flex; flex-direction: column; align-items: center; padding: 4rem 2rem; overflow-y: auto; scrollbar-width: none; }
.content-wrapper::-webkit-scrollbar { display: none; }

.landing-header { text-align: center; margin-bottom: 5rem; }
.landing-logo { height: 160px; filter: none; margin-bottom: 2rem; position: relative; z-index: 10; }
.landing-header h1 { font-size: clamp(2.5rem, 8vw, 4.5rem); font-weight: 950; letter-spacing: -3px; color: #fff; line-height: 1; margin-bottom: 1rem; }
.subtitle { font-size: 1.1rem; color: rgba(255,255,255,0.8); font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }

.roles-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 2rem; width: 100%; max-width: 1200px; margin-bottom: 6rem; }
.premium-card { background: rgba(255,255,255,0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 2.5rem; text-align: center; color: white; cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); min-height: 140px; display: flex; align-items: center; justify-content: center; }
.premium-card:hover { background: #fff; color: #000; transform: translateY(-5px); border-color: #fff; }
.premium-card h2 { font-size: 1.4rem; font-weight: 900; margin-bottom: 0.25rem; }
.premium-card p { font-size: 0.8rem; opacity: 0.6; font-weight: 700; text-transform: uppercase; }

.login-card { background: #fff; color: #000; padding: 3rem; border-radius: 20px; width: 100%; max-width: 450px; box-shadow: 0 40px 80px rgba(0,0,0,0.5); }
.back-btn { background: transparent; border: none; font-weight: 800; color: #94a3b8; cursor: pointer; margin-bottom: 1.5rem; padding: 0; }
.role-badge { padding: 0.4rem 0.8rem; background: #000; color: #fff; border-radius: 4px; font-size: 0.65rem; font-weight: 950; text-transform: uppercase; margin-bottom: 1rem; display: inline-block; }

.form-group { margin-bottom: 1.5rem; }
.form-group label { display: block; font-size: 0.8rem; font-weight: 900; color: #64748b; margin-bottom: 0.5rem; text-align: left; text-transform: uppercase; }
.form-group input { width: 100%; padding: 1.1rem; background: #f8fafc; border: 2px solid #f1f5f9; border-radius: 8px; font-weight: 800; }
.form-group input:focus { border-color: #000; outline: none; }

.login-btn { width: 100%; padding: 1.1rem; background: #000; color: #fff; font-weight: 900; border-radius: 8px; border: none; cursor: pointer; transition: 0.2s; }

.seo-content { width: 100%; max-width: 1000px; margin-top: 4rem; padding-top: 4rem; border-top: 1px solid rgba(255,255,255,0.05); }
.seo-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 3rem; text-align: left; }
.seo-item h3 { font-size: 1rem; font-weight: 900; color: #fff; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px; }
.seo-item p { font-size: 0.9rem; line-height: 1.6; color: rgba(255,255,255,0.5); font-weight: 500; }

.landing-footer { margin-top: 8rem; color: rgba(255,255,255,0.25); font-size: 0.75rem; font-weight: 700; text-align: center; }

@media (max-width: 640px) {
  .roles-container { grid-template-columns: 1fr; gap: 1rem; }
  .premium-card { min-height: 100px; padding: 1.5rem; }
  .landing-header h1 { font-size: 2.2rem; }
  .top-banner { padding: 1.5rem; }
  .login-card { padding: 2rem; }
}

.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.4s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateY(20px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-20px); }
</style>
