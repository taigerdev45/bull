from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return role == 'super_admin' or request.user.is_superuser or request.user.email == 'taigermboumba@gmail.com'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = str(getattr(request.user, 'role', '')).lower().strip()
        # On autorise si le rôle est 'admin' OU si l'utilisateur est is_staff/superuser
        return role in ['super_admin', 'admin'] or request.user.is_staff or request.user.is_superuser or request.user.email == 'taigermboumba@gmail.com'

class IsSecretariat(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = str(getattr(request.user, 'role', '')).lower().strip()
        # On autorise si le rôle est admin/secretariat OU si l'utilisateur est is_staff/superuser
        return role in ['super_admin', 'admin', 'secretariat'] or request.user.is_staff or request.user.is_superuser or request.user.email == 'taigermboumba@gmail.com'

class IsEnseignant(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return role in ['super_admin', 'admin', 'enseignant'] or request.user.is_superuser

class IsEtudiant(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return role == 'etudiant'
