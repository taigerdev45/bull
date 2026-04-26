<template>
  <div class="page-etudiants">
    <header class="page-header">
      <div class="header-content">
        <h1>Gestion des Étudiants</h1>
        <p>Inscriptions, informations administratives et suivi académique de la promotion.</p>
      </div>
      <div class="header-actions">
        <div class="export-dropdown" v-if="students.length">
          <button class="btn btn-pill dark">
            Exporter ↓
          </button>
          <div class="dropdown-menu premium-card">
            <button @click="exportData('excel')">Format Excel (.xlsx)</button>
            <button @click="exportData('pdf-p')">Document PDF (Portrait)</button>
            <button @click="exportData('pdf-l')">Document PDF (Paysage)</button>
          </div>
        </div>
        <button class="btn btn-primary btn-pill" @click="openModal('add')">
          + Nouvel Étudiant
        </button>
      </div>
    </header>

    <!-- Filtres et recherche -->
    <div class="filters-section premium-card">
      <div class="filter-row">
        <div class="filter-group flex-2">
          <label>Rechercher un dossier</label>
          <input 
            type="text" 
            v-model="searchTerm" 
            placeholder="Nom, prénom ou matricule..."
            class="form-control"
          >
        </div>
        <div class="filter-group">
          <label>Diplôme (Bac)</label>
          <select v-model="filterBac" class="form-control">
            <option value="">Tous les types</option>
            <option value="S">Scientifique (S)</option>
            <option value="ES">Économique et Social (ES)</option>
            <option value="L">Littéraire (L)</option>
            <option value="STMG">STMG</option>
            <option value="STI2D">STI2D</option>
            <option value="Autre">Autre</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Statistiques Rapides -->
    <div class="quick-stats-row">
      <div class="stat-mini premium-card">
        <span class="label">Total inscrits</span>
        <span class="value">{{ students.length }}</span>
      </div>
      <div class="stat-mini premium-card">
        <span class="label">Bacs Scientifiques</span>
        <span class="value">{{ students.filter(s => s.bac === 'S').length }}</span>
      </div>
    </div>

    <!-- Tableau des étudiants -->
    <div class="table-section premium-table-container">
      <div class="table-header-box">
        <div class="title-wrap">
          <h3>Registre Matricule</h3>
          <span class="badge-count">{{ filteredStudents.length }}</span>
        </div>
        <p class="subtitle">Base de données officielle des étudiants inscrits pour l'année en cours</p>
      </div>
      <div class="table-container">
        <table class="students-table">
          <thead>
            <tr>
              <th>Matricule</th>
              <th>Identité complète</th>
              <th>Email académique</th>
              <th>Né(e) le</th>
              <th>Bac</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in filteredStudents" :key="student.id" class="highlight-on-hover">
              <td class="font-mono">{{ student.matricule }}</td>
              <td class="font-bold">{{ student.nom }} {{ student.prenom }}</td>
              <td class="text-sm">{{ student.email }}</td>
              <td class="text-sm">{{ student.date_naissance }}</td>
              <td>
                <span class="bac-badge">{{ student.bac }}</span>
              </td>
              <td class="text-xs text-right">
                <div class="action-buttons-compact">
                  <button class="btn-circle-sm" @click="openModal('edit', student)" title="Modifier">✏️</button>
                  <button class="btn-circle-sm danger" @click="deleteStudent(student.id)" title="Supprimer">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="loading && students.length === 0">
              <td colspan="6" class="loading-state">Synchronisation sécurisée des dossiers...</td>
            </tr>
            <tr v-if="!loading && filteredStudents.length === 0">
              <td colspan="6" class="loading-state">Aucun dossier correspondant à votre recherche</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal d'ajout/modification -->
    <Transition name="modal-bounce">
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content premium-card" @click.stop>
          <div class="modal-header-premium">
            <span class="pulsar"></span>
            <h3>{{ modalMode === 'add' ? 'Nouveau Dossier' : 'Mise à jour Dossier' }}</h3>
          </div>
          
          <form @submit.prevent="saveStudent" class="modal-form">
            <div class="form-row">
              <div class="form-group">
                <label>Nom de famille</label>
                <input type="text" v-model="formData.nom" required class="form-control" placeholder="DIALLO">
              </div>
              <div class="form-group">
                <label>Prénoms</label>
                <input type="text" v-model="formData.prenom" required class="form-control" placeholder="Mamadou">
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Email académique</label>
                <input type="email" v-model="formData.email" required class="form-control" placeholder="m.diallo@uadb.edu">
              </div>
              <div class="form-group">
                <label>Numéro Matricule</label>
                <input type="text" v-model="formData.matricule" required class="form-control" placeholder="LPASUR001">
              </div>
            </div>

            <div class="id-security-card">
              <p>🧬 <strong>Identifiants générés par défaut</strong></p>
              <span>User: {{ formData.prenom || '...' }} | Pass: {{ formData.matricule || '...' }}</span>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Date de naissance</label>
                <input type="date" v-model="formData.date_naissance" required class="form-control">
              </div>
              <div class="form-group">
                <label>Lieu de naissance</label>
                <input type="text" v-model="formData.lieu_naissance" required class="form-control" placeholder="Dakar">
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Type de Baccalauréat</label>
                <select v-model="formData.bac" required class="form-control">
                  <option value="">Sélectionner...</option>
                  <option value="S">Scientifique</option>
                  <option value="ES">Économique et Social</option>
                  <option value="L">Littéraire</option>
                  <option value="STMG">STMG</option>
                  <option value="STI2D">STI2D</option>
                  <option value="Autre">Autre</option>
                </select>
              </div>
              <div class="form-group">
                <label>Lycée de provenance</label>
                <input type="text" v-model="formData.provenance" placeholder="Ex: Lycée Lamine Guèye" required class="form-control">
              </div>
            </div>

            <div class="form-actions-premium">
              <button type="button" class="btn btn-outline" @click="closeModal">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? 'Synchronisation...' : (modalMode === 'add' ? 'Créer le dossier' : 'Enregistrer') }}
              </button>
            </div>
          </form>
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

