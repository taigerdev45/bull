from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from infrastructure.config.dependency_injection import Container
from dependency_injector.wiring import inject, Provide


class ChangePasswordView(APIView):
    """View pour permettre à un utilisateur connecté de modifier son mot de passe."""
    
    from rest_framework.permissions import IsAuthenticated
    permission_classes = [IsAuthenticated]

    @inject
    def post(self, request, auth_service=Provide[Container.auth_service]):
        data = request.data
        new_password = data.get('new_password')
        
        if not new_password:
            return Response(
                {"error": "Le champ 'new_password' est obligatoire."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # L'ID de l'utilisateur Firebase (UID) est stocké dans request.user.username par notre backend
            # grâce à FirebaseAuthentication
            uid = request.user.username
            auth_service.update_user_password(uid, new_password)
            
            return Response(
                {"message": "Mot de passe modifié avec succès."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Impossible de modifier le mot de passe : {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
