from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        role_attr = str(getattr(request.user, 'role', '')).lower().strip()
        role_auth = str(request.auth.get('role', '') if isinstance(request.auth, dict) else '').lower().strip()
        role = role_attr or role_auth
        is_auth = request.user and request.user.is_authenticated
        res = is_auth and (role == 'super_admin' or request.user.is_superuser)
        if not res and is_auth:
            print(f"[PERM] IsSuperAdmin Denied for user {request.user.username} with role '{role}' (attr: '{role_attr}', auth: '{role_auth}')")
        return res

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        role_attr = str(getattr(request.user, 'role', '')).lower().strip()
        role_auth = str(request.auth.get('role', '') if isinstance(request.auth, dict) else '').lower().strip()
        role = role_attr or role_auth
        is_auth = request.user and request.user.is_authenticated
        res = is_auth and (role in ['super_admin', 'admin'] or request.user.is_superuser)
        if not res and is_auth:
            print(f"[PERM] IsAdmin Denied for user {request.user.username} with role '{role}'")
        return res

class IsSecretariat(permissions.BasePermission):
    def has_permission(self, request, view):
        role_attr = str(getattr(request.user, 'role', '')).lower().strip()
        role_auth = str(request.auth.get('role', '') if isinstance(request.auth, dict) else '').lower().strip()
        role = role_attr or role_auth
        is_auth = request.user and request.user.is_authenticated
        res = is_auth and (role in ['super_admin', 'admin', 'secretariat'] or request.user.is_superuser)
        if not res and is_auth:
            print(f"[PERM] IsSecretariat Denied for user {request.user.username} with role '{role}'")
        return res

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
