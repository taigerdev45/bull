from dependency_injector import containers, providers
from infrastructure.persistence.firebase.connection import FirebaseConnection
from infrastructure.persistence.firebase.firebase_etudiant_repository import FirebaseEtudiantRepository
from infrastructure.persistence.firebase.firebase_evaluation_repository import FirebaseEvaluationRepository
from domain.services.calculateurs.calculateur_matiere import CalculateurMatiere
from domain.services.calculateurs.calculateur_ue import CalculateurUE
from domain.services.calculateurs.calculateur_semestre import CalculateurSemestre
from domain.services.orchestre_calcul import OrchestreCalcul

class Container(containers.DeclarativeContainer):
    """Container d'injection de dépendances principal."""

    config = providers.Configuration()

    # Persistence (Singletons)
    firebase_connection = providers.Singleton(FirebaseConnection)

    # Repositories (Factories)
    etudiant_repository = providers.Factory(
        FirebaseEtudiantRepository,
        connection=firebase_connection
    )

    evaluation_repository = providers.Factory(
        FirebaseEvaluationRepository,
        connection=firebase_connection
    )

    # Services Domaine (Calculateurs)
    calculateur_matiere = providers.Factory(CalculateurMatiere)
    calculateur_ue = providers.Factory(CalculateurUE)
    calculateur_semestre = providers.Factory(CalculateurSemestre)

    # Orchestration
    orchestre_calcul = providers.Factory(
        OrchestreCalcul,
        calc_matiere=calculateur_matiere,
        calc_ue=calculateur_ue,
        calc_semestre=calculateur_semestre
    )
