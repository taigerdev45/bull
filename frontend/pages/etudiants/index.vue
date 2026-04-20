<template>
  <div class="page-etudiants">
    <header class="page-header">
      <div class="header-content">
        <h2>Gestion des Étudiants</h2>
        <p>Gérez les élèves inscrits en Licence Professionnelle ASUR.</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-secondary">
          <span class="icon">📥</span> Importer (Excel)
        </button>
        <button class="btn btn-primary">
          <span class="icon">➕</span> Ajouter un Étudiant
        </button>
      </div>
    </header>

    <div class="table-container">
      <DataTable 
        title="Liste de la Promotion" 
        :columns="columns" 
        :data="students" 
        :actions="true"
      >
        <template #status="{ row }">
          <span :class="['badge', row.status === 'Inscrit' ? 'badge-success' : 'badge-warning']">
            {{ row.status }}
          </span>
        </template>
        <template #rowActions="{ row }">
          <button class="action-btn view-btn" title="Voir le profil">👁️</button>
          <button class="action-btn edit-btn" title="Modifier">✏️</button>
          <button class="action-btn delete-btn" title="Supprimer">🗑️</button>
        </template>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

useHead({
  title: 'Étudiants | LP ASUR'
})

// Mocks
const columns = [
  { key: 'id', label: 'ID', width: '80px' },
  { key: 'nom', label: 'Nom' },
  { key: 'prenom', label: 'Prénom' },
  { key: 'bac', label: 'Baccalauréat' },
  { key: 'provenance', label: 'Étab. Provenance' },
  { key: 'status', label: 'Statut', width: '120px' }
]

const students = ref([
  { id: '1001', nom: 'Dupont', prenom: 'Jean', bac: 'S', provenance: 'Lycée A', status: 'Inscrit' },
  { id: '1002', nom: 'Martin', prenom: 'Sophie', bac: 'STI2D', provenance: 'Lycée B', status: 'Inscrit' },
  { id: '1003', nom: 'Bernard', prenom: 'Luc', bac: 'Pro SN', provenance: 'Lycée C', status: 'Inscrit' },
  { id: '1004', nom: 'Dubois', prenom: 'Marie', bac: 'S', provenance: 'Lycée A', status: 'Attente Jury' },
])
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
}

.header-content h2 {
  font-size: 1.75rem;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.header-content p {
  color: var(--text-muted);
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.6rem 1.25rem;
  border-radius: var(--radius);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn .icon {
  margin-right: 0.5rem;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
}

.btn-primary:hover {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
}

.btn-secondary {
  background-color: white;
  color: var(--text-main);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  background-color: #f8fafc;
}

.table-container {
  margin-top: 1rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-block;
}

.badge-success {
  background-color: rgba(16, 185, 129, 0.1);
  color: var(--success);
}

.badge-warning {
  background-color: rgba(245, 158, 11, 0.1);
  color: var(--warning);
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  opacity: 0.7;
  transition: opacity 0.2s;
  padding: 0 0.25rem;
}

.action-btn:hover {
  opacity: 1;
}

.view-btn:hover { transform: scale(1.1); }
.edit-btn:hover { transform: scale(1.1); }
.delete-btn:hover { transform: scale(1.1); }
</style>
