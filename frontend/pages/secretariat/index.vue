<template>
  <div class="dashboard-container">
    <div class="welcome-banner">
      <div class="welcome-text">
        <h1>Espace Secrétariat 👋</h1>
        <p>Gestion administrative et suivi des résultats ASUR.</p>
      </div>
      <div class="current-semestre-badge">
        <span>Session Actuelle :</span>
        <strong>2025-2026</strong>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card-p">
        <div class="s-icon">🎓</div>
        <div class="s-info">
          <span class="s-label">Étudiants</span>
          <span class="s-value">{{ studentCount }}</span>
        </div>
      </div>
      <div class="stat-card-p">
        <div class="s-icon">🕒</div>
        <div class="s-info">
          <span class="s-label">Absences (S5)</span>
          <span class="s-value">{{ totalAbsences }}h</span>
        </div>
      </div>
      <div class="stat-card-p">
        <div class="s-icon">👨‍🏫</div>
        <div class="s-info">
          <span class="s-label">Corps Enseignant</span>
          <span class="s-value">{{ teacherCount }}</span>
        </div>
      </div>
      <div class="stat-card-p">
        <div class="s-icon">📄</div>
        <div class="s-info">
          <span class="s-label">PVs Générés</span>
          <span class="s-value">12</span>
        </div>
      </div>
    </div>

    <div class="main-grid">
      <div class="card activity-card">
        <div class="card-header">
          <h3>Dernières Évaluations</h3>
          <NuxtLink to="/saisie" class="btn-text">Gérer les notes</NuxtLink>
        </div>
        <div class="card-body">
          <div v-for="i in 4" :key="i" class="list-item">
            <div class="status-dot"></div>
            <div class="list-content">
              <p>Mise à jour des notes : <strong>Programmation Java</strong></p>
              <span>Il y a 2 heures</span>
            </div>
          </div>
        </div>
      </div>

      <div class="card help-card">
        <div class="card-header">
          <h3>Guide Secrétariat</h3>
        </div>
        <div class="card-body">
          <ul class="guide-list">
            <li>
              <strong>Étape 1 :</strong> Vérifiez la liste des <NuxtLink to="/etudiants">étudiants</NuxtLink>.
            </li>
            <li>
              <strong>Étape 2 :</strong> Saisissez les <NuxtLink to="/secretariat/absences">absences</NuxtLink> hebdomadaires.
            </li>
            <li>
              <strong>Étape 3 :</strong> Préparez le <NuxtLink to="/deliberations">Jury</NuxtLink> en fin de semestre.
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

useHead({ title: 'Secrétariat | Bull ASUR' })

const { fetchApi } = useApi()
const studentCount = ref('--')
const teacherCount = ref('--')
const totalAbsences = ref('--')

onMounted(async () => {
  try {
    const [ets, tchs, abs] = await Promise.allSettled([
      fetchApi('/etudiants/'),
      fetchApi('/enseignants/'),
      fetchApi('/absences/')
    ])
    
    if (ets.status === 'fulfilled') studentCount.value = ets.value.length
    if (tchs.status === 'fulfilled') teacherCount.value = tchs.value.length
    if (abs.status === 'fulfilled') {
      totalAbsences.value = abs.value.reduce((acc, curr) => acc + (curr.nombre_heures || 0), 0)
    }
  } catch (e) {}
})
</script>

<style scoped>
.dashboard-container { display: flex; flex-direction: column; gap: 2rem; }

.welcome-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #000046, #1cb5e0);
  padding: 2.5rem;
  border-radius: var(--radius-xl);
  color: white;
  box-shadow: var(--shadow-lg);
}

.welcome-text h1 { font-size: 2rem; font-weight: 800; margin: 0; }
.welcome-text p { opacity: 0.9; font-size: 1.1rem; margin-top: 0.5rem; }

.current-semestre-badge {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(8px);
  padding: 0.75rem 1.5rem;
  border-radius: 999px;
  display: flex; gap: 0.5rem; align-items: center;
  border: 1px solid rgba(255,255,255,0.2);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.stat-card-p {
  background: white;
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  gap: 1.25rem;
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
}

.s-icon { font-size: 2rem; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; background: #f8fafc; border-radius: 12px; }
.s-info { display: flex; flex-direction: column; }
.s-label { font-size: 0.8rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
.s-value { font-size: 1.5rem; font-weight: 800; color: #1e293b; }

.main-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; }

.card { background: white; border-radius: var(--radius-lg); border: 1px solid var(--border-light); }
.card-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid var(--border-light); display: flex; justify-content: space-between; align-items: center; }
.card-header h3 { font-size: 1.1rem; font-weight: 700; margin: 0; }
.card-body { padding: 1.5rem; }

.list-item { display: flex; gap: 1rem; padding-bottom: 1rem; margin-bottom: 1rem; border-bottom: 1px dashed #f1f5f9; }
.status-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; margin-top: 6px; }
.list-content p { font-size: 0.9rem; margin: 0; }
.list-content span { font-size: 0.75rem; color: #94a3b8; }

.guide-list { list-style: none; padding: 0; margin: 0; }
.guide-list li { margin-bottom: 1.25rem; font-size: 0.95rem; color: #475569; position: relative; padding-left: 1.5rem; }
.guide-list li::before { content: "→"; position: absolute; left: 0; color: var(--primary); font-weight: 900; }
.guide-list a { color: var(--primary); text-decoration: none; font-weight: 600; }

.btn-text { color: var(--primary); font-weight: 600; text-decoration: none; font-size: 0.9rem; }

@media (max-width: 1024px) { .main-grid { grid-template-columns: 1fr; } }
</style>
