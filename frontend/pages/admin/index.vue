<template>
  <div class="dashboard-container">
    <div class="welcome-banner">
      <div class="welcome-text">
        <h1>Bon retour, Administrateur</h1>
        <p>Aperçu de l'activité globale du système.</p>
      </div>
      <div class="current-semestre-badge">
        <span>Semestre Actif :</span>
        <strong>S5</strong>
      </div>
    </div>

    <div class="stats-grid">
      <StatCard label="Étudiants Inscrits" value="128" :trend="12">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 00-3-3.87"></path><path d="M16 3.13a4 4 0 010 7.75"></path></svg>
        </template>
      </StatCard>
      <StatCard label="Matières Actives" value="16" :trend="0">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="24"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"></path></svg>
        </template>
      </StatCard>
      <StatCard label="Notes Saisies" value="1,240" :trend="8">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="24"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
        </template>
      </StatCard>
      <StatCard label="Taux Absences" value="2.4%" :trend="-5">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        </template>
      </StatCard>
    </div>

    <div class="main-grid">
      <!-- Activity Feed -->
      <div class="card activity-card">
        <div class="card-header">
          <h3>Activités Récentes</h3>
          <NuxtLink to="/admin/audit" class="btn-text">Voir tout</NuxtLink>
        </div>
        <div class="card-body">
          <div v-if="pending" class="loader-container">
            <div class="loader-p"></div>
          </div>
          <div v-else-if="activities.length" v-for="log in activities" :key="log.id" class="activity-item">
            <div class="activity-dot" :class="getActionClass(log.action_type)"></div>
            <div class="activity-content">
              <p>
                <strong>{{ formatAction(log.action_type) }}</strong> 
                par {{ log.user_email }}
              </p>
              <div class="activity-details" v-if="log.details">{{ log.details }}</div>
              <span>{{ formatDate(log.created_at) }}</span>
            </div>
          </div>
          <div v-else class="empty-state">Aucune activité récente.</div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card actions-card">
        <div class="card-header">
          <h3>Actions Rapides</h3>
        </div>
        <div class="card-body">
          <div class="action-buttons">
            <NuxtLink to="/secretariat/etudiants" class="action-btn-p">
              <span class="a-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><line x1="19" y1="8" x2="19" y2="14"></line><line x1="16" y1="11" x2="22" y2="11"></line></svg>
              </span>
              Inscrire Étudiant
            </NuxtLink>
            <NuxtLink to="/admin/referentiels" class="action-btn-p">
              <span class="a-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              </span>
              Manager UEs
            </NuxtLink>
            <NuxtLink to="/admin/logs" class="action-btn-p">
              <span class="a-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
              </span>
              Consultation Logs
            </NuxtLink>
            <NuxtLink to="/profil" class="action-btn-p">
              <span class="a-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20"><path d="M12.22 2h-.44a2 2 0 00-2 2v.18a2 2 0 01-1 1.73l-.43.25a2 2 0 01-2 0l-.15-.08a2 2 0 00-2.73.73l-.22.38a2 2 0 00.73 2.73l.15.1a2 2 0 011 1.72v.51a2 2 0 01-1 1.74l-.15.09a2 2 0 00-.73 2.73l.22.38a2 2 0 002.73.73l.15-.08a2 2 0 012 0l.43.25a2 2 0 011 1.73V20a2 2 0 002 2h.44a2 2 0 002-2v-.18a2 2 0 011-1.73l.43-.25a2 2 0 012 0l.15.08a2 2 0 002.73-.73l.22-.39a2 2 0 00-.73-2.73l-.15-.08a2 2 0 01-1-1.74v-.5a2 2 0 011-1.74l.15-.09a2 2 0 00.73-2.73l-.22-.38a2 2 0 00-2.73-.73l-.15.08a2 2 0 01-2 0l-.43-.25a2 2 0 01-1-1.73V4a2 2 0 00-2-2z"></path></svg>
              </span>
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
  background: var(--bg-sidebar);
  padding: 3rem;
  border-radius: var(--radius-xl);
  color: white;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.welcome-text h1 { font-size: 1.7rem; font-weight: 800; margin-bottom: 0.5rem; }
.welcome-text p { opacity: 0.6; font-size: 1.1rem; }

.current-semestre-badge {
  background: rgba(255,255,255,0.1);
  padding: 1rem 2rem;
  border-radius: 12px;
  display: flex;
  gap: 0.75rem;
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

.activity-content p { font-size: 0.95rem; color: var(--text-primary); margin: 0; }
.activity-content span { font-size: 0.8rem; color: var(--text-muted); }

.activity-details {
  font-size: 0.75rem;
  color: #64748b;
  background: #f8fafc;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  margin: 0.4rem 0;
  border-left: 3px solid #e2e8f0;
}

.activity-dot.success { background: #22c55e; }
.activity-dot.warning { background: #f59e0b; }
.activity-dot.danger { background: #ef4444; }
.activity-dot.info { background: #3b82f6; }

.loader-container {
  display: flex;
  justify-content: center;
  padding: 3rem;
}

.loader-p {
  width: 30px;
  height: 30px;
  border: 3px solid #f1f5f9;
  border-top-color: #0f172a;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.empty-state {
  text-align: center;
  color: #94a3b8;
  padding: 2rem;
  font-style: italic;
}

.action-buttons {
...  display: flex;
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
