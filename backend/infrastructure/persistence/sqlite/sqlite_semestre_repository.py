from typing import List, Optional
from domain.entities.semestre import Semestre
from domain.repositories.i_semestre_repository import ISemestreRepository
from ..django_models.models import SemestreModel

class SQLiteSemestreRepository(ISemestreRepository):
    """Implémentation du repository Semestre utilisant l'ORM Django (SQLite/Turso)."""

    def save(self, semestre: Semestre) -> None:
        SemestreModel.objects.update_or_create(
            id=semestre.id,
            defaults={'libelle': semestre.libelle}
        )

    def get_by_id(self, semestre_id: str) -> Optional[Semestre]:
        try:
            model = SemestreModel.objects.get(id=semestre_id)
            return self._to_entity(model)
        except SemestreModel.DoesNotExist:
            return None

    def list_all(self) -> List[Semestre]:
        models = SemestreModel.objects.all()
        return [self._to_entity(m) for m in models]

    def delete(self, semestre_id: str) -> None:
        SemestreModel.objects.filter(id=semestre_id).delete()

    def _to_entity(self, model: SemestreModel) -> Semestre:
        return Semestre(
            libelle=model.libelle,
            id=model.id
        )
