from typing import List, Optional
from domain.entities.matiere import Matiere
from domain.value_objects.coefficient import Coefficient
from domain.repositories.i_matiere_repository import IMatiereRepository
from ..django_models.models import MatiereModel, UEModel, EnseignantModel

class SQLiteMatiereRepository(IMatiereRepository):
    """Implémentation du repository Matière utilisant l'ORM Django (SQLite/Turso)."""

    def save(self, matiere: Matiere) -> None:
        # Récupération de l'instance UE correspondante
        ue_model = UEModel.objects.get(id=matiere._ue_id)
        
        defaults = {
            'libelle': matiere.libelle,
            'coefficient': matiere.coefficient,
            'credits': matiere.credits,
            'ue': ue_model,
        }
        
        if matiere.enseignant_id:
            enseignant_model = EnseignantModel.objects.get(id=matiere.enseignant_id)
            defaults['enseignant'] = enseignant_model

        MatiereModel.objects.update_or_create(
            id=matiere.id,
            defaults=defaults
        )

    def get_by_id(self, id: str) -> Optional[Matiere]:
        try:
            model = MatiereModel.objects.get(id=id)
            return self._to_entity(model)
        except MatiereModel.DoesNotExist:
            return None

    def get_by_libelle(self, libelle: str) -> Optional[Matiere]:
        try:
            model = MatiereModel.objects.get(libelle=libelle)
            return self._to_entity(model)
        except MatiereModel.DoesNotExist:
            return None

    def list_all(self) -> List[Matiere]:
        models = MatiereModel.objects.all()
        return [self._to_entity(m) for m in models]

    def get_by_ue(self, ue_id: str) -> List[Matiere]:
        models = MatiereModel.objects.filter(ue_id=ue_id)
        return [self._to_entity(m) for m in models]

    def get_by_enseignant(self, enseignant_id: str) -> List[Matiere]:
        models = MatiereModel.objects.filter(enseignant_id=enseignant_id)
        return [self._to_entity(m) for m in models]

    def attribuer_enseignant(self, matiere_id: str, enseignant_id: str) -> None:
        MatiereModel.objects.filter(id=matiere_id).update(enseignant_id=enseignant_id)

    def delete(self, id: str) -> None:
        MatiereModel.objects.filter(id=id).delete()

    def _to_entity(self, model: MatiereModel) -> Matiere:
        return Matiere(
            libelle=model.libelle,
            coefficient=Coefficient(model.coefficient),
            credits=model.credits,
            ue_id=model.ue.id,
            enseignant_id=model.enseignant.id if model.enseignant else None,
            id=model.id
        )
