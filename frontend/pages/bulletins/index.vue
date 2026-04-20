<template>
  <div class="page-bulletins">
    <header class="page-header">
      <div class="header-content">
        <h2>Bulletins Individuels</h2>
        <p>Générez et imprimez les bulletins (modèle INPTIC A4).</p>
      </div>
      <div class="header-actions">
        <div class="toggle-group no-print">
          <button 
            v-for="sem in ['S5', 'S6', 'Annuel']" 
            :key="sem"
            class="toggle-btn"
            :class="{ active: selectedSemester === sem }"
            @click="selectedSemester = sem"
          >
            {{ sem === 'Annuel' ? 'Annuel' : 'Semestre ' + sem.substring(1) }}
          </button>
        </div>
        <button class="btn btn-secondary" @click="printBulletin">
          <span class="icon">🖨️</span> Imprimer / PDF
        </button>
      </div>
    </header>

    <div class="content-wrapper">
      <div class="students-list no-print" v-if="!isEtudiant">
        <h3>Étudiants ({{ selectedSemester }})</h3>
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
                    <td colspan="5">{{ ue.id }} : {{ ue.libelle }}</td>
                  </tr>
                  <tr v-for="matiere in ue.matieres" :key="matiere.libelle">
                    <td class="matiere">{{ matiere.libelle }}</td>
                    <td class="center">{{ matiere.credits || '--' }}</td>
                    <td class="center">{{ matiere.coeff || '1.00' }}</td>
                    <td class="center text-blue font-bold">{{ matiere.moyenne?.toFixed(2) }}</td>
                    <td class="center">{{ matiere.moyenne_classe?.toFixed(2) || '11.50' }}</td>
                  </tr>
                  <tr class="ue-moyenne font-bold">
                    <td class="right">Moyenne {{ ue.id }}</td>
                    <td class="center">{{ ue.total_credits_ue || '--' }}</td>
                    <td class="center">--</td>
                    <td class="center text-blue">{{ ue.moyenne_ue?.toFixed(2) }}</td>
                    <td class="center">--</td>
                  </tr>
                </template>

                <!-- Pénalités -->
                <tr class="penalties-row">
                  <td class="matiere">Pénalités d'absences</td>
                  <td colspan="2" class="center text-orange font-bold">0,01/heure</td>
                  <td class="center">{{ bulletinData?.absences || 0 }} heure(s)</td>
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
                <tr>
                   <td width="50%">Rang de l'étudiant au Semestre</td>
                   <td>Mention</td>
                </tr>
                <tr class="font-bold">
                   <td>{{ bulletinData?.rang || 'Non classé' }}</td>
                   <td>{{ bulletinData?.mention || 'Passable' }}</td>
                </tr>
              </table>
            </div>

            <!-- Validation des crédits (Semestre) -->
            <div class="validation-block mt-4">
              <h4 class="text-center font-bold mb-1">Etat de la Validation des Crédits au {{ selectedSemester }}</h4>
              <table class="validation-table">
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
                    <td class="center">{{ ue.coeff_s1 || '3,00' }}</td>
                    <td class="center">{{ ue.note_s1 || '11,61' }}</td>
                    <td class="center">{{ ue.rang_s1 || '23' }}</td>
                    <td class="center">{{ ue.moy_classe_s1 || '10,34' }}</td>
                  </tr>
                  <tr>
                    <td class="matiere pl-4">Semestre 2</td>
                    <td class="center">{{ ue.coeff_s2 || '3,00' }}</td>
                    <td class="center">{{ ue.note_s2 || '10,78' }}</td>
                    <td class="center">{{ ue.rang_s2 || '2' }}</td>
                    <td class="center">{{ ue.moy_classe_s2 || '11,09' }}</td>
                  </tr>
                  <tr class="annual-row font-bold">
                    <td class="matiere pl-4">Annuel</td>
                    <td class="center">{{ ue.coeff_annuel || '6,00' }}</td>
                    <td class="center text-blue">{{ ue.note_annuel || '10,90' }}</td>
                    <td class="center">{{ ue.rang_annuel || '5' }}</td>
                    <td class="center">{{ ue.moy_classe_annuel || '10,71' }}</td>
                  </tr>
                </template>

                <!-- Ligne de Moyenne Annuelle Totale -->
                <tr class="ue-header-annual">
                  <td colspan="5">Moyenne Annuelle</td>
                </tr>
                <tr class="font-bold">
                  <td class="pl-4">Annuel</td>
                  <td class="center">42.00</td>
                  <td class="center text-blue">12.78</td>
                  <td class="center">10</td>
                  <td class="center">11.06</td>
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
                <tr>
                  <td v-for="ue in bulletinData?.ues_annuel" :key="ue.id" class="center font-bold">{{ ue.id }}</td>
                  <td class="center font-bold bg-light">Bilan annuel</td>
                </tr>
                <tr>
                  <td v-for="ue in bulletinData?.ues_annuel" :key="ue.id" class="center">{{ ue.status_annuel || 'VALIDÉ' }}</td>
                  <td class="center font-bold text-blue">ADMIS</td>
                </tr>
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
      </div>
      
      <div v-else-if="!isDataLoading" class="empty-selection">
        <p>Sélectionnez un étudiant dans la liste pour prévisualiser son bulletin.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useApi } from '~/composables/useApi'

useHead({ title: 'Bulletins | Bull ASUR' })

const { apiFetch } = useApi()
const authRole = useCookie('authRole', { default: () => 'etudiant' })
const isEtudiant = computed(() => authRole.value === 'etudiant')
const etudiantMonId = 'TEST2026001' // ID statique de l'étudiant connecté (demo)

