from typing import Optional
from application.dto.bulletin_dto import BulletinDTO, EtudiantDTO
from domain.repositories.i_etudiant_repository import IEtudiantRepository
from domain.repositories.i_resultat_repository import IResultatRepository

class BulletinService:
    """Service de préparation des données pour les bulletins."""

    def __init__(self, etudiant_repo: IEtudiantRepository, resultat_repo: IResultatRepository):
        self.etudiant_repo = etudiant_repo
        self.resultat_repo = resultat_repo

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
        
        bulletin = BulletinDTO(
            etudiant=dto_etudiant,
            type_bulletin=type_bulletin,
            date_generation=datetime.now().isoformat(),
            saisie_par="SYSTEM"
        )

        if type_bulletin == "SEMESTRIEL":
            # Appel au repository resultat pour les détails
            pass
        elif type_bulletin == "ANNUEL":
            # Agrégation S5 + S6
            pass
            
        return bulletin
