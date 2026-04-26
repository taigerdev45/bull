<template>
  <div class="page-enseignants">
    <header class="page-header">
      <div class="header-content">
        <h1>Gestion des Enseignants</h1>
        <p>Administrez les profils des intervenants et assignez leurs unités d'enseignement.</p>
      </div>
      <div class="header-actions">
        <div class="export-dropdown" v-if="teachers.length">
          <button class="btn btn-pill dark">
            Exporter ↓
          </button>
          <div class="dropdown-menu premium-card">
            <button @click="exportData('excel')">Liste Excel (.xlsx)</button>
            <button @click="exportData('pdf-p')">Liste PDF (Portrait)</button>
            <button @click="exportData('pdf-l')">Liste PDF (Paysage)</button>
          </div>
        </div>
        <button class="btn btn-primary btn-pill shadow-strong" @click="openModal('add')">
          + Nouveau Profil
        </button>
      </div>
    </header>

    <!-- Filtres & Stats -->
    <div class="filters-row premium-card">
      <div class="search-wrapper">
        <label>Rechercher un profil</label>
        <div class="input-with-icon">
          <span class="icon">🔍</span>
          <input 
            type="text" 
            v-model="searchTerm" 
            placeholder="Nom, matricule ou spécialité..."
            class="form-control"
          >
        </div>
      </div>
      <div class="status-indicator">
        <div class="indicator-pulsar"></div>
        <p><strong>{{ filteredTeachers.length }}</strong> intervenants actifs</p>
      </div>
    </div>

    <!-- Grid des Enseignants -->
    <div class="teachers-grid">
      <div v-for="teacher in filteredTeachers" :key="teacher.id" class="teacher-card premium-card">
        <div class="card-inner">
          <div class="profile-section">
            <div class="avatar-monochrome">
              {{ teacher.prenom.charAt(0) }}{{ teacher.nom.charAt(0) }}
            </div>
            <div class="id-wrap">
              <h3>{{ teacher.prenom }} {{ teacher.nom }}</h3>
              <span class="matricule-tag">{{ teacher.matricule }}</span>
            </div>
          </div>

          <div class="details-section">
            <div class="detail-row">
              <span class="label">Contact</span>
              <span class="val">{{ teacher.email }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Expertise</span>
              <span class="val highlight">{{ teacher.specialite || 'Enseignant-Chercheur' }}</span>
            </div>
          </div>

          <div class="assignments-section">
            <label>Unités d'Enseignement</label>
            <div class="tags-row">
              <span v-for="mat in teacher.matieres" :key="mat" class="ue-tag">
                {{ mat }}
              </span>
              <span v-if="!teacher.matieres?.length" class="no-ue">Aucune UE assignée</span>
            </div>
          </div>

          <div class="card-footer-actions">
            <button class="btn-action" @click="openModal('edit', teacher)" title="Modifier">✏️</button>
            <button class="btn-action dark" @click="openAssignModal(teacher)" title="Assigner">📚</button>
            <button class="btn-action danger" @click="deleteTeacher(teacher.id)" title="Supprimer">🗑️</button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredTeachers.length === 0" class="empty-state-card premium-card">
        <div class="icon">👤</div>
        <h3>Aucun enseignant</h3>
        <p>Ajoutez un nouvel intervenant pour commencer l'attribution.</p>
      </div>
    </div>

    <!-- Modal Formulaire -->
    <Transition name="modal-bounce">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content premium-card">
          <div class="modal-header-premium">
            <span class="pulsar"></span>
            <h3>{{ modalMode === 'add' ? 'Création de Profil' : 'Édition Profil' }}</h3>
          </div>
          
          <form @submit.prevent="saveTeacher" class="modal-form">
            <div class="form-row">
              <div class="form-group stack">
                <label>Nom</label>
                <input v-model="formData.nom" required class="form-control" placeholder="DIOP">
              </div>
              <div class="form-group stack">
                <label>Prénom</label>
                <input v-model="formData.prenom" required class="form-control" placeholder="Abdoulaye">
              </div>
            </div>

            <div class="form-row mt-1">
              <div class="form-group stack">
                <label>Email Professionnel</label>
                <input type="email" v-model="formData.email" required class="form-control" placeholder="a.diop@uadb.edu">
              </div>
              <div class="form-group stack">
                <label>Matricule (Accès)</label>
                <input v-model="formData.matricule" required class="form-control" placeholder="ENS-001">
              </div>
            </div>

            <div class="security-note">
              <p>🧬 <strong>Accès Académique</strong></p>
              <span>Authentification par matricule activée par défaut.</span>
            </div>

            <div class="form-row">
              <div class="form-group stack">
                <label>Téléphone</label>
                <input v-model="formData.telephone" class="form-control" placeholder="+221 ...">
              </div>
              <div class="form-group stack">
                <label>Domaine / Spécialité</label>
                <input v-model="formData.specialite" class="form-control" placeholder="Informatique">
              </div>
            </div>

            <div class="form-actions-premium mt-2">
              <button type="button" class="btn btn-outline" @click="closeModal">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? 'Synchronisation...' : 'Valider le profil' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>

    <!-- Modal Assignation -->
    <Transition name="modal-bounce">
      <div v-if="showAssignModal" class="modal-overlay" @click.self="closeAssignModal">
        <div class="modal-content premium-card assign-box">
          <div class="modal-header-premium">
            <span class="pulsar"></span>
            <h3>Attribution des UE</h3>
          </div>
          <div class="modal-body-scroll">
            <p class="target-teacher">Enseignant : <strong>{{ selectedTeacher?.prenom }} {{ selectedTeacher?.nom }}</strong></p>
            
            <div class="ues-stack">
              <div v-for="ue in availableUEs" :key="ue.id" class="ue-group">
                <h4 class="ue-title">{{ ue.libelle }} <span>{{ ue.code }}</span></h4>
                <div class="matieres-checklist">
                  <label v-for="mat in ue.matieres" :key="mat.id" class="check-item-premium">
                    <input type="checkbox" :value="mat.id" v-model="selectedMatieres">
                    <div class="custom-box"></div>
                    <div class="item-info">
                      <span class="name">{{ mat.libelle }}</span>
                      <span class="meta">{{ mat.coefficient }} Coeff • {{ mat.credits }} Crédits</span>
                    </div>
                  </label>
                </div>
              </div>
            </div>
          </div>
          <div class="form-actions-premium">
            <button class="btn btn-outline" @click="closeAssignModal">Fermer</button>
            <button class="btn btn-primary" @click="assignMatieres" :disabled="loading">
              {{ loading ? 'Mise à jour...' : 'Confirmer l\'Assignation' }}
            </button>
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
useHead({ title: 'Gestion Enseignants | Bull ASUR' })

// État
const teachers = ref([])
const searchTerm = ref('')
const showModal = ref(false)
const modalMode = ref('add')
const loading = ref(false)
const currentTeacher = ref(null)
const showAssignModal = ref(false)
const selectedTeacher = ref(null)
const selectedMatieres = ref([])
const availableUEs = ref([])

const formData = ref({ nom: '', prenom: '', email: '', matricule: '', telephone: '', specialite: '' })

// Computed
const filteredTeachers = computed(() => {
  if (!searchTerm.value) return teachers.value
  const s = searchTerm.value.toLowerCase()
  return teachers.value.filter(t => t.nom.toLowerCase().includes(s) || t.prenom.toLowerCase().includes(s) || t.matricule.toLowerCase().includes(s))
})

// Logic
const loadInitialData = async () => {
  try {
    const [tRes, ueRes] = await Promise.all([fetchApi('/enseignants/'), fetchApi('/ues/')])
    teachers.value = tRes
    availableUEs.value = ueRes
  } catch (err) {
    console.error(err)
  }
}

const openModal = (mode, teacher = null) => {
  modalMode.value = mode
  if (mode === 'edit' && teacher) {
    currentTeacher.value = teacher
    formData.value = { ...teacher, telephone: teacher.telephone || '' }
  } else {
    formData.value = { nom: '', prenom: '', email: '', matricule: 'ENS-', telephone: '', specialite: '' }
  }
  showModal.value = true
}

const closeModal = () => { showModal.value = false; currentTeacher.value = null; }

const saveTeacher = async () => {
  loading.value = true
  try {
    const isAdd = modalMode.value === 'add'
    const url = isAdd ? '/enseignants/' : `/enseignants/${currentTeacher.value.id}/`
    await fetchApi(url, { method: isAdd ? 'POST' : 'PATCH', body: formData.value })
    await loadInitialData()
    closeModal()
  } catch (err) {
    alert(err.data?.error || "Erreur de synchronisation")
  } finally {
    loading.value = false
  }
}

const deleteTeacher = async (id) => {
  if (!confirm("Effacer définitivement ce profil ?")) return
  try {
    await fetchApi(`/enseignants/${id}/`, { method: 'DELETE' })
    await loadInitialData()
  } catch (err) {
    alert("Erreur")
  }
}

const openAssignModal = (teacher) => {
  selectedTeacher.value = teacher
  selectedMatieres.value = teacher.matiere_ids || []
  showAssignModal.value = true
}

const closeAssignModal = () => { showAssignModal.value = false; selectedTeacher.value = null; }

const assignMatieres = async () => {
  loading.value = true
  try {
    await fetchApi(`/enseignants/${selectedTeacher.value.id}/assign-matieres/`, { method: 'POST', body: { matiere_ids: selectedMatieres.value } })
    await loadInitialData()
    closeAssignModal()
  } catch (err) {
    alert("Échec de l'attribution")
  } finally {
    loading.value = false
  }
}

const exportData = (type) => {
  const data = teachers.value.map(t => ({ Nom: t.nom, Prénom: t.prenom, Spécialité: t.specialite || 'N/A', Email: t.email }))
  if (type === 'excel') exportToExcel(data, 'Enseignants_ASUR.xlsx')
  else exportToPDF(['Nom', 'Prénom', 'Spécialité', 'Email'], teachers.value.map(t => [t.nom, t.prenom, t.specialite || 'N/A', t.email]), 'Enseignants.pdf', type === 'pdf-l' ? 'l' : 'p')
}

onMounted(loadInitialData)
</script>

<style scoped>
.page-enseignants { padding: clamp(1.5rem, 4vw, 4rem) 2rem; max-width: 1540px; margin: 0 auto; animation: slideIn 0.6s ease-out; }
@keyframes slideIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }

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

