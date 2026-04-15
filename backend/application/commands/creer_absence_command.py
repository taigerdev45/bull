from dataclasses import dataclass
from datetime import date
from domain.entities.absence import Absence
from domain.repositories.i_absence_repository import IAbsenceRepository
from application.dto.absence_dto import AbsenceCreateDTO
from domain.services.orchestre_calcul import OrchestreCalcul

@dataclass(frozen=True)
class CreerAbsenceCommand:
    """Commande pour enregistrer une absence."""
    etudiant_id: str
    matiere_id: str
    nombre_heures: int
    date_absence: date
    saisie_par_id: str

class CreerAbsenceHandler:
    """Gestionnaire de la commande CreerAbsence."""

    def __init__(self, absence_repo: IAbsenceRepository, orchestrateur: OrchestreCalcul):
        self._absence_repo = absence_repo
        self._orchestrateur = orchestrateur

    def handle(self, command: CreerAbsenceCommand) -> str:
        # 1. Création de l'entité
        absence = Absence(
            etudiant_id=command.etudiant_id,
            matiere_id=command.matiere_id,
            nombre_heures=command.nombre_heures,
            date_absence=command.date_absence,
            saisie_par=command.saisie_par_id
        )

        # 2. Persistance
        absence_id = self._absence_repo.creer(absence)

        # 3. Recalcul de la moyenne (Pénalité mise à jour)
        # Note: L'orchestrateur s'occupe de la cascade (Matière -> UE -> Semestre)
        # Pour optimiser, on pourrait passer le contexte spécifique
        self._orchestrateur.calculer_bulletin_semestre(
            etudiant_id=command.etudiant_id,
            semestre_libelle="S5", # Idéalement dynamisé depuis le référentiel de la matière
            data={} # L'orchestrateur récupère les données via les repos injectés
        )

        return absence_id
