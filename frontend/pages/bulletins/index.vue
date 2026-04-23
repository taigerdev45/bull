<template>
  <div class="page-bulletins">
    <header class="page-header no-print">
      <div class="header-content">
        <h2>Bulletins Individuels</h2>
        <div class="header-subtitle">
          <span class="dot"></span>
          <p>Modèle officiel INPTIC A4</p>
        </div>
      </div>
      <div class="toggle-container">
        <!-- Toolbar Secrétariat -->
        <div v-if="!isEtudiant" class="admin-toolbar no-print">
          <button class="tool-btn" :class="{ active: editMode === null }" @click="editMode = null">👁️ Vue</button>
          <button class="tool-btn" :class="{ active: editMode === 'structure' }" @click="editMode = 'structure'">🏗️ Structure</button>
          <button class="tool-btn" :class="{ active: editMode === 'data' }" @click="editMode = 'data'">📝 Saisie</button>
        </div>
        
        <div class="toggle-group">
          <button 
            v-for="sem in ['S5', 'S6', 'Annuel']" 
            :key="sem"
            class="toggle-btn"
            :class="{ active: selectedSemester === sem }"
            @click="selectedSemester = sem"
          >
            {{ sem === 'Annuel' ? 'Annuel' : 'Semestre ' + sem.substring(1) }}
          </button>
          <div class="toggle-slider" :class="'pos-' + selectedSemester"></div>
        </div>
      </div>
    </header>

    <div class="content-wrapper">
      <div class="students-list no-print" v-if="!isEtudiant">
        <h3>Liste d'Étudiants </h3>
        <div v-if="isDataLoading" class="mini-loader">Chargement...</div>
        <ul v-else>
          <li v-for="student in etudiantsList" :key="student.id" :class="{ active: selectedStudent === student.id }" @click="selectStudent(student.id)">
            {{ student.nom }} {{ student.prenom }}
          </li>
        </ul>
      </div>

      <div class="bulletin-preview" v-if="selectedStudent">
        <!-- Feuille A4 Portrait -->
        <div class="a4-sheet" id="printableArea">
          
          <!-- En-têtes République & INPTIC -->
          <div class="top-header">
            <div class="left-header">
              <p>INSTITUT NATIONAL DE LA POSTE, DES TECHNOLOGIES</p>
              <p>DE L'INFORMATION ET DE LA COMMUNICATION</p>
              <p class="subtitle mt-1">DIRECTION DES ETUDES ET DE LA PEDAGOGIE</p>
            </div>
            <div class="center-header">
              <h1 class="main-title">Bulletin de notes {{ selectedSemester === 'Annuel' ? 'Annuel' : 'du ' + selectedSemester }}</h1>
              <p class="annee-univ">Année universitaire : 2025/2026</p>
            </div>
            <div class="right-header">
              <p>RÉPUBLIQUE GABONAISE</p>
              <p>-------------</p>
              <p>Union - Travail - Justice</p>
              <p>-------------</p>
              <img src="~/assets/images/logo_inptic.png" alt="Logo INPTIC" class="logo-inptic-img" />
            </div>
          </div>

          <!-- Bloc Classe (Double bordure) -->
          <div class="class-block">
             <strong>Classe :</strong> Licence Professionnelle Réseaux et Télécommunications <strong>Option Administration et Sécurité des Réseaux (ASUR)</strong>
          </div>

          <!-- Bloc Info Étudiant -->
          <div class="student-info-block mt-2">
            <div class="info-row">
              <div class="label-col">Nom(s) et Prénom(s)</div>
              <div class="val-col font-bold">{{ studentInfo?.nom }} {{ studentInfo?.prenom }}</div>
            </div>
            <div class="info-row">
              <div class="label-col">Date et lieu de naissance</div>
              <div class="val-col">Né(e) le {{ studentInfo?.date_naissance }} à {{ studentInfo?.lieu_naissance || 'Libreville' }}</div>
            </div>
          </div>

          <!-- MODÈLE SEMESTRIEL (S5 / S6) -->
          <template v-if="selectedSemester !== 'Annuel'">
            <table class="grades-table mt-4">
              <thead>
                <tr>
                  <th></th>
                  <th width="60" class="center">Crédits</th>
                  <th width="80" class="center">Coefficients</th>
                  <th width="110" class="center">Notes de l'étudiant</th>
                  <th width="110" class="center">Moyenne de classe</th>
                </tr>
              </thead>
              <tbody>
                <template v-for="ue in bulletinData?.ues" :key="ue.id">
                  <tr class="ue-header">
                    <td colspan="5">
                      <div class="flex-between">
                        <span>{{ ue.id }} : {{ ue.libelle }}</span>
                        <div v-if="editMode === 'structure'" class="ue-tools no-print">
                          <button class="icon-btn" @click="editUE(ue)">✏️</button>
                          <button class="icon-btn" @click="addMatiere(ue)">➕</button>
                        </div>
                      </div>
                    </td>
                  </tr>
                  <tr v-for="matiere in ue.matieres" :key="matiere.libelle">
                    <td class="matiere">
                      {{ matiere.libelle }}
                      <button v-if="editMode === 'structure'" class="icon-btn no-print" @click="editMatiere(ue, matiere)">✏️</button>
                    </td>
                    <td class="center">{{ matiere.credits || '--' }}</td>
                    <td class="center">{{ matiere.coeff || '1.00' }}</td>
                    <td class="center text-blue font-bold">{{ matiere.moyenne?.toFixed(2) }}</td>
                    <td class="center">{{ matiere.moyenne_classe?.toFixed(2) || '--' }}</td>
                  </tr>
                  <tr class="ue-moyenne font-bold">
                    <td class="right">Moyenne {{ ue.id }}</td>
                    <td class="center">{{ ue.total_credits_ue || '--' }}</td>
                    <td class="center">--</td>
                    <td class="center text-blue">{{ ue.moyenne_ue?.toFixed(2) }}</td>
                    <td class="center">--</td>
                  </tr>
                </template>

                <tr class="penalties-row">
                  <td class="matiere">Pénalités d'absences</td>
                  <td colspan="2" class="center text-orange font-bold">0,01/heure</td>
                  <td class="center">
                    <div v-if="editMode === 'data'" class="absence-input-wrap">
                      <input type="number" v-model="bulletinData.absences" class="abs-field" @change="saveAbsence" />
                    </div>
                    <span v-else>{{ bulletinData?.absences || 0 }} heure(s)</span>
                  </td>
                  <td></td>
                </tr>
                
                <!-- Total Semestre -->
                <tr class="semester-total-row">
                  <td colspan="3" class="right font-bold">Moyenne {{ selectedSemester }}</td>
                  <td class="center font-bold text-blue bg-light">{{ bulletinData?.moyenne_generale?.toFixed(2) }}</td>
                  <td class="center">{{ bulletinData?.moyenne_classe_generale || '11.80' }}</td>
                </tr>
              </tbody>
            </table>

            <!-- Rang & Mention (Table 2x2) -->
            <div class="rank-mention-block mt-2">
              <table class="simple-table center-table">
                <tbody>
                  <tr>
                    <td width="50%">Rang de l'étudiant au Semestre</td>
                    <td>Mention</td>
                  </tr>
                  <tr class="font-bold">
                    <td>{{ bulletinData?.rang || 'Non classé' }}</td>
                    <td>{{ bulletinData?.mention || 'Passable' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Validation des crédits (Semestre) -->
            <div class="validation-block mt-4">
              <h4 class="text-center font-bold mb-1">Etat de la Validation des Crédits au {{ selectedSemester }}</h4>
              <table class="validation-table">
                <tbody>
                  <tr>
                    <td v-for="ue in bulletinData?.ues" :key="ue.id" class="center">{{ ue.id }}</td>
                    <td class="center">Crédits validés au {{ selectedSemester }}</td>
                  </tr>
                  <tr>
                    <td v-for="ue in bulletinData?.ues" :key="ue.id" class="center">
                      {{ ue.credits_acquis }} Crédits / {{ ue.total_credits_ue }}
                    </td>
                    <td class="center">{{ bulletinData?.credits_acquis }} Crédits / {{ bulletinData?.total_credits || 30 }}</td>
                  </tr>
                  <tr>
                    <td :colspan="(bulletinData?.ues?.length || 0)" class="center text-blue font-bold">
                      {{ bulletinData?.validation_commentaire || 'Semestre Acquis' }}
                    </td>
                    <td class="center text-blue font-bold">{{ bulletinData?.valide ? 'Semestre Acquis' : 'NON VALIDE' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>

          <!-- MODÈLE ANNUEL -->
          <template v-else>
            <table class="grades-table mt-4">
              <thead>
                <tr>
                  <th></th>
                  <th width="80" class="center">Coefficients</th>
                  <th width="100" class="center">Notes</th>
                  <th width="80" class="center">Rang</th>
                  <th width="110" class="center">Moyenne de classe</th>
                </tr>
              </thead>
              <tbody>
                <template v-for="ue in bulletinData?.ues_annuel" :key="ue.id">
                  <tr class="ue-header-annual">
                    <td colspan="5">{{ ue.id }} : {{ ue.libelle }}</td>
                  </tr>
                  <tr>
                    <td class="matiere pl-4">Semestre 1</td>
                    <td class="center">{{ ue.coeff_s1 || '--' }}</td>
                    <td class="center">{{ ue.note_s1 || '--' }}</td>
                    <td class="center">{{ ue.rang_s1 || '--' }}</td>
                    <td class="center">{{ ue.moy_classe_s1 || '--' }}</td>
                  </tr>
                  <tr>
                    <td class="matiere pl-4">Semestre 2</td>
                    <td class="center">{{ ue.coeff_s2 || '--' }}</td>
                    <td class="center">{{ ue.note_s2 || '--' }}</td>
                    <td class="center">{{ ue.rang_s2 || '--' }}</td>
                    <td class="center">{{ ue.moy_classe_s2 || '--' }}</td>
                  </tr>
                  <tr class="annual-row font-bold">
                    <td class="matiere pl-4">Annuel</td>
                    <td class="center">{{ ue.coeff_annuel || '--' }}</td>
                    <td class="center text-blue">{{ ue.note_annuel || '--' }}</td>
                    <td class="center">{{ ue.rang_annuel || '--' }}</td>
                    <td class="center">{{ ue.moy_classe_annuel || '--' }}</td>
                  </tr>
                </template>

                <!-- Ligne de Moyenne Annuelle Totale -->
                <tr class="ue-header-annual">
                  <td colspan="5">Moyenne Annuelle</td>
                </tr>
                <tr class="font-bold">
                  <td class="pl-4">Annuel</td>
                  <td class="center">{{ bulletinData?.total_coeff_annuel || '--' }}</td>
                  <td class="center text-blue">{{ bulletinData?.moyenne_annuelle?.toFixed(2) || '--' }}</td>
                  <td class="center">{{ bulletinData?.rang_annuel || '--' }}</td>
                  <td class="center">{{ bulletinData?.moyenne_classe_annuelle?.toFixed(2) || '--' }}</td>
                </tr>
              </tbody>
            </table>

            <!-- Rang de l'étudiant à l'année -->
            <div class="annual-summary-block mt-4">
               <div class="summary-header text-center font-bold">Rang de l'étudiant à l'année</div>
               <div class="summary-value text-center font-bold text-blue p-2 border-l border-r border-b">{{ bulletinData?.rang_annuel || '5ème' }}</div>
            </div>

            <!-- Bilan Annuel par UE -->
            <div class="annual-bilan mt-4">
              <table class="bilan-table">
                <tbody>
                  <tr>
                    <td v-for="ue in bulletinData?.ues_annuel" :key="ue.id" class="center font-bold">{{ ue.id }}</td>
                    <td class="center font-bold bg-light">Bilan annuel</td>
                  </tr>
                  <tr>
                    <td v-for="ue in bulletinData?.ues_annuel" :key="ue.id" class="center">{{ ue.status_annuel || 'VALIDÉ' }}</td>
                    <td class="center font-bold text-blue">ADMIS</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="decision-block-annual mt-4">
               <p>Décision du Conseil d'Etablissement : <strong class="text-blue">{{ bulletinData?.decision || 'ADMIS' }}</strong></p>
               <p>Mention : <strong class="text-blue">{{ bulletinData?.mention_annuelle || 'Assez Bien' }}</strong></p>
            </div>
          </template>

          <!-- Signatures (identique) -->
          <div class="decision-footer mt-5" v-if="selectedSemester !== 'Annuel'">
            <div class="decision-text">
              <p>Décision du Jury : <strong class="text-blue">{{ bulletinData?.decision || 'Semestre 5 validé' }}</strong></p>
            </div>
            <div class="signature-block">
              <p>Fait à Libreville, le {{ new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) }}</p>
              <p class="direction">Le Directeur des Etudes et de la Pédagogie</p>
              <p class="name mt-4">Davy Edgard MOUSSAVOU</p>
            </div>
          </div>
          
          <div class="decision-footer mt-5" v-else>
            <div class="decision-text"></div>
            <div class="signature-block">
              <p>Fait à Libreville, le {{ new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) }}</p>
              <p class="direction">Le Directeur des Etudes et de la Pédagogie</p>
              <p class="name mt-4">Davy Edgard MOUSSAVOU</p>
            </div>
          </div>

          <div class="footer-note">
            Il ne sera délivré qu'un seul et unique exemplaire de bulletins de notes. L'étudiant est donc prié d'en faire plusieurs copies légalisées.
          </div>
        </div>

        <!-- Structure Editor Tools -->
        <div v-if="editMode === 'structure'" class="structure-tools no-print">
          <button class="btn btn-dashed" @click="addNewUE">
            <span class="icon">➕</span> Ajouter une Unité d'Enseignement (UE)
          </button>
        </div>

        <!-- Action d'impression en bas (Hors feuille A4) -->
        <div class="bulletin-actions no-print">
          <button class="btn btn-primary btn-lg" @click="printBulletin">
            <span class="icon">🖨️</span> Imprimer le bulletin en PDF
          </button>
        </div>
      </div>
      
      <div v-else-if="!isDataLoading" class="empty-selection">
        <p>Sélectionnez un étudiant dans la liste pour prévisualiser son bulletin.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const { fetchApi } = useApi()
const route = useRoute()
const authRole = useCookie('authRole', { default: () => 'etudiant' })
const isEtudiant = computed(() => authRole.value === 'etudiant')

const selectedSemester = ref('S5')
const etudiantsList = ref([])

const studentInfo = ref(null)
const selectedStudent = ref(null)
const isDataLoading = ref(false)
const bulletinData = ref(null)
const editMode = ref(null) // null | 'structure' | 'data'

const fetchEtudiants = async () => {
  try {
    const result = await fetchApi('/etudiants/')
    if (result) etudiantsList.value = result
  } catch (e) {
    console.error('Erreur lors du chargement des étudiants', e)
  }
}

onMounted(async () => {
  const authId = useCookie('authId')
  
  // Priorité au paramètre d'URL (depuis délibérations)
  const queryStudent = route.query.student
  const querySem = route.query.semestre
  
  if (querySem) selectedSemester.value = querySem

  if (isEtudiant.value) {
    selectedStudent.value = authId.value
    await loadBulletin(selectedStudent.value, selectedSemester.value)
  } else if (queryStudent) {
    selectedStudent.value = queryStudent
    await fetchEtudiants()
    await loadBulletin(selectedStudent.value, selectedSemester.value)
  } else {
    await fetchEtudiants()
  }
})

watch(selectedSemester, (newVal) => {
  if (selectedStudent.value) {
    loadBulletin(selectedStudent.value, newVal)
  }
})

const selectStudent = (id) => {
  selectedStudent.value = id
  loadBulletin(id, selectedSemester.value)
}

const loadBulletin = async (id, semester) => {
  isDataLoading.value = true
  try {
    // 1. Informations de l'étudiant
    const detailedStudent = await fetchApi(`/etudiants/${id}/`)
    studentInfo.value = detailedStudent

    // 2. Données du bulletin (calculées par le backend)
    let endpoint = `/resultats/semestre/${id}/`
    let params = { semestre: semester.replace('S', '') }
    
    if (semester === 'Annuel') {
      endpoint = `/resultats/annuel/${id}/`
      params = {}
    }

    const response = await fetchApi(endpoint, { params })
    
    // On adapte la réponse si nécessaire ou on l'assigne directement
    // Le backend (ResultatSemestreView) est censé renvoyer la structure DDD complète
    bulletinData.value = response
    
  } catch (error) {
    console.error('Failed to load bulletin:', error)
    alert("Erreur lors du chargement du bulletin.")
  } finally {
    isDataLoading.value = false
  }
}

// Actions Structure
const addNewUE = () => {
  // Optionnel: implémenter la modification de structure via API
  alert("La modification de structure doit être effectuée via les paramètres académiques.")
}

const addMatiere = (ue) => {
  alert("L'ajout de matière doit être effectué via les paramètres académiques.")
}

const saveAbsence = async () => {
  try {
    // Note: Le backend devrait avoir un endpoint dédié aux absences
    console.log("Saving absences for", selectedStudent.value, ":", bulletinData.value.absences)
    // await fetchApi(`/absences/`, { method: 'POST', body: { ... } })
  } catch (e) {
    console.error("Save failed", e)
  }
}

const printBulletin = () => {
  if (selectedStudent.value) {
    window.print()
  } else {
    alert("Veuillez sélectionner un étudiant d'abord.")
  }
}
</script>

<style scoped>
.page-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 2.5rem; 
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(0,0,128,0.1);
}
.header-content h2 { 
  font-size: 2rem; 
  color: #000080; 
  margin-bottom: 0.5rem; 
  font-weight: 800;
  letter-spacing: -0.02em;
}
.header-subtitle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.95rem;
}
.header-subtitle .dot {
  width: 8px;
  height: 8px;
  background-color: #000080;
  border-radius: 50%;
  display: inline-block;
}

