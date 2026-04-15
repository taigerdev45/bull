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
        # Logique de chargement et mapping vers DTO
        pass

    def obtenir_resultat_annuel(self, etudiant_id: str) -> Optional[ResultatAnnuelDTO]:
        # Logique d'agrégation S5 + S6
        pass

    def executer_stats_query(self, query: ObtenirStatsPromotionQuery) -> Dict:
        # Calcul des stats promotionnelles
        return {
            "moyenne_classe": 0.0,
            "min": 0.0,
            "max": 0.0,
            "taux_reussite": 0.0
        }

    def lister_evaluations(self, query: ListerEvaluationsEtudiantQuery) -> List:
        # Récupération de l'historique des notes
        return self._evaluation_repo.obtenir_par_etudiant(query.etudiant_id)
