from typing import List, Optional
from domain.entities.ue import UE
from domain.repositories.i_ue_repository import IUERepository
from ..django_models.models import UEModel, SemestreModel

class SQLiteUERepository(IUERepository):
    """Implémentation du repository UE utilisant l'ORM Django (SQLite/Turso)."""

    def save(self, ue: UE) -> None:
        semestre_model = SemestreModel.objects.get(id=ue._semestre_id)
        
        defaults = {
            'code': ue.code,
            'libelle': ue.libelle,
            'credits': ue.credits,
            'semestre': semestre_model
        }
        
        UEModel.objects.update_or_create(
            id=ue.id,
            defaults=defaults
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
        ue = UE(
            code=model.code,
            libelle=model.libelle,
            credits=model.credits,
            semestre_id=model.semestre.id,
            id=model.id
        )
        # On pourrait ici charger aussi les matieres si l'entité UE en a besoin immédiatement
        return ue
