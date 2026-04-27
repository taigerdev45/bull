from typing import List, Optional
from domain.entities.matiere import Matiere
from domain.value_objects.coefficient import Coefficient
from domain.repositories.i_matiere_repository import IMatiereRepository
from infrastructure.persistence.django_models.models import MatiereModel, UEModel

class DjangoMatiereRepository(IMatiereRepository):
    def save(self, matiere: Matiere) -> None:
        # Recherche robuste de l'UE (par ID ou par Code) pour éviter le crash 500
        try:
            ue = UEModel.objects.get(id=matiere._ue_id)
        except (UEModel.DoesNotExist, Exception):
            try:
                ue = UEModel.objects.get(code=matiere._ue_id)
            except UEModel.DoesNotExist:
                raise ValueError(f"Unité d'Enseignement '{matiere._ue_id}' introuvable.")
        
        MatiereModel.objects.update_or_create(
            id=matiere.id,
            defaults={
                'libelle': matiere.libelle,
                'coefficient': matiere.coefficient,
                'credits': matiere.credits,
                'ue': ue,
                'enseignant_id': matiere.enseignant_id
            }
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
        # On tente de filtrer par le user_id (UID Supabase) ou par l'ID technique
        models = MatiereModel.objects.filter(
            models.Q(enseignant__user_id=enseignant_id) | 
            models.Q(enseignant_id=enseignant_id)
        )
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
