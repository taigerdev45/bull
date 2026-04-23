<template>
  <div class="page-container">
    <!-- Header -->
    <header class="module-header">
      <div class="title-section">
        <h1>Gestion du Personnel</h1>
        <p>Créez et gérez les comptes Secrétariat et Enseignants.</p>
      </div>
      <div class="actions-section">
        <button class="btn btn-primary" @click="openCreate">
          <span class="icon">➕</span> Nouveau Membre
        </button>
      </div>
    </header>

    <!-- Stats rapides -->
    <section class="stats-row">
      <div class="stat-card" v-for="s in stats" :key="s.label">
        <span class="stat-icon">{{ s.icon }}</span>
        <div class="stat-body">
          <span class="stat-value">{{ s.value }}</span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
      </div>
    </section>

    <!-- Filtres -->
    <div class="filter-bar">
      <input v-model="search" type="search" placeholder="Rechercher par nom, email..." class="search-input" />
      <select v-model="filterRole" class="role-filter">
        <option value="">Tous les rôles</option>
        <option value="admin">Admin</option>
        <option value="secretariat">Secrétariat</option>
        <option value="enseignant">Enseignant</option>
      </select>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div v-if="loading" class="loader-row">
        <div class="spinner"></div>
        <span>Chargement du personnel...</span>
      </div>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Nom Complet</th>
            <th>Email</th>
            <th>Rôle</th>
            <th>Téléphone</th>
            <th>Compte Auth</th>
            <th class="th-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filtered.length === 0">
            <td colspan="6" class="empty-row">Aucun membre trouvé.</td>
          </tr>
          <tr v-for="p in filtered" :key="p.id">
            <td class="td-name">
              <div class="avatar">{{ initials(p) }}</div>
              <span>{{ p.prenom }} {{ p.nom }}</span>
            </td>
            <td class="td-email">{{ p.email }}</td>
            <td><span :class="['role-badge', p.role]">{{ roleLabel(p.role) }}</span></td>
            <td>{{ p.numero_telephone || '—' }}</td>
            <td>
              <span :class="['auth-badge', p.user_id ? 'active' : 'none']">
                {{ p.user_id ? '✅ Actif' : '❌ Aucun' }}
              </span>
            </td>
            <td class="td-actions">
              <button class="icon-btn delete" title="Supprimer" @click="confirmDelete(p)">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ─── Modal Création ──────────────────────────────────────── -->
    <Transition name="modal-fade">
      <div v-if="modal.show" class="modal-overlay" @click.self="modal.show = false">
        <div class="modal-box">
          <div class="modal-header">
            <h2>Nouveau Membre du Personnel</h2>
            <button class="modal-close" @click="modal.show = false">✕</button>
          </div>

          <form class="modal-form" @submit.prevent="handleSubmit">
            <div class="form-grid">
              <div class="form-group">
                <label>Nom</label>
                <input v-model="form.nom" required placeholder="Ex: DIALLO" autocomplete="family-name" />
              </div>
              <div class="form-group">
                <label>Prénom</label>
                <input v-model="form.prenom" required placeholder="Ex: Aminata" autocomplete="given-name" />
              </div>
              <div class="form-group full-width">
                <label>Email</label>
                <input v-model="form.email" type="email" required placeholder="email@univ.ga" autocomplete="email" />
              </div>
              <div class="form-group">
                <label>Rôle</label>
                <select v-model="form.role" required>
                  <option value="">-- Choisir un rôle --</option>
                  <option value="secretariat">Secrétariat</option>
                  <option value="enseignant">Enseignant</option>
                  <option value="admin">Administrateur</option>
                </select>
              </div>
              <div class="form-group">
                <label>Téléphone (optionnel)</label>
                <input v-model="form.numero_telephone" type="tel" placeholder="+241 07 XX XX XX" autocomplete="tel" />
              </div>
              <div class="form-group full-width">
                <label>
                  Mot de passe provisoire
                  <span class="hint">(crée le compte de connexion)</span>
                </label>
                <input v-model="form.password" type="password" required minlength="8" placeholder="Min. 8 caractères" autocomplete="new-password" />
              </div>
            </div>

            <div v-if="errorMsg" class="form-error">⚠️ {{ errorMsg }}</div>

            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" @click="modal.show = false">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                {{ submitting ? 'Création en cours...' : '✅ Créer le compte' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useApi } from '~/composables/useApi'

