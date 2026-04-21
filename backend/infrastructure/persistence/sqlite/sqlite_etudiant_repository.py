from typing import List, Optional
from domain.entities.etudiant import Etudiant
from domain.repositories.i_etudiant_repository import IEtudiantRepository
from ..django_models.models import EtudiantModel
from datetime import date

class SQLiteEtudiantRepository(IEtudiantRepository):
    """Implémentation du repository Étudiant utilisant l'ORM Django (SQLite/Turso)."""

    def save(self, etudiant: Etudiant) -> None:
        defaults = {
            'nom': etudiant._nom,
            'prenom': etudiant._prenom,
            'email': etudiant.email,
            'matricule': etudiant.matricule,
            'user_id': etudiant.user_id,
            'date_naissance': etudiant._date_naissance,
            'lieu_naissance': etudiant._lieu_naissance,
            'bac': etudiant._bac,
            'provenance': etudiant._provenance,
        }
        EtudiantModel.objects.update_or_create(
            id=etudiant.id,
            defaults=defaults
        )

    def get_by_id(self, etudiant_id: str) -> Optional[Etudiant]:
        try:
            model = EtudiantModel.objects.get(id=etudiant_id)
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

    def delete(self, etudiant_id: str) -> None:
        EtudiantModel.objects.filter(id=etudiant_id).delete()

    def _to_entity(self, model: EtudiantModel) -> Etudiant:
        return Etudiant(
            nom=model.nom,
            prenom=model.prenom,
            matricule=model.matricule,
            email=model.email,
            date_naissance=model.date_naissance,
            user_id=model.user_id,
            lieu_naissance=model.lieu_naissance,
            bac=model.bac,
            provenance=model.provenance,
            id=model.id
        )