useHead({ title: 'Gestion des Étudiants | Bull ASUR' })

// État
const students = ref([])
const searchTerm = ref('')
const filterBac = ref('')
const showModal = ref(false)
const modalMode = ref('add')
const loading = ref(false)
const currentStudent = ref(null)

// Formulaire
const formData = ref({
  nom: '',
  prenom: '',
  email: '',
  matricule: '',
  date_naissance: '',
  lieu_naissance: '',
  bac: '',
  provenance: ''
})

// Filtrage
const filteredStudents = computed(() => {
  return students.value.filter(student => {
    const searchLower = searchTerm.value.toLowerCase()
    const matchesSearch = `${student.nom} ${student.prenom} ${student.matricule}`.toLowerCase().includes(searchLower)
    const matchesBac = !filterBac.value || student.bac === filterBac.value
    return matchesSearch && matchesBac
  }).sort((a, b) => a.nom.localeCompare(b.nom))
})

// Méthodes
const loadStudents = async () => {
  loading.value = true
  try {
    const response = await fetchApi('/etudiants/')
    students.value = response
  } catch (error) {
    console.error('Erreur loading students', error)
  } finally {
    loading.value = false
  }
}

const exportData = (type) => {
  const data = students.value.map(s => ({
    Nom: s.nom,
    Prénom: s.prenom,
    Matricule: s.matricule,
    Email: s.email,
    'Date Naissance': s.date_naissance,
    'Lieu Naissance': s.lieu_naissance,
    Bac: s.bac,
    Provenance: s.provenance
  }))

  if (type === 'excel') {
    exportToExcel(data, 'Liste_Etudiants_ASUR.xlsx')
  } else {
    const headers = ['Matricule', 'Nom', 'Prénom', 'Bac', 'Provenance']
    const rows = students.value.map(s => [s.matricule, s.nom, s.prenom, s.bac, s.provenance])
    exportToPDF(headers, rows, 'Registre_Etudiants.pdf', type === 'pdf-l' ? 'l' : 'p')
  }
}

