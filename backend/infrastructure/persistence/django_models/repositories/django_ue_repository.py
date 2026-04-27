from typing import List, Optional
from domain.entities.ue import UE
from domain.repositories.i_ue_repository import IUERepository
from infrastructure.persistence.django_models.models import UEModel, SemestreModel

class DjangoUERepository(IUERepository):
    def save(self, ue: UE) -> None:
        # Recherche robuste du semestre (par ID ou par Code)
        sem_id = str(ue._semestre_id)
        try:
            semestre = SemestreModel.objects.get(id=sem_id)
        except (SemestreModel.DoesNotExist, Exception):
            try:
                semestre = SemestreModel.objects.get(libelle=sem_id)
            except SemestreModel.DoesNotExist:
                semestre = SemestreModel.objects.create(
                    id=sem_id,
                    libelle=f"Semestre {sem_id}"[:200]
                )
        
        # Recherche de l'UE existante par ID ou par Code pour éviter les IntegrityError
        ue_model = UEModel.objects.filter(id=ue.id).first()
        if not ue_model:
            ue_model = UEModel.objects.filter(code=ue.code).first()
            
        if ue_model:
            ue_model.code = ue.code
            ue_model.libelle = ue.libelle
            ue_model.credits = ue.credits
            ue_model.semestre = semestre
            ue_model.save()
        else:
            UEModel.objects.create(
                id=ue.id,
                code=ue.code,
                libelle=ue.libelle,
                credits=ue.credits,
                semestre=semestre
            )

    def get_by_id(self, ue_id: str) -> Optional[UE]:
        try:
            model = UEModel.objects.get(id=ue_id)
            return self._to_entity(model)
        except UEModel.DoesNotExist:
            return None

    def list_all(self) -> List[UE]:
        models = UEModel.objects.all().select_related('semestre')
        return [self._to_entity(m) for m in models]

    def get_by_semestre(self, semestre_id: int) -> List[UE]:
        models = UEModel.objects.filter(semestre_id=str(semestre_id)).select_related('semestre')
        return [self._to_entity(m) for m in models]

    def delete(self, ue_id: str) -> None:
        UEModel.objects.filter(id=ue_id).delete()

    def _to_entity(self, model: UEModel) -> UE:
        return UE(
            code=model.code,
            libelle=model.libelle,
            credits=model.credits,
            semestre_id=model.semestre.id,
            id=model.id
        )
