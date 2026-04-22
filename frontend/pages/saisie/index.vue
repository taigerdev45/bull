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

const { apiFetch } = useApi()
const authRole = useCookie('authRole', { default: () => 'etudiant' })
const isEnseignant = computed(() => authRole.value === 'enseignant')

const selectedMatiere = ref('M1') // M1 correspond à 'Architecture Réseaux' dans le mock
const availableMatieres = ref([])
const etudiants = ref([])
const isSaving = ref(false)

const loadInitialData = async () => {
  try {
    const { useMockDb } = await import('~/composables/useMockDb.js')
    const db = useMockDb()
    
    // Charger les matières
    availableMatieres.value = db.getCollection('matieres')
    if (availableMatieres.value.length > 0 && !availableMatieres.value.find(m => m.id === selectedMatiere.value)) {
      selectedMatiere.value = availableMatieres.value[0].id
    }

    // Charger les étudiants et leurs notes
    const allStudents = db.getCollection('etudiants')
    const allNotes = db.getCollection('notes')
    
    etudiants.value = allStudents.map(student => {
      // Trouver les notes de cet étudiant pour la matière sélectionnée
      const notes = allNotes.filter(n => n.etudiant_id === student.id && n.matiere_id === selectedMatiere.value)
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
        absences: 0 // Simplifié pour le mock
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
  loadInitialData() // Recharger les notes quand la matière change
}

const isRattrapageEligible = (etudiant) => {
  const cc = etudiant.cc !== null && etudiant.cc !== '' ? Number(etudiant.cc) : null;
  const ex = etudiant.exam !== null && etudiant.exam !== '' ? Number(etudiant.exam) : null;
  if (cc === null || ex === null) return true; // S'il manque une note, rattrapage ouvert
  return (cc * 0.4 + ex * 0.6) < 10; // Ouvert si la note est inférieure à 10
}

const calculateMoyenne = (etudiant) => {
  let cc = etudiant.cc !== null && etudiant.cc !== '' ? Number(etudiant.cc) : null;
  let ex = etudiant.exam !== null && etudiant.exam !== '' ? Number(etudiant.exam) : null;
  let rat = etudiant.ratrap !== null && etudiant.ratrap !== '' ? Number(etudiant.ratrap) : null;

  // Force le nettoyage du rattrapage si l'étudiant a >= 10
  if (!isRattrapageEligible(etudiant)) {
    rat = null;
  }
  
  let baseMoyenne = null;
  
  if (rat !== null) {
    if (cc === null && ex !== null) {
      baseMoyenne = (rat * 0.4) + (ex * 0.6); // Le rattrapage remplace le CC
    } else if (ex === null && cc !== null) {
      baseMoyenne = (cc * 0.4) + (rat * 0.6); // Le rattrapage remplace l'Examen
    } else if (cc !== null && ex !== null) {
      // Les 3 notes sont présentes : on conserve les 2 meilleures
      let finalCC = cc;
      let finalEx = ex;
      
      if (rat > Math.min(cc, ex)) {
        if (cc < ex) {
          finalCC = rat; // Le rattrapage remplace le CC
        } else {
          finalEx = rat; // Le rattrapage remplace l'Exam
        }
      }
      baseMoyenne = (finalCC * 0.4) + (finalEx * 0.6);
    } else {
      baseMoyenne = rat; // Seulement le rattrapage
    }
  } else {
    // Calcul normal
    if (cc !== null && ex !== null) {
      baseMoyenne = (cc * 0.4) + (ex * 0.6);
    } else if (cc !== null) {
      baseMoyenne = cc;
    } else if (ex !== null) {
      baseMoyenne = ex;
    }
  }

  if (baseMoyenne !== null) {
    const absenceMalus = (etudiant.absences || 0) * 0.01;
    let finalGrade = baseMoyenne - absenceMalus;
    return Math.max(0, finalGrade).toFixed(2);
  }
  
  return '-';
}

const saveGrades = async () => {
  try {
    isSaving.value = true;
    
    const { useMockDb } = await import('~/composables/useMockDb.js')
    const db = useMockDb()
    let allNotes = db.getCollection('notes')
    
    // Formatage des objets pour POST /api/evaluations/bulk/ et MockDB
    const payload = [];
    
    // Nettoyer les anciennes notes pour cette matière
    allNotes = allNotes.filter(n => n.matiere_id !== selectedMatiere.value)

    etudiants.value.forEach(etudiant => {
      if (etudiant.cc !== null && etudiant.cc !== '') {
        const note = { etudiant_id: etudiant.id, matiere_id: selectedMatiere.value, type: "CC", note: Number(etudiant.cc), id: Math.random().toString(36).substring(2, 9) }
        payload.push(note);
        allNotes.push(note);
      }
      if (etudiant.exam !== null && etudiant.exam !== '') {
        const note = { etudiant_id: etudiant.id, matiere_id: selectedMatiere.value, type: "Examen", note: Number(etudiant.exam), id: Math.random().toString(36).substring(2, 9) }
        payload.push(note);
        allNotes.push(note);
      }
      if (etudiant.ratrap !== null && etudiant.ratrap !== '') {
        const note = { etudiant_id: etudiant.id, matiere_id: selectedMatiere.value, type: "Rattrapage", note: Number(etudiant.ratrap), id: Math.random().toString(36).substring(2, 9) }
        payload.push(note);
        allNotes.push(note);
      }
    });

    console.log('Simulation POST vers /api/evaluations/bulk/ avec ce payload:', payload);

    // Sauvegarde dans la fausse BDD
    db.setCollection('notes', allNotes)

    setTimeout(() => {
      isSaving.value = false;
      alert('Notes enregistrées avec succès dans la base de données locale !');
    }, 800);

  } catch (error) {
    console.error(error);
    isSaving.value = false;
    alert('Erreur lors de l\'enregistrement des notes.');
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
