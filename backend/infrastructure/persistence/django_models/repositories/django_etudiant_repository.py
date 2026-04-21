from typing import List, Optional
from domain.entities.etudiant import Etudiant
from domain.repositories.i_etudiant_repository import IEtudiantRepository
from infrastructure.persistence.django_models.models import EtudiantModel

class DjangoEtudiantRepository(IEtudiantRepository):
    def save(self, etudiant: Etudiant) -> None:
        EtudiantModel.objects.update_or_create(
            id=etudiant.id,
            defaults={
                'nom': etudiant.nom,
                'prenom': etudiant.prenom,
                'email': etudiant.email,
                'matricule': etudiant.matricule,
                'user_id': etudiant.user_id,
                'date_naissance': etudiant.date_naissance,
                'lieu_naissance': etudiant.lieu_naissance,
                'bac': etudiant.bac,
                'provenance': etudiant.provenance
            }
        )

    def get_by_id(self, id: str) -> Optional[Etudiant]:
        try:
            model = EtudiantModel.objects.get(id=id)
            return self._to_entity(model)
        except EtudiantModel.DoesNotExist:
            return None

    def get_by_matricule(self, matricule: str) -> Optional[Etudiant]:
        try:
            model = EtudiantModel.objects.get(matricule=matricule)
            return self._to_entity(model)
        except EtudiantModel.DoesNotExist:
            return None

    def list_all(self) -> List[Etudiant]:
        models = EtudiantModel.objects.all()
        return [self._to_entity(m) for m in models]

    def delete(self, id: str) -> None:
        EtudiantModel.objects.filter(id=id).delete()

    def _to_entity(self, model: EtudiantModel) -> Etudiant:
        return Etudiant(
            nom=model.nom,
            prenom=model.prenom,
            email=model.email,
            matricule=model.matricule,
            date_naissance=model.date_naissance,
            user_id=model.user_id,
            lieu_naissance=model.lieu_naissance,
            bac=model.bac,
            provenance=model.provenance,
            id=model.id
        )
