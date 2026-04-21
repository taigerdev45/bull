from typing import List, Optional
from domain.entities.personnel import Personnel
from domain.repositories.i_personnel_repository import IPersonnelRepository
from infrastructure.persistence.django_models.models import PersonnelModel

class DjangoPersonnelRepository(IPersonnelRepository):
    def save(self, personnel: Personnel) -> None:
        PersonnelModel.objects.update_or_create(
            id=personnel.id,
            defaults={
                'nom': personnel._nom,
                'prenom': personnel._prenom,
                'email': personnel._email,
                'role': personnel._role,
                'numero_telephone': personnel._numero_telephone,
                'user_id': personnel._user_id,
                'derniere_connexion': personnel._derniere_connexion
            }
        )

    def get_by_id(self, personnel_id: str) -> Optional[Personnel]:
        try:
            model = PersonnelModel.objects.get(id=personnel_id)
            return self._to_entity(model)
        except PersonnelModel.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[Personnel]:
        try:
            model = PersonnelModel.objects.get(email=email)
            return self._to_entity(model)
        except PersonnelModel.DoesNotExist:
            return None

    def list_all(self) -> List[Personnel]:
        models = PersonnelModel.objects.all()
        return [self._to_entity(m) for m in models]

    def delete(self, personnel_id: str) -> None:
        PersonnelModel.objects.filter(id=personnel_id).delete()

    def _to_entity(self, model: PersonnelModel) -> Personnel:
        return Personnel(
            nom=model.nom,
            prenom=model.prenom,
            email=model.email,
            role=model.role,
            numero_telephone=model.numero_telephone,
            derniere_connexion=model.derniere_connexion.isoformat() if model.derniere_connexion else None,
            user_id=model.user_id,
            id=model.id
        )
