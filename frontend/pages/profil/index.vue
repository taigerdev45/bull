<template>
  <div class="page-container">
    <div class="profil-layout">
      <!-- Left Side: Profile Summary -->
      <div class="card side-profile">
        <div class="avatar-box">
          <div class="avatar-large" :style="{ backgroundColor: avatarColor }">{{ initial }}</div>
          <button class="edit-avatar">📷</button>
        </div>
        <div class="side-info">
          <h3>{{ fullName }}</h3>
          <span class="role-chip">{{ currentRole.toUpperCase() }}</span>
        </div>
        <div class="side-stats">
          <div class="s-stat">
            <strong>2026</strong>
            <span>Année LP</span>
          </div>
          <div class="s-stat">
             <strong>ASUR</strong>
             <span>Spécialité</span>
          </div>
        </div>
      </div>

      <!-- Right Side: Details Form -->
      <div class="card main-profile">
        <header class="section-header">
          <h3>Informations Personnelles</h3>
          <p>Mettez à jour vos informations de contact.</p>
        </header>

        <form @submit.prevent="updateProfile" class="profile-form">
          <div class="form-grid">
            <div class="field">
              <label>Nom complet</label>
              <input type="text" v-model="fullName" placeholder="Ex: Jean Dupont" />
            </div>
            <div class="field">
              <label>Email Professionnel</label>
              <input type="email" v-model="email" disabled />
              <small>L'email est géré par l'administration.</small>
            </div>
            <div class="field">
               <label>Téléphone</label>
               <input type="tel" v-model="phone" placeholder="+241 ..." />
            </div>
          </div>

          <div class="divider"></div>

          <header class="section-header">
            <h3>Sécurité</h3>
            <p>Changez votre mot de passe régulièrement pour sécuriser votre accès.</p>
          </header>

          <div class="form-grid">
            <div class="field">
              <label>Mot de passe actuel</label>
              <input type="password" v-model="pass.current" placeholder="••••••••" />
            </div>
            <div class="field">
              <label>Nouveau mot de passe</label>
              <input type="password" v-model="pass.new" placeholder="••••••••" />
            </div>
          </div>

          <div class="form-footer">
            <button type="submit" class="btn btn-primary" :disabled="saving">
              {{ saving ? 'Enregistrement...' : 'Mettre à jour mon profil' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

useHead({ title: 'Profil | Bull ASUR' })

const currentRole = useCookie('authRole', { default: () => 'etudiant' })
const fullName = useCookie('authFullName', { default: () => 'Administrateur Principal' })
const email = useCookie('authEmail', { default: () => 'taigermboumba@gmail.com' })
const phone = ref('+241 07 00 00 00')
const saving = ref(false)
const pass = ref({ current: '', new: '' })

const initial = computed(() => fullName.value ? fullName.value.charAt(0).toUpperCase() : 'A')
const avatarColor = computed(() => '#2563eb')

const updateProfile = async () => {
  saving.value = true
  setTimeout(() => {
    saving.value = false
    alert('Profil mis à jour avec succès !')
  }, 1000)
}
</script>

<style scoped>
.profil-layout { display: grid; grid-template-columns: 320px 1fr; gap: 2rem; align-items: flex-start; }

.card { background: white; border-radius: var(--radius-lg); border: 1px solid var(--border-light); box-shadow: var(--shadow-sm); overflow: hidden; }

.side-profile { padding: 3rem 1.5rem; display: flex; flex-direction: column; align-items: center; text-align: center; }

.avatar-box { position: relative; margin-bottom: 1.5rem; }
.avatar-large { width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: 800; color: white; border: 4px solid white; box-shadow: var(--shadow-md); }
.edit-avatar { position: absolute; bottom: 0; right: 0; background: white; border: 1px solid var(--border-light); border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: var(--shadow-sm); }

.side-info h3 { font-size: 1.25rem; font-weight: 700; color: #0f172a; margin-bottom: 0.5rem; }
.role-chip { background: #f1f5f9; color: #475569; font-size: 0.75rem; font-weight: 700; padding: 0.35rem 1rem; border-radius: 99px; }

.side-stats { width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; border-top: 1px solid #f1f5f9; margin-top: 2rem; padding-top: 2rem; }
.s-stat { display: flex; flex-direction: column; gap: 0.25rem; }
.s-stat strong { font-size: 1rem; color: #0f172a; }
.s-stat span { font-size: 0.75rem; color: #94a3b8; font-weight: 500; }

.main-profile { padding: 2.5rem; }
.section-header { margin-bottom: 2rem; }
.section-header h3 { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin: 0; }
.section-header p { font-size: 0.85rem; color: #64748b; margin-top: 0.25rem; }

.divider { height: 1px; background: #f1f5f9; margin: 2rem 0; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.field { display: flex; flex-direction: column; gap: 0.5rem; }
.field label { font-size: 0.85rem; font-weight: 600; color: #475569; }
.field input { padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.95rem; width: 100%; transition: all 0.2s; }
.field input:focus { border-color: var(--primary); outline: none; box-shadow: 0 0 0 4px var(--primary-glow); }
.field input:disabled { background: #f8fafc; color: #94a3b8; cursor: not-allowed; }
.field small { font-size: 0.75rem; color: #94a3b8; }

.form-footer { margin-top: 2.5rem; display: flex; justify-content: flex-end; }
.btn-primary { padding: 0.8rem 2rem; border-radius: 8px; background: var(--primary); color: white; font-weight: 700; cursor: pointer; border: none; box-shadow: 0 4px 12px var(--primary-glow); transition: all 0.2s; }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 16px var(--primary-glow); }

@media (max-width: 900px) {
  .profil-layout { grid-template-columns: 1fr; }
}
</style>
