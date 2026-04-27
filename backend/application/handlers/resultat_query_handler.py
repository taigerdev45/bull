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
        # Récupération des résultats du semestre
        from infrastructure.persistence.django_models.models import ResultatSemestreModel, ResultatUEModel, UEModel
        from django.db.models import Avg, Max, Min, Count
        
        qs = ResultatSemestreModel.objects.all().select_related('etudiant')
        if query.semestre:
            qs = qs.filter(numero_semestre=query.semestre)
            
        resultats = []
        somme_moyennes = 0
        nb_valide = 0
        
        # Pour les stats par UE
        ues_stats = {} # {ue_code: [moyennes]}
        
        # Pour la distribution des mentions
        mentions_dist = {
            "Excellent": 0,
            "Très Bien": 0,
            "Bien": 0,
            "Assez Bien": 0,
            "Passable": 0,
            "Ajourné": 0
        }

        for res in qs:
            etudiant = res.etudiant
            moyenne = res.valeur_moyenne
            somme_moyennes += moyenne
            
            if moyenne >= 10:
                nb_valide += 1
                
            # Mention simple
            if moyenne >= 16: mentions_dist["Très Bien"] += 1
            elif moyenne >= 14: mentions_dist["Bien"] += 1
            elif moyenne >= 12: mentions_dist["Assez Bien"] += 1
            elif moyenne >= 10: mentions_dist["Passable"] += 1
            else: mentions_dist["Ajourné"] += 1

            # Récupérer les moyennes d'UE
            ues_res = ResultatUEModel.objects.filter(etudiant=etudiant, ue__semestre_id=str(res.numero_semestre))
            
            detail_ues = {}
            for ur in ues_res:
                ue_code = ur.ue.code
                detail_ues[ue_code] = ur.valeur_moyenne
                if ue_code not in ues_stats:
                    ues_stats[ue_code] = []
                ues_stats[ue_code].append(ur.valeur_moyenne)

            resultats.append({
                "id": etudiant.matricule,
                "nom": etudiant.nom,
                "prenom": etudiant.prenom,
                "moyS5": moyenne,
                "credits": res.details.get('credits_acquis', 0),
                "decision": "Validé" if moyenne >= 10 else "Ajourné",
                "ues": detail_ues
            })
            
        # Calcul des stats par UE
        final_ues_stats = []
        for code, mops in ues_stats.items():
            if mops:
                final_ues_stats.append({
                    "code": code,
                    "moyenne": sum(mops) / len(mops),
                    "min": min(mops),
                    "max": max(mops),
                    "taux_reussite_ue": len([m for m in mops if m >= 10]) / len(mops) * 100
                })

        count = len(resultats)
        return {
            "resultats": resultats,
            "total_etudiants": count,
            "moyenne_classe": somme_moyennes / count if count else 0,
            "taux_reussite": (nb_valide / count * 100) if count else 0,
            "min_moyenne": min(r["moyS5"] for r in resultats) if resultats else 0,
            "max_moyenne": max(r["moyS5"] for r in resultats) if resultats else 0,
            "mentions_distribution": mentions_dist,
            "stats_par_ue": final_ues_stats
        }

    def lister_evaluations(self, query: ListerEvaluationsEtudiantQuery) -> List:
        # Récupération de l'historique des notes
        return self._evaluation_repo.obtenir_par_etudiant(query.etudiant_id)
