<template>
  <div class="page-edition-bulletins">
    <header class="page-header">
      <div class="header-content">
        <h1>Architecture Académique</h1>
        <p>Configuration structurelle : Semestres, UE et référentiel des matières.</p>
      </div>
    </header>

    <!-- Onglets Premium -->
    <div class="tabs-nav-premium premium-card">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-item', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        <span class="tab-label">{{ tab.label }}</span>
        <div class="active-line"></div>
      </button>
    </div>

    <!-- Contenu des onglets -->
    <div class="main-content-area">
      <!-- Semestres -->
      <div v-if="activeTab === 'semestres'" class="panel-premium animate-in">
        <div class="panel-header-box">
          <div class="text">
            <h3>Cycles Semestriels</h3>
            <p>Définition des périodes d'enseignement actives.</p>
          </div>
          <button class="btn btn-primary btn-pill shadow-strong" @click="openModal('semestre', 'add')">+ Nouveau Cycle</button>
        </div>
        
        <div class="premium-table-container">
          <table class="premium-table">
            <thead>
              <tr>
                <th>Libellé du Cycle</th>
                <th>Année Académique</th>
                <th class="text-right">Gestion</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in semestres" :key="item.id" class="highlight-on-hover">
                <td class="font-bold">{{ item.libelle }}</td>
                <td class="text-sm">{{ item.annee_universitaire }}</td>
                <td class="text-right">
                  <div class="action-buttons-compact">
                    <button class="btn-circle-sm" @click="openModal('semestre', 'edit', item)">✏️</button>
                    <button class="btn-circle-sm danger" @click="deleteItem('semestre', item.id)">🗑️</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- UE -->
      <div v-if="activeTab === 'ues'" class="panel-premium animate-in">
        <div class="panel-header-box">
          <div class="text">
            <h3>Unités d'Enseignement</h3>
            <p>Organisation des blocs pédagogiques par semestre.</p>
          </div>
          <button class="btn btn-primary btn-pill shadow-strong" @click="openModal('ue', 'add')">+ Nouvelle UE</button>
        </div>
        
        <div class="premium-table-container">
          <table class="premium-table">
            <thead>
              <tr>
                <th>Code UE</th>
                <th>Désignation de l'Unité</th>
                <th>Cycle Associé</th>
                <th class="text-right">Gestion</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in ues" :key="item.id" class="highlight-on-hover">
                <td class="font-mono">{{ item.code }}</td>
                <td class="font-bold">{{ item.libelle }}</td>
                <td class="text-sm">{{ getSemestreLibelle(item.semestre_id) }}</td>
                <td class="text-right">
                  <div class="action-buttons-compact">
                    <button class="btn-circle-sm" @click="openModal('ue', 'edit', item)">✏️</button>
                    <button class="btn-circle-sm danger" @click="deleteItem('ue', item.id)">🗑️</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Matières -->
      <div v-if="activeTab === 'matieres'" class="panel-premium animate-in">
        <div class="panel-header-box">
          <div class="text">
            <h3>Référentiel des Matières</h3>
            <p>Détails des coefficients et crédits ECTS par unité.</p>
          </div>
          <button class="btn btn-primary btn-pill shadow-strong" @click="openModal('matiere', 'add')">+ Nouvelle Matière</button>
        </div>
        
        <div class="premium-table-container">
          <table class="premium-table">
            <thead>
              <tr>
                <th>Libellé Matière</th>
                <th class="text-center">Coeff</th>
                <th class="text-center">ECTS</th>
                <th>Appartient à l'UE</th>
                <th class="text-right">Gestion</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in matieres" :key="item.id" class="highlight-on-hover">
                <td class="font-bold">{{ item.libelle }}</td>
                <td class="text-center">{{ item.coefficient }}</td>
                <td class="text-center font-mono">{{ item.credits }}</td>
                <td class="text-sm">{{ getUELibelle(item.ue_id) }}</td>
                <td class="text-right">
                  <div class="action-buttons-compact">
                    <button class="btn-circle-sm" @click="openModal('matiere', 'edit', item)">✏️</button>
                    <button class="btn-circle-sm danger" @click="deleteItem('matiere', item.id)">🗑️</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Absences Summary -->
      <div v-if="activeTab === 'absences'" class="panel-premium animate-in">
        <div class="panel-header-box">
          <div class="text">
            <h3>Suivi Global des Absences</h3>
            <p>Console d'administration des pénalités horaires.</p>
          </div>
          <button class="btn btn-primary btn-pill shadow-strong" @click="openModal('absence', 'add')">+ Log Absence</button>
        </div>

        <div class="filters-row-table">
          <div class="f-group">
            <label>Filtrer par étudiant</label>
            <select v-model="absenceFilters.etudiant_id" class="form-control">
              <option value="">Tous les dossiers</option>
              <option v-for="etudiant in etudiants" :key="etudiant.id" :value="etudiant.id">
                {{ etudiant.nom }} {{ etudiant.prenom }}
              </option>
            </select>
          </div>
        </div>
        
        <div class="premium-table-container">
          <table class="premium-table">
            <thead>
              <tr>
                <th>Étudiant</th>
                <th>Matière</th>
                <th class="text-center">Heures</th>
                <th class="text-right">Gestion</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredAbsences" :key="item.id" class="highlight-on-hover">
                <td class="font-bold">{{ getEtudiantLibelle(item.etudiant_id) }}</td>
                <td class="text-sm">{{ getMatiereLibelle(item.matiere_id) }}</td>
                <td class="text-center"><span class="badge-black">{{ item.heures }}H</span></td>
                <td class="text-right">
                  <div class="action-buttons-compact">
                    <button class="btn-circle-sm" @click="openModal('absence', 'edit', item)">✏️</button>
                    <button class="btn-circle-sm danger" @click="deleteItem('absence', item.id)">🗑️</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal Workflow Premium -->
    <Transition name="modal-bounce">
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content premium-card" @click.stop>
          <div class="modal-header-premium">
            <span class="pulsar"></span>
            <h3>{{ getModalTitle() }}</h3>
          </div>
          
          <form @submit.prevent="saveItem" class="modal-form">
            <!-- Semestre Form -->
            <div v-if="modalType === 'semestre'" class="stack">
              <div class="form-group">
                <label>Désignation du Cycle</label>
                <input v-model="formData.libelle" required class="form-control" placeholder="Ex: Semestre 5">
              </div>
              <div class="form-group mt-1">
                <label>Année Universitaire</label>
                <input v-model="formData.annee_universitaire" required class="form-control" placeholder="2025-2026">
              </div>
            </div>

            <!-- UE Form -->
            <div v-if="modalType === 'ue'" class="stack">
              <div class="form-row">
                <div class="form-group">
                  <label>Code Unique</label>
                  <input v-model="formData.code" required class="form-control" placeholder="UE5-1">
                </div>
                <div class="form-group">
                  <label>Libellé de l'Unité</label>
                  <input v-model="formData.libelle" required class="form-control" placeholder="Mathématiques">
                </div>
              </div>
              <div class="form-group mt-1">
                <label>Cycles Associé</label>
                <select v-model="formData.semestre_id" required class="form-control">
                  <option value="">Sélectionner un cycle...</option>
                  <option v-for="s in semestres" :key="s.id" :value="s.id">{{ s.libelle }} ({{ s.annee_universitaire }})</option>
                </select>
              </div>
            </div>

            <!-- Matière Form -->
            <div v-if="modalType === 'matiere'" class="stack">
              <div class="form-group">
                <label>Nom de la matière</label>
                <input v-model="formData.libelle" required class="form-control" placeholder="Algèbre">
              </div>
              <div class="form-row mt-1">
                <div class="form-group">
                  <label>Coefficient</label>
                  <input type="number" v-model="formData.coefficient" required step="0.5" class="form-control">
                </div>
                <div class="form-group">
                  <label>Crédits ECTS</label>
                  <input type="number" v-model="formData.credits" required class="form-control">
                </div>
              </div>
              <div class="form-group mt-1">
                <label>Unité d'Enseignement (UE)</label>
                <select v-model="formData.ue_id" required class="form-control">
                  <option value="">Choisir l'UE cible...</option>
                  <option v-for="u in ues" :key="u.id" :value="u.id">{{ u.code }} - {{ u.libelle }}</option>
                </select>
              </div>
            </div>

            <!-- Absence Form -->
            <div v-if="modalType === 'absence'" class="stack">
              <div class="form-group">
                <label>Étudiant</label>
                <select v-model="formData.etudiant_id" required class="form-control">
                  <option value="">-- Profil --</option>
                  <option v-for="e in etudiants" :key="e.id" :value="e.id">{{ e.nom }} {{ e.prenom }}</option>
                </select>
              </div>
              <div class="form-row mt-1">
                <div class="form-group">
                  <label>Matière</label>
                  <select v-model="formData.matiere_id" required class="form-control">
                    <option value="">-- UE/Matière --</option>
                    <option v-for="m in matieres" :key="m.id" :value="m.id">{{ m.libelle }}</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Heures</label>
                  <input type="number" v-model="formData.heures" required step="0.5" class="form-control">
                </div>
              </div>
            </div>

            <div class="form-actions-premium mt-2">
              <button type="button" class="btn btn-outline" @click="closeModal">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? 'Synchronisation...' : 'Enregistrer les modifications' }}
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

