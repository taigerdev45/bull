<template>
  <div class="audit-page">
    <header class="page-header">
      <div class="title-wrap">
        <span class="badge">Sécurité</span>
        <h1>Journal d'Audit Système</h1>
        <p>Traçabilité complète des actions critiques effectuées sur la plateforme.</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-outline" @click="fetchLogs">
          <span class="icon">🔄</span> Actualiser
        </button>
      </div>
    </header>

    <div class="filters-card shadow-soft">
      <div class="filter-group">
        <label>Recherche</label>
        <input v-model="filters.search" placeholder="Utilisateur, action..." class="input-modern" />
      </div>
      <div class="filter-group">
        <label>Type d'action</label>
        <select v-model="filters.type" class="select-modern">
          <option value="">Tous les types</option>
          <option value="LOGIN">Connexion</option>
          <option value="NOTE_UPDATE">Modif. Notes</option>
          <option value="USER_MGMT">Gestion Utilisateurs</option>
          <option value="DOC_GEN">Génération Documents</option>
        </select>
      </div>
    </div>

    <div class="table-container shadow-soft">
      <div v-if="loading" class="loading-state">
        <div class="loader-p"></div>
        <span>Récupération des journaux de sécurité...</span>
      </div>
      
      <table v-else class="audit-table">
        <thead>
          <tr>
            <th>Horodatage</th>
            <th>Utilisateur</th>
            <th>Action</th>
            <th>Cible</th>
            <th>Détails</th>
            <th>Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in filteredLogs" :key="log.id">
            <td class="td-time">{{ formatTime(log.timestamp) }}</td>
            <td class="td-user">
              <div class="user-pill">{{ log.user_name }}</div>
            </td>
            <td class="td-action">
              <span :class="['action-tag', log.action_type.toLowerCase()]">{{ log.action_type }}</span>
            </td>
            <td>{{ log.target_id || '-' }}</td>
            <td class="td-details">{{ log.details }}</td>
            <td>
              <span class="status-dot success"></span>
              {{ log.status || 'OK' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
const { fetchApi } = useApi()

definePageMeta({ middleware: ['auth', 'admin-only'] })
useHead({ title: 'Journal d\'Audit | Bull ASUR' })

const logs = ref([])
const loading = ref(true)
const filters = ref({ search: '', type: '' })

const fetchLogs = async () => {
  loading.value = true
  try {
    const res = await fetchApi('/audit/logs/')
    logs.value = Array.isArray(res) ? res : []
  } catch (e) {
    console.error("Audit log error:", e)
    logs.value = []
  } finally {
    loading.value = false
  }
}

const filteredLogs = computed(() => {
  return logs.value.filter(l => {
    const matchesSearch = l.user_name.toLowerCase().includes(filters.value.search.toLowerCase()) || 
                          l.details.toLowerCase().includes(filters.value.search.toLowerCase())
    const matchesType = !filters.value.type || l.action_type === filters.value.type
    return matchesSearch && matchesType
  })
})

const formatTime = (ts) => {
  return new Date(ts).toLocaleString('fr-FR', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit'
  })
}

onMounted(fetchLogs)
</script>

<style scoped>
.audit-page { padding: 4rem; max-width: 1600px; margin: 0 auto; animation: fadeIn 0.5s ease-out; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 4rem; }
.badge { background: #fee2e2; color: #dc2626; padding: 0.4rem 1rem; border-radius: 999px; font-weight: 900; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; display: inline-block; margin-bottom: 1rem; }
h1 { font-size: 3rem; font-weight: 950; letter-spacing: -2px; color: #000; line-height: 1; margin-bottom: 0.75rem; }
p { color: #64748b; font-size: 1.1rem; font-weight: 500; }

.filters-card { background: #fff; padding: 1.5rem 2rem; border-radius: 24px; border: 1px solid #f1f5f9; display: flex; gap: 2rem; margin-bottom: 2rem; }
.filter-group { display: flex; flex-direction: column; gap: 0.5rem; flex: 1; }
.filter-group label { font-size: 0.7rem; font-weight: 800; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.5px; }

.input-modern, .select-modern { padding: 0.75rem 1.25rem; border-radius: 12px; border: 1.5px solid #f1f5f9; background: #fafafa; font-weight: 600; font-size: 0.9rem; transition: all 0.2s; outline: none; }
.input-modern:focus, .select-modern:focus { border-color: #000; background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }

.table-container { background: #fff; border-radius: 32px; border: 1px solid #f1f5f9; overflow: hidden; }
.audit-table { width: 100%; border-collapse: collapse; }
.audit-table th { padding: 1.5rem; text-align: left; font-size: 0.7rem; font-weight: 900; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; background: #fafafa; border-bottom: 1px solid #f1f5f9; }
.audit-table td { padding: 1.5rem; border-bottom: 1px solid #f8fafc; font-size: 0.9rem; color: #475569; }
.audit-table tr:last-child td { border-bottom: none; }
.audit-table tr:hover td { background: #fafcff; }

.user-pill { background: #f1f5f9; color: #1e293b; padding: 0.4rem 0.8rem; border-radius: 8px; font-weight: 800; display: inline-block; }
.action-tag { padding: 0.3rem 0.6rem; border-radius: 6px; font-size: 0.7rem; font-weight: 900; }
.action-tag.login { background: #f0fdf4; color: #166534; }
.action-tag.note_update { background: #fef2f2; color: #991b1b; }
.action-tag.doc_gen { background: #eff6ff; color: #1e40af; }

.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 0.5rem; }
.status-dot.success { background: #16a34a; box-shadow: 0 0 8px #16a34a; }

.loading-state { padding: 8rem; text-align: center; color: #64748b; }
.loader-p { width: 30px; height: 30px; border: 3px solid #f1f5f9; border-top-color: #000; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 1.5rem; }
@keyframes spin { to { transform: rotate(360deg); } }

.btn { padding: 0.8rem 1.5rem; border-radius: 12px; font-weight: 800; cursor: pointer; border: none; transition: all 0.2s; }
.btn-outline { background: #fff; color: #000; border: 1.5px solid #e2e8f0; }
.btn-outline:hover { border-color: #000; background: #fafafa; }
</style>
