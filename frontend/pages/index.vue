<template>
  <div class="landing-page" @mousemove="handleMouseMove">
    <!-- Overlay Effet Spatial : "Ballon" de Particules -->
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

    <!-- PWA Install Prompt (Fixed) -->
    <client-only>
      <div v-if="installPrompt" class="install-card-fixed premium-card">
        <p>Installer Bull ASUR sur votre appareil ?</p>
        <div class="actions">
          <button @click="installApp" class="btn-install">Installer</button>
          <button @click="installPrompt = null" class="btn-dismiss">Plus tard</button>
        </div>
      </div>
    </client-only>

    <div class="content-wrapper">
      <header class="landing-header">
        <div class="main-logo-container">
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
              <p>Profil & Résultats</p>
            </div>
          </div>

          <div @click="selectRole('enseignant')" class="premium-card enseignant-border">
            <div class="card-content">
              <h2>Enseignant</h2>
              <p>Saisie & Matières</p>
            </div>
          </div>

          <div @click="selectRole('secretariat')" class="premium-card secretariat-border">
            <div class="card-content">
              <h2>Secrétariat</h2>
              <p>Administration</p>
            </div>
          </div>

          <div @click="selectRole('admin')" class="premium-card admin-border">
            <div class="card-content">
              <h2>Admin</h2>
              <p>Maintenance</p>
            </div>
          </div>
        </div>

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

      <!-- SEO Content in Cards -->
      <section class="seo-content">
        <div class="seo-grid">
          <article class="seo-card-premium">
            <div class="card-body-seo">
              <h3>ASUR Excellence</h3>
              <p>Le système Bull ASUR est le moteur de gestion académique de l'INPTIC, spécialisé pour la Licence ASUR au Gabon.</p>
            </div>
          </article>
          <article class="seo-card-premium">
            <div class="card-body-seo">
              <h3>Digitalisation INPTIC</h3>
              <p>Transition numérique complète pour la gestion des bulletins de notes et délibérations scolaires en temps réel.</p>
            </div>
          </article>
          <article class="seo-card-premium">
            <div class="card-body-seo">
              <h3>Standard SaaS Premium</h3>
              <p>Une expérience utilisateur haut de gamme combinant sécurité réseau et ergonomie moderne pour l'éducation.</p>
            </div>
          </article>
        </div>
      </section>

      <footer class="landing-footer">
        <p>&copy; 2026 INPTIC - Bull ASUR</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

definePageMeta({ layout: 'empty' })

const router = useRouter(); const { fetchApi } = useApi()

// PWA Install Logic
const installPrompt = ref(null)
onMounted(() => {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault()
    installPrompt.value = e
  })
})
const installApp = async () => {
  if (!installPrompt.value) return
  installPrompt.value.prompt()
  const { outcome } = await installPrompt.value.userChoice
  if (outcome === 'accepted') installPrompt.value = null
}

// Bubble Animation Logic (Antigravity Magnetic Ball)
const bubbleCanvas = ref(null)
let ctx = null; let particles = []
const bubbleCount = 90
const mouse = { x: -100, y: -100 }

class Particle {
  constructor() {
    this.reset()
  }
  reset() {
    this.x = Math.random() * window.innerWidth
    this.y = Math.random() * window.innerHeight
    this.size = Math.random() * 2 + 0.5
    this.baseX = this.x
    this.baseY = this.y
    this.density = (Math.random() * 25) + 5
    this.friction = 0.96
    this.vx = 0; this.vy = 0
    this.color = "rgba(255, 255, 255, " + (Math.random() * 0.4 + 0.2) + ")"
  }
  update() {
    let dx = mouse.x - this.x
    let dy = mouse.y - this.y
    let distance = Math.sqrt(dx * dx + dy * dy)
    let forceDirectionX = dx / distance
    let forceDirectionY = dy / distance
    
    // Antigravity ball formation
    const radius = 45 
    let force = (radius - distance) / radius
    
    if (distance < radius) {
      this.vx += forceDirectionX * force * 2
      this.vy += forceDirectionY * force * 2
    } else {
      this.vx += (mouse.x - this.x) / this.density
      this.vy += (mouse.y - this.y) / this.density
    }

    this.vx *= this.friction; this.vy *= this.friction
    this.x += this.vx; this.y += this.vy
  }
  draw() {
    ctx.fillStyle = this.color
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
    ctx.fill()
  }
}

