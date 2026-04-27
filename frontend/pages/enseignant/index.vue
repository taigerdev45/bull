<template>
  <div class="dashboard-enseignant">
    <header class="dashboard-header">
      <div class="welcome-badge">Espace Enseignant</div>
      <h1>Tableau de Bord</h1>
      <p class="subtitle">Bienvenue, {{ authName }}. Gérez vos matières et vos évaluations.</p>
    </header>

    <div class="stats-grid">
      <div class="stat-card premium-card">
        <div class="stat-icon modules">📚</div>
        <div class="stat-content">
          <h3>{{ matieres.length }}</h3>
          <p>Matières assignées</p>
        </div>
      </div>
      <div class="stat-card premium-card">
        <div class="stat-icon grades">📝</div>
        <div class="stat-content">
          <h3>{{ ues.length }}</h3>
          <p>Unités d'Enseignement</p>
        </div>
      </div>
      <div class="stat-card premium-card">
        <div class="stat-icon calendar">📅</div>
        <div class="stat-content">
          <h3>S5</h3>
          <p>Semestre Actif</p>
        </div>
      </div>
    </div>

    <!-- Actions Rapides Dynamiques -->
    <div class="actions-panel">
      <div class="panel-header">
        <h3>Vos Matières en cours</h3>
        <p>Cliquez sur une matière pour accéder à la saisie des notes.</p>
      </div>
      
      <div v-if="loading" class="loading-state">
        <div class="loader-p"></div>
        <p>Chargement de vos attributions...</p>
      </div>

      <div v-else-if="matieres.length > 0" class="shortcut-grid">
        <div v-for="m in matieres" :key="m.id" class="shortcut-card premium-card" @click="goToSaisie(m)">
          <div class="card-glow"></div>
          <span class="icon">🔖</span>
          <div class="card-info">
            <h4>{{ m.libelle }}</h4>
            <p>Coefficient : {{ m.coefficient }} | Crédits : {{ m.credits }}</p>
          </div>
          <div class="arrow">→</div>
        </div>
      </div>

      <div v-else class="empty-state-p premium-card">
        <span class="icon">📭</span>
        <p>Aucune matière ne vous est assignée pour le moment.</p>
        <small>Contactez le secrétariat pour vos attributions.</small>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const { fetchApi } = useApi()
const router = useRouter()

useHead({ title: 'Dashboard Enseignant | Bull ASUR' })

const authName = useCookie('authFullName')
const matieres = ref([])
const ues = ref([])
const loading = ref(true)

const loadDashboard = async () => {
  loading.value = true
  try {
    const [mRes, uRes] = await Promise.all([
      fetchApi('/matieres/'),
      fetchApi('/ues/')
    ])
    matieres.value = Array.isArray(mRes) ? mRes : []
    ues.value = Array.isArray(uRes) ? uRes : []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const goToSaisie = (matiere) => {
  // Navigation vers la console de notation avec pré-sélection
  router.push({
    path: '/secretariat/modification-notes',
    query: { matiere_id: matiere.id, ue_id: matiere.ue_id }
  })
}

onMounted(loadDashboard)
</script>

<style scoped>
.dashboard-enseignant { padding: 4rem; max-width: 1400px; margin: 0 auto; animation: fadeIn 0.6s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.welcome-badge { background: #f1f5f9; color: #64748b; padding: 0.4rem 1rem; border-radius: 50px; font-weight: 900; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; display: inline-block; margin-bottom: 1rem; }
.dashboard-header h1 { font-size: 3.5rem; font-weight: 950; letter-spacing: -3px; color: #000; margin-bottom: 0.5rem; }
.subtitle { color: #64748b; font-size: 1.1rem; font-weight: 600; }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; margin: 4rem 0; }
.stat-card { padding: 2rem; display: flex; align-items: center; border-radius: 24px; transition: 0.3s; }
.stat-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.05); }
.stat-icon { width: 64px; height: 64px; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 2rem; margin-right: 1.5rem; }
.stat-icon.modules { background: #ecfdf5; color: #059669; }
.stat-icon.grades { background: #eff6ff; color: #2563eb; }
.stat-icon.calendar { background: #fff7ed; color: #d97706; }
.stat-content h3 { font-size: 1.8rem; font-weight: 950; line-height: 1; }
.stat-content p { color: #94a3b8; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }

.panel-header { margin-bottom: 2rem; }
.panel-header h3 { font-size: 1.5rem; font-weight: 900; letter-spacing: -0.5px; }
.panel-header p { color: #94a3b8; font-weight: 600; }

.shortcut-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; }
.shortcut-card { position: relative; padding: 2rem; display: flex; align-items: center; gap: 1.5rem; cursor: pointer; overflow: hidden; transition: 0.4s cubic-bezier(0.2, 1, 0.3, 1); }
.shortcut-card:hover { background: #000; color: #fff; transform: scale(1.02); }
.shortcut-card:hover .icon { background: rgba(255,255,255,0.1); }
.shortcut-card .icon { width: 50px; height: 50px; background: #f8fafc; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; transition: 0.3s; }
.card-info h4 { font-size: 1.2rem; font-weight: 900; margin-bottom: 0.25rem; }
.card-info p { font-size: 0.75rem; font-weight: 700; opacity: 0.6; text-transform: uppercase; }
.arrow { margin-left: auto; font-size: 1.5rem; font-weight: 100; opacity: 0.3; }

.empty-state-p { padding: 4rem; text-align: center; border: 2px dashed #e2e8f0; background: transparent; color: #94a3b8; }
.empty-state-p .icon { font-size: 3rem; display: block; margin-bottom: 1rem; opacity: 0.2; }
.empty-state-p p { font-weight: 800; color: #64748b; font-size: 1.1rem; }

.loading-state { padding: 4rem; text-align: center; color: #94a3b8; font-weight: 700; }
.loader-p { width: 30px; height: 30px; border: 3px solid #f1f5f9; border-top-color: #000; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 1.5rem; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .dashboard-enseignant { padding: 2rem; }
  .dashboard-header h1 { font-size: 2.5rem; }
  .shortcut-grid { grid-template-columns: 1fr; }
}
</style>