useHead({ title: 'Personnel | Bull ASUR' })

const { fetchApi } = useApi()

const personnel = ref([])
const loading = ref(true)
const submitting = ref(false)
const search = ref('')
const filterRole = ref('')
const errorMsg = ref('')

const modal = reactive({ show: false })
const defaultForm = { nom: '', prenom: '', email: '', role: '', password: '', numero_telephone: '' }
const form = reactive({ ...defaultForm })

// ─── Stats ────────────────────────────────────────────────────────
const stats = computed(() => [
  { icon: '👥', label: 'Total Personnel', value: personnel.value.length },
  { icon: '🏫', label: 'Secrétariat', value: personnel.value.filter(p => p.role === 'secretariat').length },
  { icon: '🎓', label: 'Enseignants', value: personnel.value.filter(p => p.role === 'enseignant').length },
  { icon: '🔑', label: 'Administrateurs', value: personnel.value.filter(p => p.role === 'admin').length },
])

// ─── Filtrage ─────────────────────────────────────────────────────
const filtered = computed(() => {
  return personnel.value.filter(p => {
    const matchSearch = !search.value ||
      `${p.nom} ${p.prenom} ${p.email}`.toLowerCase().includes(search.value.toLowerCase())
    const matchRole = !filterRole.value || p.role === filterRole.value
    return matchSearch && matchRole
  })
})

// ─── Data ─────────────────────────────────────────────────────────
const loadData = async () => {
  loading.value = true
  try {
    const data = await fetchApi('/personnel/')
    personnel.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error('Fetch personnel error', err)
    personnel.value = []
  } finally {
    loading.value = false
  }
}

onMounted(loadData)

// ─── Helpers ──────────────────────────────────────────────────────
const initials = (p) => `${p.prenom?.[0] || ''}${p.nom?.[0] || ''}`.toUpperCase()

const roleLabel = (role) => ({
  admin: 'Admin',
  secretariat: 'Secrétariat',
  enseignant: 'Enseignant',
  super_admin: 'Super Admin'
}[role] || role)

// ─── Actions ──────────────────────────────────────────────────────
const openCreate = () => {
  Object.assign(form, defaultForm)
  errorMsg.value = ''
  modal.show = true
}

const handleSubmit = async () => {
  submitting.value = true
  errorMsg.value = ''
  try {
    await fetchApi('/personnel/', {
      method: 'POST',
      body: { ...form }
    })
    modal.show = false
    await loadData()
  } catch (err) {
    errorMsg.value = err.data?.error || err.data?.message || 'Erreur lors de la création du compte.'
  } finally {
    submitting.value = false
  }
}

const confirmDelete = async (p) => {
  if (!confirm(`Supprimer ${p.prenom} ${p.nom} ? Cette action est irréversible.`)) return
  try {
    await fetchApi(`/personnel/${p.id}/`, { method: 'DELETE' })
    await loadData()
  } catch (err) {
    alert(err.data?.error || 'Impossible de supprimer.')
  }
}
</script>

