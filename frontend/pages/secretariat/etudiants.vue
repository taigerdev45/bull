<template>
  <div class="page-etudiants">
    <header class="page-header">
      <div class="header-content">
        <h2>Gestion des Étudiants</h2>
        <p>Inscriptions, informations administratives et suivi académique.</p>
      </div>
      <div class="header-actions">
        <div class="export-dropdown" v-if="students.length">
          <button class="btn btn-secondary shadow-sm">
            Exporter
          </button>
          <div class="dropdown-menu">
            <button @click="exportData('excel')">Excel (.xlsx)</button>
            <button @click="exportData('pdf-p')">PDF Portrait</button>
            <button @click="exportData('pdf-l')">PDF Paysage</button>
          </div>
        </div>
        <button class="btn btn-primary" @click="openModal('add')">
          Ajouter un Étudiant
        </button>
      </div>
    </header>

    <!-- Filtres et recherche -->
    <div class="filters-section">
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchTerm" 
          placeholder="Rechercher par nom, prénom..."
          class="form-control"
        >
      </div>
      <div class="filter-options">
        <select v-model="filterBac" class="form-control">
          <option value="">Tous les bacs</option>
          <option value="S">Scientifique</option>
          <option value="ES">Économique et Social</option>
          <option value="L">Littéraire</option>
          <option value="STMG">STMG</option>
          <option value="STI2D">STI2D</option>
          <option value="Autre">Autre</option>
        </select>
      </div>
    </div>

    <!-- Tableau des étudiants -->
    <div class="table-container">
      <DataTable
        :columns="studentColumns"
        :data="filteredStudents"
        title="Liste des étudiants"
        :actions="true"
      >
        <template #actions="{ row }">
          <button class="btn btn-sm btn-secondary" @click="openModal('edit', row)">
            ✏️
          </button>
          <button class="btn btn-sm btn-danger" @click="deleteStudent(row.id)">
            🗑️
          </button>
        </template>
      </DataTable>
    </div>

    <!-- Modal d'ajout/modification -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalMode === 'add' ? 'Ajouter' : 'Modifier' }} un étudiant</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        
        <form @submit.prevent="saveStudent" class="modal-form">
          <div class="form-row">
            <div class="form-group">
              <label for="nom">Nom *</label>
              <input 
                type="text" 
                id="nom" 
                v-model="formData.nom" 
                required 
                class="form-control"
              >
            </div>
            <div class="form-group">
              <label for="prenom">Prénom *</label>
              <input 
                type="text" 
                id="prenom" 
                v-model="formData.prenom" 
                required 
                class="form-control"
              >
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="email">Email *</label>
              <input 
                type="email" 
                id="email" 
                v-model="formData.email" 
                required 
                class="form-control"
                placeholder="email@example.com"
              >
            </div>
            <div class="form-group">
              <label for="matricule">Matricule *</label>
              <input 
                type="text" 
                id="matricule" 
                v-model="formData.matricule" 
                required 
                class="form-control"
                placeholder="Ex: LPASUR001"
              >
            </div>
          </div>

          <div class="alert-info-credentials">
            <p><strong>Note :</strong> Les identifiants de connexion par défaut seront :</p>
            <ul>
              <li><strong>Identifiant :</strong> {{ formData.prenom || 'Prénom' }}</li>
              <li><strong>Mot de passe :</strong> {{ formData.matricule || 'Matricule' }}</li>
            </ul>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="date_naissance">Date de naissance *</label>
              <input 
                type="date" 
                id="date_naissance" 
                v-model="formData.date_naissance" 
                required 
                class="form-control"
              >
            </div>
            <div class="form-group">
              <label for="lieu_naissance">Lieu de naissance *</label>
              <input 
                type="text" 
                id="lieu_naissance" 
                v-model="formData.lieu_naissance" 
                required 
                class="form-control"
              >
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="bac">Type de Bac *</label>
              <select id="bac" v-model="formData.bac" required class="form-control">
                <option value="">Sélectionner...</option>
                <option value="S">Scientifique</option>
                <option value="ES">Économique et Social</option>
                <option value="L">Littéraire</option>
                <option value="STMG">STMG</option>
                <option value="STI2D">STI2D</option>
                <option value="Autre">Autre</option>
              </select>
            </div>
            <div class="form-group">
              <label for="provenance">Provenance *</label>
              <input 
                type="text" 
                id="provenance" 
                v-model="formData.provenance" 
                placeholder="Lycée d'origine"
                required 
                class="form-control"
              >
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="closeModal">
              Annuler
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Enregistrement...' : (modalMode === 'add' ? 'Ajouter' : 'Modifier') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

useHead({ title: 'Gestion des Étudiants | Bull ASUR' })

// État
const students = ref([])
const searchTerm = ref('')
const filterBac = ref('')
const showModal = ref(false)
const modalMode = ref('add') // 'add' ou 'edit'
const loading = ref(false)
const currentStudent = ref(null)

