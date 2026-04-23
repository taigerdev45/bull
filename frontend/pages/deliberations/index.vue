<template>
  <div class="page-container">
     <header class="page-header">
        <div class="header-info">
           <h1>Procès Verbaux & Délibérations</h1>
           <p>Validation collective des résultats par promotion et par semestre.</p>
        </div>
        <div class="header-actions">
           <button class="btn btn-primary" @click="startDelib">
             <span>📢</span> Lancer la Délibération
           </button>
        </div>
     </header>

     <div class="stats-mini-grid">
        <div class="mini-stat">
           <span class="label">Admis (Session Normale)</span>
           <span class="value success">82%</span>
        </div>
        <div class="mini-stat">
           <span class="label">En Rattrapage</span>
           <span class="value warning">18%</span>
        </div>
        <div class="mini-stat">
           <span class="label">Moyenne Générale Promo</span>
           <span class="value">11.24</span>
        </div>
     </div>

     <div class="pv-card">
        <UiDataTable 
          title="Registre de Délibération - S5" 
          subtitle="Résultats synthétiques pour validation du jury"
          :columns="columns" 
          :data="results" 
          :actions="true"
        >
           <template #moyenne="{ row }">
              <strong :class="row.moyenne >= 10 ? 'text-success' : 'text-danger'">
                 {{ row.moyenne.toFixed(2) }}
              </strong>
           </template>
           <template #decision="{ row }">
              <span :class="['badge', row.moyenne >= 10 ? 'badge-success' : 'badge-danger']">
                 {{ row.moyenne >= 10 ? 'ADMIS' : 'RATTRAPAGE' }}
              </span>
           </template>
           <template #rowActions="{ row }">
              <button class="action-btn" @click="viewDetails(row)">Détails</button>
           </template>
        </UiDataTable>
     </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import UiDataTable from '~/components/ui/DataTable.vue'

useHead({ title: 'Délibérations | Bull ASUR' })

const columns = [
  { key: 'matricule', label: 'Matricule' },
  { key: 'nom', label: 'Nom & Prénom' },
  { key: 'moyenne', label: 'Moyenne' },
  { key: 'credits', label: 'Crédits' },
  { key: 'decision', label: 'Décision Jury' }
]

const results = ref([
  { id: 1, matricule: '23ASUR001', nom: 'MOUKIKA Brady', moyenne: 14.50, credits: 30 },
  { id: 2, matricule: '23ASUR002', nom: 'MBA NSOME Yannick', moyenne: 12.75, credits: 30 },
  { id: 3, matricule: '23ASUR003', nom: 'ZUE David', moyenne: 9.80, credits: 24 },
  { id: 4, matricule: '23ASUR004', nom: 'NDONG Marie', moyenne: 11.20, credits: 30 }
])

const startDelib = () => { alert('Simulation du moteur de délibération...') }
const viewDetails = (row) => { alert(`Détails pour ${row.nom}`) }
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; }
.header-info h1 { font-size: 1.75rem; font-weight: 800; color: #1e293b; margin: 0; }
.header-info p { color: #64748b; font-size: 1rem; margin-top: 0.25rem; }

.stats-mini-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 2rem; }
.mini-stat { background: white; padding: 1.5rem; border-radius: var(--radius-lg); border: 1px solid var(--border-light); display: flex; flex-direction: column; gap: 0.25rem; box-shadow: var(--shadow-sm); }
.mini-stat .label { font-size: 0.7rem; color: #64748b; font-weight: 800; text-transform: uppercase; }
.mini-stat .value { font-size: 1.75rem; font-weight: 800; color: #1e293b; }
.mini-stat .value.success { color: #10b981; }
.mini-stat .value.warning { color: #f59e0b; }

.pv-card { background: white; border-radius: var(--radius-xl); border: 1px solid var(--border-light); overflow: hidden; }

.text-success { color: #059669; }
.text-danger { color: #dc2626; }

.badge { padding: 0.35rem 0.85rem; border-radius: 99px; font-size: 0.7rem; font-weight: 800; }
.badge-success { background: #ecfdf5; color: #065f46; }
.badge-danger { background: #fef2f2; color: #991b1b; }

.action-btn { background: #f1f5f9; border: none; padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; color: #475569; }
.action-btn:hover { background: #e2e8f0; color: #0f172a; }

.btn { padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; border: none; font-size: 0.9rem; transition: all 0.2s; }
.btn-primary { background: var(--primary); color: white; box-shadow: 0 4px 12px var(--primary-glow); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 16px var(--primary-glow); }
</style>