<style scoped>
/* Header */
.module-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; }
.title-section h1 { font-size: 1.75rem; font-weight: 800; color: #1e293b; margin: 0; }
.title-section p { color: #64748b; font-size: 1rem; margin: 0.25rem 0 0; }
.actions-section { display: flex; gap: 0.75rem; }

/* Stats */
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.stat-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem 1.5rem; display: flex; align-items: center; gap: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.stat-icon { font-size: 1.75rem; }
.stat-body { display: flex; flex-direction: column; }
.stat-value { font-size: 1.5rem; font-weight: 800; color: #0f172a; line-height: 1; }
.stat-label { font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; margin-top: 0.2rem; }

/* Filters */
.filter-bar { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.search-input { flex: 1; padding: 0.75rem 1rem; border: 1.5px solid #e2e8f0; border-radius: 10px; font-size: 0.95rem; color: #334155; outline: none; background: white; }
.search-input:focus { border-color: #6366f1; }
.role-filter { padding: 0.75rem 1rem; border: 1.5px solid #e2e8f0; border-radius: 10px; font-weight: 600; color: #334155; background: white; outline: none; }

/* Table */
.table-card { background: white; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 1px 6px rgba(0,0,0,0.04); }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th { padding: 1rem 1.25rem; text-align: left; font-size: 0.65rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.7px; border-bottom: 1px solid #f1f5f9; background: #fafafa; }
.data-table td { padding: 1rem 1.25rem; border-bottom: 1px solid #f8fafc; font-size: 0.9rem; }
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: #fafcff; }
.th-actions { text-align: right; }
.td-actions { text-align: right; }

.td-name { display: flex; align-items: center; gap: 0.75rem; font-weight: 600; color: #1e293b; }
.avatar { width: 32px; height: 32px; background: linear-gradient(135deg,#6366f1,#8b5cf6); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.7rem; font-weight: 800; flex-shrink: 0; }
.td-email { color: #64748b; font-size: 0.85rem; }

.role-badge { padding: 0.3rem 0.75rem; border-radius: 999px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; }
.role-badge.secretariat { background: #f0fdf4; color: #166534; }
.role-badge.enseignant { background: #eff6ff; color: #1d4ed8; }
.role-badge.admin, .role-badge.super_admin { background: #fef3c7; color: #92400e; }

.auth-badge { font-size: 0.8rem; font-weight: 600; }
.auth-badge.active { color: #16a34a; }
.auth-badge.none { color: #dc2626; }

.icon-btn { background: none; border: none; cursor: pointer; padding: 0.3rem; opacity: 0.4; transition: opacity 0.2s; font-size: 1rem; }
.icon-btn:hover { opacity: 1; }
.empty-row { text-align: center; color: #94a3b8; padding: 3rem; font-style: italic; }

.loader-row { display: flex; align-items: center; gap: 1rem; padding: 2rem 1.5rem; color: #64748b; }
.spinner { width: 24px; height: 24px; border: 3px solid #f1f5f9; border-top-color: #6366f1; border-radius: 50%; animation: spin 1s linear infinite; flex-shrink: 0; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Buttons */
.btn { padding: 0.7rem 1.25rem; border-radius: 10px; font-weight: 700; font-size: 0.9rem; cursor: pointer; border: none; display: flex; align-items: center; gap: 0.5rem; transition: all 0.2s; }
.btn-primary { background: #6366f1; color: white; box-shadow: 0 4px 12px rgba(99,102,241,0.3); }
.btn-primary:hover { background: #4f46e5; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-ghost { background: #f1f5f9; color: #64748b; }
.btn-ghost:hover { background: #e2e8f0; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(15,23,42,0.55); display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 1rem; backdrop-filter: blur(4px); }
.modal-box { background: white; border-radius: 20px; width: 100%; max-width: 600px; box-shadow: 0 25px 50px rgba(0,0,0,0.25); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2rem; border-bottom: 1px solid #f1f5f9; }
.modal-header h2 { font-size: 1.2rem; font-weight: 800; color: #0f172a; margin: 0; }
.modal-close { background: none; border: none; font-size: 1.1rem; cursor: pointer; color: #94a3b8; }
.modal-form { padding: 1.5rem 2rem; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
.form-group { display: flex; flex-direction: column; gap: 0.5rem; }
.form-group.full-width { grid-column: 1 / -1; }
.form-group label { font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }
.form-group input, .form-group select { padding: 0.75rem 1rem; border: 1.5px solid #e2e8f0; border-radius: 9px; font-size: 0.95rem; font-weight: 500; color: #0f172a; background: #f8fafc; outline: none; transition: border-color 0.2s; }
.form-group input:focus, .form-group select:focus { border-color: #6366f1; background: white; }
.hint { font-weight: 400; font-size: 0.75rem; color: #94a3b8; margin-left: 0.25rem; text-transform: none; }
.form-error { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 0.75rem 1rem; border-radius: 8px; font-size: 0.9rem; margin-top: 1rem; }
.modal-footer { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #f1f5f9; }

.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.25s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

@media (max-width: 900px) {
  .stats-row { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
  .stats-row { grid-template-columns: 1fr; }
  .form-grid { grid-template-columns: 1fr; }
  .form-group.full-width { grid-column: 1; }
}
</style>
