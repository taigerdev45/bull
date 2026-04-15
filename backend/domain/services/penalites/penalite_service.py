from infrastructure.config.constants import PENALITE_PAR_HEURE
from domain.services.interfaces.i_penalite_service import IPenaliteService

class PenaliteService(IPenaliteService):
    """
    Service de calcul des pénalités selon les absences.
    Suit le principe de Responsabilité Unique (SRP).
    """

    def calculer(self, etudiant_id: str, matiere_id: str) -> float:
        """
        Calcule la pénalité. 
        Note: Pour l'instant retourne 0.0, peut être lié à un IAbsenceRepository plus tard.
        """
        # Logique future: absences = self._absence_repo.get_by_etudiant_matiere(etudiant_id, matiere_id)
        # return len(absences) * PENALITE_PAR_HEURE
        return 0.0
