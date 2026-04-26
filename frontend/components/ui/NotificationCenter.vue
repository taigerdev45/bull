<template>
  <div class="notification-center">
    <div class="notif-bell-wrapper" @click="toggleDropdown">
      <span class="n-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="24" height="24">
          <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
          <path d="M13.73 21a2 2 0 01-3.46 0"></path>
        </svg>
      </span>
      <span v-if="unreadCount > 0" class="notif-badge">{{ unreadCount }}</span>
    </div>

    <Transition name="fade-scale">
      <div v-if="isOpen" class="notif-dropdown premium-card" v-click-outside="closeDropdown">
        <div class="dropdown-header">
          <h3>Centre de Notifications</h3>
          <button v-if="unreadCount > 0" @click="markAllAsRead" class="btn-text">Tout marquer comme lu</button>
        </div>

        <div class="notif-list custom-scrollbar">
          <div v-for="notif in notifications" :key="notif.id" :class="['notif-item', { 'unread': !notif.read }]" @click="markAsRead(notif)">
            <div class="notif-icon-box" :class="notif.type">
              <span v-if="notif.type === 'grade'">✍️</span>
              <span v-else-if="notif.type === 'absence'">⌛</span>
              <span v-else>🔔</span>
            </div>
            <div class="notif-content">
              <p class="notif-title">{{ notif.title }}</p>
              <p class="notif-msg">{{ notif.message }}</p>
              <span class="notif-time">{{ notif.time }}</span>
            </div>
            <div v-if="!notif.read" class="unread-dot"></div>
          </div>

          <div v-if="notifications.length === 0" class="notif-empty">
            <div class="empty-icon">📭</div>
            <p>Aucune notification de profil</p>
          </div>
        </div>

        <div class="dropdown-footer">
          <NuxtLink to="/notifications" class="see-all" @click="closeDropdown">Voir toutes les activités</NuxtLink>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const isOpen = ref(false)

// Simulation de données (Idéalement via un Store Pinia ou Composable)
const notifications = ref([
  { id: 1, type: 'grade', title: 'Nouvelle Note', message: 'Votre note de Java a été publiée : 16.5/20', time: 'Il y a 10 min', read: false },
  { id: 2, type: 'absence', title: 'Alerte Absence', message: 'Une absence a été signalée en Mathématiques.', time: 'Hier', read: false },
  { id: 3, type: 'system', title: 'Sécurité', message: 'Connexion détectée depuis un nouvel appareil.', time: 'Il y a 2 jours', read: true }
])

const unreadCount = computed(() => notifications.value.filter(n => !n.read).length)

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

const markAsRead = (notif) => {
  notif.read = true
}

const markAllAsRead = () => {
  notifications.value.forEach(n => n.read = true)
}

// Directive simple click-outside
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value()
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
}
</script>

<style scoped>
.notification-center { position: relative; }

.notif-bell-wrapper { cursor: pointer; position: relative; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 12px; transition: all 0.2s; color: #64748b; }
.notif-bell-wrapper:hover { background: #f1f5f9; color: #000; }

.notif-badge { position: absolute; top: -2px; right: -2px; min-width: 18px; height: 18px; padding: 0 5px; background: #000; color: #fff; border-radius: 20px; font-size: 10px; font-weight: 900; display: flex; align-items: center; justify-content: center; border: 2.5px solid #fff; }

.notif-dropdown { position: absolute; top: 120%; right: 0; width: 380px; z-index: 1000; overflow: hidden; border-radius: 24px; animation: slideUp 0.3s ease-out; }

@keyframes slideUp { from { opacity: 0; transform: translateY(10px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }

.dropdown-header { padding: 1.5rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; }
.dropdown-header h3 { font-size: 0.95rem; font-weight: 900; letter-spacing: -0.5px; }

.btn-text { background: transparent; border: none; font-size: 0.75rem; font-weight: 800; color: #64748b; cursor: pointer; text-decoration: underline; }
.btn-text:hover { color: #000; }

.notif-list { max-height: 400px; overflow-y: auto; }

.notif-item { display: flex; gap: 1rem; padding: 1.25rem 1.5rem; cursor: pointer; transition: all 0.2s; position: relative; border-bottom: 1px solid #f8fafc; }
.notif-item:hover { background: #f8fafc; }
.notif-item.unread { background: #fafafa; }

.notif-icon-box { width: 42px; height: 42px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0; background: #fff; border: 2px solid #f1f5f9; }
.notif-icon-box.grade { border-color: #000; }
.notif-icon-box.absence { border-color: #f1f5f9; }

.notif-content { flex: 1; display: flex; flex-direction: column; gap: 0.2rem; }
.notif-title { font-size: 0.9rem; font-weight: 800; color: #000; }
.notif-msg { font-size: 0.8rem; color: #64748b; font-weight: 500; line-height: 1.4; }
.notif-time { font-size: 0.7rem; font-weight: 700; color: #94a3b8; margin-top: 0.25rem; }

.unread-dot { width: 8px; height: 8px; background: #000; border-radius: 50%; position: absolute; right: 1.5rem; top: 1.5rem; }

.notif-empty { padding: 4rem 2rem; text-align: center; }
.empty-icon { font-size: 2.5rem; margin-bottom: 1rem; opacity: 0.2; }
.notif-empty p { font-size: 0.9rem; font-weight: 700; color: #94a3b8; }

.dropdown-footer { padding: 1.25rem; background: #fafafa; text-align: center; }
.see-all { font-size: 0.8rem; font-weight: 900; color: #000; text-decoration: none; }

.fade-scale-enter-active, .fade-scale-leave-active { transition: all 0.2s ease; }
.fade-scale-enter-from, .fade-scale-leave-to { opacity: 0; transform: scale(0.95) translateY(10px); }
</style>
