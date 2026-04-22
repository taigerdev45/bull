<template>
  <div class="bulletin-generator">
    <!-- Boutons de génération -->
    <div class="generation-controls">
      <h3>Génération des Bulletins</h3>
      
      <div class="control-group">
        <label>Sélectionner un étudiant:</label>
        <select v-model="selectedEtudiantId" class="form-control">
          <option value="">Choisir un étudiant...</option>
          <option v-for="etudiant in etudiants" :key="etudiant.id" :value="etudiant.id">
            {{ etudiant.nom }} {{ etudiant.prenom }} ({{ etudiant.matricule }})
          </option>
        </select>
      </div>
      
      <div class="button-group">
        <button @click="generateBulletinS5" :disabled="!selectedEtudiantId" class="btn btn-primary">
          <span>PDF</span> Bulletin S5
        </button>
        <button @click="generateBulletinS6" :disabled="!selectedEtudiantId" class="btn btn-primary">
          <span>PDF</span> Bulletin S6
        </button>
        <button @click="generateBulletinAnnuel" :disabled="!selectedEtudiantId" class="btn btn-success">
          <span>PDF</span> Bulletin Annuel
        </button>
      </div>
    </div>
    
    <!-- Export Excel -->
    <div class="export-controls">
      <h3>Export Excel</h3>
      
      <div class="button-group">
        <button @click="exportReleveNotesS5" class="btn btn-secondary">
          <span>Excel</span> Relevé S5
        </button>
        <button @click="exportReleveNotesS6" class="btn btn-secondary">
          <span>Excel</span> Relevé S6
        </button>
        <button @click="exportDecisionsJury" class="btn btn-info">
          <span>Excel</span> Décisions Jury
        </button>
      </div>
    </div>
    
    <!-- Aperçu du bulletin -->
    <div v-if="bulletinPreview" class="bulletin-preview">
      <h3>Aperçu du Bulletin</h3>
      <div class="preview-content">
        <div class="bulletin-header">
          <h4>{{ bulletinPreview.type }}</h4>
          <p>Date d'émission: {{ bulletinPreview.date_emission }}</p>
        </div>
        
        <div class="etudiant-info">
          <h5>Informations Étudiant</h5>
          <p><strong>Nom:</strong> {{ bulletinPreview.etudiant.nom }}</p>
          <p><strong>Prénom:</strong> {{ bulletinPreview.etudiant.prenom }}</p>
          <p><strong>Matricule:</strong> {{ bulletinPreview.etudiant.matricule }}</p>
          <p><strong>Date de naissance:</strong> {{ bulletinPreview.etudiant.date_naissance }}</p>
          <p><strong>Lieu de naissance:</strong> {{ bulletinPreview.etudiant.lieu_naissance }}</p>
        </div>
        
        <div class="resultats">
          <h5>Résultats</h5>
          <div v-if="bulletinPreview.ues && bulletinPreview.ues.length > 0">
            <div v-for="ue in bulletinPreview.ues" :key="ue.id" class="ue-resultat">
              <h6>{{ ue.code }} - {{ ue.libelle }}</h6>
              <p>Moyenne UE: {{ ue.moyenne_ue }}/20 | Crédits: {{ ue.credits_acquis }}/{{ ue.credits_total }}</p>
              <p>Statut: {{ ue.acquise ? 'Acquise' : ue.compensee ? 'Compensée' : 'Non acquise' }}</p>
              
              <div v-if="ue.matieres" class="matieres-detail">
                <div v-for="mat in ue.matieres" :key="mat.id" class="matiere-resultat">
                  <p>{{ mat.libelle }}: {{ mat.moyenne }}/20 (Coef: {{ mat.coefficient }})</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="statistiques">
          <h5>Statistiques</h5>
          <p><strong>Moyenne générale:</strong> {{ bulletinPreview.statistiques?.moyenne_generale }}/20</p>
          <p><strong>Crédits acquis:</strong> {{ bulletinPreview.statistiques?.credits_acquis }}</p>
          <p><strong>UE acquises:</strong> {{ bulletinPreview.statistiques?.ue_acquises }}</p>
        </div>
        
        <div class="decision">
          <h5>Décision</h5>
          <p :class="getDecisionClass(bulletinPreview.decision?.couleur)">
            <strong>{{ bulletinPreview.decision?.statut }}</strong>
          </p>
          <p>{{ bulletinPreview.decision?.detail }}</p>
        </div>
        
        <div class="preview-actions">
          <button @click="downloadPDF" class="btn btn-primary">
            <span>PDF</span> Télécharger
          </button>
          <button @click="closePreview" class="btn btn-secondary">
            Fermer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BulletinService from '~/services/bulletinService'

const bulletinService = BulletinService

// État
const etudiants = ref([])
const selectedEtudiantId = ref('')
const bulletinPreview = ref(null)
const loading = ref(false)

