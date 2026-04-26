<template>
  <div class="page-absences">
    <header class="page-header">
      <div class="header-content">
        <h1>Saisie des Absences</h1>
        <p>Comptabilisation rigoureuse des heures d'absence par étudiant et unité d'enseignement.</p>
      </div>
      <div class="header-actions">
        <div class="export-dropdown" v-if="absences.length">
          <button class="btn btn-pill dark">
            Exporter ↓
          </button>
          <div class="dropdown-menu premium-card">
            <button @click="exportData('excel')">Journal Excel (.xlsx)</button>
            <button @click="exportData('pdf-p')">Rapport PDF (Portrait)</button>
            <button @click="exportData('pdf-l')">Rapport PDF (Paysage)</button>
          </div>
        </div>
        <button class="btn btn-primary btn-pill" @click="showAddModal = true">
          + Nouvelle Absence
        </button>
      </div>
    </header>

    <!-- Filtre Étudiant -->
    <div class="filters-section premium-card">
      <div class="filter-row">
        <div class="filter-group max-w-400">
          <label>Cibler un étudiant</label>
          <select v-model="selectedEtudiant" @change="fetchAbsences" class="form-control">
            <option value="">Tous les dossiers archivés</option>
            <option v-for="et in etudiants" :key="et.id" :value="et.id">
              {{ et.prenom }} {{ et.nom }} ({{ et.matricule }})
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loader -->
    <div v-if="pending" class="loading-state-wrap">
      <div class="pulsar-dark"></div>
      <p>Synchronisation du registre...</p>
    </div>

    <!-- Grid des Absences -->
    <div v-else class="absences-grid">
      <div v-for="absence in absences" :key="absence.id" class="absence-card premium-card">
        <div class="card-header">
          <span class="type-badge">ABSENCE</span>
          <span class="hours-badge">{{ absence.nombre_heures }}H</span>
        </div>
        <div class="card-body">
          <h3>{{ getMatiereLibelle(absence.matiere_id) }}</h3>
          <p class="date">{{ formatDate(absence.date_absence) }}</p>
          <div class="student-info">
            <span class="label">Étudiant</span>
            <p class="name">{{ getEtudiantNom(absence.etudiant_id) }}</p>
          </div>
        </div>
        <div class="card-footer">
          <button class="btn-delete" @click="deleteAbsence(absence)">Révoquer l'entrée 🗑️</button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="absences.length === 0" class="empty-state premium-card">
        <div class="empty-icon">🗃️</div>
        <h3>Registre Vierge</h3>
        <p>Aucune absence n'a été répertoriée pour cette sélection.</p>
      </div>
    </div>

    <!-- Modal Nouvelle Absence -->
    <Transition name="modal-bounce">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal-content premium-card">
          <div class="modal-header-premium">
            <span class="pulsar"></span>
            <h3>Enregistrer une Absence</h3>
          </div>

          <form class="modal-form" @submit.prevent="submitAbsence">
            <div class="form-group stack">
              <label>Étudiant concerné</label>
              <select v-model="form.etudiant_id" required class="form-control">
                <option value="">-- Sélectionner l'étudiant --</option>
                <option v-for="et in etudiants" :key="et.id" :value="et.id">
                  {{ et.prenom }} {{ et.nom }} ({{ et.matricule }})
                </option>
              </select>
            </div>

            <div class="form-group stack mt-1">
              <label>Matière (UE)</label>
              <select v-model="form.matiere_id" required class="form-control">
                <option value="">-- Sélectionner l'UE --</option>
                <option v-for="mat in matieres" :key="mat.id" :value="mat.id">
                  {{ mat.libelle }}
                </option>
              </select>
            </div>

            <div class="form-row mt-1">
              <div class="form-group">
                <label>Volume horaire</label>
                <input type="number" v-model.number="form.nombre_heures" min="1" max="50" required class="form-control">
              </div>
              <div class="form-group">
                <label>Date effective</label>
                <input type="date" v-model="form.date_absence" required class="form-control">
              </div>
            </div>

            <div class="form-actions-premium mt-2">
              <button type="button" class="btn btn-outline" @click="showAddModal = false">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                {{ submitting ? 'Enregistrement...' : 'Confirmer l\'absence' }}
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