const handleMouseMove = (e) => {
  mouse.x = e.clientX; mouse.y = e.clientY
}

const animate = () => {
  if (!ctx || !bubbleCanvas.value) return
  ctx.clearRect(0, 0, bubbleCanvas.value.width, bubbleCanvas.value.height)
  particles.forEach(p => { p.update(); p.draw() })
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

const selectedRole = ref(null); const showLoginForm = ref(false)
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
  } catch (e) { alert("Accès refusé") } finally { loading.value = false }
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

.roles-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; width: 100%; max-width: 1100px; margin-bottom: 6rem; }
.premium-card { background: rgba(255,255,255,0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 2.5rem 1.5rem; text-align: center; color: white; cursor: pointer; transition: all 0.3s; min-height: 120px; display: flex; align-items: center; justify-content: center; }
.premium-card:hover { background: #fff; color: #000; transform: translateY(-5px); border-color: #fff; }
.premium-card h2 { font-size: 1.3rem; font-weight: 900; margin-bottom: 0.25rem; }
.premium-card p { font-size: 0.75rem; opacity: 0.6; font-weight: 700; text-transform: uppercase; }

.login-card { background: #fff; color: #000; padding: 3rem; border-radius: 20px; width: 100%; max-width: 450px; box-shadow: 0 40px 80px rgba(0,0,0,0.5); }
.back-btn { background: transparent; border: none; font-weight: 800; color: #94a3b8; cursor: pointer; margin-bottom: 1.5rem; padding: 0; }
.role-badge { padding: 0.4rem 0.8rem; background: #000; color: #fff; border-radius: 4px; font-size: 0.65rem; font-weight: 950; text-transform: uppercase; margin-bottom: 1rem; display: inline-block; }

/* SEO Cards Modern */
.seo-content { width: 100%; max-width: 1200px; margin-top: 4rem; padding-top: 4rem; border-top: 1px solid rgba(255,255,255,0.1); }
.seo-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
.seo-card-premium { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 2.5rem; transition: all 0.3s; }
.seo-card-premium:hover { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.2); }
.seo-card-premium h3 { font-size: 1.1rem; font-weight: 900; color: #fff; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px; }
.seo-card-premium p { font-size: 0.9rem; line-height: 1.6; color: rgba(255,255,255,0.6); font-weight: 500; }

.landing-footer { margin-top: 8rem; color: rgba(255,255,255,0.25); font-size: 0.75rem; font-weight: 700; text-align: center; }

/* Fixed Install Prompt */
.install-card-fixed { position: fixed; bottom: 2rem; left: 2rem; z-index: 1000; background: #fff; color: #000; padding: 1.5rem 2rem; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.4); display: flex; flex-direction: column; gap: 1rem; border: none; min-height: auto; }
.install-card-fixed p { font-weight: 800; font-size: 0.9rem; }
.install-card-fixed .actions { display: flex; gap: 1rem; }
.btn-install { background: #000; color: #fff; border: none; padding: 0.6rem 1.2rem; border-radius: 10px; font-weight: 800; cursor: pointer; }
.btn-dismiss { background: #f1f5f9; color: #64748b; border: none; padding: 0.6rem 1.2rem; border-radius: 10px; font-weight: 800; cursor: pointer; }

@media (max-width: 640px) {
  .roles-container { grid-template-columns: 1fr; gap: 1rem; }
  .premium-card { min-height: 100px; padding: 1.5rem; }
  .landing-header h1 { font-size: 2.2rem; }
  .top-banner { padding: 1.5rem; }
  .install-card-fixed { left: 1rem; right: 1rem; bottom: 1rem; }
}

.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.4s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateY(20px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-20px); }
</style>
