<template>
  <div class="page-etudiants">
    <header class="page-header">
      <div class="header-content">
        <h2>Gestion des Étudiants</h2>
        <p>Gérez les élèves inscrits en Licence Professionnelle ASUR.</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-secondary">
          <span class="icon">📥</span> Importer (Excel)
        </button>
        <button class="btn btn-primary" @click="openModal('add')">
          <span class="icon">➕</span> Ajouter un Étudiant
        </button>
      </div>
    </header>

    <div class="table-container">
      <div v-if="pending" class="loader-container">
        <div class="spinner"></div>
        <p>Chargement des étudiants...</p>
      </div>
      <DataTable 
        v-else
        title="Liste de la Promotion" 
        :columns="columns" 
        :data="students" 
        :actions="true"
      >
        <template #status="{ row }">
          <span :class="['badge', row.status === 'Inscrit' ? 'badge-success' : 'badge-warning']">
            {{ row.status || 'Inscrit' }}
          </span>
        </template>
        <template #rowActions="{ row }">
          <button class="action-btn view-btn" @click="openModal('view', row)" title="Voir le profil">👁️</button>
          <button class="action-btn edit-btn" @click="openModal('edit', row)" title="Modifier">✏️</button>
          <button class="action-btn delete-btn" @click="confirmDelete(row)" title="Supprimer">🗑️</button>
        </template>
      </DataTable>
    </div>

    <!-- Modal Étudiant -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <header class="modal-header">
          <h3>{{ modalMode === 'add' ? 'Ajouter un Étudiant' : modalMode === 'edit' ? 'Modifier l\'Étudiant' : 'Fiche Étudiant' }}</h3>
          <button class="close-btn" @click="closeModal">&times;</button>
        </header>
        
        <form @submit.prevent="saveStudent" class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Nom</label>
              <input v-model="form.nom" required :disabled="modalMode === 'view'" placeholder="Mouk" />
            </div>
            <div class="form-group">
              <label>Prénom</label>
              <input v-model="form.prenom" required :disabled="modalMode === 'view'" placeholder="Brady" />
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" v-model="form.email" required :disabled="modalMode === 'view'" placeholder="brady.mouk@example.com" />
            </div>
            <div class="form-group">
              <label>Matricule</label>
              <input v-model="form.matricule" required :disabled="modalMode === 'view'" placeholder="23ASUR001" />
            </div>
            <div class="form-group">
              <label>Date de Naissance</label>
              <input type="date" v-model="form.date_naissance" required :disabled="modalMode === 'view'" />
            </div>
            <div class="form-group">
              <label>Lieu de Naissance</label>
              <input v-model="form.lieu_naissance" required :disabled="modalMode === 'view'" placeholder="Libreville" />
            </div>
            <div class="form-group">
              <label>Baccalauréat</label>
              <input v-model="form.bac" required :disabled="modalMode === 'view'" placeholder="L1, L2, C, D ..." />
            </div>
            <div class="form-group">
              <label>Provenance</label>
              <input v-model="form.provenance" required :disabled="modalMode === 'view'" placeholder="Lycée Technique" />
            </div>
          </div>
          
          <footer class="modal-footer" v-if="modalMode !== 'view'">
            <button type="button" class="btn btn-secondary" @click="closeModal">Annuler</button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              {{ saving ? 'Enregistrement...' : 'Enregistrer' }}
            </button>
          </footer>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

useHead({ title: 'Étudiants | LP ASUR' })

const { fetchApi } = useApi()
const students = ref([])
const pending = ref(true)
const saving = ref(false)

const columns = [
  { key: 'matricule', label: 'Matricule' },
  { key: 'nom', label: 'Nom' },
  { key: 'prenom', label: 'Prénom' },
  { key: 'email', label: 'Email' },
  { key: 'bac', label: 'Baccalauréat' },
  { key: 'provenance', label: 'Étab. Provenance' }
]

// Modal State
const showModal = ref(false)
const modalMode = ref('view') // 'add' | 'edit' | 'view'
const form = ref({
  id: '',
  nom: '',
  prenom: '',
  email: '',
  matricule: '',
  date_naissance: '',
  lieu_naissance: '',
  bac: '',
  provenance: '',
  status: 'Inscrit'
})

const fetchStudents = async () => {
  pending.value = true
  try {
    const data = await fetchApi('/etudiants/')
    if (data) students.value = data
  } catch (e) {
    console.error('Fetch failed', e)
  } finally {
    pending.value = false
  }
}

onMounted(fetchStudents)

const openModal = (mode, student = null) => {
  modalMode.value = mode
  if (student) {
    form.value = { ...student }
  } else {
    form.value = { id: '', nom: '', prenom: '', email: '', matricule: '', date_naissance: '', lieu_naissance: '', bac: '', provenance: '', status: 'Inscrit' }
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveStudent = async () => {
  saving.value = true
  try {
    const method = modalMode.value === 'add' ? 'POST' : 'PATCH'
    const url = modalMode.value === 'add' ? '/etudiants/' : `/etudiants/${form.value.id}/`
    
    await fetchApi(url, {
      method,
      body: form.value
    })
    
    await fetchStudents()
    closeModal()
  } catch (e) {
    console.error('Erreur lors de l\'enregistrement', e)
    alert(e.data?.error || 'Erreur lors de l\'enregistrement')
  } finally {
    saving.value = false
  }
}

const confirmDelete = async (student) => {
  if (confirm(`Êtes-vous sûr de vouloir supprimer l'étudiant ${student.nom}?`)) {
    try {
      await fetchApi(`/etudiants/${student.id}/`, { method: 'DELETE' })
      await fetchStudents()
    } catch (e) {
      console.error('Erreur lors de la suppression', e)
      alert('Erreur lors de la suppression')
    }
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
}

.header-content h2 {
  font-size: 1.75rem;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.header-content p {
  color: var(--text-muted);
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.6rem 1.25rem;
  border-radius: var(--radius);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn .icon {
  margin-right: 0.5rem;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
}

.btn-primary:hover {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
}

.btn-secondary {
  background-color: white;
  color: var(--text-main);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  background-color: #f8fafc;
}

.table-container {
  margin-top: 1rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-block;
}

.badge-success {
  background-color: rgba(16, 185, 129, 0.1);
  color: var(--success);
}

.badge-warning {
  background-color: rgba(245, 158, 11, 0.1);
  color: var(--warning);
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  opacity: 0.7;
  transition: opacity 0.2s;
  padding: 0 0.25rem;
}

.action-btn:hover { opacity: 1; transform: scale(1.1); }

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}
.modal-content {
  background: white;
  width: 100%;
  max-width: 600px;
  border-radius: var(--radius);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}
.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8fafc;
}
.modal-header h3 { margin: 0; color: #000080; font-size: 1.25rem; }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-muted); }

.modal-body { padding: 1.5rem; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-group { display: flex; flex-direction: column; gap: 0.5rem; }
.form-group label { font-weight: 600; font-size: 0.9rem; color: var(--text-main); }
.form-group input { padding: 0.6rem; border: 1px solid var(--border); border-radius: 4px; font-size: 0.95rem; }
.form-group input:focus { border-color: var(--primary); outline: none; box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1); }
.form-group input:disabled { background-color: #f1f5f9; cursor: not-allowed; }

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background-color: #f8fafc;
}

.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4rem;
  color: var(--text-muted);
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
