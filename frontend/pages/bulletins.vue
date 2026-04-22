<template>
  <div class="page-bulletins-index">
    <div class="loading-content">
      <div class="loading-spinner"></div>
      <p>Redirection vers la page des bulletins...</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { navigateTo } from '#app'

useHead({ title: 'Bulletins | Bull ASUR' })

onMounted(() => {
  // Récupérer le rôle depuis le cookie
  const role = useCookie('authRole', { default: () => 'etudiant' })
  
  // Rediriger selon le rôle
  switch (role.value) {
    case 'secretariat':
      navigateTo('/secretariat/bulletins')
      break
    case 'admin':
      navigateTo('/secretariat/bulletins')
      break
    case 'enseignant':
      navigateTo('/enseignant/bulletins')
      break
    case 'etudiant':
      navigateTo('/etudiant/bulletins')
      break
    default:
      navigateTo('/etudiant/bulletins')
  }
})
</script>

<style scoped>
.page-bulletins-index {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
  flex-direction: column;
}

.loading-content {
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border);
  border-top: 4px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-content p {
  color: var(--text-muted);
  font-size: 1rem;
}
</style>
