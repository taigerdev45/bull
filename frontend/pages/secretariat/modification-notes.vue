<template>
  <div class="page-modification-notes">
    <header class="page-header">
      <div class="header-content">
        <h2>Modification des Notes</h2>
        <p>Consultation et modification des notes des étudiants par semestre et matière.</p>
      </div>
    </header>

    <!-- Filtres principaux -->
    <div class="filters-section">
      <div class="filter-group">
        <label for="semestre_filter">Semestre:</label>
        <select id="semestre_filter" v-model="filters.semestre_id" @change="loadData" class="form-control">
          <option value="">Sélectionner un semestre...</option>
          <option v-for="semestre in semestres" :key="semestre.id" :value="semestre.id">
            {{ semestre.libelle }} ({{ semestre.annee_universitaire }})
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="ue_filter">Unité d'Enseignement:</label>
        <select id="ue_filter" v-model="filters.ue_id" @change="loadMatieres" class="form-control">
          <option value="">Toutes les UE</option>
          <option v-for="ue in filteredUEs" :key="ue.id" :value="ue.id">
            {{ ue.code }} - {{ ue.libelle }}
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="matiere_filter">Matière:</label>
        <select id="matiere_filter" v-model="filters.matiere_id" @change="loadNotes" class="form-control">
          <option value="">Toutes les matières</option>
          <option v-for="matiere in filteredMatieres" :key="matiere.id" :value="matiere.id">
            {{ matiere.libelle }}
          </option>
        </select>
      </div>
    </div>

    <!-- Tableau des notes -->
    <div v-if="filters.semestre_id" class="notes-container">
      <div class="table-header">
        <h3>Notes {{ getMatiereLibelle(filters.matiere_id) || 'du semestre' }}</h3>
        <div class="batch-actions">
          <div class="export-dropdown">
            <button class="btn btn-secondary">
              <span>📊</span> Exporter
            </button>
            <div class="dropdown-menu">
              <button @click="exportNotes('excel')">Excel (.xlsx)</button>
              <button @click="exportNotes('pdf')">PDF (.pdf)</button>
            </div>
          </div>
          <button class="btn btn-primary" @click="saveAllNotes" :disabled="!hasChanges || loading">
            💾 Enregistrer tout
          </button>
        </div>
      </div>

      <div class="table-container">
        <table class="notes-table">
          <thead>
            <tr>
              <th>Étudiant</th>
              <th v-for="evaluationType in evaluationTypes" :key="evaluationType.key">
                {{ evaluationType.label }}
              </th>
              <th>Moyenne</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="etudiant in etudiants" :key="etudiant.id">
              <td class="etudiant-info">
                <div class="etudiant-name">{{ etudiant.nom }} {{ etudiant.prenom }}</div>
                <div class="etudiant-details">{{ etudiant.date_naissance }}</div>
              </td>
              
              <td v-for="type in evaluationTypes" :key="type.key" class="note-cell">
                <input 
                  type="number" 
                  :value="getNoteValue(etudiant.id, type.key)"
                  @input="updateNote(etudiant.id, type.key, $event.target.value)"
                  :min="0"
                  :max="20"
                  step="0.5"
                  class="note-input"
                  :class="{ 'modified': isNoteModified(etudiant.id, type.key) }"
                />
              </td>
              
              <td class="moyenne-cell">
                <span class="moyenne" :class="getMoyenneClass(calculerMoyenne(etudiant.id))">
                  {{ calculerMoyenne(etudiant.id).toFixed(2) }}
                </span>
              </td>
              
              <td class="actions-cell">
                <button class="btn btn-sm btn-secondary" @click="resetStudentNotes(etudiant.id)">
                  🔄 Réinitialiser
                </button>
                <button class="btn btn-sm btn-danger" @click="deleteStudentNotes(etudiant.id)">
                  🗑️ Supprimer
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Statistiques -->
      <div class="stats-section">
        <h4>Statistiques de la matière</h4>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">Moyenne générale</div>
            <div class="stat-value">{{ stats.moyenneGenerale.toFixed(2) }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Note la plus haute</div>
            <div class="stat-value">{{ stats.noteMax.toFixed(2) }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Note la plus basse</div>
            <div class="stat-value">{{ stats.noteMin.toFixed(2) }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Taux de réussite</div>
            <div class="stat-value">{{ stats.tauxReussite.toFixed(1) }}%</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Message si aucune donnée -->
    <div v-else class="empty-state">
      <div class="empty-icon">📚</div>
      <h3>Sélectionnez un semestre pour commencer</h3>
      <p>Choisissez un semestre, une UE et une matière pour visualiser et modifier les notes.</p>
    </div>

    <!-- Modal d'historique des modifications -->
    <div v-if="showHistoryModal" class="modal-overlay" @click="closeHistoryModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Historique des modifications</h3>
          <button class="modal-close" @click="closeHistoryModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="history-list">
            <div v-for="modification in selectedHistory" :key="modification.id" class="history-item">
              <div class="history-info">
                <strong>{{ modification.etudiant }}</strong>
                <span class="history-date">{{ formatDate(modification.date) }}</span>
              </div>
              <div class="history-changes">
                <span class="old-value">{{ modification.ancienne_valeur }}</span>
                <span class="arrow">→</span>
                <span class="new-value">{{ modification.nouvelle_valeur }}</span>
                <span class="history-type">({{ modification.type_evaluation }})</span>
              </div>
              <div class="history-author">
                Par: {{ modification.auteur }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const { exportToExcel, exportToPDF } = useExport()
useHead({ title: 'Modification des Notes | Bull ASUR' })

// État
const loading = ref(false)
const showHistoryModal = ref(false)
const selectedHistory = ref([])

// Données
const semestres = ref([])
const ues = ref([])
const matieres = ref([])
const evaluations = ref([])
const originalEvaluations = ref([])
const etudiants = ref([])

// Filtres
const filters = ref({
  semestre_id: '',
  ue_id: '',
  matiere_id: ''
})

// Types d'évaluations
const evaluationTypes = [
  { key: 'controle_continu', label: 'Contrôle Continu' },
  { key: 'examen_final', label: 'Examen Final' },
  { key: 'rattrapage', label: 'Rattrapage' }
]

// Computed
const filteredUEs = computed(() => {
  if (!filters.value.semestre_id) return []
  return ues.value.filter(ue => ue.semestre_id === filters.value.semestre_id)
})

const filteredMatieres = computed(() => {
  if (!filters.value.ue_id) return []
  return matieres.value.filter(mat => mat.ue_id === filters.value.ue_id)
})

const hasChanges = computed(() => {
  return JSON.stringify(evaluations.value) !== JSON.stringify(originalEvaluations.value)
})

const stats = computed(() => {
  if (!evaluations.value.length) return {
    moyenneGenerale: 0,
    noteMax: 0,
    noteMin: 0,
    tauxReussite: 0
  }

  const moyennes = etudiants.value.map(etudiant => calculerMoyenne(etudiant.id))
  const validMoyennes = moyennes.filter(m => m > 0)
  
  return {
    moyenneGenerale: validMoyennes.reduce((a, b) => a + b, 0) / validMoyennes.length || 0,
    noteMax: Math.max(...validMoyennes, 0),
    noteMin: Math.min(...validMoyennes, 20),
    tauxReussite: (validMoyennes.filter(m => m >= 10).length / validMoyennes.length) * 100 || 0
  }
})

// Méthodes
const getMatiereLibelle = (matiereId) => {
  if (!matiereId) return ''
  const matiere = matieres.value.find(m => m.id === matiereId)
  return matiere ? matiere.libelle : ''
}

const getNoteValue = (etudiantId, type) => {
  const evaluation = evaluations.value.find(e => 
    e.etudiant_id === etudiantId && e.type === type
  )
  return evaluation ? evaluation.note : ''
}

const updateNote = (etudiantId, type, value) => {
  const numValue = parseFloat(value)
  if (isNaN(numValue) || numValue < 0 || numValue > 20) return
  
  const existingIndex = evaluations.value.findIndex(e => 
    e.etudiant_id === etudiantId && e.type === type
  )
  
  if (existingIndex !== -1) {
    evaluations.value[existingIndex].note = numValue
  } else {
    evaluations.value.push({
      etudiant_id: etudiantId,
      matiere_id: filters.value.matiere_id,
      type: type,
      note: numValue,
      date_evaluation: new Date().toISOString()
    })
  }
}

const isNoteModified = (etudiantId, type) => {
  const current = getNoteValue(etudiantId, type)
  const original = originalEvaluations.value.find(e => 
    e.etudiant_id === etudiantId && e.type === type
  )
  return current !== (original ? original.note : '')
}

const calculerMoyenne = (etudiantId) => {
  const etudiantEvaluations = evaluations.value.filter(e => e.etudiant_id === etudiantId)
  
  if (etudiantEvaluations.length === 0) return 0
  
  // Pondération : CC 40%, Examen 60%, Rattrapage remplace la plus basse des deux
  const cc = etudiantEvaluations.find(e => e.type === 'CC')?.note || 0
  const examen = etudiantEvaluations.find(e => e.type === 'EXAMEN')?.note || 0
  const rattrapage = etudiantEvaluations.find(e => e.type === 'RATTRAPAGE')?.note
  
  if (rattrapage && rattrapage > Math.min(cc, examen)) {
    const minNote = Math.min(cc, examen)
    const maxNote = Math.max(cc, examen)
    return (maxNote * 0.6 + rattrapage * 0.4)
  }
  
  return (cc * 0.4 + examen * 0.6)
}

const getMoyenneClass = (moyenne) => {
  if (moyenne >= 15) return 'excellent'
  if (moyenne >= 12) return 'bien'
  if (moyenne >= 10) return 'passable'
  return 'insuffisant'
}

const resetStudentNotes = (etudiantId) => {
  if (!confirm('Réinitialiser toutes les notes de cet étudiant ?')) return
  
  evaluations.value = evaluations.value.filter(e => e.etudiant_id !== etudiantId)
}

const deleteStudentNotes = (etudiantId) => {
  if (!confirm('Supprimer définitivement toutes les notes de cet étudiant ?')) return
  
  evaluations.value = evaluations.value.filter(e => e.etudiant_id !== etudiantId)
}

const saveAllNotes = async () => {
  if (!filters.value.matiere_id) return
  loading.value = true
  
  try {
    await $fetch(`${$config.public.apiBase}/evaluations/bulk/`, {
      method: 'POST',
      body: {
        matiere_id: filters.value.matiere_id,
        evaluations: evaluations.value
      }
    })
    
    originalEvaluations.value = JSON.parse(JSON.stringify(evaluations.value))
    console.log('Évaluations enregistrées avec succès')
    
  } catch (error) {
    console.error('Erreur lors de l\'enregistrement:', error)
  } finally {
    loading.value = false
  }
}

const exportNotes = (format = 'excel') => {
  const libelleMatiere = getMatiereLibelle(filters.value.matiere_id) || 'matiere'
  const filename = `notes_${libelleMatiere}_${new Date().toISOString().split('T')[0]}`

  const data = etudiants.value.map(etudiant => {
    const row = {
      Étudiant: `${etudiant.nom} ${etudiant.prenom}`,
      Matricule: etudiant.matricule || '-'
    }
    evaluationTypes.forEach(type => {
      row[type.label] = getNoteValue(etudiant.id, type.key) || '-'
    })
    row['Moyenne'] = calculerMoyenne(etudiant.id).toFixed(2)
    return row
  })

  if (format === 'excel') {
    exportToExcel(data, `${filename}.xlsx`)
  } else {
    const headers = ['Étudiant', 'Matricule', ...evaluationTypes.map(t => t.label), 'Moyenne']
    const rows = etudiants.value.map(etudiant => [
      `${etudiant.nom} ${etudiant.prenom}`,
      etudiant.matricule || '-',
      ...evaluationTypes.map(type => getNoteValue(etudiant.id, type.key) || '-'),
      calculerMoyenne(etudiant.id).toFixed(2)
    ])
    exportToPDF(headers, rows, `${filename}.pdf`, 'l')
  }
}

const showHistory = async (etudiantId) => {
  try {
    const response = await $fetch(`${$config.public.apiBase}/notes/history/${etudiantId}`)
    selectedHistory.value = response
    showHistoryModal.value = true
  } catch (error) {
    console.error('Erreur lors du chargement de l\'historique:', error)
  }
}

const closeHistoryModal = () => {
  showHistoryModal.value = false
  selectedHistory.value = []
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('fr-FR')
}

// Chargement des données
const loadSemestres = async () => {
  try {
    const response = await $fetch(`${$config.public.apiBase}/semestres`)
    semestres.value = response
  } catch (error) {
    console.error('Erreur lors du chargement des semestres:', error)
  }
}

const loadUEs = async () => {
  try {
    const response = await $fetch(`${$config.public.apiBase}/ues`)
    ues.value = response
  } catch (error) {
    console.error('Erreur lors du chargement des UE:', error)
  }
}

const loadMatieres = async () => {
  if (!filters.value.semestre_id) return
  
  try {
    const response = await $fetch(`${$config.public.apiBase}/matieres`)
    matieres.value = response
  } catch (error) {
    console.error('Erreur lors du chargement des matières:', error)
  }
}

const loadEtudiants = async () => {
  try {
    const response = await $fetch(`${$config.public.apiBase}/etudiants`)
    etudiants.value = response
  } catch (error) {
    console.error('Erreur lors du chargement des étudiants:', error)
  }
}

const loadNotes = async () => {
  if (!filters.value.matiere_id) {
    evaluations.value = []
    originalEvaluations.value = []
    return
  }
  
  try {
    const response = await $fetch(`${$config.public.apiBase}/evaluations/matiere/${filters.value.matiere_id}`)
    evaluations.value = response
    originalEvaluations.value = JSON.parse(JSON.stringify(response))
  } catch (error) {
    console.error('Erreur lors du chargement des évaluations:', error)
    evaluations.value = []
    originalEvaluations.value = []
  }
}

const loadData = async () => {
  await loadEtudiants()
  await loadNotes()
}

onMounted(() => {
  loadSemestres()
  loadUEs()
})

watch(() => filters.value.ue_id, () => {
  filters.value.matiere_id = ''
  loadNotes()
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

.filters-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.filter-group label {
  font-weight: 500;
  color: var(--text-main);
  font-size: 0.9rem;
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

.notes-container {
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
  background: var(--bg-color);
}

.table-header h3 {
  margin: 0;
  color: var(--text-main);
}

.batch-actions {
  display: flex;
  gap: 0.5rem;
}

.table-container {
  overflow-x: auto;
}

.notes-table {
  width: 100%;
  border-collapse: collapse;
}

.notes-table th {
  background: var(--bg-color);
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--text-main);
  border-bottom: 2px solid var(--border);
}

.notes-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--border);
}

.etudiant-info .etudiant-name {
  font-weight: 600;
  color: var(--text-main);
}

.etudiant-info .etudiant-details {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.note-cell {
  text-align: center;
}

.note-input {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  text-align: center;
  font-weight: 500;
  transition: all 0.2s;
}

.note-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(87, 108, 168, 0.2);
}

.note-input.modified {
  border-color: var(--warning);
  background: rgba(245, 158, 11, 0.1);
}

.moyenne-cell {
  text-align: center;
  font-weight: 700;
}

.moyenne.excellent { color: #10b981; }
.moyenne.bien { color: #3b82f6; }
.moyenne.passable { color: #f59e0b; }
.moyenne.insuffisant { color: var(--danger); }

.actions-cell {
  text-align: center;
}

.stats-section {
  padding: 1.5rem;
  background: var(--bg-color);
  border-top: 1px solid var(--border);
}

.stats-section h4 {
  margin: 0 0 1rem 0;
  color: var(--text-main);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: var(--surface);
  padding: 1rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  text-align: center;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  margin-bottom: 0.5rem;
  color: var(--text-main);
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
  max-height: 80vh;
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

.modal-body {
  padding: 1.5rem;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.history-item {
  padding: 1rem;
  background: var(--bg-color);
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

.history-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.history-date {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.history-changes {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.old-value {
  color: var(--danger);
  text-decoration: line-through;
}

.new-value {
  color: var(--success);
  font-weight: 600;
}

.arrow {
  color: var(--text-muted);
}

.history-type {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.history-author {
  font-size: 0.85rem;
  color: var(--text-muted);
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

.btn-primary:hover:not(:disabled) {
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

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .filters-section {
    flex-direction: column;
  }
  
  .table-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .batch-actions {
    justify-content: center;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .notes-table {
    font-size: 0.85rem;
  }
  
  .notes-table th,
  .notes-table td {
    padding: 0.5rem;
  }
  
  .note-input {
    width: 60px;
  }
}
</style>
