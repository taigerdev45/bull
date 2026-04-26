<template>
  <div class="page-modification-notes">
    <header class="page-header">
      <div class="header-content">
        <h1>Console de Notation</h1>
        <p>Révision et validation terminale des performances académiques.</p>
      </div>
    </header>

    <!-- Filtres Dynamiques -->
    <div class="filters-panel premium-card">
      <div class="filter-row">
        <div class="filter-group">
          <label>Cycle de Formation</label>
          <select v-model="filters.semestre_id" @change="loadData" class="form-control">
            <option value="">Sélectionner un semestre...</option>
            <option v-for="s in semestres" :key="s.id" :value="s.id">{{ s.libelle }}</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>Unité d'Enseignement</label>
          <select v-model="filters.ue_id" @change="loadMatieres" class="form-control">
            <option value="">Toutes les UE</option>
            <option v-for="ue in filteredUEs" :key="ue.id" :value="ue.id">{{ ue.libelle }}</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>Matière Spécifique</label>
          <select v-model="filters.matiere_id" @change="loadNotes" class="form-control">
            <option value="">Toutes les matières</option>
            <option v-for="m in filteredMatieres" :key="m.id" :value="m.id">{{ m.libelle }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Interface de Notation -->
    <div v-if="filters.semestre_id" class="notes-workspace animate-in">
      <div class="workspace-header">
        <div class="ctx">
          <h3>Table de Notation : {{ getMatiereLibelle(filters.matiere_id) }}</h3>
          <p v-if="hasChanges" class="unsaved-warn">⚠️ Modifications non synchronisées</p>
        </div>
        <div class="ctx-actions">
          <div class="export-dropdown" v-if="etudiants.length">
            <button class="btn btn-pill dark">Export ↓</button>
            <div class="dropdown-menu premium-card">
              <button @click="exportNotes('excel')">Journal Excel</button>
              <button @click="exportNotes('pdf')">Rapport PDF</button>
            </div>
          </div>
          <button class="btn btn-primary btn-pill shadow-strong" @click="saveAllNotes" :disabled="!hasChanges || loading">
            {{ loading ? 'Synchronisation...' : 'Valider & Enregistrer' }}
          </button>
        </div>
      </div>

      <div class="premium-table-container">
        <table class="grading-table">
          <thead>
            <tr>
              <th>Identité & Matricule</th>
              <th v-for="type in evaluationTypes" :key="type.key" class="text-center">{{ type.label }}</th>
              <th class="text-center">Moyenne</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="etudiant in etudiants" :key="etudiant.id" class="highlight-on-hover">
              <td class="student-profile">
                <span class="name">{{ etudiant.nom }} {{ etudiant.prenom }}</span>
                <span class="id">{{ etudiant.matricule }}</span>
              </td>
              
              <td v-for="type in evaluationTypes" :key="type.key" class="cell-input">
                <input 
                  type="number" 
                  :value="getNoteValue(etudiant.id, type.key)"
                  @input="updateNote(etudiant.id, type.key, $event.target.value)"
                  min="0" max="20" step="0.5"
                  class="grade-input"
                  :class="{ 'modified': isNoteModified(etudiant.id, type.key) }"
                />
              </td>
              
              <td class="cell-moyenne">
                <span :class="['grade-badge', getMoyenneClass(calculerMoyenne(etudiant.id))]">
                  {{ calculerMoyenne(etudiant.id).toFixed(2) }}
                </span>
              </td>
              
              <td class="text-right">
                <div class="action-buttons-compact">
                  <button class="btn-circle-sm" @click="showHistory(etudiant.id)" title="Historique">🕒</button>
                  <button class="btn-circle-sm danger" @click="deleteStudentNotes(etudiant.id)" title="Réinitialiser">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Stats Summary -->
      <div class="notation-stats premium-card">
        <div class="s-tile">
          <span class="l">Moyenne Groupe</span>
          <span class="v">{{ stats.moyenneGenerale.toFixed(2) }}</span>
        </div>
        <div class="s-tile">
          <span class="l">Major de Promo</span>
          <span class="v">{{ stats.noteMax.toFixed(2) }}</span>
        </div>
        <div class="s-tile">
          <span class="l">Taux de Réussite</span>
          <span class="v highlight">{{ stats.tauxReussite.toFixed(1) }}%</span>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state-p premium-card">
      <div class="icon">🔍</div>
      <h3>Consultation des registres</h3>
      <p>Veuillez définir un prisme de recherche (Semestre/UE) pour charger les notes.</p>
    </div>

    <!-- Modal Historique -->
    <Transition name="modal-bounce">
      <div v-if="showHistoryModal" class="modal-overlay" @click="closeHistoryModal">
        <div class="modal-content premium-card">
          <div class="modal-header-premium">
            <span class="pulsar"></span>
            <h3>Historique de Traçabilité</h3>
          </div>
          <div class="history-scroll">
            <div v-for="mod in selectedHistory" :key="mod.id" class="history-log-item">
              <div class="log-head">
                <span class="date">{{ formatDate(mod.date) }}</span>
                <span class="type">{{ mod.type_evaluation }}</span>
              </div>
              <div class="log-body">
                <span class="old">{{ mod.ancienne_valeur }}</span>
                <span class="arrow">→</span>
                <span class="new">{{ mod.nouvelle_valeur }}</span>
              </div>
              <div class="log-foot">Auteur : {{ mod.auteur }}</div>
            </div>
            <div v-if="selectedHistory.length === 0" class="no-history">Aucune modification enregistrée</div>
          </div>
          <div class="form-actions-premium">
            <button class="btn btn-primary btn-pill" @click="closeHistoryModal">Fermer</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useApi } from '~/composables/useApi'

