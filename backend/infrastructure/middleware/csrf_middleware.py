from django.utils.deprecation import MiddlewareMixin

class DisableCSRFMiddleware(MiddlewareMixin):
    """
    Middleware pour désactiver la protection CSRF sur les endpoints d'API.
    Utile car l'API utilise des tokens Bearer (Supabase) qui sont protégés contre le CSRF.
    """
    def process_request(self, request):
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
