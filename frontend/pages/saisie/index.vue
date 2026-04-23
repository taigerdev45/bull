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

    <!-- Zone filtres -->
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
        <div class="eval-badge" :class="evalItem.type?.toLowerCase()">{{ evalItem.type }}</div>
        <div class="eval-main">
          <h3>{{ evalItem.matiere_libelle || 'Matière Inconnue' }}</h3>
          <p>{{ formatDate(evalItem.date_evaluation) }}</p>
        </div>
        <div class="eval-stats">
          <div class="es-item">
            <span class="l">Type</span>
            <span class="v">{{ evalItem.type }}</span>
          </div>
          <div class="es-item">
            <span class="l">Note</span>
            <span class="v" :class="{ empty: evalItem.note == null }">
              {{ evalItem.note != null ? evalItem.note.toFixed(2) : '--' }}
            </span>
          </div>
        </div>
        <div class="eval-actions">
          <button class="btn-full" @click="deleteEval(evalItem)">🗑️ Supprimer</button>
        </div>
      </div>

      <div v-if="evaluations.length === 0" class="empty-state">
        <div class="empty-icon">📂</div>
        <h3>Aucune évaluation trouvée</h3>
        <p>Commencez par créer une nouvelle session d'évaluation.</p>
      </div>
    </div>

    <!-- ─── Modal Nouvelle Évaluation ─────────────────────────── -->
    <Transition name="modal-fade">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal-box">
          <div class="modal-header">
            <h2>Nouvelle Évaluation</h2>
            <button class="modal-close" @click="showAddModal = false">✕</button>
          </div>

          <form class="modal-form" @submit.prevent="submitEval">
            <div class="form-grid">
              <div class="form-group">
                <label>Étudiant</label>
                <select v-model="evalForm.etudiant_id" required>
                  <option value="">-- Sélectionner --</option>
                  <option v-for="et in etudiants" :key="et.id" :value="et.id">
                    {{ et.prenom }} {{ et.nom }} ({{ et.matricule }})
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>Matière</label>
                <select v-model="evalForm.matiere_id" required>
                  <option value="">-- Sélectionner --</option>
                  <option v-for="mat in matieres" :key="mat.id" :value="mat.id">
                    {{ mat.libelle }}
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>Type d'évaluation</label>
                <select v-model="evalForm.type" required>
                  <option value="CC">Contrôle Continu (CC)</option>
                  <option value="EXAMEN">Examen Final</option>
                  <option value="RATTRAPAGE">Rattrapage</option>
                </select>
              </div>

              <div class="form-group">
                <label>Note (sur 20)</label>
                <input
                  type="number"
                  v-model.number="evalForm.note"
                  min="0"
                  max="20"
                  step="0.25"
                  required
                  placeholder="Ex: 14.5"
                />
              </div>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" @click="showAddModal = false">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                {{ submitting ? 'Enregistrement...' : '✅ Enregistrer la note' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

useHead({ title: 'Saisie Notes | Bull ASUR' })

const { fetchApi } = useApi()
const evaluations = ref([])
const ues = ref([])
const etudiants = ref([])
const matieres = ref([])
const pending = ref(true)
const submitting = ref(false)
const showAddModal = ref(false)
const selectedUE = ref('')
const selectedSemestre = ref('5')

const evalForm = ref({
  etudiant_id: '',
  matiere_id: '',
  type: 'CC',
  note: null
})

const fetchAll = async () => {
  pending.value = true
  try {
    // Chargement en parallèle de toutes les données nécessaires
    const [evalData, ueData, etData, matData] = await Promise.allSettled([
      fetchApi('/evaluations/'),
      fetchApi('/ues/'),         // URL correcte
      fetchApi('/etudiants/'),
      fetchApi('/matieres/')
    ])

    evaluations.value = evalData.status === 'fulfilled' && Array.isArray(evalData.value) ? evalData.value : []
    ues.value        = ueData.status === 'fulfilled'   && Array.isArray(ueData.value)   ? ueData.value   : []
    etudiants.value  = etData.status === 'fulfilled'   && Array.isArray(etData.value)   ? etData.value   : []
    matieres.value   = matData.status === 'fulfilled'  && Array.isArray(matData.value)  ? matData.value  : []
  } finally {
    pending.value = false
  }
}

onMounted(fetchAll)

const formatDate = (d) => {
  if (!d) return 'Date non définie'
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

const submitEval = async () => {
  submitting.value = true
  try {
    await fetchApi('/evaluations/', {
      method: 'POST',
      body: evalForm.value
    })
    showAddModal.value = false
    evalForm.value = { etudiant_id: '', matiere_id: '', type: 'CC', note: null }
    await fetchAll()
  } catch (err) {
    const msg = err.data?.error || err.data?.message || 'Erreur lors de la création. Vérifiez vos droits.'
    alert(msg)
  } finally {
    submitting.value = false
  }
}

const deleteEval = async (evalItem) => {
  if (!confirm(`Supprimer cette évaluation ?`)) return
  try {
    await fetchApi(`/evaluations/${evalItem.id}/`, { method: 'DELETE' })
    await fetchAll()
  } catch (err) {
    alert('Impossible de supprimer. Vérifiez vos droits.')
  }
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
.eval-badge.cc { background: #eef2ff; color: #3730a3; }
.eval-badge.examen { background: #fef3c7; color: #92400e; }
.eval-badge.rattrapage { background: #fee2e2; color: #991b1b; }

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
.btn-full { width: 100%; padding: 0.75rem; background: #fff1f2; border: 1px solid #fecaca; border-radius: 8px; font-weight: 700; color: #dc2626; cursor: pointer; transition: all 0.2s; font-size: 0.85rem; }
.btn-full:hover { background: #dc2626; color: white; }

.empty-state { grid-column: 1 / -1; display: flex; flex-direction: column; align-items: center; padding: 5rem; text-align: center; background: white; border-radius: var(--radius-xl); border: 2px dashed var(--border-light); }
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-state h3 { font-size: 1.25rem; font-weight: 700; color: #1e293b; }
.empty-state p { color: #64748b; margin-top: 0.5rem; }

.loader { display: flex; flex-direction: column; align-items: center; padding: 5rem; }
.spinner { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }

.btn { padding: 0.7rem 1.25rem; border-radius: 8px; font-weight: 700; font-size: 0.9rem; cursor: pointer; border: none; display: flex; align-items: center; gap: 0.5rem; transition: all 0.2s; }
.btn-primary { background: var(--primary); color: white; box-shadow: 0 4px 12px var(--primary-glow); }
.btn-ghost { background: #f1f5f9; color: #64748b; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(15,23,42,0.5); display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 1rem; backdrop-filter: blur(4px); }
.modal-box { background: white; border-radius: var(--radius-xl, 16px); width: 100%; max-width: 600px; box-shadow: 0 25px 50px rgba(0,0,0,0.25); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2rem; border-bottom: 1px solid #f1f5f9; }
.modal-header h2 { font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0; }
.modal-close { background: none; border: none; font-size: 1.1rem; cursor: pointer; color: #94a3b8; padding: 0.25rem; }
.modal-form { padding: 1.5rem 2rem; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
.form-group { display: flex; flex-direction: column; gap: 0.5rem; }
.form-group label { font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }
.form-group input, .form-group select { padding: 0.75rem 1rem; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 0.95rem; font-weight: 500; color: #0f172a; background: #f8fafc; outline: none; transition: border-color 0.2s; }
.form-group input:focus, .form-group select:focus { border-color: var(--primary); background: white; }
.modal-footer { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #f1f5f9; }

.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.25s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
</style>
