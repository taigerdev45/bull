<template>
  <div class="stat-card">
    <div class="stat-icon" :style="{ backgroundColor: color + '15', color: color }">
      <slot name="icon">📊</slot>
    </div>
    <div class="stat-info">
      <span class="stat-label">{{ label }}</span>
      <h3 class="stat-value">{{ value }}</h3>
      <p v-if="trend" class="stat-trend" :class="trendClass">
        {{ trend > 0 ? '↑' : '↓' }} {{ Math.abs(trend) }}% 
        <span class="trend-text">ce mois</span>
      </p>
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
  background: var(--bg-surface);
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  display: flex;
  align-items: center;
  gap: 1.25rem;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid var(--border-light);
}
.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
.stat-icon {
  width: 54px;
  height: 54px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}
.stat-info {
  display: flex;
  flex-direction: column;
}
.stat-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.stat-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0.1rem 0;
}
.stat-trend {
  font-size: 0.75rem;
  font-weight: 600;
}
.trend-up { color: #10b981; }
.trend-down { color: #ef4444; }
.trend-text { color: var(--text-muted); font-weight: 400; }
</style>
