from infrastructure.config.constants import PENALITE_PAR_HEURE
from domain.services.interfaces.i_penalite_service import IPenaliteService
from domain.repositories.i_absence_repository import IAbsenceRepository

class PenaliteService(IPenaliteService):
    """
    Service de calcul des pénalités selon les absences.
    Récupère les données via le repository des absences.
    """

    def __init__(self, absence_repo: IAbsenceRepository):
        self._absence_repo = absence_repo

    def calculer(self, etudiant_id: str, matiere_id: str) -> float:
        """
        Calcule la pénalité totale (0.01 pt par heure d'absence).
        """
        total_heures = self._absence_repo.calculer_total_heures(etudiant_id, matiere_id)
        return float(total_heures * PENALITE_PAR_HEURE)
