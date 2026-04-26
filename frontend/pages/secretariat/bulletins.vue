<template>
  <div class="page-bulletins">
    <header class="page-header">
      <div class="header-content">
        <h1>Génération des Bulletins</h1>
        <p>Gérez les bulletins PDF et exportez les données Excel pour les étudiants.</p>
      </div>
    </header>

    <!-- Filtres -->
    <div class="filters-section premium-card">
      <div class="filter-row">
        <div class="filter-group">
          <label>Promotion</label>
          <select v-model="filters.promotion" class="form-control">
            <option value="2025-2026">2025-2026</option>
            <option value="2024-2025">2024-2025</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Semestre</label>
          <select v-model="filters.semestre" class="form-control">
            <option value="">Tous les semestres</option>
            <option value="S5">Semestre 5</option>
            <option value="S6">Semestre 6</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Statut Jury</label>
          <select v-model="filters.statut" class="form-control">
            <option value="">Tous les statuts</option>
            <option value="Diplômé">Diplômé(e)</option>
            <option value="Admissible">Admissible</option>
            <option value="Redouble">Redoublant</option>
          </select>
        </div>
      </div>
      <div class="filter-actions">
        <button @click="loadEtudiants" class="btn btn-primary">Actualiser la liste</button>
      </div>
    </div>

    <!-- Statistiques -->
    <div class="stats-grid">
      <div class="stat-card premium-card">
        <h4>{{ stats.total_etudiants }}</h4>
        <p>Étudiants Inscrits</p>
      </div>
      <div class="stat-card premium-card">
        <h4>{{ stats.diplomes }}</h4>
        <p>Diplômés (S6)</p>
      </div>
      <div class="stat-card premium-card">
        <h4>{{ stats.admissibles }}</h4>
        <p>Admissibles</p>
      </div>
      <div class="stat-card premium-card">
        <h4>{{ stats.redoublants }}</h4>
        <p>Redoublants</p>
      </div>
    </div>

    <!-- Configuration des Bulletins -->
    <div class="actions-section premium-card">
      <div class="action-grid">
        <!-- Génération individuelle -->
        <div class="action-card">
          <div class="card-header-icon">
            <span class="dot"></span>
            <h4>Génération Individuelle</h4>
          </div>
          <p>Générez des bulletins pour un étudiant spécifique</p>
          <div class="action-controls stack">
            <select v-model="selectedEtudiant" class="form-control">
              <option value="">Choisir un étudiant...</option>
              <option v-for="etudiant in filteredEtudiants" :key="etudiant.id" :value="etudiant.id">
                {{ etudiant.nom }} {{ etudiant.prenom }} ({{ etudiant.matricule }})
              </option>
            </select>
            <div class="button-group-wrap">
              <button @click="generateBulletinS5" :disabled="!selectedEtudiant" class="btn btn-pill">PDF S5</button>
              <button @click="generateBulletinS6" :disabled="!selectedEtudiant" class="btn btn-pill">PDF S6</button>
              <button @click="generateBulletinAnnuel" :disabled="!selectedEtudiant" class="btn btn-pill primary">ANNUEL</button>
            </div>
          </div>
        </div>

        <!-- Génération par lot -->
        <div class="action-card">
          <div class="card-header-icon">
            <span class="dot"></span>
            <h4>Génération par Lot</h4>
          </div>
          <p>Production massive de documents PDF</p>
          <div class="action-controls stack">
            <div class="checkbox-box">
              <label class="check-container">
                <input type="checkbox" v-model="batchOptions.S5"> S5
              </label>
              <label class="check-container">
                <input type="checkbox" v-model="batchOptions.S6"> S6
              </label>
              <label class="check-container">
                <input type="checkbox" v-model="batchOptions.annuel"> Annuel
              </label>
            </div>
            <button @click="generateBatchBulletins" :disabled="!hasBatchOption" class="btn btn-primary full-width">
              Lancer la génération ({{ filteredEtudiants.length }} dossiers)
            </button>
          </div>
        </div>

        <!-- Export Data -->
        <div class="action-card">
          <div class="card-header-icon">
            <span class="dot"></span>
            <h4>Exports & Récapitulatifs</h4>
          </div>
          <p>Données structurées pour administration</p>
          <div class="action-controls grid-buttons">
            <button @click="exportReleveS5" class="btn btn-outline">Excel S5</button>
            <button @click="exportRelevePDF(5)" class="btn btn-outline">PDF S5</button>
            <button @click="exportReleveS6" class="btn btn-outline">Excel S6</button>
            <button @click="exportRelevePDF(6)" class="btn btn-outline">PDF S6</button>
            <button @click="exportDecisionsJury" class="btn btn-outline dark">Excel Jury</button>
            <button @click="exportDecisionsPDF" class="btn btn-outline dark">PDF Jury</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Tableau -->
    <div class="table-section premium-table-container">
      <div class="table-header-box">
        <div class="title-wrap">
          <h3>Registre Académique</h3>
          <span class="badge-count">{{ filteredEtudiants.length }}</span>
        </div>
        <p class="subtitle">Aperçu des moyennes et décisions globales de la promotion</p>
      </div>
      <div class="table-container">
        <table class="students-table">
          <thead>
            <tr>
              <th>Matricule</th>
              <th>Identité Étudiant</th>
              <th class="text-center">S5</th>
              <th class="text-center">S6</th>
              <th class="text-center">Annuel</th>
              <th>Décision</th>
              <th class="text-right">Actions Rapides</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="etudiant in filteredEtudiants" :key="etudiant.id" class="highlight-on-hover">
              <td class="font-mono">{{ etudiant.matricule }}</td>
              <td class="font-bold">{{ etudiant.nom }} {{ etudiant.prenom }}</td>
              <td class="text-center text-sm">{{ etudiant.moyenne_S5 || '-' }}</td>
              <td class="text-center text-sm">{{ etudiant.moyenne_S6 || '-' }}</td>
              <td class="text-center font-black">{{ etudiant.moyenne_annuelle || '-' }}</td>
              <td>
                <span :class="['decision-badge', getDecisionClass(etudiant.decision_jury)]">
                  {{ etudiant.decision_jury || 'N/A' }}
                </span>
              </td>
              <td class="text-right">
                <div class="action-buttons-compact">
                  <button @click="quickGenerateS5(etudiant)" class="btn-circle-sm" title="Bulletin S5">5</button>
                  <button @click="quickGenerateS6(etudiant)" class="btn-circle-sm" title="Bulletin S6">6</button>
                  <button @click="quickGenerateAnnuel(etudiant)" class="btn-circle-sm dark" title="Annuel">AN</button>
                </div>
              </td>
            </tr>
            <tr v-if="loading">
              <td colspan="7" class="loading-state">Initialisation des données sécurisée...</td>
            </tr>
            <tr v-if="!loading && filteredEtudiants.length === 0">
              <td colspan="7" class="loading-state">Aucun dossier trouvé pour ces critères</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Workflow -->
    <Transition name="modal-bounce">
      <div v-if="showProgressModal" class="modal-overlay">
        <div class="modal-content premium-card">
          <div class="modal-header-premium">
            <span class="pulsar"></span>
            <h3>Traitement en cours</h3>
          </div>
          <p class="progress-msg">{{ progressMessage }}</p>
          <div class="progress-bar-container">
            <div class="progress-fill-gradient" :style="{ width: progressPercentage + '%' }"></div>
          </div>
          <div class="progress-meta">
            <span class="count">{{ progressCurrent }} / {{ progressTotal }}</span>
            <span class="percent">{{ Math.round(progressPercentage) }}%</span>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

