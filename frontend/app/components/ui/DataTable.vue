<template>
  <div class="datatable-wrapper">
    <div class="datatable-header" v-if="title || $slots.actions">
      <h3 v-if="title">{{ title }}</h3>
      <div class="actions">
        <slot name="actions" />
      </div>
    </div>
    
    <div class="table-responsive">
      <table class="datatable">
        <thead>
          <tr>
            <th v-for="(col, index) in columns" :key="index" :style="{ width: col.width }">
              {{ col.label }}
            </th>
            <th v-if="$slots.rowActions || actions" class="actions-col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!data || data.length === 0">
            <td :colspan="columns.length + (actions ? 1 : 0)" class="empty-state">
              Aucune donnée disponible.
            </td>
          </tr>
          <tr v-for="(row, rowIndex) in data" :key="rowIndex">
            <td v-for="(col, colIndex) in columns" :key="colIndex">
              <slot :name="col.key" :row="row">
                {{ row[col.key] }}
              </slot>
            </td>
            <td v-if="$slots.rowActions || actions" class="actions-col">
              <slot name="rowActions" :row="row" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  columns: {
    type: Array,
    required: true
  },
  data: {
    type: Array,
    required: true
  },
  actions: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.datatable-wrapper {
  background-color: var(--surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.datatable-header {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border);
}

.datatable-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-main);
  margin: 0;
}

.table-responsive {
  overflow-x: auto;
}

.datatable {
  width: 100%;
  border-collapse: collapse;
}

.datatable th, .datatable td {
  padding: 1rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

.datatable th {
  background-color: #f8fafc;
  font-weight: 600;
  color: var(--text-muted);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.datatable tbody tr {
  transition: background-color 0.2s ease;
}

.datatable tbody tr:hover {
  background-color: #f1f5f9;
}

.actions-col {
  text-align: right;
  width: 120px;
}

.empty-state {
  text-align: center;
  padding: 3rem 1.5rem !important;
  color: var(--text-muted);
  font-style: italic;
}
</style>
