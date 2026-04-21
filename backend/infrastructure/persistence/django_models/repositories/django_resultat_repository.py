from typing import List, Optional
from domain.entities.resultat import ResultatUE, ResultatSemestre, ResultatAnnuel
from domain.repositories.i_resultat_repository import IResultatRepository
from domain.value_objects.moyenne import Moyenne
from infrastructure.persistence.django_models.models import (
    ResultatUEModel, ResultatSemestreModel, ResultatAnnuelModel,
    EtudiantModel, UEModel
)

class DjangoResultatRepository(IResultatRepository):
    # Résultat UE
    def save_ue(self, resultat: ResultatUE) -> None:
        ResultatUEModel.objects.update_or_create(
            etudiant_id=resultat._etudiant_id,
            ue_id=resultat._ue_id,
            defaults={
                'valeur_moyenne': resultat._moyenne.valeur,
                'details': resultat._moyenne.details
            }
        )

    def obtenir_ue_details(self, etudiant_id: str, semestre: int) -> List[ResultatUE]:
        # On filtre par étudiant et on s'assure que l'UE appartient au semestre
        models = ResultatUEModel.objects.filter(
            etudiant_id=etudiant_id, 
            ue__semestre__id=semestre # semestre ici est souvent un ID dans le contexte du calcul
        )
        # Si semestre est un entier (numéro), on adapte
        if isinstance(semestre, int):
             models = ResultatUEModel.objects.filter(
                etudiant_id=etudiant_id, 
                ue__semestre__libelle__icontains=str(semestre)
            )

        return [ResultatUE(m.etudiant_id, m.ue_id, Moyenne(m.valeur_moyenne, m.details), m.id) for m in models]

    # Résultat Semestre
    def save_semestre(self, resultat: ResultatSemestre) -> None:
        ResultatSemestreModel.objects.update_or_create(
            etudiant_id=resultat._etudiant_id,
            numero_semestre=resultat._semestre,
            defaults={
                'valeur_moyenne': resultat._moyenne.valeur,
                'details': resultat._moyenne.details
            }
        )

    def get_par_etudiant_semestre(self, etudiant_id: str, semestre: int) -> Optional[ResultatSemestre]:
        try:
            model = ResultatSemestreModel.objects.get(etudiant_id=etudiant_id, numero_semestre=semestre)
            return ResultatSemestre(model.etudiant_id, model.numero_semestre, Moyenne(model.valeur_moyenne, model.details), model.id)
        except ResultatSemestreModel.DoesNotExist:
            return None

    # Résultat Annuel
    def save_annuel(self, resultat: ResultatAnnuel) -> None:
        ResultatAnnuelModel.objects.update_or_create(
            etudiant_id=resultat._etudiant_id,
            annee_academique=resultat._annee_academique,
            defaults={
                'valeur_moyenne': resultat._moyenne.valeur,
                'details': resultat._moyenne.details
            }
        )

    def get_par_etudiant_annuel(self, etudiant_id: str) -> Optional[ResultatAnnuel]:
        try:
            # On prend le plus récent résultat annuel pour cet étudiant
            model = ResultatAnnuelModel.objects.filter(etudiant_id=etudiant_id).latest('created_at')
            return ResultatAnnuel(model.etudiant_id, model.annee_academique, Moyenne(model.valeur_moyenne, model.details), model.id)
        except ResultatAnnuelModel.DoesNotExist:
            return None
            
    def delete_all_for_etudiant(self, etudiant_id: str) -> None:
        ResultatUEModel.objects.filter(etudiant_id=etudiant_id).delete()
        ResultatSemestreModel.objects.filter(etudiant_id=etudiant_id).delete()
        ResultatAnnuelModel.objects.filter(etudiant_id=etudiant_id).delete()
