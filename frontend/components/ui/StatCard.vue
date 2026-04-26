<template>
  <div class="stat-card">
    <div class="stat-icon-monochrome">
      <slot name="icon">📊</slot>
    </div>
    <div class="stat-info">
      <span class="stat-label">{{ label }}</span>
      <h3 class="stat-value">{{ value }}</h3>
      <div v-if="trend" class="trend-container">
        <span class="stat-trend" :class="trendClass">
          {{ trend > 0 ? '↑' : '↓' }} {{ Math.abs(trend) }}%
        </span>
        <span class="trend-text">ce mois</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  label: String,
  value: [String, Number],
  trend: Number,
  color: { type: String, default: '#2563eb' }
})
const trendClass = computed(() => props.trend > 0 ? 'trend-up' : 'trend-down')
</script>

<style scoped>
.stat-card {
  background: white;
  padding: 1.75rem;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  transition: all 0.3s;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: black;
}
.stat-icon-monochrome {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  color: black;
  font-size: 1.4rem;
}
.stat-info {
  display: flex;
  flex-direction: column;
}
.stat-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.stat-value {
  font-size: 1.4rem;
  font-weight: 800;
  color: black;
  margin: 0.2rem 0;
}
.trend-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.stat-trend {
  font-size: 0.8rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
}
.trend-up { background: #f1f5f9; color: black; }
.trend-down { background: #f1f5f9; color: #666; }
.trend-text { color: #94a3b8; font-size: 0.75rem; }
</style>