const { fetchApi } = useApi()
const { exportToExcel, exportToPDF } = useExport()
useHead({ title: 'Console de Notation | Bull ASUR' })

// État
const loading = ref(false)
const showHistoryModal = ref(false)
const selectedHistory = ref([])
const semestres = ref([]); const ues = ref([]); const matieres = ref([]); const etudiants = ref([])
const evaluations = ref([]); const originalEvaluations = ref([])
const filters = ref({ semestre_id: '', ue_id: '', matiere_id: '' })

const evaluationTypes = [
  { key: 'CC', label: 'Contrôle Continu' },
  { key: 'EXAMEN', label: 'Examen Final' },
  { key: 'RATTRAPAGE', label: 'Rattrapage' }
]

// Computed
const filteredUEs = computed(() => filters.value.semestre_id ? ues.value.filter(u => u.semestre_id === filters.value.semestre_id) : [])
const filteredMatieres = computed(() => filters.value.ue_id ? matieres.value.filter(m => m.ue_id === filters.value.ue_id) : [])
const hasChanges = computed(() => JSON.stringify(evaluations.value) !== JSON.stringify(originalEvaluations.value))

const stats = computed(() => {
  const ms = etudiants.value.map(e => calculerMoyenne(e.id)).filter(m => m > 0)
  return {
    moyenneGenerale: ms.length ? ms.reduce((a, b) => a + b, 0) / ms.length : 0,
    noteMax: ms.length ? Math.max(...ms) : 0,
    tauxReussite: ms.length ? (ms.filter(m => m >= 10).length / ms.length) * 100 : 0
  }
})

// Logic
const loadInitial = async () => {
  const [s, u, m, e] = await Promise.all([fetchApi('/semestres/'), fetchApi('/ues/'), fetchApi('/matieres/'), fetchApi('/etudiants/')])
  semestres.value = s; ues.value = u; matieres.value = m; etudiants.value = e
}

const loadNotes = async () => {
  if (!filters.value.matiere_id) return
  const data = await fetchApi(`/evaluations/matiere/${filters.value.matiere_id}/`)
  evaluations.value = data || []
  originalEvaluations.value = JSON.parse(JSON.stringify(evaluations.value))
}

