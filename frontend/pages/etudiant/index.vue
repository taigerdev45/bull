<template>
  <div class="dashboard-etudiant">
    <header class="dashboard-header">
      <h2>Espace Étudiant</h2>
      <p class="subtitle" v-if="!isLoading">Consultez vos performances scolaires pour le Semestre {{ studentResults?.semestre || 5 }}.</p>
      <p class="subtitle" v-else>Chargement de vos résultats...</p>
    </header>

    <div v-if="isLoading" class="loading-state">
       Chargement des données en cours...
    </div>

    <div v-else-if="studentResults" class="dashboard-content">
      <div class="stats-overview">
        <div class="kpi-card">
          <h4>Moyenne S{{ studentResults.semestre || 5 }}</h4>
          <div class="value" :class="{ success: studentResults.moyenne_generale >= 10 }">
            {{ studentResults.moyenne_generale }}<small>/20</small>
          </div>
        </div>
        <div class="kpi-card">
          <h4>Crédits</h4>
          <div class="value">
            {{ studentResults.credits_acquis }}<small>/{{ studentResults.total_credits || 30 }}</small>
          </div>
        </div>
        <div class="kpi-card">
          <h4>Absences</h4>
          <div class="value warning">{{ absencesCount }}<small>heures</small></div>
        </div>
      </div>

      <div class="widgets">
        <div class="widget">
          <h3>Mes Unités d'Enseignement (UE)</h3>
          <ul class="grade-list">
            <li v-for="ue in studentResults.ues" :key="ue.id">
              <div class="ue-info">
                <strong>{{ ue.id }} : {{ ue.libelle }}</strong>
              </div>
              <div class="ue-moyenne">{{ ue.moyenne_ue.toFixed(2) }} / 20</div>
            </li>
          </ul>
          <NuxtLink to="/bulletins" class="link-btn">Voir mon bulletin détaillé →</NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useApi } from '~/composables/useApi'

useHead({ title: 'Espace Étudiant | Bull ASUR' })

const { apiFetch } = useApi()
const isLoading = ref(true)
const studentResults = ref(null)

// En démo, on simule l'ID de l'étudiant connecté
const studentId = 'TEST2026001' 

const fetchResults = async () => {
  try {
    isLoading.value = true
    // Appel réel vers l'API selon la nouvelle doc
    const response = await apiFetch(`/api/resultats/semestre/${studentId}/`, {
      params: { semestre: 5 }
    })
    studentResults.value = response
  } catch (error) {
    console.error('Failed to fetch student results:', error)
    // Fallback pour la démo si l'API n'est pas encore live
    studentResults.value = {
      moyenne_generale: 12.45,
      credits_acquis: 30,
      total_credits: 30,
      ues: [
        { id: 'UE5-1', libelle: 'Enseignement Général', moyenne_ue: 11.50 },
        { id: 'UE5-2', libelle: 'Connaissances LAN', moyenne_ue: 13.20 }
      ]
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchResults()
})

const absencesCount = ref(4) // Mock pour l'instant
</script>

<style scoped>
.dashboard-header { margin-bottom: 2rem; padding: 2rem; background: var(--bg-sidebar); border-radius: var(--radius-lg); color: white; }
.dashboard-header h2 { font-size: 2rem; color: white; margin-bottom: 0.5rem; font-weight: 800; }
.subtitle { color: rgba(255,255,255,0.6); font-size: 1rem; }

.stats-overview { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 2.5rem; }
.kpi-card { background: white; padding: 2rem; border-radius: var(--radius-lg); border: 1px solid var(--border-light); text-align: center; box-shadow: var(--shadow-sm); }
.kpi-card h4 { font-size: 0.85rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase; margin-bottom: 1rem; letter-spacing: 0.5px; }
.kpi-card .value { font-size: 2.5rem; font-weight: 800; color: black; }
.kpi-card .value small { font-size: 1rem; color: var(--text-muted); font-weight: 500; margin-left: 0.4rem; }

.value.success { border-bottom: 4px solid black; }
.value.warning { border-bottom: 4px solid #666; }

.widgets { width: 100%; display: grid; grid-template-columns: 1fr; gap: 2rem; }
.widget { background: white; padding: 2rem; border-radius: var(--radius-lg); border: 1px solid var(--border-light); }
.widget h3 { font-size: 1.3rem; margin-bottom: 1.5rem; font-weight: 700; border-bottom: 1px solid #f1f1f1; padding-bottom: 1rem; }

.grade-list { list-style: none; padding: 0; }
.grade-list li { display: flex; justify-content: space-between; padding: 1.25rem 0; border-bottom: 1px solid #f9f9f9; }
.grade-list li:last-child { border-bottom: none; }
.ue-info strong { color: black; font-weight: 600; }
.ue-moyenne { font-weight: 800; color: black; }

.link-btn { display: inline-block; margin-top: 1.5rem; color: black; font-weight: 700; text-decoration: underline; text-underline-offset: 4px; }
.link-btn:hover { opacity: 0.7; }

@media (max-width: 768px) {
  .stats-overview { grid-template-columns: 1fr; }
}
</style>