// Charger les étudiants
const loadEtudiants = async () => {
  try {
    // Simulation - à remplacer par appel API réel
    const mockEtudiants = [
      {
        id: 1,
        nom: 'DIALLO',
        prenom: 'Mamadou',
        matricule: 'LPASUR001',
        date_naissance: '2000-01-15',
        lieu_naissance: 'Dakar',
        bac: 'S',
        provenance: 'Lycée Blaise Diagne'
      },
      {
        id: 2,
        nom: 'FALL',
        prenom: 'Aïssa',
        matricule: 'LPASUR002',
        date_naissance: '2001-03-20',
        lieu_naissance: 'Thiès',
        bac: 'ES',
        provenance: 'Lycée Jean Mermoz'
      }
    ]
    etudiants.value = mockEtudiants
  } catch (error) {
    console.error('Erreur chargement étudiants:', error)
  }
}

// Générer bulletin S5
const generateBulletinS5 = async () => {
  const etudiant = etudiants.value.find(e => e.id === parseInt(selectedEtudiantId.value))
  if (!etudiant) return
  
  loading.value = true
  
  try {
    // Simulation des résultats S5
    const resultatsS5 = {
      ues: [
        {
          id: 'UE5-1',
          code: 'UE5-1',
          libelle: 'Enseignement Général',
          moyenne_ue: 11.50,
          credits_acquis: 8,
          credits_total: 10,
          acquise: true,
          compensee: false,
          matieres: [
            { id: 1, libelle: 'Anglais technique', moyenne: 12, coefficient: 1, credits: 2 },
            { id: 2, libelle: 'Management d\'équipe', moyenne: 10, coefficient: 1, credits: 1 },
            { id: 3, libelle: 'Communication', moyenne: 13, coefficient: 2, credits: 1 }
          ]
        },
        {
          id: 'UE5-2',
          code: 'UE5-2',
          libelle: 'Connaissances de Base et Outils pour les Réseaux d\'Entreprise',
          moyenne_ue: 12.80,
          credits_acquis: 20,
          credits_total: 20,
          acquise: true,
          compensee: false,
          matieres: [
            { id: 4, libelle: 'Remise à niveau IOS', moyenne: 11, coefficient: 2, credits: 2 },
            { id: 5, libelle: 'Connaissance des réseaux LAN', moyenne: 14, coefficient: 2, credits: 2 }
          ]
        }
      ],
      credits_acquis: 28,
      moyenne_generale: 12.15
    }
    
    bulletinPreview.value = bulletinService.generateBulletinS5(etudiant, resultatsS5)
  } catch (error) {
    console.error('Erreur génération bulletin S5:', error)
  } finally {
    loading.value = false
  }
}

// Générer bulletin S6
const generateBulletinS6 = async () => {
  const etudiant = etudiants.value.find(e => e.id === parseInt(selectedEtudiantId.value))
  if (!etudiant) return
  
  loading.value = true
  
  try {
    // Simulation des résultats S6
    const resultatsS6 = {
      ues: [
        {
          id: 'UE6-1',
          code: 'UE6-1',
          libelle: 'Sciences de Base',
          moyenne_ue: 13.20,
          credits_acquis: 17,
          credits_total: 17,
          acquise: true,
          compensee: false,
          matieres: [
            { id: 6, libelle: 'Environnement Windows', moyenne: 14, coefficient: 3, credits: 3 },
            { id: 7, libelle: 'Environnement Linux', moyenne: 12, coefficient: 3, credits: 3 }
          ]
        },
        {
          id: 'UE6-2',
          code: 'UE6-2',
          libelle: 'Télécommunications et Réseaux',
          moyenne_ue: 11.00,
          credits_acquis: 10,
          credits_total: 13,
          acquise: false,
          compensee: true,
          matieres: [
            { id: 8, libelle: 'Méthodologie de rédaction du rapport de stage', moyenne: 13, coefficient: 2, credits: 2 },
            { id: 9, libelle: 'Soutenance', moyenne: 0, coefficient: 8, credits: 8 }
          ]
        }
      ],
      credits_acquis: 27,
      moyenne_generale: 12.10
    }
    
    bulletinPreview.value = bulletinService.generateBulletinS6(etudiant, resultatsS6)
  } catch (error) {
    console.error('Erreur génération bulletin S6:', error)
  } finally {
    loading.value = false
  }
}

// Générer bulletin annuel
const generateBulletinAnnuel = async () => {
  const etudiant = etudiants.value.find(e => e.id === parseInt(selectedEtudiantId.value))
  if (!etudiant) return
  
  loading.value = true
  
  try {
    // Simulation des résultats S5 et S6
    const resultatsS5 = {
      credits_acquis: 28,
      moyenne_generale: 12.15,
      ues: []
    }
    
    const resultatsS6 = {
      credits_acquis: 27,
      moyenne_generale: 12.10,
      ues: []
    }
    
    bulletinPreview.value = bulletinService.generateBulletinAnnuel(etudiant, resultatsS5, resultatsS6)
  } catch (error) {
    console.error('Erreur génération bulletin annuel:', error)
  } finally {
    loading.value = false
  }
}

