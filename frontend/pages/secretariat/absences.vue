<template>
  <div class="page-container">
    <header class="page-header">
      <div class="header-info">
        <h1>Saisie des Absences</h1>
        <p>Comptabilisation des heures pénalisantes par étudiant et matière.</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="showAddModal = true">
          <span>➕</span> Nouvelle Absence
        </button>
      </div>
    </header>

    <!-- Zone filtres -->
    <div class="filter-card">
      <div class="field">
        <label>Étudiant</label>
        <select v-model="selectedEtudiant" @change="fetchAbsences">
          <option value="">Tous les étudiants</option>
          <option v-for="et in etudiants" :key="et.id" :value="et.id">
            {{ et.prenom }} {{ et.nom }} ({{ et.matricule }})
          </option>
        </select>
      </div>
    </div>

    <div v-if="pending" class="loader">
      <div class="spinner"></div>
      <p>Chargement des absences...</p>
    </div>

    <div v-else class="evaluations-grid">
      <div v-for="absence in absences" :key="absence.id" class="eval-card">
        <div class="eval-badge">Absence</div>
        <div class="eval-main">
          <h3>{{ getMatiereLibelle(absence.matiere_id) }}</h3>
          <p>{{ formatDate(absence.date_absence) }}</p>
        </div>
        <div class="eval-stats">
          <div class="es-item">
            <span class="l">Étudiant</span>
            <span class="v student-name">{{ getEtudiantNom(absence.etudiant_id) }}</span>
          </div>
          <div class="es-item">
            <span class="l">Heures</span>
            <span class="v text-danger">{{ absence.nombre_heures }}h</span>
          </div>
        </div>
        <div class="eval-actions">
          <button class="btn-full" @click="deleteAbsence(absence)">🗑️ Supprimer</button>
        </div>
      </div>

      <div v-if="absences.length === 0" class="empty-state">
        <div class="empty-icon">📂</div>
        <h3>Aucune absence trouvée</h3>
        <p>Commencez par enregistrer une absence pour un étudiant.</p>
      </div>
    </div>

    <!-- ─── Modal Nouvelle Absence ─────────────────────────── -->
    <Transition name="modal-fade">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal-box">
          <div class="modal-header">
            <h2>Nouvelle Absence</h2>
            <button class="modal-close" @click="showAddModal = false">✕</button>
          </div>

          <form class="modal-form" @submit.prevent="submitAbsence">
            <div class="form-grid">
              <div class="form-group">
                <label>Étudiant</label>
                <select v-model="form.etudiant_id" required>
                  <option value="">-- Sélectionner --</option>
                  <option v-for="et in etudiants" :key="et.id" :value="et.id">
                    {{ et.prenom }} {{ et.nom }} ({{ et.matricule }})
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>Matière</label>
                <select v-model="form.matiere_id" required>
                  <option value="">-- Sélectionner --</option>
                  <option v-for="mat in matieres" :key="mat.id" :value="mat.id">
                    {{ mat.libelle }}
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>Nombre d'heures</label>
                <input
                  type="number"
                  v-model.number="form.nombre_heures"
                  min="1"
                  max="50"
                  required
                  placeholder="Ex: 2"
                />
              </div>

              <div class="form-group">
                <label>Date de l'absence</label>
                <input
                  type="date"
                  v-model="form.date_absence"
                  required
                />
              </div>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" @click="showAddModal = false">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                {{ submitting ? 'Enregistrement...' : '✅ Enregistrer l\'absence' }}
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

useHead({ title: 'Saisie Absences | Secrétariat Bull ASUR' })

const { fetchApi } = useApi()
const absences = ref([])
const etudiants = ref([])
const matieres = ref([])
const pending = ref(true)
const submitting = ref(false)
const showAddModal = ref(false)
const selectedEtudiant = ref('')

const form = ref({
  etudiant_id: '',
  matiere_id: '',
  nombre_heures: 2,
  date_absence: new Date().toISOString().split('T')[0]
})

