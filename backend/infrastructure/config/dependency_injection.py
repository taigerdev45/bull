from dependency_injector import containers, providers

from domain.repositories.i_evaluation_repository import IEvaluationRepository
from domain.repositories.i_etudiant_repository import IEtudiantRepository
from domain.repositories.i_resultat_repository import IResultatRepository
from domain.repositories.i_absence_repository import IAbsenceRepository
from domain.repositories.i_matiere_repository import IMatiereRepository
from domain.repositories.i_ue_repository import IUERepository
from domain.repositories.i_semestre_repository import ISemestreRepository
from domain.repositories.i_enseignant_repository import IEnseignantRepository
from domain.repositories.i_personnel_repository import IPersonnelRepository
from domain.repositories.i_audit_repository import IAuditRepository
from domain.repositories.i_config_repository import IConfigRepository

from infrastructure.persistence.django_models.repositories.django_evaluation_repository import DjangoEvaluationRepository
from infrastructure.persistence.django_models.repositories.django_etudiant_repository import DjangoEtudiantRepository
from infrastructure.persistence.django_models.repositories.django_resultat_repository import DjangoResultatRepository
from infrastructure.persistence.django_models.repositories.django_absence_repository import DjangoAbsenceRepository
from infrastructure.persistence.django_models.repositories.django_matiere_repository import DjangoMatiereRepository
from infrastructure.persistence.django_models.repositories.django_ue_repository import DjangoUERepository
from infrastructure.persistence.django_models.repositories.django_semestre_repository import DjangoSemestreRepository
from infrastructure.persistence.django_models.repositories.django_enseignant_repository import DjangoEnseignantRepository
from infrastructure.persistence.django_models.repositories.django_personnel_repository import DjangoPersonnelRepository
from infrastructure.persistence.django_models.repositories.django_audit_repository import DjangoAuditRepository
from infrastructure.persistence.django_models.repositories.django_config_repository import DjangoConfigRepository

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
from domain.services.calculateurs.calculateur_matiere import CalculateurMatiere
from domain.services.orchestre_calcul import OrchestreCalcul

class Container(containers.DeclarativeContainer):
    """Conteneur d'injection de dépendances principal (Pattern Inversion of Control)."""
    
    # Configuration
    config = providers.Configuration()
    
    # Repositories (Implémentations Django/Supabase)
    evaluation_repo = providers.Factory(DjangoEvaluationRepository)
    etudiant_repo = providers.Factory(DjangoEtudiantRepository)
    resultat_repo = providers.Factory(DjangoResultatRepository)
    absence_repo = providers.Factory(DjangoAbsenceRepository)
    matiere_repo = providers.Factory(DjangoMatiereRepository)
    ue_repo = providers.Factory(DjangoUERepository)
    semestre_repo = providers.Factory(DjangoSemestreRepository)
    enseignant_repo = providers.Factory(DjangoEnseignantRepository)
    personnel_repo = providers.Factory(DjangoPersonnelRepository)
    audit_repo = providers.Factory(DjangoAuditRepository)
    config_repo = providers.Factory(DjangoConfigRepository)
    
    # Auth
    auth_service = providers.Singleton(SupabaseAuthService)
    
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
    
    # Orchestrateur
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
    
    audit_service = providers.Factory(
        AuditService,
        audit_repo=audit_repo
    )

    audit_log_handler = providers.Singleton(
        AuditLogHandler,
        audit_service=audit_service
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

    create_staff_handler = providers.Factory(
        CreateStaffHandler,
        personnel_repo=personnel_repo,
        auth_service=auth_service
    )
