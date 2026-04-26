from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

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
            "is_authenticated": user.is_authenticated,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "claims": getattr(user, 'supabase_claims', {})
        })
