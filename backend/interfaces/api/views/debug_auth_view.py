from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from interfaces.api.permissions.supabase_auth import SupabaseAuthentication

class DebugAuthView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        auth = SupabaseAuthentication()
        auth_res = None
        try:
            auth_res = auth.authenticate(request)
        except Exception as e:
            auth_res = f"Auth Error: {str(e)}"
            
        role_detected = "N/A"
        if isinstance(auth_res, tuple):
            role_detected = getattr(auth_res[0], 'role', 'NO_ROLE_ON_USER')
            
        return Response({
            "user_in_request": str(request.user),
            "user_authenticated": request.user.is_authenticated if request.user else False,
            "user_role_in_request": getattr(request.user, 'role', 'N/A'),
            "manual_auth_check_role": role_detected,
            "manual_auth_check_full": str(auth_res)
        })
