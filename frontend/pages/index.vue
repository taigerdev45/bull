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

    <!-- PWA Install Prompt -->
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
          <div @click="selectRole('etudiant')" class="premium-card role-card etudiant-border">
            <div class="card-content">
              <h2>Étudiant</h2>
              <p>Profil & Résultats</p>
            </div>
          </div>

          <div @click="selectRole('enseignant')" class="premium-card role-card enseignant-border">
            <div class="card-content">
              <h2>Enseignant</h2>
              <p>Saisie & Matières</p>
            </div>
          </div>

          <div @click="selectRole('secretariat')" class="premium-card role-card secretariat-border">
            <div class="card-content">
              <h2>Secrétariat</h2>
              <p>Administration</p>
            </div>
          </div>

          <div @click="selectRole('admin')" class="premium-card role-card admin-border">
            <div class="card-content">
              <h2>Admin</h2>
              <p>Maintenance</p>
            </div>
          </div>
        </div>

        <!-- FORMULAIRE DE CONNEXION PREMIUM -->
        <div v-else key="login" class="login-container">
          <div class="login-card-premium glass-morphism">
            <div class="login-header-p">
              <button class="back-link" @click="showLoginForm = false">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="3"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                Changer de rôle
              </button>
              <div class="badge-container">
                <span class="role-chip" :class="selectedRole">{{ roleTitle }}</span>
              </div>
              <h2>Identification</h2>
              <p class="login-desc">Veuillez renseigner vos identifiants pour accéder à votre espace de travail.</p>
            </div>
            
            <form class="login-form-p" @submit.prevent="handleLogin">
              <div class="input-group-p">
                <label>Identifiant Académique</label>
                <div class="input-wrapper">
                  <span class="i-icon"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
                  <input type="email" v-model="username" placeholder="votre.nom@inptic.ga" required autocomplete="email" />
                </div>
              </div>
              
              <div class="input-group-p">
                <label>Mot de passe</label>
                <div class="input-wrapper">
                  <span class="i-icon"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg></span>
                  <input type="password" v-model="password" placeholder="••••••••" required autocomplete="current-password" />
                </div>
              </div>
              
              <div class="form-footer-p">
                <button type="submit" class="submit-btn-p" :disabled="loading">
                  <div class="btn-shine"></div>
                  <span v-if="!loading">Accéder au Système</span>
                  <div v-else class="loader-p"></div>
                </button>
                <a href="#" class="forgot-link">Problème de connexion ?</a>
              </div>
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
        <p>&copy; 2026 INPTIC - Bull ASUR v2.5</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

definePageMeta({ layout: 'empty' })

const router = useRouter(); const { fetchApi } = useApi()

// PWA Install Logic
const installPrompt = ref(null)
onMounted(() => {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault(); installPrompt.value = e
  })
})
const installApp = async () => {
  if (!installPrompt.value) return
  installPrompt.value.prompt()
  const { outcome } = await installPrompt.value.userChoice
  if (outcome === 'accepted') installPrompt.value = null
}

// Bubble Animation Logic
const bubbleCanvas = ref(null)
let ctx = null; let particles = []; let animationFrame = null
const bubbleCount = 60
const mouse = { x: -100, y: -100 }

class Particle {
  constructor() { this.reset() }
  reset() {
    this.x = Math.random() * window.innerWidth; this.y = Math.random() * window.innerHeight
    this.size = Math.random() * 2 + 0.5; this.density = (Math.random() * 25) + 5
    this.friction = 0.96; this.vx = 0; this.vy = 0
    this.color = "rgba(255, 255, 255, " + (Math.random() * 0.4 + 0.2) + ")"
  }
  update() {
    let dx = mouse.x - this.x; let dy = mouse.y - this.y
    let distance = Math.sqrt(dx * dx + dy * dy) || 1
    let forceDirectionX = dx / distance; let forceDirectionY = dy / distance
    const radius = 45; let force = (radius - distance) / radius
    if (distance < radius) { this.vx += forceDirectionX * force * 2; this.vy += forceDirectionY * force * 2 }
    else { this.vx += (mouse.x - this.x) / this.density; this.vy += (mouse.y - this.y) / this.density }
    this.vx *= this.friction; this.vy *= this.friction; this.x += this.vx; this.y += this.vy
  }
  draw() { ctx.fillStyle = this.color; ctx.beginPath(); ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2); ctx.fill() }
}

const handleMouseMove = (e) => { mouse.x = e.clientX; mouse.y = e.clientY }
const animate = () => {
  if (!ctx || !bubbleCanvas.value) return
  ctx.clearRect(0, 0, bubbleCanvas.value.width, bubbleCanvas.value.height)
  particles.forEach(p => { p.update(); p.draw() })
  animationFrame = requestAnimationFrame(animate)
}

