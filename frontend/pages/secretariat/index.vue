<template>
  <div class="dashboard-secretariat">
    <div class="welcome-header premium-card darker">
      <div class="welcome-inner">
        <div class="main-info">
          <h1>Espace Secrétariat</h1>
          <p>Supervision académique et archivage des dossiers étudiants.</p>
        </div>
        <div class="session-info">
          <span class="label">Période Académique</span>
          <span class="value">2025 - 2026</span>
        </div>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card premium-card">
        <div class="s-head">
          <span class="icon">👥</span>
          <h3>Effectif Global</h3>
        </div>
        <div class="s-body">
          <span class="value">{{ studentCount }}</span>
          <span class="meta">Étudiants Inscrits</span>
        </div>
      </div>
      <div class="stat-card premium-card">
        <div class="s-head">
          <span class="icon">⌛</span>
          <h3>Heures d'Abscences</h3>
        </div>
        <div class="s-body">
          <span class="value text-black">{{ totalAbsences }}H</span>
          <span class="meta">Total Cumulé S5</span>
        </div>
      </div>
      <div class="stat-card premium-card">
        <div class="s-head">
          <span class="icon">👨‍🏫</span>
          <h3>Intervenants</h3>
        </div>
        <div class="s-body">
          <span class="value">{{ teacherCount }}</span>
          <span class="meta">Corps Enseignant</span>
        </div>
      </div>
      <div class="stat-card premium-card">
        <div class="s-head">
          <span class="icon">📄</span>
          <h3>Documents</h3>
        </div>
        <div class="s-body">
          <span class="value">142</span>
          <span class="meta">PV & Bulletins (S5)</span>
        </div>
      </div>
    </div>

    <div class="main-grid-layout">
      <!-- Activités Récentes -->
      <div class="activity-section premium-card">
        <div class="section-header">
          <h3>Flux d'activités</h3>
          <NuxtLink to="/secretariat/bulletins" class="btn-link">Editer les bulletins →</NuxtLink>
        </div>
        <div class="section-body">
          <div v-for="i in 5" :key="i" class="activity-item">
            <span class="timestamp">12:4{{ i }}</span>
            <div class="msg">
              <p>Mise à jour des notes : <strong>Unité {{ i+102 }} - Java</strong></p>
              <span class="author">Effectué par : Admin Académique</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Guide -->
      <div class="guide-section premium-card">
        <h3>Protocoles Administratifs</h3>
        <ul class="protocol-list">
          <li>
            <div class="num">01</div>
            <div class="text">
              <strong>Vérification des Inscriptions</strong>
              <p>Contrôlez les matricules sur le <NuxtLink to="/secretariat/etudiants">Registre</NuxtLink>.</p>
            </div>
          </li>
          <li>
            <div class="num">02</div>
            <div class="text">
              <strong>Journal des Absences</strong>
              <p>Saisissez les rapports hebdomadaires <NuxtLink to="/secretariat/absences">ici</NuxtLink>.</p>
            </div>
          </li>
          <li>
            <div class="num">03</div>
            <div class="text">
              <strong>Délibérations Finales</strong>
              <p>Préparez les <NuxtLink to="/secretariat/bulletins">Jury de fin de cycle</NuxtLink>.</p>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

useHead({ title: 'Dashboard Secrétariat | Bull ASUR' })

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
.dashboard-secretariat { padding: clamp(1.5rem, 4vw, 4rem) 2rem; max-width: 1500px; margin: 0 auto; animation: slideUp 0.6s ease-out; }

@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.welcome-header { padding: 4rem; margin-bottom: 3rem; position: relative; overflow: hidden; border-radius: 32px; background: #000; color: #fff; }
.welcome-header.darker { background: linear-gradient(135deg, #000 0%, #1a1a1a 100%); }

.welcome-inner { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 2rem; position: relative; z-index: 2; }
.main-info h1 { font-size: clamp(2rem, 5vw, 3rem); font-weight: 900; letter-spacing: -2px; margin-bottom: 0.5rem; line-height: 1; }
.main-info p { opacity: 0.7; font-size: 1.1rem; font-weight: 500; }

.session-info { background: rgba(255,255,255,0.1); padding: 1.25rem 2.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.15); }
.session-info .label { font-size: 0.75rem; font-weight: 800; text-transform: uppercase; color: rgba(255,255,255,0.5); display: block; margin-bottom: 0.25rem; }
.session-info .value { font-size: 1.25rem; font-weight: 900; }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 2rem; margin-bottom: 5rem; }
.stat-card { padding: 3rem 2rem; background: #fff; }
.s-head { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem; }
.s-head .icon { font-size: 1.5rem; }
.s-head h3 { font-size: 0.75rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px; }

.s-body .value { font-size: 1.6rem; font-weight: 900; letter-spacing: -1px; line-height: 1; display: block; margin-bottom: 0.5rem; color: #000; }
.s-body .meta { font-size: 0.8rem; font-weight: 800; color: #64748b; text-transform: uppercase; }

.main-grid-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; }

.activity-section { padding: 3rem; background: #fff; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 3rem; }
.section-header h3 { font-size: 1.4rem; font-weight: 900; letter-spacing: -0.5px; }
.btn-link { font-size: 0.85rem; font-weight: 800; color: #000; text-decoration: none; border-bottom: 2px solid #000; }

.activity-item { display: flex; gap: 2rem; margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid #f1f5f9; }
.activity-item .timestamp { font-weight: 800; font-size: 0.85rem; color: #94a3b8; font-family: monospace; }
.activity-item .msg p { font-size: 0.95rem; margin-bottom: 0.25rem; }
.activity-item .msg p strong { color: #000; }
.activity-item .msg .author { font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; }

.guide-section { padding: 3rem; background: #fafafa; border: none; }
.guide-section h3 { font-size: 1.25rem; font-weight: 900; margin-bottom: 2.5rem; }

.protocol-list { list-style: none; padding: 0; }
.protocol-list li { display: flex; gap: 1.5rem; margin-bottom: 2.5rem; align-items: flex-start; }
.protocol-list .num { width: 36px; height: 36px; background: #000; color: #fff; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 900; flex-shrink: 0; }
.protocol-list .text strong { display: block; font-size: 0.95rem; font-weight: 800; margin-bottom: 0.25rem; }
.protocol-list .text p { font-size: 0.85rem; color: #64748b; font-weight: 500; }
.protocol-list a { color: #000; font-weight: 900; text-decoration: underline; }

@media (max-width: 1024px) {
  .main-grid-layout { grid-template-columns: 1fr; }
}
</style>