const fetchInitialData = async () => {
  pending.value = true
  try {
    const [etData, matData] = await Promise.allSettled([
      fetchApi('/etudiants/'),
      fetchApi('/matieres/')
    ])
    
    etudiants.value = etData.status === 'fulfilled' && Array.isArray(etData.value) ? etData.value : []
    matieres.value = matData.status === 'fulfilled' && Array.isArray(matData.value) ? matData.value : []

    await fetchAbsences()
  } finally {
    pending.value = false
  }
}

const fetchAbsences = async () => {
  pending.value = true
  try {
    let url = '/absences/'
    if (selectedEtudiant.value) {
      url += `?etudiant_id=${selectedEtudiant.value}`
    }
    const data = await fetchApi(url)
    absences.value = Array.isArray(data) ? data : []
  } catch (e) {
    absences.value = []
  } finally {
    pending.value = false
  }
}

onMounted(fetchInitialData)

const getMatiereLibelle = (id) => {
  const mat = matieres.value.find(m => m.id === id)
  return mat ? mat.libelle : 'Matière Inconnue'
}

const getEtudiantNom = (id) => {
  const et = etudiants.value.find(e => e.id === id)
  return et ? `${et.prenom} ${et.nom}` : 'Étudiant Inconnu'
}

const formatDate = (d) => {
  if (!d) return 'Date non définie'
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

const submitAbsence = async () => {
  submitting.value = true
  try {
    await fetchApi('/absences/', {
      method: 'POST',
      body: form.value
    })
    showAddModal.value = false
    form.value.nombre_heures = 2
    await fetchAbsences()
  } catch (err) {
    const msg = err.data?.error || err.data?.message || 'Erreur lors de la création.'
    alert(msg)
  } finally {
    submitting.value = false
  }
}

const deleteAbsence = async (absenceItem) => {
  if (!confirm(`Supprimer cette absence de ${absenceItem.nombre_heures}h ?`)) return
  try {
    await fetchApi(`/absences/${absenceItem.id}/`, { method: 'DELETE' })
    await fetchAbsences()
  } catch (err) {
    alert('Impossible de supprimer l\'absence. Vérifiez vos droits.')
  }
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; }
.header-info h1 { font-size: 1.75rem; font-weight: 800; color: #1e293b; margin: 0; }
.header-info p { color: #64748b; font-size: 1rem; margin: 0.25rem 0 0; }

.filter-card { background: white; padding: 1.5rem; border-radius: var(--radius-lg); border: 1px solid var(--border-light); display: flex; gap: 2rem; margin-bottom: 2rem; box-shadow: var(--shadow-sm); }
.filter-card .field { flex: 1; display: flex; flex-direction: column; gap: 0.5rem; max-width: 400px; }
.filter-card label { font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
.filter-card select { padding: 0.75rem; border: 1px solid var(--border-light); border-radius: 8px; font-weight: 600; color: #334155; outline: none; background-color: #fbfcfe; }

.evaluations-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem; }
.eval-card { background: white; border-radius: var(--radius-lg); border: 1px solid var(--border-light); overflow: hidden; display: flex; flex-direction: column; transition: all 0.2s; box-shadow: var(--shadow-sm); }
.eval-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }

.eval-badge { background: #fee2e2; color: #991b1b; padding: 0.3rem 0.8rem; border-radius: 99px; font-size: 0.65rem; font-weight: 800; text-transform: uppercase; align-self: flex-start; margin: 1.25rem 1.25rem 0; }

.eval-main { padding: 1rem 1.25rem; }
.eval-main h3 { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin: 0; }
.eval-main p { font-size: 0.8rem; color: #94a3b8; margin-top: 0.25rem; }

.eval-stats { display: grid; grid-template-columns: 1fr 1fr; border-top: 1px solid #f1f5f9; border-bottom: 1px solid #f1f5f9; padding: 1rem 0; }
.es-item { display: flex; flex-direction: column; align-items: center; justify-content: center; border-right: 1px solid #f1f5f9; text-align: center; padding: 0 0.5rem; }
.es-item:last-child { border-right: none; }
.es-item .l { font-size: 0.6rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
.es-item .v { font-size: 1.1rem; font-weight: 800; color: #334155; margin-top: 2px; }
.es-item .v.text-danger { color: #dc2626; }
.es-item .student-name { font-size: 0.9rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 100%; }

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
