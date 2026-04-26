<template>
  <div class="dashboard-enseignant">
    <header class="dashboard-header">
      <h2>Espace Enseignant</h2>
      <p class="subtitle">Bienvenue ! Gérez les évaluations de vos matières.</p>
    </header>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon modules">📚</div>
        <div class="stat-content">
          <h3>2</h3>
          <p>Matières assignées</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon grades">✅</div>
        <div class="stat-content">
          <h3>48</h3>
          <p>Notes à saisir</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon alert">⚠️</div>
        <div class="stat-content">
          <h3>S5</h3>
          <p>Semestre en cours</p>
        </div>
      </div>
    </div>

    <div class="actions-panel">
      <h3>Accès rapides</h3>
      <div class="shortcut-grid">
        <NuxtLink to="/saisie" class="shortcut-card">
          <span class="icon">📝</span>
          <h4>Saisie des notes</h4>
          <p>Anglais technique (UE5-1)</p>
        </NuxtLink>
        <NuxtLink to="/saisie" class="shortcut-card">
          <span class="icon">📝</span>
          <h4>Saisie des notes</h4>
          <p>Management d'équipe (UE5-1)</p>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({ title: 'Dashboard Enseignant | Bull ASUR' })
</script>

<style scoped>
.dashboard-header { margin-bottom: 2rem; }
.dashboard-header h2 { font-size: 1.75rem; color: var(--text-main); margin-bottom: 0.25rem; font-weight: 700; }
.subtitle { color: var(--text-muted); font-size: 1rem; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-bottom: 2.5rem; }
.stat-card { background-color: var(--surface); border-radius: var(--radius); padding: 1.5rem; display: flex; align-items: center; box-shadow: var(--shadow); border: 1px solid var(--border); }
.stat-icon { width: 56px; height: 56px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.75rem; margin-right: 1.25rem; }
.stat-icon.modules { background-color: rgba(16, 185, 129, 0.1); color: #10b981; }
.stat-icon.grades { background-color: rgba(37, 99, 235, 0.1); color: #3b82f6; }
.stat-icon.alert { background-color: rgba(245, 158, 11, 0.1); color: #f59e0b; }
.stat-content h3 { font-size: 1.4rem; font-weight: 700; line-height: 1.2; }
.stat-content p { color: var(--text-muted); font-size: 0.875rem; font-weight: 500; }
.actions-panel h3 { font-size: 1.2rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }
.shortcut-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }
.shortcut-card { display: block; padding: 1.5rem; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); text-decoration: none; color: var(--text-main); transition: transform 0.2s, box-shadow 0.2s; }
.shortcut-card:hover { transform: translateY(-3px); box-shadow: var(--shadow); border-color: var(--primary); }
.shortcut-card .icon { font-size: 2rem; display: block; margin-bottom: 0.75rem; }
.shortcut-card h4 { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem; }
.shortcut-card p { font-size: 0.9rem; color: var(--text-muted); }
</style>
