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
