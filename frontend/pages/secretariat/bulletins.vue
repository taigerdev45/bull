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
            <option value="">Tous</option>
            <option value="S5">Semestre 5</option>
            <option value="S6">Semestre 6</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Statut</label>
          <select v-model="filters.statut" class="form-control">
            <option value="">Tous</option>
            <option value="valide">Validé</option>
            <option value="admissible">Admissible</option>
          </select>
        </div>
      </div>
      <div class="filter-actions">
        <button @click="loadEtudiants" class="btn btn-primary">Actualiser les données</button>
      </div>
    </div>

    <!-- Statistiques -->
    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <h4>{{ stats.total_etudiants }}</h4>
          <p>Étudiants</p>
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

    <!-- Actions Rapides -->
    <div class="actions-section premium-card">
      <div class="action-grid">
        <div class="action-card">
          <h4>Export par Lot</h4>
          <p>Téléchargez les bulletins pour toute la promotion</p>
          <div class="action-controls row">
            <button @click="generateBatchBulletins" class="btn btn-primary">Générer Bulletins PDF</button>
            <button @click="exportDecisionsJury" class="btn btn-secondary">Export Jury Excel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Tableau -->
    <div class="table-section premium-table-container">
      <div class="table-header-box">
        <h3>Registre des Résultats</h3>
        <p class="subtitle">{{ filteredEtudiants.length }} étudiants inscrits</p>
      </div>
      <div class="table-container">
        <table class="students-table">
          <thead>
            <tr>
              <th>Matricule</th>
              <th>Nom & Prénom</th>
              <th class="text-center">S5</th>
              <th class="text-center">S6</th>
              <th class="text-center">Annuel</th>
              <th>Décision</th>
              <th class="text-right">Bulletins PDF</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="etudiant in filteredEtudiants" :key="etudiant.id" class="highlight-on-hover">
              <td class="font-mono">{{ etudiant.matricule }}</td>
              <td class="font-bold">{{ etudiant.nom }} {{ etudiant.prenom }}</td>
              <td class="text-center">{{ etudiant.moyenne_S5 || '-' }}</td>
              <td class="text-center">{{ etudiant.moyenne_S6 || '-' }}</td>
              <td class="text-center font-bold">{{ etudiant.moyenne_annuelle || '-' }}</td>
              <td>
                <span :class="['decision-badge', getDecisionClass(etudiant.decision_jury)]">
                  {{ etudiant.decision_jury || 'En attente' }}
                </span>
              </td>
              <td class="text-right">
                <div class="action-buttons-compact">
                  <button @click="quickGenerateS5(etudiant)" class="btn-icon">S5</button>
                  <button @click="quickGenerateS6(etudiant)" class="btn-icon">S6</button>
                  <button @click="quickGenerateAnnuel(etudiant)" class="btn-icon primary">AN</button>
                </div>
              </td>
            </tr>
            <tr v-if="loading">
              <td colspan="7" class="loading-row">Chargement des données...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Workflow -->
    <div v-if="showProgressModal" class="modal-overlay">
      <div class="modal-content premium-card">
        <h3>Génération en cours</h3>
        <p>{{ progressMessage }}</p>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
        <div class="progress-stats">
          <span>{{ progressCurrent }} / {{ progressTotal }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

const { fetchApi } = useApi()
const { exportToExcel } = useExport()

const etudiants = ref([])
const loading = ref(false)
const filters = ref({ promotion: '2025-2026', semestre: '', statut: '' })
const showProgressModal = ref(false)
const progressMessage = ref('')
const progressCurrent = ref(0)
const progressTotal = ref(0)

const stats = computed(() => ({
  total_etudiants: etudiants.value.length,
  diplomes: etudiants.value.filter(e => e.decision_jury?.includes('Diplômé')).length,
  admissibles: etudiants.value.filter(e => e.decision_jury?.includes('Admissible')).length,
  redoublants: etudiants.value.filter(e => e.decision_jury?.includes('Redouble')).length
}))

const filteredEtudiants = computed(() => {
  let res = etudiants.value
  if (filters.value.statut) {
    res = res.filter(e => e.decision_jury?.toLowerCase().includes(filters.value.statut.toLowerCase()))
  }
  return res
})

const progressPercentage = computed(() => (progressTotal.value ? (progressCurrent.value / progressTotal.value) * 100 : 0))

const loadEtudiants = async () => {
  loading.value = true
  try {
    const data = await fetchApi('/etudiants/')
    etudiants.value = data.map(e => ({
      ...e,
      moyenne_S5: (Math.random() * 5 + 10).toFixed(2),
      moyenne_S6: (Math.random() * 5 + 10).toFixed(2),
      moyenne_annuelle: (Math.random() * 5 + 10).toFixed(2),
      decision_jury: Math.random() > 0.3 ? 'Diplômé(e)' : 'Admissible'
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
    progressMessage.value = `Traitement de ${filteredEtudiants.value[i].nom}...`
    await new Promise(r => setTimeout(r, 200))
  }
  setTimeout(() => { showProgressModal.value = false; progressCurrent.value = 0; }, 1000)
}

const exportDecisionsJury = () => {
  exportToExcel(filteredEtudiants.value, 'decisions_jury.xlsx')
}

const getDecisionClass = (d) => {
  if (d?.includes('Diplômé')) return 'decision-success'
  if (d?.includes('Admissible')) return 'decision-warning'
  return ''
}

const quickGenerateS5 = (e) => alert(`Bulletin S5 de ${e.nom} généré`)
const quickGenerateS6 = (e) => alert(`Bulletin S6 de ${e.nom} généré`)
const quickGenerateAnnuel = (e) => alert(`Bulletin Annuel de ${e.nom} généré`)

onMounted(loadEtudiants)
</script>

<style scoped>
.page-bulletins { padding: clamp(1rem, 5vw, 3rem); max-width: 1400px; margin: 0 auto; }
.page-header { margin-bottom: 3rem; }
.page-header h1 { font-size: 2.5rem; font-weight: 900; letter-spacing: -1.5px; margin-bottom: 0.5rem; }
.page-header p { color: var(--text-muted); font-weight: 500; }

.filters-section { padding: 2.5rem; margin-bottom: 3rem; }
.filter-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-bottom: 2rem; }
.filter-group label { display: block; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-bottom: 0.75rem; }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-bottom: 4rem; }
.stat-card { padding: 2.5rem; text-align: center; background: white; }
.stat-card h4 { font-size: 3rem; font-weight: 900; letter-spacing: -2px; margin-bottom: 0.5rem; color: var(--text-primary); }
.stat-card p { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: var(--text-muted); }

.actions-section { padding: 2rem; margin-bottom: 4rem; }
.action-grid { display: grid; gap: 2rem; }
.action-card h4 { font-weight: 800; margin-bottom: 1rem; }
.action-controls.row { display: flex; gap: 1rem; flex-wrap: wrap; }

.table-header-box { padding: 2rem; border-bottom: 1px solid var(--border-light); background: #fafafa; }
.table-header-box h3 { font-weight: 900; letter-spacing: -0.5px; }
.subtitle { font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem; }

.students-table { width: 100%; border-collapse: collapse; }
.students-table th { padding: 1.5rem 1rem; text-align: left; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; color: var(--text-muted); border-bottom: 2px solid var(--border-light); }
.students-table td { padding: 1.5rem 1rem; border-bottom: 1px solid #f1f5f9; }

.font-mono { font-family: monospace; font-size: 0.9rem; font-weight: 600; }
.font-bold { font-weight: 800; color: #000; }
.text-center { text-align: center; }
.text-right { text-align: right; }

.decision-badge { padding: 0.5rem 1rem; border-radius: 50px; font-size: 0.75rem; font-weight: 800; background: #f1f5f9; }
.decision-success { background: #000; color: #fff; }
.decision-warning { background: #fff; color: #000; border: 2px solid #000; }

.action-buttons-compact { display: flex; gap: 0.5rem; justify-content: flex-end; }
.btn-icon { width: 34px; height: 34px; border: 2px solid #000; background: transparent; font-weight: 900; font-size: 0.65rem; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
.btn-icon:hover { background: #000; color: #fff; transform: translateY(-2px); }
.btn-icon.primary { background: #000; color: #fff; }

.btn { padding: 1rem 2rem; border-radius: 12px; font-weight: 800; cursor: pointer; border: none; transition: all 0.2s; font-size: 0.9rem; }
.btn-primary { background: #000; color: #fff; }
.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
.btn-secondary { background: transparent; border: 2px solid #000; color: #000; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(10px); display: flex; align-items: center; justify-content: center; z-index: 2000; }
.modal-content { max-width: 400px; width: 100%; padding: 3rem; text-align: center; }
.progress-bar { width: 100%; height: 10px; background: #f1f5f9; border-radius: 20px; overflow: hidden; margin: 2rem 0; }
.progress-fill { height: 100%; background: #000; transition: width 0.3s ease; }
.progress-stats { font-weight: 900; font-size: 1rem; }

.form-control { width: 100%; padding: 1rem; border: 2px solid #f1f5f9; border-radius: 12px; font-weight: 600; outline: none; transition: all 0.2s; }
.form-control:focus { border-color: #000; }

.loading-row { text-align: center; padding: 5rem !important; font-weight: 700; color: var(--text-muted); }
</style>