const { fetchApi } = useApi()
const { exportToExcel, exportToPDF } = useExport()

useHead({ title: 'Saisie Absences | Bull ASUR' })

// État
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

// Logic
const fetchInitialData = async () => {
  pending.value = true
  try {
    const [etData, matData] = await Promise.allSettled([
      fetchApi('/etudiants/'),
      fetchApi('/matieres/')
    ])
    etudiants.value = etData.status === 'fulfilled' ? etData.value : []
    matieres.value = matData.status === 'fulfilled' ? matData.value : []
    await fetchAbsences()
  } finally {
    pending.value = false
  }
}

const fetchAbsences = async () => {
  pending.value = true
  try {
    let url = '/absences/'
    if (selectedEtudiant.value) url += `?etudiant_id=${selectedEtudiant.value}`
    absences.value = await fetchApi(url)
  } catch (e) {
    absences.value = []
  } finally {
    pending.value = false
  }
}

const submitAbsence = async () => {
  submitting.value = true
  try {
    await fetchApi('/absences/', { method: 'POST', body: form.value })
    showAddModal.value = false
    await fetchAbsences()
  } catch (err) {
    alert(err.data?.error || 'Erreur lors de la création.')
  } finally {
    submitting.value = false
  }
}

const deleteAbsence = async (item) => {
  if (!confirm(`Supprimer cette absence (${item.nombre_heures}h) ?`)) return
  try {
    await fetchApi(`/absences/${item.id}/`, { method: 'DELETE' })
    await fetchAbsences()
  } catch (err) {
    alert('Action impossible.')
  }
}

const exportData = (type) => {
  const data = absences.value.map(a => ({ Étudiant: getEtudiantNom(a.etudiant_id), Matière: getMatiereLibelle(a.matiere_id), Heures: a.nombre_heures, Date: formatDate(a.date_absence) }))
  if (type === 'excel') { exportToExcel(data, 'Journal_Absences.xlsx') }
  else {
    const headers = ['Étudiant', 'Matière', 'Heures', 'Date']
    const rows = absences.value.map(a => [getEtudiantNom(a.etudiant_id), getMatiereLibelle(a.matiere_id), `${a.nombre_heures}h`, formatDate(a.date_absence)])
    exportToPDF(headers, rows, 'Registre_Absences.pdf', type === 'pdf-l' ? 'l' : 'p')
  }
}

const getMatiereLibelle = (id) => matieres.value.find(m => m.id === id)?.libelle || 'UE Inconnue'
const getEtudiantNom = (id) => {
  const et = etudiants.value.find(e => e.id === id)
  return et ? `${et.prenom} ${et.nom}` : 'Profil Inconnu'
}
const formatDate = (d) => new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })

onMounted(fetchInitialData)
</script>

<style scoped>
.page-absences { padding: clamp(1.5rem, 4vw, 4rem) 2rem; max-width: 1500px; margin: 0 auto; animation: fadeIn 0.6s ease-out; }

@keyframes fadeIn { from { opacity: 0; transform: scale(0.98); } to { opacity: 1; transform: scale(1); } }

