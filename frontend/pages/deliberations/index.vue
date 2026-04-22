<template>
  <div class="page-deliberation">
    <header class="page-header">
      <div class="header-content">
        <h2>Délibérations du Jury (S5)</h2>
        <p>Année universitaire 2025-2026 - Liste récapitulative des résultats</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-secondary">
          <span class="icon">📊</span> Exporter Excel
        </button>
        <button class="btn btn-primary">
          <span class="icon">✔️</span> Valider les décisions
        </button>
      </div>
    </header>

    <div class="grid-container">
      <table class="grid-delib">
        <thead>
          <tr>
            <th>Étudiant</th>
            <th class="center">Moy S5</th>
            <th class="center">UE5-1</th>
            <th class="center">UE5-2</th>
            <th class="center">Crédits</th>
            <th class="center">Décision S5</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="res in resultats" :key="res.id" :class="{'is-failed': res.decision === 'Ajourné'}">
            <td class="font-bold">{{ res.nom }} {{ res.prenom }}</td>
            <td class="center font-bold value">
              {{ res.moyS5 }}
            </td>
            <td class="center">{{ res.ue1 }}</td>
            <td class="center">{{ res.ue2 }}</td>
            <td class="center badge-container">
              <span :class="['badge-sm', res.credits === 30 ? 'badge-success' : 'badge-warning']">
                {{ res.credits }} / 30
              </span>
            </td>
            <td class="center">
              <span :class="['decision-badge', res.decision === 'Validé' ? 'valid' : 'invalid']">
                {{ res.decision }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

useHead({ title: 'Délibérations | LP ASUR' })

const { fetchApi } = useApi()
const isLoading = ref(true)
const resultats = ref([])

const loadResultats = async () => {
  isLoading.value = true
  try {
    const response = await fetchApi('/resultats/promotion/stats/', {
      params: { 
        semestre: 5, // Par défaut S5 pour cette page
        promo_id: 'LP_ASUR_2026' 
      }
    })
    
    if (response && response.resultats) {
      resultats.value = response.resultats
    }
  } catch(error) {
    console.error('Failed to load resultats:', error)
    alert("Erreur lors du chargement des délibérations.")
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadResultats()
})
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
  border: none;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
}

.btn-secondary {
  background-color: white;
  color: var(--text-main);
  border: 1px solid var(--border);
}

.grid-container {
  background-color: var(--surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow-x: auto;
}

.grid-delib {
  width: 100%;
  border-collapse: collapse;
}

.grid-delib th, .grid-delib td {
  padding: 1rem;
  border-bottom: 1px solid var(--border);
}

.grid-delib th {
  background-color: #f8fafc;
  color: var(--text-muted);
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
}

.grid-delib tbody tr:hover {
  background-color: #f1f5f9;
}

.center { text-align: center; }
.font-bold { font-weight: 600; color: var(--text-main); }

.grid-delib tbody tr.is-failed {
  background-color: rgba(239, 68, 68, 0.03);
}

.grid-delib tbody tr.is-failed .value {
  color: var(--danger);
}

.badge-sm {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 700;
}

.badge-success { background-color: rgba(16, 185, 129, 0.1); color: var(--success); }
.badge-warning { background-color: rgba(239, 68, 68, 0.1); color: var(--danger); }

.decision-badge {
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 700;
}

.valid {
  background-color: var(--success);
  color: white;
}

.invalid {
  background-color: var(--danger);
  color: white;
}
</style>