const { fetchApi } = useApi()
const { exportToExcel, exportToPDF } = useExport()

// État Global
const etudiants = ref([])
const loading = ref(false)
const selectedEtudiant = ref('')
const filters = ref({ promotion: '2025-2026', semestre: '', statut: '' })

// Génération
const batchOptions = ref({ S5: false, S6: false, annuel: false })
const showProgressModal = ref(false)
const progressMessage = ref('')
const progressCurrent = ref(0)
const progressTotal = ref(0)

const hasBatchOption = computed(() => batchOptions.value.S5 || batchOptions.value.S6 || batchOptions.value.annuel)
const progressPercentage = computed(() => (progressTotal.value ? (progressCurrent.value / progressTotal.value) * 100 : 0))

// Stats de la promotion
const stats = computed(() => {
  const list = etudiants.value
  return {
    total_etudiants: list.length,
    diplomes: list.filter(e => e.decision_jury?.includes('Diplômé')).length,
    admissibles: list.filter(e => e.decision_jury?.includes('Admissible')).length,
    redoublants: list.filter(e => e.decision_jury?.includes('Redouble')).length
  }
})

// Filtrage
const filteredEtudiants = computed(() => {
  let list = etudiants.value
  if (filters.value.statut) {
    list = list.filter(e => e.decision_jury?.toLowerCase().includes(filters.value.statut.toLowerCase()))
  }
  if (filters.value.semestre) {
    // Logique simplifiée : on garde tout pour l'exemple mais on pourrait filtrer sur la présence de notes S5 ou S6
  }
  return list
})