const resizeCanvas = () => {
  if (bubbleCanvas.value) {
    bubbleCanvas.value.width = window.innerWidth
    bubbleCanvas.value.height = window.innerHeight
  }
}

onMounted(() => {
  if (bubbleCanvas.value) {
    resizeCanvas()
    ctx = bubbleCanvas.value.getContext('2d')
    for (let i = 0; i < bubbleCount; i++) particles.push(new Particle())
    animate()
  }
  window.addEventListener('resize', resizeCanvas)
})

onBeforeUnmount(() => {
  if (animationFrame) cancelAnimationFrame(animationFrame)
  window.removeEventListener('resize', resizeCanvas)
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
  } catch (e) { alert("Accès refusé - Veuillez vérifier vos identifiants") } finally { loading.value = false }
}
</script>

<style scoped>
.landing-page { position: relative; min-height: 100vh; width: 100%; display: flex; flex-direction: column; background-image: url('~/assets/images/acceuil_bull.jpeg'); background-size: cover; background-position: center; overflow: hidden; font-family: 'Inter', sans-serif; }
.bubble-layer { position: absolute; inset: 0; z-index: 2; pointer-events: none; }
.overlay { position: absolute; inset: 0; background: radial-gradient(circle at center, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.7) 100%); backdrop-filter: blur(2px); z-index: 1; }

