from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        auth = request.auth if isinstance(request.auth, dict) else {}
        app_meta = auth.get('app_metadata', {})
        user_meta = auth.get('user_metadata', {})
        role = (auth.get('role') or app_meta.get('role') or user_meta.get('role', '')).lower().strip()
        
        is_auth = request.user and request.user.is_authenticated
        return is_auth and (role == 'super_admin' or request.user.is_superuser or request.user.email == 'taigermboumba@gmail.com')

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        auth = request.auth if isinstance(request.auth, dict) else {}
        app_meta = auth.get('app_metadata', {})
        user_meta = auth.get('user_metadata', {})
        role = (auth.get('role') or app_meta.get('role') or user_meta.get('role', '')).lower().strip()
        
        is_auth = request.user and request.user.is_authenticated
        return is_auth and (role in ['super_admin', 'admin'] or request.user.is_superuser or request.user.email == 'taigermboumba@gmail.com')

class IsSecretariat(permissions.BasePermission):
    def has_permission(self, request, view):
        auth = request.auth if isinstance(request.auth, dict) else {}
        app_meta = auth.get('app_metadata', {})
        user_meta = auth.get('user_metadata', {})
        role = (auth.get('role') or app_meta.get('role') or user_meta.get('role', '')).lower().strip()
        
        is_auth = request.user and request.user.is_authenticated
        return is_auth and (role in ['super_admin', 'admin', 'secretariat'] or request.user.is_superuser or request.user.email == 'taigermboumba@gmail.com')

class IsEnseignant(permissions.BasePermission):
    def has_permission(self, request, view):
        role_attr = str(getattr(request.user, 'role', '')).lower().strip()
        role_auth = str(request.auth.get('role', '') if isinstance(request.auth, dict) else '').lower().strip()
        role = role_attr or role_auth
        is_auth = request.user and request.user.is_authenticated
        res = is_auth and (role in ['super_admin', 'admin', 'enseignant'] or request.user.is_superuser)
        return res

class IsEtudiant(permissions.BasePermission):
    def has_permission(self, request, view):
        role_attr = str(getattr(request.user, 'role', '')).lower().strip()
        role_auth = str(request.auth.get('role', '') if isinstance(request.auth, dict) else '').lower().strip()
        role = role_attr or role_auth
        return request.user.is_authenticated and role == 'etudiant'
