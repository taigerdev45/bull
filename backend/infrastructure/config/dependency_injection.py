from dependency_injector import containers, providers

from domain.repositories.i_evaluation_repository import IEvaluationRepository
from domain.repositories.i_etudiant_repository import IEtudiantRepository
from domain.repositories.i_resultat_repository import IResultatRepository
from domain.services.calculateurs.calculateur_matiere import CalculateurMatiere
from domain.services.orchestre_calcul import OrchestreCalcul
from infrastructure.persistence.sqlite.sqlite_evaluation_repository import SQLiteEvaluationRepository
from infrastructure.persistence.sqlite.sqlite_etudiant_repository import SQLiteEtudiantRepository
from infrastructure.persistence.sqlite.sqlite_resultat_repository import SQLiteResultatRepository
from infrastructure.persistence.sqlite.sqlite_absence_repository import SQLiteAbsenceRepository
from infrastructure.persistence.sqlite.sqlite_matiere_repository import SQLiteMatiereRepository
from infrastructure.persistence.sqlite.sqlite_ue_repository import SQLiteUERepository
from infrastructure.persistence.sqlite.sqlite_semestre_repository import SQLiteSemestreRepository
from infrastructure.persistence.sqlite.sqlite_enseignant_repository import SQLiteEnseignantRepository
from infrastructure.persistence.sqlite.sqlite_personnel_repository import SQLitePersonnelRepository
from infrastructure.persistence.sqlite.sqlite_audit_repository import SQLiteAuditRepository
from infrastructure.persistence.sqlite.sqlite_config_repository import SQLiteConfigRepository
from infrastructure.auth.supabase_auth_service import SupabaseAuthService

from application.services.evaluation_service import EvaluationService
from application.services.bulletin_service import BulletinService
from application.commands.creer_absence_command import CreerAbsenceHandler
from application.handlers.evaluation_command_handler import EvaluationCommandHandler
from application.handlers.resultat_query_handler import ResultatQueryHandler
from application.services.import_export_service import ImportExportService
from application.commands.importer_evaluations_command import ImporterEvaluationsHandler
from infrastructure.parsers.openpyxl_parser import OpenpyxlParser
from infrastructure.generators.excel_generator import ExcelGenerator
from domain.services.penalites.penalite_service import PenaliteService
from application.services.audit_service import AuditService
from domain.events.handlers.audit_log_handler import AuditLogHandler
from application.commands.create_staff_command import CreateStaffHandler

class Store: # Placeholder to match existing structure if needed, but Container is the one used.
    pass

class Container(containers.DeclarativeContainer):
    """Conteneur d'injection de dépendances principal (Pattern Inversion of Control)."""
    
    # Configuration
    config = providers.Configuration()
    
    # Repositories (Abstractions - DAP/Turso)
    evaluation_repo = providers.Factory(SQLiteEvaluationRepository)
    etudiant_repo = providers.Factory(SQLiteEtudiantRepository)
    resultat_repo = providers.Factory(SQLiteResultatRepository)
    absence_repo = providers.Factory(SQLiteAbsenceRepository)
    matiere_repo = providers.Factory(SQLiteMatiereRepository)
    ue_repo = providers.Factory(SQLiteUERepository)
    audit_repo = providers.Factory(SQLiteAuditRepository)
    semestre_repo = providers.Factory(SQLiteSemestreRepository)
    enseignant_repo = providers.Factory(SQLiteEnseignantRepository)
    personnel_repo = providers.Factory(SQLitePersonnelRepository)
    auth_service = providers.Singleton(SupabaseAuthService)
    config_repo = providers.Singleton(SQLiteConfigRepository)
    
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
        ue_repo=ue_repo,
        matiere_repo=matiere_repo,
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
        resultat_repo=resultat_repo,
        orchestrateur=orchestre_calcul
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

    create_staff_handler = providers.Factory(
        CreateStaffHandler,
        personnel_repo=personnel_repo,
        auth_service=auth_service
    )
