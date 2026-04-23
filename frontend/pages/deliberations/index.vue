<template>
  <div class="page-deliberations">
    <header class="page-header">
      <div class="header-info">
        <h1>Procès-Verbaux & Délibérations</h1>
        <p>Validation collective des résultats par promotion et par semestre.</p>
      </div>
      <div class="header-actions">
        <div class="semester-selector">
          <button 
            v-for="s in [5, 6]" 
            :key="s" 
            class="sem-btn" 
            :class="{ active: selectedSemestre === s }"
            @click="changeSemestre(s)"
          >
            S{{ s }}
          </button>
        </div>
        <button class="btn btn-primary" @click="fetchStats" :disabled="isLoading">
          <span v-if="isLoading" class="loader-sm"></span>
          <span v-else>🔄</span> Actualiser les données
        </button>
      </div>
    </header>

    <div class="stats-overview">
      <div class="stat-card">
        <div class="stat-icon success">🎓</div>
        <div class="stat-details">
          <span class="label">Taux de Réussite</span>
          <span class="value success">{{ stats.taux_reussite?.toFixed(1) }}%</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon info">📊</div>
        <div class="stat-details">
          <span class="label">Moyenne Générale</span>
          <span class="value">{{ stats.moyenne_classe?.toFixed(2) }}</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon warning">👥</div>
        <div class="stat-details">
          <span class="label">Effectif Total</span>
          <span class="value">{{ stats.resultats?.length || 0 }}</span>
        </div>
      </div>
    </div>

    <div class="pv-card">
      <div class="card-header">
        <h3>Registre de Délibération - Semestre {{ selectedSemestre }}</h3>
        <div class="search-bar">
          <input type="text" v-model="searchQuery" placeholder="Rechercher un étudiant..." />
        </div>
      </div>

      <div class="table-container" v-if="!isLoading">
        <table class="modern-table">
          <thead>
            <tr>
              <th>Matricule</th>
              <th>Nom & Prénom</th>
              <th class="center">Moyenne</th>
              <th class="center">Crédits Acquis</th>
              <th class="center">Décision Jury</th>
              <th class="center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="res in filteredResults" :key="res.id">
              <td><span class="matricule-tag">{{ res.id }}</span></td>
              <td><strong>{{ res.nom }}</strong> {{ res.prenom }}</td>
              <td class="center">
                <span :class="['moy-val', res.moyS5 >= 10 ? 'text-success' : 'text-danger']">
                  {{ res.moyS5?.toFixed(2) }}
                </span>
              </td>
              <td class="center">
                <div class="credits-badge">{{ res.credits }} / 30</div>
              </td>
              <td class="center">
                <span :class="['status-pill', res.decision === 'Validé' ? 'valid' : 'fail']">
                  {{ res.decision }}
                </span>
              </td>
              <td class="center">
                <button class="btn-icon" title="Voir Bulletin" @click="viewBulletin(res.id)">📄</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-else class="table-loading">
        <div class="shimmer-row" v-for="i in 5" :key="i"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
const { fetchApi } = useApi()
const selectedSemestre = ref(5)
const isLoading = ref(false)
const searchQuery = ref('')
const stats = ref({
  resultats: [],
  moyenne_classe: 0,
  taux_reussite: 0
})

const changeSemestre = (s) => {
  selectedSemestre.value = s
  fetchStats()
}

const fetchStats = async () => {
  isLoading.value = true
  try {
    const data = await fetchApi('/resultats/promotion/stats/', {
      params: { 
        semestre: selectedSemestre.value,
        promo_id: 'LP_ASUR_2026' // Valeur par défaut pour l'instant
      }
    })
    if (data) stats.value = data
  } catch (error) {
    console.error('Erreur stats deliberations:', error)
  } finally {
    isLoading.value = false
  }
}

const filteredResults = computed(() => {
  if (!searchQuery.value) return stats.value.resultats
  const q = searchQuery.value.toLowerCase()
  return stats.value.resultats.filter(r => 
    r.nom.toLowerCase().includes(q) || 
    r.prenom.toLowerCase().includes(q) || 
    r.id.toLowerCase().includes(q)
  )
})

const viewBulletin = (studentId) => {
  navigateTo(`/bulletins?student=${studentId}&semestre=S${selectedSemestre.value}`)
}

onMounted(fetchStats)
</script>

<style scoped>
.page-deliberations {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header-info h1 {
  font-size: 2rem;
  font-weight: 800;
  color: #0c1b33;
  margin: 0;
  letter-spacing: -0.02em;
}

.header-info p {
  color: #64748b;
  margin-top: 0.25rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.semester-selector {
  display: flex;
  background: #f1f5f9;
  padding: 4px;
  border-radius: 12px;
}

.sem-btn {
  padding: 0.5rem 1.25rem;
  border: none;
  background: transparent;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  color: #64748b;
}

.sem-btn.active {
  background: white;
  color: #000080;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  border: 1px solid #f1f5f9;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-icon.success { background: #ecfdf5; }
.stat-icon.info { background: #eff6ff; }
.stat-icon.warning { background: #fffbeb; }

.stat-details {
  display: flex;
  flex-direction: column;
}

.stat-details .label {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
}

.stat-details .value {
  font-size: 1.5rem;
  font-weight: 800;
  color: #0f172a;
}

.value.success { color: #10b981; }

.pv-card {
  background: white;
  border-radius: 1.5rem;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  border: 1px solid #f1f5f9;
  overflow: hidden;
}

.card-header {
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f1f5f9;
}

.card-header h3 {
  margin: 0;
  font-weight: 700;
  color: #0c1b33;
}

.search-bar input {
  padding: 0.6rem 1rem;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  width: 250px;
  font-size: 0.9rem;
}

.table-container {
  overflow-x: auto;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
}

.modern-table th {
  text-align: left;
  padding: 1rem 2rem;
  background: #f8fafc;
  color: #64748b;
  font-size: 0.75rem;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.modern-table td {
  padding: 1.25rem 2rem;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
  font-size: 0.95rem;
}

.center { text-align: center !important; }

.matricule-tag {
  background: #f1f5f9;
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
  font-family: monospace;
  font-weight: 700;
  font-size: 0.85rem;
}

.moy-val {
  font-weight: 800;
  font-size: 1.1rem;
}

.credits-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #f0f4ff;
  color: #000080;
  border-radius: 99px;
  font-weight: 700;
  font-size: 0.8rem;
}

.status-pill {
  padding: 0.4rem 1rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
}

.status-pill.valid { background: #dcfce7; color: #15803d; }
.status-pill.fail { background: #fee2e2; color: #b91c1c; }

.btn-icon {
  background: #f1f5f9;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: #e2e8f0;
  transform: scale(1.1);
}

.text-success { color: #10b981; }
.text-danger { color: #ef4444; }

.btn-primary {
  background: #000080;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
}

.btn-primary:hover {
  background: #0000a0;
  box-shadow: 0 8px 15px rgba(0,0,128,0.2);
}

.loader-sm {
  width: 16px;
  height: 16px;
  border: 2px solid white;
  border-bottom-color: transparent;
  border-radius: 50%;
  display: inline-block;
  animation: rotation 1s linear infinite;
}

@keyframes rotation {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.shimmer-row {
  height: 60px;
  margin: 1rem 2rem;
  background: linear-gradient(90deg, #f1f5f9 25%, #f8fafc 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 12px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
