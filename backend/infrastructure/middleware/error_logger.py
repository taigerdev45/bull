import logging

logger = logging.getLogger(__name__)

class DRFErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 403:
            user = request.user
            auth = getattr(request, 'auth', 'None')
            role = getattr(user, 'role', 'N/A')
            is_staff = getattr(user, 'is_staff', False)
            is_active = getattr(user, 'is_active', False)
            email = getattr(user, 'email', 'N/A')
            
            log_msg = f"[403 FORBIDDEN] Path: {request.path} | Email: {email} | Role: {role} | IsStaff: {is_staff} | IsActive: {is_active}"
            logger.warning(log_msg)
            print(log_msg)
        return response