useHead({ title: 'Architecture Académique | Bull ASUR' })

// État
const activeTab = ref('semestres')
const showModal = ref(false)
const modalType = ref('')
const modalMode = ref('add')
const loading = ref(false)
const currentItem = ref(null)

// Données
const semestres = ref([])
const ues = ref([])
const matieres = ref([])
const absences = ref([])
const etudiants = ref([])

const absenceFilters = ref({ etudiant_id: '', matiere_id: '' })
const formData = ref({})

const tabs = [
  { id: 'semestres', label: 'Cycles (S5/S6)' },
  { id: 'ues', label: 'Unités (UE)' },
  { id: 'matieres', label: 'Matières' },
  { id: 'absences', label: 'Absences' }
]

// Computed
const filteredAbsences = computed(() => {
  return absences.value.filter(a => !absenceFilters.value.etudiant_id || a.etudiant_id === absenceFilters.value.etudiant_id)
})

// Logic
const loadAllData = async () => {
  try {
    const [s, u, m, a, e] = await Promise.all([
      fetchApi('/semestres/'), fetchApi('/ues/'), fetchApi('/matieres/'),
      fetchApi('/absences/'), fetchApi('/etudiants/')
    ])
    semestres.value = s || []
    ues.value = u || []
    matieres.value = m || []
    absences.value = a || []
    etudiants.value = e || []
  } catch (err) {
    console.error(err)
  }
}

