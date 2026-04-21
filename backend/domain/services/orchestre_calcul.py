from typing import Dict, List, Optional, Any
from domain.repositories.i_evaluation_repository import IEvaluationRepository
from domain.repositories.i_resultat_repository import IResultatRepository
from domain.repositories.i_ue_repository import IUERepository
from domain.repositories.i_matiere_repository import IMatiereRepository
from domain.services.calculateurs.calculateur_matiere import CalculateurMatiere
from domain.services.calculateurs.calculateur_ue import CalculateurUE
from domain.services.calculateurs.calculateur_semestre import CalculateurSemestre
from domain.services.calculateurs.calculateur_annuel import CalculateurAnnuel
from domain.services.validateurs.validateur_compensation import ValidateurCompensation
from domain.value_objects.moyenne import Moyenne, TypeCalculMoyenne
from domain.entities.resultat import ResultatUE, ResultatSemestre, ResultatAnnuel

class OrchestreCalcul:
    """
    Façade orchestrant le calcul complet en cascade pour un étudiant.
    Suit les principes de la POO (Encapsulation, Injection de Dépendances).
    """

    def __init__(self, 
                 evaluation_repo: IEvaluationRepository,
                 resultat_repo: IResultatRepository,
                 ue_repo: IUERepository,
                 matiere_repo: IMatiereRepository,
                 calc_matiere: Optional[CalculateurMatiere] = None, 
                 calc_ue: Optional[CalculateurUE] = None, 
                 calc_semestre: Optional[CalculateurSemestre] = None,
                 calc_annuel: Optional[CalculateurAnnuel] = None):
        """Initialise l'orchestrateur avec ses dépendances."""
        self._evaluation_repo = evaluation_repo
        self._resultat_repo = resultat_repo
        self._ue_repo = ue_repo
        self._matiere_repo = matiere_repo
        
        # Les calculateurs sont injectés ou créés par défaut (Pattern Strategy)
        self._calc_matiere = calc_matiere
        self._calc_ue = calc_ue or CalculateurUE()
        self._calc_semestre = calc_semestre or CalculateurSemestre()
        self._calc_annuel = calc_annuel or CalculateurAnnuel()

    def recalculer_pour_etudiant(self, etudiant_id: str) -> Dict[str, Any]:
        """
        Méthode principale appelée par les handlers et le CLI.
        Recalcule S5, S6 et l'Annuel dans une seule passe.
        """
        print(f"🔄 Recalcul complet pour l'étudiant {etudiant_id}...")
        
        # 1. Calcul Annuel (qui déclenche S5 et S6 internally)
        resultat = self.calculer_resultat_annuel(etudiant_id)
        
        # 2. Persistance des résultats semestriels et annuel
        # S5
        s5_data = resultat['semestre_1']
        moy_s5 = Moyenne(s5_data['moyenne_generale'], TypeCalculMoyenne.ARITHMETIQUE, s5_data)
        self._resultat_repo.save_semestre(ResultatSemestre(etudiant_id, 5, moy_s5))
        
        # S6
        s6_data = resultat['semestre_2']
        moy_s6 = Moyenne(s6_data['moyenne_generale'], TypeCalculMoyenne.ARITHMETIQUE, s6_data)
        self._resultat_repo.save_semestre(ResultatSemestre(etudiant_id, 6, moy_s6))
        
        # Annuel
        moy_ann = Moyenne(resultat['moyenne_annuelle'], TypeCalculMoyenne.ANNUEL, resultat)
        self._resultat_repo.save_annuel(ResultatAnnuel(etudiant_id, "2025-2026", moy_ann))
        
        # 3. Persistance des résultats d'UE
        for s_data in [s5_data, s6_data]:
            for ue_res in s_data['resultats_ues']:
                moy_ue = Moyenne(ue_res['moyenne_ue'], TypeCalculMoyenne.PONDEREE, ue_res)
                self._resultat_repo.save_ue(ResultatUE(etudiant_id, ue_res['ue_id'], moy_ue))

        print(f"✅ Recalcul terminé pour {etudiant_id}")
        return resultat

    def calculer_semestre_par_referentiel(self, etudiant_id: str, semestre_index: int) -> Dict[str, Any]:
        """
        Calcule les résultats d'un semestre en récupérant la structure depuis le référentiel.
        """
        ues = self._ue_repo.get_by_semestre(semestre_index)
        
        data_semestre = {
            'semestre': semestre_index,
            'ues': []
        }
        
        for ue in ues:
            matieres = self._matiere_repo.get_by_ue(ue.id)
            ue_data = {
                'id': ue.id,
                'code': ue.code,
                'libelle': ue.libelle,
                'credits': ue.credits,
                'matieres': [{'id': m.id, 'libelle': m.libelle, 'coefficient': m.coefficient} for m in matieres]
            }
            data_semestre['ues'].append(ue_data)
            
        return self.calculer_bulletin_semestre(etudiant_id, f"Semestre {semestre_index}", data_semestre)

    def calculer_resultat_annuel(self, etudiant_id: str, s1_index: int = 5, s2_index: int = 6) -> Dict[str, Any]:
        """
        Calcule le résultat annuel basé sur deux semestres.
        Par défaut S5 et S6 pour LP ASUR.
        """
        res_s1 = self.calculer_semestre_par_referentiel(etudiant_id, s1_index)
        res_s2 = self.calculer_semestre_par_referentiel(etudiant_id, s2_index)
        
        contexte_annuel = {
            'moyenne_s1': Moyenne(res_s1['moyenne_generale'], TypeCalculMoyenne.ARITHMETIQUE, res_s1),
            'moyenne_s2': Moyenne(res_s2['moyenne_generale'], TypeCalculMoyenne.ARITHMETIQUE, res_s2)
        }
        
        moy_annuelle = self._calc_annuel.calculer(contexte_annuel)
        
        return {
            'etudiant_id': etudiant_id,
            'semestre_1': res_s1,
            'semestre_2': res_s2,
            'moyenne_annuelle': moy_annuelle.valeur,
            'mention': moy_annuelle.details.get('mention') if moy_annuelle.details else None,
            'total_credits': res_s1['total_credits'] + res_s2['total_credits']
        }

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
            matieres_details = []
            
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
                
                if self._calc_matiere and self._calc_matiere.peut_calculer(contexte_m):
                    moy_m = self._calc_matiere.calculer(contexte_m)
                    moyennes_matieres[m_id] = moy_m
                    coeffs_matieres[m_id] = m_data.get('coefficient', 1)
                    
                    matieres_details.append({
                        'id': m_id,
                        'libelle': m_data.get('libelle'),
                        'coefficient': coeffs_matieres[m_id],
                        'moyenne': moy_m.valeur,
                        'details': moy_m.details
                    })

            # Calcul de la moyenne d'UE
            contexte_ue = {
                'moyennes_matieres': moyennes_matieres,
                'coefficients_matieres': coeffs_matieres
            }
            moy_ue = self._calc_ue.calculer(contexte_ue)
            moyennes_ue_objs.append(moy_ue)
            
            resultats_ues.append({
                'ue_id': ue_data['id'],
                'code': ue_data.get('code'),
                'libelle': ue_data.get('libelle'),
                'credits_potentiels': ue_data['credits'],
                'moyenne_ue': moy_ue.valeur,
                'matieres': matieres_details
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
            val_res = validateur.valider(Moyenne(res['moyenne_ue'], TypeCalculMoyenne.PONDEREE, {}), moy_semestre)
            
            total_credits += val_res.credits_acquis
            res['statut'] = val_res.statut
            res['credits_acquis'] = val_res.credits_acquis
            details_validation.append(val_res)

        return {
            'etudiant_id': etudiant_id,
            'semestre': semestre_libelle,
            'moyenne_generale': moy_semestre.valeur,
            'total_credits': total_credits,
            'resultats_ues': resultats_ues
        }
