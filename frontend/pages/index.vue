<template>
  <div class="landing-page">
    <div class="overlay"></div>
    <div class="content-wrapper">
      <header class="landing-header">
        <h1>Bienvenue sur Bull ASUR</h1>
        <p>Le portail de gestion des bulletins de notes <strong>DAR 3</strong></p>
      </header>

      <div class="roles-grid">
        <NuxtLink to="/login?role=etudiant" class="role-card etudiant-theme">
          <h2>Espace Étudiant</h2>
          <p>Consultez vos notes officielles.</p>
        </NuxtLink>

        <NuxtLink to="/login?role=enseignant" class="role-card enseignant-theme">
          <h2>Espace Enseignant</h2>
          <p>Gerez vos evaluations simplement.</p>
        </NuxtLink>

        <NuxtLink to="/login?role=secretariat" class="role-card secretariat-theme">
          <h2>Secrétariat Pédagogique</h2>
          <p>Gestion administrative de l'ensemble du personnel.</p>
        </NuxtLink>

        <NuxtLink to="/login?role=admin" class="role-card admin-theme">
          <h2>Administrateur</h2>
          <p>Management système.</p>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'empty'
})

useHead({
  title: 'Accueil | Bull ASUR'
})
</script>

<style scoped>
.landing-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Image en arrière-plan */
  background-image: url('~/assets/images/acceuil_bull.jpeg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.7); /* Couche sombre pour lisibilité */
  z-index: 1;
}

.content-wrapper {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1200px;
  padding: 2rem;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.landing-header {
  text-align: center;
  margin-bottom: 4rem;
}

.landing-header h1 {
  font-size: 3.5rem;
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 1rem;
  text-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.landing-header p {
  font-size: 1.25rem;
  font-weight: 300;
  color: rgba(255,255,255,0.9);
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
  width: 100%;
}

.role-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-bottom: 4px solid transparent;
  border-radius: 1rem;
  padding: 2.5rem 2rem;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: white;
}

.role-card:hover {
  transform: translateY(-8px);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.3);
}

/* Thèmes par couleur selon le rôle */
.etudiant-theme { border-bottom-color: #3b82f6; }
.enseignant-theme { border-bottom-color: #10b981; }
.secretariat-theme { border-bottom-color: #8b5cf6; }
.admin-theme { border-bottom-color: #f59e0b; }

.role-card h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.role-card p {
  font-size: 0.95rem;
  line-height: 1.6;
  opacity: 0.85;
}

@media (max-width: 768px) {
  .landing-header h1 { font-size: 2.5rem; }
  .landing-header p { font-size: 1rem; }
  .roles-grid { grid-template-columns: 1fr; }
}
</style>
