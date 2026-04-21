from typing import List, Optional
from domain.entities.enseignant import Enseignant
from domain.repositories.i_enseignant_repository import IEnseignantRepository
from ..django_models.models import EnseignantModel

class SQLiteEnseignantRepository(IEnseignantRepository):
    """Implémentation du repository Enseignant utilisant l'ORM Django (SQLite/Turso)."""

    def save(self, enseignant: Enseignant) -> None:
        defaults = {
            'nom': enseignant._nom,
            'prenom': enseignant._prenom,
            'email': enseignant.email,
            'matricule': enseignant.matricule,
            'user_id': enseignant.user_id
        }
        EnseignantModel.objects.update_or_create(
            id=enseignant.id,
            defaults=defaults
        )

    def get_by_id(self, enseignant_id: str) -> Optional[Enseignant]:
        try:
            model = EnseignantModel.objects.get(id=enseignant_id)
            return self._to_entity(model)
        except EnseignantModel.DoesNotExist:
            return None

    def get_by_matricule(self, matricule: str) -> Optional[Enseignant]:
        try:
            model = EnseignantModel.objects.get(matricule=matricule)
            return self._to_entity(model)
        except EnseignantModel.DoesNotExist:
            return None

    def list_all(self) -> List[Enseignant]:
        models = EnseignantModel.objects.all()
        return [self._to_entity(m) for m in models]

    def delete(self, enseignant_id: str) -> None:
        EnseignantModel.objects.filter(id=enseignant_id).delete()

    def _to_entity(self, model: EnseignantModel) -> Enseignant:
        return Enseignant(
            nom=model.nom,
            prenom=model.prenom,
            email=model.email,
            matricule=model.matricule,
            user_id=model.user_id,
            id=model.id
        )
