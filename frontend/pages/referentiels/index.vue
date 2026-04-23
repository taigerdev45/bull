<template>
  <div class="page-container">
    <header class="page-header">
      <div class="header-info">
        <h1>Référentiels Pédagogiques</h1>
        <p>Structure des Unités d'Enseignement et des matières associées.</p>
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
              <button class="icon-btn edit" @click="openUEModal('edit', ue)">✏️</button>
              <button class="icon-btn delete" @click="confirmDeleteUE(ue)">🗑️</button>
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
              <tr v-for="mat in ue.matieres" :key="mat.id">
                <td class="m-name">{{ mat.libelle }}</td>
                <td class="m-val center">{{ mat.coefficient }}</td>
                <td class="m-val center">{{ mat.credits }}</td>
                <td class="m-actions">
                  <button @click="editMatiere(mat, ue)">✏️</button>
                </td>
              </tr>
              <tr v-if="!ue.matieres?.length">
                <td colspan="4" class="empty-m">Aucune matière affectée.</td>
              </tr>
            </tbody>
          </table>
          
          <button class="add-m-btn" @click="addMatiere(ue)">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

const { fetchApi } = useApi()
const ues = ref([])
const pending = ref(true)

const fetchReferentiel = async () => {
  pending.value = true
  try {
    const data = await fetchApi('/referentiels/ue/')
    if (data) ues.value = data
  } catch (e) {
    console.error('Fetch referentiel error', e)
  } finally {
    pending.value = false
  }
}

onMounted(fetchReferentiel)

const totalCredits = (ue) => {
  if (!ue.matieres) return 0
  return ue.matieres.reduce((acc, m) => acc + (m.credits || 0), 0)
}

const openUEModal = (mode, ue = null) => {
  alert('Fonctionnalité en cours de refonte...')
}

const confirmDeleteUE = (ue) => {
  if(confirm(`Supprimer l'UE ${ue.code} ?`)) {
     alert('Option de suppression désactivée en mode démo.')
  }
}

const addMatiere = (ue) => {
  alert(`Ajout de matière à l'UE ${ue.code}`)
}

const editMatiere = (mat, ue) => {
  alert(`Édition de ${mat.libelle}`)
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

.ue-content { padding: 1rem 1.5rem; flex: 1; }
.matiere-list { width: 100%; border-collapse: collapse; }
.matiere-list th { padding: 0.75rem 0.5rem; text-align: left; font-size: 0.65rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; border-bottom: 1px solid #f1f5f9; }
.matiere-list td { padding: 0.85rem 0.5rem; border-bottom: 1px solid #f1f5f9; font-size: 0.9rem; }
.matiere-list tr:last-child td { border-bottom: none; }

.center { text-align: center !important; }
.m-name { font-weight: 600; color: #334155; }
.m-val { font-weight: 700; color: #0f172a; }
.m-actions { text-align: right; }
.m-actions button { background: none; border: none; cursor: pointer; padding: 0.25rem; opacity: 0.3; transition: opacity 0.2s; }
.m-actions button:hover { opacity: 1; }

.empty-m { text-align: center; color: #94a3b8; padding: 2rem; font-style: italic; }

.add-m-btn { width: 100%; margin-top: 1.5rem; padding: 0.75rem; border: 1px dashed var(--border-light); background: #fdfdfd; color: #64748b; font-weight: 600; border-radius: var(--radius-md); cursor: pointer; font-size: 0.8rem; transition: all 0.2s; }
.add-m-btn:hover { border-color: var(--primary); color: var(--primary); background: #eff6ff; }

.ue-footer { padding: 1rem 1.5rem; background: #f8fafc; border-top: 1px solid var(--border-light); display: flex; justify-content: flex-end; }
.total-badge { background: white; border: 1px solid var(--border-light); padding: 0.5rem 1rem; border-radius: 12px; display: flex; gap: 0.75rem; align-items: center; box-shadow: var(--shadow-sm); }
.t-lbl { font-size: 0.65rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
.t-val { font-size: 1rem; font-weight: 800; color: var(--primary); }

.loader { display: flex; flex-direction: column; align-items: center; padding: 5rem; }
.spinner { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }

.btn { padding: 0.7rem 1.25rem; border-radius: 8px; font-weight: 700; font-size: 0.9rem; cursor: pointer; border: none; display: flex; align-items: center; gap: 0.5rem; }
.btn-primary { background: var(--primary); color: white; }
</style>
