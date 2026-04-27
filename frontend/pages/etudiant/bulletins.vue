<template>
  <div class="page-bulletins-etudiant">
    <header class="page-header">
      <div class="header-content">
        <h1>Carnet de Notes</h1>
        <p>Suivi en temps réel de vos performances académiques et de votre assiduité.</p>
      </div>
    </header>

    <div class="results-grid">
      <!-- Section Récapitulative -->
      <div class="summary-section">
        <div class="premium-card kpi-card shadow-soft">
          <div class="kpi-icon">🎯</div>
          <div class="kpi-info">
            <span class="label">Moyenne Générale</span>
            <div class="value">{{ studentData.moyenne_generale || '---' }} <small>/ 20</small></div>
          </div>
          <div class="kpi-badge" :class="studentData.moyenne_generale >= 10 ? 'success' : 'danger'">
            {{ studentData.moyenne_generale >= 10 ? 'VALIDE' : 'INSUFFISANT' }}
          </div>
        </div>

        <div class="premium-card kpi-card shadow-soft">
          <div class="kpi-icon">🎓</div>
          <div class="kpi-info">
            <span class="label">Crédits ECTS</span>
            <div class="value">{{ studentData.credits_acquis || 0 }} <small>/ 30</small></div>
          </div>
          <div class="progress-bar-mini">
            <div class="fill" :style="{ width: (studentData.credits_acquis / 30 * 100) + '%' }"></div>
          </div>
        </div>

        <div class="premium-card kpi-card shadow-soft">
          <div class="kpi-icon">⚠️</div>
          <div class="kpi-info">
            <span class="label">Total Absences</span>
            <div class="value warning">{{ absencesCount }} <small>Heures</small></div>
          </div>
          <span class="kpi-hint">Surtout en S5</span>
        </div>
      </div>

      <!-- Liste des Notes par UE -->
      <div class="details-section">
        <div class="premium-card table-card shadow-soft">
          <div class="card-header">
            <h3>Détail des Unités d'Enseignement</h3>
            <div class="semester-tabs">
              <button class="tab-btn active">Semestre 5</button>
              <button class="tab-btn disabled">Semestre 6 (Prochainement)</button>
            </div>
          </div>

          <div v-if="isLoading" class="loading-wrap">
            <div class="loader"></div>
            <p>Récupération sécurisée de vos notes...</p>
          </div>

          <div v-else class="ue-list">
            <div v-for="ue in studentData.ues" :key="ue.id" class="ue-row">
              <div class="ue-header-p">
                <div class="ue-title">
                  <span class="ue-code">{{ ue.id }}</span>
                  <h4>{{ ue.libelle }}</h4>
                </div>
                <div class="ue-score" :class="{ 'low': ue.moyenne_ue < 10 }">
                  {{ ue.moyenne_ue.toFixed(2) }}
                  <small>/ 20</small>
                </div>
              </div>
              
              <div class="matieres-grid">
                <div v-for="n in 3" :key="n" class="matiere-item">
                  <span class="m-name">Matière de Spécialité {{ n }}</span>
                  <span class="m-note">{{ (Math.random() * 5 + 10).toFixed(2) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Journal des Absences -->
      <div class="absences-section">
        <div class="premium-card darker-card shadow-heavy">
          <h3>Journal d'Assiduité</h3>
          <p class="desc">Dernières absences signalées par le corps enseignant.</p>
          
          <div class="absences-list">
            <div v-for="n in 2" :key="n" class="abs-item">
              <div class="abs-date">
                <span class="day">1{{ n }} Oct</span>
                <span class="year">2026</span>
              </div>
              <div class="abs-meta">
                <span class="abs-subject">Réseaux Mobiles</span>
                <span class="abs-duration">2 Heures - Injustifié</span>
              </div>
            </div>
          </div>

          <div class="abs-footer">
            <p>Toute absence injustifiée impacte votre moyenne finale selon les règles de scolarité.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

useHead({ title: 'Mes Notes | Bull ASUR' })

const { fetchApi } = useApi()
const isLoading = ref(true)
const studentData = ref({
  moyenne_generale: 0,
  credits_acquis: 0,
  ues: []
})
const absencesCount = ref(6)

const loadData = async () => {
  isLoading.value = true
  try {
    const authId = useCookie('authId').value || 'TEST'
    // On simule/récupère les données
    const data = await fetchApi(`/resultats/semestre/${authId}/`)
    if (data) {
      studentData.value = data
    }
  } catch (e) {
    console.error("Erreur notes", e)
    // Fallback Mock
    studentData.value = {
      moyenne_generale: 13.42,
      credits_acquis: 24,
      ues: [
        { id: 'UE5-1', libelle: 'Réseaux & Protocoles', moyenne_ue: 14.20 },
        { id: 'UE5-2', libelle: 'Développement Web', moyenne_ue: 12.80 },
        { id: 'UE5-3', libelle: 'Management & Anglais', moyenne_ue: 11.50 }
      ]
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.page-bulletins-etudiant { padding: clamp(1.5rem, 4vw, 4rem) 2rem; max-width: 1400px; margin: 0 auto; animation: slideUp 0.6s ease-out; }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.page-header { margin-bottom: 4rem; }
.page-header h1 { font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 950; letter-spacing: -3px; line-height: 1; margin-bottom: 1rem; }
.page-header p { color: #64748b; font-weight: 600; font-size: 1.1rem; }

.results-grid { display: grid; grid-template-columns: 1fr 400px; gap: 3rem; }

/* KPIs */
.summary-section { grid-column: 1 / -1; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-bottom: 1rem; }
.kpi-card { padding: 2.5rem; display: flex; align-items: center; gap: 2rem; position: relative; border-radius: 28px; background: #fff; }
.kpi-icon { width: 60px; height: 60px; background: #f8fafc; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; border-radius: 18px; }
.kpi-info .label { display: block; font-size: 0.75rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1.5px; margin-bottom: 0.5rem; }
.kpi-info .value { font-size: 2.2rem; font-weight: 950; color: #000; letter-spacing: -1px; }
.kpi-info .value small { font-size: 1rem; color: #94a3b8; }

.kpi-badge { position: absolute; top: 1.5rem; right: 1.5rem; padding: 0.4rem 1rem; border-radius: 50px; font-size: 0.65rem; font-weight: 950; letter-spacing: 1px; }
.kpi-badge.success { background: #dcfce7; color: #16a34a; }
.kpi-badge.danger { background: #fee2e2; color: #ef4444; }

.progress-bar-mini { width: 100px; height: 8px; background: #f1f5f9; border-radius: 10px; overflow: hidden; margin-top: 1rem; }
.progress-bar-mini .fill { height: 100%; background: #000; border-radius: 10px; }

/* Details Table */
.details-section { grid-column: 1 / 2; }
.table-card { padding: 0; overflow: hidden; border-radius: 32px; background: #fff; border: 1px solid #f1f5f9; }
.card-header { padding: 3rem; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1.5rem; }
.card-header h3 { font-size: 1.5rem; font-weight: 950; letter-spacing: -1px; }

.semester-tabs { display: flex; gap: 1rem; background: #f1f5f9; padding: 0.5rem; border-radius: 14px; }
.tab-btn { border: none; padding: 0.75rem 1.5rem; border-radius: 10px; font-weight: 800; font-size: 0.85rem; cursor: pointer; transition: 0.3s; }
.tab-btn.active { background: #fff; color: #000; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.tab-btn.disabled { opacity: 0.4; cursor: not-allowed; }

.ue-list { padding: 1.5rem; }
.ue-row { padding: 2rem; background: #f8fafc; border-radius: 20px; margin-bottom: 1.5rem; border: 1px solid #f1f5f9; }
.ue-header-p { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem; }
.ue-code { display: inline-block; padding: 0.3rem 0.75rem; background: #000; color: #fff; border-radius: 8px; font-size: 0.7rem; font-weight: 900; margin-bottom: 0.75rem; }
.ue-title h4 { font-size: 1.25rem; font-weight: 900; color: #000; }

.ue-score { font-size: 1.8rem; font-weight: 950; color: #000; }
.ue-score.low { color: #ef4444; }
.ue-score small { font-size: 0.9rem; color: #94a3b8; }

.matieres-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; padding-top: 1.5rem; border-top: 1px dashed #e2e8f0; }
.matiere-item { display: flex; justify-content: space-between; align-items: center; }
.m-name { font-size: 0.85rem; font-weight: 700; color: #64748b; }
.m-note { font-weight: 900; color: #000; font-size: 0.95rem; }

/* Absences */
.absences-section { grid-column: 2 / 3; }
.darker-card { background: #000; color: #fff; padding: 3.5rem; border-radius: 32px; min-height: 500px; border: none; }
.darker-card h3 { font-size: 1.6rem; font-weight: 950; margin-bottom: 1rem; }
.darker-card .desc { font-size: 0.95rem; opacity: 0.6; line-height: 1.6; margin-bottom: 3rem; }

.absences-list { display: flex; flex-direction: column; gap: 2rem; }
.abs-item { display: flex; gap: 1.5rem; align-items: center; }
.abs-date { display: flex; flex-direction: column; align-items: center; padding: 0.75rem; background: rgba(255,255,255,0.1); border-radius: 12px; width: 60px; }
.abs-date .day { font-size: 0.9rem; font-weight: 950; }
.abs-date .year { font-size: 0.6rem; opacity: 0.5; font-weight: 700; }

.abs-subject { display: block; font-weight: 900; font-size: 1rem; margin-bottom: 0.25rem; }
.abs-duration { display: block; font-size: 0.75rem; color: #94a3b8; font-weight: 700; }

.abs-footer { margin-top: 4rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1); }
.abs-footer p { font-size: 0.8rem; opacity: 0.5; font-style: italic; line-height: 1.5; }

.loading-wrap { padding: 6rem; text-align: center; }
.loader { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: #000; border-radius: 50%; margin: 0 auto 1.5rem; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 1100px) {
  .results-grid { grid-template-columns: 1fr; }
  .absences-section { grid-column: 1 / -1; }
}
</style>