/* Toggle Group Modernized */
.toggle-container {
  display: flex;
  align-items: center;
}
.toggle-group {
  position: relative;
  display: flex;
  background-color: #f1f5f9;
  padding: 6px;
  border-radius: 100px;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
  z-index: 1;
}
.toggle-btn {
  position: relative;
  padding: 0.7rem 1.8rem;
  border-radius: 100px;
  border: none;
  background: transparent;
  color: #475569;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
  font-size: 0.9rem;
  z-index: 2;
  white-space: nowrap;
}
.toggle-btn.active {
  color: white;
}
.toggle-slider {
  position: absolute;
  top: 6px;
  left: 6px;
  height: calc(100% - 12px);
  width: calc(33.33% - 8px);
  background-color: #000080;
  border-radius: 100px;
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
  z-index: 1;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 128, 0.3);
}

.toggle-slider.pos-S5 { transform: translateX(0); width: 105px; }
.toggle-slider.pos-S6 { transform: translateX(105px); width: 105px; }
.toggle-slider.pos-Annuel { transform: translateX(210px); width: 90px; }

/* Correction des largeurs du slider */
.toggle-btn:nth-child(1) { width: 105px; }
.toggle-btn:nth-child(2) { width: 105px; }
.toggle-btn:nth-child(3) { width: 90px; }