// Formulaire
const formData = ref({
  nom: '',
  prenom: '',
  email: '',
  matricule: '',
  date_naissance: '',
  lieu_naissance: '',
  bac: '',
  provenance: ''
})

// Colonnes du tableau
const studentColumns = [
  { key: 'nom', label: 'Nom' },
  { key: 'prenom', label: 'Prénom' },
  { key: 'matricule', label: 'Matricule' },
  { key: 'email', label: 'Email' },
  { key: 'date_naissance', label: 'Né(e) le' },
  { key: 'bac', label: 'Bac' }
]

// Filtrage
const filteredStudents = computed(() => {
  return students.value.filter(student => {
    const searchLower = searchTerm.value.toLowerCase()
    const matchesSearch = `${student.nom} ${student.prenom} ${student.matricule}`.toLowerCase().includes(searchLower)
    const matchesBac = !filterBac.value || student.bac === filterBac.value
    return matchesSearch && matchesBac
  })
})

const { fetchApi } = useApi()
const { exportToExcel, exportToPDF } = useExport()

// Méthodes
const exportData = (type) => {
  const data = students.value.map(s => ({
    Nom: s.nom,
    Prénom: s.prenom,
    Matricule: s.matricule,
    Email: s.email,
    'Date Naissance': s.date_naissance,
    'Lieu Naissance': s.lieu_naissance,
    Bac: s.bac,
    Provenance: s.provenance
  }))

  if (type === 'excel') {
    exportToExcel(data, 'liste_etudiants.xlsx')
  } else {
    const headers = ['Matricule', 'Nom', 'Prénom', 'Bac', 'Date Naiss.']
    const rows = students.value.map(s => [
      s.matricule, 
      s.nom, 
      s.prenom, 
      s.bac, 
      s.date_naissance
    ])
    exportToPDF(headers, rows, 'liste_etudiants.pdf', type === 'pdf-l' ? 'l' : 'p')
  }
}

const openModal = (mode, student = null) => {
  modalMode.value = mode
  currentStudent.value = student
  
  if (mode === 'edit' && student) {
    formData.value = { ...student }
  } else {
    resetForm()
  }
  
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  resetForm()
  currentStudent.value = null
}

const resetForm = () => {
  formData.value = {
    nom: '',
    prenom: '',
    email: '',
    matricule: '',
    date_naissance: '',
    lieu_naissance: '',
    bac: '',
    provenance: ''
  }
}

const loadStudents = async () => {
  try {
    const response = await fetchApi('/etudiants/')
    students.value = response
  } catch (error) {
    console.error('Erreur lors du chargement des étudiants', error)
  }
}

const saveStudent = async () => {
  loading.value = true
  
  try {
    const url = modalMode.value === 'add' 
      ? '/etudiants/'
      : `/etudiants/${currentStudent.value.id}/`
    
    const method = modalMode.value === 'add' ? 'POST' : 'PATCH'
    
    const response = await fetchApi(url, {
      method,
      body: formData.value
    })
    
    await loadStudents()
    closeModal()
    console.log('Étudiant enregistré avec succès via API')
    
  } catch (error) {
    console.error('Erreur lors de l\'enregistrement', error)
    alert(error.data?.error || "Erreur lors de l'enregistrement")
  } finally {
    loading.value = false
  }
}

const deleteStudent = async (studentId) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer cet étudiant ?')) {
    return
  }
  
  try {
    await fetchApi(`/etudiants/${studentId}/`, {
      method: 'DELETE'
    })
    
    await loadStudents()
    console.log('Étudiant supprimé avec succès')
    
  } catch (error) {
    console.error('Erreur lors de la suppression', error)
    alert("Erreur lors de la suppression")
  }
}

onMounted(() => {
  loadStudents()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.header-content h2 {
  font-size: 1.75rem;
  color: var(--text-main);
  margin-bottom: 0.25rem;
  font-weight: 700;
}

.header-content p {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.filters-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

.search-box {
  flex: 1;
}

.search-box input {
  width: 100%;
}

.filter-options select {
  min-width: 150px;
}

.table-container {
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  overflow: hidden;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--surface);
  border-radius: var(--radius);
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.modal-header h3 {
  margin: 0;
  color: var(--text-main);
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-muted);
}

.modal-form {
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-main);
}

.form-control {
  padding: 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--radius);
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-hover);
}

.btn-secondary {
  background: var(--bg-color);
  color: var(--text-main);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  background: var(--border);
}

.btn-danger {
  background: var(--danger);
  color: white;
}

.btn-sm {
  padding: 0.5rem;
  font-size: 0.85rem;
}

.alert-info-credentials {
  background-color: #f0f9ff;
  border-left: 4px solid #0ea5e9;
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 4px;
}

.alert-info-credentials p {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #0369a1;
}

.alert-info-credentials ul {
  list-style: none;
  padding-left: 0.5rem;
}

.alert-info-credentials li {
  font-size: 0.9rem;
  color: #0c4a6e;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filters-section {
    flex-direction: column;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
}
</style>
