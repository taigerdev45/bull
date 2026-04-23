<template>
  <div class="students-module">
    <!-- Header Page -->
    <header class="module-header">
      <div class="title-section">
        <h1>Gestion Administrative des Étudiants</h1>
        <p>Registre centralisé de la promotion ASUR</p>
      </div>
      <div class="actions-section">
        <button class="btn btn-primary" @click="handleCreate">
          <span class="icon">➕</span> Nouvel Étudiant
        </button>
      </div>
    </header>

    <!-- Stats Dashboard -->
    <section class="stats-overview">
      <div v-for="stat in stats" :key="stat.label" class="stat-item">
        <span class="stat-label">{{ stat.label }}</span>
        <span class="stat-value">{{ stat.value }}</span>
      </div>
    </section>

    <!-- Data Table Section -->
    <section class="data-section">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Synchronisation avec le serveur...</p>
      </div>

      <div v-else class="table-container">
        <UiDataTable
          title="Registre des Étudiants"
          :columns="headers"
          :data="students"
          :actions="true"
        >
          <!-- Custom Slots for Table Cells -->
          <template #status="{ row }">
            <span :class="['status-chip', row.status?.toLowerCase()]">
              {{ row.status || 'Inscrit' }}
            </span>
          </template>

          <template #rowActions="{ row }">
            <div class="row-actions">
              <button class="icon-btn" title="Voir détails" @click="handleView(row)">👁️</button>
              <button class="icon-btn edit" title="Modifier" @click="handleEdit(row)">✏️</button>
              <button class="icon-btn delete" title="Supprimer" @click="handleDelete(row)">🗑️</button>
            </div>
          </template>
        </UiDataTable>
      </div>
    </section>

    <!-- Modal Form (Unified for Create/Edit/View) -->
    <Transition name="modal-fade">
      <div v-if="modal.show" class="modal-backdrop" @click.self="closeModal">
        <div class="modal-box">
          <header class="modal-header">
            <h3>{{ modal.title }}</h3>
            <button class="close-x" @click="closeModal">&times;</button>
          </header>

          <form @submit.prevent="handleSubmit" class="modal-form">
            <div class="form-grid">
              <div class="form-group">
                <label>Nom</label>
                <input v-model="form.nom" required :disabled="modal.mode === 'view'" placeholder="Nom de famille" />
              </div>

              <div class="form-group">
                <label>Prénom</label>
                <input v-model="form.prenom" required :disabled="modal.mode === 'view'" placeholder="Prénom(s)" />
              </div>

              <div class="form-group">
                <label>Email</label>
                <input type="email" v-model="form.email" required :disabled="modal.mode === 'view'" placeholder="email@univ.ga" />
              </div>

              <div class="form-group">
                <label>Matricule ASUR</label>
                <input v-model="form.matricule" required :disabled="modal.mode === 'view'" placeholder="Ex: 23ASUR001" />
              </div>

              <!-- Mot de passe : affiché uniquement lors de la création -->
              <div v-if="modal.mode === 'add'" class="form-group full-width">
                <label>Mot de passe provisoire <span class="hint">(crée le compte de connexion de l'étudiant)</span></label>
                <input type="password" v-model="form.password" required :disabled="modal.mode === 'view'" placeholder="Min. 8 caractères" autocomplete="new-password" minlength="8" />
              </div>

              <div class="form-group">
                <label>Date de Naissance</label>
                <input type="date" v-model="form.date_naissance" required :disabled="modal.mode === 'view'" />
              </div>

              <div class="form-group">
                <label>Lieu de Naissance</label>
                <input v-model="form.lieu_naissance" required :disabled="modal.mode === 'view'" placeholder="Ville" />
              </div>

              <div class="form-group">
                <label>Série Baccalauréat</label>
                <input v-model="form.bac" required :disabled="modal.mode === 'view'" placeholder="Ex: S, C, D..." />
              </div>

              <div class="form-group">
                <label>Établissement d'Origine</label>
                <input v-model="form.provenance" required :disabled="modal.mode === 'view'" placeholder="Lycée de provenance" />
              </div>

              <div class="form-group full-width">
                <label>Statut Administratif</label>
                <select v-model="form.status" :disabled="modal.mode === 'view'">
                  <option value="Inscrit">Inscrit</option>
                  <option value="Boursier">Boursier</option>
                  <option value="Exclu">Exclu</option>
                  <option value="Suspendu">Suspendu</option>
                </select>
              </div>
            </div>

            <footer class="form-footer" v-if="modal.mode !== 'view'">
              <button type="button" class="btn btn-alt" @click="closeModal">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                {{ submitting ? 'Enregistrement...' : 'Enregistrer les informations' }}
              </button>
            </footer>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'
import UiDataTable from '~/components/ui/DataTable.vue'

useHead({ title: 'Étudiants | Bull' })

const { fetchApi } = useApi()

// Logic State
const students = ref([])
const loading = ref(true)
const submitting = ref(false)

const headers = [
  { key: 'matricule', label: 'Matricule' },
  { key: 'nom', label: 'Nom' },
  { key: 'prenom', label: 'Prénom' },
  { key: 'email', label: 'Email' },
  { key: 'bac', label: 'Série Bac' },
  { key: 'status', label: 'Statut' }
]

const stats = computed(() => [
  { label: 'Total Étudiants', value: students.value.length },
  { label: 'Inscrits Actifs', value: students.value.filter(s => s.status === 'Inscrit').length },
  { label: 'Détails Promotion', value: 'ASUR 2026' }
])

// Modal & Form State
const modal = reactive({
  show: false,
  mode: 'add',
  title: 'Nouvel Étudiant'
})

const defaultForm = {
  id: null,
  nom: '',
  prenom: '',
  email: '',
  matricule: '',
  password: '',
  date_naissance: '',
  lieu_naissance: '',
  bac: '',
  provenance: '',
  status: 'Inscrit'
}

const form = reactive({ ...defaultForm })

// API Actions
const loadData = async () => {
  loading.value = true
  try {
    const data = await fetchApi('/etudiants/')
    students.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error('Fetch error', err)
    students.value = []
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    const isEdit = modal.mode === 'edit'
    const method = isEdit ? 'PATCH' : 'POST'
    const endpoint = isEdit ? `/etudiants/${form.id}/` : '/etudiants/'

    // En édition on n'envoie pas le password
    const payload = { ...form }
    if (isEdit) delete payload.password
    if (!payload.password) delete payload.password  // Ne pas envoyer vide

    await fetchApi(endpoint, {
      method,
      body: payload
    })

    await loadData()
    closeModal()
  } catch (err) {
    console.error('Save error', err)
    const msg = err.data?.error || err.data?.message || 'Erreur lors de la sauvegarde. Vérifiez les champs.'
    alert(msg)
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (row) => {
  if (confirm(`Êtes-vous sûr de vouloir supprimer ${row.nom} ${row.prenom} de la base de données ?`)) {
    try {
      await fetchApi(`/etudiants/${row.id}/`, { method: 'DELETE' })
      await loadData()
    } catch (err) {
      alert('Erreur lors de la suppression.')
    }
  }
}

// UI Handlers
const closeModal = () => {
  modal.show = false
  Object.assign(form, defaultForm)
}

const handleCreate = () => {
  modal.mode = 'add'
  modal.title = 'Inscription Nouvel Étudiant'
  Object.assign(form, defaultForm)
  modal.show = true
}

const handleEdit = (row) => {
  modal.mode = 'edit'
  modal.title = `Modifier Profil : ${row.nom}`
  Object.assign(form, row)
  modal.show = true
}

const handleView = (row) => {
  modal.mode = 'view'
  modal.title = `Détails Étudiant : ${row.nom}`
  Object.assign(form, row)
  modal.show = true
}

onMounted(loadData)
</script>

<style scoped>
.students-module {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Header Section */
.module-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.title-section h1 {
  font-size: 1.75rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.5px;
}

.title-section p {
  color: #64748b;
  margin-top: 0.25rem;
}

/* Stats Overview */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.stat-item {
  background: white;
  padding: 1.25rem;
  border-radius: 12px;
  border: 1px solid #cbd5e1;
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
}

/* Table Section */
.data-section {
  background: white;
  border-radius: 16px;
  overflow: hidden;
}

.row-actions {
  display: flex;
  gap: 0.5rem;
}

.status-chip {
  padding: 0.25rem 0.75rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 700;
}

.status-chip.inscrit { background: #dcfce7; color: #166534; }
.status-chip.boursier { background: #dbeafe; color: #1e40af; }
.status-chip.exclu { background: #fee2e2; color: #991b1b; }

/* Modal & Backdrop */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.modal-box {
  background: white;
  width: 100%;
  max-width: 800px;
  border-radius: 20px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
}

.close-x {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #94a3b8;
}

.modal-form {
  padding: 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full-width {
  grid-column: span 2;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
}

.form-group input, .form-group select {
  padding: 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.form-group input:focus, .form-group select:focus {
  border-color: #3b82f6;
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-footer {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* Buttons */
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary { background: #3b82f6; color: white; }
.btn-primary:hover { background: #2563eb; }
.btn-alt { background: #f1f5f9; color: #475569; }

.icon-btn {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  height: 32px;
  width: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.icon-btn:hover { background: white; border-color: #3b82f6; color: #3b82f6; }
.icon-btn.delete:hover { border-color: #ef4444; color: #ef4444; }

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 5rem;
  color: #64748b;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f1f5f9;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Transitions */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

/* Password hint label */
.hint { font-weight: 400; font-size: 0.78rem; color: #94a3b8; margin-left: 0.25rem; }
</style>
