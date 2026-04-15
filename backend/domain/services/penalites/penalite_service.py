from infrastructure.config.constants import PENALITE_PAR_HEURE
from domain.services.interfaces.i_penalite_service import IPenaliteService
from domain.repositories.i_absence_repository import IAbsenceRepository

class PenaliteService(IPenaliteService):
    """
    Service de calcul des pénalités selon les absences.
    Récupère les données via le repository des absences.
    """

    def __init__(self, absence_repo: IAbsenceRepository, config_repo: 'FirebaseConfigRepository'):
        self._absence_repo = absence_repo
        self._config_repo = config_repo

    def calculer(self, etudiant_id: str, matiere_id: str) -> float:
        """
        Calcule la pénalité totale selon le paramètre dynamique.
        """
        settings = self._config_repo.get_settings()
        valeur_penalite = settings.get('penalite_absence_par_heure', 0.01)
        total_heures = self._absence_repo.calculer_total_heures(etudiant_id, matiere_id)
        return float(total_heures * valeur_penalite)
