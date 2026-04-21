from typing import List, Optional
from domain.entities.resultat import ResultatUE, ResultatSemestre, ResultatAnnuel
from domain.value_objects.moyenne import Moyenne, TypeCalculMoyenne
from domain.repositories.i_resultat_repository import IResultatRepository
from ..django_models.models import ResultatUEModel, ResultatSemestreModel, ResultatAnnuelModel, EtudiantModel, UEModel

class SQLiteResultatRepository(IResultatRepository):
    """Implémentation du repository Résultats utilisant l'ORM Django (SQLite/Turso)."""

    def save_ue(self, resultat: ResultatUE) -> None:
        etudiant_model = EtudiantModel.objects.get(id=resultat._etudiant_id)
        ue_model = UEModel.objects.get(id=resultat._ue_id)
        
        ResultatUEModel.objects.update_or_create(
            etudiant=etudiant_model,
            ue=ue_model,
            defaults={
                'valeur_moyenne': resultat._moyenne.valeur,
                'details': resultat._moyenne.metadata
            }
        )

    def save_semestre(self, resultat: ResultatSemestre) -> None:
        etudiant_model = EtudiantModel.objects.get(id=resultat._etudiant_id)
        
        ResultatSemestreModel.objects.update_or_create(
            etudiant=etudiant_model,
            numero_semestre=resultat._semestre,
            defaults={
                'valeur_moyenne': resultat._moyenne.valeur,
                'details': resultat._moyenne.metadata
            }
        )

    def save_annuel(self, resultat: ResultatAnnuel) -> None:
        etudiant_model = EtudiantModel.objects.get(id=resultat._etudiant_id)
        
        ResultatAnnuelModel.objects.update_or_create(
            etudiant=etudiant_model,
            annee_academique=resultat._annee_academique,
            defaults={
                'valeur_moyenne': resultat._moyenne.valeur,
                'details': resultat._moyenne.metadata
            }
        )

    def get_par_etudiant_semestre(self, etudiant_id: str, semestre: int) -> Optional[ResultatSemestre]:
        try:
            model = ResultatSemestreModel.objects.get(etudiant_id=etudiant_id, numero_semestre=semestre)
            return ResultatSemestre(
                etudiant_id=model.etudiant.id,
                semestre=model.numero_semestre,
                moyenne=Moyenne(model.valeur_moyenne, TypeCalculMoyenne.PONDEREE, model.details),
                id=model.id
            )
        except ResultatSemestreModel.DoesNotExist:
            return None

    def get_par_etudiant_annuel(self, etudiant_id: str) -> Optional[ResultatAnnuel]:
        try:
            model = ResultatAnnuelModel.objects.filter(etudiant_id=etudiant_id).latest('created_at')
            return ResultatAnnuel(
                etudiant_id=model.etudiant.id,
                annee_academique=model.annee_academique,
                moyenne=Moyenne(model.valeur_moyenne, TypeCalculMoyenne.ARITHMETIQUE, model.details),
                id=model.id
            )
        except ResultatAnnuelModel.DoesNotExist:
            return None

    def obtenir_ue_details(self, etudiant_id: str, semestre: int) -> List[ResultatUE]:
        models = ResultatUEModel.objects.filter(etudiant_id=etudiant_id, ue__semestre__libelle=f"S{semestre}")
        # Note: Cette recherche par libelle S{semestre} dépend de comment les semestres sont nommés.
        # Idéalement, on filtrerait par semestre_id si disponible dans le domaine.
        return [
            ResultatUE(
                etudiant_id=m.etudiant.id,
                ue_id=m.ue.id,
                moyenne=Moyenne(m.valeur_moyenne, TypeCalculMoyenne.PONDEREE, m.details),
                id=m.id
            ) for m in models
        ]
