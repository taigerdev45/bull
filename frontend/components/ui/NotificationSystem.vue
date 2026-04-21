<template>
  <div class="notification-container">
    <TransitionGroup name="notification" tag="div">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="['notification', `notification-${notification.type}`]"
      >
        <div class="notification-icon">
          <span v-if="notification.type === 'success'">✅</span>
          <span v-else-if="notification.type === 'error'">❌</span>
          <span v-else-if="notification.type === 'warning'">⚠️</span>
          <span v-else>ℹ️</span>
        </div>
        
        <div class="notification-content">
          <div class="notification-title">{{ notification.title }}</div>
          <div class="notification-message">{{ notification.message }}</div>
        </div>
        
        <button class="notification-close" @click="removeNotification(notification.id)">
          &times;
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const notifications = ref([])
let notificationIdCounter = 0

const addNotification = (title, message, type = 'info', duration = 5000) => {
  const id = ++notificationIdCounter
  const notification = {
    id,
    title,
    message,
    type,
    timestamp: Date.now()
  }
  
  notifications.value.push(notification)
  
  // Auto-suppression après la durée spécifiée
  if (duration > 0) {
    setTimeout(() => {
      removeNotification(id)
    }, duration)
  }
  
  return id
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
  }
}

const clearAll = () => {
  notifications.value = []
}

// Gestionnaire d'événements pour les notifications globales
const handleShowNotification = (event) => {
  const { title, message, type } = event.detail
  addNotification(title, message, type)
}

onMounted(() => {
  window.addEventListener('show-notification', handleShowNotification)
})

onUnmounted(() => {
  window.removeEventListener('show-notification', handleShowNotification)
})

// Exposer les méthodes globalement
defineExpose({
  addNotification,
  removeNotification,
  clearAll
})
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  max-width: 400px;
  pointer-events: none;
}

.notification {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  margin-bottom: 0.75rem;
  border-radius: var(--radius);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  pointer-events: all;
  backdrop-filter: blur(8px);
  border: 1px solid;
}

.notification-success {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.3);
  color: #065f46;
}

.notification-error {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
  color: #7f1d1d;
}

.notification-warning {
  background: rgba(245, 158, 11, 0.1);
  border-color: rgba(245, 158, 11, 0.3);
  color: #78350f;
}

.notification-info {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
  color: #1e3a8a;
}

.notification-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
  line-height: 1.3;
}

.notification-message {
  font-size: 0.875rem;
  opacity: 0.9;
  line-height: 1.4;
}

.notification-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  opacity: 0.7;
  padding: 0;
  line-height: 1;
  flex-shrink: 0;
  transition: opacity 0.2s;
}

.notification-close:hover {
  opacity: 1;
}

/* Animations */
.notification-enter-active {
  transition: all 0.3s ease-out;
}

.notification-leave-active {
  transition: all 0.3s ease-in;
}

.notification-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.notification-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.notification-move {
  transition: transform 0.3s ease;
}

/* Responsive */
@media (max-width: 640px) {
  .notification-container {
    top: 10px;
    right: 10px;
    left: 10px;
    max-width: none;
  }
  
  .notification {
    padding: 0.875rem;
  }
  
  .notification-title {
    font-size: 0.95rem;
  }
  
  .notification-message {
    font-size: 0.8rem;
  }
}
</style>