const openModal = (mode, student = null) => {
  modalMode.value = mode
  if (mode === 'edit' && student) {
    formData.value = { ...student }
    currentStudent.value = student
  } else {
    resetForm()
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  resetForm()
}

const resetForm = () => {
  formData.value = { nom: '', prenom: '', email: '', matricule: '', date_naissance: '', lieu_naissance: '', bac: '', provenance: '' }
  currentStudent.value = null
}

const saveStudent = async () => {
  loading.value = true
  try {
    const url = modalMode.value === 'add' ? '/etudiants/' : `/etudiants/${currentStudent.value.id}/`
    const method = modalMode.value === 'add' ? 'POST' : 'PATCH'
    await fetchApi(url, { method, body: formData.value })
    await loadStudents()
    closeModal()
  } catch (error) {
    alert(error.data?.error || "Erreur lors de l'enregistrement")
  } finally {
    loading.value = false
  }
}

const deleteStudent = async (id) => {
  if (!confirm('Action irréversible. Supprimer ce dossier ?')) return
  try {
    await fetchApi(`/etudiants/${id}/`, { method: 'DELETE' })
    await loadStudents()
  } catch (error) {
    alert("Échec de la suppression")
  }
}

onMounted(loadStudents)
</script>

<style scoped>
.page-etudiants { padding: clamp(1.5rem, 4vw, 4rem) 2rem; max-width: 1500px; margin: 0 auto; animation: fadeIn 0.6s ease-out; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4rem; flex-wrap: wrap; gap: 2rem; }
.header-content h1 { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 900; letter-spacing: -2px; margin-bottom: 0.5rem; }
.header-content p { color: #64748b; font-weight: 500; font-size: 1.1rem; }
.header-actions { display: flex; gap: 1rem; position: relative; }

.export-dropdown { position: relative; }
.export-dropdown:hover .dropdown-menu { display: block; opacity: 1; pointer-events: auto; transform: translateY(0); }
.dropdown-menu { 
  display: none; position: absolute; top: 100%; left: 0; min-width: 220px; 
  background: #fff; z-index: 100; padding: 0.75rem; margin-top: 0.5rem;
  transition: all 0.2s; opacity: 0; pointer-events: none; transform: translateY(10px);
}
.dropdown-menu button { 
  width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent;
  font-weight: 700; font-size: 0.85rem; border-radius: 8px; cursor: pointer;
}
.dropdown-menu button:hover { background: #f1f5f9; }

.filters-section { padding: 2.5rem; margin-bottom: 3rem; background: #fff; }
.filter-row { display: flex; gap: 2rem; align-items: flex-end; flex-wrap: wrap; }
.filter-group { flex: 1; min-width: 200px; }
.filter-group.flex-2 { flex: 2; }
.filter-group label { display: block; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1.5px; color: #94a3b8; margin-bottom: 0.75rem; }

.quick-stats-row { display: flex; gap: 1rem; margin-bottom: 3rem; }
.stat-mini { padding: 1.25rem 2rem; display: flex; align-items: center; gap: 2rem; background: #fff; }
.stat-mini .label { font-size: 0.75rem; font-weight: 800; text-transform: uppercase; color: #64748b; }
.stat-mini .value { font-size: 1.5rem; font-weight: 900; color: #000; }

.table-header-box { padding: 2.5rem; background: #fafafa; border-bottom: 1px solid #f1f5f9; }
.title-wrap { display: flex; align-items: center; gap: 1rem; }
.title-wrap h3 { font-size: 1.6rem; font-weight: 900; letter-spacing: -1px; }
.badge-count { padding: 0.2rem 0.8rem; background: #000; color: #fff; font-size: 0.75rem; font-weight: 900; border-radius: 6px; }
.subtitle { font-size: 0.85rem; color: #64748b; margin-top: 0.4rem; }

.students-table { width: 100%; border-collapse: collapse; }
.students-table th { padding: 1.5rem 1rem; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px; border-bottom: 2px solid #000; }
.students-table td { padding: 1.5rem 1rem; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }

.font-mono { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }
.font-bold { font-weight: 800; color: #000; }
.text-sm { font-size: 0.9rem; color: #475569; font-weight: 500; }
.text-right { text-align: right; }

.bac-badge { padding: 0.4rem 0.8rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; font-weight: 900; font-size: 0.7rem; }

.action-buttons-compact { display: flex; gap: 0.4rem; justify-content: flex-end; }
.btn-circle-sm { width: 32px; height: 32px; border-radius: 50%; border: 2px solid #f1f5f9; background: #fff; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; }
.btn-circle-sm:hover { scale: 1.1; border-color: #000; }
.btn-circle-sm.danger:hover { background: #fee2e2; border-color: #ef4444; }

.btn { padding: 1rem 2rem; font-weight: 900; font-size: 0.9rem; border: none; cursor: pointer; transition: all 0.2s; border-radius: 12px; }
.btn-pill { border-radius: 50px; }
.btn-primary { background: #000; color: #fff; }
.btn-primary:hover { box-shadow: 0 10px 20px rgba(0,0,0,0.15); transform: translateY(-2px); }
.btn-pill.dark { background: transparent; border: 2px solid #000; color: #000; }
.btn-pill.dark:hover { background: #000; color: #fff; }

.modal-content { max-width: 650px; width: 100%; padding: 0; overflow: hidden; border-radius: 24px; }
.modal-header-premium { padding: 2.5rem; background: #000; color: #fff; display: flex; align-items: center; gap: 1rem; }
.modal-header-premium h3 { font-weight: 900; font-size: 1.5rem; }
.pulsar { width: 12px; height: 12px; background: #fff; border-radius: 50%; animation: pulse-white 1.5s infinite; }
@keyframes pulse-white { 0% { box-shadow: 0 0 0 0 rgba(255,255,255,0.4); } 70% { box-shadow: 0 0 0 15px rgba(255,255,255,0); } 100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); } }

.modal-form { padding: 2.5rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem; }
.form-group label { display: block; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; margin-bottom: 0.6rem; }
.form-control { width: 100%; padding: 1.1rem; border: 2px solid #f1f5f9; border-radius: 12px; font-weight: 700; outline: none; background: #fafafa; }
.form-control:focus { border-color: #000; background: #fff; }

.id-security-card { padding: 1.5rem; background: #f8fafc; border-radius: 12px; border-left: 5px solid #000; margin-bottom: 2rem; }
.id-security-card p { font-weight: 900; font-size: 0.85rem; margin-bottom: 0.4rem; }
.id-security-card span { font-family: monospace; font-weight: 700; color: #64748b; }

.form-actions-premium { display: flex; gap: 1rem; justify-content: flex-end; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #f1f5f9; }
.btn-outline { background: transparent; border: 2px solid #f1f5f9; color: #64748b; }
.btn-outline:hover { border-color: #000; color: #000; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(8px); z-index: 1000; display: flex; align-items: center; justify-content: center; }

@media (max-width: 768px) {
  .form-row { grid-template-columns: 1fr; }
  .header-actions { width: 100%; flex-direction: column; }
}
</style>
