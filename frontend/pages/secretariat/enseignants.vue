<template>
  <div class="page-enseignants">
    <header class="page-header">
      <div class="header-content">
        <h2>Gestion des Enseignants</h2>
        <p>Assignez les matières et gérez les intervenants pédagogiques.</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="openModal('add')">
          <span class="icon">➕</span> Ajouter un Enseignant
        </button>
      </div>
    </header>

    <!-- Filtres et recherche -->
    <div class="filters-section">
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchTerm" 
          placeholder="Rechercher par nom, prénom, spécialité..."
          class="form-control"
        >
      </div>
    </div>

    <!-- Tableau des enseignants -->
    <div class="table-container">
      <DataTable
        :columns="teacherColumns"
        :data="filteredTeachers"
        title="Liste des enseignants"
        :actions="true"
      >
        <template #matieres="{ row }">
          <div class="matieres-tags">
            <span v-for="mat in row.matieres" :key="mat" class="tag">
              {{ mat }}
            </span>
            <span v-if="!row.matieres?.length" class="text-muted">Aucune</span>
          </div>
        </template>
        <template #actions="{ row }">
          <button class="btn btn-sm btn-secondary" @click="openModal('edit', row)">
            ✏️
          </button>
          <button class="btn btn-sm btn-info" @click="openAssignModal(row)">
            🔗
          </button>
          <button class="btn btn-sm btn-danger" @click="deleteTeacher(row.id)">
            🗑️
          </button>
        </template>
      </DataTable>
    </div>

    <!-- Modal Ajout/Modification -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalMode === 'add' ? 'Ajouter' : 'Modifier' }} un enseignant</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        
        <form @submit.prevent="saveTeacher" class="modal-form">
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
                placeholder="ENSE001"
              >
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="telephone">Téléphone</label>
              <input 
                type="tel" 
                id="telephone" 
                v-model="formData.telephone" 
                class="form-control"
              >
            </div>
          </div>

          <div class="form-group">
            <label for="specialite">Spécialité</label>
            <input 
              type="text" 
              id="specialite" 
              v-model="formData.specialite" 
              placeholder="Réseaux, Développement, Mathématiques..."
              class="form-control"
            >
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

    <!-- Modal Assignation -->
    <div v-if="showAssignModal" class="modal-overlay" @click.self="closeAssignModal">
      <div class="modal-content">
        <header class="modal-header">
          <h3>Assigner des matières à {{ selectedTeacher?.nom }} {{ selectedTeacher?.prenom }}</h3>
          <button class="close-btn" @click="closeAssignModal">&times;</button>
        </header>
        <div class="modal-body">
          <div class="form-group">
            <label>Matières disponibles</label>
            <div class="matieres-list">
              <div v-for="ue in availableUEs" :key="ue.id" class="ue-group">
                <h4>{{ ue.libelle }}</h4>
                <div class="matieres-checkboxes">
                  <label v-for="mat in ue.matieres" :key="mat.id" class="checkbox-label">
                    <input 
                      type="checkbox" 
                      :value="mat.id"
                      v-model="selectedMatieres"
                    >
                    <span>{{ mat.libelle }} ({{ mat.coefficient }} coeff, {{ mat.credits }} ECTS)</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
        <footer class="modal-footer">
          <button class="btn btn-secondary" @click="closeAssignModal">Annuler</button>
          <button class="btn btn-primary" @click="assignMatieres">Confirmer l'assignation</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

useHead({ title: 'Gestion des Enseignants | Bull ASUR' })

// État
const teachers = ref([])
const searchTerm = ref('')
const showModal = ref(false)
const modalMode = ref('add')
const loading = ref(false)
const currentTeacher = ref(null)
const showAssignModal = ref(false)
const selectedTeacher = ref(null)
const selectedMatieres = ref([])
const availableUEs = ref([])

// Formulaire
const formData = ref({
  nom: '',
  prenom: '',
  email: '',
  matricule: '',
  telephone: '',
  specialite: ''
})

// Colonnes du tableau
const teacherColumns = [
  { key: 'nom', label: 'Nom' },
  { key: 'prenom', label: 'Prénom' },
  { key: 'email', label: 'Email' },
  { key: 'matricule', label: 'Matricule' },
  { key: 'specialite', label: 'Spécialité' },
  { key: 'matieres', label: 'Matières assignées' }
]

// Filtrage
const filteredTeachers = computed(() => {
  return teachers.value.filter(teacher => {
    const searchLower = searchTerm.value.toLowerCase()
    return `${teacher.nom} ${teacher.prenom} ${teacher.email || ''} ${teacher.matricule || ''} ${teacher.specialite || ''}`.toLowerCase().includes(searchLower)
  })
})

