from typing import List, Optional
from domain.entities.absence import Absence
from domain.repositories.i_absence_repository import IAbsenceRepository
from infrastructure.persistence.django_models.models import AbsenceModel, EtudiantModel, MatiereModel

class DjangoAbsenceRepository(IAbsenceRepository):
    def creer(self, absence: Absence) -> str:
        etudiant = EtudiantModel.objects.get(id=absence.etudiant_id)
        matiere = MatiereModel.objects.get(id=absence.matiere_id)
        
        model = AbsenceModel.objects.create(
            id=absence.id,
            etudiant=etudiant,
            matiere=matiere,
            heures=absence.nombre_heures,
            date_absence=absence.date_absence
        )
        return model.id

    def modifier(self, absence: Absence) -> None:
        AbsenceModel.objects.filter(id=absence.id).update(
            heures=absence.nombre_heures,
            date_absence=absence.date_absence
        )

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
        from django.db.models import Sum
        result = AbsenceModel.objects.filter(etudiant_id=etudiant_id, matiere_id=matiere_id).aggregate(total=Sum('heures'))
        return int(result['total'] or 0)

    def supprimer(self, absence_id: str) -> None:
        AbsenceModel.objects.filter(id=absence_id).delete()

    def _to_entity(self, model: AbsenceModel) -> Absence:
        return Absence(
            etudiant_id=model.etudiant.id,
            matiere_id=model.matiere.id,
            nombre_heures=int(model.heures),
            date_absence=model.date_absence,
            saisie_par="système",
            id=model.id
        )