.btn-secondary { background-color: white; color: var(--text-main); border: 1px solid var(--border); padding: 0.6rem 1.25rem; border-radius: var(--radius); cursor: pointer; transition: all 0.2s; }
.btn-secondary:hover { background-color: #f9fafb; border-color: #000080; color: #000080; }

.content-wrapper { display: flex; gap: 2rem; }
.students-list { width: 280px; background: var(--surface); border-radius: var(--radius); padding: 1.5rem; box-shadow: var(--shadow); }
.students-list h3 { margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }
.students-list ul { list-style: none; padding: 0; }
.students-list li { padding: 0.75rem 1rem; cursor: pointer; }
.students-list li.active { background-color: var(--primary); color: white; border-radius: 4px; }

/* === SHEET A4 PORTRAIT === */
.bulletin-preview { flex: 1; overflow-x: auto; padding-bottom: 2rem; }
.a4-sheet { 
  background-color: white; 
  width: 21cm; 
  height: 29.7cm; 
  margin: 0 auto; 
  padding: 1cm 1.5cm; 
  box-shadow: 0 0 15px rgba(0,0,0,0.1); 
  color: #000; 
  font-family: 'Times New Roman', Times, serif;
  font-size: 11pt;
  position: relative;
}

.bulletin-actions {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  margin-bottom: 3rem;
}

.btn-primary {
  background-color: #000080;
  color: white;
  border: none;
  padding: 0.8rem 2.5rem;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 128, 0.3);
  transition: all 0.3s;
  font-size: 1.1rem;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 128, 0.4);
  background-color: #0000a0;
}