// Méthodes CRUD
const openModal = (mode, teacher = null) => {
  modalMode.value = mode
  currentTeacher.value = teacher
  
  if (mode === 'edit' && teacher) {
    formData.value = { ...teacher }
  } else {
    resetForm()
  }
  
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  resetForm()
  currentTeacher.value = null
}

const resetForm = () => {
  formData.value = {
    nom: '',
    prenom: '',
    email: '',
    matricule: '',
    telephone: '',
    specialite: ''
  }
}

const saveTeacher = async () => {
  loading.value = true
  
  try {
    const url = modalMode.value === 'add' 
      ? `${$config.public.apiBase}/enseignants`
      : `${$config.public.apiBase}/enseignants/${currentTeacher.value.id}`
    
    const method = modalMode.value === 'add' ? 'POST' : 'PUT'
    
    const response = await $fetch(url, {
      method,
      body: formData.value
    })
    
    if (modalMode.value === 'add') {
      teachers.value.push({ ...response, matieres: [] })
    } else {
      const index = teachers.value.findIndex(t => t.id === currentTeacher.value.id)
      if (index !== -1) {
        teachers.value[index] = { ...response, matieres: teachers.value[index].matieres }
      }
    }
    
    closeModal()
    console.log('Enseignant enregistré avec succès')
    
  } catch (error) {
    console.error('Erreur lors de l\'enregistrement:', error)
  } finally {
    loading.value = false
  }
}

const deleteTeacher = async (teacherId) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer cet enseignant ?')) {
    return
  }
  
  try {
    await $fetch(`${$config.public.apiBase}/enseignants/${teacherId}`, {
      method: 'DELETE'
    })
    
    teachers.value = teachers.value.filter(t => t.id !== teacherId)
    console.log('Enseignant supprimé avec succès')
    
  } catch (error) {
    console.error('Erreur lors de la suppression:', error)
  }
}

// Gestion des assignations
const openAssignModal = (teacher) => {
  selectedTeacher.value = teacher
  selectedMatieres.value = teacher.matieres?.map(m => m.id) || []
  showAssignModal.value = true
}

const closeAssignModal = () => {
  showAssignModal.value = false
  selectedTeacher.value = null
  selectedMatieres.value = []
}

const assignMatieres = async () => {
  try {
    await $fetch(`${$config.public.apiBase}/enseignants/${selectedTeacher.value.id}/assign-matieres`, {
      method: 'POST',
      body: { matiere_ids: selectedMatieres.value }
    })
    
    // Mettre à jour localement
    const teacher = teachers.value.find(t => t.id === selectedTeacher.value.id)
    if (teacher) {
      teacher.matieres = selectedMatieres.value.map(id => {
        for (const ue of availableUEs.value) {
          const mat = ue.matieres.find(m => m.id === id)
          if (mat) return mat
        }
        return null
      }).filter(Boolean)
    }
    
    closeAssignModal()
    console.log('Matières assignées avec succès')
    
  } catch (error) {
    console.error('Erreur lors de l\'assignation:', error)
  }
}

// Chargement des données
const loadTeachers = async () => {
  try {
    const response = await $fetch(`${$config.public.apiBase}/enseignants`)
    teachers.value = response
  } catch (error) {
    console.error('Erreur lors du chargement des enseignants:', error)
    teachers.value = []
  }
}

const loadAvailableMatieres = async () => {
  try {
    const response = await $fetch(`${$config.public.apiBase}/matieres-with-ue`)
    availableUEs.value = response
  } catch (error) {
    console.error('Erreur lors du chargement des matières:', error)
    availableUEs.value = []
  }
}

onMounted(() => {
  loadTeachers()
  loadAvailableMatieres()
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

.table-container {
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  overflow: hidden;
}

.matieres-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.matieres-tags .tag {
  background: var(--bg-color);
  color: var(--text-muted);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  border: 1px solid var(--border);
}

.text-muted {
  color: var(--text-muted);
  font-style: italic;
}

/* Modal styles */
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

/* Modal assignation styles */
.modal-body {
  padding: 1.5rem;
}

.matieres-list {
  max-height: 400px;
  overflow-y: auto;
}

.ue-group {
  margin-bottom: 1.5rem;
}

.ue-group h4 {
  margin-bottom: 0.75rem;
  color: var(--primary);
  font-size: 1rem;
  font-weight: 600;
}

.matieres-checkboxes {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.checkbox-label:hover {
  background-color: var(--bg-color);
}

.checkbox-label input[type="checkbox"] {
  margin: 0;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background: var(--bg-color);
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

.btn-info {
  background: #3b82f6;
  color: white;
}

.btn-danger {
  background: var(--danger);
  color: white;
}

.btn-sm {
  padding: 0.5rem;
  font-size: 0.85rem;
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
