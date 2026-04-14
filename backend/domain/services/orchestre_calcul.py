from typing import Dict, List, Optional
from domain.services.calculateurs.calculateur_matiere import CalculateurMatiere
from domain.services.calculateurs.calculateur_ue import CalculateurUE
from domain.services.calculateurs.calculateur_semestre import CalculateurSemestre
from domain.services.validateurs.validateur_compensation import ValidateurCompensation

class OrchestreCalcul:
    """Façade orchestrant le calcul complet en cascade pour un étudiant.
    
    Cette classe coordonne la séquence de calcul allant des notes individuelles
    jusqu'à la validation du semestre et l'acquisition des crédits ECTS.
    
    Attributes:
        calc_matiere (CalculateurMatiere): Stratégie de calcul des moyennes par matière.
        calc_ue (CalculateurUE): Stratégie d'agrégation des UEs.
        calc_semestre (CalculateurSemestre): Calcul de la moyenne générale.
        validateur (ValidateurCompensation): Moteur de décision pour les crédits.
    """

    def __init__(self, 
                 calc_matiere: Optional[CalculateurMatiere] = None, 
                 calc_ue: Optional[CalculateurUE] = None, 
                 calc_semestre: Optional[CalculateurSemestre] = None):
        """Initialise l'orchestrateur avec ses dépendances (ou valeurs par défaut)."""
        self.calc_matiere = calc_matiere or CalculateurMatiere()
        self.calc_ue = calc_ue or CalculateurUE()
        self.calc_semestre = calc_semestre or CalculateurSemestre()
        self.validateur = ValidateurCompensation()

    def calculer_bulletin_semestre(self, etudiant_id: str, semestre: int, data: Dict) -> Dict:
        """Exécute le calcul complet du bulletin pour un semestre donné.
        
        Args:
            etudiant_id (str): Identifiant unique de l'étudiant.
            semestre (int): Numéro du semestre (ex: 5).
            data (Dict): Dictionnaire contenant l'arborescence des UEs, matières et notes.
            
        Returns:
            Dict: Un dictionnaire contenant les résultats agrégés, crédits et moyennes.
            
        Raises:
            ValidationError: Si la structure des données est invalide.
        """
        resultats_ues: List[Dict] = []
        moyennes_ue_objects = []
        
        for ue_data in data.get('ues', []):
            moyennes_matieres = {}
            coeffs_matieres = {}
            
            for m_data in ue_data.get('matieres', []):
                moy_m = self.calc_matiere.calculer({
                    'evaluations': m_data['evaluations'],
                    'heures_absence': m_data['heures_absence']
                })
                moyennes_matieres[m_data['id']] = moy_m
                coeffs_matieres[m_data['id']] = m_data['coefficient']

            moy_ue = self.calc_ue.calculer({
                'moyennes_matieres': moyennes_matieres,
                'coefficients_matieres': coeffs_matieres
            })
            moyennes_ue_objects.append(moy_ue)
            
            resultats_ues.append({
                'ue_id': ue_data['id'],
                'credits_potentiels': ue_data['credits'],
                'moyenne_ue': moy_ue
            })

        moy_semestre = self.calc_semestre.calculer({
            'moyennes_ue': moyennes_ue_objects
        })

        total_credits = 0
        details_validation = []
        
        for res in resultats_ues:
            val_res = self.validateur.valider({
                'moyenne_ue': res['moyenne_ue'].valeur,
                'moyenne_generale_semestre': moy_semestre.valeur,
                'credits_ue': res['credits_potentiels']
            })
            total_credits += val_res.credits_acquis
            details_validation.append(val_res)

        return {
            'etudiant_id': etudiant_id,
            'semestre': semestre,
            'moyenne_generale': moy_semestre.valeur,
            'total_credits': total_credits,
            'details': details_validation
        }
