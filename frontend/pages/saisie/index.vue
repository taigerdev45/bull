<template>
  <div class="page-saisie">
    <header class="page-header">
      <div class="header-content">
        <h2>Saisie des Notes et Absences</h2>
        <p>Semestre 5 - Anglais technique (UE5-1)</p>
      </div>
      <div class="header-actions">
        <!-- Selecteur de matière -->
        <select class="matiere-select" v-model="selectedMatiere" @change="onMatiereChange">
          <option v-for="matiere in availableMatieres" :key="matiere.id" :value="matiere.id">
            {{ matiere.libelle }}
          </option>
        </select>
        <button class="btn btn-primary" @click="saveGrades" :disabled="isSaving">
          <span v-if="!isSaving">Enregistrer les Notes</span>
          <span v-else>Enregistrement...</span>
        </button>
      </div>
    </header>

    <div class="table-container">
      <table class="grid-saisie">
        <thead>
          <tr>
            <th width="80">ID</th>
            <th>Étudiant</th>
            <th width="120" class="center">Note CC (40%)</th>
            <th width="120" class="center">Examen (60%)</th>
            <th width="120" class="center">Rattrapage</th>
            <th width="120" class="center">Absences (h)</th>
            <th width="120" class="center bg-gray">Moyenne (*)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="etudiant in etudiants" :key="etudiant.id" :class="{'is-failed': parseFloat(calculateMoyenne(etudiant)) < 10 && calculateMoyenne(etudiant) !== '-'}">
            <td>{{ etudiant.id }}</td>
            <td class="font-bold">{{ etudiant.nom }} {{ etudiant.prenom }}</td>
            <td class="center">
              <input type="number" min="0" max="20" step="0.25" v-model.number="etudiant.cc" class="grade-input" />
            </td>
            <td class="center">
              <input type="number" min="0" max="20" step="0.25" v-model.number="etudiant.exam" class="grade-input" />
            </td>
            <td class="center">
              <input 
                type="number" 
                min="0" max="20" step="0.25" 
                v-model.number="etudiant.ratrap" 
                class="grade-input" 
                :disabled="!isRattrapageEligible(etudiant)"
                :title="!isRattrapageEligible(etudiant) ? 'Rattrapage non autorisé (moyenne >= 10)' : ''"
              />
            </td>
            <td class="center">
              <input 
                type="number" 
                min="0" 
                v-model.number="etudiant.absences" 
                class="grade-input abscence" 
                :disabled="isEnseignant"
                :title="isEnseignant ? 'La gestion des absences relève du secrétariat' : ''"
              />
            </td>
            <td class="center bg-gray font-bold value-cell">
              {{ calculateMoyenne(etudiant) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useApi } from '~/composables/useApi'

useHead({
  title: 'Saisie | Bull ASUR'
})

const { fetchApi } = useApi()
const authRole = useCookie('authRole', { default: () => 'etudiant' })
const isEnseignant = computed(() => authRole.value === 'enseignant')

const selectedMatiere = ref('')
const availableMatieres = ref([])
const etudiants = ref([])
const isSaving = ref(false)

const loadInitialData = async () => {
  try {
    // 1. Charger les matières
    const matieresData = await fetchApi('/matieres/')
    availableMatieres.value = matieresData || []
    
    if (availableMatieres.value.length > 0 && !selectedMatiere.value) {
      selectedMatiere.value = availableMatieres.value[0].id
    }

    if (!selectedMatiere.value) return

    // 2. Charger les étudiants
    const studentsData = await fetchApi('/etudiants/')
    
    // 3. Charger les notes existantes pour cette matière
    const evaluationsData = await fetchApi(`/evaluations/matiere/${selectedMatiere.value}/`)
    
    etudiants.value = studentsData.map(student => {
      // Filtrer les notes de cet étudiant
      const notes = evaluationsData.filter(n => n.etudiant_id === student.id || n.etudiant === student.id)
      const cc = notes.find(n => n.type === 'CC')?.note ?? null
      const exam = notes.find(n => n.type === 'Examen')?.note ?? null
      const ratrap = notes.find(n => n.type === 'Rattrapage')?.note ?? null
      
      return {
        id: student.id,
        nom: student.nom,
        prenom: student.prenom,
        cc,
        exam,
        ratrap,
        absences: 0 // À lier au service d'absences plus tard
      }
    })
  } catch (error) {
    console.error('Erreur chargement données:', error)
  }
}

onMounted(() => {
  loadInitialData()
})

const onMatiereChange = () => {
  loadInitialData()
}

const calculateMoyenne = (etudiant) => {
  const cc = parseFloat(etudiant.cc)
  const exam = parseFloat(etudiant.exam)
  const ratrap = parseFloat(etudiant.ratrap)

  if (isNaN(cc) && isNaN(exam)) return '-'

  let baseMoyenne = 0
  if (!isNaN(cc) && !isNaN(exam)) {
    baseMoyenne = (cc * 0.4) + (exam * 0.6)
  } else if (!isNaN(cc)) {
    baseMoyenne = cc * 0.4
  } else if (!isNaN(exam)) {
    baseMoyenne = exam * 0.6
  }

  // Si rattrapage, on prend le max entre la moyenne initiale et le rattrapage
  if (!isNaN(ratrap)) {
    return Math.max(baseMoyenne, ratrap).toFixed(2)
  }

  return baseMoyenne.toFixed(2)
}

const isRattrapageEligible = (etudiant) => {
  const moy = calculateMoyenne(etudiant)
  if (moy === '-') return false
  return parseFloat(moy) < 10
}

const saveGrades = async () => {
  try {
    isSaving.value = true;
    const payload = [];
    
    etudiants.value.forEach(etudiant => {
      if (etudiant.cc !== null && etudiant.cc !== '') {
        payload.push({ etudiant_id: etudiant.id, matiere_id: selectedMatiere.value, type: "CC", note: Number(etudiant.cc) });
      }
      if (etudiant.exam !== null && etudiant.exam !== '') {
        payload.push({ etudiant_id: etudiant.id, matiere_id: selectedMatiere.value, type: "Examen", note: Number(etudiant.exam) });
      }
      if (etudiant.ratrap !== null && etudiant.ratrap !== '') {
        payload.push({ etudiant_id: etudiant.id, matiere_id: selectedMatiere.value, type: "Rattrapage", note: Number(etudiant.ratrap) });
      }
    });

    await fetchApi('/evaluations/bulk/', {
      method: 'POST',
      body: payload
    })

    alert('Notes enregistrées avec succès !');
    await loadInitialData(); // Recharger pour confirmer
  } catch (error) {
    console.error(error);
    alert('Erreur lors de l\'enregistrement des notes : ' + (error.data?.error || 'Erreur inconnue'));
  } finally {
    isSaving.value = false;
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
}

.header-content h2 {
  font-size: 1.75rem;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.header-content p {
  color: var(--text-muted);
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.matiere-select {
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background-color: var(--surface);
  font-size: 0.95rem;
  outline: none;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.6rem 1.25rem;
  border-radius: var(--radius);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
}

.btn-primary:hover {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
}

.table-container {
  background-color: var(--surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow-x: auto;
}

.grid-saisie {
  width: 100%;
  border-collapse: collapse;
}

.grid-saisie th, .grid-saisie td {
  padding: 0.8rem 1rem;
  border-bottom: 1px solid var(--border);
  border-right: 1px solid var(--border);
}

.grid-saisie th:last-child, .grid-saisie td:last-child {
  border-right: none;
}

.grid-saisie th {
  background-color: #f8fafc;
  color: var(--text-muted);
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
}

.grid-saisie tbody tr {
  transition: background-color 0.2s;
}

.grid-saisie tbody tr:hover {
  background-color: #f1f5f9;
}

.grid-saisie tbody tr.is-failed .value-cell {
  color: var(--danger);
}

.center {
  text-align: center;
}

.bg-gray {
  background-color: #f8fafc;
}

.font-bold {
  font-weight: 600;
  color: var(--text-main);
}

.grade-input {
  width: 70px;
  text-align: center;
  padding: 0.4rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.grade-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.grade-input.abscence {
  width: 60px;
}
</style>
