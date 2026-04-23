from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from interfaces.api.permissions.role_permissions import IsAdmin, IsSuperAdmin
from application.commands.create_staff_command import CreateStaffCommand, CreateStaffHandler
from infrastructure.config.dependency_injection import Container
from dependency_injector.wiring import inject, Provide

@extend_schema(tags=['Administration'])
class PersonnelViewSet(viewsets.ViewSet):
    """ViewSet pour la gestion du personnel par les admins."""

    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsSuperAdmin()]
        if self.action == 'create':
            return [IsAdmin()]
        return [permissions.AllowAny()]  # Lecture libre pour les admins connectés

    @inject
    def create(self, request, handler: CreateStaffHandler = Provide[Container.create_staff_handler]):
        data = request.data
        try:
            command = CreateStaffCommand(
                nom=data.get('nom'),
                prenom=data.get('prenom'),
                email=data.get('email'),
                password=data.get('password'),
                role=data.get('role')
            )
            
            user_id = handler.handle(command)
            return Response(
                {"message": "Membre du personnel créé.", "user_id": user_id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @inject
    def list(self, request, repo=Provide[Container.personnel_repo]):
        personnels = repo.list_all()
        return Response([
            {
                "id": p.id,
                "nom": p._nom,
                "prenom": p._prenom,
                "email": p._email,
                "role": p._role,
                "numero_telephone": p._numero_telephone,
                "user_id": p._user_id
            } for p in personnels
        ])

    @inject
    def destroy(self, request, pk=None, repo=Provide[Container.personnel_repo]):
        """Supprime un membre du personnel."""
        try:
            repo.delete(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