const selectedSemester = ref('S5')
const etudiantsList = ref([
  { id: 'TEST2026001', nom: 'MBA NSOME', prenom: 'Yannick Lionel' },
  { id: 'TEST2026002', nom: 'Martin', prenom: 'Sophie' },
  { id: 'TEST2026003', nom: 'Bernard', prenom: 'Luc' },
])

const selectedStudent = ref(null)
const isDataLoading = ref(false)
const bulletinData = ref(null)
const studentInfo = ref(null)

const fetchEtudiants = async () => {
  try {
    const result = await apiFetch('/api/etudiants/')
    if (result) etudiantsList.value = result
  } catch (e) {
    console.error('Failed to fetch etudiants:', e)
  }
}

onMounted(() => {
  if (isEtudiant.value) {
    selectedStudent.value = etudiantMonId
    loadBulletin(etudiantMonId, selectedSemester.value)
  } else {
    fetchEtudiants()
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
    const detailedStudent = await apiFetch(`/api/etudiants/${id}/`).catch(() => null)
    studentInfo.value = detailedStudent || etudiantsList.value.find(s => s.id === id)
    if (!studentInfo.value?.date_naissance) {
      studentInfo.value.date_naissance = '05/05/1989' // Mock pour démo
    }

    if (semester === 'Annuel') {
      bulletinData.value = {
        rang_annuel: '5ème',
        mention_annuelle: 'Assez Bien',
        decision: 'ADMIS',
        ues_annuel: [
          { id: 'UE1', libelle: 'Communication / Management', coeff_s1: '4,50', note_s1: '12,00', rang_s1: '5', moy_classe_s1: '11,06', coeff_s2: '9,00', note_s2: '11,27', rang_s2: '1', moy_classe_s2: '12,12', coeff_annuel: '13,50', note_annuel: '11,45', rang_annuel: '2', moy_classe_annuel: '11,67', status_annuel: 'VALIDÉ' },
          { id: 'UE2', libelle: 'Sciences de base (Réseaux)', coeff_s1: '6,00', note_s1: '12,40', rang_s1: '1', moy_classe_s1: '9,34', coeff_s2: '3,00', note_s2: '11,14', rang_s2: '1', moy_classe_s2: '10,30', coeff_annuel: '9,00', note_annuel: '12,05', rang_annuel: '1', moy_classe_annuel: '9,66', status_annuel: 'VALIDÉ' }
        ]
      }
    } else {
      const response = await apiFetch(`/api/resultats/semestre/${id}/`, { params: { semestre: semester.replace('S', '') } }).catch(() => null)
      
      bulletinData.value = response || {
        moyenne_generale: 10.66,
        moyenne_classe_generale: 11.80,
        mention: 'Passable',
        rang: 'Non classé',
        absences: 0,
        credits_acquis: 30,
        total_credits: 30,
        valide: true,
        validation_commentaire: 'Semestre Acquis par Compensation',
        decision: `${semester} validé`,
        ues: [
          {
            id: 'UE5-1',
            libelle: 'ENSEIGNEMENT GENERAL',
            total_credits_ue: 12,
            credits_acquis: 13,
            moyenne_ue: 11.45,
            matieres: [
              { libelle: 'Anglais technique', credits: 2, coeff: '1,00', moyenne: 10.75, moyenne_classe: 12.49 },
              { libelle: 'Management d\'équipe', credits: 1, coeff: '1,00', moyenne: 14.00, moyenne_classe: 14.19 },
              { libelle: 'Communication', credits: 1, coeff: '2,00', moyenne: 11.80, moyenne_classe: 11.63 }
            ]
          },
          {
            id: 'UE5-2',
            libelle: 'CONNAISSANCES DE BASE ET OUTILS',
            total_credits_ue: 18,
            credits_acquis: 17,
            moyenne_ue: 10.07,
            matieres: [
              { libelle: 'Remise à niveau IOS', credits: 2, coeff: '2,00', moyenne: 6.00, moyenne_classe: 8.50 },
              { libelle: 'Connaissance des réseaux LAN', credits: 2, coeff: '2,00', moyenne: 15.00, moyenne_classe: 12.96 }
            ]
          }
        ]
      }
    }

    setTimeout(() => {
      isDataLoading.value = false
    }, 400)
  } catch (error) {
    console.error('Failed to load bulletin:', error)
    isDataLoading.value = false
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
.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; }
.header-content h2 { font-size: 1.75rem; color: var(--text-main); margin-bottom: 0.25rem; font-weight: 700; }

/* Toggle Group Styles */
.toggle-group {
  display: flex;
  background-color: #f0f2f5;
  padding: 4px;
  border-radius: 50px;
  margin-right: 1.5rem;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
}
.toggle-btn {
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  border: none;
  background: transparent;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}
.toggle-btn.active {
  background-color: #000080;
  color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 128, 0.2), 0 2px 4px -1px rgba(0, 0, 128, 0.1);
}
.toggle-btn:hover:not(.active) {
  background-color: rgba(0, 0, 128, 0.05);
  color: #000080;
}

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
.signature-block .name { margin-top: 3.5rem; text-decoration: underline; font-weight: bold; }

.footer-note { position: absolute; bottom: 0.5cm; left: 0; width: 100%; text-align: center; font-size: 8pt; font-style: italic; }

.mini-loader { padding: 2rem; text-align: center; color: var(--primary); font-style: italic; }

@media print {
  body * { visibility: hidden; }
  .no-print { display: none !important; }
  #printableArea, #printableArea * { visibility: visible; }
  #printableArea { position: absolute; left: 0; top: 0; margin: 0; padding: 0; box-shadow: none; width: 100%; }
  @page { size: A4; margin: 0.5cm; }
}
</style>
