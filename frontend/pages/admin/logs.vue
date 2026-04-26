<template>
  <div class="page-container">
    <header class="page-header">
      <div class="header-info">
        <h1>📑 Journaux d'Audit</h1>
        <p>Suivi de toutes les actions critiques effectuées sur la plateforme.</p>
      </div>
      <div class="header-actions">
        <div class="export-dropdown" v-if="logs.length">
          <button class="btn btn-secondary shadow-sm">
            <span>📥</span> Exporter
          </button>
          <div class="dropdown-menu">
            <button @click="handleExport('excel')">Excel (.xlsx)</button>
            <button @click="handleExport('pdf-p')">PDF Portrait</button>
            <button @click="handleExport('pdf-l')">PDF Paysage</button>
          </div>
        </div>
        <button class="btn btn-ghost" @click="fetchLogs">
          <span>🔄</span> Actualiser
        </button>
      </div>
    </header>

    <!-- Filtres -->
    <div class="filter-card">
      <div class="filter-grid">
        <div class="field">
          <label>Action</label>
          <select v-model="filters.action" @change="fetchLogs">
            <option value="">Toutes les actions</option>
            <option value="LOGIN">Connexion</option>
            <option value="CREATE_NOTE">Saisie de note</option>
            <option value="UPDATE_NOTE">Modif. note</option>
            <option value="GENERATE_BULLETIN">Génér. Bulletin</option>
            <option value="CREATE_STUDENT">Création Étudiant</option>
          </select>
        </div>
        <div class="field">
          <label>Type d'Entité</label>
          <select v-model="filters.entity_type" @change="fetchLogs">
            <option value="">Tous les types</option>
            <option value="etudiant">Étudiant</option>
            <option value="note">Note</option>
            <option value="bulletin">Bulletin</option>
            <option value="ue">UE / Matière</option>
          </select>
        </div>
        <div class="field">
          <label>Date Début</label>
          <input type="date" v-model="filters.date_debut" @change="fetchLogs">
        </div>
      </div>
    </div>

    <div v-if="pending" class="loader">
      <div class="spinner"></div>
      <p>Récupération des logs...</p>
    </div>

    <div v-else class="logs-container">
      <div class="table-wrapper">
        <table class="logs-table">
          <thead>
            <tr>
              <th>Date & Heure</th>
              <th>Action</th>
              <th>Utilisateur</th>
              <th>Entité</th>
              <th>Détails</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(log, idx) in logs" :key="idx">
              <td class="timestamp">{{ formatDateTime(log.timestamp) }}</td>
              <td><span class="badge" :class="getActionClass(log.action)">{{ log.action }}</span></td>
              <td class="user-id">{{ log.utilisateur_uid || 'Système' }}</td>
              <td><span class="entity-type">{{ log.entity_type }}</span> <small>{{ log.entity_id }}</small></td>
              <td class="details">{{ log.details }}</td>
            </tr>
            <tr v-if="logs.length === 0">
              <td colspan="5" class="empty-msg">Aucun log trouvé pour ces critères.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

useHead({ title: 'Journaux d\'Audit | Admin Bull ASUR' })

const { fetchApi } = useApi()
const { exportToExcel, exportToPDF } = useExport()

const logs = ref([])
const pending = ref(true)
const filters = ref({
  action: '',
  entity_type: '',
  date_debut: '',
  date_fin: ''
})

const fetchLogs = async () => {
  pending.value = true
  try {
    let query = ''
    const params = new URLSearchParams()
    if (filters.value.action) params.append('action', filters.value.action)
    if (filters.value.entity_type) params.append('entity_type', filters.value.entity_type)
    if (filters.value.date_debut) params.append('date_debut', filters.value.date_debut)
    
    const queryString = params.toString()
    const data = await fetchApi(`/audit/${queryString ? '?' + queryString : ''}`)
    logs.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error("Erreur logs:", e)
  } finally {
    pending.value = false
  }
}

const handleExport = (type) => {
  const data = logs.value.map(l => ({
    Date: formatDateTime(l.timestamp),
    Action: l.action,
    Utilisateur: l.utilisateur_uid || 'Système',
    Entité: l.entity_type,
    ID_Entité: l.entity_id,
    Détails: l.details
  }))

  if (type === 'excel') {
    exportToExcel(data, 'audit_logs_bullasur.xlsx')
  } else {
    const headers = ['Date', 'Action', 'Utilisateur', 'Détails']
    const rows = logs.value.map(l => [
      formatDateTime(l.timestamp),
      l.action,
      l.utilisateur_uid?.substring(0, 8) || 'Système',
      l.details?.substring(0, 50) + (l.details?.length > 50 ? '...' : '')
    ])
    exportToPDF(headers, rows, 'audit_logs.pdf', type === 'pdf-l' ? 'l' : 'p')
  }
}

const formatDateTime = (ts) => {
  if (!ts) return '-'
  return new Date(ts).toLocaleString('fr-FR')
}

const getActionClass = (action) => {
  if (action?.includes('CREATE')) return 'badge-create'
  if (action?.includes('UPDATE')) return 'badge-update'
  if (action?.includes('DELETE')) return 'badge-delete'
  if (action?.includes('LOGIN')) return 'badge-login'
  return 'badge-info'
}

onMounted(fetchLogs)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; }
.header-info h1 { font-size: 1.75rem; font-weight: 800; color: #1e293b; margin: 0; }
.header-info p { color: #64748b; margin-top: 0.25rem; }

.filter-card { background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.filter-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; }
.field { display: flex; flex-direction: column; gap: 0.5rem; }
.field label { font-size: 0.7rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
.field select, .field input { padding: 0.6rem; border: 1px solid #e2e8f0; border-radius: 6px; outline: none; font-size: 0.9rem; }

.logs-container { background: white; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
.table-wrapper { overflow-x: auto; }
.logs-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.logs-table th { background: #f8fafc; padding: 1rem; text-align: left; font-weight: 700; color: #475569; border-bottom: 1px solid #e2e8f0; }
.logs-table td { padding: 1rem; border-bottom: 1px solid #f1f5f9; vertical-align: top; }

.timestamp { color: #64748b; font-family: monospace; white-space: nowrap; }
.user-id { font-weight: 600; color: #334155; }
.entity-type { font-weight: 700; color: var(--primary); text-transform: capitalize; }
.details { color: #475569; line-height: 1.4; max-width: 400px; }

.badge { padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.badge-create { background: #dcfce7; color: #166534; }
.badge-update { background: #fef9c3; color: #854d0e; }
.badge-delete { background: #fee2e2; color: #991b1b; }
.badge-login { background: #e0f2fe; color: #075985; }
.badge-info { background: #f1f5f9; color: #475569; }

.empty-msg { text-align: center; padding: 3rem; color: #94a3b8; font-style: italic; }

.loader { display: flex; flex-direction: column; align-items: center; padding: 5rem; }
.spinner { width: 40px; height: 40px; border: 3px solid #f1f5f9; border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }

.btn { padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; border: none; align-items: center; gap: 0.5rem; display: inline-flex; transition: all 0.2s; }
.btn-secondary { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
.btn-secondary:hover { background: #e2e8f0; }
.btn-ghost { background: transparent; color: #64748b; }
.btn-ghost:hover { background: #f8fafc; }
</style>
