<template>
  <div class="page-container">
     <div class="breadcrumb-nav">
        <NuxtLink to="/saisie">← Retour aux évaluations</NuxtLink>
     </div>

     <div v-if="pending" class="loader">
        <div class="spinner"></div>
     </div>

     <template v-else>
       <header class="page-header">
          <div class="header-info">
             <span class="eval-type-badge">{{ evaluation?.type }}</span>
             <h1>Saisie : {{ evaluation?.matiere_libelle }}</h1>
             <p>Promo ASUR • Session {{ evaluation?.session }} • {{ formatDate(evaluation?.date) }}</p>
          </div>
          <div class="header-actions">
             <button class="btn btn-secondary" @click="fetchData">
               <span>🔄</span> Actualiser
             </button>
             <button class="btn btn-primary" @click="saveAll" :disabled="saving">
               <span>💾</span> {{ saving ? 'Enregistrement...' : 'Enregistrer tout' }}
             </button>
          </div>
       </header>

       <div class="notes-table-card">
          <table class="notes-table">
             <thead>
                <tr>
                   <th>Étudiant</th>
                   <th width="120" class="center">Note / 20</th>
                   <th>Observations / Commentaires</th>
                </tr>
             </thead>
             <tbody>
                <tr v-for="note in notes" :key="note.etudiant_id">
                   <td class="st-name">
                     <div class="st-avatar">{{ (note.nom || 'E').charAt(0) }}</div>
                     <span>{{ note.nom }} {{ note.prenom }}</span>
                   </td>
                   <td>
                      <input type="number" step="0.25" min="0" max="20" v-model="note.valeur" class="note-input" />
                   </td>
                   <td>
                      <input type="text" v-model="note.observation" placeholder="Ajouter un commentaire..." class="obs-input" />
                   </td>
                </tr>
                <tr v-if="notes.length === 0">
                   <td colspan="3" class="empty">Aucun étudiant inscrit dans cette promotion.</td>
                </tr>
             </tbody>
          </table>
       </div>
     </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useApi } from '~/composables/useApi'

const route = useRoute()
const { fetchApi } = useApi()
const evaluation = ref(null)
const notes = ref([])
const pending = ref(true)
const saving = ref(false)

const fetchData = async () => {
  pending.value = true
  try {
    const evalId = route.params.id
    const evalData = await fetchApi(`/evaluations/${evalId}/`)
    evaluation.value = evalData
    
    // On récupère les notes existantes ou on pré-remplit
    const notesData = await fetchApi(`/evaluations/${evalId}/notes/`)
    notes.value = notesData || []
  } catch (e) {
    console.error('Fetch detail error', e)
  } finally {
    pending.value = false
  }
}

onMounted(fetchData)

const formatDate = (d) => {
  if (!d) return ''
  return new Date(d).toLocaleDateString()
}

const saveAll = async () => {
  saving.value = true
  try {
    const evalId = route.params.id
    await fetchApi(`/evaluations/${evalId}/notes/bulk_update/`, {
      method: 'POST',
      body: { notes: notes.value }
    })
    alert('Notes enregistrées avec succès !')
  } catch (e) {
    alert('Erreur lors de la sauvegarde.')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.breadcrumb-nav { margin-bottom: 1.5rem; }
.breadcrumb-nav a { 
  color: var(--text-muted); 
  text-decoration: none; 
  font-weight: 600; 
  font-size: 0.85rem; 
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.breadcrumb-nav a:hover { color: var(--primary); }

.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; }
.header-info h1 { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0; }
.header-info p { color: #64748b; font-size: 0.95rem; margin-top: 0.25rem; }

.eval-type-badge { 
  background: #f1f5f9; 
  color: #475569; 
  padding: 0.3rem 0.8rem; 
  border-radius: 99px; 
  font-size: 0.7rem; 
  font-weight: 800; 
  text-transform: uppercase; 
  margin-bottom: 0.75rem; 
  display: inline-block;
  border: 1px solid #e2e8f0;
}

.notes-table-card { background: white; border-radius: var(--radius-lg); border: 1px solid var(--border-light); shadow: var(--shadow-sm); overflow: hidden; }
.notes-table { width: 100%; border-collapse: collapse; }
.notes-table th { padding: 1.25rem; background: #f8fafc; text-align: left; font-size: 0.7rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
.notes-table td { padding: 0.85rem 1.25rem; border-bottom: 1px solid #f1f5f9; }

.st-name { display: flex; align-items: center; gap: 1rem; font-weight: 600; color: #334155; }
.st-avatar { width: 32px; height: 32px; background: #eef2ff; color: var(--primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 800; }

.note-input { width: 100%; padding: 0.65rem; border: 1px solid #e2e8f0; border-radius: 8px; font-weight: 800; font-size: 1.15rem; color: var(--primary); text-align: center; background: #fbfcfe; transition: all 0.2s; }
.note-input:focus { border-color: var(--primary); outline: none; background: white; box-shadow: 0 0 0 4px var(--primary-glow); }

.obs-input { width: 100%; padding: 0.65rem; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.9rem; transition: all 0.2s; }
.obs-input:focus { border-color: var(--primary); outline: none; box-shadow: 0 0 0 4px var(--primary-glow); }

.center { text-align: center; }
.empty { text-align: center; padding: 4rem; color: #94a3b8; font-style: italic; }

.btn { padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; border: none; font-size: 0.9rem; }
.btn-primary { background: var(--primary); color: white; box-shadow: 0 4px 12px var(--primary-glow); }
.btn-secondary { background: white; border: 1px solid var(--border-light); color: #334155; }

.loader { display: flex; justify-content: center; padding: 5rem; }
.spinner { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
