<template>
  <div class="page-profil">
    <header class="page-header">
      <div class="header-content">
        <h1>Mon Profil</h1>
        <p>Gérez vos informations personnelles et vos paramètres de sécurité.</p>
      </div>
    </header>

    <div class="profil-grid">
      <!-- Section Identité -->
      <div class="profil-main premium-card">
        <div class="profile-hero">
          <div class="avatar-large">{{ roleChar }}</div>
          <div class="hero-text">
            <h2>{{ userFullName || 'Utilisateur' }}</h2>
            <span class="role-tag">{{ currentRole.toUpperCase() }}</span>
          </div>
        </div>

        <div class="details-rows">
          <div class="detail-item">
            <label>Adresse E-mail</label>
            <div class="val">{{ userEmail }}</div>
          </div>
          <div class="detail-item">
            <label>Identifiant unique</label>
            <div class="val font-mono">#{{ userId || '---' }}</div>
          </div>
          <div class="detail-item" v-if="currentRole === 'etudiant'">
            <label>Matricule</label>
            <div class="val font-bold">{{ userMatricule || 'Non renseigné' }}</div>
          </div>
        </div>
      </div>

      <!-- Section Sécurité / Actions -->
      <div class="profil-side">
        <div class="premium-card darker-section">
          <h3>Sécurité du compte</h3>
          <p class="description">Protégez votre compte en modifiant régulièrement votre mot de passe.</p>
          <button class="btn btn-outline-white full-width" @click="openPasswordModal">
            Modifier le mot de passe
          </button>
        </div>

        <div class="premium-card mt-2">
          <h3>Préférences</h3>
          <div class="preferences-list">
            <label class="switch-item">
              <span>Notifications Email</span>
              <input type="checkbox" checked disabled>
              <div class="slider"></div>
            </label>
            <label class="switch-item">
              <span>Thème Sombre</span>
              <input type="checkbox" disabled>
              <div class="slider"></div>
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Changement de Passe (Simple UI) -->
    <Transition name="modal-bounce">
      <div v-if="showModal" class="modal-overlay" @click="showModal = false">
        <div class="modal-content premium-card" @click.stop>
          <div class="modal-header-premium">
            <span class="pulsar"></span>
            <h3>Sécurité</h3>
          </div>
          <div class="modal-body">
            <p>Pour modifier votre mot de passe, veuillez contacter l'administrateur système ou le secrétariat pédagogique.</p>
            <div class="info-box">
              Les modifications de sécurité sont actuellement restreintes pour garantir l'intégrité académique.
            </div>
          </div>
          <div class="form-actions-premium">
            <button class="btn btn-primary btn-pill" @click="showModal = false">Compris</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

useHead({ title: 'Profil | Bull ASUR' })

const currentRole = useCookie('authRole', { default: () => 'etudiant' })
const userEmail = useCookie('authEmail')
const userFullName = useCookie('authFullName')
const userId = useCookie('authId')
const userMatricule = useCookie('authMatricule')

const roleChar = computed(() => currentRole.value.charAt(0).toUpperCase())
const showModal = ref(false)

const openPasswordModal = () => {
  showModal.value = true
}
</script>

<style scoped>
.page-profil { padding: clamp(1.5rem, 4vw, 4rem) 2rem; max-width: 1200px; margin: 0 auto; animation: slideUp 0.6s ease-out; }

@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.page-header { margin-bottom: 4rem; }
.page-header h1 { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 950; letter-spacing: -3px; line-height: 1; margin-bottom: 0.5rem; }
.page-header p { color: #64748b; font-weight: 600; font-size: 1.1rem; }

.profil-grid { display: grid; grid-template-columns: 1fr 380px; gap: 2.5rem; }

.profil-main { padding: 4rem; background: #fff; }
.profile-hero { display: flex; align-items: center; gap: 3rem; margin-bottom: 4rem; padding-bottom: 4rem; border-bottom: 1px solid #f1f5f9; }
.avatar-large { width: 120px; height: 120px; background: #000; color: #fff; font-size: 4rem; font-weight: 950; display: flex; align-items: center; justify-content: center; border-radius: 32px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
.hero-text h2 { font-size: 2.5rem; font-weight: 950; letter-spacing: -1.5px; margin-bottom: 0.5rem; }
.role-tag { padding: 0.5rem 1.25rem; background: #f1f5f9; color: #000; border-radius: 50px; font-weight: 900; font-size: 0.75rem; letter-spacing: 1px; }

.details-rows { display: flex; flex-direction: column; gap: 2rem; }
.detail-item label { display: block; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1.5px; margin-bottom: 0.75rem; }
.detail-item .val { font-size: 1.25rem; font-weight: 800; color: #000; }
.font-mono { font-family: monospace; opacity: 0.6; }
.font-bold { color: #000; }

.profil-side { display: flex; flex-direction: column; gap: 2rem; }
.darker-section { background: #000; color: #fff; padding: 3rem; border: none; }
.darker-section h3 { font-size: 1.4rem; font-weight: 900; margin-bottom: 1rem; }
.darker-section .description { font-size: 0.9rem; opacity: 0.7; margin-bottom: 2.5rem; }

.preferences-list { display: flex; flex-direction: column; gap: 1.5rem; }
.switch-item { display: flex; justify-content: space-between; align-items: center; opacity: 0.5; cursor: not-allowed; }
.switch-item span { font-weight: 800; font-size: 0.95rem; }

.btn-outline-white { background: transparent; border: 2px solid rgba(255,255,255,0.3); color: #fff; padding: 1rem; border-radius: 12px; font-weight: 900; cursor: pointer; transition: all 0.2s; }
.btn-outline-white:hover { border-color: #fff; background: rgba(255,255,255,0.1); }
.full-width { width: 100%; }

.modal-body { padding: 3rem; text-align: center; }
.info-box { margin-top: 2rem; padding: 1.5rem; background: #f8fafc; border-radius: 12px; font-size: 0.85rem; font-weight: 700; color: #64748b; border: 1px solid #f1f5f9; }

.mt-2 { margin-top: 2rem; }

@media (max-width: 1024px) {
  .profil-grid { grid-template-columns: 1fr; }
  .profil-main { padding: 2.5rem; }
}
</style>
