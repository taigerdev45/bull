<script setup>
// Redirection immédiate vers l'accueil car le login a été unifié
onMounted(() => {
  const route = useRoute()
  const role = route.query.role
  const target = role ? `/?role=${role}` : '/'
  navigateTo(target)
})
</script>

<template>
  <div class="redirecting">
    Chargement...
  </div>
</template>

<style scoped>
.redirecting {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: black;
  color: white;
}
</style>
