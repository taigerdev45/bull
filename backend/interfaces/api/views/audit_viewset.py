from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container
from datetime import datetime

@extend_schema(tags=['Administration'])
class AuditViewSet(viewsets.ViewSet):
    """ViewSet pour la consultation des logs d'audit."""

    @inject
    def __init__(self, audit_service=Provide[Container.audit_service], **kwargs):
        super().__init__(**kwargs)
        self.audit_service = audit_service

    @action(detail=False, methods=['get'], url_path='etudiant/(?P<etudiant_id>[^/.]+)')
    def etudiant(self, request, etudiant_id=None):
        """Récupère l'audit pour un étudiant spécifique."""
        # Validation des permissions (simulée ici, devrait utiliser DRF permissions)
        # if not request.user.is_staff:
        #    return Response(status=status.HTTP_403_FORBIDDEN)

        params = {
            'action': request.query_params.get('action'),
            'date_debut': request.query_params.get('date_debut'),
            'date_fin': request.query_params.get('date_fin'),
        }

        logs = self.audit_service.obtenir_audit_etudiant(etudiant_id, params)
        return Response(logs)
