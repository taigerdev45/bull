from typing import List, Optional
from domain.entities.enseignant import Enseignant
from domain.repositories.i_enseignant_repository import IEnseignantRepository
from infrastructure.persistence.django_models.models import EnseignantModel

class DjangoEnseignantRepository(IEnseignantRepository):
    def save(self, enseignant: Enseignant) -> None:
        EnseignantModel.objects.update_or_create(
            id=enseignant.id,
            defaults={
                'nom': enseignant.nom,
                'prenom': enseignant.prenom,
                'email': enseignant.email,
                'matricule': enseignant.matricule,
                'user_id': enseignant.user_id
            }
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
            id=model.id,
            matricule=model.matricule,
            user_id=model.user_id
        )

    def get_by_user_id(self, user_id: str) -> Optional[Enseignant]:
        try:
            model = EnseignantModel.objects.get(user_id=user_id)
            return self._to_entity(model)
        except EnseignantModel.DoesNotExist:
            return None
