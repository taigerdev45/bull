from typing import Optional, List, Dict, Any
from application.dto.bulletin_dto import BulletinDTO, EtudiantDTO
from application.dto.resultat_dto import ResultatSemestreDTO, ResultatAnnuelDTO, UEDetailDTO, MatiereDetailDTO
from domain.repositories.i_etudiant_repository import IEtudiantRepository
from domain.repositories.i_resultat_repository import IResultatRepository
from domain.services.orchestre_calcul import OrchestreCalcul

class BulletinService:
    """Service de préparation des données pour les bulletins."""

    def __init__(self, 
                 etudiant_repo: IEtudiantRepository, 
                 resultat_repo: IResultatRepository,
                 orchestrateur: OrchestreCalcul):
        self.etudiant_repo = etudiant_repo
        self.resultat_repo = resultat_repo
        self.orchestrateur = orchestrateur

    def préparer_donnees_bulletin(self, etudiant_id: str, type_bulletin: str, semestre: Optional[int] = None) -> Optional[BulletinDTO]:
        """Récupère et formate les données pour la génération d'un bulletin."""
        etudiant = self.etudiant_repo.get_by_id(etudiant_id)
        if not etudiant:
            return None
            
        from datetime import datetime
        dto_etudiant = EtudiantDTO(
            id=etudiant.id,
            nom=etudiant._nom,
            prenom=etudiant._prenom,
            matricule=etudiant._matricule,
            date_naissance=etudiant._date_naissance.isoformat()
        )
        
        bulletin_dto = BulletinDTO(
            etudiant=dto_etudiant,
            type_bulletin=type_bulletin,
            date_generation=datetime.now().isoformat(),
            saisie_par="SYSTEM"
        )

        if type_bulletin == "SEMESTRIEL":
            if not semestre:
                return None
            res = self.orchestrateur.calculer_semestre_par_referentiel(etudiant_id, semestre)
            bulletin_dto.resultat_semestre = self._map_to_semestre_dto(res)
            
        elif type_bulletin == "ANNUEL":
            # Par défaut S5 (semestre 5) et S6 (semestre 6) pour LP ASUR
            res_annuel = self.orchestrateur.calculer_resultat_annuel(etudiant_id)
            
            semestres_dtos = {
                "S5": self._map_to_semestre_dto(res_annuel['semestre_1']),
                "S6": self._map_to_semestre_dto(res_annuel['semestre_2'])
            }
            
            bulletin_dto.resultat_annuel = ResultatAnnuelDTO(
                etudiant_id=etudiant_id,
                moyenne_annuelle=res_annuel['moyenne_annuelle'],
                total_credits=res_annuel['total_credits'],
                decision="ADMIS" if res_annuel['moyenne_annuelle'] >= 10 else "AJOURNE",
                mention=res_annuel['mention'] or "Passable",
                semestres=semestres_dtos
            )
            
        return bulletin_dto

    def _map_to_semestre_dto(self, res: Dict[str, Any]) -> ResultatSemestreDTO:
        ues_dtos = []
        for ue in res['resultats_ues']:
            matieres_dtos = []
            for m in ue.get('matieres', []):
                matieres_dtos.append(MatiereDetailDTO(
                    id=m['id'],
                    libelle=m['libelle'],
                    coefficient=m['coefficient'],
                    moyenne=round(m['moyenne'], 2),
                    note_cc=m['details'].get('note_cc'),
                    note_examen=m['details'].get('note_examen'),
                    note_rattrapage=m['details'].get('note_rattrapage'),
                    penalite=m['details'].get('penalite', 0.0)
                ))
            
            ues_dtos.append(UEDetailDTO(
                id=ue['ue_id'],
                code=ue.get('code', ''),
                libelle=ue['libelle'],
                moyenne_ue=round(ue['moyenne_ue'], 2),
                statut=ue.get('statut', 'NON_ACQUISE'),
                credits_acquis=ue.get('credits_acquis', 0),
                compensee=ue.get('statut') == 'VAL_COMP',
                matieres=matieres_dtos
            ))
            
        return ResultatSemestreDTO(
            etudiant_id=res['etudiant_id'],
            semestre=int(res['semestre'].replace("Semestre ", "")) if "Semestre" in str(res['semestre']) else 1,
            moyenne_generale=round(res['moyenne_generale'], 2),
            credits_acquis=res['total_credits'],
            total_credits=sum(ue.get('credits_potentiels', 0) for ue in res['resultats_ues']),
            valide=res['moyenne_generale'] >= 10,
            ues=ues_dtos
        )
