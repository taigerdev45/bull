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
      <div class="profil-main premium-card shadow-soft">
        <div class="profile-hero">
          <div class="avatar-large">{{ roleChar }}</div>
          <div class="hero-text">
            <h2>{{ profileData.name || 'Utilisateur' }}</h2>
            <div class="hero-badges">
              <span class="role-tag" :class="currentRole">{{ currentRole.toUpperCase() }}</span>
              <span v-if="profileData.email" class="email-badge">{{ profileData.email }}</span>
            </div>
          </div>
          <button v-if="!isEditing" @click="isEditing = true" class="btn-edit-toggle">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            Modifier
          </button>
        </div>

        <form @submit.prevent="saveProfile" class="details-rows">
          <div class="detail-item" :class="{ 'is-editing': isEditing }">
            <label>Nom complet</label>
            <div v-if="!isEditing" class="val">{{ profileData.name || 'Non renseigné' }}</div>
            <input v-else type="text" v-model="tempData.name" class="input-premium" placeholder="Votre nom complet" required />
          </div>

          <div class="detail-item">
            <label>Adresse E-mail</label>
            <div class="val disabled-val">{{ profileData.email }}</div>
            <p class="input-hint" v-if="isEditing">L'adresse email ne peut pas être modifiée pour des raisons de sécurité.</p>
          </div>

          <div class="detail-item">
            <label>Identifiant unique (UID)</label>
            <div class="val font-mono disabled-val">#{{ profileData.id || '---' }}</div>
          </div>

          <div class="detail-item" v-if="currentRole === 'etudiant'">
            <label>Matricule Académique</label>
            <div class="val font-bold disabled-val">{{ userMatricule || 'Non disponible' }}</div>
          </div>

          <transition name="fade">
            <div v-if="isEditing" class="edit-actions">
              <button type="button" @click="cancelEdit" class="btn btn-ghost" :disabled="saving">Annuler</button>
              <button type="submit" class="btn btn-primary btn-save" :disabled="saving">
                <span v-if="!saving">Enregistrer les modifications</span>
                <span v-else class="loader-small"></span>
              </button>
            </div>
          </transition>
        </form>
      </div>

      <!-- Section Sécurité / Actions -->
      <div class="profil-side">
        <div class="premium-card darker-section shadow-heavy">
          <div class="side-header">
            <div class="side-icon-box">🔐</div>
            <h3>Sécurité</h3>
          </div>
          <p class="description">Maintenez la sécurité de votre compte en mettant à jour votre accès.</p>
          <button class="btn btn-outline-white full-width" @click="openPasswordModal">
            Modifier le mot de passe
          </button>
        </div>

        <div class="premium-card preferences-card shadow-soft">
          <div class="side-header">
            <div class="side-icon-box">🎨</div>
            <h3>Préférences</h3>
          </div>
          <div class="preferences-list">
            <label class="switch-item">
              <div class="switch-info">
                <span class="sw-title">Notifications Email</span>
                <span class="sw-desc">Recevoir mes relevés par mail</span>
              </div>
              <div class="switch-wrapper">
                <input type="checkbox" checked disabled>
                <div class="slider"></div>
              </div>
            </label>
            <label class="switch-item">
              <div class="switch-info">
                <span class="sw-title">Thème Sombre</span>
                <span class="sw-desc">Désactiver le mode clair</span>
              </div>
              <div class="switch-wrapper">
                <input type="checkbox" disabled>
                <div class="slider"></div>
              </div>
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Changement de Passe (Premium Design) -->
    <Transition name="modal-bounce">
      <div v-if="showModal" class="modal-overlay" @click="showModal = false">
        <div class="modal-content-premium glass-morphism" @click.stop>
          <div class="modal-header-p">
            <div class="pulsar"></div>
            <h3>Mise à jour de sécurité</h3>
          </div>
          <div class="modal-body-p">
            <div class="warning-large">⚠️</div>
            <p>Conformément à la politique de l'INPTIC, les modifications de mot de passe sont restreintes.</p>
            <div class="info-box-premium">
              <p>Veuillez contacter le <strong>Secrétariat Académique</strong> ou l'<strong>Administrateur</strong> pour toute réinitialisation d'accès.</p>
            </div>
          </div>
          <div class="modal-footer-p">
            <button class="btn btn-dark full-width" @click="showModal = false">Compris</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

