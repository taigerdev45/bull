// Service de génération de bulletins PDF et export Excel
export class BulletinService {
  
  // Génération du bulletin S5
  generateBulletinS5(etudiant, resultats) {
    const bulletin = {
      type: 'BULLETIN S5',
      etudiant: {
        nom: etudiant.nom,
        prenom: etudiant.prenom,
        matricule: etudiant.matricule,
        date_naissance: etudiant.date_naissance,
        lieu_naissance: etudiant.lieu_naissance,
        bac: etudiant.bac,
        provenance: etudiant.provenance
      },
      semestre: {
        id: 'S5',
        libelle: 'Semestre 5',
        annee: '2025-2026'
      },
      ues: resultats.ues || [],
      statistiques: this.calculateStatistiques(resultats),
      decision: this.calculateDecision(resultats),
      date_emission: new Date().toLocaleDateString('fr-FR')
    }
    
    return bulletin
  }
  
  // Génération du bulletin S6
  generateBulletinS6(etudiant, resultats) {
    const bulletin = {
      type: 'BULLETIN S6',
      etudiant: {
        nom: etudiant.nom,
        prenom: etudiant.prenom,
        matricule: etudiant.matricule,
        date_naissance: etudiant.date_naissance,
        lieu_naissance: etudiant.lieu_naissance,
        bac: etudiant.bac,
        provenance: etudiant.provenance
      },
      semestre: {
        id: 'S6',
        libelle: 'Semestre 6',
        annee: '2025-2026'
      },
      ues: resultats.ues || [],
      statistiques: this.calculateStatistiques(resultats),
      decision: this.calculateDecision(resultats),
      date_emission: new Date().toLocaleDateString('fr-FR')
    }
    
    return bulletin
  }
  
  // Génération du bulletin annuel
  generateBulletinAnnuel(etudiant, resultatsS5, resultatsS6) {
    const moyenneAnnuelle = this.calculateMoyenneAnnuelle(resultatsS5, resultatsS6)
    const creditsTotal = (resultatsS5.credits_acquis || 0) + (resultatsS6.credits_acquis || 0)
    
    const bulletin = {
      type: 'BULLETIN ANNUEL',
      etudiant: {
        nom: etudiant.nom,
        prenom: etudiant.prenom,
        matricule: etudiant.matricule,
        date_naissance: etudiant.date_naissance,
        lieu_naissance: etudiant.lieu_naissance,
        bac: etudiant.bac,
        provenance: etudiant.provenance
      },
      annee: '2025-2026',
      resultats: {
        S5: resultatsS5,
        S6: resultatsS6
      },
      moyenne_annuelle: moyenneAnnuelle,
      credits_total: creditsTotal,
      mention: this.getMention(moyenneAnnuelle),
      decision_jury: this.getDecisionAnnuelle(resultatsS5, resultatsS6),
      statistiques_promotion: this.getStatistiquesPromotion(),
      date_emission: new Date().toLocaleDateString('fr-FR')
    }
    
    return bulletin
  }
  
  // Calcul des statistiques
  calculateStatistiques(resultats) {
    if (!resultats.ues || resultats.ues.length === 0) {
      return {
        moyenne_generale: 0,
        credits_acquis: 0,
        ue_acquises: 0,
        ue_compensees: 0,
        ue_non_acquises: 0
      }
    }
    
    const notes = []
    let creditsAcquis = 0
    let ueAcquises = 0
    let ueCompensees = 0
    let ueNonAcquises = 0
    
    resultats.ues.forEach(ue => {
      if (ue.matieres) {
        ue.matieres.forEach(mat => {
          if (mat.moyenne !== undefined && mat.moyenne !== null) {
            notes.push(mat.moyenne)
          }
        })
      }
      
      if (ue.acquise) ueAcquises++
      else if (ue.compensee) ueCompensees++
      else ueNonAcquises++
      
      creditsAcquis += ue.credits_acquis || 0
    })
    
    const moyenneGenerale = notes.length > 0 
      ? notes.reduce((a, b) => a + b, 0) / notes.length 
      : 0
    
    return {
      moyenne_generale: moyenneGenerale.toFixed(2),
      credits_acquis: creditsAcquis,
      ue_acquises: ueAcquises,
      ue_compensees: ueCompensees,
      ue_non_acquises: ueNonAcquises
    }
  }
  
  // Calcul de la décision de semestre
  calculateDecision(resultats) {
    const credits = resultats.credits_acquis || 0
    
    if (credits >= 30) {
      return {
        statut: 'Validé',
        detail: 'Semestre validé - Tous les crédits acquis',
        couleur: 'green'
      }
    } else if (credits >= 25) {
      return {
        statut: 'Admissible',
        detail: 'En attente de validation finale',
        couleur: 'orange'
      }
    } else {
      return {
        statut: 'Non validé',
        detail: 'Crédits insuffisants - Redoublement',
        couleur: 'red'
      }
    }
  }
  
