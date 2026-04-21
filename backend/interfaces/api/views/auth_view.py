from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from application.commands.register_user_command import RegisterUserCommand, RegisterUserHandler
from infrastructure.config.dependency_injection import Container
from dependency_injector.wiring import inject, Provide

class RegisterView(APIView):
    """View pour l'auto-inscription des étudiants et enseignants."""
    
    permission_classes = [] # Ouvert à tous pour l'inscription initiale

    @inject
    def post(self, request, handler: RegisterUserHandler = Provide[Container.register_user_handler]):
        data = request.data
        try:
            # Extraction et validation basique
            email = data.get('email')
            password = data.get('password')
            matricule = data.get('matricule')
            role = data.get('role')

            if not all([email, password, matricule, role]):
                return Response(
                    {"error": "Tous les champs (email, password, matricule, role) sont obligatoires."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            command = RegisterUserCommand(
                email=email,
                password=password,
                matricule=matricule,
                role=role
            )
            
            user_id = handler.handle(command)
            return Response(
                {"message": "Inscription réussie.", "user_id": user_id},
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