const updateNote = (eid, type, val) => {
  const n = parseFloat(val); if (isNaN(n) || n < 0 || n > 20) return
  const idx = evaluations.value.findIndex(e => e.etudiant_id === eid && e.type === type)
  if (idx !== -1) evaluations.value[idx].note = n
  else evaluations.value.push({ etudiant_id: eid, matiere_id: filters.value.matiere_id, type, note: n })
}

const getNoteValue = (eid, type) => evaluations.value.find(e => e.etudiant_id === eid && e.type === type)?.note || ''
const isNoteModified = (eid, type) => getNoteValue(eid, type) !== (originalEvaluations.value.find(e => e.etudiant_id === eid && e.type === type)?.note || '')

const calculerMoyenne = (eid) => {
  const evs = evaluations.value.filter(e => e.etudiant_id === eid)
  const cc = evs.find(e => e.type === 'CC')?.note || 0
  const ex = evs.find(e => e.type === 'EXAMEN')?.note || 0
  const rat = evs.find(e => e.type === 'RATTRAPAGE')?.note
  if (rat && rat > Math.min(cc, ex)) return (Math.max(cc, ex) * 0.6 + rat * 0.4)
  return (cc * 0.4 + ex * 0.6)
}

const getMoyenneClass = (m) => m >= 14 ? 'excellent' : (m >= 10 ? 'passable' : 'fail')

const saveAllNotes = async () => {
  loading.value = true
  try {
    await fetchApi('/evaluations/bulk/', { method: 'POST', body: { matiere_id: filters.value.matiere_id, evaluations: evaluations.value } })
    await loadNotes()
  } catch (err) { alert("Erreur d'enregistrement") } finally { loading.value = false }
}

const exportNotes = (fmt) => {
  const data = etudiants.value.map(e => ({ Étudiant: `${e.nom} ${e.prenom}`, Moyenne: calculerMoyenne(e.id).toFixed(2) }))
  if (fmt === 'excel') exportToExcel(data, 'Notes.xlsx')
  else exportToPDF(['Étudiant', 'Moyenne'], etudiants.value.map(e => [`${e.nom} ${e.prenom}`, calculerMoyenne(e.id).toFixed(2)]), 'Notes.pdf')
}

const showHistory = async (id) => {
  // Mock history for demo or real API
  selectedHistory.value = [
    { id: 1, date: new Date(), type_evaluation: 'CC', ancienne_valeur: 10, nouvelle_valeur: 14, auteur: 'Admin' }
  ]
  showHistoryModal.value = true
}

const closeHistoryModal = () => { showHistoryModal.value = false; selectedHistory.value = [] }
const formatDate = (d) => new Date(d).toLocaleString()
const getMatiereLibelle = (id) => matieres.value.find(m => m.id === id)?.libelle || 'Matière'

onMounted(loadInitial)
watch(() => filters.value.ue_id, () => { filters.value.matiere_id = ''; evaluations.value = [] })
</script>

<style scoped>
.page-modification-notes { padding: clamp(1.5rem, 4vw, 4rem) 2rem; max-width: 1600px; margin: 0 auto; }

