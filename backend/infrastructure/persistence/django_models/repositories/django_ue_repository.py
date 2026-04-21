from typing import List, Optional
from domain.entities.ue import UE
from domain.repositories.i_ue_repository import IUERepository
from infrastructure.persistence.django_models.models import UEModel, SemestreModel

class DjangoUERepository(IUERepository):
    def save(self, ue: UE) -> None:
        semestre = SemestreModel.objects.get(id=ue._semestre_id)
        
        UEModel.objects.update_or_create(
            id=ue.id,
            defaults={
                'code': ue.code,
                'libelle': ue.libelle,
                'credits': ue.credits,
                'semestre': semestre
            }
        )

    def get_by_id(self, ue_id: str) -> Optional[UE]:
        try:
            model = UEModel.objects.get(id=ue_id)
            return self._to_entity(model)
        except UEModel.DoesNotExist:
            return None

    def list_all(self) -> List[UE]:
        models = UEModel.objects.all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: UEModel) -> UE:
        return UE(
            code=model.code,
            libelle=model.libelle,
            credits=model.credits,
            semestre_id=model.semestre.id,
            id=model.id
        )
