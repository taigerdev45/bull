<template>
  <div class="page-profil">
    <header class="page-header">
      <h2>Mon Profil</h2>
      <p>Gérez vos informations personnelles et préférences de connexion.</p>
    </header>

    <div class="profil-card">
      <div class="profil-header">
        <div class="avatar-large">{{ initial }}</div>
        <div class="profil-main-info">
          <h3>{{ fullName }}</h3>
          <p class="role-badge">{{ currentRole.toUpperCase() }}</p>
        </div>
      </div>

      <form class="profil-form" @submit.prevent>
        <div class="form-group">
          <label>Identifiant (Prénom)</label>
          <input type="text" :value="username" disabled />
        </div>
        <div class="form-group">
          <label>Adresse Email</label>
          <input type="email" :value="email" disabled />
        </div>
        
        <div class="form-group mt-2">
          <h4>Changer le mot de passe</h4>
          <div class="form-row">
            <input type="password" placeholder="Mot de passe actuel" />
            <input type="password" placeholder="Nouveau mot de passe" />
          </div>
        </div>
        
        <div class="actions">
          <button type="submit" class="btn btn-primary">Enregistrer les modifications</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

useHead({ title: 'Profil | Bull ASUR' })

const route = useRoute()

// Lecture globale du rôle et des informations utilisateur
const currentRole = useCookie('authRole', { default: () => 'etudiant' })
const username = useCookie('authUsername', { default: () => 'Yannick' })
const email = useCookie('authEmail', { default: () => 'yannick.mba@inptic.ga' })
const fullName = useCookie('authFullName', { default: () => 'MBA NSOME Yannick Lionel' })

const initial = computed(() => fullName.value.charAt(0).toUpperCase() || 'U')
</script>

<style scoped>
.page-header { margin-bottom: 2rem; }
.page-header h2 { font-size: 1.75rem; color: var(--text-main); font-weight: 700; margin-bottom: 0.25rem; }
.page-header p { color: var(--text-muted); }

.profil-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 2rem; max-width: 700px; box-shadow: var(--shadow); }

.profil-header { display: flex; align-items: center; gap: 1.5rem; margin-bottom: 2.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border); }
.avatar-large { width: 80px; height: 80px; background: var(--primary); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: bold; }
.profil-main-info h3 { font-size: 1.5rem; margin-bottom: 0.25rem; color: var(--text-main); }
.role-badge { display: inline-block; background: var(--theme-dark); color: white; padding: 0.2rem 0.75rem; border-radius: 99px; font-size: 0.8rem; font-weight: 600; }

.profil-form .form-group { margin-bottom: 1.5rem; }
.profil-form label { display: block; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-main); }
.profil-form input { width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: var(--radius); outline: none; }
.profil-form input:focus { border-color: var(--primary); }
.profil-form input:disabled { background-color: #f1f5f9; color: var(--text-muted); cursor: not-allowed; }

.form-group h4 { font-size: 1.1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1rem; color: var(--text-main); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

.actions { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid var(--border); text-align: right; }
.btn { padding: 0.75rem 1.5rem; border: none; border-radius: var(--radius); cursor: pointer; font-weight: 600; font-family: inherit; transition: background 0.2s; }
.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: var(--primary-hover); }

@media (max-width: 600px) {
  .form-row { grid-template-columns: 1fr; }
}
</style>
