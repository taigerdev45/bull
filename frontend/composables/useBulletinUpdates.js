export const useBulletinUpdates = () => {
  const { $fetch } = useNuxtApp()
  
  // Mettre à jour tous les bulletins lors d'une modification structurelle
  const updateBulletinsOnStructuralChange = async (changeType, changedItem) => {
    try {
      console.log(`Mise à jour automatique des bulletins suite à: ${changeType}`)
      
      // Appel à l'API pour mettre à jour tous les bulletins
      const response = await $fetch('/api/bulletins/update-on-structural-change', {
        method: 'POST',
        body: {
          change_type: changeType,
          changed_item: changedItem,
          timestamp: new Date().toISOString()
        }
      })
      
      // Afficher une notification de succès
      showNotification(
        `Mise à jour automatique des bulletins terminée`,
        `${response.updated_count} bulletin(s) mis à jour`,
        'success'
      )
      
      return response
    } catch (error) {
      console.error('Erreur lors de la mise à jour automatique des bulletins:', error)
      
      // Afficher une notification d'erreur
      showNotification(
        'Erreur de synchronisation',
        'La mise à jour automatique des bulletins a échoué',
        'error'
      )
      
      throw error
    }
  }
  
  // Mettre à jour un bulletin spécifique lors d'une modification individuelle
  const updateSingleBulletin = async (etudiantId, changeType, changedData) => {
    try {
      console.log(`Mise à jour du bulletin de l'étudiant ${etudiantId} suite à: ${changeType}`)
      
      const response = await $fetch(`/api/bulletins/${etudiantId}/update`, {
        method: 'POST',
        body: {
          change_type: changeType,
          changed_data: changedData,
          timestamp: new Date().toISOString()
        }
      })
      
      showNotification(
        'Bulletin mis à jour',
        `Le bulletin a été recalculé automatiquement`,
        'success'
      )
      
      return response
    } catch (error) {
      console.error('Erreur lors de la mise à jour du bulletin:', error)
      showNotification(
        'Erreur de mise à jour',
        'Le bulletin n\'a pas pu être mis à jour automatiquement',
        'error'
      )
      throw error
    }
  }
  
  // Calculer les statistiques de mise à jour
  const calculateUpdateStats = async () => {
    try {
      const response = await $fetch('/api/bulletins/update-stats')
      return response
    } catch (error) {
      console.error('Erreur lors du calcul des statistiques:', error)
      return null
    }
  }
  
  // Vérifier l'état de synchronisation des bulletins
  const checkSyncStatus = async () => {
    try {
      const response = await $fetch('/api/bulletins/sync-status')
      return response
    } catch (error) {
      console.error('Erreur lors de la vérification du statut de synchronisation:', error)
      return null
    }
  }
  
  // Forcer la synchronisation manuelle de tous les bulletins
  const forceSyncAllBulletins = async () => {
    try {
      const response = await $fetch('/api/bulletins/force-sync', {
        method: 'POST'
      })
      
      showNotification(
        'Synchronisation forcée',
        `${response.updated_count} bulletin(s) synchronisé(s)`,
        'success'
      )
      
      return response
    } catch (error) {
      console.error('Erreur lors de la synchronisation forcée:', error)
      showNotification(
        'Erreur de synchronisation',
        'La synchronisation forcée a échoué',
        'error'
      )
      throw error
    }
  }
  
  // Système de notification simple
  const showNotification = (title, message, type = 'info') => {
    // Créer un événement personnalisé pour les notifications
    const event = new CustomEvent('show-notification', {
      detail: { title, message, type }
    })
    window.dispatchEvent(event)
    
    // Fallback console
    console.log(`[${type.toUpperCase()}] ${title}: ${message}`)
  }
  
  return {
    updateBulletinsOnStructuralChange,
    updateSingleBulletin,
    calculateUpdateStats,
    checkSyncStatus,
    forceSyncAllBulletins
  }
}
