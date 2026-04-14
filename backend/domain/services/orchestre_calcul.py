from typing import Dict, List
from domain.services.calculateurs.calculateur_matiere import CalculateurMatiere
from domain.services.calculateurs.calculateur_ue import CalculateurUE
from domain.services.calculateurs.calculateur_semestre import CalculateurSemestre
from domain.services.validateurs.validateur_compensation import ValidateurCompensation
from domain.events.event_dispatcher import dispatcher
from domain.events.event import Event # Assumons une classe base Event

class OrchestreCalcul:
    """Façade orchestrant le calcul complet en cascade pour un étudiant."""

    def __init__(self):
        self.calc_matiere = CalculateurMatiere()
        self.calc_ue = CalculateurUE()
        self.calc_semestre = CalculateurSemestre()
        self.validateur = ValidateurCompensation()

    def calculer_bulletin_semestre(self, etudiant_id: str, semestre: int, data: Dict):
        """
        data: {
            'ues': [
                {
                    'id': 'UE1',
                    'credits': 6,
                    'matieres': [
                        {'id': 'M1', 'coeff': 2, 'evals': [...], 'abs': 2},
                        ...
                    ]
                },
                ...
            ]
        }
        """
        resultats_ues = []
        moyennes_ue_objects = []
        
        # 1. Calcul des Matières et UEs
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
            
            # Stockage temporaire pour la validation
            resultats_ues.append({
                'ue_id': ue_data['id'],
                'credits_potentiels': ue_data['credits'],
                'moyenne_ue': moy_ue
            })

        # 2. Calcul de la moyenne du Semestre
        moy_semestre = self.calc_semestre.calculer({
            'moyennes_ue': moyennes_ue_objects
        })

        # 3. Validation de la compensation et calcul des crédits
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

        # 4. Émission d'événements
        # dispatcher.dispatch(...) 

        return {
            'etudiant_id': etudiant_id,
            'semestre': semestre,
            'moyenne_generale': moy_semestre.valeur,
            'total_credits': total_credits,
            'details': details_validation
        }