.top-banner { position: relative; z-index: 10; display: flex; justify-content: space-between; padding: 2rem 4rem; color: white; font-size: 0.7rem; font-weight: 800; }
.separator { width: 40px; height: 3px; background: #fff; margin-top: 8px; }

.content-wrapper { position: relative; z-index: 5; flex: 1; display: flex; flex-direction: column; align-items: center; padding: 4rem 2rem; }
.content-wrapper::-webkit-scrollbar { display: none; }

.landing-header { text-align: center; margin-bottom: 4rem; }
.landing-logo { height: 140px; filter: drop-shadow(0 0 20px rgba(255,255,255,0.2)); margin-bottom: 2rem; position: relative; z-index: 10; }
.landing-header h1 { font-size: clamp(2.5rem, 8vw, 4.5rem); font-weight: 950; letter-spacing: -3px; color: #fff; line-height: 1; margin-bottom: 1rem; }
.subtitle { font-size: 1rem; color: rgba(255,255,255,0.7); font-weight: 600; text-transform: uppercase; letter-spacing: 2px; }

/* Role Cards */
.roles-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; width: 100%; max-width: 1100px; margin-bottom: 6rem; }
.role-card { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 2.5rem 1.5rem; text-align: center; color: white; cursor: pointer; transition: all 0.4s cubic-bezier(0.2, 1, 0.3, 1); min-height: 160px; display: flex; align-items: center; justify-content: center; }
.role-card:hover { background: #fff; color: #000; transform: translateY(-10px) scale(1.02); box-shadow: 0 40px 100px rgba(0,0,0,0.5); }
.role-icon { font-size: 2.5rem; margin-bottom: 1rem; }
.role-card h2 { font-size: 1.4rem; font-weight: 950; margin-bottom: 0.25rem; }
.role-card p { font-size: 0.75rem; opacity: 0.6; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }

/* FORMULAIRE DE CONNEXION PREMIUM */
.login-container { width: 100%; display: flex; justify-content: center; margin-bottom: 6rem; }
.login-card-premium { background: rgba(255,255,255,0.95); backdrop-filter: blur(40px); color: #000; padding: 3.5rem; border-radius: 32px; width: 100%; max-width: 500px; box-shadow: 0 60px 120px rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.2); position: relative; overflow: hidden; }

.back-link { background: #000; color: #fff; border: none; font-weight: 900; font-size: 0.75rem; cursor: pointer; margin-bottom: 2.5rem; padding: 0.6rem 1.2rem; border-radius: 50px; display: flex; align-items: center; gap: 0.5rem; transition: 0.3s; }
.back-link:hover { transform: translateX(-5px); opacity: 0.8; }

.login-header-p { text-align: left; margin-bottom: 2.5rem; }
.badge-container { margin-bottom: 1rem; }
.role-chip { padding: 0.5rem 1.5rem; border-radius: 50px; font-size: 0.7rem; font-weight: 950; text-transform: uppercase; letter-spacing: 2px; background: #f1f5f9; color: #64748b; }
.role-chip.admin { background: #fee2e2; color: #ef4444; }
.role-chip.etudiant { background: #dcfce7; color: #16a34a; }
.role-chip.enseignant { background: #e0f2fe; color: #0284c7; }
.role-chip.secretariat { background: #fef9c3; color: #ca8a04; }

.login-header-p h2 { font-size: 2.2rem; font-weight: 950; letter-spacing: -1px; margin-bottom: 0.5rem; }
.login-desc { color: #64748b; font-size: 0.95rem; line-height: 1.5; font-weight: 600; }

.input-group-p { margin-bottom: 1.8rem; }
.input-group-p label { display: block; font-size: 0.8rem; font-weight: 950; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.75rem; letter-spacing: 1px; }
.input-wrapper { position: relative; display: flex; align-items: center; }
.input-wrapper .i-icon { position: absolute; left: 1.25rem; color: #cbd5e1; transition: 0.3s; }
.input-wrapper input { width: 100%; padding: 1.25rem 1.25rem 1.25rem 3.5rem; background: #f8fafc; border: 2.5px solid #f1f5f9; border-radius: 18px; font-weight: 800; font-size: 1rem; color: #000; transition: all 0.3s; }
.input-wrapper input:focus { border-color: #000; outline: none; background: #fff; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
.input-wrapper input:focus + .i-icon { color: #000; }

.form-footer-p { margin-top: 3rem; }
.submit-btn-p { width: 100%; padding: 1.4rem; background: #000; color: #fff; font-weight: 950; border-radius: 20px; border: none; cursor: pointer; position: relative; overflow: hidden; font-size: 1.1rem; transition: 0.3s; }
.submit-btn-p:hover { transform: scale(1.02); box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
.btn-shine { position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent); transform: rotate(45deg); animation: shine 3s infinite; }
@keyframes shine { 0% { left: -100%; } 100% { left: 100%; } }

.forgot-link { display: block; text-align: center; margin-top: 1.5rem; font-size: 0.85rem; font-weight: 900; color: #94a3b8; text-decoration: none; transition: 0.3s; }
.forgot-link:hover { color: #000; }

.loader-p { width: 24px; height: 24px; border: 4px solid rgba(255,255,255,0.2); border-top-color: #fff; border-radius: 50%; margin: 0 auto; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* SEO Cards */
.seo-content { width: 100%; max-width: 1200px; margin-top: 4rem; padding-top: 4rem; border-top: 1px solid rgba(255,255,255,0.1); }
.seo-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
.seo-card-premium { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 2.5rem; transition: all 0.3s; }
.seo-card-premium:hover { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.2); }
.seo-card-premium h3 { font-size: 1.1rem; font-weight: 950; color: #fff; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px; }
.seo-card-premium p { font-size: 0.9rem; line-height: 1.6; color: rgba(255,255,255,0.6); font-weight: 600; }

.landing-footer { margin-top: 8rem; color: rgba(255,255,255,0.25); font-size: 0.75rem; font-weight: 800; text-align: center; }

/* Install Prompt */
.install-card-fixed { position: fixed; bottom: 2rem; left: 2rem; z-index: 1000; background: #fff; color: #000; padding: 1.5rem 2rem; border-radius: 20px; box-shadow: 0 40px 80px rgba(0,0,0,0.5); display: flex; flex-direction: column; gap: 1rem; }
.install-card-fixed p { font-weight: 900; font-size: 0.9rem; }
.btn-install { background: #000; color: #fff; border: none; padding: 0.6rem 1.2rem; border-radius: 12px; font-weight: 950; cursor: pointer; }
.btn-dismiss { background: #f1f5f9; color: #64748b; border: none; padding: 0.6rem 1.2rem; border-radius: 12px; font-weight: 950; cursor: pointer; }

@media (max-width: 640px) {
  .top-banner { padding: 1.5rem 2rem; flex-direction: column; align-items: center; gap: 0.5rem; text-align: center; }
  .separator { margin: 4px auto 0; }
  
  .content-wrapper { padding: 2rem 1.5rem; }
  .landing-header { margin-bottom: 2.5rem; }
  .landing-logo { height: 90px; margin-bottom: 1.5rem; }
  .landing-header h1 { font-size: 2.5rem; letter-spacing: -1.5px; }
  .subtitle { font-size: 0.8rem; letter-spacing: 1px; }

  .roles-container { grid-template-columns: 1fr; gap: 1rem; margin-bottom: 4rem; }
  .role-card { padding: 2rem 1.5rem; min-height: 120px; }
  
  .login-card-premium { padding: 2.5rem 1.5rem; border-radius: 24px; }
  .login-header-p h2 { font-size: 1.8rem; }
  .submit-btn-p { padding: 1.2rem; font-size: 1rem; }
  
  .seo-grid { grid-template-columns: 1fr; gap: 1rem; }
  .seo-card-premium { padding: 1.5rem; }
  
  .install-card-fixed { left: 1rem; right: 1rem; bottom: 1rem; align-items: center; text-align: center; }
}

.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
.fade-slide-enter-from { opacity: 0; transform: translateY(30px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-30px); }
</style>
