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
            logger.warning(f"[403 FORBIDDEN] Path: {request.path} | User: {user} | Role: {role} | Auth: {auth}")
            print(f"[403 FORBIDDEN] Path: {request.path} | User: {user} | Role: {role}")
        return response
