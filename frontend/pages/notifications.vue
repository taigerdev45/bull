<template>
  <div class="page-notifications">
    <header class="page-header">
      <div class="header-content">
        <h1>Centre d'Activités</h1>
        <p>Historique complet de vos notifications et alertes système.</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-pill dark" @click="markAllAsRead">Tout marquer comme lu</button>
      </div>
    </header>

    <div class="notifications-container premium-card">
      <div class="notif-filters">
        <button v-for="f in filters" :key="f.key" :class="['filter-btn', { 'active': activeFilter === f.key }]" @click="activeFilter = f.key">
          {{ f.label }}
        </button>
      </div>

      <div class="notif-full-list">
        <div v-for="notif in filteredNotifications" :key="notif.id" :class="['notif-card', { 'unread': !notif.read }]">
          <div class="notif-visual">
            <div class="notif-icon-circle" :class="notif.type">
              <span v-if="notif.type === 'grade'">✍️</span>
              <span v-else-if="notif.type === 'absence'">⌛</span>
              <span v-else-if="notif.type === 'security'">🛡️</span>
              <span v-else>📢</span>
            </div>
          </div>
          
          <div class="notif-main-content">
            <div class="notif-head">
              <h3>{{ notif.title }}</h3>
              <span class="timestamp">{{ notif.fullDate }}</span>
            </div>
            <p class="description">{{ notif.message }}</p>
            <div class="notif-footer">
              <span class="category">{{ notif.category }}</span>
              <button v-if="!notif.read" class="mark-read-link" @click="notif.read = true">Marquer comme lu</button>
            </div>
          </div>

          <div v-if="!notif.read" class="unread-status-line"></div>
        </div>

        <div v-if="filteredNotifications.length === 0" class="empty-notif-state">
          <div class="icon-empty">✨</div>
          <h3>Aucune notification trouvée</h3>
          <p>Vous êtes à jour ! Toutes les notifications ont été traitées.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

useHead({ title: 'Notifications | Bull ASUR' })

const activeFilter = ref('all')
const filters = [
  { key: 'all', label: 'Toutes' },
  { key: 'unread', label: 'Non lues' },
  { key: 'academic', label: 'Académique' },
  { key: 'system', label: 'Système' }
]

const notifications = ref([
  { id: 1, type: 'grade', category: 'ACADÉMIQUE', title: 'Nouvelle Note : Programmation Java', message: 'Votre note pour le TP de Java (Semaine 4) a été saisie par l\'enseignant. Vous avez obtenu 16.5/20.', fullDate: '26 Avril 2026, 14:30', read: false },
  { id: 2, type: 'absence', category: 'ACADÉMIQUE', title: 'Absence Signalée', message: 'Une absence non justifiée a été enregistrée pour le cours de Mathématiques du 25 Avril.', fullDate: '25 Avril 2026, 09:15', read: false },
  { id: 3, type: 'security', category: 'SYSTÈME', title: 'Nouvelle Connexion', message: 'Votre compte a été accédé depuis une nouvelle adresse IP (Libreville, Gabon).', fullDate: '24 Avril 2026, 21:05', read: true },
  { id: 4, type: 'system', category: 'SYSTÈME', title: 'Mise à jour Système', message: 'Bull ASUR a été mis à jour vers la version 2.0. Découvrez les nouvelles interfaces premium.', fullDate: '22 Avril 2026, 08:00', read: true }
])

const filteredNotifications = computed(() => {
  let list = notifications.value
  if (activeFilter.value === 'unread') list = list.filter(n => !n.read)
  else if (activeFilter.value === 'academic') list = list.filter(n => n.type === 'grade' || n.type === 'absence')
  else if (activeFilter.value === 'system') list = list.filter(n => n.type === 'security' || n.type === 'system')
  return list
})

const markAllAsRead = () => {
  notifications.value.forEach(n => n.read = true)
}
</script>

<style scoped>
.page-notifications { padding: clamp(1.5rem, 4vw, 4rem) 2rem; max-width: 1000px; margin: 0 auto; animation: slideUp 0.6s ease-out; }

@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 4rem; }
.page-header h1 { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 950; letter-spacing: -3px; line-height: 1; margin-bottom: 0.5rem; }
.page-header p { color: #64748b; font-weight: 600; font-size: 1.1rem; }

.notifications-container { background: #fff; overflow: hidden; }

.notif-filters { display: flex; gap: 1rem; padding: 1.5rem 2.5rem; border-bottom: 1px solid #f1f5f9; background: #fafafa; }
.filter-btn { padding: 0.6rem 1.5rem; border-radius: 50px; border: none; background: transparent; font-size: 0.8rem; font-weight: 900; color: #64748b; cursor: pointer; transition: all 0.2s; }
.filter-btn:hover { color: #000; }
.filter-btn.active { background: #000; color: #fff; }

.notif-full-list { display: flex; flex-direction: column; }

.notif-card { display: flex; gap: 2.5rem; padding: 3rem; border-bottom: 1px solid #f1f5f9; position: relative; transition: all 0.2s; }
.notif-card:hover { background: #fcfcfc; }
.notif-card.unread { background: #fff; }

.unread-status-line { position: absolute; left: 0; top: 0; bottom: 0; width: 6px; background: #000; }

.notif-icon-circle { width: 64px; height: 64px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; flex-shrink: 0; background: #fff; border: 3px solid #f1f5f9; }
.notif-icon-circle.grade { border-color: #000; }
.notif-icon-circle.absence { border-color: #f1f5f9; }
.notif-icon-circle.security { border-color: #000; background: #000; color: #fff; }

.notif-main-content { flex: 1; }
.notif-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; }
.notif-head h3 { font-size: 1.25rem; font-weight: 900; letter-spacing: -0.5px; }
.timestamp { font-size: 0.8rem; color: #94a3b8; font-weight: 700; }

.description { font-size: 1rem; line-height: 1.6; color: #475569; font-weight: 500; margin-bottom: 1.5rem; max-width: 700px; }

.notif-footer { display: flex; justify-content: space-between; align-items: center; }
.category { font-size: 0.65rem; font-weight: 900; color: #94a3b8; letter-spacing: 1.5px; background: #f8fafc; padding: 0.4rem 1rem; border-radius: 4px; }
.mark-read-link { background: transparent; border: none; color: #000; font-size: 0.8rem; font-weight: 900; text-decoration: underline; cursor: pointer; }

.empty-notif-state { padding: 8rem 2rem; text-align: center; }
.icon-empty { font-size: 4rem; margin-bottom: 2rem; opacity: 0.2; }
.empty-notif-state h3 { font-size: 1.5rem; font-weight: 900; margin-bottom: 0.5rem; }
.empty-notif-state p { color: #64748b; font-weight: 600; }

.btn { padding: 1.1rem 2.2rem; font-weight: 900; border: none; cursor: pointer; border-radius: 14px; transition: all 0.2s; }
.btn-pill { border-radius: 50px; }
.dark { background: #000; color: #fff; }

@media (max-width: 768px) {
  .notif-card { flex-direction: column; gap: 1.5rem; padding: 2rem; }
  .notif-head { flex-direction: column; gap: 0.5rem; }
}
</style>
