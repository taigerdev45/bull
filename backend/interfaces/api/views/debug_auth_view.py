from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class DebugAuthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        auth = request.auth
        
        return Response({
            "is_authenticated": user.is_authenticated if user else False,
            "username": user.username if user else "None",
            "email": getattr(user, 'email', 'N/A'),
            "role": getattr(user, 'role', 'N/A'),
            "is_staff": getattr(user, 'is_staff', False),
            "is_superuser": getattr(user, 'is_superuser', False),
            "auth_type": str(type(auth)) if auth else "None",
            "headers": {k: v for k, v in request.META.items() if k.startswith('HTTP_AUTHORIZATION')}
        })
