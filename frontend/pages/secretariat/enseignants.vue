<template>
  <div class="page-enseignants">
    <header class="page-header">
      <div class="header-content">
        <h2>👨‍🏫 Gestion des Enseignants</h2>
        <p>Administrez les intervenants et assignez leurs unités d'enseignement.</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary shadow-sm" @click="openModal('add')">
          <span class="icon">➕</span> Ajouter un Enseignant
        </button>
      </div>
    </header>

    <!-- Filtres et recherche -->
    <div class="filters-card">
      <div class="search-input-wrapper">
        <span class="search-icon">🔍</span>
        <input 
          type="text" 
          v-model="searchTerm" 
          placeholder="Rechercher par nom, matricule ou spécialité..."
          class="search-input"
        >
      </div>
      <div class="stats-badge">
        <strong>{{ filteredTeachers.length }}</strong> enseignants trouvés
      </div>
    </div>

    <!-- Liste des enseignants -->
    <div class="teachers-grid">
      <div v-for="teacher in filteredTeachers" :key="teacher.id" class="teacher-card shadow-sm">
        <div class="teacher-card-inner">
          <div class="teacher-header">
            <div class="teacher-avatar">
              {{ teacher.prenom.charAt(0) }}{{ teacher.nom.charAt(0) }}
            </div>
            <div class="teacher-identity">
              <h3>{{ teacher.prenom }} {{ teacher.nom }}</h3>
              <span class="matricule-badge">{{ teacher.matricule }}</span>
            </div>
          </div>
          
          <div class="teacher-body">
            <div class="info-item">
              <span class="info-label">📧 Email</span>
              <span class="info-value">{{ teacher.email }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">📱 Tel</span>
              <span class="info-value">{{ teacher.telephone || 'Non renseigné' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">🎓 Spécialité</span>
              <span class="info-value highlight">{{ teacher.specialite || 'Généraliste' }}</span>
            </div>
            
            <div class="matieres-section">
              <span class="info-label">📚 Matières assignées</span>
              <div class="matieres-tags">
                <span v-for="mat in teacher.matieres" :key="mat" class="tag-matiere">
                  {{ mat }}
                </span>
                <span v-if="!teacher.matieres?.length" class="empty-msg">Aucune matière</span>
              </div>
            </div>
          </div>
          
          <div class="teacher-footer">
            <button class="action-btn btn-edit" title="Modifier" @click="openModal('edit', teacher)">
              <span>✏️</span>
            </button>
            <button class="action-btn btn-assign" title="Assigner Matières" @click="openAssignModal(teacher)">
              <span>📚</span>
            </button>
            <button class="action-btn btn-delete" title="Supprimer" @click="deleteTeacher(teacher.id)">
              <span>🗑️</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Ajout/Modification -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-window">
        <div class="modal-header">
          <h3>{{ modalMode === 'add' ? '✨ Nouveau Profil' : '📝 Modifier le Profil' }}</h3>
          <button class="btn-close" @click="closeModal">✕</button>
        </div>
        
        <form @submit.prevent="saveTeacher" class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Nom *</label>
              <input v-model="formData.nom" required class="form-input">
            </div>
            <div class="form-group">
              <label>Prénom *</label>
              <input v-model="formData.prenom" required class="form-input">
            </div>
            <div class="form-group">
              <label>Email *</label>
              <input type="email" v-model="formData.email" required class="form-input">
            </div>
            <div class="form-group">
              <label>Matricule *</label>
              <input v-model="formData.matricule" required class="form-input" placeholder="ENS-XXX">
              <small class="hint">Doit commencer par ENS-</small>
            </div>
            <div class="form-group">
              <label>Téléphone</label>
              <input v-model="formData.telephone" class="form-input">
            </div>
            <div class="form-group">
              <label>Spécialité</label>
              <input v-model="formData.specialite" class="form-input">
            </div>
          </div>

          <div class="credentials-info">
            <p><strong>Compte Enseignant :</strong> Un compte sera créé automatiquement. Le mot de passe initial sera le matricule.</p>
          </div>

          <div class="form-footer">
            <button type="button" class="btn btn-ghost" @click="closeModal">Annuler</button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Action en cours...' : (modalMode === 'add' ? 'Créer le profil' : 'Enregistrer') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Assignation -->
    <div v-if="showAssignModal" class="modal-overlay" @click.self="closeAssignModal">
      <div class="modal-window assign-modal">
        <div class="modal-header">
          <div class="header-title">
            <h3>Assignation des Matières</h3>
            <p>{{ selectedTeacher?.prenom }} {{ selectedTeacher?.nom }}</p>
          </div>
          <button class="btn-close" @click="closeAssignModal">✕</button>
        </div>
        <div class="modal-body scrollable">
          <div class="ue-stack">
            <div v-for="ue in availableUEs" :key="ue.id" class="ue-item">
              <div class="ue-header">UE: {{ ue.libelle }} <span class="ue-code">{{ ue.code }}</span></div>
              <div class="matieres-checklist">
                <label v-for="mat in ue.matieres" :key="mat.id" class="matiere-check-label">
                  <input 
                    type="checkbox" 
                    :value="mat.id"
                    v-model="selectedMatieres"
                  >
                  <div class="check-custom"></div>
                  <div class="matiere-info">
                    <span class="m-name">{{ mat.libelle }}</span>
                    <span class="m-meta">{{ mat.coefficient }} coeff • {{ mat.credits }} ECTS</span>
                  </div>
                </label>
              </div>
            </div>
          </div>
        </div>
        <div class="form-footer">
          <button class="btn btn-ghost" @click="closeAssignModal">Annuler</button>
          <button class="btn btn-primary" @click="assignMatieres" :disabled="loading">
            {{ loading ? 'Assignation...' : 'Confirmer l\'Assignation' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const { fetchApi } = useApi()
useHead({ title: 'Enseignants | Secretariat Bull ASUR' })

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

// Formulaire
const formData = ref({
  nom: '',
  prenom: '',
  email: '',
  matricule: '',
  telephone: '',
  specialite: ''
})

// Filtrage
const filteredTeachers = computed(() => {
  if (!searchTerm.value) return teachers.value
  const lowSearch = searchTerm.value.toLowerCase()
  return teachers.value.filter(t => 
    t.nom.toLowerCase().includes(lowSearch) || 
    t.prenom.toLowerCase().includes(lowSearch) || 
    t.matricule.toLowerCase().includes(lowSearch) ||
    (t.specialite && t.specialite.toLowerCase().includes(lowSearch))
  )
})

// Méthodes API
const loadTeachers = async () => {
  try {
    const res = await fetchApi('/enseignants/')
    teachers.value = res
  } catch (err) {
    console.error('Erreur chargement enseignants', err)
  }
}

const loadUEs = async () => {
  try {
    const res = await fetchApi('/ues/')
    availableUEs.value = res
  } catch (err) {
    console.error('Erreur chargement UEs', err)
  }
}

const openModal = (mode, teacher = null) => {
  modalMode.value = mode
  if (mode === 'edit' && teacher) {
    currentTeacher.value = teacher
    formData.value = {
      nom: teacher.nom,
      prenom: teacher.prenom,
      email: teacher.email,
      matricule: teacher.matricule,
      telephone: teacher.telephone || '',
      specialite: teacher.specialite || ''
    }
  } else {
    resetForm()
  }
  showModal.value = true
}

const resetForm = () => {
  formData.value = { nom: '', prenom: '', email: '', matricule: 'ENS-', telephone: '', specialite: '' }
}

const closeModal = () => {
  showModal.value = false
  currentTeacher.value = null
}

const saveTeacher = async () => {
  loading.value = true
  try {
    const isAdd = modalMode.value === 'add'
    const url = isAdd ? '/enseignants/' : `/enseignants/${currentTeacher.value.id}/`
    const method = isAdd ? 'POST' : 'PATCH'
    
    const payload = { ...formData.value }
    if (isAdd) payload.password = formData.value.matricule

    await fetchApi(url, { method, body: payload })
    await loadTeachers()
    closeModal()
  } catch (err) {
    alert(err.data?.error || "Erreur lors de l'enregistrement")
  } finally {
    loading.value = false
  }
}

const deleteTeacher = async (id) => {
  if (!confirm("Supprimer définitivement cet enseignant ?")) return
  try {
    await fetchApi(`/enseignants/${id}/`, { method: 'DELETE' })
    await loadTeachers()
  } catch (err) {
    alert("Erreur lors de la suppression")
  }
}

// Assignation
const openAssignModal = (teacher) => {
  selectedTeacher.value = teacher
  selectedMatieres.value = teacher.matiere_ids || []
  showAssignModal.value = true
}

const closeAssignModal = () => {
  showAssignModal.value = false
  selectedTeacher.value = null
}

const assignMatieres = async () => {
  loading.value = true
  try {
    await fetchApi(`/enseignants/${selectedTeacher.value.id}/assign-matieres/`, {
      method: 'POST',
      body: { matiere_ids: selectedMatieres.value }
    })
    await loadTeachers()
    closeAssignModal()
  } catch (err) {
    alert("Erreur lors de l'assignation")
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadTeachers()
  loadUEs()
})
</script>

<style scoped>
.page-enseignants {
  padding: 1rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header-content h2 { margin: 0; font-size: 1.8rem; color: #1e293b; }
.header-content p { margin: 0.5rem 0 0; color: #64748b; }

.filters-card {
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  background: #f1f5f9;
  padding: 0.5rem 1rem;
  border-radius: 0.75rem;
  width: 100%;
  max-width: 400px;
}

.search-input {
  background: transparent;
  border: none;
  margin-left: 0.5rem;
  width: 100%;
  outline: none;
}

.stats-badge {
  background: #e0f2fe;
  color: #0369a1;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.9rem;
}

/* Grid layout for teachers */
.teachers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.teacher-card {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  position: relative;
  transition: transform 0.2s;
}

.teacher-card:hover { transform: translateY(-4px); }

.teacher-card-inner {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.teacher-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.teacher-avatar {
  width: 50px;
  height: 50px;
  background: #3b82f6;
  color: white;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
}

.teacher-identity h3 { margin: 0; font-size: 1.1rem; color: #1e293b; }
.matricule-badge { font-size: 0.75rem; color: #3b82f6; font-weight: 600; background: #eff6ff; padding: 2px 6px; border-radius: 4px; }

.teacher-body { flex: 1; display: flex; flex-direction: column; gap: 0.75rem; }

.info-item { display: flex; justify-content: space-between; font-size: 0.9rem; }
.info-label { color: #64748b; }
.info-value { font-weight: 500; color: #334155; }
.info-value.highlight { color: #2563eb; }

.matieres-section { margin-top: 0.5rem; }
.matieres-tags { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }
.tag-matiere { background: #f8fafc; border: 1px solid #e2e8f0; color: #475569; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; }
.empty-msg { font-size: 0.8rem; color: #94a3b8; font-style: italic; }

.teacher-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
  display: flex;
  gap: 0.75rem;
}

.action-btn {
  flex: 1;
  border: none;
  background: #f8fafc;
  padding: 0.5rem;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-edit:hover { background: #dcfce7; color: #166534; }
.btn-assign:hover { background: #dbeafe; color: #1e40af; }
.btn-delete:hover { background: #fee2e2; color: #991b1b; }

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-window {
  background: white;
  width: 100%;
  max-width: 600px;
  border-radius: 1.25rem;
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 { margin: 0; font-size: 1.25rem; }
.header-title p { margin: 4px 0 0; color: #3b82f6; font-weight: 500; font-size: 0.9rem; }

.btn-close { background: none; border: none; font-size: 1.2rem; cursor: pointer; color: #94a3b8; }

.modal-body { padding: 1.5rem; }
.modal-body.scrollable { max-height: 60vh; overflow-y: auto; }

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-group { display: flex; flex-direction: column; gap: 0.5rem; }
.form-group label { font-size: 0.85rem; font-weight: 600; color: #475569; }
.form-input { 
  padding: 0.6rem 0.75rem; 
  border: 1px solid #e2e8f0; 
  border-radius: 0.5rem; 
  outline: none;
  transition: border-color 0.2s;
}
.form-input:focus { border-color: #3b82f6; }
.hint { font-size: 0.75rem; color: #94a3b8; }

.credentials-info {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 0.75rem;
  margin-bottom: 1.5rem;
  border: 1px dashed #cbd5e1;
}

.credentials-info p { margin: 0; font-size: 0.85rem; color: #475569; }

.form-footer {
  padding: 1.5rem;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* Assign modal specific */
.ue-stack { display: flex; flex-direction: column; gap: 1.5rem; }
.ue-header { 
  padding: 0.5rem 0; 
  border-bottom: 2px solid #3b82f6; 
  font-weight: 700; 
  font-size: 0.95rem;
  display: flex;
  justify-content: space-between;
}
.ue-code { color: #94a3b8; font-weight: 400; font-size: 0.85rem; }

.matieres-checklist { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.75rem; }

.matiere-check-label {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border: 1px solid #f1f5f9;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.matiere-check-label:hover { border-color: #3b82f6; background: #eff6ff; }

.matiere-check-label input { display: none; }
.check-custom {
  width: 20px;
  height: 20px;
  border: 2px solid #cbd5e1;
  border-radius: 6px;
  margin-right: 1rem;
  position: relative;
}

.matiere-check-label input:checked + .check-custom {
  background: #3b82f6;
  border-color: #3b82f6;
}

.matiere-check-label input:checked + .check-custom::after {
  content: '✓';
  position: absolute;
  color: white;
  font-size: 14px;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}

.matiere-info { display: flex; flex-direction: column; }
.m-name { font-weight: 600; font-size: 0.95rem; color: #1e293b; }
.m-meta { font-size: 0.8rem; color: #64748b; }

.btn {
  padding: 0.6rem 1.25rem;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary { background: #2563eb; color: white; }
.btn-primary:hover { background: #1e40af; }
.btn-ghost { background: transparent; color: #64748b; }
.btn-ghost:hover { background: #f1f5f9; }

@media (max-width: 640px) {
  .form-grid { grid-template-columns: 1fr; }
  .page-header { flex-direction: column; align-items: stretch; gap: 1rem; }
  .filters-card { flex-direction: column; gap: 1rem; }
}
</style>
