from typing import List, Optional
from domain.entities.absence import Absence
from domain.repositories.i_absence_repository import IAbsenceRepository
from ..django_models.models import AbsenceModel, EtudiantModel, MatiereModel
from django.db.models import Sum

class SQLiteAbsenceRepository(IAbsenceRepository):
    """Implémentation du repository Absence utilisant l'ORM Django (SQLite/Turso)."""

    def creer(self, absence: Absence) -> str:
        etudiant_model = EtudiantModel.objects.get(id=absence.etudiant_id)
        matiere_model = MatiereModel.objects.get(id=absence.matiere_id)
        
        model = AbsenceModel.objects.create(
            id=absence.id,
            etudiant=etudiant_model,
            matiere=matiere_model,
            heures=absence.heures,
            date_absence=absence.date_absence,
            justifiee=absence.justifiee
        )
        return model.id

    def modifier(self, absence: Absence) -> None:
        AbsenceModel.objects.filter(id=absence.id).update(
            heures=absence.heures,
            date_absence=absence.date_absence,
            justifiee=absence.justifiee
        )

    def supprimer(self, absence_id: str) -> None:
        AbsenceModel.objects.filter(id=absence_id).delete()

    def obtenir_par_id(self, absence_id: str) -> Optional[Absence]:
        try:
            model = AbsenceModel.objects.get(id=absence_id)
            return self._to_entity(model)
        except AbsenceModel.DoesNotExist:
            return None

    def obtenir_par_etudiant(self, etudiant_id: str) -> List[Absence]:
        models = AbsenceModel.objects.filter(etudiant_id=etudiant_id)
        return [self._to_entity(m) for m in models]

    def obtenir_par_etudiant_matiere(self, etudiant_id: str, matiere_id: str) -> List[Absence]:
        models = AbsenceModel.objects.filter(etudiant_id=etudiant_id, matiere_id=matiere_id)
        return [self._to_entity(m) for m in models]

    def calculer_total_heures(self, etudiant_id: str, matiere_id: str) -> int:
        total = AbsenceModel.objects.filter(
            etudiant_id=etudiant_id, 
            matiere_id=matiere_id
        ).aggregate(total=Sum('heures'))['total'] or 0.0
        return int(total)

    def _to_entity(self, model: AbsenceModel) -> Absence:
        return Absence(
            etudiant_id=model.etudiant.id,
            matiere_id=model.matiere.id,
            heures=model.heures,
            date_absence=model.date_absence,
            justifiee=model.justifiee,
            id=model.id
        )
