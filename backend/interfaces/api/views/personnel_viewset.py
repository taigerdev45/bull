from rest_framework import viewsets, status
from rest_framework.response import Response
from interfaces.api.permissions.role_permissions import IsAdmin, IsSuperAdmin
from application.commands.create_staff_command import CreateStaffCommand, CreateStaffHandler
from infrastructure.config.dependency_injection import Container
from dependency_injector.wiring import inject, Provide

class PersonnelViewSet(viewsets.ViewSet):
    """ViewSet pour la gestion du personnel par les admins."""

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdmin()]
        return [IsSuperAdmin()] # Lister/Supprimer réservé au SuperAdmin

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
                "user_id": p._user_id
            } for p in personnels
        ])
