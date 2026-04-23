<template>
  <div class="page-container">
    <header class="page-header">
      <div class="header-info">
        <h1>Saisie des Évaluations</h1>
        <p>Enregistrez les notes par matière et par session.</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="showAddModal = true">
          <span>➕</span> Nouvelle Évaluation
        </button>
      </div>
    </header>

    <div class="filter-card">
       <div class="field">
          <label>Unité d'Enseignement</label>
          <select v-model="selectedUE">
             <option value="">Toutes les UEs</option>
             <option v-for="ue in ues" :key="ue.id" :value="ue.id">{{ ue.code }} - {{ ue.libelle }}</option>
          </select>
       </div>
       <div class="field">
          <label>Semestre</label>
          <select v-model="selectedSemestre">
             <option value="5">Semestre 5</option>
             <option value="6">Semestre 6</option>
          </select>
       </div>
    </div>

    <div v-if="pending" class="loader">
      <div class="spinner"></div>
      <p>Chargement des sessions d'examen...</p>
    </div>

    <div v-else class="evaluations-grid">
       <div v-for="evalItem in evaluations" :key="evalItem.id" class="eval-card">
          <div class="eval-badge" :class="evalItem.type.toLowerCase()">{{ evalItem.type }}</div>
          <div class="eval-main">
             <h3>{{ evalItem.matiere_libelle || 'Matière Inconnue' }}</h3>
             <p>{{ formatDate(evalItem.date) }}</p>
          </div>
          <div class="eval-stats">
             <div class="es-item">
                <span class="l">Session</span>
                <span class="v">{{ evalItem.session === 'normale' ? 'SN' : 'SR' }}</span>
             </div>
             <div class="es-item">
                <span class="l">Moyenne</span>
                <span class="v" :class="{ empty: !evalItem.moyenne_classe }">
                  {{ evalItem.moyenne_classe ? evalItem.moyenne_classe.toFixed(2) : '--' }}
                </span>
             </div>
          </div>
          <div class="eval-actions">
             <button class="btn-full" @click="enterNotes(evalItem)">Saisir les notes →</button>
          </div>
       </div>

       <div v-if="evaluations.length === 0" class="empty-state">
          <div class="empty-icon">📂</div>
          <h3>Aucune évaluation trouvée</h3>
          <p>Commencez par créer une nouvelle session d'évaluation.</p>
       </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

useHead({ title: 'Saisie Notes | Bull ASUR' })

const { fetchApi } = useApi()
const evaluations = ref([])
const ues = ref([])
const pending = ref(true)
const selectedUE = ref('')
const selectedSemestre = ref('5')

const fetchEvaluations = async () => {
  pending.value = true
  try {
    const data = await fetchApi('/evaluations/')
    if (data) evaluations.value = data
    
    const ueData = await fetchApi('/referentiels/ue/')
    if (ueData) ues.value = ueData
  } catch (e) {
    console.error('Fetch error', e)
  } finally {
    pending.value = false
  }
}

onMounted(fetchEvaluations)

const formatDate = (d) => {
  if (!d) return 'Date non définie'
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

const enterNotes = (evalItem) => {
  navigateTo(`/saisie/${evalItem.id}`)
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; }
.header-info h1 { font-size: 1.75rem; font-weight: 800; color: #1e293b; margin: 0; }
.header-info p { color: #64748b; font-size: 1rem; margin: 0.25rem 0 0; }

.filter-card { background: white; padding: 1.5rem; border-radius: var(--radius-lg); border: 1px solid var(--border-light); display: flex; gap: 2rem; margin-bottom: 2rem; box-shadow: var(--shadow-sm); }
.filter-card .field { flex: 1; display: flex; flex-direction: column; gap: 0.5rem; }
.filter-card label { font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
.filter-card select { padding: 0.75rem; border: 1px solid var(--border-light); border-radius: 8px; font-weight: 600; color: #334155; outline: none; background-color: #fbfcfe; }

.evaluations-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem; }
.eval-card { background: white; border-radius: var(--radius-lg); border: 1px solid var(--border-light); overflow: hidden; display: flex; flex-direction: column; transition: all 0.2s; box-shadow: var(--shadow-sm); }
.eval-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }

.eval-badge { padding: 0.3rem 0.8rem; border-radius: 99px; font-size: 0.65rem; font-weight: 800; text-transform: uppercase; align-self: flex-start; margin: 1.25rem 1.25rem 0; }
.eval-badge.ds { background: #eef2ff; color: #3730a3; }
.eval-badge.examen { background: #fef3c7; color: #92400e; }
.eval-badge.tp { background: #ecfdf5; color: #065f46; }

.eval-main { padding: 1rem 1.25rem; }
.eval-main h3 { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin: 0; }
.eval-main p { font-size: 0.8rem; color: #94a3b8; margin-top: 0.25rem; }

.eval-stats { display: grid; grid-template-columns: 1fr 1fr; border-top: 1px solid #f1f5f9; border-bottom: 1px solid #f1f5f9; padding: 1rem 0; }
.es-item { display: flex; flex-direction: column; align-items: center; border-right: 1px solid #f1f5f9; }
.es-item:last-child { border-right: none; }
.es-item .l { font-size: 0.6rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
.es-item .v { font-size: 1.1rem; font-weight: 800; color: #334155; }
.es-item .v.empty { color: #cbd5e1; }

.eval-actions { padding: 1rem; }
.btn-full { width: 100%; padding: 0.75rem; background: #f8fafc; border: 1px solid var(--border-light); border-radius: 8px; font-weight: 700; color: var(--primary); cursor: pointer; transition: all 0.2s; font-size: 0.85rem; }
.btn-full:hover { background: var(--primary); color: white; border-color: var(--primary); }

.empty-state { grid-column: 1 / -1; display: flex; flex-direction: column; align-items: center; padding: 5rem; text-align: center; background: white; border-radius: var(--radius-xl); border: 2px dashed var(--border-light); }
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-state h3 { font-size: 1.25rem; font-weight: 700; color: #1e293b; }
.empty-state p { color: #64748b; margin-top: 0.5rem; }

.loader { display: flex; flex-direction: column; align-items: center; padding: 5rem; }
.spinner { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }

.btn { padding: 0.7rem 1.25rem; border-radius: 8px; font-weight: 700; font-size: 0.9rem; cursor: pointer; border: none; display: flex; align-items: center; gap: 0.5rem; }
.btn-primary { background: var(--primary); color: white; box-shadow: 0 4px 12px var(--primary-glow); }
</style>
