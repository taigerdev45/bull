<template>
  <div class="page-edition-bulletins">
    <header class="page-header">
      <div class="header-content">
        <h2>Édition des Bulletins</h2>
        <p>Gestion de la structure des bulletins : semestres, UE, matières et absences.</p>
      </div>
    </header>

    <!-- Onglets de navigation -->
    <div class="tabs-container">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab-button', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- Contenu des onglets -->
    <div class="tab-content">
      <!-- Onglet Semestres -->
      <div v-if="activeTab === 'semestres'" class="tab-panel">
        <div class="panel-header">
          <h3>Gestion des Semestres</h3>
          <button class="btn btn-primary" @click="openModal('semestre', 'add')">
            Ajouter un semestre
          </button>
        </div>
        
        <div class="table-container">
          <DataTable
            :columns="semestreColumns"
            :data="semestres"
            :actions="true"
          >
            <template #actions="{ row }">
              <button class="btn btn-sm btn-secondary" @click="openModal('semestre', 'edit', row)">
                Modifier
              </button>
              <button class="btn btn-sm btn-danger" @click="deleteItem('semestre', row.id)">
                Supprimer
              </button>
            </template>
          </DataTable>
        </div>
      </div>

      <!-- Onglet UE -->
      <div v-if="activeTab === 'ues'" class="tab-panel">
        <div class="panel-header">
          <h3>Gestion des Unités d'Enseignement</h3>
          <button class="btn btn-primary" @click="openModal('ue', 'add')">
            Ajouter une UE
          </button>
        </div>
        
        <div class="table-container">
          <DataTable
            :columns="ueColumns"
            :data="ues"
            :actions="true"
          >
            <template #semestre="{ row }">
              {{ getSemestreLibelle(row.semestre_id) }}
            </template>
            <template #actions="{ row }">
              <button class="btn btn-sm btn-secondary" @click="openModal('ue', 'edit', row)">
                Modifier
              </button>
              <button class="btn btn-sm btn-danger" @click="deleteItem('ue', row.id)">
                Supprimer
              </button>
            </template>
          </DataTable>
        </div>
      </div>

      <!-- Onglet Matières -->
      <div v-if="activeTab === 'matieres'" class="tab-panel">
        <div class="panel-header">
          <h3>Gestion des Matières</h3>
          <button class="btn btn-primary" @click="openModal('matiere', 'add')">
            Ajouter une matière
          </button>
        </div>
        
        <div class="table-container">
          <DataTable
            :columns="matiereColumns"
            :data="matieres"
            :actions="true"
          >
            <template #ue="{ row }">
              {{ getUELibelle(row.ue_id) }}
            </template>
            <template #actions="{ row }">
              <button class="btn btn-sm btn-secondary" @click="openModal('matiere', 'edit', row)">
                Modifier
              </button>
              <button class="btn btn-sm btn-danger" @click="deleteItem('matiere', row.id)">
                Supprimer
              </button>
            </template>
          </DataTable>
        </div>
      </div>

      <!-- Onglet Absences -->
      <div v-if="activeTab === 'absences'" class="tab-panel">
        <div class="panel-header">
          <h3>Gestion des Absences</h3>
          <button class="btn btn-primary" @click="openModal('absence', 'add')">
            Ajouter une absence
          </button>
        </div>
        
        <!-- Filtres pour les absences -->
        <div class="filters-section">
          <div class="filter-group">
            <label>Étudiant</label>
            <select v-model="absenceFilters.etudiant_id" class="form-control">
              <option value="">Tous les étudiants</option>
              <option v-for="etudiant in etudiants" :key="etudiant.id" :value="etudiant.id">
                {{ etudiant.nom }} {{ etudiant.prenom }}
              </option>
            </select>
          </div>
          <div class="filter-group">
            <label>Matière</label>
            <select v-model="absenceFilters.matiere_id" class="form-control">
              <option value="">Toutes les matières</option>
              <option v-for="matiere in matieres" :key="matiere.id" :value="matiere.id">
                {{ matiere.libelle }}
              </option>
            </select>
          </div>
        </div>
        
        <div class="table-container">
          <DataTable
            :columns="absenceColumns"
            :data="filteredAbsences"
            :actions="true"
          >
            <template #etudiant="{ row }">
              {{ getEtudiantLibelle(row.etudiant_id) }}
            </template>
            <template #matiere="{ row }">
              {{ getMatiereLibelle(row.matiere_id) }}
            </template>
            <template #actions="{ row }">
              <button class="btn btn-sm btn-secondary" @click="openModal('absence', 'edit', row)">
                Modifier
              </button>
              <button class="btn btn-sm btn-danger" @click="deleteItem('absence', row.id)">
                Supprimer
              </button>
            </template>
          </DataTable>
        </div>
      </div>
    </div>

    <!-- Modal générique pour tous les CRUD -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ getModalTitle() }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        
        <form @submit.prevent="saveItem" class="modal-form">
          <!-- Semestre Form -->
          <div v-if="modalType === 'semestre'">
            <div class="form-group">
              <label for="semestre_libelle">Libellé *</label>
              <input 
                type="text" 
                id="semestre_libelle" 
                v-model="formData.libelle" 
                required 
                class="form-control"
                placeholder="Ex: Semestre 5"
              >
            </div>
            <div class="form-group">
              <label for="semestre_annee">Année universitaire *</label>
              <input 
                type="text" 
                id="semestre_annee" 
                v-model="formData.annee_universitaire" 
                required 
                class="form-control"
                placeholder="Ex: 2025-2026"
              >
            </div>
          </div>

          <!-- UE Form -->
          <div v-if="modalType === 'ue'">
            <div class="form-group">
              <label for="ue_code">Code *</label>
              <input 
                type="text" 
                id="ue_code" 
                v-model="formData.code" 
                required 
                class="form-control"
                placeholder="Ex: UE5-1"
              >
            </div>
            <div class="form-group">
              <label for="ue_libelle">Libellé *</label>
              <input 
                type="text" 
                id="ue_libelle" 
                v-model="formData.libelle" 
                required 
                class="form-control"
                placeholder="Ex: Enseignement Général"
              >
            </div>
            <div class="form-group">
              <label for="ue_semestre">Semestre *</label>
              <select id="ue_semestre" v-model="formData.semestre_id" required class="form-control">
                <option value="">Sélectionner un semestre...</option>
                <option v-for="semestre in semestres" :key="semestre.id" :value="semestre.id">
                  {{ semestre.libelle }} ({{ semestre.annee_universitaire }})
                </option>
              </select>
            </div>
          </div>

          <!-- Matière Form -->
          <div v-if="modalType === 'matiere'">
            <div class="form-row">
              <div class="form-group">
                <label for="matiere_libelle">Libellé *</label>
                <input 
                  type="text" 
                  id="matiere_libelle" 
                  v-model="formData.libelle" 
                  required 
                  class="form-control"
                  placeholder="Ex: Anglais technique"
                >
              </div>
              <div class="form-group">
                <label for="matiere_coefficient">Coefficient *</label>
                <input 
                  type="number" 
                  id="matiere_coefficient" 
                  v-model="formData.coefficient" 
                  required 
                  min="1"
                  step="0.5"
                  class="form-control"
                >
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="matiere_credits">Crédits ECTS *</label>
                <input 
                  type="number" 
                  id="matiere_credits" 
                  v-model="formData.credits" 
                  required 
                  min="1"
                  class="form-control"
                >
              </div>
              <div class="form-group">
                <label for="matiere_ue">UE *</label>
                <select id="matiere_ue" v-model="formData.ue_id" required class="form-control">
                  <option value="">Sélectionner une UE...</option>
                  <option v-for="ue in ues" :key="ue.id" :value="ue.id">
                    {{ ue.code }} - {{ ue.libelle }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Absence Form -->
          <div v-if="modalType === 'absence'">
            <div class="form-row">
              <div class="form-group">
                <label for="absence_etudiant">Étudiant *</label>
                <select id="absence_etudiant" v-model="formData.etudiant_id" required class="form-control">
                  <option value="">Sélectionner un étudiant...</option>
                  <option v-for="etudiant in etudiants" :key="etudiant.id" :value="etudiant.id">
                    {{ etudiant.nom }} {{ etudiant.prenom }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label for="absence_matiere">Matière *</label>
                <select id="absence_matiere" v-model="formData.matiere_id" required class="form-control">
                  <option value="">Sélectionner une matière...</option>
                  <option v-for="matiere in matieres" :key="matiere.id" :value="matiere.id">
                    {{ matiere.libelle }}
                  </option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label for="absence_heures">Nombre d'heures *</label>
              <input 
                type="number" 
                id="absence_heures" 
                v-model="formData.heures" 
                required 
                min="0.5"
                step="0.5"
                class="form-control"
                placeholder="Ex: 2.5"
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

useHead({ title: 'Édition des Bulletins | Bull ASUR' })

// État
const activeTab = ref('semestres')
const showModal = ref(false)
const modalType = ref('')
const modalMode = ref('add')
const loading = ref(false)
const currentItem = ref(null)

// Données
const semestres = ref([])
const ues = ref([])
const matieres = ref([])
const absences = ref([])
const etudiants = ref([])

// Filtres pour les absences
const absenceFilters = ref({
  etudiant_id: '',
  matiere_id: ''
})

// Formulaire générique
const formData = ref({})

// Onglets
const tabs = [
  { id: 'semestres', label: 'Semestres' },
  { id: 'ues', label: 'Unités d\'Enseignement' },
  { id: 'matieres', label: 'Matières' },
  { id: 'absences', label: 'Absences' }
]

// Colonnes des tableaux
const semestreColumns = [
  { key: 'libelle', label: 'Libellé' },
  { key: 'annee_universitaire', label: 'Année universitaire' }
]

const ueColumns = [
  { key: 'code', label: 'Code' },
  { key: 'libelle', label: 'Libellé' },
  { key: 'semestre', label: 'Semestre' }
]

const matiereColumns = [
  { key: 'libelle', label: 'Libellé' },
  { key: 'coefficient', label: 'Coefficient' },
  { key: 'credits', label: 'Crédits ECTS' },
  { key: 'ue', label: 'UE' }
]

const absenceColumns = [
  { key: 'etudiant', label: 'Étudiant' },
  { key: 'matiere', label: 'Matière' },
  { key: 'heures', label: 'Heures d\'absence' }
]

// Computed
const filteredAbsences = computed(() => {
  return absences.value.filter(absence => {
    const matchesEtudiant = !absenceFilters.value.etudiant_id || absence.etudiant_id === absenceFilters.value.etudiant_id
    const matchesMatiere = !absenceFilters.value.matiere_id || absence.matiere_id === absenceFilters.value.matiere_id
    return matchesEtudiant && matchesMatiere
  })
})

// Méthodes utilitaires
const getModalTitle = () => {
  const typeLabels = {
    semestre: 'Semestre',
    ue: 'Unité d\'Enseignement',
    matiere: 'Matière',
    absence: 'Absence'
  }
  const action = modalMode.value === 'add' ? 'Ajouter' : 'Modifier'
  return `${action} un(e) ${typeLabels[modalType.value]}`
}

const getSemestreLibelle = (semestreId) => {
  const semestre = semestres.value.find(s => s.id === semestreId)
  return semestre ? `${semestre.libelle} (${semestre.annee_universitaire})` : 'N/A'
}

const getUELibelle = (ueId) => {
  const ue = ues.value.find(u => u.id === ueId)
  return ue ? `${ue.code} - ${ue.libelle}` : 'N/A'
}

const getMatiereLibelle = (matiereId) => {
  const matiere = matieres.value.find(m => m.id === matiereId)
  return matiere ? matiere.libelle : 'N/A'
}

const getEtudiantLibelle = (etudiantId) => {
  const etudiant = etudiants.value.find(e => e.id === etudiantId)
  return etudiant ? `${etudiant.nom} ${etudiant.prenom}` : 'N/A'
}

// Méthodes CRUD
const openModal = (type, mode, item = null) => {
  modalType.value = type
  modalMode.value = mode
  currentItem.value = item
  
  if (mode === 'edit' && item) {
    formData.value = { ...item }
  } else {
    resetForm()
  }
  
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  resetForm()
  currentItem.value = null
}

const resetForm = () => {
  formData.value = {}
}

const saveItem = async () => {
  loading.value = true
  
  try {
    const apiEndpoints = {
      semestre: 'semestres',
      ue: 'ues',
      matiere: 'matieres',
      absence: 'absences'
    }
    
    const endpoint = apiEndpoints[modalType.value]
    const url = modalMode.value === 'add' 
      ? `${$config.public.apiBase}/${endpoint}`
      : `${$config.public.apiBase}/${endpoint}/${currentItem.value.id}`
    
    const method = modalMode.value === 'add' ? 'POST' : 'PUT'
    
    const response = await $fetch(url, {
      method,
      body: formData.value
    })
    
    // Mise à jour locale
    const dataArray = {
      semestre: semestres,
      ue: ues,
      matiere: matieres,
      absence: absences
    }[modalType.value].value
    
    if (modalMode.value === 'add') {
      dataArray.push(response)
    } else {
      const index = dataArray.findIndex(item => item.id === currentItem.value.id)
      if (index !== -1) {
        dataArray[index] = response
      }
    }
    
    // TODO: Implémenter la mise à jour automatique des bulletins
    
    closeModal()
    console.log(`${modalType.value} enregistré avec succès`)
    
  } catch (error) {
    console.error(`Erreur lors de l'enregistrement:`, error)
  } finally {
    loading.value = false
  }
}

const deleteItem = async (type, itemId) => {
  const typeLabels = {
    semestre: 'ce semestre',
    ue: 'cette UE',
    matiere: 'cette matière',
    absence: 'cette absence'
  }
  
  if (!confirm(`Êtes-vous sûr de vouloir supprimer ${typeLabels[type]} ?`)) {
    return
  }
  
  try {
    const apiEndpoints = {
      semestre: 'semestres',
      ue: 'ues',
      matiere: 'matieres',
      absence: 'absences'
    }
    
    await $fetch(`${$config.public.apiBase}/${apiEndpoints[type]}/${itemId}`, {
      method: 'DELETE'
    })
    
    // Mise à jour locale
    const dataArray = {
      semestre: semestres,
      ue: ues,
      matiere: matieres,
      absence: absences
    }[type].value
    
    const index = dataArray.findIndex(item => item.id === itemId)
    if (index !== -1) {
      dataArray.splice(index, 1)
    }
    
    // TODO: Implémenter la mise à jour automatique des bulletins
    
    console.log(`${type} supprimé avec succès`)
    
  } catch (error) {
    console.error(`Erreur lors de la suppression:`, error)
  }
}

// Chargement des données
const loadData = async () => {
  try {
    const [semestresRes, uesRes, matieresRes, absencesRes, etudiantsRes] = await Promise.all([
      $fetch(`${$config.public.apiBase}/semestres`),
      $fetch(`${$config.public.apiBase}/ues`),
      $fetch(`${$config.public.apiBase}/matieres`),
      $fetch(`${$config.public.apiBase}/absences`),
      $fetch(`${$config.public.apiBase}/etudiants`)
    ])
    
    semestres.value = semestresRes
    ues.value = uesRes
    matieres.value = matieresRes
    absences.value = absencesRes
    etudiants.value = etudiantsRes
  } catch (error) {
    console.error('Erreur lors du chargement des données:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page-header {
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

.tabs-container {
  margin-bottom: 2rem;
}

.tabs {
  display: flex;
  border-bottom: 1px solid var(--border);
}

.tab-button {
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-muted);
  transition: all 0.2s;
}

.tab-button:hover {
  color: var(--text-main);
  background: var(--bg-color);
}

.tab-button.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
  background: var(--bg-color);
}

.tab-panel {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.panel-header h3 {
  font-size: 1.25rem;
  color: var(--text-main);
  margin: 0;
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

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  color: var(--text-main);
  font-size: 0.9rem;
}

.filter-group select {
  min-width: 200px;
}

.table-container {
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  overflow: hidden;
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
  margin-bottom: 1rem;
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

@media (max-width: 768px) {
  .tabs {
    flex-wrap: wrap;
  }
  
  .tab-button {
    flex: 1;
    min-width: 120px;
    text-align: center;
  }
  
  .panel-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
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
