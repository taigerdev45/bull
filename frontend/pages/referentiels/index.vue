<template>
  <div class="page-container">
    <header class="page-header">
      <div class="header-info">
        <h1>Référentiels Pédagogiques</h1>
        <p>Gérez les Unités d'Enseignement et les matières associées.</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="openUEModal('add')">
          <span>➕</span> Créer une UE
        </button>
      </div>
    </header>

    <div v-if="pending" class="loader">
      <div class="spinner"></div>
      <p>Chargement de la structure...</p>
    </div>

    <div v-else-if="ues.length === 0" class="empty-state">
      <div class="empty-icon">📚</div>
      <h3>Aucune UE configurée</h3>
      <p>Créez votre première Unité d'Enseignement.</p>
      <button class="btn btn-primary" @click="openUEModal('add')">➕ Créer une UE</button>
    </div>

    <div v-else class="referentiels-grid">
      <div v-for="ue in ues" :key="ue.id" class="ue-card">
        <div class="ue-header">
          <div class="ue-title">
            <span class="ue-code">{{ ue.code }}</span>
            <h3>{{ ue.libelle }}</h3>
          </div>
          <div class="ue-meta">
            <span class="badge">Semestre {{ ue.semestre_id }}</span>
            <div class="header-actions-group">
              <button class="icon-btn" title="Modifier" @click="openUEModal('edit', ue)">✏️</button>
              <button class="icon-btn delete" title="Supprimer" @click="confirmDeleteUE(ue)">🗑️</button>
            </div>
          </div>
        </div>

        <div class="ue-content">
          <table class="matiere-list">
            <thead>
              <tr>
                <th>Matière</th>
                <th class="center">Coeff.</th>
                <th class="center">Crédits</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="mat in (ue.matieres || [])" :key="mat.id">
                <td class="m-name">{{ mat.libelle }}</td>
                <td class="m-val center">{{ mat.coefficient }}</td>
                <td class="m-val center">{{ mat.credits }}</td>
                <td class="m-actions">
                  <button title="Modifier" @click="openMatiereModal('edit', mat, ue)">✏️</button>
                  <button title="Supprimer" @click="confirmDeleteMatiere(mat)">🗑️</button>
                </td>
              </tr>
              <tr v-if="!(ue.matieres?.length)">
                <td colspan="4" class="empty-m">Aucune matière affectée.</td>
              </tr>
            </tbody>
          </table>
          <button class="add-m-btn" @click="openMatiereModal('add', null, ue)">
            <span>➕</span> Ajouter une matière
          </button>
        </div>

        <div class="ue-footer">
          <div class="total-badge">
            <span class="t-lbl">Crédits Totaux</span>
            <span class="t-val">{{ totalCredits(ue) }} / 30</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ─── Modal UE ─────────────────────────────────────────────── -->
    <Transition name="modal-fade">
      <div v-if="ueModal.show" class="modal-overlay" @click.self="ueModal.show = false">
        <div class="modal-box">
          <div class="modal-header">
            <h2>{{ ueModal.mode === 'add' ? 'Nouvelle Unité d\'Enseignement' : 'Modifier l\'UE' }}</h2>
            <button class="modal-close" @click="ueModal.show = false">✕</button>
          </div>
          <form class="modal-form" @submit.prevent="submitUE">
            <div class="form-grid">
              <div class="form-group">
                <label>Code UE</label>
                <input v-model="ueForm.code" required placeholder="Ex: UE5-1" :readonly="ueModal.mode === 'edit'" />
                <span class="hint">Format : UE5-1, UE6-2...</span>
              </div>
              <div class="form-group">
                <label>Semestre</label>
                <select v-model.number="ueForm.semestre_id" required>
                  <option value="">-- Choisir --</option>
                  <option :value="5">Semestre 5</option>
                  <option :value="6">Semestre 6</option>
                </select>
              </div>
              <div class="form-group full-width">
                <label>Libellé</label>
                <input v-model="ueForm.libelle" required placeholder="Ex: Enseignement Général" />
              </div>
              <div class="form-group">
                <label>Crédits ECTS</label>
                <input v-model.number="ueForm.credits" type="number" required min="1" max="30" placeholder="6" />
              </div>
            </div>
            <div v-if="ueModal.error" class="form-error">⚠️ {{ ueModal.error }}</div>
            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" @click="ueModal.show = false">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="ueModal.loading">
                {{ ueModal.loading ? 'Enregistrement...' : '✅ ' + (ueModal.mode === 'add' ? 'Créer' : 'Mettre à jour') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>

    <!-- ─── Modal Matière ─────────────────────────────────────────── -->
    <Transition name="modal-fade">
      <div v-if="matiereModal.show" class="modal-overlay" @click.self="matiereModal.show = false">
        <div class="modal-box">
          <div class="modal-header">
            <h2>{{ matiereModal.mode === 'add' ? 'Ajouter une Matière' : 'Modifier la Matière' }}</h2>
            <button class="modal-close" @click="matiereModal.show = false">✕</button>
          </div>
          <form class="modal-form" @submit.prevent="submitMatiere">
            <div class="form-grid">
              <div class="form-group full-width">
                <label>Libellé de la matière</label>
                <input v-model="matiereForm.libelle" required placeholder="Ex: Mathématiques Appliquées" />
              </div>
              <div class="form-group">
                <label>Coefficient</label>
                <input v-model.number="matiereForm.coefficient" type="number" required min="1" step="0.5" placeholder="2" />
              </div>
              <div class="form-group">
                <label>Crédits ECTS</label>
                <input v-model.number="matiereForm.credits" type="number" required min="1" placeholder="3" />
              </div>
              <div class="form-group full-width">
                <label>UE Associée</label>
                <select v-model="matiereForm.ue_id" required>
                  <option v-for="ue in ues" :key="ue.id" :value="ue.code">{{ ue.code }} — {{ ue.libelle }}</option>
                </select>
              </div>
            </div>
            <div v-if="matiereModal.error" class="form-error">⚠️ {{ matiereModal.error }}</div>
            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" @click="matiereModal.show = false">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="matiereModal.loading">
                {{ matiereModal.loading ? 'Enregistrement...' : '✅ ' + (matiereModal.mode === 'add' ? 'Ajouter' : 'Modifier') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useApi } from '~/composables/useApi'

useHead({ title: 'Référentiels | Bull ASUR' })

const { fetchApi } = useApi()
const ues = ref([])
const pending = ref(true)

// ─── State Modals ─────────────────────────────────────────────────
const ueModal = reactive({ show: false, mode: 'add', loading: false, error: '', editId: null })
const matiereModal = reactive({ show: false, mode: 'add', loading: false, error: '', editId: null })

const defaultUEForm = { code: '', libelle: '', credits: 6, semestre_id: '' }
const defaultMatiereForm = { libelle: '', coefficient: 2, credits: 3, ue_id: '', enseignant_id: null }

const ueForm = reactive({ ...defaultUEForm })
const matiereForm = reactive({ ...defaultMatiereForm })

// ─── Data Fetch ───────────────────────────────────────────────────
const fetchReferentiel = async () => {
  pending.value = true
  try {
    const data = await fetchApi('/ues/')
    ues.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('Fetch referentiel error', e)
    ues.value = []
  } finally {
    pending.value = false
  }
}

onMounted(fetchReferentiel)

// ─── Helpers ──────────────────────────────────────────────────────
const totalCredits = (ue) => (ue.matieres || []).reduce((acc, m) => acc + (m.credits || 0), 0)

// ─── UE Actions ───────────────────────────────────────────────────
const openUEModal = (mode, ue = null) => {
  ueModal.mode = mode
  ueModal.error = ''
  ueModal.editId = ue?.id || null
  if (mode === 'edit' && ue) {
    Object.assign(ueForm, { code: ue.code, libelle: ue.libelle, credits: ue.credits, semestre_id: ue.semestre_id })
  } else {
    Object.assign(ueForm, defaultUEForm)
  }
  ueModal.show = true
}

const submitUE = async () => {
  ueModal.loading = true
  ueModal.error = ''
  try {
    if (ueModal.mode === 'add') {
      await fetchApi('/ues/', { method: 'POST', body: { ...ueForm } })
    } else {
      await fetchApi(`/ues/${ueModal.editId}/`, { method: 'PUT', body: { ...ueForm } })
    }
    ueModal.show = false
    await fetchReferentiel()
  } catch (err) {
    ueModal.error = err.data?.code?.[0] || err.data?.error || err.data?.libelle?.[0] || 'Erreur lors de la sauvegarde. Vérifiez le format du code UE (ex: UE5-1).'
  } finally {
    ueModal.loading = false
  }
}

const confirmDeleteUE = async (ue) => {
  if (!confirm(`Supprimer l'UE ${ue.code} et toutes ses matières ?`)) return
  try {
    await fetchApi(`/ues/${ue.id}/`, { method: 'DELETE' })
    await fetchReferentiel()
  } catch (err) {
    alert(err.data?.error || 'Impossible de supprimer cette UE.')
  }
}

// ─── Matière Actions ──────────────────────────────────────────────
const openMatiereModal = (mode, mat = null, ue = null) => {
  matiereModal.mode = mode
  matiereModal.error = ''
  matiereModal.editId = mat?.id || null
  if (mode === 'edit' && mat) {
    Object.assign(matiereForm, { libelle: mat.libelle, coefficient: mat.coefficient, credits: mat.credits, ue_id: mat.ue_id })
  } else {
    Object.assign(matiereForm, { ...defaultMatiereForm, ue_id: ue?.code || '' })
  }
  matiereModal.show = true
}

const submitMatiere = async () => {
  matiereModal.loading = true
  matiereModal.error = ''
  try {
    if (matiereModal.mode === 'add') {
      await fetchApi('/matieres/', { method: 'POST', body: { ...matiereForm } })
    } else {
      await fetchApi(`/matieres/${matiereModal.editId}/`, { method: 'PUT', body: { ...matiereForm } })
    }
    matiereModal.show = false
    await fetchReferentiel()
  } catch (err) {
    matiereModal.error = err.data?.error || err.data?.libelle?.[0] || 'Erreur lors de la sauvegarde.'
  } finally {
    matiereModal.loading = false
  }
}

const confirmDeleteMatiere = async (mat) => {
  if (!confirm(`Supprimer la matière "${mat.libelle}" ?`)) return
  try {
    await fetchApi(`/matieres/${mat.id}/`, { method: 'DELETE' })
    await fetchReferentiel()
  } catch (err) {
    alert(err.data?.error || 'Impossible de supprimer cette matière.')
  }
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; }
.header-info h1 { font-size: 1.75rem; font-weight: 800; color: #1e293b; margin: 0; }
.header-info p { color: #64748b; font-size: 1rem; margin: 0.25rem 0 0; }

.referentiels-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 2rem; }

.ue-card { background: white; border-radius: var(--radius-lg); border: 1px solid var(--border-light); box-shadow: var(--shadow-sm); overflow: hidden; display: flex; flex-direction: column; transition: all 0.2s; }
.ue-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }

.ue-header { padding: 1.5rem; background: #f8fafc; border-bottom: 1px solid var(--border-light); display: flex; justify-content: space-between; align-items: flex-start; }
.ue-title { display: flex; flex-direction: column; gap: 0.25rem; }
.ue-code { font-size: 0.7rem; font-weight: 800; color: var(--primary); text-transform: uppercase; letter-spacing: 1px; }
.ue-title h3 { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin: 0; }

.ue-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 0.75rem; }
.badge { background: #eef2ff; color: #3730a3; font-size: 0.7rem; font-weight: 700; padding: 0.35rem 0.75rem; border-radius: 999px; }

.header-actions-group { display: flex; gap: 0.5rem; }
.icon-btn { background: none; border: none; cursor: pointer; padding: 0.25rem; opacity: 0.4; transition: opacity 0.2s; font-size: 1.1rem; }
.icon-btn:hover { opacity: 1; }
.icon-btn.delete:hover { color: #dc2626; }

.ue-content { padding: 1rem 1.5rem; flex: 1; }
.matiere-list { width: 100%; border-collapse: collapse; }
.matiere-list th { padding: 0.75rem 0.5rem; text-align: left; font-size: 0.65rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; border-bottom: 1px solid #f1f5f9; }
.matiere-list td { padding: 0.85rem 0.5rem; border-bottom: 1px solid #f1f5f9; font-size: 0.9rem; }
.matiere-list tr:last-child td { border-bottom: none; }
.center { text-align: center !important; }
.m-name { font-weight: 600; color: #334155; }
.m-val { font-weight: 700; color: #0f172a; }
.m-actions { text-align: right; display: flex; gap: 0.25rem; justify-content: flex-end; }
.m-actions button { background: none; border: none; cursor: pointer; padding: 0.25rem; opacity: 0.3; transition: opacity 0.2s; font-size: 0.9rem; }
.m-actions button:hover { opacity: 1; }
.empty-m { text-align: center; color: #94a3b8; padding: 2rem; font-style: italic; }

.add-m-btn { width: 100%; margin-top: 1.5rem; padding: 0.75rem; border: 1px dashed var(--border-light); background: #fdfdfd; color: #64748b; font-weight: 600; border-radius: var(--radius-md, 10px); cursor: pointer; font-size: 0.8rem; transition: all 0.2s; }
.add-m-btn:hover { border-color: var(--primary); color: var(--primary); background: #eff6ff; }

.ue-footer { padding: 1rem 1.5rem; background: #f8fafc; border-top: 1px solid var(--border-light); display: flex; justify-content: flex-end; }
.total-badge { background: white; border: 1px solid var(--border-light); padding: 0.5rem 1rem; border-radius: 12px; display: flex; gap: 0.75rem; align-items: center; box-shadow: var(--shadow-sm); }
.t-lbl { font-size: 0.65rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
.t-val { font-size: 1rem; font-weight: 800; color: var(--primary); }

.loader { display: flex; flex-direction: column; align-items: center; padding: 5rem; }
.spinner { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state { display: flex; flex-direction: column; align-items: center; padding: 5rem; background: white; border-radius: 16px; border: 2px dashed var(--border-light); text-align: center; }
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-state h3 { font-size: 1.25rem; font-weight: 700; color: #1e293b; }
.empty-state p { color: #64748b; margin-bottom: 1.5rem; }

/* Buttons */
.btn { padding: 0.7rem 1.25rem; border-radius: 10px; font-weight: 700; font-size: 0.9rem; cursor: pointer; border: none; display: flex; align-items: center; gap: 0.5rem; transition: all 0.2s; }
.btn-primary { background: var(--primary); color: white; box-shadow: 0 4px 12px var(--primary-glow, rgba(99,102,241,.3)); }
.btn-primary:hover { filter: brightness(1.1); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-ghost { background: #f1f5f9; color: #64748b; }
.btn-ghost:hover { background: #e2e8f0; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(15,23,42,0.55); display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 1rem; backdrop-filter: blur(4px); }
.modal-box { background: white; border-radius: 20px; width: 100%; max-width: 560px; box-shadow: 0 25px 50px rgba(0,0,0,0.25); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2rem; border-bottom: 1px solid #f1f5f9; }
.modal-header h2 { font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 0; }
.modal-close { background: none; border: none; font-size: 1.1rem; cursor: pointer; color: #94a3b8; }
.modal-form { padding: 1.5rem 2rem; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
.form-group { display: flex; flex-direction: column; gap: 0.4rem; }
.form-group.full-width { grid-column: 1 / -1; }
.form-group label { font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }
.form-group input, .form-group select { padding: 0.75rem 1rem; border: 1.5px solid #e2e8f0; border-radius: 9px; font-size: 0.95rem; color: #0f172a; background: #f8fafc; outline: none; transition: border-color 0.2s; }
.form-group input:focus, .form-group select:focus { border-color: #6366f1; background: white; }
.form-group input[readonly] { background: #f1f5f9; color: #64748b; cursor: not-allowed; }
.hint { font-size: 0.72rem; color: #94a3b8; margin-top: -0.2rem; }
.form-error { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 0.75rem 1rem; border-radius: 8px; font-size: 0.88rem; margin-top: 1rem; }
.modal-footer { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #f1f5f9; }

.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.25s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
</style>