const getModalTitle = () => {
  const lbls = { semestre: 'un Cycle', ue: 'une UE', matiere: 'une Matière', absence: 'un Log Absence' }
  return `${modalMode.value === 'add' ? 'Ajouter' : 'Modifier'} ${lbls[modalType.value]}`
}

const getSemestreLibelle = (id) => semestres.value.find(s => s.id === id)?.libelle || 'N/A'
const getUELibelle = (id) => ues.value.find(u => u.id === id)?.libelle || 'N/A'
const getMatiereLibelle = (id) => matieres.value.find(m => m.id === id)?.libelle || 'N/A'
const getEtudiantLibelle = (id) => {
  const et = etudiants.value.find(e => e.id === id)
  return et ? `${et.nom} ${et.prenom}` : 'Inconnu'
}

const openModal = (type, mode, item = null) => {
  modalType.value = type; modalMode.value = mode; currentItem.value = item
  formData.value = item ? { ...item } : {}
  showModal.value = true
}

const closeModal = () => { showModal.value = false; resetForm(); currentItem.value = null }
const resetForm = () => { formData.value = {} }

const saveItem = async () => {
  loading.value = true
  try {
    const endpoints = { semestre: 'semestres', ue: 'ues', matiere: 'matieres', absence: 'absences' }
    const ep = endpoints[modalType.value]
    const url = modalMode.value === 'add' ? `/${ep}/` : `/${ep}/${currentItem.value.id}/`
    await fetchApi(url, { method: modalMode.value === 'add' ? 'POST' : 'PATCH', body: formData.value })
    await loadAllData(); closeModal()
  } catch (err) {
    alert("Erreur de sauvegarde")
  } finally { loading.value = false }
}

const deleteItem = async (type, id) => {
  if (!confirm("Voulez-vous supprimer cet élément ?")) return
  try {
    const endpoints = { semestre: 'semestres', ue: 'ues', matiere: 'matieres', absence: 'absences' }
    await fetchApi(`/${endpoints[type]}/${id}/`, { method: 'DELETE' })
    await loadAllData()
  } catch (err) {
    alert("Suppression impossible")
  }
}

onMounted(loadAllData)
</script>

