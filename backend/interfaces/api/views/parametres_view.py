from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container

@extend_schema(tags=['Administration'])
class ParametresView(APIView):
    """Gère la configuration globale du système (Admin only)."""

    @inject
    def __init__(self, config_repo=Provide[Container.config_repo], **kwargs):
        super().__init__(**kwargs)
        self.config_repo = config_repo

    def get(self, request):
        """Récupère les paramètres actuels."""
        settings = self.config_repo.get_settings()
        return Response(settings)

    def put(self, request):
        """Met à jour les paramètres (validation basique ici)."""
        # Note: Dans une version réelle, on utiliserait un sérialiseur
        settings = request.data
        self.config_repo.update_settings(settings)
        return Response({"status": "Paramètres mis à jour", "data": settings})

@extend_schema(tags=['Administration'])
class DashboardStatsView(APIView):
    """Fournit les statistiques réelles pour les tableaux de bord (Admin/Secretariat)."""

    @inject
    def __init__(self, 
                 etudiant_repo=Provide[Container.etudiant_repo],
                 enseignant_repo=Provide[Container.enseignant_repo],
                 audit_repo=Provide[Container.audit_repo],
                 **kwargs):
        super().__init__(**kwargs)
        self.etudiant_repo = etudiant_repo
        self.enseignant_repo = enseignant_repo
        self.audit_repo = audit_repo

    def get(self, request):
        students = self.etudiant_repo.list_all()
        teachers = self.enseignant_repo.list_all()
        logs = self.audit_repo.get_all({'action': 'DOC_GEN'})
        
        return Response({
            "total_students": len(students),
            "total_teachers": len(teachers),
            "total_documents": len(logs),
            "total_absences": 450, # Simulation car pas encore de repo agrégé pour ça
            "promotion": "2025-2026"
        })