useHead({ title: 'Profil | Bull ASUR' })

const { fetchApi } = useApi()

const currentRole = useCookie('authRole', { default: () => 'etudiant' })
const userMatricule = useCookie('authMatricule')

const profileData = ref({
  id: '',
  email: '',
  name: '',
  role: ''
})

const tempData = ref({ name: '' })
const isEditing = ref(false)
const saving = ref(false)
const showModal = ref(false)

const roleChar = computed(() => (profileData.value.name || '?').charAt(0).toUpperCase())

const loadProfile = async () => {
  try {
    const data = await fetchApi('/auth/me/')
    if (data) {
      profileData.value = {
        id: data.id,
        email: data.email,
        name: data.name || useCookie('authFullName').value,
        role: data.role
      }
      tempData.value.name = profileData.value.name
    }
  } catch (e) {
    console.error("Erreur lors du chargement du profil", e)
  }
}

const saveProfile = async () => {
  if (saving.value) return
  saving.value = true
  try {
    const res = await fetchApi('/auth/me/', {
      method: 'PATCH',
      body: { name: tempData.value.name }
    })
    profileData.value.name = res.name
    useCookie('authFullName').value = res.name
    isEditing.value = false
    alert("Profil mis à jour !")
  } catch (e) {
    alert("Erreur lors de la mise à jour")
  } finally {
    saving.value = false
  }
}

const cancelEdit = () => {
  tempData.value.name = profileData.value.name
  isEditing.value = false
}

