<template>
  <div class="dashboard-etudiant">
    <header class="dashboard-header">
      <div class="header-main">
        <div class="welcome-badge">Espace Personnel</div>
        <h2>Salut {{ userName || 'Étudiant' }} !</h2>
        <p class="subtitle">Aperçu rapide de votre progression académique au Semestre 5.</p>
      </div>
    </header>

    <div v-if="isLoading" class="loading-state">
       <div class="loader-p"></div>
       <p>Synchronisation de votre dossier...</p>
    </div>

    <div v-else-if="studentResults" class="dashboard-content">
      <div class="stats-overview">
        <div class="kpi-card shadow-soft">
          <div class="kpi-head">
            <span class="kpi-label">Moyenne S5</span>
            <span class="kpi-icon">📈</span>
          </div>
          <div class="value" :class="{ success: studentResults.moyenne_generale >= 10 }">
            {{ studentResults.moyenne_generale }}<small>/20</small>
          </div>
        </div>

        <div class="kpi-card shadow-soft">
          <div class="kpi-head">
            <span class="kpi-label">Crédits</span>
            <span class="kpi-icon">🛡️</span>
          </div>
          <div class="value">
            {{ studentResults.credits_acquis }}<small>/30</small>
          </div>
        </div>

        <div class="kpi-card shadow-soft warning">
          <div class="kpi-head">
            <span class="kpi-label">Absences</span>
            <span class="kpi-icon">⏰</span>
          </div>
          <div class="value">{{ absencesCount }}<small>h</small></div>
        </div>
      </div>

      <div class="widgets-grid">
        <div class="premium-card main-widget shadow-soft">
          <div class="widget-header">
            <h3>Dernières Notes par UE</h3>
            <NuxtLink to="/bulletins" class="btn-text">Détail complet →</NuxtLink>
          </div>
          <ul class="ue-mini-list">
            <li v-for="ue in studentResults.ues" :key="ue.id">
              <div class="ue-meta">
                <span class="ue-code">{{ ue.id }}</span>
                <span class="ue-name">{{ ue.libelle }}</span>
              </div>
              <div class="ue-score" :class="{ 'low': ue.moyenne_ue < 10 }">
                {{ ue.moyenne_ue.toFixed(2) }}
              </div>
            </li>
          </ul>
        </div>

        <div class="side-widgets">
          <div class="premium-card dark-card">
            <h4>Statut Administratif</h4>
            <div class="status-box">
              <span class="status-dot"></span>
              En règle (Scolarité)
            </div>
            <p class="small-info">Votre dossier est à jour pour la session normale des examens.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

useHead({ title: 'Dashboard Étudiant | Bull ASUR' })

const { fetchApi } = useApi()
const isLoading = ref(true)
const studentResults = ref(null)
const userName = useCookie('authFullName')
const absencesCount = ref(6)

const fetchResults = async () => {
  try {
    isLoading.value = true
    const authId = useCookie('authId').value || 'TEST'
    const response = await fetchApi(`/resultats/semestre/${authId}/`)
    studentResults.value = response
  } catch (error) {
    console.error('Failed to fetch:', error)
    // Mock
    studentResults.value = {
      moyenne_generale: 12.85,
      credits_acquis: 26,
      ues: [
        { id: 'UE5-1', libelle: 'Enseignement Général', moyenne_ue: 11.50 },
        { id: 'UE5-2', libelle: 'Connaissances LAN', moyenne_ue: 14.20 },
        { id: 'UE5-3', libelle: 'Sécurité Réseaux', moyenne_ue: 12.10 }
      ]
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchResults)
</script>

<style scoped>
.dashboard-etudiant { padding: 4rem; max-width: 1400px; margin: 0 auto; animation: fadeIn 0.6s ease-out; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.dashboard-header { margin-bottom: 4rem; }
.welcome-badge { display: inline-block; padding: 0.5rem 1rem; background: #000; color: #fff; border-radius: 8px; font-weight: 900; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 1.5rem; }
.dashboard-header h2 { font-size: clamp(2.5rem, 5vw, 3.5rem); font-weight: 950; letter-spacing: -2px; line-height: 1; margin-bottom: 0.75rem; color: #000; }
.subtitle { color: #64748b; font-weight: 600; font-size: 1.1rem; }

.stats-overview { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-bottom: 4rem; }
.kpi-card { background: white; padding: 2.5rem; border-radius: 28px; position: relative; border: 1px solid #f1f5f9; }
.kpi-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.kpi-label { font-size: 0.75rem; font-weight: 900; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; }
.kpi-card .value { font-size: 3rem; font-weight: 950; color: #000; letter-spacing: -1.5px; line-height: 1; }
.kpi-card .value small { font-size: 1rem; color: #94a3b8; margin-left: 0.5rem; }
.kpi-card.warning .value { color: #ef4444; }

.widgets-grid { display: grid; grid-template-columns: 1fr 380px; gap: 3rem; }
.main-widget { background: #fff; padding: 3rem; border-radius: 32px; border: 1px solid #f1f5f9; }
.widget-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2.5rem; }
.widget-header h3 { font-size: 1.4rem; font-weight: 950; letter-spacing: -1px; }
.btn-text { font-weight: 900; color: #000; text-decoration: none; font-size: 0.85rem; border-bottom: 2px solid #000; padding-bottom: 2px; }

.ue-mini-list { list-style: none; padding: 0; }
.ue-mini-list li { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 0; border-bottom: 1px solid #f1f5f9; }
.ue-mini-list li:last-child { border-bottom: none; }
.ue-meta { display: flex; align-items: center; gap: 1.5rem; }
.ue-code { background: #f1f5f9; color: #64748b; padding: 0.4rem 0.8rem; border-radius: 8px; font-weight: 900; font-size: 0.7rem; }
.ue-name { font-weight: 800; color: #000; font-size: 1rem; }
.ue-score { font-size: 1.5rem; font-weight: 950; color: #000; }
.ue-score.low { color: #ef4444; }

.dark-card { background: #000; color: #fff; padding: 3rem; border-radius: 32px; border: none; }
.dark-card h4 { font-size: 1.2rem; font-weight: 950; margin-bottom: 1.5rem; }
.status-box { display: inline-flex; align-items: center; gap: 0.75rem; background: rgba(255,255,255,0.1); padding: 0.75rem 1.25rem; border-radius: 12px; font-weight: 800; font-size: 0.9rem; margin-bottom: 1.5rem; }
.status-dot { width: 10px; height: 10px; background: #16a34a; border-radius: 50%; box-shadow: 0 0 10px #16a34a; }
.small-info { font-size: 0.8rem; opacity: 0.5; font-weight: 600; line-height: 1.5; }

.loader-p { width: 30px; height: 30px; border: 3px solid #f1f5f9; border-top-color: #000; border-radius: 50%; animation: spin 0.8s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.loading-state { padding: 8rem; text-align: center; }

@media (max-width: 1100px) {
  .widgets-grid { grid-template-columns: 1fr; }
  .dashboard-header { padding: 0; }
  .dashboard-etudiant { padding: 2rem; }
}
</style>