.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4rem; flex-wrap: wrap; gap: 2rem; }
.header-content h1 { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 900; letter-spacing: -2px; margin-bottom: 0.5rem; }
.header-content p { color: #64748b; font-weight: 500; font-size: 1.1rem; }
.header-actions { display: flex; gap: 1rem; position: relative; }

.export-dropdown { position: relative; }
.export-dropdown:hover .dropdown-menu { display: block; opacity: 1; pointer-events: auto; transform: translateY(0); }
.dropdown-menu { 
  display: none; position: absolute; top: 100%; right: 0; min-width: 240px; 
  background: #fff; z-index: 100; padding: 0.75rem; margin-top: 0.5rem;
  transition: all 0.2s; opacity: 0; pointer-events: none; transform: translateY(10px);
}
.dropdown-menu button { 
  width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent;
  font-weight: 700; font-size: 0.85rem; border-radius: 8px; cursor: pointer;
}
.dropdown-menu button:hover { background: #f1f5f9; }

.filters-section { padding: 2rem 3rem; margin-bottom: 3rem; background: #fff; }
.filter-group label { display: block; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1.5px; color: #94a3b8; margin-bottom: 0.75rem; }
.max-w-400 { max-width: 400px; }

.absences-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 2rem; }
.absence-card { background: #fff; padding: 2rem; border: 1px solid #f1f5f9; transition: all 0.3s; }
.absence-card:hover { transform: translateY(-5px); }

.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.type-badge { font-size: 0.65rem; font-weight: 900; padding: 0.3rem 0.75rem; background: #fee2e2; color: #991b1b; border-radius: 50px; }
.hours-badge { font-size: 1.25rem; font-weight: 900; color: #000; letter-spacing: -1px; }

.card-body h3 { font-size: 1.2rem; font-weight: 900; margin-bottom: 0.25rem; letter-spacing: -0.5px; }
.card-body .date { font-size: 0.85rem; color: #94a3b8; font-weight: 600; margin-bottom: 1.5rem; }

.student-info { padding: 1.25rem; background: #f8fafc; border-radius: 12px; }
.student-info .label { font-size: 0.65rem; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.25rem; display: block; }
.student-info .name { font-weight: 800; font-size: 0.95rem; color: #000; margin: 0; }

.card-footer { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #f1f5f9; }
.btn-delete { width: 100%; padding: 0.75rem; background: transparent; border: 2px solid #fee2e2; border-radius: 10px; color: #ef4444; font-weight: 900; cursor: pointer; transition: all 0.2s; font-size: 0.8rem; }
.btn-delete:hover { background: #ef4444; color: #fff; border-color: #ef4444; }

.loading-state-wrap { padding: 6rem; text-align: center; }
.pulsar-dark { width: 40px; height: 40px; background: #000; border-radius: 50%; margin: 0 auto 1.5rem; animation: pulse-black 1.5s infinite; }
@keyframes pulse-black { 0% { box-shadow: 0 0 0 0 rgba(0,0,0,0.4); } 70% { box-shadow: 0 0 0 20px rgba(0,0,0,0); } 100% { box-shadow: 0 0 0 0 rgba(0,0,0,0); } }

.empty-state { grid-column: 1 / -1; padding: 6rem; text-align: center; border: 3px dashed #f1f5f9; }
.empty-icon { font-size: 3.5rem; margin-bottom: 1.5rem; opacity: 0.3; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(8px); z-index: 1000; display: flex; align-items: center; justify-content: center; }
.modal-content { max-width: 550px; width: 100%; border-radius: 24px; overflow: hidden; }
.modal-header-premium { padding: 2.5rem; background: #000; color: #fff; display: flex; align-items: center; gap: 1rem; }
.modal-header-premium h3 { font-weight: 900; font-size: 1.5rem; }
.pulsar { width: 12px; height: 12px; background: #fff; border-radius: 50%; animation: pulse-white 1.5s infinite; }
@keyframes pulse-white { 0% { box-shadow: 0 0 0 0 rgba(255,255,255,0.4); } 70% { box-shadow: 0 0 0 15px rgba(255,255,255,0); } 100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); } }

.modal-form { padding: 2.5rem; }
.form-group.stack { display: flex; flex-direction: column; gap: 0.6rem; }
.form-group label { font-size: 0.7rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; }
.form-control { width: 100%; padding: 1.1rem; border: 2px solid #f1f5f9; border-radius: 12px; font-weight: 700; background: #fafafa; outline: none; }
.form-control:focus { border-color: #000; background: #fff; }

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.form-actions-premium { display: flex; gap: 1rem; justify-content: flex-end; border-top: 1px solid #f1f5f9; padding-top: 2rem; }

.btn { padding: 1rem 2rem; font-weight: 900; font-size: 0.9rem; border: none; cursor: pointer; border-radius: 12px; transition: all 0.2s; }
.btn-primary { background: #000; color: #fff; }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(0,0,0,0.15); }
.btn-pill { border-radius: 50px; }
.btn-pill.dark { background: transparent; border: 2px solid #000; color: #000; }
.btn-outline { background: transparent; border: 2px solid #f1f5f9; color: #64748b; }

.mt-1 { margin-top: 1.5rem; }
.mt-2 { margin-top: 3rem; }
</style>