.page-header { margin-bottom: 4rem; }
.page-header h1 { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 950; letter-spacing: -3px; line-height: 1; }
.page-header p { color: #64748b; font-weight: 600; font-size: 1.1rem; }

.filters-panel { padding: 3rem; background: #fff; margin-bottom: 4rem; }
.filter-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2.5rem; }
.filter-group label { display: block; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1.5px; margin-bottom: 1rem; }

.form-control { width: 100%; padding: 1.25rem; border: 2.5px solid #f1f5f9; border-radius: 16px; font-weight: 800; outline: none; transition: all 0.2s; background: #fafafa; }
.form-control:focus { border-color: #000; background: #fff; }

.workspace-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 3rem; }
.workspace-header h3 { font-size: 1.8rem; font-weight: 950; letter-spacing: -1px; }
.unsaved-warn { font-size: 0.8rem; color: #e11d48; font-weight: 800; text-transform: uppercase; margin-top: 0.5rem; }
.ctx-actions { display: flex; gap: 1rem; }

.grading-table { width: 100%; border-collapse: collapse; }
.grading-table th { padding: 1.5rem 1rem; font-size: 0.7rem; font-weight: 950; text-transform: uppercase; color: #94a3b8; border-bottom: 2px solid #000; text-align: left; }
.grading-table td { padding: 1.25rem 1rem; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }

.student-profile { display: flex; flex-direction: column; }
.student-profile .name { font-weight: 800; color: #000; font-size: 1rem; }
.student-profile .id { font-size: 0.75rem; font-weight: 700; color: #94a3b8; font-family: monospace; }

.cell-input { text-align: center; }
.grade-input { width: 80px; padding: 0.8rem; border: 2px solid #f1f5f9; border-radius: 12px; text-align: center; font-weight: 900; font-size: 1rem; transition: all 0.2s; }
.grade-input:focus { border-color: #000; background: #fff; scale: 1.1; }
.grade-input.modified { border-color: #000; background: #f8fafc; }

.grade-badge { padding: 0.6rem 1.2rem; border-radius: 50px; font-weight: 900; font-size: 0.9rem; }
.grade-badge.excellent { background: #000; color: #fff; }
.grade-badge.passable { background: #f1f5f9; color: #000; }
.grade-badge.fail { border: 2px solid #000; color: #000; }

.notation-stats { display: flex; gap: 4rem; padding: 3rem; background: #000; color: #fff; margin-top: 5rem; border-radius: 32px; }
.s-tile { display: flex; flex-direction: column; gap: 0.25rem; }
.s-tile .l { font-size: 0.7rem; font-weight: 800; text-transform: uppercase; color: #64748b; }
.s-tile .v { font-size: 3rem; font-weight: 950; letter-spacing: -2px; }
.s-tile .v.highlight { color: #fff; text-decoration: underline; }

.empty-state-p { padding: 8rem; text-align: center; border: 3px dashed #f1f5f9; background: transparent; }
.empty-state-p .icon { font-size: 4rem; margin-bottom: 2rem; opacity: 0.2; }

.history-scroll { padding: 2.5rem; max-height: 50vh; overflow-y: auto; }
.history-log-item { padding: 1.5rem; border-bottom: 1px solid #f1f5f9; }
.log-head { display: flex; justify-content: space-between; margin-bottom: 0.5rem; }
.log-head .date { font-size: 0.75rem; color: #94a3b8; font-weight: 700; }
.log-head .type { font-size: 0.7rem; font-weight: 900; background: #000; color: #fff; padding: 0.2rem 0.5rem; border-radius: 4px; }
.log-body { display: flex; align-items: center; gap: 1rem; font-size: 1.2rem; font-weight: 950; margin: 1rem 0; }
.log-body .old { color: #94a3b8; text-decoration: line-through; }
.log-foot { font-size: 0.75rem; font-weight: 700; color: #64748b; }

.btn { padding: 1.1rem 2.2rem; font-weight: 900; border: none; cursor: pointer; border-radius: 14px; transition: all 0.2s; }
.btn-primary { background: #000; color: #fff; }
.btn-primary:disabled { opacity: 0.3; pointer-events: none; }
.btn-pill { border-radius: 50px; }

.modal-header-premium { padding: 2.5rem; background: #000; color: #fff; display: flex; align-items: center; gap: 1rem; }
.pulsar { width: 12px; height: 12px; background: #fff; border-radius: 50%; animation: pulse-white 1.5s infinite; }
@keyframes pulse-white { 0% { box-shadow: 0 0 0 0 rgba(255,255,255,0.4); } 70% { box-shadow: 0 0 0 15px rgba(255,255,255,0); } 100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); } }

.animate-in { animation: slideUp 0.6s ease-out; }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
