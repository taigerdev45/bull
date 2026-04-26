<template>
  <div class="page-bulletins">
    <header class="page-header">
      <div class="header-content">
        <h2>Génération des Bulletins</h2>
        <p>Générez les bulletins PDF et exportez les données Excel pour les étudiants.</p>
      </div>
    </header>

    <!-- Filtres -->
    <div class="filters-section">
      <div class="filter-row">
        <div class="filter-group">
          <label for="promotion">Promotion:</label>
          <select id="promotion" v-model="filters.promotion" class="form-control">
            <option value="2025-2026">2025-2026</option>
            <option value="2024-2025">2024-2025</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="semestre">Semestre:</label>
          <select id="semestre" v-model="filters.semestre" class="form-control">
            <option value="">Tous</option>
            <option value="S5">Semestre 5</option>
            <option value="S6">Semestre 6</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="statut">Statut:</label>
          <select id="statut" v-model="filters.statut" class="form-control">
            <option value="">Tous</option>
            <option value="valide">Validé</option>
            <option value="admissible">Admissible</option>
            <option value="non_valide">Non validé</option>
          </select>
        </div>
      </div>
      
      <div class="filter-actions">
        <button @click="applyFilters" class="btn btn-primary">
          <span>Appliquer</span>
        </button>
        <button @click="resetFilters" class="btn btn-secondary">
          <span>Réinitialiser</span>
        </button>
      </div>
    </div>

    <!-- Statistiques -->
    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <h4>{{ stats.total_etudiants }}</h4>
          <p>Total Étudiants</p>
        </div>
        <div class="stat-card">
          <h4>{{ stats.diplomes }}</h4>
          <p>Diplômés</p>
        </div>
        <div class="stat-card">
          <h4>{{ stats.admissibles }}</h4>
          <p>Admissibles</p>
        </div>
        <div class="stat-card">
          <h4>{{ stats.redoublants }}</h4>
          <p>Redoublants</p>
        </div>
      </div>
    </div>

    <!-- Actions de génération -->
    <div class="actions-section">
      <h3>Actions de Génération</h3>
      
      <div class="action-grid">
        <!-- Génération individuelle -->
        <div class="action-card">
          <h4>Génération Individuelle</h4>
          <p>Générez des bulletins pour des étudiants spécifiques</p>
          
          <div class="action-controls">
            <select v-model="selectedEtudiant" class="form-control">
              <option value="">Choisir un étudiant...</option>
              <option v-for="etudiant in filteredEtudiants" :key="etudiant.id" :value="etudiant.id">
                {{ etudiant.nom }} {{ etudiant.prenom }} ({{ etudiant.matricule }})
              </option>
            </select>
            
            <div class="button-group">
              <button @click="generateBulletinS5" :disabled="!selectedEtudiant" class="btn btn-primary">
                <span>PDF</span> Bulletin S5
              </button>
              <button @click="generateBulletinS6" :disabled="!selectedEtudiant" class="btn btn-primary">
                <span>PDF</span> Bulletin S6
              </button>
              <button @click="generateBulletinAnnuel" :disabled="!selectedEtudiant" class="btn btn-success">
                <span>PDF</span> Bulletin Annuel
              </button>
            </div>
          </div>
        </div>

        <!-- Génération par lot -->
        <div class="action-card">
          <h4>Génération par Lot</h4>
          <p>Générez tous les bulletins pour la promotion</p>
          
          <div class="action-controls">
            <div class="checkbox-group">
              <label>
                <input type="checkbox" v-model="batchOptions.S5">
                Bulletins S5
              </label>
              <label>
                <input type="checkbox" v-model="batchOptions.S6">
                Bulletins S6
              </label>
              <label>
                <input type="checkbox" v-model="batchOptions.annuel">
                Bulletins Annuels
              </label>
            </div>
            
            <button @click="generateBatchBulletins" :disabled="!hasBatchOption" class="btn btn-success">
              <span>PDF</span> Générer le Lot
            </button>
          </div>
        </div>

        <!-- Export Excel -->
        <div class="action-card">
          <h4>Export Excel</h4>
          <p>Exportez les données en format Excel</p>
          
          <div class="action-controls">
            <div class="button-group">
              <button @click="exportReleveS5" class="btn btn-secondary">
                <span>📊</span> Excel S5
              </button>
              <button @click="exportRelevePDF(5)" class="btn btn-secondary">
                <span>📄</span> PDF S5
              </button>
              <button @click="exportReleveS6" class="btn btn-secondary">
                <span>📊</span> Excel S6
              </button>
              <button @click="exportRelevePDF(6)" class="btn btn-secondary">
                <span>📄</span> PDF S6
              </button>
              <button @click="exportDecisionsJury" class="btn btn-info">
                <span>📊</span> Excel Jury
              </button>
              <button @click="exportDecisionsPDF('l')" class="btn btn-info">
                <span>📄</span> PDF Jury (L)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tableau des étudiants -->
    <div class="table-section">
      <h3>Liste des Étudiants</h3>
      
      <div class="table-container">
        <table class="students-table">
          <thead>
            <tr>
              <th>Matricule</th>
              <th>Nom</th>
              <th>Prénom</th>
              <th>Moyenne S5</th>
              <th>Crédits S5</th>
              <th>Moyenne S6</th>
              <th>Crédits S6</th>
              <th>Moyenne Annuelle</th>
              <th>Décision</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="etudiant in filteredEtudiants" :key="etudiant.id">
              <td>{{ etudiant.matricule }}</td>
              <td>{{ etudiant.nom }}</td>
              <td>{{ etudiant.prenom }}</td>
              <td>{{ etudiant.moyenne_S5 || '-' }}</td>
              <td>{{ etudiant.credits_S5 || '-' }}</td>
              <td>{{ etudiant.moyenne_S6 || '-' }}</td>
              <td>{{ etudiant.credits_S6 || '-' }}</td>
              <td>{{ etudiant.moyenne_annuelle || '-' }}</td>
              <td>
                <span :class="getDecisionClass(etudiant.decision_jury)">
                  {{ etudiant.decision_jury || '-' }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="quickGenerateS5(etudiant)" class="btn btn-sm btn-primary" title="Bulletin S5">
                    <span>PDF</span>
                  </button>
                  <button @click="quickGenerateS6(etudiant)" class="btn btn-sm btn-primary" title="Bulletin S6">
                    <span>PDF</span>
                  </button>
                  <button @click="quickGenerateAnnuel(etudiant)" class="btn btn-sm btn-success" title="Bulletin Annuel">
                    <span>PDF</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal de progression -->
    <div v-if="showProgressModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Génération en Cours...</h3>
        </div>
        <div class="modal-body">
          <div class="progress-info">
            <p>{{ progressMessage }}</p>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
            </div>
            <p>{{ progressCurrent }} / {{ progressTotal }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import BulletinService from '~/services/bulletinService'

const { exportToExcel, exportToPDF } = useExport()
const bulletinService = BulletinService

useHead({ title: 'Génération des Bulletins | Bull ASUR' })

// État
const etudiants = ref([])
const selectedEtudiant = ref('')
const loading = ref(false)

// Filtres
const filters = ref({
  promotion: '2025-2026',
  semestre: '',
  statut: ''
})

// Options de génération par lot
const batchOptions = ref({
  S5: false,
  S6: false,
  annuel: false
})

// Progression
const showProgressModal = ref(false)
const progressMessage = ref('')
const progressCurrent = ref(0)
const progressTotal = ref(0)

// Statistiques
const stats = ref({
  total_etudiants: 0,
  diplomes: 0,
  admissibles: 0,
  redoublants: 0
})

// Étudiants filtrés
const filteredEtudiants = computed(() => {
  let filtered = etudiants.value
  
  if (filters.value.semestre) {
    filtered = filtered.filter(e => {
      if (filters.value.semestre === 'S5') return e.moyenne_S5
      if (filters.value.semestre === 'S6') return e.moyenne_S6
      return true
    })
  }
  
  if (filters.value.statut) {
    filtered = filtered.filter(e => e.decision_jury === filters.value.statut)
  }
  
  return filtered
})

// Vérifier si une option de lot est sélectionnée
const hasBatchOption = computed(() => {
  return batchOptions.value.S5 || batchOptions.value.S6 || batchOptions.value.annuel
})

// Charger les étudiants
const loadEtudiants = async () => {
  try {
    // Simulation - à remplacer par appel API réel
    const mockEtudiants = [
      {
        id: 1,
        matricule: 'LPASUR001',
        nom: 'DIALLO',
        prenom: 'Mamadou',
        moyenne_S5: 12.15,
        credits_S5: 28,
        moyenne_S6: 12.10,
        credits_S6: 27,
        moyenne_annuelle: 12.13,
        decision_jury: 'Diplômé(e)'
      },
      {
        id: 2,
        matricule: 'LPASUR002',
        nom: 'FALL',
        prenom: 'Aïssa',
        moyenne_S5: 10.50,
        credits_S5: 25,
        moyenne_S6: 11.20,
        credits_S6: 28,
        moyenne_annuelle: 10.85,
        decision_jury: 'Admissible'
      },
      {
        id: 3,
        matricule: 'LPASUR003',
        nom: 'BA',
        prenom: 'Ousmane',
        moyenne_S5: 8.75,
        credits_S5: 20,
        moyenne_S6: 9.20,
        credits_S6: 22,
        moyenne_annuelle: 8.98,
        decision_jury: 'Redouble la Licence 3'
      }
    ]
    
    etudiants.value = mockEtudiants
    calculateStats()
  } catch (error) {
    console.error('Erreur chargement étudiants:', error)
  }
}

// Calculer les statistiques
const calculateStats = () => {
  stats.value.total_etudiants = etudiants.value.length
  stats.value.diplomes = etudiants.value.filter(e => e.decision_jury === 'Diplômé(e)').length
  stats.value.admissibles = etudiants.value.filter(e => e.decision_jury === 'Admissible').length
  stats.value.redoublants = etudiants.value.filter(e => e.decision_jury === 'Redouble la Licence 3').length
}

// Appliquer les filtres
const applyFilters = () => {
  // Les filtres sont appliqués automatiquement via le computed
  console.log('Filtres appliqués:', filters.value)
}

// Réinitialiser les filtres
const resetFilters = () => {
  filters.value = {
    promotion: '2025-2026',
    semestre: '',
    statut: ''
  }
}

// Générer bulletin S5
const generateBulletinS5 = () => {
  const etudiant = etudiants.value.find(e => e.id === parseInt(selectedEtudiant.value))
  if (!etudiant) return
  
  console.log(`Génération bulletin S5 pour ${etudiant.nom} ${etudiant.prenom}`)
  // Ici on appellerait le service de génération PDF
}

// Générer bulletin S6
const generateBulletinS6 = () => {
  const etudiant = etudiants.value.find(e => e.id === parseInt(selectedEtudiant.value))
  if (!etudiant) return
  
  console.log(`Génération bulletin S6 pour ${etudiant.nom} ${etudiant.prenom}`)
}

// Générer bulletin annuel
const generateBulletinAnnuel = () => {
  const etudiant = etudiants.value.find(e => e.id === parseInt(selectedEtudiant.value))
  if (!etudiant) return
  
  console.log(`Génération bulletin annuel pour ${etudiant.nom} ${etudiant.prenom}`)
}

// Générer bulletins par lot
const generateBatchBulletins = async () => {
  showProgressModal.value = true
  progressMessage.value = 'Préparation de la génération...'
  progressTotal.value = filteredEtudiants.value.length
  progressCurrent.value = 0
  
  for (let i = 0; i < filteredEtudiants.value.length; i++) {
    const etudiant = filteredEtudiants.value[i]
    progressCurrent.value = i + 1
    progressMessage.value = `Génération pour ${etudiant.nom} ${etudiant.prenom}...`
    
    // Simulation de traitement
    await new Promise(resolve => setTimeout(resolve, 500))
    
    if (batchOptions.value.S5) {
      console.log(`Génération S5 pour ${etudiant.nom}`)
    }
    if (batchOptions.value.S6) {
      console.log(`Génération S6 pour ${etudiant.nom}`)
    }
    if (batchOptions.value.annuel) {
      console.log(`Génération annuel pour ${etudiant.nom}`)
    }
  }
  
  progressMessage.value = 'Génération terminée!'
  setTimeout(() => {
    showProgressModal.value = false
  }, 2000)
}

// Export Excel
const exportReleveS5 = () => {
  try {
    const exportData = bulletinService.exportExcelReleveNotes(filteredEtudiants.value, 5)
    console.log('Export Excel S5:', exportData.filename)
  } catch (error) {
    console.error('Erreur export Excel S5:', error)
  }
}

const exportReleveS6 = () => {
  try {
    const exportData = bulletinService.exportExcelReleveNotes(filteredEtudiants.value, 6)
    console.log('Export Excel S6:', exportData.filename)
  } catch (error) {
    console.error('Erreur export Excel S6:', error)
  }
}

const exportDecisionsJury = () => {
  try {
    const exportData = bulletinService.exportExcelDecisionsJury(filteredEtudiants.value)
    console.log('Export décisions jury:', exportData.filename)
  } catch (error) {
    console.error('Erreur export décisions jury:', error)
  }
}

const exportRelevePDF = (semestre) => {
  const headers = ['Matricule', 'Nom', 'Prénom', `Moyenne S${semestre}`, `Crédits S${semestre}`]
  const rows = filteredEtudiants.value.map(e => [
    e.matricule,
    e.nom,
    e.prenom,
    e[`moyenne_S${semestre}`] || '-',
    e[`credits_S${semestre}`] || '-'
  ])
  exportToPDF(headers, rows, `releve_notes_S${semestre}.pdf`, 'p')
}

const exportDecisionsPDF = (orientation = 'p') => {
  const headers = ['Matricule', 'Nom', 'Prénom', 'Moy. Annuelle', 'Décision']
  const rows = filteredEtudiants.value.map(e => [
    e.matricule,
    e.nom,
    e.prenom,
    e.moyenne_annuelle || '-',
    e.decision_jury || 'En attente'
  ])
  exportToPDF(headers, rows, 'decisions_jury.pdf', orientation)
}

// Génération rapide depuis le tableau
const quickGenerateS5 = (etudiant) => {
  console.log(`Génération rapide S5 pour ${etudiant.nom} ${etudiant.prenom}`)
}

const quickGenerateS6 = (etudiant) => {
  console.log(`Génération rapide S6 pour ${etudiant.nom} ${etudiant.prenom}`)
}

const quickGenerateAnnuel = (etudiant) => {
  console.log(`Génération rapide annuel pour ${etudiant.nom} ${etudiant.prenom}`)
}

// Obtenir classe CSS pour décision
const getDecisionClass = (decision) => {
  if (!decision) return ''
  
  switch (decision) {
    case 'Diplômé(e)':
      return 'decision-success'
    case 'Admissible':
      return 'decision-warning'
    case 'Redouble la Licence 3':
      return 'decision-danger'
    default:
      return ''
  }
}

onMounted(() => {
  loadEtudiants()
})
</script>

<style scoped>
.page-bulletins {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.page-header h2 {
  font-size: 1.75rem;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.page-header p {
  color: var(--text-muted);
  font-size: 1rem;
}

.filters-section {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid var(--border);
}

.filter-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.filter-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-main);
}

.filter-actions {
  display: flex;
  gap: 1rem;
}

.stats-section {
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1.5rem;
  text-align: center;
  border: 1px solid var(--border);
  border-left: 4px solid var(--primary);
}

.stat-card.success {
  border-left-color: var(--success);
}

.stat-card.warning {
  border-left-color: var(--warning);
}

.stat-card.danger {
  border-left-color: var(--danger);
}

.stat-card h4 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: var(--text-main);
}

.stat-card p {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.actions-section {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid var(--border);
}

.actions-section h3 {
  margin-bottom: 1.5rem;
  color: var(--text-main);
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: var(--bg-color);
  border-radius: var(--radius);
  padding: 1.5rem;
  border: 1px solid var(--border);
}

.action-card h4 {
  margin-bottom: 0.5rem;
  color: var(--primary);
}

.action-card p {
  color: var(--text-muted);
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.action-controls {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.button-group {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--radius);
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
}

.btn-success {
  background: var(--success);
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #059669;
}

.btn-secondary {
  background: var(--bg-color);
  color: var(--text-main);
  border: 1px solid var(--border);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--border);
}

.btn-info {
  background: var(--info);
  color: white;
}

.btn-info:hover:not(:disabled) {
  background: #0284c7;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 0.95rem;
  background: var(--bg-color);
  color: var(--text-main);
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
}

.table-section {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1.5rem;
  border: 1px solid var(--border);
}

.table-section h3 {
  margin-bottom: 1.5rem;
  color: var(--text-main);
}

.table-container {
  overflow-x: auto;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
}

.students-table th,
.students-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

.students-table th {
  background: var(--bg-color);
  font-weight: 600;
  color: var(--text-main);
}

.students-table tr:hover {
  background: var(--bg-color);
}

.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.decision-success {
  color: var(--success);
  font-weight: 600;
}

.decision-warning {
  color: var(--warning);
  font-weight: 600;
}

.decision-danger {
  color: var(--danger);
  font-weight: 600;
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
  padding: 2rem;
  max-width: 500px;
  width: 90%;
}

.modal-header h3 {
  margin-bottom: 1rem;
  color: var(--text-main);
}

.progress-info p {
  margin-bottom: 1rem;
  color: var(--text-main);
}

.progress-bar {
  width: 100%;
  height: 20px;
  background: var(--bg-color);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: var(--primary);
  transition: width 0.3s ease;
}

@media (max-width: 768px) {
  .filter-row {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
  
  .button-group {
    flex-direction: column;
  }
  
  .filter-actions {
    flex-direction: column;
  }
}
</style>
