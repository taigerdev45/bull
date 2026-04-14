from typing import Optional
from application.dto.bulletin_dto import BulletinDTO, EtudiantDTO
from domain.repositories.i_etudiant_repository import IEtudiantRepository
from domain.repositories.i_resultat_repository import IResultatRepository

class BulletinService:
    """Service de préparation des données pour les bulletins."""

    def __init__(self, etudiant_repo: IEtudiantRepository, resultat_repo: IResultatRepository):
        self.etudiant_repo = etudiant_repo
        self.resultat_repo = resultat_repo

    def préparer_donnees_bulletin(self, etudiant_id: str, semestre: int) -> Optional[BulletinDTO]:
        """Récupère et formate les données pour la génération d'un bulletin."""
        etudiant = self.etudiant_repo.get_by_id(etudiant_id)
        if not etudiant:
            return None
            
        # Simulation de la récupération des résultats calculés
        # En production: self.resultat_repo.get_par_etudiant_semestre(...)
        
        dto_etudiant = EtudiantDTO(
            id=etudiant.id,
            nom=etudiant._nom,
            prenom=etudiant._prenom,
            matricule=etudiant._matricule,
            date_naissance=etudiant._date_naissance.isoformat()
        )
        
        return BulletinDTO(
            etudiant=dto_etudiant,
            semestre=semestre,
            moyenne_generale=0.0,
            total_credits=0,
            resultats_ues=[],
            mention="Ajourné",
            decision_jury="REDOUBLEMENT"
        )