.text-blue { color: #000080; }
.text-orange { color: #e67e22; }
.font-bold { font-weight: bold; }
.center { text-align: center; }
.right { text-align: right; }

.top-header { display: flex; justify-content: space-between; text-align: center; margin-bottom: 1rem; font-size: 9pt; }
.top-header .left-header, .top-header .right-header { width: 25%; }
.left-header { color: #000080; }
.right-header { color: #000080; }
.logo-inptic-img { max-height: 80px; width: auto; object-fit: contain; margin-top: 0.5rem; }

.center-header { flex: 1; margin-top: 1.5rem; }
.main-title { font-size: 16pt; color: #000080; font-weight: bold; margin-bottom: 0.5rem; }
.annee-univ { color: #000080; }

.class-block { border: 4px double #000080; padding: 0.5rem; margin-top: 1rem; text-align: center; color: #000080; font-size: 11pt; }
.student-info-block { border: 1px solid #000080; margin-bottom: 1rem; font-size: 10pt; }
.info-row { display: flex; border-bottom: 1px solid #000080; }
.info-row:last-child { border-bottom: none; }
.label-col { width: 35%; padding: 0.2rem 0.5rem; border-right: 1px solid #000080; color: #000; }
.val-col { flex: 1; padding: 0.2rem 0.5rem; color: #000080; }

.grades-table { width: 100%; border-collapse: collapse; margin-bottom: 0.5rem; border: 1px solid #000; }
.grades-table th, .grades-table td { border: 1px solid #000; padding: 0.2rem 0.4rem; font-size: 9.5pt; }
.grades-table th { background-color: #f0f4ff; color: #000080; font-weight: normal; }

.ue-header td { background-color: #f0f4ff; color: #000080; font-weight: bold; border-top: 2px solid #000080; }
.ue-header-annual td { background-color: #f0f4ff; color: #000080; font-weight: bold; }
.matiere { padding-left: 0.5rem; color: #000080; }
.pl-4 { padding-left: 1.5rem !important; }

.semester-total-row td { padding: 0.4rem; border-top: 2px solid #000; }
.bg-light { background-color: #f9f9f9; }

.simple-table { width: 100%; border-collapse: collapse; border: 1px solid #000; }
.simple-table td { border: 1px solid #000; padding: 0.3rem; }
.center-table td { text-align: center; }

.validation-table { width: 100%; border-collapse: collapse; border: 1px solid #000; }
.validation-table td { border: 1px solid #000; padding: 0.3rem 0; font-size: 9pt; }

.bilan-table { width: 100%; border-collapse: collapse; border: 1px solid #000; }
.bilan-table td { border: 1px solid #000; padding: 0.4rem; }

.annual-summary-block { border: 1px solid #000; overflow: hidden; }
.summary-header { background-color: #f0f4ff; color: #000080; border-bottom: 2px solid #000; padding: 0.3rem; }

.decision-footer { display: flex; position: relative; font-size: 11pt; }
.decision-text { flex: 1; padding-top: 1.5rem; padding-left: 0.5rem; color: #000080; }
.signature-block { width: 300px; text-align: center; color: #000080; }
.signature-block .direction { margin-top: 0.5rem; }
.flex-between { display: flex; justify-content: space-between; align-items: center; }
.ue-tools { display: flex; gap: 0.5rem; }
.icon-btn { 
  background: white; 
  border: 1px solid #cbd5e1; 
  border-radius: 4px; 
  padding: 2px 5px; 
  cursor: pointer; 
  font-size: 0.8rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.icon-btn:hover { background-color: #f1f5f9; border-color: #000080; }

.absence-input-wrap { display: flex; justify-content: center; }
.abs-field { 
  width: 60px; 
  text-align: center; 
  border: 1px solid #94a3b8; 
  border-radius: 4px; 
  padding: 2px;
  font-weight: bold;
  color: #e67e22;
}

.structure-tools {
  padding: 1.5rem;
  border-top: 1px dashed var(--border);
  margin-top: 2rem;
  text-align: center;
}
.btn-dashed {
  background: transparent;
  border: 2px dashed #cbd5e1;
  color: #64748b;
  padding: 0.8rem 2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}
.btn-dashed:hover {
  border-color: #000080;
  color: #000080;
  background-color: #f8fafc;
}

@media print {
  body * { visibility: hidden; }
  .no-print { display: none !important; }
  #printableArea, #printableArea * { visibility: visible; }
  #printableArea { position: absolute; left: 0; top: 0; margin: 0; padding: 0; box-shadow: none; width: 100%; }
  @page { size: A4; margin: 0.5cm; }
}
</style>