  // Calcul de la moyenne annuelle
  calculateMoyenneAnnuelle(resultatsS5, resultatsS6) {
    const moyS5 = resultatsS5.moyenne_generale || 0
    const moyS6 = resultatsS6.moyenne_generale || 0
    
    if (moyS5 === 0 && moyS6 === 0) return 0
    if (moyS5 === 0) return moyS6
    if (moyS6 === 0) return moyS5
    
    return ((moyS5 + moyS6) / 2).toFixed(2)
  }
  
  // Obtention de la mention
  getMention(moyenne) {
    const moy = parseFloat(moyenne)
    if (moy >= 16) return 'Très Bien'
    if (moy >= 14) return 'Bien'
    if (moy >= 12) return 'Assez Bien'
    if (moy >= 10) return 'Passable'
    return 'Insuffisant'
  }
  
  // Décision annuelle du jury
  getDecisionAnnuelle(resultatsS5, resultatsS6) {
    const creditsS5 = resultatsS5.credits_acquis || 0
    const creditsS6 = resultatsS6.credits_acquis || 0
    const creditsTotal = creditsS5 + creditsS6
    
    if (creditsTotal >= 60) {
      return {
        statut: 'Diplômé(e)',
        detail: 'Les deux semestres validés - 60 crédits acquis',
        couleur: 'green'
      }
    } else if (creditsTotal >= 52) {
      // Cas particulier : reprise de soutenance
      const ue6_2 = resultatsS6.ues?.find(ue => ue.id === 'UE6-2')
      if (ue6_2 && !ue6_2.acquise) {
        return {
          statut: 'Reprise de soutenance',
          detail: 'Tous les crédits acquis sauf l\'UE6-2 (soutenance)',
          couleur: 'orange'
        }
      }
    }
    
    return {
      statut: 'Redouble la Licence 3',
      detail: 'Crédits insuffisants - Conditions non remplies',
      couleur: 'red'
    }
  }
  
  // Statistiques de promotion (mock)
  getStatistiquesPromotion() {
    return {
      effectif_total: 24,
      moyenne_classe: 12.45,
      note_min: 8.50,
      note_max: 17.80,
      ecart_type: 2.34,
      taux_reussite: 87.5
    }
  }
  
  // Export Excel des relevés de notes
  exportExcelReleveNotes(etudiants, semestre) {
    const data = []
    
    // En-têtes
    const headers = [
      'Matricule', 'Nom', 'Prénom', 'UE', 'Matière', 
      'Note CC', 'Note Examen', 'Note Rattrapage', 'Moyenne',
      'Crédits', 'Absences (h)', 'Décision UE'
    ]
    
    etudiants.forEach(etudiant => {
      etudiant.ues?.forEach(ue => {
        ue.matieres?.forEach(matiere => {
          data.push([
            etudiant.matricule || '',
            etudiant.nom || '',
            etudiant.prenom || '',
            ue.code || '',
            matiere.libelle || '',
            matiere.note_cc || '',
            matiere.note_examen || '',
            matiere.note_rattrapage || '',
            matiere.moyenne || '',
            matiere.credits || '',
            matiere.absences || '',
            matiere.decision_ue || ''
          ])
        })
      })
    })
    
    return {
      headers,
      data,
      filename: `releve_notes_S${semestre}_${new Date().toISOString().split('T')[0]}.xlsx`
    }
  }
  
  // Export Excel des décisions de jury
  exportExcelDecisionsJury(etudiants) {
    const data = []
    
    const headers = [
      'Matricule', 'Nom', 'Prénom', 'Moyenne S5', 'Crédits S5', 
      'Moyenne S6', 'Crédits S6', 'Moyenne Annuelle', 'Total Crédits',
      'Décision Jury', 'Mention'
    ]
    
    etudiants.forEach(etudiant => {
      data.push([
        etudiant.matricule || '',
        etudiant.nom || '',
        etudiant.prenom || '',
        etudiant.resultatsS5?.moyenne_generale || '',
        etudiant.resultatsS5?.credits_acquis || '',
        etudiant.resultatsS6?.moyenne_generale || '',
        etudiant.resultatsS6?.credits_acquis || '',
        etudiant.moyenne_annuelle || '',
        etudiant.credits_total || '',
        etudiant.decision_jury?.statut || '',
        etudiant.mention || ''
      ])
    })
    
    return {
      headers,
      data,
      filename: `decisions_jury_${new Date().toISOString().split('T')[0]}.xlsx`
    }
  }
}

export default new BulletinService()
