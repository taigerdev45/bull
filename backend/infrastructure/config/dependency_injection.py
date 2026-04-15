from dependency_injector import containers, providers

from domain.repositories.i_evaluation_repository import IEvaluationRepository
from domain.repositories.i_etudiant_repository import IEtudiantRepository
from domain.repositories.i_resultat_repository import IResultatRepository
from domain.services.calculateurs.calculateur_matiere import CalculateurMatiere
from domain.services.orchestre_calcul import OrchestreCalcul
from infrastructure.persistence.firebase.firebase_evaluation_repository import FirebaseEvaluationRepository
from infrastructure.persistence.firebase.firebase_etudiant_repository import FirebaseEtudiantRepository
from infrastructure.persistence.firebase.firebase_resultat_repository import FirebaseResultatRepository
from infrastructure.persistence.firebase.connection import FirebaseConnection
from application.services.evaluation_service import EvaluationService
from application.services.bulletin_service import BulletinService
from infrastructure.persistence.firebase.firebase_absence_repository import FirebaseAbsenceRepository
from application.commands.creer_absence_command import CreerAbsenceHandler
from domain.services.penalites.penalite_service import PenaliteService

class Container(containers.DeclarativeContainer):
    """Conteneur d'injection de dépendances principal (Pattern Inversion of Control)."""
    
    # Configuration
    config = providers.Configuration()
    
    # Singletons
    firebase_connection = providers.Singleton(FirebaseConnection)
    
    # Repositories (Abstractions - DAP)
    evaluation_repo = providers.Factory(
        FirebaseEvaluationRepository,
        connection=firebase_connection
    )
    
    etudiant_repo = providers.Factory(
        FirebaseEtudiantRepository,
        connection=firebase_connection
    )
    
    resultat_repo = providers.Factory(
        FirebaseResultatRepository,
        connection=firebase_connection
    )
    
    absence_repo = providers.Factory(
        FirebaseAbsenceRepository,
        connection=firebase_connection
    )
    
    # Services métier (Domaine)
    penalite_service = providers.Factory(
        'domain.services.penalites.penalite_service.PenaliteService'
    )
    
    calculateur_matiere = providers.Factory(
        CalculateurMatiere,
        penalite_service=penalite_service
    )
    
    # Façade principale (Domaine)
    orchestre_calcul = providers.Factory(
        OrchestreCalcul,
        evaluation_repo=evaluation_repo,
        resultat_repo=resultat_repo,
        calc_matiere=calculateur_matiere
    )
    
    # Services applicatifs (Application)
    evaluation_service = providers.Factory(
        EvaluationService,
        evaluation_repo=evaluation_repo,
        orchestrateur=orchestre_calcul
    )
    
    bulletin_service = providers.Factory(
        BulletinService,
        etudiant_repo=etudiant_repo,
        resultat_repo=resultat_repo
    )
    
    creer_absence_handler = providers.Factory(
        CreerAbsenceHandler,
        absence_repo=absence_repo,
        orchestrateur=orchestre_calcul
    )
