from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container
from interfaces.api.serializers.notification_serializer import NotificationSerializer

class NotificationViewSet(viewsets.ViewSet):
    """ViewSet pour gérer les notifications utilisateurs."""
    permission_classes = [permissions.IsAuthenticated]

    @inject
    def __init__(self, repo=Provide[Container.notification_repo], **kwargs):
        super().__init__(**kwargs)
        self.repo = repo

    def list(self, request):
        """Récupère les notifications de l'utilisateur connecté."""
        uid = getattr(request.user, 'uid', request.user.username)
        notifications = self.repo.list_by_user(uid)
        serializer = NotificationSerializer([n.to_dict() for n in notifications], many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        """Marque une notification comme lue."""
        self.repo.mark_as_read(pk)
        return Response({"status": "notification lue"})

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        """Marque toutes les notifications de l'utilisateur comme lues."""
        uid = getattr(request.user, 'uid', request.user.username)
        notifications = self.repo.list_by_user(uid, only_unread=True)
        for n in notifications:
            self.repo.mark_as_read(n.id)
        return Response({"status": "toutes les notifications lues"})

    def destroy(self, request, pk=None):
        """Supprime une notification."""
        self.repo.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
