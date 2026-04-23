<template>
  <div class="data-table-container">
    <div class="table-header">
      <div class="header-info">
        <h3>{{ title }}</h3>
        <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
      </div>
      <div class="header-actions">
        <div class="search-input">
          <span>🔍</span>
          <input v-model="search" type="text" placeholder="Rechercher..." />
        </div>
        <slot name="headerActions"></slot>
      </div>
    </div>

    <div class="table-content">
      <table class="premium-table">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col.key">
              {{ col.label }}
            </th>
            <th v-if="actions" class="actions-col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in filteredData" :key="index">
            <td v-for="col in columns" :key="col.key">
              <slot :name="col.key" :row="row">
                {{ row[col.key] }}
              </slot>
            </td>
            <td v-if="actions" class="actions-cell">
              <slot name="rowActions" :row="row"></slot>
            </td>
          </tr>
          <tr v-if="filteredData.length === 0">
            <td :colspan="columns.length + (actions ? 1 : 0)" class="empty-state">
              Aucune donnée trouvée.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="table-footer">
      <span>Affichage de {{ filteredData.length }} sur {{ data.length }} entrées</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  title: String,
  subtitle: String,
  columns: Array,
  data: Array,
  actions: Boolean
})

const search = ref('')

const filteredData = computed(() => {
  if (!search.value) return props.data
  const q = search.value.toLowerCase()
  return props.data.filter(item => 
    Object.values(item).some(val => String(val).toLowerCase().includes(q))
  )
})
</script>

<style scoped>
.data-table-container {
  background: white;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
}

.table-header {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-light);
  gap: 1.5rem;
}

.header-info h3 { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); }
.subtitle { font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem; }

.header-actions { display: flex; gap: 1rem; align-items: center; }

.search-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f1f5f9;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  transition: all 0.2s;
}

.search-input:focus-within {
  background: white;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px var(--primary-glow);
}

.search-input input {
  border: none;
  background: none;
  outline: none;
  font-size: 0.85rem;
}

.table-content { overflow-x: auto; }

.premium-table { width: 100%; border-collapse: collapse; text-align: left; }
.premium-table th {
  padding: 1rem 1.5rem;
  background: #f8fafc;
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.premium-table td {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-light);
  font-size: 0.95rem;
  color: var(--text-primary);
}

.premium-table tr:last-child td { border-bottom: none; }
.premium-table tr:hover td { background: #fbfcfe; }

.actions-col { text-align: center; }
.actions-cell {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.empty-state { text-align: center; padding: 3rem; color: var(--text-muted); }

.table-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border-light);
  font-size: 0.8rem;
  color: var(--text-muted);
  background: #fbfcfe;
}
</style>
