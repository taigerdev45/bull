from typing import Optional
from domain.repositories.i_config_repository import IConfigRepository
from infrastructure.persistence.django_models.models import ParametreConfigModel

class DjangoConfigRepository(IConfigRepository):
    def get_value(self, key: str) -> Optional[str]:
        try:
            model = ParametreConfigModel.objects.get(cle=key)
            return model.valeur
        except ParametreConfigModel.DoesNotExist:
            return None

    def set_value(self, key: str, value: str, description: str = "") -> None:
        ParametreConfigModel.objects.update_or_create(
            cle=key,
            defaults={
                'valeur': str(value),
                'description': description
            }
        )
