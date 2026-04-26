<template>
  <div class="dashboard-container">
    <div class="welcome-banner">
      <div class="welcome-text">
        <h1>Bon retour, Administrateur 👋</h1>
        <p>Voici un aperçu de l'activité globale de Bull ASUR.</p>
      </div>
      <div class="current-semestre-badge">
        <span>Semestre Actif :</span>
        <strong>S5</strong>
      </div>
    </div>

    <div class="stats-grid">
      <StatCard label="Étudiants Inscrits" value="128" :trend="12" color="#2563eb">
        <template #icon>👨‍🎓</template>
      </StatCard>
      <StatCard label="Matières Actives" value="16" :trend="0" color="#7c3aed">
        <template #icon>📖</template>
      </StatCard>
      <StatCard label="Notes Saisies" value="1,240" :trend="8" color="#10b981">
        <template #icon>📝</template>
      </StatCard>
      <StatCard label="Taux Absences" value="2.4%" :trend="-5" color="#ef4444">
        <template #icon>⚠️</template>
      </StatCard>
    </div>

    <div class="main-grid">
      <!-- Activity Feed -->
      <div class="card activity-card">
        <div class="card-header">
          <h3>Activités Récentes</h3>
          <button class="btn-text">Voir tout</button>
        </div>
        <div class="card-body">
          <div v-for="i in 5" :key="i" class="activity-item">
            <div class="activity-dot"></div>
            <div class="activity-content">
              <p><strong>Note ajoutée</strong> en Algorithmique par Mr. Dupont</p>
              <span>Il y a 10 minutes</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card actions-card">
        <div class="card-header">
          <h3>Actions Rapides</h3>
        </div>
        <div class="card-body">
          <div class="action-buttons">
            <NuxtLink to="/etudiants" class="action-btn-p">
              <span class="a-icon">➕</span>
              Inscrire Étudiant
            </NuxtLink>
            <NuxtLink to="/referentiels" class="action-btn-p">
              <span class="a-icon">🔍</span>
              Manager UEs
            </NuxtLink>
            <NuxtLink to="/admin/logs" class="action-btn-p">
              <span class="a-icon">📑</span>
              Consultation Logs
            </NuxtLink>
            <NuxtLink to="/profil" class="action-btn-p">
              <span class="a-icon">⚙️</span>
              Configuration profil
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import StatCard from '~/components/ui/StatCard.vue'
useHead({ title: 'Dashboard | Bull ASUR' })
</script>

<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.welcome-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #1e3a8a, #3b82f6);
  padding: 2.5rem;
  border-radius: var(--radius-xl);
  color: white;
  box-shadow: var(--shadow-lg);
}

.welcome-text h1 { font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem; }
.welcome-text p { opacity: 0.8; font-size: 1.1rem; }

.current-semestre-badge {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(8px);
  padding: 0.75rem 1.5rem;
  border-radius: 999px;
  display: flex;
  gap: 0.5rem;
  align-items: center;
  border: 1px solid rgba(255,255,255,0.2);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
}

.main-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

.card {
  background: white;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
}

.card-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 { font-size: 1.1rem; font-weight: 700; }

.card-body { padding: 1.5rem; }

.activity-item {
  display: flex;
  gap: 1rem;
  padding-bottom: 1.25rem;
  margin-bottom: 1.25rem;
  border-bottom: 1px dashed var(--border-light);
}

.activity-item:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }

.activity-dot {
  width: 10px; height: 10px;
  background: var(--primary);
  border-radius: 50%;
  margin-top: 5px;
  flex-shrink: 0;
}

.activity-content p { font-size: 0.95rem; color: var(--text-primary); }
.activity-content span { font-size: 0.8rem; color: var(--text-muted); }

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-btn-p {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f1f5f9;
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 600;
  transition: all 0.2s;
}

.action-btn-p:hover {
  background: #e2e8f0;
  transform: translateX(4px);
}

.a-icon { font-size: 1.2rem; }

.btn-text {
  background: none; border: none; color: var(--primary); font-weight: 600; cursor: pointer;
}

@media (max-width: 1024px) {
  .main-grid { grid-template-columns: 1fr; }
}
</style>
