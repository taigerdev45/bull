from dependency_injector import containers, providers
from infrastructure.persistence.firebase.connection import FirebaseConnection
from infrastructure.persistence.firebase.firebase_etudiant_repository import FirebaseEtudiantRepository
from infrastructure.persistence.firebase.firebase_evaluation_repository import FirebaseEvaluationRepository
from infrastructure.persistence.firebase.firebase_resultat_repository import FirebaseResultatRepository
from domain.services.calculateurs.calculateur_matiere import CalculateurMatiere
from domain.services.calculateurs.calculateur_ue import CalculateurUE
from domain.services.calculateurs.calculateur_semestre import CalculateurSemestre
from domain.services.orchestre_calcul import OrchestreCalcul
from application.services.evaluation_service import EvaluationService
from application.services.bulletin_service import BulletinService

class Container(containers.DeclarativeContainer):
    """Container d'injection de dépendances principal."""

    config = providers.Configuration()

    # Persistence
    firebase_connection = providers.Singleton(FirebaseConnection)
    etudiant_repo = providers.Factory(FirebaseEtudiantRepository, connection=firebase_connection)
    evaluation_repo = providers.Factory(FirebaseEvaluationRepository, connection=firebase_connection)
    resultat_repo = providers.Factory(FirebaseResultatRepository, connection=firebase_connection)

    # Domaine
    calc_matiere = providers.Factory(CalculateurMatiere)
    calc_ue = providers.Factory(CalculateurUE)
    calc_semestre = providers.Factory(CalculateurSemestre)
    orchestrateur = providers.Factory(
        OrchestreCalcul,
        calc_matiere=calc_matiere,
        calc_ue=calc_ue,
        calc_semestre=calc_semestre
    )

    # Application
    evaluation_service = providers.Factory(
        EvaluationService,
        evaluation_repo=evaluation_repo,
        orchestrateur=orchestrateur
    )
    
    bulletin_service = providers.Factory(
        BulletinService,
        etudiant_repo=etudiant_repo,
        resultat_repo=resultat_repo
    )
