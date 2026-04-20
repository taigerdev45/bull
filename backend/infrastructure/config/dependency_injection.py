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
from application.handlers.evaluation_command_handler import EvaluationCommandHandler
from application.handlers.resultat_query_handler import ResultatQueryHandler
from application.services.import_export_service import ImportExportService
from application.commands.importer_evaluations_command import ImporterEvaluationsHandler
from infrastructure.parsers.openpyxl_parser import OpenpyxlParser
from infrastructure.generators.excel_generator import ExcelGenerator
from infrastructure.persistence.firebase.firebase_matiere_repository import FirebaseMatiereRepository
from infrastructure.persistence.firebase.firebase_config_repository import FirebaseConfigRepository
from domain.services.penalites.penalite_service import PenaliteService
from infrastructure.persistence.firebase.firebase_audit_repository import FirebaseAuditRepository
from application.services.audit_service import AuditService
from domain.events.handlers.audit_log_handler import AuditLogHandler
from infrastructure.persistence.firebase.firebase_ue_repository import FirebaseUERepository

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

    matiere_repo = providers.Factory(
        FirebaseMatiereRepository,
        connection=firebase_connection
    )

    ue_repo = providers.Factory(
        FirebaseUERepository,
        connection=firebase_connection
    )

    audit_repo = providers.Factory(
        FirebaseAuditRepository,
        connection=firebase_connection
    )

    config_repo = providers.Singleton(
        FirebaseConfigRepository,
        connection=firebase_connection
    )
    
    # Services métier (Domaine)
    penalite_service = providers.Factory(
        PenaliteService,
        absence_repo=absence_repo,
        config_repo=config_repo
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

    evaluation_command_handler = providers.Factory(
        EvaluationCommandHandler,
        evaluation_repo=evaluation_repo,
        orchestre_calcul=orchestre_calcul
    )

    resultat_query_handler = providers.Factory(
        ResultatQueryHandler,
        resultat_repo=resultat_repo,
        evaluation_repo=evaluation_repo
    )

    resultat_query_handler = providers.Factory(
        ResultatQueryHandler,
        resultat_repo=resultat_repo,
        evaluation_repo=evaluation_repo
    )

    excel_parser = providers.Factory(OpenpyxlParser)
    excel_generator = providers.Factory(ExcelGenerator)

    importer_evaluations_handler = providers.Factory(
        ImporterEvaluationsHandler,
        etudiant_repo=etudiant_repo,
        matiere_repo=matiere_repo,
        evaluation_repo=evaluation_repo
    )

    import_export_service = providers.Factory(
        ImportExportService,
        parser=excel_parser,
        generator=excel_generator,
        import_handler=importer_evaluations_handler
    )

    import_export_service = providers.Factory(
        ImportExportService,
        parser=excel_parser,
        generator=excel_generator,
        import_handler=importer_evaluations_handler
    )

    audit_service = providers.Factory(
        AuditService,
        audit_repo=audit_repo
    )

    audit_log_handler = providers.Singleton(
        AuditLogHandler,
        audit_service=audit_service
    )

    audit_log_handler = providers.Singleton(
        AuditLogHandler,
        audit_service=audit_service
    )