.filters-row { padding: 2.5rem 3rem; margin-bottom: 4rem; background: #fff; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 2rem; }
.search-wrapper { flex: 1; min-width: 300px; }
.search-wrapper label { display: block; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1.5px; color: #94a3b8; margin-bottom: 0.75rem; }
.input-with-icon { position: relative; }
.input-with-icon .icon { position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); color: #94a3b8; font-size: 0.9rem; }
.input-with-icon .form-control { padding-left: 3rem; }

.status-indicator { display: flex; align-items: center; gap: 1rem; padding: 1.25rem 2rem; background: #f8fafc; border-radius: 50px; }
.indicator-pulsar { width: 10px; height: 10px; background: #000; border-radius: 50%; animation: pulse-black 1.5s infinite; }
@keyframes pulse-black { 0% { box-shadow: 0 0 0 0 rgba(0,0,0,0.4); } 70% { box-shadow: 0 0 0 10px rgba(0,0,0,0); } 100% { box-shadow: 0 0 0 0 rgba(0,0,0,0); } }
.status-indicator p { font-size: 0.85rem; font-weight: 700; margin: 0; color: #64748b; }

.teachers-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 2.5rem; }
.teacher-card { background: #fff; border: 1px solid #f1f5f9; position: relative; transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1); }
.teacher-card:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.08); }
.card-inner { padding: 2.5rem; }

.profile-section { display: flex; align-items: center; gap: 1.5rem; margin-bottom: 2.5rem; }
.avatar-monochrome { width: 64px; height: 64px; background: #000; color: #fff; display: flex; align-items: center; justify-content: center; border-radius: 20px; font-size: 1.4rem; font-weight: 900; }
.id-wrap h3 { font-size: 1.25rem; font-weight: 950; margin-bottom: 0.25rem; letter-spacing: -0.5px; }
.matricule-tag { font-size: 0.75rem; font-weight: 800; background: #f1f5f9; padding: 0.25rem 0.6rem; border-radius: 4px; color: #475569; }

.details-section { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2.5rem; }
.detail-row { display: flex; justify-content: space-between; align-items: baseline; }
.detail-row .label { font-size: 0.65rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.5px; }
.detail-row .val { font-size: 0.95rem; font-weight: 700; color: #000; }
.detail-row .val.highlight { color: #000; padding: 0.25rem 0.75rem; background: #f8fafc; border-radius: 6px; }

.assignments-section label { display: block; font-size: 0.65rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; margin-bottom: 1rem; }
.tags-row { display: flex; flex-wrap: wrap; gap: 0.5rem; min-height: 40px; }
.ue-tag { font-size: 0.75rem; font-weight: 800; padding: 0.4rem 0.8rem; background: #fff; border: 2px solid #f1f5f9; border-radius: 10px; }
.no-ue { font-size: 0.8rem; font-style: italic; color: #cbd5e1; }

.card-footer-actions { margin-top: 2.5rem; padding-top: 2rem; border-top: 1px solid #f1f5f9; display: flex; gap: 0.75rem; }
.btn-action { flex: 1; padding: 0.8rem; border-radius: 12px; border: 1.5px solid #f1f5f9; background: #fff; cursor: pointer; transition: all 0.2s; font-size: 0.9rem; }
.btn-action:hover { border-color: #000; transform: scale(1.05); }
.btn-action.dark { background: #000; color: #fff; border-color: #000; }
.btn-action.danger:hover { background: #fee2e2; border-color: #ef4444; }

.empty-state-card { grid-column: 1 / -1; padding: 7rem; text-align: center; border: 3px dashed #f1f5f9; background: transparent; }
.empty-state-card .icon { font-size: 4rem; margin-bottom: 1.5rem; opacity: 0.2; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(10px); z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 1.5rem; }
.modal-content { max-width: 650px; width: 100%; border-radius: 28px; overflow: hidden; }
.modal-header-premium { padding: 2.5rem; background: #000; color: #fff; display: flex; align-items: center; gap: 1rem; }
.modal-header-premium h3 { font-weight: 900; font-size: 1.6rem; letter-spacing: -0.5px; }
.pulsar { width: 12px; height: 12px; background: #fff; border-radius: 50%; animation: pulse-white 1.5s infinite; }
@keyframes pulse-white { 0% { box-shadow: 0 0 0 0 rgba(255,255,255,0.4); } 70% { box-shadow: 0 0 0 15px rgba(255,255,255,0); } 100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); } }

.modal-form { padding: 2.5rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.form-group.stack { display: flex; flex-direction: column; gap: 0.75rem; }
.form-group label { font-size: 0.7rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; }
.form-control { width: 100%; padding: 1.2rem; border: 2.5px solid #f1f5f9; border-radius: 14px; font-weight: 700; background: #fafafa; outline: none; transition: all 0.2s; }
.form-control:focus { border-color: #000; background: #fff; box-shadow: 0 0 0 5px rgba(0,0,0,0.05); }

.security-note { padding: 1.25rem 1.5rem; background: #f8fafc; border-left: 6px solid #000; margin: 1.5rem 0 2rem; border-radius: 8px; }
.security-note p { font-weight: 900; font-size: 0.85rem; margin-bottom: 0.25rem; }
.security-note span { font-size: 0.8rem; color: #64748b; font-weight: 600; }

.modal-body-scroll { padding: 2.5rem; max-height: 60vh; overflow-y: auto; }
.assign-box { max-width: 600px; }
.target-teacher { margin-bottom: 2.5rem; font-size: 1.1rem; }
.ue-group { margin-bottom: 3rem; }
.ue-title { font-size: 1rem; font-weight: 900; border-bottom: 2px solid #000; padding-bottom: 0.75rem; margin-bottom: 1.5rem; display: flex; justify-content: space-between; }
.ue-title span { color: #94a3b8; font-weight: 600; font-size: 0.8rem; }

.matieres-checklist { display: flex; flex-direction: column; gap: 0.75rem; }
.check-item-premium { display: flex; align-items: center; padding: 1rem; border: 2px solid #f1f5f9; border-radius: 12px; cursor: pointer; transition: all 0.2s; }
.check-item-premium:hover { border-color: #000; background: #fafafa; }
.check-item-premium input { display: none; }
.custom-box { width: 22px; height: 22px; border: 2px solid #e2e8f0; border-radius: 7px; margin-right: 1.25rem; position: relative; transition: all 0.2s; }
.check-item-premium input:checked + .custom-box { background: #000; border-color: #000; }
.check-item-premium input:checked + .custom-box::after { content: '✓'; position: absolute; color: #fff; font-size: 14px; left: 5px; top: 1px; }

.item-info .name { font-weight: 800; font-size: 1rem; display: block; }
.item-info .meta { font-size: 0.75rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; }

.btn { padding: 1.1rem 2.2rem; font-weight: 900; font-size: 0.95rem; border: none; cursor: pointer; border-radius: 14px; }
.btn-primary { background: #000; color: #fff; }
.btn-primary:disabled { opacity: 0.4; pointer-events: none; }
.btn-pill { border-radius: 50px; }
.btn-outline { background: transparent; border: 2.5px solid #f1f5f9; color: #64748b; }
.btn-outline:hover { border-color: #000; color: #000; }

.shadow-strong { box-shadow: 0 10px 25px rgba(0,0,0,0.15); }

.mt-1 { margin-top: 1.5rem; }
.mt-2 { margin-top: 3rem; }
</style>