const openPasswordModal = () => {
  showModal.value = true
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.page-profil { padding: clamp(1.5rem, 4vw, 4rem) 2rem; max-width: 1300px; margin: 0 auto; animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

.page-header { margin-bottom: 4rem; }
.page-header h1 { font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 950; letter-spacing: -3px; line-height: 1; margin-bottom: 0.75rem; }
.page-header p { color: #64748b; font-weight: 600; font-size: 1.1rem; }

.profil-grid { display: grid; grid-template-columns: 1fr 420px; gap: 3rem; }

.profil-main { padding: 4rem; background: #fff; border-radius: 32px; border: 1px solid #f1f5f9; position: relative; }
.shadow-soft { box-shadow: 0 10px 40px rgba(0,0,0,0.02); }

.profile-hero { display: flex; align-items: flex-start; gap: 3rem; margin-bottom: 5rem; padding-bottom: 4rem; border-bottom: 1px solid #f1f5f9; position: relative; }
.avatar-large { width: 140px; height: 140px; background: #000; color: #fff; font-size: 5rem; font-weight: 950; display: flex; align-items: center; justify-content: center; border-radius: 40px; box-shadow: 0 30px 60px rgba(0,0,0,0.15); transform: rotate(-3deg); }

.hero-text h2 { font-size: 3rem; font-weight: 950; letter-spacing: -2px; margin-bottom: 1rem; color: #000; }
.hero-badges { display: flex; gap: 1rem; align-items: center; }
.role-tag { padding: 0.6rem 1.5rem; background: #f1f5f9; color: #000; border-radius: 50px; font-weight: 950; font-size: 0.7rem; letter-spacing: 2px; }
.role-tag.admin { background: #fee2e2; color: #ef4444; }
.email-badge { color: #94a3b8; font-weight: 700; font-size: 0.9rem; }

.btn-edit-toggle { position: absolute; right: 0; top: 0; background: #f8fafc; border: none; padding: 0.75rem 1.5rem; border-radius: 12px; font-weight: 900; color: #000; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; transition: 0.3s; }
.btn-edit-toggle:hover { background: #000; color: #fff; }

.details-rows { max-width: 600px; }
.detail-item { margin-bottom: 3rem; transition: 0.3s; }
.detail-item.is-editing { padding-left: 1.5rem; border-left: 4px solid #000; }
.detail-item label { display: block; font-size: 0.75rem; font-weight: 950; text-transform: uppercase; color: #94a3b8; letter-spacing: 2px; margin-bottom: 1rem; }
.detail-item .val { font-size: 1.5rem; font-weight: 800; color: #000; line-height: 1.2; }
.disabled-val { opacity: 0.4; }

.input-premium { width: 100%; padding: 1.2rem; background: #f8fafc; border: 2.5px solid #f1f5f9; border-radius: 16px; font-size: 1.25rem; font-weight: 800; color: #000; transition: 0.3s; }
.input-premium:focus { outline: none; border-color: #000; background: #fff; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
.input-hint { font-size: 0.8rem; color: #94a3b8; margin-top: 0.75rem; font-weight: 700; }

.edit-actions { margin-top: 4rem; display: flex; gap: 1.5rem; align-items: center; }
.btn-save { background: #000; color: #fff; padding: 1.2rem 2.5rem; border-radius: 18px; font-weight: 950; border: none; cursor: pointer; flex: 1; transition: 0.3s; }
.btn-save:hover { transform: scale(1.02); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
.btn-ghost { background: transparent; border: none; color: #94a3b8; font-weight: 900; cursor: pointer; padding: 0 1rem; }

/* Sidebar */
.profil-side { display: flex; flex-direction: column; gap: 2.5rem; }
.darker-section { background: #000; color: #fff; padding: 3.5rem; border: none; border-radius: 32px; }
.shadow-heavy { box-shadow: 0 40px 100px rgba(0,0,0,0.15); }

.side-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; }
.side-icon-box { font-size: 1.5rem; }
.side-header h3 { font-size: 1.6rem; font-weight: 950; letter-spacing: -1px; }

.darker-section .description { font-size: 1rem; opacity: 0.6; line-height: 1.6; font-weight: 600; margin-bottom: 3rem; }

.preferences-card { background: #fff; border: 1px solid #f1f5f9; border-radius: 32px; padding: 3rem; }
.preferences-list { display: flex; flex-direction: column; gap: 2rem; }

.switch-item { display: flex; justify-content: space-between; align-items: center; }
.sw-title { display: block; font-weight: 900; font-size: 1rem; color: #000; margin-bottom: 0.25rem; }
.sw-desc { display: block; font-size: 0.8rem; color: #94a3b8; font-weight: 700; }

.switch-wrapper { width: 50px; height: 26px; position: relative; opacity: 0.3; cursor: not-allowed; }
.switch-wrapper input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: #f1f5f9; border-radius: 34px; border: 2px solid #e2e8f0; }
.slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 2px; bottom: 2px; background-color: #94a3b8; border-radius: 50%; }

.btn-outline-white { background: transparent; border: 2px solid rgba(255,255,255,0.2); color: #fff; padding: 1.25rem; border-radius: 16px; font-weight: 950; cursor: pointer; transition: 0.3s; }
.btn-outline-white:hover { border-color: #fff; background: #fff; color: #000; }
.full-width { width: 100%; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 2rem; }
.modal-content-premium { background: #fff; width: 100%; max-width: 500px; border-radius: 40px; padding: 4rem; text-align: center; }

.warning-large { font-size: 4rem; margin-bottom: 2rem; }
.modal-header-p h3 { font-size: 1.8rem; font-weight: 950; margin-bottom: 1.5rem; letter-spacing: -1px; }
.modal-body-p p { font-size: 1.1rem; color: #1e293b; font-weight: 600; line-height: 1.5; margin-bottom: 2rem; }

.info-box-premium { background: #f1f5f9; padding: 2rem; border-radius: 24px; color: #475569; font-size: 0.95rem; font-weight: 600; }
.info-box-premium strong { color: #000; }

.modal-footer-p { margin-top: 3rem; }
.btn-dark { background: #000; color: #fff; border: none; padding: 1.25rem; border-radius: 16px; font-weight: 950; cursor: pointer; }

@media (max-width: 1024px) {
  .profil-grid { grid-template-columns: 1fr; }
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
