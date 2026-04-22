from typing import List, Dict, Optional
from domain.repositories.i_resultat_repository import IResultatRepository
from domain.repositories.i_evaluation_repository import IEvaluationRepository
from application.dto.resultat_dto import ResultatSemestreDTO, ResultatAnnuelDTO
from application.queries.lister_evaluations_etudiant_query import ListerEvaluationsEtudiantQuery
from application.queries.obtenir_stats_promotion_query import ObtenirStatsPromotionQuery

class ResultatQueryHandler:
    """Handler gérant les accès en lecture seule aux résultats."""

    def __init__(self, resultat_repo: IResultatRepository, evaluation_repo: IEvaluationRepository):
        self._resultat_repo = resultat_repo
        self._evaluation_repo = evaluation_repo

    def obtenir_resultat_semestre(self, etudiant_id: str, semestre: int) -> Optional[ResultatSemestreDTO]:
        resultat = self._resultat_repo.get_par_etudiant_semestre(etudiant_id, semestre)
        if not resultat:
            return None
        
        # Récupération des détails (Moyennes par UE)
        resultats_ues = self._resultat_repo.obtenir_ue_details(etudiant_id, semestre)
        
        ues_dto = []
        for res_ue in resultats_ues:
            # On pourrait enrichir ici avec le libellé de l'UE si besoin
            ues_dto.append({
                "id": res_ue._ue_id,
                "libelle": res_ue._moyenne.details.get('libelle', res_ue._ue_id),
                "moyenne_ue": res_ue._moyenne.valeur,
                "total_credits_ue": res_ue._moyenne.details.get('total_credits', 6),
                "credits_acquis": res_ue._moyenne.details.get('credits_acquis', 6 if res_ue._moyenne.valeur >= 10 else 0),
                "matieres": res_ue._moyenne.details.get('matieres', [])
            })

        return ResultatSemestreDTO(
            etudiant_id=etudiant_id,
            semestre=semestre,
            moyenne_generale=resultat._moyenne.valeur,
            mention=resultat._moyenne.details.get('mention', 'Passable'),
            rang=resultat._moyenne.details.get('rang', 'Non classé'),
            total_credits=resultat._moyenne.details.get('total_credits', 30),
            credits_acquis=resultat._moyenne.details.get('credits_acquis', 0),
            valide=resultat._moyenne.valeur >= 10,
            ues=ues_dto
        )

    def obtenir_resultat_annuel(self, etudiant_id: str) -> Optional[ResultatAnnuelDTO]:
        resultat = self._resultat_repo.get_par_etudiant_annuel(etudiant_id)
        if not resultat:
            return None
        
        return ResultatAnnuelDTO(
            etudiant_id=etudiant_id,
            annee=resultat._annee_academique,
            moyenne_annuelle=resultat._moyenne.valeur,
            mention=resultat._moyenne.details.get('mention', 'Passable'),
            rang_annuel=resultat._moyenne.details.get('rang', 'Non classé'),
            decision=resultat._moyenne.details.get('decision', 'ADMIS'),
            ues_annuel=resultat._moyenne.details.get('ues_annuel', [])
        )

    def executer_stats_query(self, query: ObtenirStatsPromotionQuery) -> Dict:
        # Simplification: on récupère tous les résultats du semestre
        # Une vraie implémentation utiliserait un service ou une vue SQL optimisée
        from infrastructure.persistence.django_models.models import ResultatSemestreModel
        
        qs = ResultatSemestreModel.objects.all()
        if query.semestre:
            qs = qs.filter(numero_semestre=query.semestre)
        
        # Pour les délibérations, on veut souvent la liste des étudiants avec leurs moyennes
        if query.promotion_id: # On simule le filtrage par promo via les étudiants
            pass # TODO: filtrer par promo_id
            
        resultats = []
        for res in qs:
            etudiant = res.etudiant
            resultats.append({
                "id": etudiant.matricule,
                "nom": etudiant.nom,
                "prenom": etudiant.prenom,
                "moyS5": res.valeur_moyenne,
                "credits": res.details.get('credits_acquis', 0),
                "decision": "Validé" if res.valeur_moyenne >= 10 else "Ajourné",
                "ue1": 12.0, # Mocks pour les détails UEs
                "ue2": 11.0
            })
            
        return {
            "resultats": resultats,
            "moyenne_classe": sum(r["moyS5"] for r in resultats) / len(resultats) if resultats else 0,
            "taux_reussite": (len([r for r in resultats if r["decision"] == "Validé"]) / len(resultats) * 100) if resultats else 0
        }

    def lister_evaluations(self, query: ListerEvaluationsEtudiantQuery) -> List:
        # Récupération de l'historique des notes
        return self._evaluation_repo.obtenir_par_etudiant(query.etudiant_id)
