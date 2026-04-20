<template>
  <div class="page-referentiels">
    <header class="page-header">
      <div class="header-content">
        <h2>Gestion des Référentiels Pédagogiques</h2>
        <p>Gérez la structure académique: Unités d'Enseignement (UE) et Matières.</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="addUE">
          <span class="icon">➕</span> Ajouter une UE
        </button>
      </div>
    </header>

    <div class="referentiels-container">
      <div class="ue-card" v-for="ue in ues" :key="ue.id">
        <div class="ue-header">
          <div class="ue-title">
            <h3>{{ ue.code }} : {{ ue.libelle }}</h3>
            <span class="badge">{{ ue.semestre }}</span>
          </div>
          <div class="ue-actions">
            <button class="action-btn edit-btn">✏️</button>
            <button class="action-btn delete-btn">🗑️</button>
          </div>
        </div>

        <table class="matieres-table">
          <thead>
            <tr>
              <th>Matière</th>
              <th width="100" class="center">Coefficient</th>
              <th width="100" class="center">Crédits</th>
              <th width="80" class="center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="mat in ue.matieres" :key="mat.id">
              <td>{{ mat.libelle }}</td>
              <td class="center font-bold">{{ mat.coefficient }}</td>
              <td class="center font-bold">{{ mat.credits }}</td>
              <td class="center actions-cell">
                <button class="action-btn edit-sm-btn">✏️</button>
              </td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td class="add-matiere-cell">
                <button class="btn btn-dashed">
                  <span class="icon">➕</span> Ajouter une matière à {{ ue.code }}
                </button>
              </td>
              <td class="center total-lbl">Total :</td>
              <td class="center total-val">{{ totalCredits(ue) }}</td>
              <td></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

useHead({
  title: 'Référentiels | LP ASUR'
})

const ues = ref([
  {
    id: 1,
    code: 'UE5-1',
    libelle: 'Enseignement Général',
    semestre: 'Semestre 5',
    matieres: [
      { id: 101, libelle: 'Anglais technique', coefficient: 1, credits: 2 },
      { id: 102, libelle: 'Management d\'équipe', coefficient: 1, credits: 1 },
      { id: 103, libelle: 'Communication', coefficient: 2, credits: 1 },
      { id: 104, libelle: 'Droit de l\'informatique', coefficient: 2, credits: 2 },
    ]
  },
  {
    id: 2,
    code: 'UE5-2',
    libelle: 'Connaissances de Base et Outils LAN',
    semestre: 'Semestre 5',
    matieres: [
      { id: 201, libelle: 'Remise à niveau IOS', coefficient: 2, credits: 2 },
      { id: 202, libelle: 'Connaissance des réseaux LAN', coefficient: 2, credits: 2 },
    ]
  }
])

const totalCredits = (ue) => {
  return ue.matieres.reduce((acc, current) => acc + current.credits, 0)
}

const addUE = () => {
  alert('Ouverture de la modale de création d\'UE...')
}
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

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.6rem 1.25rem;
  border-radius: var(--radius);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
}

.btn-primary { background-color: var(--primary); color: white; }
.btn-primary:hover { background-color: var(--primary-hover); transform: translateY(-1px); }
.btn-secondary { background-color: white; color: var(--text-main); border: 1px solid var(--border); }
.btn-dashed { 
  background-color: transparent; 
  border: 1px dashed var(--border); 
  color: var(--text-muted); 
  width: 100%;
  justify-content: center;
  padding: 0.4rem;
  font-size: 0.85rem;
}
.btn-dashed:hover { background-color: #f8fafc; border-color: var(--primary); color: var(--primary); }

.referentiels-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.ue-card {
  background-color: var(--surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  overflow: hidden;
}

.ue-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8fafc;
}

.ue-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.ue-title h3 {
  font-size: 1.2rem;
  color: var(--text-main);
  margin: 0;
}

.badge {
  background-color: rgba(37, 99, 235, 0.1);
  color: var(--primary);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  opacity: 0.7;
  padding: 0.25rem;
  transition: opacity 0.2s, transform 0.2s;
}

.action-btn:hover { opacity: 1; transform: scale(1.1); }
.edit-sm-btn { font-size: 0.95rem; }

.matieres-table {
  width: 100%;
  border-collapse: collapse;
}

.matieres-table th, .matieres-table td {
  padding: 0.75rem 1.5rem;
  border-bottom: 1px solid var(--border);
}

.matieres-table th {
  text-align: left;
  font-weight: 600;
  color: var(--text-muted);
  font-size: 0.85rem;
  text-transform: uppercase;
}

.matieres-table tbody tr:hover {
  background-color: #fbfcfe;
}

.add-matiere-cell {
  padding: 0.75rem 1.5rem;
}

.total-lbl {
  font-weight: 600;
  color: var(--text-muted);
  text-align: right;
}

.total-val {
  font-weight: 700;
  color: var(--primary);
  font-size: 1.1rem;
}

.center { text-align: center; }
.font-bold { font-weight: 600; color: var(--text-main); }
</style>
