<template>
  <div class="dashboard-secretariat">
    <header class="dashboard-header">
      <h2>Tableau de Bord - Secrétariat Pédagogique</h2>
      <p class="subtitle">Gestion des Étudiants, Absences et Édition des résultats.</p>
    </header>

    <div class="shortcut-grid">
      <NuxtLink to="/etudiants" class="shortcut-card">
        <h4>Gestion des Étudiants</h4>
        <p>Inscriptions et liste officielle.</p>
      </NuxtLink>

      <NuxtLink to="/saisie" class="shortcut-card">
        <h4>Saisie des Absences</h4>
        <p>Comptabilisation des heures pénalisantes par matière.</p>
      </NuxtLink>

      <NuxtLink to="/deliberations" class="shortcut-card">
        <h4>Préparation du Jury</h4>
        <p>Résultats annuels et décisions finale.</p>
      </NuxtLink>

      <NuxtLink to="/secretariat/enseignants" class="shortcut-card">
        <h4>Gestion des Enseignants</h4>
        <p>Assignation des matières et gestion du personnel.</p>
      </NuxtLink>

      <NuxtLink to="/secretariat/edition-bulletins" class="shortcut-card">
        <h4>Édition des Bulletins</h4>
        <p>Gestion de la structure : semestres, UE, matières, absences.</p>
      </NuxtLink>

      <NuxtLink to="/secretariat/modification-notes" class="shortcut-card">
        <h4>Modification des Notes</h4>
        <p>Consultation et correction des notes par matière.</p>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
useHead({ title: 'Secrétariat | Bull ASUR' })
</script>

<style scoped>
.dashboard-header { margin-bottom: 2rem; }
.dashboard-header h2 { font-size: 1.75rem; color: var(--text-main); margin-bottom: 0.25rem; font-weight: 700; }
.subtitle { color: var(--text-muted); font-size: 1rem; }

.shortcut-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
.shortcut-card { display: block; padding: 2rem 1.5rem; border-radius: var(--radius); background: var(--surface); border: 1px solid var(--border); box-shadow: var(--shadow); text-align: left; text-decoration: none; color: var(--text-main); transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s; border-left: 5px solid var(--primary); }
.shortcut-card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px -5px rgba(0,0,0,0.1); border-color: var(--primary); }
.shortcut-card h4 { font-size: 1.25rem; font-weight: 700; margin-bottom: 0.75rem; color: var(--text-main); }
.shortcut-card p { font-size: 0.95rem; color: var(--text-muted); line-height: 1.5; }
</style>