// Export Excel relevé S5
const exportReleveNotesS5 = () => {
  try {
    const exportData = bulletinService.exportExcelReleveNotes(etudiants.value, 5)
    downloadExcelFile(exportData)
  } catch (error) {
    console.error('Erreur export Excel S5:', error)
  }
}

// Export Excel relevé S6
const exportReleveNotesS6 = () => {
  try {
    const exportData = bulletinService.exportExcelReleveNotes(etudiants.value, 6)
    downloadExcelFile(exportData)
  } catch (error) {
    console.error('Erreur export Excel S6:', error)
  }
}

// Export Excel décisions jury
const exportDecisionsJury = () => {
  try {
    const exportData = bulletinService.exportExcelDecisionsJury(etudiants.value)
    downloadExcelFile(exportData)
  } catch (error) {
    console.error('Erreur export décisions jury:', error)
  }
}

// Télécharger fichier Excel (simulation)
const downloadExcelFile = (exportData) => {
  // Création du contenu CSV (simulation Excel)
  const csvContent = [
    exportData.headers.join(','),
    ...exportData.data.map(row => row.join(','))
  ].join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  link.setAttribute('href', url)
  link.setAttribute('download', exportData.filename)
  link.style.visibility = 'hidden'
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  console.log(`Export Excel créé: ${exportData.filename}`)
}

// Télécharger PDF (simulation)
const downloadPDF = () => {
  if (!bulletinPreview.value) return
  
  // Simulation de génération PDF
  const pdfContent = `
    BULLETIN: ${bulletinPreview.value.type}
    Étudiant: ${bulletinPreview.value.etudiant.nom} ${bulletinPreview.value.etudiant.prenom}
    Matricule: ${bulletinPreview.value.etudiant.matricule}
    Date: ${bulletinPreview.value.date_emission}
    
    MOYENNE: ${bulletinPreview.value.statistiques?.moyenne_generale}/20
    CRÉDITS: ${bulletinPreview.value.statistiques?.credits_acquis}
    DÉCISION: ${bulletinPreview.value.decision?.statut}
  `
  
  const blob = new Blob([pdfContent], { type: 'text/plain;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  const filename = `bulletin_${bulletinPreview.value.etudiant.matricule}_${new Date().toISOString().split('T')[0]}.txt`
  
  link.setAttribute('href', url)
  link.setAttribute('download', filename)
  link.style.visibility = 'hidden'
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  console.log(`Bulletin PDF créé: ${filename}`)
}

// Obtenir classe CSS pour décision
const getDecisionClass = (couleur) => {
  return {
    'decision-success': couleur === 'green',
    'decision-warning': couleur === 'orange',
    'decision-danger': couleur === 'red'
  }
}

// Fermer aperçu
const closePreview = () => {
  bulletinPreview.value = null
}

onMounted(() => {
  loadEtudiants()
})
</script>

<style scoped>
.bulletin-generator {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.generation-controls, .export-controls {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid var(--border);
}

.generation-controls h3, .export-controls h3 {
  margin-bottom: 1rem;
  color: var(--text-main);
}

.control-group {
  margin-bottom: 1rem;
}

.control-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-main);
}

.button-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--radius);
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
}

.btn-success {
  background: var(--success);
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #059669;
}

.btn-secondary {
  background: var(--bg-color);
  color: var(--text-main);
  border: 1px solid var(--border);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--border);
}

.btn-info {
  background: var(--info);
  color: white;
}

.btn-info:hover:not(:disabled) {
  background: #0284c7;
}

.bulletin-preview {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 2rem;
  border: 1px solid var(--border);
  margin-top: 2rem;
}

.preview-content {
  max-height: 600px;
  overflow-y: auto;
}

.bulletin-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--border);
}

.etudiant-info, .resultats, .statistiques, .decision {
  margin-bottom: 1.5rem;
}

.etudiant-info h5, .resultats h5, .statistiques h5, .decision h5 {
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.ue-resultat {
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--bg-color);
  border-radius: var(--radius);
  border-left: 4px solid var(--primary);
}

.matieres-detail {
  margin-left: 1rem;
  margin-top: 0.5rem;
}

.matiere-resultat {
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
  color: var(--text-muted);
}

.decision-success {
  color: var(--success);
  font-weight: bold;
}

.decision-warning {
  color: var(--warning);
  font-weight: bold;
}

.decision-danger {
  color: var(--danger);
  font-weight: bold;
}

.preview-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 0.95rem;
  background: var(--bg-color);
  color: var(--text-main);
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
}
</style>
