from typing import Dict, List, Optional, Any
from domain.repositories.i_evaluation_repository import IEvaluationRepository
from domain.repositories.i_resultat_repository import IResultatRepository
from domain.services.calculateurs.calculateur_matiere import CalculateurMatiere
from domain.services.calculateurs.calculateur_ue import CalculateurUE
from domain.services.calculateurs.calculateur_semestre import CalculateurSemestre
from domain.services.validateurs.validateur_compensation import ValidateurCompensation
from domain.value_objects.moyenne import Moyenne

class OrchestreCalcul:
    """
    Façade orchestrant le calcul complet en cascade pour un étudiant.
    Suit les principes de la POO (Encapsulation, Injection de Dépendances).
    """

    def __init__(self, 
                 evaluation_repo: IEvaluationRepository,
                 resultat_repo: IResultatRepository,
                 calc_matiere: Optional[CalculateurMatiere] = None, 
                 calc_ue: Optional[CalculateurUE] = None, 
                 calc_semestre: Optional[CalculateurSemestre] = None):
        """Initialise l'orchestrateur avec ses dépandances."""
        self._evaluation_repo = evaluation_repo
        self._resultat_repo = resultat_repo
        
        # Les calculateurs sont injectés ou créés par défaut (Pattern Strategy)
        self._calc_matiere = calc_matiere
        self._calc_ue = calc_ue or CalculateurUE()
        self._calc_semestre = calc_semestre or CalculateurSemestre()

    def calculer_bulletin_semestre(self, etudiant_id: str, semestre_libelle: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestre le calcul global :
        Matières -> UEs -> Semestre -> Validation (Compensation)
        """
        resultats_ues: List[Dict] = []
        moyennes_ue_objs: List[Moyenne] = []
        
        for ue_data in data.get('ues', []):
            moyennes_matieres = {}
            coeffs_matieres = {}
            
            for m_data in ue_data.get('matieres', []):
                m_id = m_data['id']
                
                # Récupération des évaluations via le repository
                evals = self._evaluation_repo.obtenir_par_etudiant_matiere(etudiant_id, m_id)
                
                # Calcul de la moyenne de matière (Strategy)
                contexte_m = {
                    'etudiant_id': etudiant_id,
                    'matiere_id': m_id,
                    'evaluations': evals
                }
                
                if self._calc_matiere.peut_calculer(contexte_m):
                    moy_m = self._calc_matiere.calculer(contexte_m)
                    moyennes_matieres[m_id] = moy_m
                    coeffs_matieres[m_id] = m_data.get('coefficient', 1)

            # Calcul de la moyenne d'UE
            contexte_ue = {
                'moyennes_matieres': moyennes_matieres,
                'coefficients_matieres': coeffs_matieres
            }
            moy_ue = self._calc_ue.calculer(contexte_ue)
            moyennes_ue_objs.append(moy_ue)
            
            resultats_ues.append({
                'ue_id': ue_data['id'],
                'libelle': ue_data.get('libelle'),
                'credits_potentiels': ue_data['credits'],
                'moyenne_ue': moy_ue
            })

        # Calcul de la moyenne du semestre
        contexte_s = {'moyennes_ue': moyennes_ue_objs}
        moy_semestre = self._calc_semestre.calculer(contexte_s)

        # Validation et Crédits (Chain of Responsibility / Strategy)
        total_credits = 0
        details_validation = []
        
        for res in resultats_ues:
            # Nouveau Validateur avec injection des crédits de l'UE
            validateur = ValidateurCompensation(credits_ue=res['credits_potentiels'])
            val_res = validateur.valider(res['moyenne_ue'], moy_semestre)
            
            total_credits += val_res.credits_acquis
            details_validation.append(val_res)

        return {
            'etudiant_id': etudiant_id,
            'semestre': semestre_libelle,
            'moyenne_generale': moy_semestre.valeur,
            'total_credits': total_credits,
            'resultats_ues': resultats_ues,
            'details_validation': details_validation
        }
