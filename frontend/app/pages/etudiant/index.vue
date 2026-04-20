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
.dashboard-header { margin-bottom: 2rem; }
.dashboard-header h2 { font-size: 1.75rem; color: var(--text-main); margin-bottom: 0.25rem; font-weight: 700; }
.subtitle { color: var(--text-muted); font-size: 1rem; }

.stats-overview { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 2rem; }
.kpi-card { background: var(--surface); padding: 1.5rem; border-radius: var(--radius); border: 1px solid var(--border); box-shadow: var(--shadow); text-align: center; }
.kpi-card h4 { font-size: 0.95rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; margin-bottom: 0.5rem; }
.kpi-card .value { font-size: 2.2rem; font-weight: 800; color: var(--text-main); }
.kpi-card .value small { font-size: 1rem; color: var(--text-muted); font-weight: 500; margin-left: 0.2rem; }
.value.success { color: var(--success); }
.value.warning { color: var(--warning); }

.widgets { max-width: 600px; }
.widget { background: var(--surface); padding: 1.5rem; border-radius: var(--radius); border: 1px solid var(--border); }
.widget h3 { font-size: 1.2rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }

.grade-list { list-style: none; padding: 0; }
.grade-list li { display: flex; justify-content: space-between; padding: 1rem 0; border-bottom: 1px solid var(--border); }
.grade-list li:last-child { border-bottom: none; }
.ue-info strong { color: var(--text-main); }
.ue-moyenne { font-weight: bold; color: var(--primary); }

.link-btn { display: inline-block; margin-top: 1rem; color: var(--primary); font-weight: 600; text-decoration: none; }
.link-btn:hover { text-decoration: underline; }

@media (max-width: 768px) {
  .stats-overview { grid-template-columns: 1fr; }
}
</style>