<style scoped>
.page-edition-bulletins { padding: clamp(1.5rem, 4vw, 4rem) 2rem; max-width: 1540px; margin: 0 auto; }

.page-header { margin-bottom: 4rem; }
.page-header h1 { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 900; letter-spacing: -2px; line-height: 1; margin-bottom: 0.5rem; }
.page-header p { color: #64748b; font-size: 1.1rem; font-weight: 500; }

.tabs-nav-premium { display: flex; padding: 0.5rem; background: #fff; margin-bottom: 4rem; gap: 0.5rem; }
.tab-item { flex: 1; padding: 1.25rem; background: transparent; border: none; cursor: pointer; position: relative; transition: all 0.3s; }
.tab-item .tab-label { font-size: 0.85rem; font-weight: 900; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
.tab-item.active .tab-label { color: #000; }
.active-line { height: 4px; background: #000; position: absolute; bottom: 0; left: 10%; right: 10%; border-radius: 10px 10px 0 0; transform: scaleX(0); transition: transform 0.3s; }
.tab-item.active .active-line { transform: scaleX(1); }

.animate-in { animation: slideUp 0.5s ease-out; }
@keyframes slideUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }

.panel-premium { margin-bottom: 4rem; }
.panel-header-box { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2.5rem; }
.panel-header-box h3 { font-size: 1.75rem; font-weight: 950; letter-spacing: -1px; line-height: 1; margin-bottom: 0.5rem; }
.panel-header-box p { color: #64748b; font-weight: 500; }

.premium-table { width: 100%; border-collapse: collapse; }
.premium-table th { padding: 1.5rem 1.25rem; text-align: left; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; border-bottom: 2px solid #000; }
.premium-table td { padding: 1.5rem 1.25rem; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }

.font-bold { font-weight: 800; color: #000; }
.font-mono { font-family: monospace; font-size: 0.85rem; color: #64748b; font-weight: 700; }
.text-sm { font-size: 0.9rem; color: #64748b; }
.badge-black { padding: 0.4rem 0.8rem; background: #000; color: #fff; font-size: 0.75rem; font-weight: 900; border-radius: 6px; }

.filters-row-table { margin-bottom: 2rem; padding: 1.5rem; background: #fafafa; border-radius: 16px; border: 1px solid #f1f5f9; }
.f-group label { display: block; font-size: 0.65rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; margin-bottom: 0.5rem; }

.action-buttons-compact { display: flex; gap: 0.5rem; justify-content: flex-end; }
.btn-circle-sm { width: 32px; height: 32px; border-radius: 50%; border: 2.5px solid #f1f5f9; background: #fff; font-size: 0.9rem; cursor: pointer; transition: all 0.2s; }
.btn-circle-sm:hover { scale: 1.1; border-color: #000; }

.btn { padding: 1.1rem 2.2rem; font-weight: 900; border: none; cursor: pointer; border-radius: 14px; transition: all 0.2s; }
.btn-primary { background: #000; color: #fff; }
.btn-primary:hover { transform: translateY(-4px); box-shadow: var(--shadow-strong); }
.btn-pill { border-radius: 50px; }
.btn-outline { background: transparent; border: 2.5px solid #f1f5f9; color: #64748b; }

.modal-header-premium { padding: 2.5rem; background: #000; color: #fff; display: flex; align-items: center; gap: 1rem; }
.pulsar { width: 12px; height: 12px; background: #fff; border-radius: 50%; animation: pulse-white 1.5s infinite; }
@keyframes pulse-white { 0% { box-shadow: 0 0 0 0 rgba(255,255,255,0.4); } 70% { box-shadow: 0 0 0 15px rgba(255,255,255,0); } 100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); } }

.modal-form { padding: 2.5rem; }
.form-group label { display: block; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; margin-bottom: 0.6rem; }
.form-control { width: 100%; padding: 1.1rem; border: 2.5px solid #f1f5f9; border-radius: 14px; font-weight: 700; background: #fafafa; outline: none; }
.form-control:focus { border-color: #000; background: #fff; }

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.stack { display: flex; flex-direction: column; gap: 0.5rem; }
.mt-1 { margin-top: 1.5rem; }
.mt-2 { margin-top: 3rem; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(8px); z-index: 1000; display: flex; align-items: center; justify-content: center; }
.modal-content { max-width: 600px; width: 100%; border-radius: 28px; overflow: hidden; }
</style>