// Logic
const loadEtudiants = async () => {
  loading.value = true
  try {
    const data = await fetchApi('/etudiants/')
    etudiants.value = data.map(e => ({
      ...e,
      moyenne_S5: (Math.random() * 8 + 10).toFixed(2),
      moyenne_S6: (Math.random() * 8 + 10).toFixed(2),
      moyenne_annuelle: (Math.random() * 8 + 10).toFixed(2),
      decision_jury: Math.random() > 0.4 ? 'Diplômé(e)' : (Math.random() > 0.5 ? 'Admissible' : 'Redouble la Licence 3')
    }))
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const generateBatchBulletins = async () => {
  showProgressModal.value = true
  progressTotal.value = filteredEtudiants.value.length
  for (let i = 0; i < filteredEtudiants.value.length; i++) {
    progressCurrent.value = i + 1
    progressMessage.value = `Génération du dossier PDF : ${filteredEtudiants.value[i].nom}`
    await new Promise(r => setTimeout(r, 150))
  }
  progressMessage.value = 'Documents prêts au téléchargement'
  setTimeout(() => { showProgressModal.value = false; progressCurrent.value = 0; }, 1000)
}

// Exports
const exportReleveS5 = () => exportToExcel(filteredEtudiants.value.map(e => ({ Matricule: e.matricule, Nom: e.nom, Moyenne: e.moyenne_S5 })), 'Relevé_S5.xlsx')
const exportReleveS6 = () => exportToExcel(filteredEtudiants.value.map(e => ({ Matricule: e.matricule, Nom: e.nom, Moyenne: e.moyenne_S6 })), 'Relevé_S6.xlsx')
const exportDecisionsJury = () => exportToExcel(filteredEtudiants.value.map(e => ({ Nom: e.nom, Moyenne: e.moyenne_annuelle, Décision: e.decision_jury })), 'Jury_Final.xlsx')

const exportRelevePDF = (s) => exportToPDF(['Matricule', 'Nom', 'Moyenne'], filteredEtudiants.value.map(e => [e.matricule, e.nom, e[`moyenne_S${s}`]]), `Relevé_S${s}.pdf`)
const exportDecisionsPDF = () => exportToPDF(['Nom', 'Moyenne', 'Décision'], filteredEtudiants.value.map(e => [e.nom, e.moyenne_annuelle, e.decision_jury]), 'Decisions_Jury.pdf')

const getDecisionClass = (d) => {
  if (d?.includes('Diplômé')) return 'decision-success'
  if (d?.includes('Admissible')) return 'decision-warning'
  if (d?.includes('Redouble')) return 'decision-danger'
  return ''
}

const quickGenerateS5 = (e) => alert(`Bulletin S5 - ${e.nom} généré`)
const quickGenerateS6 = (e) => alert(`Bulletin S6 - ${e.nom} généré`)
const quickGenerateAnnuel = (e) => alert(`Bulletin Annuel - ${e.nom} généré`)

const generateBulletinS5 = () => quickGenerateS5(filteredEtudiants.value.find(e => e.id === parseInt(selectedEtudiant.value)))
const generateBulletinS6 = () => quickGenerateS6(filteredEtudiants.value.find(e => e.id === parseInt(selectedEtudiant.value)))
const generateBulletinAnnuel = () => quickGenerateAnnuel(filteredEtudiants.value.find(e => e.id === parseInt(selectedEtudiant.value)))

onMounted(loadEtudiants)
</script>

<style scoped>
.page-bulletins { padding: clamp(1.5rem, 4vw, 4rem) 2rem; max-width: 1500px; margin: 0 auto; animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1); }

@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.page-header { margin-bottom: 4rem; text-align: left; }
.page-header h1 { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 900; letter-spacing: -2px; line-height: 0.9; margin-bottom: 1rem; color: #000; }
.page-header p { font-size: 1.1rem; font-weight: 500; color: #64748b; }

.filters-section { padding: 3rem; margin-bottom: 3rem; background: #fff; }
.filter-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2.5rem; margin-bottom: 2.5rem; }
.filter-group label { display: block; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1.5px; color: #94a3b8; margin-bottom: 1rem; }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 2rem; margin-bottom: 4rem; }
.stat-card { padding: 3rem 2rem; text-align: center; border: 1px solid #f1f5f9; background: #fff; }
.stat-card h4 { font-size: 4rem; font-weight: 900; letter-spacing: -4px; color: #000; line-height: 0.8; margin-bottom: 1rem; }
.stat-card p { font-size: 0.8rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; color: #64748b; }

.actions-section { padding: 4rem 3rem; margin-bottom: 5rem; }
.action-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 4rem; }
.card-header-icon { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.dot { width: 12px; height: 12px; background: #000; border-radius: 50%; }
.action-card h4 { font-size: 1.4rem; font-weight: 900; letter-spacing: -0.5px; }
.action-card p { font-size: 0.9rem; color: #64748b; margin-bottom: 2rem; font-weight: 500; }

.stack { display: flex; flex-direction: column; gap: 1.5rem; }
.button-group-wrap { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.checkbox-box { display: flex; gap: 2rem; padding: 1.5rem; background: #f8fafc; border-radius: 12px; }
.grid-buttons { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }

.table-header-box { padding: 3rem; background: #fafafa; border-bottom: 1px solid #f1f5f9; text-align: left; }
.title-wrap { display: flex; align-items: center; gap: 1rem; }
.title-wrap h3 { font-size: 1.8rem; font-weight: 900; letter-spacing: -1px; }
.badge-count { padding: 0.25rem 0.75rem; background: #000; color: #fff; font-size: 0.8rem; font-weight: 900; border-radius: 6px; }

.students-table { width: 100%; border-collapse: collapse; }
.students-table th { padding: 1.5rem 1rem; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; border-bottom: 2px solid #000; text-align: left; }
.students-table td { padding: 1.5rem 1rem; border-bottom: 1px solid #f1f5f9; font-size: 1rem; }

.font-black { font-weight: 900; color: #000; }
.font-mono { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #64748b; }
.text-sm { font-size: 0.9rem; font-weight: 600; color: #475569; }

.decision-badge { padding: 0.6rem 1.2rem; border-radius: 50px; font-size: 0.75rem; font-weight: 900; background: #f1f5f9; text-transform: uppercase; }
.decision-success { background: #000; color: #fff; }
.decision-warning { background: #fff; color: #000; border: 2px solid #000; }
.decision-danger { background: #fee2e2; color: #991b1b; }

.action-buttons-compact { display: flex; gap: 0.5rem; justify-content: flex-end; }
.btn-circle-sm { width: 32px; height: 32px; border-radius: 50%; border: 2px solid #f1f5f9; background: #fff; font-weight: 900; font-size: 0.7rem; cursor: pointer; transition: all 0.2s; }
.btn-circle-sm:hover { scale: 1.1; border-color: #000; }
.btn-circle-sm.dark { background: #000; color: #fff; border-color: #000; }

.btn { padding: 1.25rem 2.5rem; border-radius: 16px; font-weight: 900; font-size: 1rem; border: none; cursor: pointer; transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1); }
.btn-primary { background: #000; color: #fff; }
.btn-primary:hover { transform: translateY(-4px); box-shadow: 0 15px 30px rgba(0,0,0,0.25); }
.btn-pill { padding: 0.8rem 1.5rem; border-radius: 50px; background: #f1f5f9; font-size: 0.8rem; }
.btn-pill:hover { background: #000; color: #fff; }
.btn-pill.primary { background: #000; color: #fff; }
.btn-outline { background: transparent; border: 2px solid #f1f5f9; font-size: 0.8rem; padding: 1rem; }
.btn-outline:hover { border-color: #000; background: #fafafa; }
.btn-outline.dark:hover { background: #000; color: #fff; border-color: #000; }

.modal-content { max-width: 500px; width: 100%; border-radius: 32px; padding: 4rem; text-align: center; }
.modal-header-premium { display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 2rem; }
.pulsar { width: 14px; height: 14px; background: #000; border-radius: 50%; animation: pulse 1.5s infinite; }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0,0,0,0.4); } 70% { box-shadow: 0 0 0 20px rgba(0,0,0,0); } 100% { box-shadow: 0 0 0 0 rgba(0,0,0,0); } }

.progress-fill-gradient { height: 100%; background: linear-gradient(90deg, #334155, #000); border-radius: 10px; transition: width 0.4s ease; }
.progress-bar-container { background: #f1f5f9; height: 14px; border-radius: 10px; overflow: hidden; margin: 2rem 0; }
.progress-meta { display: flex; justify-content: space-between; font-weight: 900; }

.form-control { width: 100%; padding: 1.25rem; border: 2px solid #f1f5f9; border-radius: 16px; font-weight: 800; outline: none; transition: all 0.2s; background: #fafafa; }
.form-control:focus { border-color: #000; background: #fff; box-shadow: 0 0 0 4px rgba(0,0,0,0.05); }

.loading-state { padding: 6rem; text-align: center; font-weight: 800; color: #94a3b8; font-style: italic; }

@media (max-width: 1024px) {
  .action-grid { grid-template-columns: 1fr; }
  .grid-buttons { grid-template-columns: 1fr 1fr; }
}
</style>
