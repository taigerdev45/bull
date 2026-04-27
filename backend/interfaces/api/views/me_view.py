from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from infrastructure.config.dependency_injection import Container
from dependency_injector.wiring import inject, Provide

class MeView(APIView):
    """Vue de diagnostic pour vérifier l'identité et le rôle de l'utilisateur."""
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Authentification'])
    def get(self, request):
        user = request.user
        return Response({
            "id": user.username,
            "email": user.email,
            "role": getattr(user, 'role', 'N/A'),
            "name": getattr(user, 'display_name', ''),
            "is_authenticated": user.is_authenticated,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "claims": getattr(user, 'supabase_claims', {})
        })

    @inject
    @extend_schema(tags=['Authentification'])
    def patch(self, request, auth_service=Provide[Container.auth_service]):
        """Met à jour les informations du profil de l'utilisateur connecté."""
        user = request.user
        data = request.data
        
        display_name = data.get('name')
        
        if not display_name:
            return Response(
                {"error": "Le champ 'name' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Mise à jour dans Supabase
            auth_service.update_user_metadata(user.username, {"display_name": display_name})
            
            return Response({
                "message": "Profil mis à jour avec succès",
                "name": display_name
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
