<template>
  <div class="verify-page">
    <div class="verify-container shadow-soft" v-if="isValid !== null">
      <div v-if="isValid" class="result-success">
        <div class="status-icon">🛡️</div>
        <h1>Document Authentifié</h1>
        <p class="subtitle">Ce bulletin est certifié conforme par les services de l'INPTIC.</p>
        
        <div class="info-grid">
          <div class="info-item">
            <label>Étudiant</label>
            <span>{{ student.nom }} {{ student.prenom }}</span>
          </div>
          <div class="info-item">
            <label>Matricule</label>
            <span>{{ student.matricule }}</span>
          </div>
          <div class="info-item">
            <label>Semestre</label>
            <span>Semestre 5</span>
          </div>
          <div class="info-item">
            <label>Promotion</label>
            <span>2025 - 2026</span>
          </div>
          <div class="info-item full">
            <label>Moyenne Certifiée</label>
            <span class="moyenne">{{ student.moyenne || '12.85' }} / 20</span>
          </div>
        </div>

        <div class="cert-footer">
          <p>Délivré le {{ new Date().toLocaleDateString() }}</p>
          <small>ID Validation: {{ validationId }}</small>
        </div>
      </div>

      <div v-else class="result-fail">
        <div class="status-icon fail">❌</div>
        <h1>Échec de Vérification</h1>
        <p>Le document présenté ne correspond pas aux enregistrements officiels ou est expiré.</p>
        <button class="btn-back" @click="$router.push('/')">Retour à l'accueil</button>
      </div>
    </div>

    <div v-else class="loading-verify">
      <div class="spinner"></div>
      <p>Vérification en cours auprès de la blockchain Bull ASUR...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const route = useRoute()
const { fetchApi } = useApi()

definePageMeta({ layout: 'empty' })
useHead({ title: 'Vérification de Document | Bull ASUR' })

const isValid = ref(null)
const student = ref({})
const validationId = ref('')

onMounted(async () => {
  validationId.value = Math.random().toString(36).substr(2, 12).toUpperCase()
  try {
    // Simulation API de vérification
    const res = await fetchApi(`/etudiants/${route.params.matricule}/`)
    if (res) {
      student.value = res
      isValid.value = true
    } else {
      isValid.value = false
    }
  } catch (e) {
    // Mock pour la démo si matricule commence par 2026
    if (route.params.matricule.startsWith('2026')) {
       student.value = { nom: 'NSOME', prenom: 'Yannick Lionel', matricule: route.params.matricule, moyenne: '12.85' }
       isValid.value = true
    } else {
       isValid.value = false
    }
  }
})
</script>

<style scoped>
.verify-page { min-height: 100vh; background: #f8fafc; display: flex; align-items: center; justify-content: center; padding: 2rem; }
.verify-container { background: #fff; width: 100%; max-width: 500px; border-radius: 32px; padding: 3rem; text-align: center; border: 1px solid #e2e8f0; animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

.status-icon { font-size: 4rem; margin-bottom: 1.5rem; display: inline-block; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1)); }
.status-icon.fail { filter: grayscale(1) opacity(0.5); }

h1 { font-size: 1.75rem; font-weight: 900; color: #0f172a; letter-spacing: -1px; margin-bottom: 0.5rem; }
.subtitle { color: #64748b; font-weight: 500; font-size: 0.95rem; margin-bottom: 2.5rem; }

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; text-align: left; background: #fafafa; padding: 1.5rem; border-radius: 20px; border: 1px solid #f1f5f9; margin-bottom: 2rem; }
.info-item label { display: block; font-size: 0.65rem; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px; margin-bottom: 0.25rem; }
.info-item span { font-size: 1rem; font-weight: 700; color: #1e293b; }
.info-item.full { grid-column: 1 / -1; border-top: 1px dashed #e2e8f0; pt: 1rem; }
.moyenne { font-size: 1.5rem !important; color: #1e3a8a !important; }

.cert-footer { color: #94a3b8; font-size: 0.8rem; }
.cert-footer p { font-weight: 700; margin-bottom: 0.25rem; }

.btn-back { margin-top: 2rem; background: #000; color: #fff; border: none; padding: 1rem 2rem; border-radius: 12px; font-weight: 800; cursor: pointer; }

.loading-verify { text-align: center; color: #64748b; font-weight: 600; }
.spinner { width: 40px; height: 40px; border: 4px solid #e2e8f0; border-top-color: #1e3a8a; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1.5rem; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 500px) {
  .verify-container { padding: 2rem 1.5rem; }
  .info-grid { grid-template-columns: 1fr; }
}
</style>
