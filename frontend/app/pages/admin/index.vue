<template>
  <div class="dashboard-admin">
    <header class="dashboard-header">
      <h2>Tableau de Bord - Administration</h2>
      <p class="subtitle">Gestion globale du système (Utilisateurs, Rôles, UEs, Semestres)</p>
    </header>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-content">
          <h3>24</h3>
          <p>Utilisateurs Actifs</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-content">
          <h3>Semestre 5</h3>
          <p>Semestre Courant</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-content">
          <h3>4</h3>
          <p>Unités d'Enseignement (UE)</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-content">
          <h3>16</h3>
          <p>Matières / Évaluations</p>
        </div>
      </div>
    </div>

    <div class="dashboard-widgets">
      <div class="widget">
        <h3>Gestion des Entités</h3>
        <ul class="activity-list">
          <li>
            <strong>Utilisateurs & Rôles</strong>
            <span class="time">Création de comptes (Enseignants, Secrétariat, Admin)</span>
          </li>
          <li>
            <strong>Semestres</strong>
            <span class="time">Définition (S5, S6) et activation du semestre courant</span>
          </li>
          <li>
            <strong>Référentiel UEs et Matières</strong>
            <span class="time">Configuration des coefficients et crédits associés</span>
          </li>
        </ul>
        <NuxtLink class="action-link" to="/referentiels">Accéder aux référentiels →</NuxtLink>
      </div>

      <div class="widget">
        <h3>Paramètres Globaux</h3>
        <ul class="activity-list">
          <li>
            <strong>Règles de Compensation</strong>
            <span class="time">Définition des crédits de rattrapage</span>
          </li>
          <li>
            <strong>Grille de Mentions</strong>
            <span class="time">(Passable 10-12, Assez Bien 12-14, etc.)</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({ title: 'Admin Dashboard | Bull ASUR' })
</script>

<style scoped>
.dashboard-header { margin-bottom: 2rem; }
.dashboard-header h2 { font-size: 1.75rem; color: var(--text-main); font-weight: 700; margin-bottom: 0.25rem; }
.subtitle { color: var(--text-muted); font-size: 1rem; }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin-bottom: 2.5rem; }
.stat-card { background-color: var(--surface); border-radius: var(--radius); padding: 1.5rem; display: flex; align-items: center; box-shadow: var(--shadow); border: 1px solid var(--border); transition: transform 0.2s ease; border-left: 4px solid var(--theme-dark); }
.stat-card:hover { transform: translateY(-2px); }

.stat-content h3 { font-size: 1.8rem; font-weight: 700; color: var(--text-main); line-height: 1.2; }
.stat-content p { color: var(--text-muted); font-size: 0.875rem; font-weight: 500; margin-top: 0.2rem; }

.dashboard-widgets { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.widget { background-color: var(--surface); border-radius: var(--radius); padding: 1.5rem; box-shadow: var(--shadow); border: 1px solid var(--border); }
.widget h3 { font-size: 1.1rem; margin-bottom: 1.25rem; color: var(--text-main); border-bottom: 1px solid var(--border); padding-bottom: 0.75rem; }

.activity-list { list-style: none; padding: 0; }
.activity-list li { padding: 1rem 0; border-bottom: 1px solid var(--border); color: var(--text-main); font-size: 0.95rem; }
.activity-list li:last-child { border-bottom: none; }
.activity-list strong { color: var(--theme-dark); }

.time { display: block; font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem; }

.action-link { display: inline-block; margin-top: 1.5rem; color: var(--primary); font-weight: 600; text-decoration: none; }
.action-link:hover { text-decoration: underline; }

@media (max-width: 768px) {
  .dashboard-widgets { grid-template-columns: 1fr; }
}
</style>
